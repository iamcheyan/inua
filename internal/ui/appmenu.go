package ui

import (
	"context"
	"log"
	"strconv"

	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/appmenu"
	"github.com/lyricat/inua/internal/gtkx"
	"github.com/lyricat/inua/internal/hypr"
	"github.com/lyricat/inua/internal/system"
)

// appMenuTarget is what a click in the bar's menu acts on, kept per widget so a
// delayed callback cannot reach a menu that has already been replaced.
type appMenuTarget struct {
	entry   appmenu.Entry
	pid     int
	bar     *bar
	section bool // a top-level entry whose children hang from a popover
}

type appMenuState struct {
	registrar  *appmenu.Registrar
	client     *appmenu.Client
	targets    map[string]appMenuTarget
	nextTarget uint64
}

func (s *shellUI) startAppMenu() {
	conn, err := system.SessionBus()
	if err != nil {
		log.Printf("appmenu: %v", err)
		return
	}
	s.appmenu.registrar = appmenu.New(conn)
	s.appmenu.client = appmenu.NewClient(s.appmenu.registrar, appmenu.NewA11y())
	s.appmenu.targets = make(map[string]appMenuTarget)
	s.appmenu.registrar.SetOnChange(func() { gtkx.Post(s.syncAppMenu) })
	go func() {
		if err := s.appmenu.registrar.Run(context.Background()); err != nil {
			log.Printf("appmenu registrar: %v", err)
		}
	}()
}

func focusedPID(snap hypr.Snapshot) int {
	for _, win := range snap.Toplevels {
		if win.Address == snap.ActiveToplevel {
			return win.PID
		}
	}
	return 0
}

// syncAppMenu shows the focused process's menu on the focused monitor's bar.
func (s *shellUI) syncAppMenu() {
	if s.appmenu.client == nil {
		return
	}
	pid := focusedPID(s.snap)
	for _, b := range s.bars {
		if b.connector() != s.snap.FocusedMonitor || pid == 0 {
			if b.appMenuPID != 0 {
				b.appMenuGen++
				b.appMenuPID = 0
				s.closeAppMenu(b)
				gtkx.Clear(&b.appMenu)
				b.appMenu.SetVisible(false)
			}
			continue
		}
		if b.appMenuPID == pid {
			continue
		}
		b.appMenuPID = pid
		b.appMenuGen++
		s.closeAppMenu(b)
		gtkx.Clear(&b.appMenu)
		b.appMenu.SetVisible(false)
		go s.loadAppMenu(b, b.appMenuGen, pid)
	}
}

// refreshAppMenu rereads the menu of the process the bar is showing, after an
// item was activated and the application may have changed it.
func (s *shellUI) refreshAppMenu(pid int) {
	for _, b := range s.bars {
		if b.appMenuPID != pid || b.connector() != s.snap.FocusedMonitor {
			continue
		}
		b.appMenuGen++
		go s.loadAppMenu(b, b.appMenuGen, pid)
	}
}

func (s *shellUI) loadAppMenu(b *bar, gen uint64, pid int) {
	entries, err := s.appmenu.client.Menu(pid)
	gtkx.Post(func() {
		if b.appMenuGen != gen || b.appMenuPID != pid || focusedPID(s.snap) != pid {
			return
		}
		if err != nil {
			log.Printf("appmenu %d: %v", pid, err)
			return
		}
		gtkx.Clear(&b.appMenu)
		s.appmenu.targets = make(map[string]appMenuTarget)
		for _, entry := range entries {
			if entry.Separator {
				continue
			}
			s.appendAppMenu(b, entry, pid)
		}
		b.appMenu.SetVisible(b.appMenu.GetFirstChild() != nil)
		log.Printf("appmenu: loaded %d entries pid=%d", len(entries), pid)
	})
}

func (s *shellUI) appendAppMenu(b *bar, entry appmenu.Entry, pid int) {
	button := gtk.NewButton()
	button.SetLabel(entry.Label)
	button.SetHasFrame(false)
	button.SetFocusable(false)
	button.SetSensitive(entry.Enabled || len(entry.Children) > 0)
	button.SetName(s.addAppMenuTarget(b, entry, pid, len(entry.Children) > 0))
	button.ConnectClicked(&s.onAppMenuClicked)
	gtkx.Append(&b.appMenu, &button.Widget)
}

func (s *shellUI) addAppMenuTarget(b *bar, entry appmenu.Entry, pid int, section bool) string {
	s.appmenu.nextTarget++
	token := strconv.FormatUint(s.appmenu.nextTarget, 10)
	s.appmenu.targets[token] = appMenuTarget{entry: entry, pid: pid, bar: b, section: section}
	return token
}

// closeAppMenu drops the menu the bar has open, if any.
func (s *shellUI) closeAppMenu(b *bar) {
	s.closeMenu()
}

// openAppMenu hangs the section the button names under it, and closes it
// again when the same button is clicked while it is open.
func (s *shellUI) openAppMenu(b *bar, button *gtk.Button, target appMenuTarget) {
	m := &s.menu
	if m.open && !m.closing && m.pid == target.pid && m.section == target.entry.Label {
		s.closeMenu()
		return
	}
	if m.open && !m.closing {
		m.pid, m.section = target.pid, target.entry.Label
		m.entries, m.stack = target.entry.Children, nil
		s.fillMenu()
		return
	}
	if m.closing {
		show := target
		m.gone = func() { s.showMenu(&button.Widget, show) }
		return
	}
	s.showMenu(&button.Widget, target)
}

// activateAppMenu invokes an entry, but only while the process it belongs to
// still has the focus the bar drew the menu for.
func (s *shellUI) activateAppMenu(target appMenuTarget) {
	if focusedPID(s.snap) != target.pid || !target.entry.Enabled {
		return
	}
	go func() {
		if err := s.appmenu.client.Activate(target.entry); err != nil {
			log.Printf("appmenu activate %q: %v", target.entry.Label, err)
		}
		gtkx.Post(func() { s.refreshAppMenu(target.pid) })
	}()
}

func (s *shellUI) bindAppMenuHandlers() {
	s.onAppMenuClicked = func(button gtk.Button) {
		log.Printf("appmenu: click %q", button.GetName())
		target, ok := s.appmenu.targets[button.GetName()]
		log.Printf("appmenu: target ok=%v", ok)
		if !ok {
			return
		}
		if target.section {
			s.openAppMenu(target.bar, &button, target)
			return
		}
		if !target.entry.Enabled {
			return
		}
		s.activateAppMenu(target)
	}
}
