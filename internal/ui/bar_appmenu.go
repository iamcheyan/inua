package ui

import (
	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/gtkx"
	"github.com/lyricat/inua/internal/i18n"
	"github.com/lyricat/inua/internal/shell"
	"github.com/lyricat/inua/internal/uikit"
)

// showBarAppMenu opens the small, consistent menu for the application named
// by this bar. The application's own global menu remains a separate feature.
func (s *shellUI) showBarAppMenu(b *bar) {
	if b.appPID == 0 {
		return
	}
	if b.appPopover.GoPointer() != 0 {
		if b.appPopover.GetVisible() {
			b.appPopover.Popdown()
			return
		}
		b.appPopover.Unparent()
		b.appPopover = gtk.Popover{}
	}
	win, ok := shell.BarWindow(s.snap, b.connector())
	if !ok || win.PID != b.appPID {
		return
	}
	name := win.Class
	if e := s.dockState.apps.ForClass(win.Class); e != nil {
		name = e.Name
	}
	pop := uikit.NewMenu([]uikit.Item{
		{Label: i18n.Tf("About %s", name), Run: func() { s.showBarAppAbout(b) }},
		{Label: i18n.T("Close Window"), Run: func() { s.closeBarAppWindow(b) }},
		{Label: i18n.Tf("Quit %s", name), Run: func() { s.quitBarApp(b) }},
	}, uikit.Below)
	pop.SetParent(&b.app.Widget)
	pop.Unref() // the title button owns it
	pop.Popup()
	b.appPopover = *pop
}

func (s *shellUI) closeBarAppWindow(b *bar) {
	win, ok := shell.BarWindow(s.snap, b.connector())
	if ok && win.PID == b.appPID {
		s.dispatch("closewindow address:" + win.Address)
	}
}

func (s *shellUI) quitBarApp(b *bar) {
	pid := b.appPID
	if pid == 0 {
		return
	}
	for _, win := range s.snap.Toplevels {
		if win.PID == pid {
			s.dispatch("closewindow address:" + win.Address)
		}
	}
}

func (s *shellUI) showBarAppAbout(b *bar) {
	win, ok := shell.BarWindow(s.snap, b.connector())
	if !ok || win.PID != b.appPID {
		return
	}
	name, icon := win.Class, win.Class
	if e := s.dockState.apps.ForClass(win.Class); e != nil {
		name, icon = e.Name, e.Icon
	}
	w := gtk.NewWindow()
	w.AddCssClass("about")
	w.SetApplication(s.app)
	w.SetTitle(i18n.Tf("About %s", name))
	w.SetDefaultSize(360, -1)
	w.SetResizable(false)
	body := gtk.NewBox(gtk.OrientationVerticalValue, 10)
	body.AddCssClass("about-body")
	mark := gtk.NewImage()
	mark.AddCssClass("about-icon")
	setIcon(mark, icon)
	mark.SetPixelSize(64)
	title := gtk.NewLabel(name)
	title.AddCssClass("about-name")
	window := gtk.NewLabel(win.Title)
	window.AddCssClass("about-window")
	window.SetEllipsize(3)
	process := gtk.NewLabel(i18n.Tf("Process %d", win.PID))
	process.AddCssClass("about-process")
	close := gtk.NewButtonWithLabel(i18n.T("Close"))
	close.AddCssClass("about-close")
	onClose := func(gtk.Button) { w.Destroy() }
	close.ConnectClicked(&onClose)
	for _, child := range []*gtk.Widget{&mark.Widget, &title.Widget, &window.Widget, &process.Widget, &close.Widget} {
		gtkx.Append(body, child)
	}
	w.SetChild(&body.Widget)
	body.Unref()
	w.Present()
}
