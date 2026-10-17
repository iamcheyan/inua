# Repository Guidelines

## Project Structure

inua is a Hyprland desktop shell written in Go and GTK4. Read `README.md` and `docs/architecture.md` first.

- `cmd/`: entry points for the shell, the command line, the light apps, the games, the assistant and the keyring service.
- `internal/shell`, `internal/apps`, `internal/games`: state and logic without GTK; their views are in `internal/ui`, `internal/appui` and `internal/gamesui`.
- `internal/hypr`, `internal/system` and others: Hyprland IPC, D-Bus and system services.
- `ui/`: Blueprint layouts, the generated `.ui` files, CSS, themes and icons.
- `config/`: sample configuration and desktop entries; `scripts/`: build and session tools; `website/`: the static website.
- Tests live next to the Go sources, named `*_test.go`.

## Build and Development Commands

Use Go 1.26 or later; running the UI needs Hyprland, GTK4 and gtk4-layer-shell.

- `make build`: builds the programs with `CGO_ENABLED=0` into `bin/`.
- `make test`: runs the Python session script tests, `go vet` and the Go tests with the race detector; needs a C compiler.
- `go test ./internal/shell`: checks one package only.
- `make generate`: compiles `.blp` into `.ui` with `blueprint-compiler`; after changing a layout, commit both.
- `make i18n`: gathers the translatable text into `po/inua.pot` and updates the catalogs in `internal/i18n/locales`.
- `make nested`: runs in a nested Hyprland window; `make run`: runs in the current Hyprland session.


### Rebuilding the running desktop shell
When a change must be visible in the current Hyprland session, build the shell binary first, then replace the running shell without leaving duplicate instances:

1. Before building, record the `inua-shell` PID and `/proc/<pid>/exe`; confirm the default IPC endpoint is `/run/user/$UID/inua/default.sock` and note whether `inua call shell state` responds.
2. Build the current source to the exact executable path used by that PID. For a local checkout build, use `go build -o bin/inua-shell ./cmd/inua-shell` and keep its required Go/GTK environment available. Do not copy a differently configured binary over the active path.
3. After the build succeeds, stop the one confirmed old `inua-shell` process with `TERM`, then start exactly one replacement from the current Hyprland session using the same environment, config path and UI directory. Do not use `shell restart` for a shell owned by a persistent terminal supervisor: `exec` can make that supervisor mark the service failed.
4. Wait for `ipc: serving on /run/user/$UID/inua/default.sock`, then verify `inua call shell state`, the new PID, `/proc/<pid>/exe`, expected bars/overview surfaces, and exactly one default `inua-shell` process. If the listener does not appear, inspect its startup log and process state; do not launch another copy while the first may still be initializing.
5. For repeated local builds, run the gitignored `./reload-shell` helper. It builds to a temporary file, replaces `bin/inua-shell` only after success, stops the one old shell, starts one replacement, and waits for IPC and process identity verification. It refuses multiple instances and refuses to start a duplicate when an old shell will not exit. Keep this helper local; do not add it to commits or PRs.

Do not report a desktop change as applied until the running executable and IPC state confirm that the rebuilt shell is active.

## Code Style and Architecture

Format Go with `gofmt` and follow standard naming: exported identifiers start with a capital letter, package names are short and lower case. Blueprint and CSS use two-space indentation, and colours refer to theme tokens.

Services and state must not import GTK. GTK calls run on the main thread; background results come back through the existing `gtkx.Post` or `gtkx.Call`. Windows, workspaces and focus follow the compositor's state. Implement the needed behaviour directly; do not add wrappers that only rename, or duplicate state.

Text the user reads is translatable: in Go through `internal/i18n` (`i18n.T`, `i18n.Tf`, `i18n.Nf`, `i18n.M`), in Blueprint as `_("…")`; run `make i18n` and commit `po/inua.pot` and the catalogs with the change. See `docs/i18n.md`.

Icons: when an icon is needed, use the SVG from Phosphor Icons (https://phosphoricons.com, MIT, the regular weight) by default. The shell's own icons are listed in `scripts/phosphor-icons.sh`, which copies them into `ui/icons/` under the freedesktop name the shell asks for (`NAME-symbolic.svg`); add a line to its list, run it, and commit the SVG. Use another source only when Phosphor has nothing fitting, and say so.

## Testing

Use the Go standard library's `testing`; name test functions `TestXxx`. Add behaviour regression tests for logic changes, using temporary directories, fake services and the private D-Bus of `internal/dbustest`; tests that need `dbus-daemon` are skipped without it. There is no coverage threshold.

Documentation, wording, simple logging, and visual or interaction changes to the UI do not get new automated tests. Check UI changes by hand in a nested session and note the steps. Do not verify an implementation by connecting to a database or starting a PostgreSQL container.

## Commits and Pull Requests

History uses both `fix(dock): ...`, `feat: ...`, `docs: ...` and "Component: what changed". A commit title says briefly what behaviour changed; keep each commit to one topic.

A PR explains the problem, the behaviour after the change and how it was verified; link the related issue if there is one. Attach screenshots for UI changes, and note any environment the change was not run in. When configuration or command behaviour changes, update the samples and documentation with it.

## Configuration and Operational Boundaries

Do not commit secrets, local user names or local absolute paths. Do not run binaries downloaded from the internet without explicit permission. Install and session-setup commands write to user or system directories; do not run them as ordinary build checks.
