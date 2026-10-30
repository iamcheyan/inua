package filesui

import (
	"codeberg.org/puregotk/puregotk/v4/gdk"
	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/gtkx"
	"github.com/lyricat/inua/internal/uikit"
)

// menuItem is an entry of a menu: a label with its key, or a separator
// when the label is empty. A checkable one shows a mark when on, and keeps
// the menu open, so several can be turned on and off in a row.
type menuItem struct {
	label, key string
	run        func()
	check, on  bool
}

// popMenu is a menu popping up over a widget, in the shell's look
// (uikit.Menu); its buttons go through the hub and are forgotten when it
// is filled again. Each opening makes its popover anew, at the pointer or
// under the button that opened it.
type popMenu struct {
	h      *hub
	parent *gtk.Widget
	pop    *gtk.Popover
	box    gtk.Box
	ptrs   []uintptr
	items  func() []menuItem // what it shows, asked again after a check
}

func newPopMenu(h *hub, parent *gtk.Widget) *popMenu {
	return &popMenu{h: h, parent: parent}
}

// open makes the popover, on at, in place of the last one.
func (m *popMenu) open(at *gtk.Widget, where uikit.MenuAt) {
	if m.pop != nil {
		m.pop.Unparent()
	}
	m.pop = gtk.NewPopover()
	m.pop.AddCssClass("files-menu")
	uikit.Menu(m.pop, where)
	m.box = *gtk.NewBox(gtk.OrientationVerticalValue, 0)
	m.pop.SetChild(&m.box.Widget)
	m.box.Unref()
	m.pop.SetParent(at)
	m.pop.Unref() // at holds it
}

// show opens the menu at x, y in its parent.
func (m *popMenu) show(items func() []menuItem, x, y int32) {
	m.open(m.parent, uikit.AtPointer)
	m.items = items
	m.fill()
	rect := gdk.Rectangle{X: x, Y: y, Width: 1, Height: 1}
	m.pop.SetPointingTo(&rect)
	m.pop.Popup()
}

// showUnder opens the menu under the button that opened it, its arrow at
// the button's middle.
func (m *popMenu) showUnder(items func() []menuItem, button *gtk.Widget) {
	m.open(button, uikit.Below)
	m.items = items
	m.fill()
	m.pop.Popup()
}

func (m *popMenu) fill() {
	m.h.forget(m.ptrs)
	m.ptrs = m.ptrs[:0]
	gtkx.Clear(&m.box)
	for _, it := range m.items() {
		if it.label == "" {
			sep := gtk.NewSeparator(gtk.OrientationHorizontalValue)
			gtkx.Append(&m.box, &sep.Widget)
			continue
		}
		b := gtk.NewButton()
		b.AddCssClass("menu-item")
		box := gtk.NewBox(gtk.OrientationHorizontalValue, 8)
		if it.check {
			mark := gtk.NewImageFromIconName("object-select-symbolic")
			mark.AddCssClass("files-menu-check")
			mark.SetOpacity(map[bool]float64{true: 1, false: 0}[it.on])
			gtkx.Append(box, &mark.Widget)
		}
		l := gtk.NewLabel(it.label)
		l.SetXalign(0)
		l.SetHexpand(true)
		gtkx.Append(box, &l.Widget)
		if it.key != "" {
			k := gtk.NewLabel(it.key)
			k.AddCssClass("menu-key")
			k.SetValign(gtk.AlignCenterValue)
			gtkx.Append(box, &k.Widget)
		}
		b.SetChild(&box.Widget)
		box.Unref()
		run, keep := it.run, it.check
		m.h.click(b, func() {
			if !keep {
				m.pop.Popdown()
			}
			if run != nil {
				run()
			}
			if keep {
				m.fill()
			}
		})
		m.ptrs = append(m.ptrs, b.GoPointer())
		gtkx.Append(&m.box, &b.Widget)
	}
}

func (m *popMenu) destroy() {
	m.h.forget(m.ptrs)
	if m.pop != nil {
		m.pop.Unparent()
	}
}
