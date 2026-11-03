package ui

import (
	"cmp"
	"slices"
	"strings"

	"codeberg.org/puregotk/puregotk/v4/gdk"
	"codeberg.org/puregotk/puregotk/v4/gtk"
	"codeberg.org/puregotk/puregotk/v4/pango"

	"github.com/lyricat/inua/internal/gtkx"
	"github.com/lyricat/inua/internal/i18n"
	"github.com/lyricat/inua/internal/layershell"
)

type wayfireSwitcher struct {
	open          bool
	win           *gtk.ApplicationWindow
	scrims        []*gtk.ApplicationWindow
	focusedMon    string
	windows       []wayfireOverviewItem
	selectedIndex int
	cardWidgets   map[string]*gtk.Box
	cardsBox      gtk.Box
	scroll        gtk.ScrolledWindow
	appLabel      *gtk.Label
	titleLabel    *gtk.Label
	refs          gtkx.Scope

	onKey        func(gtk.EventControllerKey, uint32, uint32, gdk.ModifierType) bool
	onKeyRelease func(gtk.EventControllerKey, uint32, uint32, gdk.ModifierType)
	onCardClick  func(gtk.GestureClick, int32, float64, float64)
	onCardHover  func(gtk.EventControllerMotion, float64, float64)
	onBackdrop   func(gtk.GestureClick, int32, float64, float64)
}

func (s *shellUI) bindWayfireSwitcherHandlers() {
	sw := &s.wfSwitcher

	sw.onCardClick = func(g gtk.GestureClick, _ int32, _, _ float64) {
		w := g.GetWidget()
		if w == nil {
			return
		}
		defer w.Unref()
		name := w.GetName()
		if strings.HasPrefix(name, "sw-win:") {
			addr := strings.TrimPrefix(name, "sw-win:")
			s.recordWayfireFocus(addr)
			s.snap.ActiveToplevel = addr
			s.closeWayfireSwitcher(false)
			s.focusWindow(addr)
		}
	}

	sw.onCardHover = func(m gtk.EventControllerMotion, _, _ float64) {
		w := m.GetWidget()
		if w == nil {
			return
		}
		defer w.Unref()
		name := w.GetName()
		if strings.HasPrefix(name, "sw-win:") {
			addr := strings.TrimPrefix(name, "sw-win:")
			for idx, item := range sw.windows {
				if item.address == addr {
					s.selectWayfireSwitcherIndex(idx)
					break
				}
			}
		}
	}

	sw.onBackdrop = func(g gtk.GestureClick, _ int32, x, y float64) {
		w := g.GetWidget()
		if w == nil {
			return
		}
		defer w.Unref()
		picked := w.Pick(x, y, gtk.PickDefaultValue)
		if picked != nil {
			defer picked.Unref()
			if picked.HasCssClass("wayfire-overview-backdrop") || picked.HasCssClass("wayfire-overview-scrim") {
				s.closeWayfireSwitcher(true)
			}
		}
	}

	sw.onKeyRelease = func(_ gtk.EventControllerKey, keyval, _ uint32, _ gdk.ModifierType) {
		if !sw.open {
			return
		}
		switch int32(keyval) {
		case gdk.KEY_Alt_L, gdk.KEY_Alt_R, gdk.KEY_Super_L, gdk.KEY_Super_R, gdk.KEY_Meta_L, gdk.KEY_Meta_R:
			s.commitWayfireSwitcherSelection()
		}
	}

	sw.onKey = func(_ gtk.EventControllerKey, keyval, _ uint32, mods gdk.ModifierType) bool {
		if !sw.open {
			return false
		}
		switch keyval {
		case keyEscape:
			s.closeWayfireSwitcher(true)
			return true
		case keyReturn, keyKPEnter, keySpace:
			s.commitWayfireSwitcherSelection()
			return true
		case keyTab:
			if mods&gdk.ShiftMaskValue != 0 {
				s.stepWayfireSwitcher(-1)
			} else {
				s.stepWayfireSwitcher(1)
			}
			return true
		case keyISOLeftTab:
			s.stepWayfireSwitcher(-1)
			return true
		case keyLeft, keyUp:
			s.stepWayfireSwitcher(-1)
			return true
		case keyRight, keyDown:
			s.stepWayfireSwitcher(1)
			return true
		case 0xffff: // Delete key
			if sw.selectedIndex >= 0 && sw.selectedIndex < len(sw.windows) {
				addr := sw.windows[sw.selectedIndex].address
				s.closeWayfireWindow(addr)
				sw.windows = slices.DeleteFunc(sw.windows, func(it wayfireOverviewItem) bool {
					return it.address == addr
				})
				if len(sw.windows) == 0 {
					s.closeWayfireSwitcher(false)
					return true
				}
				if sw.selectedIndex >= len(sw.windows) {
					sw.selectedIndex = max(0, len(sw.windows)-1)
				}
				s.renderWayfireSwitcher()
				s.selectWayfireSwitcherIndex(sw.selectedIndex)
			}
			return true
		}
		return false
	}
}

func (s *shellUI) toggleWayfireSwitcher() {
	if s.wfSwitcher.open {
		s.stepWayfireSwitcher(1)
		return
	}
	s.stepWayfireSwitcher(1)
}

func (s *shellUI) stepWayfireSwitcher(delta int) {
	sw := &s.wfSwitcher
	if !sw.open {
		s.openWayfireSwitcher(delta)
		return
	}
	n := len(sw.windows)
	if n == 0 {
		return
	}
	newIdx := (sw.selectedIndex + delta) % n
	if newIdx < 0 {
		newIdx += n
	}
	s.selectWayfireSwitcherIndex(newIdx)
}

func (s *shellUI) openWayfireSwitcher(initialDelta int) {
	sw := &s.wfSwitcher
	if sw.open {
		return
	}
	if s.wfOverview.open {
		s.closeWayfireOverview(false)
	}
	s.closeClipboard()
	s.closePasswords()

	sw.open = true
	focusedMon := s.snap.FocusedMonitor
	if focusedMon == "" && len(s.snap.Monitors) > 0 {
		focusedMon = s.snap.Monitors[0].Name
	}
	sw.focusedMon = focusedMon
	sw.cardWidgets = make(map[string]*gtk.Box)

	var items []wayfireOverviewItem
	for _, t := range s.snap.Toplevels {
		if t.Address == "" {
			continue
		}
		// overview.per_monitor: the switcher keeps to the focused display's
		// windows, as the overview does, instead of every window there is.
		if s.cfg.Overview.PerMonitor && len(s.snap.Monitors) > 1 && t.Monitor != focusedMon {
			continue
		}
		appName := t.Class
		iconName := t.Class
		if entry := s.dockState.apps.ForClass(t.Class); entry != nil {
			if entry.Name != "" {
				appName = entry.Name
			}
			if entry.Icon != "" {
				iconName = entry.Icon
			}
		}
		if appName == "" {
			appName = t.Title
		}
		if appName == "" {
			appName = i18n.T("Window")
		}
		title := t.Title
		if title == "" {
			title = appName
		}
		items = append(items, wayfireOverviewItem{
			address: t.Address,
			title:   title,
			class:   t.Class,
			appName: appName,
			icon:    iconName,
			monitor: t.Monitor,
			active:  t.Activated || t.Address == s.snap.ActiveToplevel,
			pid:     t.PID,
		})
	}

	mruPos := func(addr string) int {
		for i, a := range s.wayfireMRU {
			if a == addr {
				return i
			}
		}
		return len(s.wayfireMRU) + 100
	}
	slices.SortStableFunc(items, func(a, b wayfireOverviewItem) int {
		if a.active != b.active {
			if a.active {
				return -1
			}
			return 1
		}
		return cmp.Compare(mruPos(a.address), mruPos(b.address))
	})

	sw.windows = items

	if len(items) == 0 {
		s.closeWayfireSwitcher(false)
		return
	}

	if initialDelta < 0 {
		sw.selectedIndex = len(items) - 1
	} else if len(items) >= 2 && initialDelta > 0 {
		sw.selectedIndex = 1
	} else {
		sw.selectedIndex = 0
	}

	sw.win = gtk.NewApplicationWindow(s.app)
	sw.win.AddCssClass("overview")
	w := sw.win.GoPointer()
	if s.layer {
		layershell.InitForWindow(w)
		layershell.SetNamespace(w, "inua-wayfire-switcher")
		layershell.SetLayer(w, layershell.LayerOverlay)
		layershell.SetKeyboardMode(w, layershell.KeyboardExclusive)
		for _, e := range []layershell.Edge{layershell.EdgeTop, layershell.EdgeBottom, layershell.EdgeLeft, layershell.EdgeRight} {
			layershell.SetAnchor(w, e, true)
		}
		layershell.SetExclusiveZone(w, -1)
		for _, b := range s.bars {
			if b.connector() == focusedMon {
				layershell.SetMonitor(w, b.mon.GoPointer())
				break
			}
		}
	} else {
		sw.win.SetTitle(i18n.T("Task Switcher"))
		sw.win.SetDefaultSize(800, 260)
	}

	for _, m := range s.snap.Monitors {
		if m.Name == focusedMon {
			continue
		}
		scrimWin := gtk.NewApplicationWindow(s.app)
		scrimWin.AddCssClass("overview")
		swPtr := scrimWin.GoPointer()
		if s.layer {
			layershell.InitForWindow(swPtr)
			layershell.SetNamespace(swPtr, "inua-wayfire-switcher-scrim")
			layershell.SetLayer(swPtr, layershell.LayerOverlay)
			layershell.SetKeyboardMode(swPtr, layershell.KeyboardNone)
			for _, e := range []layershell.Edge{layershell.EdgeTop, layershell.EdgeBottom, layershell.EdgeLeft, layershell.EdgeRight} {
				layershell.SetAnchor(swPtr, e, true)
			}
			layershell.SetExclusiveZone(swPtr, -1)
			for _, b := range s.bars {
				if b.connector() == m.Name {
					layershell.SetMonitor(swPtr, b.mon.GoPointer())
					break
				}
			}
		}
		scrimBox := gtk.NewBox(gtk.OrientationVerticalValue, 0)
		scrimBox.AddCssClass("wayfire-overview-scrim")
		click := gtk.NewGestureClick()
		click.ConnectReleased(&sw.onBackdrop)
		scrimBox.AddController(&click.EventController)
		scrimWin.SetChild(&scrimBox.Widget)
		scrimWin.Present()
		sw.scrims = append(sw.scrims, scrimWin)
	}

	root := gtk.NewBox(gtk.OrientationVerticalValue, 0)
	root.AddCssClass("wayfire-overview-backdrop")
	root.SetHalign(gtk.AlignFillValue)
	root.SetValign(gtk.AlignFillValue)
	rootClick := gtk.NewGestureClick()
	rootClick.ConnectReleased(&sw.onBackdrop)
	root.AddController(&rootClick.EventController)

	hudContainer := gtk.NewBox(gtk.OrientationVerticalValue, 0)
	hudContainer.SetHalign(gtk.AlignCenterValue)
	hudContainer.SetValign(gtk.AlignCenterValue)
	hudContainer.SetHexpand(true)
	hudContainer.SetVexpand(true)

	hud := gtk.NewBox(gtk.OrientationVerticalValue, 10)
	hud.AddCssClass("wayfire-switcher-hud")
	gtkx.Append(hudContainer, &hud.Widget)
	gtkx.Append(root, &hudContainer.Widget)

	sw.scroll = *gtk.NewScrolledWindow()
	sw.scroll.SetPolicy(gtk.PolicyAutomaticValue, gtk.PolicyNeverValue)
	sw.scroll.SetPropagateNaturalWidth(true)
	sw.scroll.SetMaxContentWidth(920)

	sw.cardsBox = *gtk.NewBox(gtk.OrientationHorizontalValue, 8)
	sw.cardsBox.SetHalign(gtk.AlignCenterValue)
	sw.cardsBox.SetValign(gtk.AlignCenterValue)
	sw.scroll.SetChild(&sw.cardsBox.Widget)
	gtkx.Append(hud, &sw.scroll.Widget)

	infoBox := gtk.NewBox(gtk.OrientationVerticalValue, 2)
	infoBox.AddCssClass("wayfire-switcher-info")
	infoBox.SetHalign(gtk.AlignCenterValue)

	sw.appLabel = gtk.NewLabel("")
	sw.appLabel.AddCssClass("wayfire-switcher-app")
	sw.appLabel.SetHalign(gtk.AlignCenterValue)
	sw.appLabel.SetEllipsize(pango.EllipsizeEndValue)
	gtkx.Append(infoBox, &sw.appLabel.Widget)

	sw.titleLabel = gtk.NewLabel("")
	sw.titleLabel.AddCssClass("wayfire-switcher-title")
	sw.titleLabel.SetHalign(gtk.AlignCenterValue)
	sw.titleLabel.SetEllipsize(pango.EllipsizeEndValue)
	sw.titleLabel.SetMaxWidthChars(60)
	gtkx.Append(infoBox, &sw.titleLabel.Widget)

	gtkx.Append(hud, &infoBox.Widget)

	keys := gtk.NewEventControllerKey()
	keys.SetPropagationPhase(gtk.PhaseCaptureValue)
	keys.ConnectKeyPressed(&sw.onKey)
	keys.ConnectKeyReleased(&sw.onKeyRelease)
	sw.win.AddController(&keys.EventController)

	sw.win.SetChild(&root.Widget)
	sw.win.Present()

	s.renderWayfireSwitcher()
	s.selectWayfireSwitcherIndex(sw.selectedIndex)
}

func (s *shellUI) renderWayfireSwitcher() {
	sw := &s.wfSwitcher
	gtkx.Clear(&sw.cardsBox)
	sw.cardWidgets = make(map[string]*gtk.Box)

	for _, it := range sw.windows {
		card := gtk.NewBox(gtk.OrientationVerticalValue, 0)
		card.SetName("sw-win:" + it.address)
		card.AddCssClass("wayfire-switcher-card")
		card.SetFocusable(true)
		card.SetValign(gtk.AlignCenterValue)
		card.SetHalign(gtk.AlignCenterValue)

		click := gtk.NewGestureClick()
		click.ConnectReleased(&sw.onCardClick)
		card.AddController(&click.EventController)

		hover := gtk.NewEventControllerMotion()
		hover.ConnectEnter(&sw.onCardHover)
		card.AddController(&hover.EventController)

		icon := gtk.NewImage()
		setIcon(icon, it.icon)
		icon.SetPixelSize(64)
		icon.SetHalign(gtk.AlignCenterValue)
		icon.SetValign(gtk.AlignCenterValue)
		icon.SetCanTarget(false)
		gtkx.Append(card, &icon.Widget)

		sw.cardWidgets[it.address] = card
		gtkx.Append(&sw.cardsBox, &card.Widget)
	}
}

func (s *shellUI) selectWayfireSwitcherIndex(idx int) {
	sw := &s.wfSwitcher
	if idx < 0 || idx >= len(sw.windows) {
		return
	}
	if sw.selectedIndex >= 0 && sw.selectedIndex < len(sw.windows) {
		oldAddr := sw.windows[sw.selectedIndex].address
		if box, ok := sw.cardWidgets[oldAddr]; ok && box != nil {
			box.RemoveCssClass("selected")
		}
	}
	sw.selectedIndex = idx
	item := sw.windows[idx]
	if box, ok := sw.cardWidgets[item.address]; ok && box != nil {
		box.AddCssClass("selected")
		box.GrabFocus()
	}
	if sw.appLabel != nil {
		sw.appLabel.SetText(item.appName)
	}
	if sw.titleLabel != nil {
		if item.title != "" && item.title != item.appName {
			sw.titleLabel.SetText(item.title)
			sw.titleLabel.SetVisible(true)
		} else {
			sw.titleLabel.SetText("")
			sw.titleLabel.SetVisible(false)
		}
	}
}

func (s *shellUI) commitWayfireSwitcherSelection() {
	sw := &s.wfSwitcher
	if len(sw.windows) == 0 || sw.selectedIndex < 0 || sw.selectedIndex >= len(sw.windows) {
		s.closeWayfireSwitcher(true)
		return
	}
	addr := sw.windows[sw.selectedIndex].address
	s.recordWayfireFocus(addr)
	s.snap.ActiveToplevel = addr
	s.closeWayfireSwitcher(false)
	s.focusWindow(addr)
}

func (s *shellUI) closeWayfireSwitcher(restore bool) {
	sw := &s.wfSwitcher
	if !sw.open {
		return
	}
	sw.open = false

	for _, scrim := range sw.scrims {
		if scrim != nil {
			scrim.Destroy()
			scrim.Unref()
		}
	}
	sw.scrims = nil

	if sw.win != nil {
		sw.win.Destroy()
		sw.refs.Release()
		sw.win.Unref()
		sw.win = nil
	}
	sw.cardWidgets = nil
	sw.windows = nil
	sw.appLabel = nil
	sw.titleLabel = nil
}
