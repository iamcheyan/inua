package termui

import (
	"context"
	"strings"
	"time"

	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/gtkx"
	"github.com/lyricat/inua/internal/i18n"
	"github.com/lyricat/inua/internal/term/settings"
	"github.com/lyricat/inua/internal/term/webterm"
)

// The menu button at the top right of column 1 drops a menu that looks as
// the dock's drawer does (bubble.go): on the glass, a hairline round it
// and an arrow at the button, growing out of the arrow as it fades in
// (style.css). In it: the command palette and the settings, each with its
// keys in a keycap; the Web Terminal under a title of the drawer's, what
// it is doing at the title's end (its status square filled while it
// runs), then its switch; restarting the host. The Web Terminal's state
// is read when the menu opens. A new popover each time: its animation
// runs when it is made.

type headMenu struct {
	pop     *gtk.Popover
	box     *gtk.Box
	runs    map[uintptr]func() // what each item does, by its button
	onClick func(gtk.Button)
	onShut  func(gtk.Popover)
	// webBusy is set while the menu starts or stops the Web Terminal.
	webBusy bool
}

// showHeadMenu reads whether the Web Terminal runs, then drops the menu
// under the button.
func (a *App) showHeadMenu() {
	go func() {
		ctx, cancel := context.WithTimeout(context.Background(), time.Second)
		defer cancel()
		running := webterm.Running(ctx)
		gtkx.Post(func() { a.dropHeadMenu(running) })
	}()
}

func (a *App) dropHeadMenu(running bool) {
	m := &a.cols.headMenu
	if m.pop != nil {
		return // open already
	}
	if m.onClick == nil {
		m.onClick = func(b gtk.Button) {
			run := m.runs[b.GoPointer()]
			if m.pop != nil {
				m.pop.Popdown()
			}
			if run != nil {
				run()
			}
		}
		m.onShut = func(p gtk.Popover) {
			m.pop, m.box = nil, nil
			gtkx.Post(func() { p.Unparent() })
		}
	}
	m.pop = gtk.NewPopover()
	m.pop.AddCssClass("term-menu")
	m.pop.SetPosition(gtk.PosBottomValue)
	m.box = gtk.NewBox(gtk.OrientationVerticalValue, 0)
	m.box.AddCssClass("term-menu-body")
	m.pop.SetChild(&m.box.Widget)
	m.pop.SetParent(&a.cols.menu.Widget)
	m.pop.ConnectClosed(&m.onShut)
	m.pop.Unref() // the button holds it
	m.runs = map[uintptr]func(){}
	item := func(label, action string, enabled bool, run func()) {
		b := gtk.NewButton()
		b.AddCssClass("term-menu-item")
		row := gtk.NewBox(gtk.OrientationHorizontalValue, 16)
		l := gtk.NewLabel(label)
		l.SetXalign(0)
		l.SetHexpand(true)
		row.Append(&l.Widget)
		if k := a.set.Keys[action]; action != "" && k != "" {
			key := gtk.NewLabel(keycaps(k))
			key.AddCssClass("term-menu-keycap")
			key.SetValign(gtk.AlignCenterValue)
			row.Append(&key.Widget)
		}
		b.SetChild(&row.Widget)
		b.SetSensitive(enabled)
		m.runs[b.GoPointer()] = run
		b.ConnectClicked(&m.onClick)
		m.box.Append(&b.Widget)
	}
	separator := func() {
		sep := gtk.NewSeparator(gtk.OrientationHorizontalValue)
		m.box.Append(&sep.Widget)
	}

	item(i18n.T("Command palette"), "palette", true, func() {
		var p *termPane
		if s := a.shown(); s != nil {
			p = a.paneFor(s.Focus)
		}
		a.palette(p)
	})
	item(i18n.T("Settings"), "settings", true, a.openSettings)

	// The Web Terminal: a title of the drawer's, what it does at its end,
	// then its switch.
	web, busy := a.set.Web, a.webBusy()
	head := gtk.NewBox(gtk.OrientationHorizontalValue, 8)
	head.AddCssClass("term-menu-title")
	title := gtk.NewLabel(i18n.T("WEB TERMINAL"))
	title.SetXalign(0)
	title.SetHexpand(true)
	head.Append(&title.Widget)
	mark := gtk.NewBox(gtk.OrientationHorizontalValue, 0)
	mark.AddCssClass("mark")
	mark.SetValign(gtk.AlignCenterValue)
	state, class := webStatus(web, running, busy)
	meta := gtk.NewLabel(state)
	meta.AddCssClass("term-menu-state")
	if class != "" {
		mark.AddCssClass(strings.TrimPrefix(class, "s-")) // the mark's state: on, warn
		meta.AddCssClass(class)
	}
	head.Append(&mark.Widget)
	head.Append(&meta.Widget)
	m.box.Append(&head.Widget)
	toggle := i18n.T("Turn on the Web Terminal")
	if web.On {
		toggle = i18n.T("Turn off the Web Terminal")
	}
	item(toggle, "", !busy, a.toggleWeb)
	separator()

	item(i18n.T("Restart the terminal host…"), "restart_host", true, a.restartHost)
	m.pop.Popup()
}

// webStatus is what the Web Terminal is doing, in a few words, and the
// class of its mark: filled in the accent while it runs, in warn when on
// and not running, hollow off.
func webStatus(web settings.Web, running, busy bool) (string, string) {
	where := i18n.T("this computer only")
	if web.Tailscale {
		where = i18n.T("Tailscale")
	}
	switch {
	case busy && web.On:
		return i18n.T("Starting…"), ""
	case busy:
		return i18n.T("Stopping…"), ""
	case running:
		return i18n.Tf("On, %s", where), "s-on"
	case web.On:
		return i18n.T("On, but not running"), "s-warn"
	}
	return i18n.T("Off"), ""
}

// webBusy says the Web Terminal is being started or stopped, by the menu
// or by the settings.
func (a *App) webBusy() bool {
	if pr := a.prefs; pr != nil && pr.web != nil && pr.web.busy {
		return true
	}
	return a.cols.headMenu.webBusy
}

// toggleWeb turns the Web Terminal on or off, as the settings' switch
// does: with the settings open, by their switch; else here, the settings
// opened at their Web Terminal page when it fails to start.
func (a *App) toggleWeb() {
	if a.webBusy() {
		return
	}
	if pr := a.prefs; pr != nil && pr.web != nil {
		pr.web.on.SetActive(!pr.web.on.GetActive())
		pr.pages.SetVisibleChildName("web")
		pr.win.Present()
		return
	}
	m := &a.cols.headMenu
	s := &a.set
	s.Web.On = !s.Web.On
	if err := settings.Save(settings.Path(), *s); err != nil {
		s.Web.On = !s.Web.On
		a.openSettingsAt("web", err)
		return
	}
	a.useSettings(*s)
	web := s.Web
	m.webBusy = true
	go func() {
		ctx, cancel := context.WithTimeout(context.Background(), webTimeout)
		defer cancel()
		var err error
		if web.On {
			err = webterm.Start(ctx, web)
		} else {
			webterm.Stop(ctx)
		}
		gtkx.Post(func() {
			m.webBusy = false
			if err == nil {
				return
			}
			// It did not start: off again, and why, in the settings.
			s.Web.On = false
			if serr := settings.Save(settings.Path(), *s); serr == nil {
				a.useSettings(*s)
			}
			a.openSettingsAt("web", err)
		})
	}()
}
