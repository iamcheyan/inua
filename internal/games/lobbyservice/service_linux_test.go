package lobbyservice

import (
	"context"
	"net"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"testing"
	"time"
)

// fakeSystemd puts systemctl, systemd-run and inua-game-lobby on a PATH
// of their own: each writes its arguments to a log, and systemctl show
// says the state written in the state file. Nothing is started.
func fakeSystemd(t *testing.T, state string) (log, stateFile string) {
	t.Helper()
	dir := t.TempDir()
	log, stateFile = filepath.Join(dir, "log"), filepath.Join(dir, "state")
	os.WriteFile(stateFile, []byte(state), 0o644)
	script := func(name, body string) {
		os.WriteFile(filepath.Join(dir, name), []byte("#!/bin/sh\necho \""+name+" $*\" >> '"+log+"'\n"+body), 0o755)
	}
	script("systemctl", `case "$*" in *show*) cat '`+stateFile+`';; esac`+"\n")
	script("systemd-run", "")
	script("inua-game-lobby", "")
	t.Setenv("PATH", dir+":/usr/bin:/bin") // the fakes first; sh, cat
	return log, stateFile
}

func readLog(t *testing.T, log string) string {
	t.Helper()
	b, _ := os.ReadFile(log)
	return string(b)
}

// The unit's state as systemctl shows it.
func TestStatus(t *testing.T) {
	_, stateFile := fakeSystemd(t, "")
	for _, c := range []struct {
		show string
		want State
	}{
		{"ActiveState=active\nSubState=running\n", Running},
		{"ActiveState=activating\nSubState=start\n", Starting},
		{"ActiveState=activating\nSubState=auto-restart\n", Failed},
		{"ActiveState=failed\nSubState=failed\n", Failed},
		{"ActiveState=inactive\nSubState=dead\n", Stopped},
		{"", Stopped},
	} {
		os.WriteFile(stateFile, []byte(c.show), 0o644)
		if got := Status(context.Background()); got != c.want {
			t.Errorf("%q: %v, want %v", c.show, got, c.want)
		}
	}
}

// Start stops the unit that runs, then runs the lobby in a new one
// restarted on failure, listening on every address with the AI, and
// waits for it to listen.
func TestStart(t *testing.T) {
	log, _ := fakeSystemd(t, "ActiveState=activating\nSubState=start\n")
	t.Setenv("LANG", "fr_FR.UTF-8")
	l, err := net.Listen("tcp", "127.0.0.1:0") // the lobby, listening
	if err != nil {
		t.Fatal(err)
	}
	defer l.Close()
	port := l.Addr().(*net.TCPAddr).Port
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := Start(ctx, Config{Where: Network, Port: port}); err != nil {
		t.Fatal(err)
	}
	got := readLog(t, log)
	stop := strings.Index(got, "systemctl --user stop "+Unit)
	run := strings.Index(got, "systemd-run ")
	if stop < 0 || run < stop {
		t.Fatalf("not stopped before the run:\n%s", got)
	}
	line := got[run:]
	line = line[:strings.IndexByte(line, '\n')]
	for _, want := range []string{"--user", "--unit=" + Unit, "--property=Restart=on-failure", "--setenv=LANG=fr_FR.UTF-8",
		"inua-game-lobby -addr :" + strconv.Itoa(port), " -ai"} {
		if !strings.Contains(line, want) {
			t.Errorf("systemd-run without %q:\n%s", want, line)
		}
	}
	if strings.Contains(line, "--collect") {
		t.Error("a failed unit would be collected before the window tells")
	}
}

// A lobby that stops before it listens is an error, with where to look.
func TestStartFails(t *testing.T) {
	fakeSystemd(t, "ActiveState=failed\nSubState=failed\n")
	l, _ := net.Listen("tcp", "127.0.0.1:0")
	port := l.Addr().(*net.TCPAddr).Port
	l.Close() // nothing listens
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	err := Start(ctx, Config{Port: port})
	if err == nil || !strings.Contains(err.Error(), LogHint) {
		t.Fatalf("Start = %v", err)
	}
}

// Stop stops the unit and forgets its failure.
func TestStop(t *testing.T) {
	log, _ := fakeSystemd(t, "")
	Stop(context.Background())
	got := readLog(t, log)
	if !strings.Contains(got, "systemctl --user stop "+Unit) || !strings.Contains(got, "systemctl --user reset-failed "+Unit) {
		t.Errorf("log:\n%s", got)
	}
}

// Where the lobby listens and what this computer connects to.
func TestAddresses(t *testing.T) {
	c := Config{}
	if a, _ := c.Listen(); a != ":7340" {
		t.Errorf("Listen = %q", a)
	}
	if a, _ := c.Local(); a != "127.0.0.1:7340" {
		t.Errorf("Local = %q", a)
	}
	c.Port = 8000
	if a, _ := c.Listen(); a != ":8000" {
		t.Errorf("Listen = %q", a)
	}
	if u, err := c.Public(); err == nil && (!strings.HasPrefix(u, "http://") || !strings.HasSuffix(u, ":8000")) {
		t.Errorf("Public = %q", u)
	}
	c.Where = Tailscale
	if a, err := c.Local(); err == nil && !strings.HasPrefix(a, "100.") {
		t.Errorf("Local on the tailnet = %q", a)
	}
}
