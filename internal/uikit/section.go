// Package uikit builds the pieces of design/ui.md that are made of several
// widgets, the same in the shell and the apps. A piece of one widget is a
// CSS class (`outlined`, `mark`, `kicker`), not a function here.
package uikit

import (
	"codeberg.org/puregotk/puregotk/v4/glib"
	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/gtkx"
)

// Bracketed is a section's label as markup: the name in brackets, the
// brackets dimmed, [STREAM]. The name is escaped.
func Bracketed(name string) string {
	return "<span alpha='55%'>[</span>" + glib.MarkupEscapeText(name, -1) + "<span alpha='55%'>]</span>"
}

// Head is a section's head: its mark, its [LABEL] and a dim meta line that
// takes the rest of the width.
type Head struct {
	Box   *gtk.Box
	Label *gtk.Label
	Meta  *gtk.Label
}

// NewHead makes a section's head labelled name (none when empty), with
// meta after it.
func NewHead(name, meta string) Head {
	box := gtk.NewBox(gtk.OrientationHorizontalValue, 10)
	return FillHead(box, name, meta)
}

// FillHead makes box a section's head, as NewHead: for a head that a
// layout holds already (a page's sticky copy of its current section's).
func FillHead(box *gtk.Box, name, meta string) Head {
	box.AddCssClass("section-head")
	mark := gtk.NewBox(gtk.OrientationHorizontalValue, 0)
	mark.AddCssClass("mark")
	mark.SetValign(gtk.AlignCenterValue)
	gtkx.Append(box, &mark.Widget)
	h := Head{Box: box}
	h.Label = gtk.NewLabel("")
	h.Label.AddCssClass("section-label")
	h.Label.SetUseMarkup(true)
	if name != "" {
		h.Label.SetMarkup(Bracketed(name))
	} else {
		h.Label.SetVisible(false)
	}
	gtkx.Append(box, &h.Label.Widget)
	h.Meta = gtk.NewLabel(meta)
	h.Meta.AddCssClass("section-meta")
	h.Meta.SetHexpand(true)
	h.Meta.SetXalign(0)
	h.Meta.SetEllipsize(3) // end
	gtkx.Append(box, &h.Meta.Widget)
	return h
}

// Section is a section of a page: its head on a hairline over the body its
// rows go in.
type Section struct {
	Box  *gtk.Box
	Head Head
	Body *gtk.Box
}

// NewSection makes a section headed name and meta, its body empty.
func NewSection(name, meta string) Section {
	s := Section{Box: gtk.NewBox(gtk.OrientationVerticalValue, 0)}
	s.Box.AddCssClass("section")
	s.Head = NewHead(name, meta)
	gtkx.Append(s.Box, &s.Head.Box.Widget)
	s.Body = gtk.NewBox(gtk.OrientationVerticalValue, 0)
	s.Body.AddCssClass("section-body")
	gtkx.Append(s.Box, &s.Body.Widget)
	return s
}
