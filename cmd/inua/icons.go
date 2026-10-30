package main

import (
	"fmt"
	"os"
	"path/filepath"
	"slices"
	"strings"

	"github.com/lyricat/inua/internal/config"
	"github.com/lyricat/inua/internal/desktop"
	"github.com/lyricat/inua/internal/i18n"
)

// cmdIcons answers `inua icons missing`: the apps installed, shown in the
// menus, whose icon inua's own theme (config.ObjectsTheme) does not draw
// yet, so they keep the inherited one. design/icons draws the next ones
// from it.
func cmdIcons(args []string) error {
	if len(args) != 1 || args[0] != "missing" {
		usage()
	}
	drawn := themeIcons(config.ObjectsTheme)
	if drawn == nil {
		return fmt.Errorf("%s is not installed (make install)", config.ObjectsTheme)
	}
	missing := missingIcons(desktop.Scan(desktop.DataDirs(), i18n.Lang()), drawn)
	for _, m := range missing {
		fmt.Printf("%s\t%s\n", m[1], m[0])
	}
	fmt.Fprintf(os.Stderr, "%d apps without an icon of %s\n", len(missing), config.ObjectsTheme)
	return nil
}

// themeIcons are the names an installed icon theme draws apps under, nil
// when it is not installed.
func themeIcons(theme string) map[string]bool {
	var drawn map[string]bool
	for _, d := range append([]string{filepath.Join(xdgDataHome(), "icons")}, dataDirs("icons")...) {
		files, err := filepath.Glob(filepath.Join(d, theme, "*", "apps", "*"))
		if err != nil || len(files) == 0 {
			continue
		}
		if drawn == nil {
			drawn = map[string]bool{}
		}
		for _, f := range files {
			drawn[strings.TrimSuffix(filepath.Base(f), filepath.Ext(f))] = true
		}
	}
	return drawn
}

// missingIcons are the entries shown in menus whose icon is a theme's
// name (not a file's path) the theme does not draw, as (name, icon) by
// name, each icon once.
func missingIcons(entries []*desktop.Entry, drawn map[string]bool) [][2]string {
	var out [][2]string
	seen := map[string]bool{}
	for _, e := range entries {
		if e.NoDisplay || e.Icon == "" || strings.ContainsRune(e.Icon, '/') || drawn[e.Icon] || seen[e.Icon] {
			continue
		}
		seen[e.Icon] = true
		out = append(out, [2]string{e.Name, e.Icon})
	}
	slices.SortFunc(out, func(a, b [2]string) int { return strings.Compare(strings.ToLower(a[0]), strings.ToLower(b[0])) })
	return out
}

func xdgDataHome() string {
	if d := os.Getenv("XDG_DATA_HOME"); d != "" {
		return d
	}
	home, _ := os.UserHomeDir()
	return filepath.Join(home, ".local", "share")
}

func dataDirs(sub string) []string {
	dirs := os.Getenv("XDG_DATA_DIRS")
	if dirs == "" {
		dirs = "/usr/local/share:/usr/share"
	}
	var out []string
	for _, d := range filepath.SplitList(dirs) {
		if d != "" {
			out = append(out, filepath.Join(d, sub))
		}
	}
	return out
}
