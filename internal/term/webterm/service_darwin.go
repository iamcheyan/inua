package webterm

import (
	"bytes"
	"context"
	"encoding/xml"
	"errors"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"
	"time"
)

// Label is the launchd agent inua-termd serve runs as. Its property list
// is in ~/Library/LaunchAgents while the Web Terminal is on, so launchd
// starts it again at login: on a Mac no shell calls AtLogin.
const Label = "io.github.lyricat.Inua.Term.Web"

// logHint is where the agent's output goes.
const logHint = "~/Library/Logs/inua-term-web.log"

// domain is the user's GUI domain, as launchctl names it.
func domain() string { return "gui/" + strconv.Itoa(os.Getuid()) }

func plistPath(home string) string {
	return filepath.Join(home, "Library", "LaunchAgents", Label+".plist")
}

// Running says whether the agent runs.
func Running(ctx context.Context) bool {
	out, err := exec.CommandContext(ctx, "launchctl", "print", domain()+"/"+Label).Output()
	return err == nil && running(out)
}

// running says whether launchctl print's output is of a job that runs.
func running(out []byte) bool {
	for _, l := range strings.Split(string(out), "\n") {
		if strings.TrimSpace(l) == "state = running" {
			return true
		}
	}
	return false
}

// launch writes the agent's property list and has launchd run it.
func launch(ctx context.Context, self, addr string) error {
	home, err := os.UserHomeDir()
	if err != nil {
		return err
	}
	path, log := plistPath(home), filepath.Join(home, "Library", "Logs", "inua-term-web.log")
	for _, dir := range []string{filepath.Dir(path), filepath.Dir(log)} {
		if err := os.MkdirAll(dir, 0o755); err != nil {
			return err
		}
	}
	// An agent starts in launchd's environment; inua-termd serve needs the
	// folder of the host's socket, and the PATH and language of the
	// sessions it starts.
	var env [][2]string
	for _, k := range []string{"XDG_RUNTIME_DIR", "TMPDIR", "PATH", "LANG", "LANGUAGE", "LC_ALL", "LC_MESSAGES"} {
		if v := os.Getenv(k); v != "" {
			env = append(env, [2]string{k, v})
		}
	}
	if err := os.WriteFile(path, plist(Label, []string{self, "serve", "--addr", addr}, env, log), 0o644); err != nil {
		return err
	}
	// The job Stop booted out may not be gone yet: launchctl then fails
	// with "Bootstrap failed: 5: Input/output error".
	deadline := time.Now().Add(3 * time.Second)
	for {
		out, err := exec.CommandContext(ctx, "launchctl", "bootstrap", domain(), path).CombinedOutput()
		if err == nil {
			break
		}
		if time.Now().After(deadline) || ctx.Err() != nil {
			if s := strings.TrimSpace(string(out)); s != "" {
				return errors.New(s)
			}
			return err
		}
		time.Sleep(200 * time.Millisecond)
	}
	// A job bootstrapped is spawned a moment later.
	for i := 0; i < 10 && !Running(ctx); i++ {
		time.Sleep(100 * time.Millisecond)
	}
	return nil
}

// Stop ends the agent and takes its property list away, so that it does
// not start at the next login.
func Stop(ctx context.Context) {
	exec.CommandContext(ctx, "launchctl", "bootout", domain()+"/"+Label).Run()
	if home, err := os.UserHomeDir(); err == nil {
		os.Remove(plistPath(home))
	}
}

// plist is the agent's property list: it runs args with env, starts at
// login, starts again 3 seconds after a failure (not after an exit that
// went well) and writes its output to log.
func plist(label string, args []string, env [][2]string, log string) []byte {
	var b bytes.Buffer
	str := func(s string) {
		b.WriteString("<string>")
		xml.EscapeText(&b, []byte(s))
		b.WriteString("</string>")
	}
	key := func(k string) {
		b.WriteString("<key>")
		xml.EscapeText(&b, []byte(k))
		b.WriteString("</key>")
	}
	b.WriteString(`<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
`)
	key("Label")
	str(label)
	b.WriteString("\n")
	key("ProgramArguments")
	b.WriteString("<array>")
	for _, a := range args {
		str(a)
	}
	b.WriteString("</array>\n")
	key("EnvironmentVariables")
	b.WriteString("<dict>")
	for _, kv := range env {
		key(kv[0])
		str(kv[1])
	}
	b.WriteString("</dict>\n")
	key("RunAtLoad")
	b.WriteString("<true/>\n")
	key("KeepAlive")
	b.WriteString("<dict><key>SuccessfulExit</key><false/></dict>\n")
	key("ThrottleInterval")
	b.WriteString("<integer>3</integer>\n")
	key("ProcessType")
	b.WriteString("<string>Interactive</string>\n")
	key("StandardOutPath")
	str(log)
	b.WriteString("\n")
	key("StandardErrorPath")
	str(log)
	b.WriteString("\n</dict>\n</plist>\n")
	return b.Bytes()
}
