package bootstrap

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"slices"
	"strings"
)

// ShellLine is what a Hyprland config needs to start the shell.
const ShellLine = "exec-once = inua-shell"

// ErrNoShell means a Hyprland config never starts inua-shell.
var ErrNoShell = errors.New("does not start inua-shell")

var (
	execRe       = regexp.MustCompile(`\binua-shell\b`)
	sourceRe     = regexp.MustCompile(`^source\s*=\s*(.+)$`)
	luaRequireRe = regexp.MustCompile(`(?:require|dofile)\s*\(?["']([^"']+)["']\)?`)
)

func resolveConfigPath(path string) string {
	if _, err := os.Stat(path); errors.Is(err, os.ErrNotExist) {
		if strings.HasSuffix(path, "hyprland.conf") {
			luaPath := strings.TrimSuffix(path, "hyprland.conf") + "hyprland.lua"
			if _, err := os.Stat(luaPath); err == nil {
				return luaPath
			}
		}
	}
	return path
}

// FindShellStart reports where a Hyprland config starts inua-shell, as
// "file:line", following `source =` lines and Lua `require` calls. It returns
// ErrNoShell if nothing does, and an error if the config cannot be read.
func FindShellStart(path string) (string, error) {
	path = resolveConfigPath(path)
	where := ""
	err := walk(path, func(file string, n int, line string) bool {
		if execRe.MatchString(line) {
			where = fmt.Sprintf("%s:%d", file, n)
			return false
		}
		return true
	})
	if err == nil && where == "" {
		err = ErrNoShell
	}
	return where, err
}

// ErrNoSource means a Hyprland config never sources inua.conf or requires inua.lua.
var ErrNoSource = errors.New("does not source inua.conf or require inua.lua")

// overrideRe matches the settings inua.conf writes; set again after the
// source line, they would win over inua's.
var overrideRe = regexp.MustCompile(`^(kb_options|sensitivity|accel_profile)\s*=`)

// FindSource reports where a Hyprland config sources the file target (or requires
// inua in Lua), as "file:line", and which later lines set what target sets (and so
// override it). It returns ErrNoSource if nothing sources target.
func FindSource(path, target string) (where string, overrides []string, err error) {
	path = resolveConfigPath(path)
	target, err = filepath.Abs(target)
	if err != nil {
		return "", nil, err
	}
	isLua := strings.HasSuffix(path, ".lua")
	err = walk(path, func(file string, n int, line string) bool {
		switch {
		case file == target:
		case where == "":
			if isLua {
				if m := luaRequireRe.FindStringSubmatch(line); m != nil {
					mod := m[1]
					if mod == "inua" || mod == "hypr.inua" || strings.Contains(mod, "inua.lua") {
						where = fmt.Sprintf("%s:%d", file, n)
					}
				}
			} else {
				if m := sourceRe.FindStringSubmatch(line); m != nil {
					matches, _ := filepath.Glob(expand(strings.TrimSpace(m[1]), filepath.Dir(file)))
					if slices.Contains(matches, target) {
						where = fmt.Sprintf("%s:%d", file, n)
					}
				}
			}
		case overrideRe.MatchString(line):
			overrides = append(overrides, fmt.Sprintf("%s:%d", file, n))
		}
		return true
	})
	if err == nil && where == "" {
		err = ErrNoSource
	}
	return where, overrides, err
}

// walk calls visit with each line of a Hyprland config, comments stripped
// and trimmed, in the order Hyprland reads them: a sourced file's lines
// come at its `source =` or `require` line. Files that cannot be read after the first
// are skipped, like a file sourced twice. visit returns false to stop.
func walk(path string, visit func(file string, n int, line string) bool) error {
	seen := map[string]bool{}
	var read func(path string, top bool) (bool, error)
	read = func(path string, top bool) (bool, error) {
		abs, err := filepath.Abs(path)
		if err != nil || seen[abs] {
			return true, err
		}
		seen[abs] = true
		f, err := os.Open(abs)
		if err != nil {
			if top {
				return false, err
			}
			return true, nil
		}
		defer f.Close()
		isLua := strings.HasSuffix(strings.ToLower(abs), ".lua")
		sc := bufio.NewScanner(f)
		for n := 1; sc.Scan(); n++ {
			line := strings.TrimSpace(stripComment(sc.Text(), isLua))
			if !visit(abs, n, line) {
				return false, nil
			}
			if isLua {
				if m := luaRequireRe.FindStringSubmatch(line); m != nil {
					mod := m[1]
					candidates := []string{
						filepath.Join(filepath.Dir(abs), mod+".lua"),
						filepath.Join(filepath.Dir(abs), strings.TrimPrefix(mod, "hypr.")+".lua"),
					}
					for _, c := range candidates {
						if _, err := os.Stat(c); err == nil {
							if more, err := read(c, false); !more || err != nil {
								return more, err
							}
							break
						}
					}
				}
				continue
			}
			m := sourceRe.FindStringSubmatch(line)
			if m == nil {
				continue
			}
			matches, _ := filepath.Glob(expand(strings.TrimSpace(m[1]), filepath.Dir(abs)))
			for _, src := range matches {
				if more, err := read(src, false); !more || err != nil {
					return more, err
				}
			}
		}
		return true, sc.Err()
	}
	_, err := read(path, true)
	return err
}

// stripComment drops comments (# for .conf, -- for .lua).
func stripComment(line string, isLua bool) string {
	if isLua {
		if idx := strings.Index(line, "--"); idx >= 0 {
			return line[:idx]
		}
		return line
	}
	for i := 0; i < len(line); i++ {
		if line[i] != '#' {
			continue
		}
		if i+1 < len(line) && line[i+1] == '#' {
			i++
			continue
		}
		return line[:i]
	}
	return line
}

func expand(p, dir string) string {
	if p == "~" || strings.HasPrefix(p, "~/") {
		if home, err := os.UserHomeDir(); err == nil {
			p = filepath.Join(home, p[1:])
		}
	}
	if !filepath.IsAbs(p) {
		p = filepath.Join(dir, p)
	}
	return p
}
