package lobbyservice

import (
	"context"
	"errors"
	"net"
	"os"
	"os/exec"
	"strings"
	"time"

	"github.com/lyricat/inua/internal/i18n"
)

// Status is how the unit stands now.
func Status(ctx context.Context) State {
	out, _ := exec.CommandContext(ctx, "systemctl", "--user", "show", "--property=ActiveState,SubState", Unit).Output()
	props := map[string]string{}
	for _, line := range strings.Split(string(out), "\n") {
		if k, v, ok := strings.Cut(strings.TrimSpace(line), "="); ok {
			props[k] = v
		}
	}
	switch props["ActiveState"] {
	case "active", "reloading":
		return Running
	case "activating":
		if props["SubState"] == "auto-restart" {
			return Failed
		}
		return Starting
	case "failed":
		return Failed
	}
	return Stopped
}

// Start runs inua-game-lobby in the unit, as c says, and waits for it to
// listen. One running already is stopped first: where it listens may
// have changed.
func Start(ctx context.Context, c Config) error {
	args, err := c.args()
	if err != nil {
		return err
	}
	local, _ := c.Local()
	self, err := program()
	if err != nil {
		return errors.New(i18n.T("inua-game-lobby is not installed"))
	}
	Stop(ctx)
	// Not collected when it fails, for the window to tell.
	run := []string{"--user", "--unit=" + Unit, "--description=inua Game Lobby", "--quiet",
		"--property=Restart=on-failure", "--property=RestartSec=3"}
	// The unit starts in the user manager's environment; the AI needs the
	// session's bus (the keyring, for its keys) and runtime folder, and
	// the pages the language.
	for _, k := range []string{"XDG_RUNTIME_DIR", "DBUS_SESSION_BUS_ADDRESS", "PATH", "LANG", "LANGUAGE", "LC_ALL", "LC_MESSAGES"} {
		if v := os.Getenv(k); v != "" {
			run = append(run, "--setenv="+k+"="+v)
		}
	}
	run = append(append(run, "--", self), args...)
	if out, err := exec.CommandContext(ctx, "systemd-run", run...).CombinedOutput(); err != nil {
		if s := strings.TrimSpace(string(out)); s != "" {
			return errors.New(s)
		}
		return err
	}
	for {
		if conn, err := net.DialTimeout("tcp", local, time.Second); err == nil {
			conn.Close()
			return nil
		}
		if s := Status(ctx); s != Running && s != Starting {
			return errors.New(i18n.Tf("inua-game-lobby stopped: %s says why", LogHint))
		}
		select {
		case <-ctx.Done():
			return ctx.Err()
		case <-time.After(200 * time.Millisecond):
		}
	}
}

// Stop ends the unit, and forgets that it failed.
func Stop(ctx context.Context) {
	exec.CommandContext(ctx, "systemctl", "--user", "stop", Unit).Run()
	exec.CommandContext(ctx, "systemctl", "--user", "reset-failed", Unit).Run()
}
