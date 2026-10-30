package config

import (
	"os"
	"path/filepath"
	"reflect"
	"slices"
	"strings"
	"testing"
)

// fakeIconThemes points the icon folders at a temporary data directory
// with these index.theme files, by theme folder.
func fakeIconThemes(t *testing.T, themes map[string]string) {
	t.Helper()
	data := t.TempDir()
	t.Setenv("HOME", t.TempDir())
	t.Setenv("XDG_DATA_HOME", filepath.Join(data, "home"))
	t.Setenv("XDG_DATA_DIRS", filepath.Join(data, "system"))
	for name, index := range themes {
		dir := filepath.Join(data, "system", "icons", name)
		if err := os.MkdirAll(dir, 0o755); err != nil {
			t.Fatal(err)
		}
		if index != "" {
			if err := os.WriteFile(filepath.Join(dir, "index.theme"), []byte(index), 0o644); err != nil {
				t.Fatal(err)
			}
		}
	}
}

func TestIconThemes(t *testing.T) {
	icons := "[Icon Theme]\nName=%s\nDirectories=16x16/apps\n"
	fakeIconThemes(t, map[string]string{
		"Papirus":     strings.Replace(icons, "%s", "Papirus", 1),
		"numix":       strings.Replace(icons, "%s", "Numix Circle", 1),
		"Adwaita":     "[Icon Theme]\nName=Adwaita\nHidden=true\nDirectories=scalable/apps\n",
		"Hidden":      "[Icon Theme]\nName=Hidden\nHidden=true\nDirectories=scalable/apps\n",
		"DMZ-White":   "[Icon Theme]\nName=DMZ (White)\nInherits=DMZ\n", // cursors only
		"hicolor":     strings.Replace(icons, "%s", "Hicolor", 1),
		"inua-icons":  strings.Replace(icons, "%s", "inua", 1),
		"no-index":    "",
		"other-group": "[Desktop Entry]\nName=Nope\nDirectories=16x16\n",
	})
	want := []IconTheme{{"Adwaita", "Adwaita"}, {"numix", "Numix Circle"}, {"Papirus", "Papirus"}}
	if got := IconThemes(); !reflect.DeepEqual(got, want) {
		t.Errorf("IconThemes() = %v, want %v", got, want)
	}
	if !IsIconTheme("Papirus") || IsIconTheme("hicolor") || IsIconTheme("Hidden") {
		t.Error("IsIconTheme")
	}
}

func TestIconThemeSettings(t *testing.T) {
	fakeIconThemes(t, map[string]string{
		"Papirus": "[Icon Theme]\nName=Papirus\nDirectories=16x16/apps\n",
		"line":    "[Icon Theme]\nName=Line\nDirectories=16x16/apps\n",
	})
	c, w, err := Load(userFiles(t, "[style]\nicons = \"Papirus\"\napp_icons = \"Papirus\"\n"))
	if err != nil || len(w) != 0 {
		t.Fatalf("err=%v warnings=%v", err, w)
	}
	if c.Style.Icons != "Papirus" || c.Style.AppIcons != "Papirus" || c.IconThemeName() != "Papirus" || c.IconSetDir() != "" {
		t.Errorf("icons %q, app icons %q, theme %q, set %q", c.Style.Icons, c.Style.AppIcons, c.IconThemeName(), c.IconSetDir())
	}

	// A set of the user's wins over an installed theme of its name.
	c, _, err = Load(userFiles(t, "[style]\nicons = \"line\"\n"))
	if err != nil || c.IconThemeName() != "" || c.IconSetDir() == "" {
		t.Errorf("line: err=%v theme %q set %q", err, c.IconThemeName(), c.IconSetDir())
	}

	c, w, err = Load(userFiles(t, "[style]\nicons = \"Gone\"\napp_icons = \"Gone\"\n"))
	if err != nil || len(w) != 2 || c.Style.Icons != "phosphor" || c.Style.AppIcons != "" {
		t.Errorf("err=%v warnings=%v icons %q app icons %q", err, w, c.Style.Icons, c.Style.AppIcons)
	}
}

// inua's own app icons are offered among the themes once installed, the
// themes it writes for itself still not; until they are, the default
// answers the system's.
func TestObjectsTheme(t *testing.T) {
	fakeIconThemes(t, map[string]string{"inua-icons": "[Icon Theme]\nName=inua\nDirectories=16x16/apps\n"})
	if got := (Style{AppIcons: ObjectsTheme}).AppIconTheme(); got != "system" {
		t.Errorf("not installed: %q, want system", got)
	}
	fakeIconThemes(t, map[string]string{
		ObjectsTheme: "[Icon Theme]\nName=inua objects\nDirectories=scalable/apps\n",
		"inua-icons": "[Icon Theme]\nName=inua\nDirectories=16x16/apps\n",
	})
	if !IsIconTheme(ObjectsTheme) || IsIconTheme("inua-icons") {
		t.Errorf("themes offered: %v", IconThemes())
	}
	if got := (Style{AppIcons: ObjectsTheme}).AppIconTheme(); got != ObjectsTheme {
		t.Errorf("installed: %q", got)
	}
	if got := (Style{AppIcons: "system"}).AppIconTheme(); got != "system" {
		t.Errorf("system: %q", got)
	}
}

// inua's apps' own icons come from the app style once it is installed;
// the other apps' from app_icons, else the app style.
func TestInuaIconTheme(t *testing.T) {
	fakeIconThemes(t, map[string]string{ObjectsTheme: "[Icon Theme]\nName=inua objects\nDirectories=scalable/apps\n"})
	for style, want := range map[string]string{ObjectsTheme: ObjectsTheme, SoftTheme: ""} {
		if got := (Style{AppStyle: style}).InuaIconTheme(); got != want {
			t.Errorf("soft not installed, style %q: %q, want %q", style, got, want)
		}
	}
	if got := (Style{AppStyle: SoftTheme}).AppIconTheme(); got != "system" {
		t.Errorf("soft not installed: other apps %q, want system", got)
	}
	fakeIconThemes(t, map[string]string{
		ObjectsTheme: "[Icon Theme]\nName=inua objects\nDirectories=scalable/apps\n",
		SoftTheme:    "[Icon Theme]\nName=inua objects soft\nDirectories=scalable/apps\n",
		FlatTheme:    "[Icon Theme]\nName=inua objects flat\nDirectories=scalable/apps\n",
		"Papirus":    "[Icon Theme]\nName=Papirus\nDirectories=16x16/apps\n",
	})
	for _, c := range []struct {
		s          Style
		inua, rest string
	}{
		{Style{AppStyle: SoftTheme}, SoftTheme, SoftTheme},
		{Style{AppStyle: FlatTheme, AppIcons: "Papirus"}, FlatTheme, "Papirus"},
		{Style{AppStyle: ObjectsTheme, AppIcons: "system"}, ObjectsTheme, "system"},
	} {
		if got := c.s.InuaIconTheme(); got != c.inua {
			t.Errorf("%+v: inua's apps %q, want %q", c.s, got, c.inua)
		}
		if got := c.s.AppIconTheme(); got != c.rest {
			t.Errorf("%+v: other apps %q, want %q", c.s, got, c.rest)
		}
	}
}

// A theme's drawn apps are its files in scalable/apps, not its links and
// not inua's own apps.
func TestDrawnApps(t *testing.T) {
	fakeIconThemes(t, map[string]string{SoftTheme: "[Icon Theme]\nName=inua objects soft\nDirectories=scalable/apps\n"})
	apps := filepath.Join(os.Getenv("XDG_DATA_DIRS"), "icons", SoftTheme, "scalable", "apps")
	if err := os.MkdirAll(apps, 0o755); err != nil {
		t.Fatal(err)
	}
	for _, f := range []string{"vlc.svg", "firefox.svg", "io.github.lyricat.Inua.Files.svg", "notes.txt"} {
		if err := os.WriteFile(filepath.Join(apps, f), []byte("<svg/>"), 0o644); err != nil {
			t.Fatal(err)
		}
	}
	if err := os.Symlink("vlc.svg", filepath.Join(apps, "org.videolan.VLC.svg")); err != nil {
		t.Fatal(err)
	}
	if got := DrawnApps(SoftTheme); !slices.Equal(got, []string{"firefox", "vlc"}) {
		t.Errorf("DrawnApps = %q", got)
	}
	if got := DrawnApps("gone"); got != nil {
		t.Errorf("a theme not installed: %q", got)
	}
}
