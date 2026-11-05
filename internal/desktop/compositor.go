package desktop

import "strings"

// Wayfire reports whether the current session identifies itself as Wayfire.
// Wayfire does not set XDG_CURRENT_DESKTOP itself, so the session script
// does; a shell started inside an existing Wayfire session falls back to
// the compositor backend it detected.
func Wayfire() bool {
	for _, name := range CurrentDesktops() {
		if strings.EqualFold(name, "wayfire") {
			return true
		}
	}
	return false
}
