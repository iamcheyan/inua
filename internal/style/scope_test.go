package style

import (
	"strings"
	"testing"
)

// The settings window takes the apps' theme on the shell's display: its
// tokens renamed, the rules limited to it.
func TestScope(t *testing.T) {
	defs := "@define-color app #000;\n@define-color glass alpha(@app, 0.84);\n"
	css := `/* a comment, { braces } */
button.outlined, popover.menu > contents { color: @t0; background: @app; }
window.settings .page { border: 1px solid @glass; }
.settings .index, .settings { color: @app; }
window.bar .island { color: @app; }
window { background: @app; }
.x:not(.a, .b) { color: @accent_unknown; }
@keyframes spin { from { opacity: 0; } }
`
	got := Scope(defs, css, "window.settings", "apps_")
	for _, want := range []string{
		"@define-color apps_app #000;",
		"@define-color apps_glass alpha(@apps_app, 0.84);",
		"window.settings button.outlined, window.settings popover.menu > contents { color: @t0; background: @apps_app; }",
		"window.settings .page { border: 1px solid @apps_glass; }",
		"window.settings.bar .island { color: @apps_app; }",
		"window.settings .index, window.settings { color: @apps_app; }",
		"window.settings { background: @apps_app; }",
		"window.settings .x:not(.a, .b) { color: @accent_unknown; }",
	} {
		if !strings.Contains(got, want) {
			t.Errorf("no %q in\n%s", want, got)
		}
	}
	if strings.Contains(got, "keyframes") || strings.Contains(got, "comment") {
		t.Errorf("keyframes or comments kept:\n%s", got)
	}
}
