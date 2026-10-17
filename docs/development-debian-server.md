# Developing Inua on the Debian server

This machine is a server. Its XFCE desktop, X display, users' sessions and
system services are production: another person may be using them, and a
restart or logout breaks their work. Inua development here must be isolated.

## Absolute rules

- Never restart, stop, or log out the existing XFCE session, its X server,
  display manager, or `xfwm4`.
- Never use `pkill`/`killall` by program name for development cleanup. `pkill
  -x xfwm4`, for example, kills the real desktop's window manager. Stop only
  PIDs that the development script recorded.
- Never change the system's display manager, autologin, default session,
  packages needed by the server, or systemd units.
- Never install a session or desktop entry with `make install-session`, and
  never replace `~/.config/hypr` or the user's real Inua configuration.
- Do not run the shell against the server's X display (`DISPLAY=:20`). That
  would put Inua's bar and panels over the active XFCE desktop.
- Package installation is allowed only for test-only dependencies, without
  removing or upgrading the server's desktop packages:
  `weston`, `libgtk4-layer-shell0`.

## Toolchain

Go 1.26 is in the private toolchain cache downloaded by `GOTOOLCHAIN=auto`;
`~/.profile` puts it first in `PATH` for login shells.

```sh
cd ~/development/inua
go version                 # go1.26.0
go test ./internal/vm ./internal/hypr ./internal/shell ./internal/ui
go build -o bin/inua-shell ./cmd/inua-shell
go build -o bin/inua ./cmd/inua
```

## Isolated UI session

`scripts/test-headless.sh` runs a private Weston headless compositor, its own
Wayland socket and runtime directory, a private `HOME`, a separate
`XDG_RUNTIME_DIR`, and the inua instance `inua-headless`. It writes no Hyprland
configuration outside that private home and touches no system service.

```sh
scripts/test-headless.sh start
scripts/test-headless.sh status
scripts/test-headless.sh stop
```

Drive the UI through the private control socket:

```sh
export XDG_RUNTIME_DIR=$HOME/.local/state/inua-headless/run
export INUA_INSTANCE=inua-headless
bin/inua call shell state
bin/inua call launcher toggle
bin/inua call control toggle
bin/inua call settings open
bin/inua call launcher close
```

`stop` kills only the PIDs recorded by `start`, and prints the two processes it
stopped. If either the Weston or shell PID file is stale, inspect it before
doing anything by hand; never fall back to a name-based `pkill`.

Weston's headless backend does not provide `wlr-screencopy` or VNC, so this
workflow verifies state and interaction through the control socket, not a
screenshot. For visual verification, use a separate machine or a nested
compositor inside a session you own; never take over the server's X display.

## What can be checked without a display

- Unit tests for VM, Hyprland snapshot, shell state and UI packages.
- `go vet ./...`.
- A build of `bin/inua-shell` and `bin/inua`.
- The private headless session above, for startup and control-socket
  interactions.

## After a session

```sh
scripts/test-headless.sh stop
pgrep -x xfwm4              # must still show the server's window manager
pgrep -x xfce4-panel        # must still show the server's panel
```

If a test accidentally affected the real session, restore the process that
was stopped and its original arguments from its session environment; do not
reboot the machine.
