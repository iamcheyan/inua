package termui

import (
	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/gtkx"
	"github.com/lyricat/inua/internal/term/host"
	"github.com/lyricat/inua/internal/term/model"
)

// Columns 1 and 2 take the width the grip at their right edge is dragged
// to, within colWidths, and the host keeps it with the window's size
// (model.UI). Column 1's search is a button in its head, which opens the
// search in a row of its own under it; its toggle hides the column, and
// one at the top of column 2 shows it again.

// colWidths are each column's least, first and most widths.
var colWidths = [2][3]int{{180, 232, 420}, {220, 312, 560}}

// colWidth is column i's width w within its limits; 0 is its first.
func colWidth(i, w int) int {
	if w == 0 {
		return colWidths[i][1]
	}
	return max(colWidths[i][0], min(w, colWidths[i][2]))
}

// columnGrips makes the grips draggable and gives the columns their
// widths.
func (a *App) columnGrips(ui *gtkx.Builder) {
	c := &a.cols
	cols := [2]*gtk.Box{c.col1, c.col2}
	for i := range c.grips {
		c.grips[i] = &gtk.Box{}
		ui.Get([2]string{"grip1", "grip2"}[i], c.grips[i])
		c.grips[i].SetCursorFromName("col-resize")
		drag := gtk.NewGestureDrag()
		// The grip moves with the edge it sets, and the drag's offsets are
		// its own: the pointer is followed in the window's coordinates.
		inWindow := func(x float64) float64 {
			var wx, wy float64
			c.grips[i].TranslateCoordinates(&a.win.Widget, x, 0, &wx, &wy)
			return wx
		}
		c.onGripBegin[i] = func(_ gtk.GestureDrag, x, _ float64) {
			c.gripFrom, c.gripX = int(cols[i].GetWidth()), inWindow(x)
			a.holdSizes(true)
		}
		c.onGripUpdate[i] = func(g gtk.GestureDrag, dx, _ float64) {
			var x, y float64
			g.GetStartPoint(&x, &y)
			a.setColWidth(i, c.gripFrom+int(inWindow(x+dx)-c.gripX))
		}
		c.onGripEnd[i] = func(gtk.GestureDrag, float64, float64) {
			a.holdSizes(false)
			a.keepUI()
		}
		drag.ConnectDragBegin(&c.onGripBegin[i])
		drag.ConnectDragUpdate(&c.onGripUpdate[i])
		drag.ConnectDragEnd(&c.onGripEnd[i])
		c.grips[i].AddController(&drag.EventController)
	}
	c.col1Reveal, c.findReveal, c.findButton = &gtk.Revealer{}, &gtk.Revealer{}, &gtk.ToggleButton{}
	c.sidebarHide, c.sidebarShow, c.sidebarShowHead = &gtk.Button{}, &gtk.Button{}, &gtk.Box{}
	ui.Get("col1_reveal", c.col1Reveal)
	ui.Get("sidebar_hide", c.sidebarHide)
	ui.Get("sidebar_show", c.sidebarShow)
	ui.Get("sidebar_show_head", c.sidebarShowHead)
	c.onSidebar = func(gtk.Button) { a.toggleColumn(0) }
	// The terminals keep their size while it slides (applyFolds).
	c.onSlid = func(uintptr, uintptr, uintptr) {
		if c.col1Reveal.GetChildRevealed() == c.col1Reveal.GetRevealChild() {
			a.holdSizes(false)
		}
	}
	gtkx.ConnectNotify(c.col1Reveal, "child-revealed", &c.onSlid)
	c.sidebarHide.ConnectClicked(&c.onSidebar)
	c.sidebarShow.ConnectClicked(&c.onSidebar)
	ui.Get("find_reveal", c.findReveal)
	ui.Get("find_button", c.findButton)
	c.onFindButton = func(gtk.ToggleButton) {
		on := c.findButton.GetActive()
		c.findReveal.SetRevealChild(on)
		if on {
			c.find.GrabFocus()
		} else if c.find.GetText() != "" {
			c.find.SetText("") // closed, it finds nothing
		}
	}
	c.findButton.ConnectToggled(&c.onFindButton)
	for i := range c.width {
		a.setColWidth(i, 0)
	}
}

// setColWidth gives column i the width w, within its limits.
func (a *App) setColWidth(i, w int) {
	c := &a.cols
	w = colWidth(i, w)
	if w == c.width[i] {
		return
	}
	c.width[i] = w
	[2]*gtk.Box{c.col1, c.col2}[i].SetSizeRequest(int32(w), -1)
}

// holdSizes keeps every terminal's grid at its size while a column is
// dragged or slides, and gives them their tiles' sizes after: a program
// redrawn at each width on the way shook.
func (a *App) holdSizes(on bool) {
	if a.cols.held == on {
		return
	}
	a.cols.held = on
	for _, tl := range a.tiles {
		tl.pane.sizeHeld = on
		if !on {
			tl.pane.widget.QueueAllocate()
		}
	}
}

// keepUI has the host keep how the window is: its size, the columns
// folded and their widths.
func (a *App) keepUI() {
	if a.client == nil || !a.uiDone {
		return
	}
	ui := a.uiNow()
	a.ask("keep the window", func(c *host.Client) error { return c.SetUI(ui) })
}

// uiNow is how the window is.
func (a *App) uiNow() model.UI {
	return model.UI{
		Width: int(a.win.GetWidth()), Height: int(a.win.GetHeight()),
		Fold1: a.fold[0], Fold2: a.fold[1],
		Col1: a.cols.width[0], Col2: a.cols.width[1],
	}
}
