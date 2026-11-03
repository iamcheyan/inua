package ui

import (
	"os"
	"path/filepath"
)

// qtConfigPath is the KDE configuration Qt reads for its fonts and colours:
// $XDG_CONFIG_HOME/kdeglobals, else ~/.config/kdeglobals.
func qtConfigPath() string {
	if dir := os.Getenv("XDG_CONFIG_HOME"); dir != "" {
		return filepath.Join(dir, "kdeglobals")
	}
	home, err := os.UserHomeDir()
	if err != nil {
		return ""
	}
	return filepath.Join(home, ".config", "kdeglobals")
}
