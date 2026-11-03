package style

import (
	"regexp"
	"strings"
)

var fontFamily = regexp.MustCompile(`font-family\s*:\s*([^;}]*[^;}\s])`)

// SystemFonts gives a style sheet a Mac's own fonts for the families
// inua's styles name, which a Mac does not have: each font-family list
// becomes the system's monospace (a list naming one), serif (a list
// ending in serif) or sans-serif. CoreText falls back for CJK as the
// system does.
func SystemFonts(css string) string {
	return fontFamily.ReplaceAllStringFunc(css, func(decl string) string {
		list := strings.ToLower(fontFamily.FindStringSubmatch(decl)[1])
		switch {
		case list == "inherit":
			return decl
		case strings.Contains(list, "mono"):
			return `font-family: "SF Mono", Menlo, monospace`
		case strings.HasSuffix(list, " serif") || strings.HasSuffix(list, ",serif"):
			return `font-family: "New York", "Hiragino Mincho ProN", serif`
		}
		return `font-family: ".AppleSystemUIFont", "Helvetica Neue", "Hiragino Sans", sans-serif`
	})
}

// fontStacks are the families Settings offers (config.Fonts), each written
// with the fallbacks that keep Latin, Chinese, Japanese and the terminal's
// glyphs whole. Every list ends with the generic family its kind needs.
var fontStacks = map[string]struct{ sans, serif, mono string }{
	"inua": {
		sans:  `"IBM Plex Sans", "Zen Kaku Gothic New", "Noto Sans CJK JP", "Noto Sans CJK SC", sans-serif`,
		serif: `"Shippori Mincho", "Noto Serif CJK JP", "Noto Serif CJK SC", serif`,
		mono:  `"Geist Mono", "IBM Plex Mono", "JetBrains Mono", monospace`,
	},
	"maple": {
		sans:  `"Maple Mono NF CN", "Noto Sans CJK JP", "Noto Sans CJK SC", sans-serif`,
		serif: `"Maple Mono NF CN", "Noto Serif CJK JP", "Noto Serif CJK SC", serif`,
		mono:  `"Maple Mono NF CN", "JetBrainsMono Nerd Font Mono", monospace`,
	},
	"noto-sans": {
		sans:  `"Noto Sans CJK JP", "Noto Sans CJK SC", "Noto Sans CJK TC", "Noto Sans", sans-serif`,
		serif: `"Noto Sans CJK JP", "Noto Sans CJK SC", "Noto Sans", sans-serif`,
		mono:  `"Noto Sans Mono CJK JP", "Noto Sans Mono", monospace`,
	},
	"noto-serif": {
		sans:  `"Noto Serif CJK JP", "Noto Serif CJK SC", "Noto Serif", serif`,
		serif: `"Noto Serif CJK JP", "Noto Serif CJK SC", "Noto Serif", serif`,
		mono:  `"Noto Sans Mono CJK JP", "Noto Sans Mono", monospace`,
	},
	"system": {
		sans:  `"Adwaita Sans", "Cantarell", "Noto Sans CJK JP", "Noto Sans CJK SC", sans-serif`,
		serif: `"Noto Serif CJK JP", "Noto Serif CJK SC", serif`,
		mono:  `"Adwaita Mono", "DejaVu Sans Mono", "Noto Sans Mono CJK JP", monospace`,
	},
}

// FontFamily rewrites every font-family list in css to the chosen family
// (style.font), keeping a list's kind: monospace stays monospace, a list
// ending in serif stays serif, and everything else is sans. A family not in
// fontStacks leaves css as it is.
func FontFamily(css, name string) string {
	stack, ok := fontStacks[name]
	if !ok {
		return css
	}
	return fontFamily.ReplaceAllStringFunc(css, func(decl string) string {
		list := strings.ToLower(fontFamily.FindStringSubmatch(decl)[1])
		switch {
		case list == "inherit":
			return decl
		case strings.Contains(list, "mono"):
			return `font-family: ` + stack.mono
		case strings.HasSuffix(list, " serif") || strings.HasSuffix(list, ",serif"):
			return `font-family: ` + stack.serif
		}
		return `font-family: ` + stack.sans
	})
}
