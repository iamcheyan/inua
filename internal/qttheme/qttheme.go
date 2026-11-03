// Package qttheme keeps Qt applications on the desktop: their title bars,
// controls and text follow the shell's type and colours through the KDE
// configuration Qt reads (kdeglobals).
package qttheme

import (
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

// Fonts are the type families a Qt title bar and its menus use, by the shell's
// style.font choice. Qt names a family on its own, so each is a single family
// with the fallbacks that keep Chinese, Japanese and Korean whole.
var Fonts = map[string]string{
	"inua":       "IBM Plex Sans",
	"maple":      "Maple Mono NF CN",
	"noto-sans":  "Noto Sans CJK JP",
	"noto-serif": "Noto Serif CJK JP",
	"system":     "Adwaita Sans",
}

// family is the Qt family for the shell's choice, the shell's own stack when
// the choice is unknown.
func family(font string) string {
	if f, ok := Fonts[font]; ok {
		return f
	}
	return "IBM Plex Sans"
}

// qtFont is a family and size as kdeglobals writes a font: family, point
// size, then the style hints Qt stores beside them.
func qtFont(font string, size int) string {
	return family(font) + "," + strconv.Itoa(size) + ",-1,5,50,0,0,0,0,0"
}

// TextSize is the size Qt's own text takes from the shell's type scale: the
// bar sets 13 px at 100%, and a point is 4/3 of a pixel at 96 dpi.
func TextSize(textScale int) int {
	if textScale <= 0 {
		textScale = 100
	}
	return max(6, (13*textScale*3/4)/100)
}

// Apply writes the shell's type into the user's kdeglobals, so a Qt window's
// title bar and menus read at the shell's size. Only the keys named here are
// touched; the rest of the file is the user's.
func Apply(path, font string, textScale int) (bool, error) {
	size := TextSize(textScale)
	want := map[string]string{
		"General/font":                 qtFont(font, size),
		"General/menuFont":             qtFont(font, size),
		"General/toolBarFont":          qtFont(font, size),
		"General/smallestReadableFont": qtFont(font, max(6, size-1)),
		"WM/activeFont":                qtFont(font, size),
		"WM/inactiveFont":              qtFont(font, size),
	}
	old, err := os.ReadFile(path)
	if err != nil && !os.IsNotExist(err) {
		return false, err
	}
	content := string(old)
	changed := false
	for key, value := range want {
		section, name, _ := strings.Cut(key, "/")
		if setKey(&content, section, name, value) {
			changed = true
		}
	}
	if !changed {
		return false, nil
	}
	if err := os.MkdirAll(filepath.Dir(path), 0o755); err != nil {
		return false, err
	}
	file, err := os.CreateTemp(filepath.Dir(path), ".kdeglobals-*")
	if err != nil {
		return false, err
	}
	tmp := file.Name()
	if _, err := file.WriteString(content); err != nil {
		file.Close()
		os.Remove(tmp)
		return false, err
	}
	if err := file.Close(); err != nil {
		os.Remove(tmp)
		return false, err
	}
	if err := os.Rename(tmp, path); err != nil {
		os.Remove(tmp)
		return false, err
	}
	return true, nil
}

// setKey puts name=value in a section of an INI file, keeping every other
// line and the sections' order; it reports whether the text changed.
func setKey(content *string, section, name, value string) bool {
	lines := strings.Split(*content, "\n")
	start := -1
	for i, line := range lines {
		if strings.TrimSpace(line) == "["+section+"]" {
			start = i
			break
		}
	}
	if start < 0 {
		*content = strings.TrimRight(*content, "\n")
		if *content != "" {
			*content += "\n"
		}
		*content += "[" + section + "]\n" + name + "=" + value + "\n"
		return true
	}
	end := len(lines)
	for i := start + 1; i < len(lines); i++ {
		if strings.HasPrefix(strings.TrimSpace(lines[i]), "[") {
			end = i
			break
		}
	}
	for i := start + 1; i < end; i++ {
		key, _, ok := strings.Cut(lines[i], "=")
		if ok && strings.TrimSpace(key) == name {
			if lines[i] == name+"="+value {
				return false
			}
			lines[i] = name + "=" + value
			*content = strings.Join(lines, "\n")
			return true
		}
	}
	lines = append(lines[:end], append([]string{name + "=" + value}, lines[end:]...)...)
	*content = strings.Join(lines, "\n")
	return true
}
