package style

import (
	"regexp"
	"strings"
)

var (
	defined = regexp.MustCompile(`@define-color\s+([A-Za-z0-9_-]+)`)
	token   = regexp.MustCompile(`@([A-Za-z_][A-Za-z0-9_-]*)`)
	comment = regexp.MustCompile(`(?s)/\*.*?\*/`)
)

// Scope gives one kind of window colours of its own on a display whose
// colour tokens are another theme's: GTK's @define-color is the
// display's, so the tokens defs defines are renamed with prefix, and css's
// rules, using them, are limited to the windows window matches (as
// "window.settings"). A selector of the window by its class alone
// (.settings …) is the window's; one of other windows (window.bar …)
// keeps its classes on window's, so it matches only a window of both; the
// keyframes are left to the display's sheet.
func Scope(defs, css, window, prefix string) string {
	names := map[string]bool{}
	for _, m := range defined.FindAllStringSubmatch(defs, -1) {
		names[m[1]] = true
	}
	rename := func(s string) string {
		s = defined.ReplaceAllStringFunc(s, func(d string) string {
			m := defined.FindStringSubmatch(d)
			return strings.TrimSuffix(d, m[1]) + prefix + m[1]
		})
		return token.ReplaceAllStringFunc(s, func(t string) string {
			if names[t[1:]] {
				return "@" + prefix + t[1:]
			}
			return t
		})
	}
	_, class, _ := strings.Cut(window, ".")
	class = "." + class // ".settings": a rule of the window by its class alone
	var b strings.Builder
	b.WriteString(rename(defs))
	b.WriteByte('\n')
	css = comment.ReplaceAllString(css, "")
	for {
		open := strings.IndexByte(css, '{')
		if open < 0 {
			break
		}
		end := blockEnd(css, open)
		sel, body := strings.TrimSpace(css[:open]), css[open:end]
		css = css[end:]
		if strings.HasPrefix(sel, "@") {
			continue // @keyframes
		}
		var out []string
		for _, s := range splitTop(sel) {
			if s = strings.TrimSpace(s); s == "" {
				continue
			}
			if rest, ok := strings.CutPrefix(s, window); ok && (rest == "" || strings.ContainsAny(rest[:1], ".:# >")) {
				out = append(out, s) // already window's
			} else if rest, ok := strings.CutPrefix(s, "window"); ok && (rest == "" || strings.ContainsAny(rest[:1], ".:# >")) {
				out = append(out, window+rest)
			} else if rest, ok := strings.CutPrefix(s, class); ok && (rest == "" || strings.ContainsAny(rest[:1], ".:# >")) {
				out = append(out, window+rest) // the window itself, by its class
			} else {
				out = append(out, window+" "+s)
			}
		}
		b.WriteString(strings.Join(out, ", "))
		b.WriteByte(' ')
		b.WriteString(rename(body))
		b.WriteByte('\n')
	}
	return b.String()
}

// blockEnd is the index just past the block whose '{' is at open.
func blockEnd(css string, open int) int {
	depth := 0
	for i := open; i < len(css); i++ {
		switch css[i] {
		case '{':
			depth++
		case '}':
			if depth--; depth == 0 {
				return i + 1
			}
		}
	}
	return len(css)
}

// splitTop splits a selector list at its commas, but not those in
// parentheses (:not(a, b)).
func splitTop(sel string) []string {
	var out []string
	depth, from := 0, 0
	for i, r := range sel {
		switch r {
		case '(':
			depth++
		case ')':
			depth--
		case ',':
			if depth == 0 {
				out = append(out, sel[from:i])
				from = i + 1
			}
		}
	}
	return append(out, sel[from:])
}
