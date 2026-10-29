package ui

import (
	"log"
	"strconv"

	"codeberg.org/puregotk/puregotk/v4/gdk"
	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/appmenu"
	"github.com/lyricat/inua/internal/layershell"
)

// A menu cannot be a GTK popover here: the bar is a layer-shell surface, and
// Wayland only lets a popup hang from an xdg_toplevel. The menu is a card in
// its own overlay surface instead, hung under the bar the way the calendar is
// (drop.go), with submenus opened in place.
type menuPanel struct {
	drop     drop
	open     bool
	closing  bool
	win      *gtk.Window
	backdrop *gtk.Box
	card     *gtk.Box
	keys     *gtk.EventController
	pid      int
	section  string
	entries  []appmenu.Entry
	stack    []int
	rows     map[string]menuRow
	next     uint64
	gone     func()
}

type menuRow struct {
	target appMenuTarget
	expand bool
	path   []int
}

func (s *shellUI) buildMenuPanel() {
	m := &s.menu
	m.win = gtk.NewWindow()
	m.backdrop = gtk.NewBox(gtk.OrientationVerticalValue, 0)
	m.card = gtk.NewBox(gtk.OrientationVerticalValue, 0)
	m.card.AddCssClass("menu-panel")
	m.backdrop.Append(&m.card.Widget)
	m.win.SetChild(&m.backdrop.Widget)

	keys := gtk.NewEventControllerKey()
	keys.SetPropagationPhase(gtk.PhaseCaptureValue)
	keys.ConnectKeyPressed(&s.onMenuKey)
	m.win.AddController(&keys.EventController)
	m.keys = &keys.EventController

	click := gtk.NewGestureClick()
	click.ConnectPressed(&s.onMenuBackdrop)
	m.backdrop.AddController(&click.EventController)

	m.drop.attach(m.win, &keys.EventController, m.backdrop, &m.card.Widget, layershell.LayerOverlay, false)
	m.win.SetApplication(s.app)
	w := m.win.GoPointer()
	if s.layer {
		layershell.InitForWindow(w)
		layershell.SetNamespace(w, "inua-appmenu")
		layershell.SetLayer(w, layershell.LayerOverlay)
		// On demand: the focused application keeps the focus its menu is for.
		layershell.SetKeyboardMode(w, layershell.KeyboardOnDemand)
		for _, e := range []layershell.Edge{layershell.EdgeTop, layershell.EdgeBottom, layershell.EdgeLeft, layershell.EdgeRight} {
			layershell.SetAnchor(w, e, true)
		}
		layershell.SetExclusiveZone(w, -1)
		if mon := s.focusedMonitor(); mon != nil {
			layershell.SetMonitor(w, mon.GoPointer())
		}
	}
	if m.rows == nil {
		m.rows = make(map[string]menuRow)
	}
}

// showMenu hangs the application's menu under the button that was clicked,
// opening the section that button names.
func (s *shellUI) showMenu(button *gtk.Widget, target appMenuTarget) {
	m := &s.menu
	if m.win == nil {
		s.buildMenuPanel()
	}
	m.pid = target.pid
	m.section = target.entry.Label
	m.entries = target.entry.Children
	m.stack = nil
	m.open = true
	m.closing = false
	s.fillMenu()
	log.Printf("menu: show pid=%d section=%q rows=%d win=%v", m.pid, m.section, len(m.rows), m.win != nil)
	s.dropFromBar(&m.drop, nil, func(*bar) *gtk.Widget { return button })
	log.Printf("menu: hung hanging=%v host=%v u=%v", m.drop.hanging, m.drop.host != nil, m.drop.u)
}

func (s *shellUI) closeMenu() {
	m := &s.menu
	if !m.open || m.closing {
		return
	}
	m.closing = true
	m.drop.close(func() { s.onMenuGone(0) })
}

func (s *shellUI) onMenuGone(uintptr) {
	m := &s.menu
	m.open = false
	m.closing = false
	if g := m.gone; g != nil {
		m.gone = nil
		g()
	}
}

// fillMenu draws the rows of the section, with the branch in stack opened.
func (s *shellUI) fillMenu() {
	m := &s.menu
	for ch := m.card.GetFirstChild(); ch != nil; ch = m.card.GetFirstChild() {
		m.card.Remove(ch)
	}
	m.rows = make(map[string]menuRow)
	m.next = 0
	s.appendMenuRows(m.entries, 0, nil)
}

func (s *shellUI) appendMenuRows(entries []appmenu.Entry, depth int, prefix []int) {
	m := &s.menu
	for i, entry := range entries {
		if entry.Separator {
			line := gtk.NewSeparator(gtk.OrientationHorizontalValue)
			line.AddCssClass("menu-line")
			m.card.Append(&line.Widget)
			continue
		}
		path := append(append([]int{}, prefix...), i)
		expanded := equalPath(m.stack, path)

		box := gtk.NewBox(gtk.OrientationHorizontalValue, 10)
		box.AddCssClass("menu-row")
		label := gtk.NewLabel(entry.Label)
		label.SetXalign(0)
		label.SetHexpand(true)
		box.Append(&label.Widget)
		if len(entry.Children) > 0 {
			mark := gtk.NewLabel("›")
			mark.AddCssClass("menu-mark")
			box.Append(&mark.Widget)
		}
		button := gtk.NewButton()
		button.SetChild(&box.Widget)
		button.SetHasFrame(false)
		button.SetFocusable(false)
		button.AddCssClass("menu-item")
		if depth > 0 {
			button.AddCssClass("menu-sub")
		}
		if !entry.Enabled && len(entry.Children) == 0 {
			button.SetSensitive(false)
		}
		m.next++
		token := strconv.FormatUint(m.next, 10)
		button.SetName(token)
		m.rows[token] = menuRow{target: appMenuTarget{entry: entry, pid: m.pid}, expand: len(entry.Children) > 0, path: path}
		button.ConnectClicked(&s.onMenuRow)
		m.card.Append(&button.Widget)

		if expanded {
			s.appendMenuRows(entry.Children, depth+1, path)
		}
	}
}

func equalPath(stack, path []int) bool {
	if len(stack) != len(path) {
		return false
	}
	for i := range stack {
		if stack[i] != path[i] {
			return false
		}
	}
	return true
}

func (s *shellUI) bindMenuHandlers() {
	s.onMenuRow = func(button gtk.Button) {
		m := &s.menu
		row, ok := m.rows[button.GetName()]
		if !ok {
			return
		}
		log.Printf("menu: row %q expand=%v", row.target.entry.Label, row.expand)
		if row.expand {
			if equalPath(m.stack, row.path) {
				m.stack = m.stack[:len(row.path)-1]
			} else {
				m.stack = row.path
			}
			s.fillMenu()
			return
		}
		s.activateAppMenu(row.target)
		s.closeMenu()
	}
	s.onMenuBackdrop = func(g gtk.GestureClick, _ int32, x, y float64) {
		if s.barClick(s.barUnder(g.GetWidget()), x, y) {
			return // the bar takes it: another section, or this one again
		}
		m := &s.menu
		hit := m.backdrop.Pick(x, y, gtk.PickDefaultValue)
		if hit == nil {
			return
		}
		outside := hit.GoPointer() != m.card.GoPointer() && !hit.IsAncestor(&m.card.Widget)
		hit.Unref()
		if outside {
			s.closeMenu()
		}
	}
	s.onMenuKey = func(_ gtk.EventControllerKey, key uint32, _ uint32, _ gdk.ModifierType) bool {
		if key == uint32(gdk.KEY_Escape) {
			s.closeMenu()
			return true
		}
		return false
	}
}

// menuOwnedBy reports whether the open menu belongs to pid.
func (s *shellUI) menuOwnedBy(pid int) bool {
	return s.menu.open && s.menu.pid == pid
}
