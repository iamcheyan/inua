package webterm

import (
	"context"
	"errors"
	"os"
	"os/exec"
	"strings"
)

// Unit is the systemd user unit inua-termd serve runs in.
const Unit = "inua-term-web.service"

// logHint is where the unit's output goes.
const logHint = "journalctl --user -u " + Unit

// Running says whether the unit runs.
func Running(ctx context.Context) bool {
	return exec.CommandContext(ctx, "systemctl", "--user", "is-active", "--quiet", Unit).Run() == nil
}

// launch runs self serve --addr addr in the unit.
func launch(ctx context.Context, self, addr string) error {
	exec.CommandContext(ctx, "systemctl", "--user", "reset-failed", Unit).Run()
	args := []string{"--user", "--unit=" + Unit, "--description=inua-term Web Terminal", "--collect", "--quiet",
		"--property=Restart=on-failure", "--property=RestartSec=3"}
	// The unit starts in the user manager's environment; inua-termd serve
	// needs the session's bus (the keyring) and runtime folder (the
	// host's socket), and the language.
	for _, k := range []string{"XDG_RUNTIME_DIR", "DBUS_SESSION_BUS_ADDRESS", "PATH", "LANG", "LANGUAGE", "LC_ALL", "LC_MESSAGES"} {
		if v := os.Getenv(k); v != "" {
			args = append(args, "--setenv="+k+"="+v)
		}
	}
	args = append(args, "--", self, "serve", "--addr", addr)
	if out, err := exec.CommandContext(ctx, "systemd-run", args...).CombinedOutput(); err != nil {
		if s := strings.TrimSpace(string(out)); s != "" {
			return errors.New(s)
		}
		return err
	}
	return nil
}

// Stop ends the unit.
func Stop(ctx context.Context) {
	exec.CommandContext(ctx, "systemctl", "--user", "stop", Unit).Run()
}
