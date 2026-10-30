package uikit

import (
	"codeberg.org/puregotk/puregotk/v4/gtk"
)

// MenuAt is where a menu opens: under its trigger or above it, with an
// arrow at the trigger's middle, or at the pointer, without one.
type MenuAt int

const (
	Below MenuAt = iota
	Above
	AtPointer
)

// onMenuMap restarts a menu's growing each time it shows: GTK plays a CSS
// animation when the style first has it, so a popover kept between opens
// (Files', Mail's) would grow only once. Each show trades its animation
// for its twin of another name (grow-a, grow-b), which GTK starts afresh.
var onMenuMap = func(w gtk.Widget) {
	if w.HasCssClass("grow-a") {
		w.RemoveCssClass("grow-a")
		w.AddCssClass("grow-b")
		return
	}
	w.RemoveCssClass("grow-b")
	w.AddCssClass("grow-a")
}

// Menu gives pop the look and motion of design/ui.md's menus: the glass
// in a hairline with the floating cards' shadow, growing out of where it
// opens, its items `.menu-item` (or GTK's own, in a popover menu).
func Menu(pop *gtk.Popover, at MenuAt) {
	pop.AddCssClass("glass-menu")
	switch at {
	case Below:
		pop.SetHasArrow(true)
		pop.SetPosition(gtk.PosBottomValue)
	case Above:
		pop.AddCssClass("above")
		pop.SetHasArrow(true)
		pop.SetPosition(gtk.PosTopValue)
	case AtPointer:
		pop.AddCssClass("at-pointer")
		pop.SetHasArrow(false)
	}
	pop.ConnectMap(&onMenuMap)
}
