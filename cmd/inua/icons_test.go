package main

import (
	"testing"

	"github.com/lyricat/inua/internal/desktop"
)

// Only apps shown in the menus, named by a theme's icon it lacks, once.
func TestMissingIcons(t *testing.T) {
	entries := []*desktop.Entry{
		{Name: "Firefox", Icon: "firefox"},
		{Name: "kitty", Icon: "kitty"},
		{Name: "Zed", Icon: "/opt/zed/zed.png"},
		{Name: "Helper", Icon: "helper", NoDisplay: true},
		{Name: "Alacritty", Icon: "Alacritty"},
		{Name: "XTerm", Icon: "mini.xterm"},
		{Name: "UXTerm", Icon: "mini.xterm"},
	}
	got := missingIcons(entries, map[string]bool{"firefox": true})
	want := [][2]string{{"Alacritty", "Alacritty"}, {"kitty", "kitty"}, {"XTerm", "mini.xterm"}}
	if len(got) != len(want) {
		t.Fatalf("got %v, want %v", got, want)
	}
	for i := range want {
		if got[i] != want[i] {
			t.Errorf("%d: got %v, want %v", i, got[i], want[i])
		}
	}
}
