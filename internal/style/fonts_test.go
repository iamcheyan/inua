package style

import (
	"strings"
	"testing"
)

func TestSystemFonts(t *testing.T) {
	for in, want := range map[string]string{
		`a { font-family: "Geist Mono", "IBM Plex Mono", monospace; }`:           `a { font-family: "SF Mono", Menlo, monospace; }`,
		`a { font-family: "JetBrainsMono Nerd Font Mono" }`:                      `a { font-family: "SF Mono", Menlo, monospace }`,
		`a { font-family: "IBM Plex Sans", "Zen Kaku Gothic New", sans-serif; }`: `a { font-family: ".AppleSystemUIFont", "Helvetica Neue", "Hiragino Sans", sans-serif; }`,
		`a { font-family: "Shippori Mincho", "Noto Serif CJK JP", serif; }`:      `a { font-family: "New York", "Hiragino Mincho ProN", serif; }`,
		`a { font-family: inherit; font-size: 12px; }`:                           `a { font-family: inherit; font-size: 12px; }`,
	} {
		if got := SystemFonts(in); got != want {
			t.Errorf("SystemFonts(%q)\n got %q\nwant %q", in, got, want)
		}
	}
}

func TestFontFamily(t *testing.T) {
	css := `a { font-family: "IBM Plex Sans", sans-serif; }` +
		`b { font-family: "Geist Mono", monospace; }` +
		`c { font-family: "Shippori Mincho", serif; }` +
		`d { font-family: inherit; }`
	got := FontFamily(css, "maple")
	for _, want := range []string{
		`a { font-family: "Maple Mono NF CN", "Noto Sans CJK JP", "Noto Sans CJK SC", sans-serif; }`,
		`b { font-family: "Maple Mono NF CN", "JetBrainsMono Nerd Font Mono", monospace; }`,
		`c { font-family: "Maple Mono NF CN", "Noto Serif CJK JP", "Noto Serif CJK SC", serif; }`,
		`d { font-family: inherit; }`,
	} {
		if !strings.Contains(got, want) {
			t.Errorf("FontFamily(maple) lacks %q:\n%s", want, got)
		}
	}
	if got := FontFamily(css, "unknown"); got != css {
		t.Errorf("an unknown family changed the sheet:\n%s", got)
	}
}
