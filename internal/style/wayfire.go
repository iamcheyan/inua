package style

// WayfireControls returns the built-in GTK control skin for a Wayfire session.
// The default skin is already defined by ui/style.css; this loads after it.
func WayfireControls(name string) string {
	switch name {
	case "soft":
		return `
button.outlined, menubutton.outlined > button,
button.suggested-action, button.destructive-action, button.primary,
button.plain, button.tool,
entry, dropdown > button, spinbutton,
.settings entry, .settings dropdown > button, .settings spinbutton {
  border-radius: 6px;
}
switch, .settings switch, .settings switch slider {
  border-radius: 999px;
}
`
	case "outline":
		return `
button.outlined, menubutton.outlined > button,
button.suggested-action, button.destructive-action, button.primary,
button.plain, button.tool,
entry, dropdown > button, spinbutton,
.settings entry, .settings dropdown > button, .settings spinbutton,
switch, .settings switch, .settings switch slider {
  border-radius: 0;
}
button.outlined, menubutton.outlined > button,
.settings entry, .settings dropdown > button, .settings spinbutton {
  background: transparent;
}
`
	default:
		return ""
	}
}

// ThemeControls is the control skin that goes with a colour theme, so the
// seven built-in themes change the desktop's controls as well as its colours:
// square and transparent for the cool editions, rounded for the paper ones.
var ThemeControls = map[string]string{
	"yoru": "inua", "washi": "soft", "aojashin": "soft",
	"suimen": "inua", "rinko": "soft", "bunko": "outline", "denko": "outline",
}

// ControlsFor is the skin a theme uses unless the user chose one.
func ControlsFor(theme string) string {
	if skin, ok := ThemeControls[theme]; ok {
		return skin
	}
	return "inua"
}
