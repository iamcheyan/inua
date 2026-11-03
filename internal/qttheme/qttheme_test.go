package qttheme

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestApplyWritesFontsAndKeepsTheRest(t *testing.T) {
	path := filepath.Join(t.TempDir(), "kdeglobals")
	before := "[Colors:Window]\nBackgroundNormal=1,2,3\n\n[General]\nColorScheme=BreezeDark\n\n[KDE]\nwidgetStyle=Breeze\n"
	if err := os.WriteFile(path, []byte(before), 0o644); err != nil {
		t.Fatal(err)
	}
	changed, err := Apply(path, "maple", 100)
	if err != nil || !changed {
		t.Fatalf("Apply = %v, %v; want changed", changed, err)
	}
	got, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	text := string(got)
	for _, want := range []string{
		"ColorScheme=BreezeDark",
		"widgetStyle=Breeze",
		"[WM]",
		"General/font",
	} {
		if want == "General/font" {
			if !strings.Contains(text, "font=Maple Mono NF CN,9,") {
				t.Errorf("the general font is not the chosen family at the shell's size:\n%s", text)
			}
			continue
		}
		if !strings.Contains(text, want) {
			t.Errorf("Apply dropped %q:\n%s", want, text)
		}
	}
	if !strings.Contains(text, "activeFont=Maple Mono NF CN,9,") {
		t.Errorf("the title bar's font did not follow:\n%s", text)
	}
	if changed, err = Apply(path, "maple", 100); err != nil || changed {
		t.Fatalf("second Apply = %v, %v; want unchanged", changed, err)
	}
	changed, err = Apply(path, "inua", 100)
	if err != nil || !changed {
		t.Fatalf("family change = %v, %v; want changed", changed, err)
	}
}

func TestApplyCreatesTheFile(t *testing.T) {
	path := filepath.Join(t.TempDir(), "nested", "kdeglobals")
	if changed, err := Apply(path, "inua", 125); err != nil || !changed {
		t.Fatalf("Apply = %v, %v", changed, err)
	}
	got, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	if !strings.Contains(string(got), "[General]") || !strings.Contains(string(got), "font=IBM Plex Sans,12,") {
		t.Errorf("a missing file was not written with the shell's type:\n%s", got)
	}
}
