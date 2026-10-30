package ui

import (
	"unsafe"

	"codeberg.org/puregotk/puregotk/v4/graphene"
	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/gtkx"
	"github.com/lyricat/inua/internal/uikit"
)

// stickyHead keeps the head of the section being read at the top of a
// settings page: once a section's own head scrolls under the top edge, a
// copy of it (the page's sticky_NAME, over the scrolled area) takes its
// place, until the next section's head reaches the top.
type stickyHead struct {
	scroll      gtk.ScrolledWindow
	box         gtk.Box
	label, meta *gtk.Label
	shown       uintptr // the section whose head is shown, 0 for none
}

// buildStickyHeads finds every page's scrolled area and sticky head, fills
// the head with a mark and two labels, and follows the page's scrolling.
func (s *shellUI) buildStickyHeads(ui *gtkx.Builder) {
	st := &s.settings
	st.sticky = map[uintptr]*stickyHead{}
	for _, name := range settingsPages {
		h := &stickyHead{}
		ui.Get("scroll_"+name, &h.scroll)
		ui.Get("sticky_"+name, &h.box)
		head := uikit.FillHead(&h.box, "", "")
		h.label, h.meta = head.Label, head.Meta
		h.label.SetVisible(true)
		adj := h.scroll.GetVadjustment()
		st.sticky[adj.Ptr] = h
		adj.ConnectValueChanged(&s.onSettingsScroll)
	}
}

// updateSticky shows the head of the last section whose own head has
// scrolled under the top edge, or nothing while the first is in view.
func (s *shellUI) updateSticky(adj gtk.Adjustment) {
	h := s.settings.sticky[adj.Ptr]
	if h == nil {
		return
	}
	top := adj.GetValue()
	page := h.scroll.GetChild().GetFirstChild() // viewport > page box
	var cur, head *gtk.Widget
	for sec := page.GetFirstChild(); sec != nil; sec = sec.GetNextSibling() {
		if !sec.HasCssClass("section") {
			continue
		}
		hd := sec.GetFirstChild()
		var r graphene.Rect
		if hd == nil || !hd.ComputeBounds(page, &r) {
			continue
		}
		if y := float64((*(*[4]float32)(unsafe.Pointer(&r)))[1]); y < top {
			cur, head = sec, hd
		}
	}
	if cur == nil {
		h.shown = 0
		h.box.SetVisible(false)
		return
	}
	if cur.Ptr != h.shown {
		h.shown = cur.Ptr
		for w := head.GetFirstChild(); w != nil; w = w.GetNextSibling() {
			switch {
			case w.HasCssClass("section-label"):
				h.label.SetLabel(gtk.LabelNewFromInternalPtr(w.Ptr).GetLabel())
			case w.HasCssClass("section-meta"):
				h.meta.SetLabel(gtk.LabelNewFromInternalPtr(w.Ptr).GetLabel())
			}
		}
	}
	h.box.SetVisible(true)
}
