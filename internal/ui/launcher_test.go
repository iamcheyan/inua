package ui

import (
	"slices"
	"testing"
)

// An app's icon given as a file goes by the snap's name, then the file's,
// in an icon theme: so a snap's (Chromium's) can follow the chosen one.
func TestFileIconNames(t *testing.T) {
	for path, want := range map[string][]string{
		"/snap/chromium/current/chromium.png":    {"chromium"},
		"/snap/spotify/89/usr/share/spotify.png": {"spotify"},
		"/snap/code/current/meta/gui/vscode.png": {"code", "vscode"},
		"/opt/zoom/zoom.svg":                     {"zoom"},
		"/usr/share/pixmaps/foo.xpm":             {"foo"},
	} {
		if got := fileIconNames(path); !slices.Equal(got, want) {
			t.Errorf("%s: %q, want %q", path, got, want)
		}
	}
}
