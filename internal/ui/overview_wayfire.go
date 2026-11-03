package ui

import (
	"context"
	"fmt"
	"log"
	"slices"
	"strconv"
	"strings"
	"time"

	"codeberg.org/puregotk/puregotk/v4/gdk"
	"codeberg.org/puregotk/puregotk/v4/gobject"
	"codeberg.org/puregotk/puregotk/v4/gobject/types"
	"codeberg.org/puregotk/puregotk/v4/gtk"
	"codeberg.org/puregotk/puregotk/v4/pango"

	"github.com/lyricat/inua/internal/gtkx"
	"github.com/lyricat/inua/internal/i18n"
	"github.com/lyricat/inua/internal/layershell"
)

type wayfireOverview struct {
	open          bool
	win           *gtk.ApplicationWindow
	scrims        []*gtk.ApplicationWindow
	focusedMon    string
	allWindows    []wayfireOverviewItem
	windows       []wayfireOverviewItem
	selectedIndex int
	cardWidgets   map[string]*gtk.Box
	wsWidgets     map[int]*gtk.Box
	workspacesBox gtk.Box
	windowsBox    gtk.Box
	scroll        gtk.ScrolledWindow
	refs          gtkx.Scope

	onCardClick      func(gtk.GestureClick, int32, float64, float64)
	onCardClose      func(gtk.Button)
	onCardHover      func(gtk.EventControllerMotion, float64, float64)
	onWorkspaceClick func(gtk.GestureClick, int32, float64, float64)
	onBackdropClick  func(gtk.GestureClick, int32, float64, float64)
	onDragPrepare    func(gtk.DragSource, float64, float64) gdk.ContentProvider
	onDragBegin      func(gtk.DragSource, uintptr)
	onDragEnd        func(gtk.DragSource, uintptr, bool)
	onDropMotion     func(gtk.DropTarget, float64, float64) gdk.DragAction
	onDropLeave      func(gtk.DropTarget)
	onDrop           func(gtk.DropTarget, uintptr, float64, float64) bool
	onKey            func(gtk.EventControllerKey, uint32, uint32, gdk.ModifierType) bool
}

type wayfireOverviewItem struct {
	address     string
	title       string
	class       string
	appName     string
	icon        string
	monitor     string
	workspaceID int
	active      bool
	pid         int
}

func (s *shellUI) bindWayfireOverviewHandlers() {
	o := &s.wfOverview

	o.onCardClick = func(g gtk.GestureClick, _ int32, _, _ float64) {
		w := g.GetWidget()
		if w == nil {
			return
		}
		defer w.Unref()
		name := w.GetName()
		if strings.HasPrefix(name, "wf-window:") {
			addr := strings.TrimPrefix(name, "wf-window:")
			s.closeWayfireOverview(false)
			s.focusWindow(addr)
		}
	}

	o.onCardClose = func(b gtk.Button) {
		name := b.GetName()
		if strings.HasPrefix(name, "wf-close:") {
			addr := strings.TrimPrefix(name, "wf-close:")
			s.closeWayfireWindow(addr)
			s.removeWayfireWindowItem(addr)
		}
	}

	o.onCardHover = func(m gtk.EventControllerMotion, _, _ float64) {
		w := m.GetWidget()
		if w == nil {
			return
		}
		defer w.Unref()
		name := w.GetName()
		if strings.HasPrefix(name, "wf-window:") {
			addr := strings.TrimPrefix(name, "wf-window:")
			for idx, item := range o.windows {
				if item.address == addr {
					s.selectWayfireOverviewIndex(idx)
					break
				}
			}
		}
	}

	o.onWorkspaceClick = func(g gtk.GestureClick, _ int32, _, _ float64) {
		w := g.GetWidget()
		if w == nil {
			return
		}
		defer w.Unref()
		name := w.GetName()
		if strings.HasPrefix(name, "workspace:") {
			wsID, err := strconv.Atoi(strings.TrimPrefix(name, "workspace:"))
			if err == nil {
				s.switchWayfireWorkspace(wsID)
				s.closeWayfireOverview(false)
			}
		}
	}

	o.onBackdropClick = func(g gtk.GestureClick, _ int32, x, y float64) {
		w := g.GetWidget()
		if w == nil {
			return
		}
		defer w.Unref()
		picked := w.Pick(x, y, gtk.PickDefaultValue)
		if picked != nil {
			defer picked.Unref()
			if picked.HasCssClass("wayfire-overview-backdrop") || picked.HasCssClass("wayfire-overview-scrim") {
				s.closeWayfireOverview(true)
			}
		}
	}

	o.onDragPrepare = func(source gtk.DragSource, _, _ float64) gdk.ContentProvider {
		content := source.GetContent()
		if content == nil {
			return gdk.ContentProvider{}
		}
		return *content
	}

	o.onDragBegin = func(source gtk.DragSource, _ uintptr) {
		if w := source.GetWidget(); w != nil {
			w.AddCssClass("dragging")
			w.Unref()
		}
	}

	o.onDragEnd = func(source gtk.DragSource, _ uintptr, _ bool) {
		if w := source.GetWidget(); w != nil {
			w.RemoveCssClass("dragging")
			w.Unref()
		}
	}

	o.onDropMotion = func(dt gtk.DropTarget, _, _ float64) gdk.DragAction {
		if w := dt.GetWidget(); w != nil {
			w.AddCssClass("drop-target")
			w.Unref()
		}
		return gdk.ActionMoveValue
	}

	o.onDropLeave = func(dt gtk.DropTarget) {
		if w := dt.GetWidget(); w != nil {
			w.RemoveCssClass("drop-target")
			w.Unref()
		}
	}

	o.onDrop = func(dt gtk.DropTarget, _ uintptr, _, _ float64) bool {
		w := dt.GetWidget()
		if w == nil {
			return false
		}
		defer w.Unref()
		w.RemoveCssClass("drop-target")
		val := dt.GetValue()
		if val == nil {
			return false
		}
		addr := val.GetString()
		if addr == "" {
			return false
		}
		name := w.GetName()
		if !strings.HasPrefix(name, "workspace:") {
			return false
		}
		wsID, err := strconv.Atoi(strings.TrimPrefix(name, "workspace:"))
		if err != nil {
			return false
		}
		s.moveWayfireWindowToWorkspace(addr, wsID)
		return true
	}

	o.onKey = func(_ gtk.EventControllerKey, keyval, _ uint32, mods gdk.ModifierType) bool {
		if !o.open {
			return false
		}
		switch keyval {
		case keyEscape:
			s.closeWayfireOverview(true)
			return true
		case keyReturn, keyKPEnter, keySpace:
			s.commitWayfireOverviewSelection()
			return true
		case keyLeft, keyUp:
			s.stepWayfireOverview(-1)
			return true
		case keyRight, keyDown:
			s.stepWayfireOverview(1)
			return true
		case '1', '2', '3', '4':
			wsID := int(keyval - '0')
			s.switchWayfireWorkspace(wsID)
			s.closeWayfireOverview(false)
			return true
		case 0xffff: // Delete key
			s.closeWayfireSelectedWindow()
			return true
		case 'w', 'W':
			if mods&gdk.ControlMaskValue != 0 {
				s.closeWayfireSelectedWindow()
				return true
			}
		}
		return false
	}
}

func (s *shellUI) currentWayfireActiveWorkspace() int {
	if s.wayfireActiveWorkspace > 0 {
		return s.wayfireActiveWorkspace
	}
	focusedMon := s.snap.FocusedMonitor
	for _, m := range s.snap.Monitors {
		if m.Name == focusedMon && m.ActiveWorkspaceID > 0 {
			return m.ActiveWorkspaceID
		}
	}
	return 1
}

func (s *shellUI) moveWayfireWindowToWorkspace(address string, workspace int) {
	if s.wayfireWinWorkspaces == nil {
		s.wayfireWinWorkspaces = make(map[string]int)
	}
	s.wayfireWinWorkspaces[address] = workspace
	client := s.wayfire
	if client == nil {
		return
	}
	go func() {
		ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
		defer cancel()
		if err := client.SendWindowToWorkspace(ctx, address, workspace); err != nil {
			log.Printf("wayfire: send window %s to workspace %d: %v", address, workspace, err)
		}
	}()
	gtkx.Post(func() {
		if s.wfOverview.open {
			s.renderWayfireOverview()
		}
	})
}

func (s *shellUI) switchWayfireWorkspace(workspace int) {
	client := s.wayfire
	if client == nil {
		return
	}
	s.wayfireActiveWorkspace = workspace
	go func() {
		ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
		defer cancel()
		if err := client.SwitchWorkspace(ctx, workspace); err != nil {
			log.Printf("wayfire: switch workspace %d: %v", workspace, err)
		}
	}()
}

func (s *shellUI) showWayfireOverview() {
	if s.wfOverview.open {
		return
	}
	if s.wfSwitcher.open {
		s.closeWayfireSwitcher(false)
	}
	s.closeClipboard()
	s.closePasswords()

	o := &s.wfOverview
	o.open = true
	s.overview.st.Open = true
	s.syncOverviewDocks()

	focusedMon := s.snap.FocusedMonitor
	if focusedMon == "" && len(s.snap.Monitors) > 0 {
		focusedMon = s.snap.Monitors[0].Name
	}
	o.focusedMon = focusedMon
	o.cardWidgets = make(map[string]*gtk.Box)
	o.wsWidgets = make(map[int]*gtk.Box)

	activeWS := s.currentWayfireActiveWorkspace()

	var items []wayfireOverviewItem
	for _, t := range s.snap.Toplevels {
		if t.Address == "" {
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
		wsID := t.WorkspaceID
		if wsID <= 0 {
			wsID = activeWS
		}
		if override, ok := s.wayfireWinWorkspaces[t.Address]; ok && override > 0 {
			wsID = override
		}
		items = append(items, wayfireOverviewItem{
			address:     t.Address,
			title:       title,
			class:       t.Class,
			appName:     appName,
			icon:        iconName,
			monitor:     t.Monitor,
			workspaceID: wsID,
			active:      t.Activated || t.Address == s.snap.ActiveToplevel,
			pid:         t.PID,
		})
	}

	o.allWindows = items

	o.win = gtk.NewApplicationWindow(s.app)
	o.win.AddCssClass("overview")
	w := o.win.GoPointer()
	if s.layer {
		layershell.InitForWindow(w)
		layershell.SetNamespace(w, "inua-wayfire-overview")
		layershell.SetLayer(w, layershell.LayerTop)
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
		o.win.SetTitle(i18n.T("Activities Overview"))
		o.win.SetDefaultSize(1200, 800)
	}

	for _, m := range s.snap.Monitors {
		if m.Name == focusedMon {
			continue
		}
		scrimWin := gtk.NewApplicationWindow(s.app)
		scrimWin.AddCssClass("overview")
		sw := scrimWin.GoPointer()
		if s.layer {
			layershell.InitForWindow(sw)
			layershell.SetNamespace(sw, "inua-wayfire-overview-scrim")
			layershell.SetLayer(sw, layershell.LayerTop)
			layershell.SetKeyboardMode(sw, layershell.KeyboardNone)
			for _, e := range []layershell.Edge{layershell.EdgeTop, layershell.EdgeBottom, layershell.EdgeLeft, layershell.EdgeRight} {
				layershell.SetAnchor(sw, e, true)
			}
			layershell.SetExclusiveZone(sw, -1)
			for _, b := range s.bars {
				if b.connector() == m.Name {
					layershell.SetMonitor(sw, b.mon.GoPointer())
					break
				}
			}
		}
		scrimBox := gtk.NewBox(gtk.OrientationVerticalValue, 0)
		scrimBox.AddCssClass("wayfire-overview-scrim")
		scrimClick := gtk.NewGestureClick()
		scrimClick.ConnectReleased(&o.onBackdropClick)
		scrimBox.AddController(&scrimClick.EventController)
		scrimWin.SetChild(&scrimBox.Widget)
		scrimWin.Present()
		o.scrims = append(o.scrims, scrimWin)
	}

	root := gtk.NewBox(gtk.OrientationVerticalValue, 16)
	root.AddCssClass("wayfire-overview-backdrop")
	root.SetHalign(gtk.AlignFillValue)
	root.SetValign(gtk.AlignFillValue)
	rootClick := gtk.NewGestureClick()
	rootClick.ConnectReleased(&o.onBackdropClick)
	root.AddController(&rootClick.EventController)

	// Top Workspaces Bar
	o.workspacesBox = *gtk.NewBox(gtk.OrientationHorizontalValue, 16)
	o.workspacesBox.AddCssClass("wayfire-workspaces-bar")
	o.workspacesBox.SetHalign(gtk.AlignCenterValue)
	gtkx.Append(root, &o.workspacesBox.Widget)

	// Middle Windows Row (Scrolled)
	o.scroll = *gtk.NewScrolledWindow()
	o.scroll.AddCssClass("wayfire-windows-scroll")
	o.scroll.SetPolicy(gtk.PolicyAutomaticValue, gtk.PolicyNeverValue)
	o.scroll.SetPropagateNaturalHeight(true)
	o.scroll.SetVexpand(true)
	o.scroll.SetHexpand(true)

	o.windowsBox = *gtk.NewBox(gtk.OrientationHorizontalValue, 18)
	o.windowsBox.AddCssClass("wayfire-windows-row")
	o.windowsBox.SetHalign(gtk.AlignCenterValue)
	o.windowsBox.SetValign(gtk.AlignCenterValue)
	o.scroll.SetChild(&o.windowsBox.Widget)
	gtkx.Append(root, &o.scroll.Widget)

	// Bottom Hint Footer
	footer := gtk.NewBox(gtk.OrientationHorizontalValue, 16)
	footer.AddCssClass("wayfire-overview-footer")
	footer.SetHalign(gtk.AlignCenterValue)

	hintDrag := gtk.NewLabel(i18n.T("Drag window to workspace · Click to switch · 1..4 switch workspace · Esc close"))
	hintDrag.AddCssClass("wayfire-overview-status")
	gtkx.Append(footer, &hintDrag.Widget)
	gtkx.Append(root, &footer.Widget)

	keys := gtk.NewEventControllerKey()
	keys.SetPropagationPhase(gtk.PhaseCaptureValue)
	keys.ConnectKeyPressed(&o.onKey)
	o.win.AddController(&keys.EventController)

	o.win.SetChild(&root.Widget)
	o.win.Present()

	s.renderWayfireOverview()
}

func (s *shellUI) renderWayfireOverview() {
	o := &s.wfOverview
	gtkx.Clear(&o.workspacesBox)
	gtkx.Clear(&o.windowsBox)
	o.cardWidgets = make(map[string]*gtk.Box)
	o.wsWidgets = make(map[int]*gtk.Box)

	activeWS := s.currentWayfireActiveWorkspace()

	// 1. Build Top Workspaces Bar (Workspaces 1 to 4)
	wsCount := 4
	for i := 1; i <= wsCount; i++ {
		wsCard := gtk.NewBox(gtk.OrientationVerticalValue, 4)
		wsCard.SetName(fmt.Sprintf("workspace:%d", i))
		wsCard.AddCssClass("wayfire-workspace-card")
		if i == activeWS {
			wsCard.AddCssClass("active")
		}

		wsClick := gtk.NewGestureClick()
		wsClick.ConnectReleased(&o.onWorkspaceClick)
		wsCard.AddController(&wsClick.EventController)

		drop := gtk.NewDropTarget(types.GType(gobject.TypeStringVal), gdk.ActionMoveValue)
		drop.ConnectMotion(&o.onDropMotion)
		drop.ConnectLeave(&o.onDropLeave)
		drop.ConnectDrop(&o.onDrop)
		wsCard.AddController(&drop.EventController)

		// Workspace Header: number
		numLbl := gtk.NewLabel(strconv.Itoa(i))
		numLbl.AddCssClass("wayfire-workspace-num")
		numLbl.SetHalign(gtk.AlignCenterValue)
		gtkx.Append(wsCard, &numLbl.Widget)

		// Window Count in this workspace
		inWs := 0
		for _, w := range o.allWindows {
			if w.workspaceID == i {
				inWs++
			}
		}
		countLbl := gtk.NewLabel(i18n.Nf("%d window", "%d windows", inWs, inWs))
		countLbl.AddCssClass("wayfire-workspace-count")
		countLbl.SetHalign(gtk.AlignCenterValue)
		gtkx.Append(wsCard, &countLbl.Widget)

		o.wsWidgets[i] = wsCard
		gtkx.Append(&o.workspacesBox, &wsCard.Widget)
	}

	// 2. Filter windows on the current active workspace
	var currentWindows []wayfireOverviewItem
	for _, it := range o.allWindows {
		if it.workspaceID == activeWS {
			currentWindows = append(currentWindows, it)
		}
	}
	// If current workspace has no windows, show all windows so screen isn't empty
	if len(currentWindows) == 0 && len(o.allWindows) > 0 {
		currentWindows = o.allWindows
	}
	o.windows = currentWindows

	if len(o.windows) == 0 {
		empty := gtk.NewLabel(i18n.T("No open windows in this workspace"))
		empty.AddCssClass("overview-empty")
		empty.SetHalign(gtk.AlignCenterValue)
		empty.SetValign(gtk.AlignCenterValue)
		gtkx.Append(&o.windowsBox, &empty.Widget)
		return
	}

	// 3. Arrange windows horizontally from left to right (从左到右排列)
	for i, it := range o.windows {
		tile := s.buildWayfireWindowTile(it)
		o.cardWidgets[it.address] = tile
		gtkx.Append(&o.windowsBox, &tile.Widget)
		if i == o.selectedIndex {
			tile.AddCssClass("selected")
		}
	}
}

func (s *shellUI) buildWayfireWindowTile(it wayfireOverviewItem) *gtk.Box {
	tile := gtk.NewBox(gtk.OrientationVerticalValue, 8)
	tile.SetName("wf-window:" + it.address)
	tile.AddCssClass("wayfire-window-tile")
	tile.SetFocusable(true)
	tile.SetValign(gtk.AlignCenterValue)
	tile.SetHalign(gtk.AlignCenterValue)

	// Drag Source: allow dragging window tile to top workspaces bar
	var val gobject.Value
	val.Init(gobject.TypeStringVal)
	val.SetString(it.address)
	content := gdk.NewContentProviderForValue(&val)
	val.Unset()

	drag := gtk.NewDragSource()
	drag.SetActions(gdk.ActionMoveValue)
	drag.SetContent(content)
	content.Unref()

	drag.ConnectPrepare(&s.wfOverview.onDragPrepare)
	drag.ConnectDragBegin(&s.wfOverview.onDragBegin)
	drag.ConnectDragEnd(&s.wfOverview.onDragEnd)
	tile.AddController(&drag.EventController)

	// Click to activate
	click := gtk.NewGestureClick()
	click.ConnectReleased(&s.wfOverview.onCardClick)
	tile.AddController(&click.EventController)

	hover := gtk.NewEventControllerMotion()
	hover.ConnectEnter(&s.wfOverview.onCardHover)
	tile.AddController(&hover.EventController)

	// Top Bar: App Icon + App Name + Close Button
	topBar := gtk.NewBox(gtk.OrientationHorizontalValue, 10)
	topBar.SetValign(gtk.AlignCenterValue)

	icon := gtk.NewImage()
	setIcon(icon, it.icon)
	icon.SetPixelSize(38)
	icon.SetValign(gtk.AlignCenterValue)
	icon.SetCanTarget(false)
	gtkx.Append(topBar, &icon.Widget)

	appLbl := gtk.NewLabel(it.appName)
	appLbl.AddCssClass("wayfire-tile-app")
	appLbl.SetHalign(gtk.AlignStartValue)
	appLbl.SetHexpand(true)
	appLbl.SetEllipsize(3)
	appLbl.SetCanTarget(false)
	gtkx.Append(topBar, &appLbl.Widget)

	closeBtn := gtk.NewButton()
	closeBtn.SetName("wf-close:" + it.address)
	closeBtn.SetLabel("×")
	closeBtn.AddCssClass("wayfire-card-close")
	closeBtn.SetTooltipText(i18n.T("Close window"))
	closeBtn.SetValign(gtk.AlignStartValue)
	closeBtn.ConnectClicked(&s.wfOverview.onCardClose)
	gtkx.Append(topBar, &closeBtn.Widget)

	gtkx.Append(tile, &topBar.Widget)

	// Title
	titleLbl := gtk.NewLabel(it.title)
	titleLbl.AddCssClass("wayfire-tile-title")
	titleLbl.SetWrap(true)
	titleLbl.SetWrapMode(pango.WrapWordCharValue)
	titleLbl.SetLines(3)
	titleLbl.SetEllipsize(3)
	titleLbl.SetHalign(gtk.AlignStartValue)
	titleLbl.SetVexpand(true)
	titleLbl.SetCanTarget(false)
	gtkx.Append(tile, &titleLbl.Widget)

	// Footer: Active indicator & Monitor
	foot := gtk.NewBox(gtk.OrientationHorizontalValue, 8)
	foot.AddCssClass("wayfire-tile-footer")
	foot.SetValign(gtk.AlignCenterValue)

	if it.active {
		dot := gtk.NewBox(gtk.OrientationHorizontalValue, 0)
		dot.AddCssClass("mark")
		dot.AddCssClass("on")
		dot.SetSizeRequest(7, 7)
		dot.SetValign(gtk.AlignCenterValue)
		gtkx.Append(foot, &dot.Widget)

		actLbl := gtk.NewLabel(i18n.T("Active"))
		actLbl.AddCssClass("wayfire-card-active")
		gtkx.Append(foot, &actLbl.Widget)
	}

	if len(s.snap.Monitors) > 1 {
		monBadge := gtk.NewLabel(it.monitor)
		monBadge.AddCssClass("wayfire-card-mon")
		gtkx.Append(foot, &monBadge.Widget)
	}

	gtkx.Append(tile, &foot.Widget)
	return tile
}

func (s *shellUI) stepWayfireOverview(delta int) {
	o := &s.wfOverview
	n := len(o.windows)
	if n == 0 {
		return
	}
	newIdx := (o.selectedIndex + delta) % n
	if newIdx < 0 {
		newIdx += n
	}
	s.selectWayfireOverviewIndex(newIdx)
}

func (s *shellUI) selectWayfireOverviewIndex(idx int) {
	o := &s.wfOverview
	if idx < 0 || idx >= len(o.windows) {
		return
	}
	if o.selectedIndex >= 0 && o.selectedIndex < len(o.windows) {
		oldAddr := o.windows[o.selectedIndex].address
		if box, ok := o.cardWidgets[oldAddr]; ok && box != nil {
			box.RemoveCssClass("selected")
		}
	}
	o.selectedIndex = idx
	newAddr := o.windows[idx].address
	if box, ok := o.cardWidgets[newAddr]; ok && box != nil {
		box.AddCssClass("selected")
		box.GrabFocus()
	}
}

func (s *shellUI) commitWayfireOverviewSelection() {
	o := &s.wfOverview
	if len(o.windows) == 0 || o.selectedIndex < 0 || o.selectedIndex >= len(o.windows) {
		s.closeWayfireOverview(true)
		return
	}
	addr := o.windows[o.selectedIndex].address
	s.closeWayfireOverview(false)
	s.focusWindow(addr)
}

func (s *shellUI) closeWayfireSelectedWindow() {
	o := &s.wfOverview
	if len(o.windows) == 0 || o.selectedIndex < 0 || o.selectedIndex >= len(o.windows) {
		return
	}
	addr := o.windows[o.selectedIndex].address
	s.closeWayfireWindow(addr)
	s.removeWayfireWindowItem(addr)
}

func (s *shellUI) removeWayfireWindowItem(addr string) {
	o := &s.wfOverview
	o.allWindows = slices.DeleteFunc(o.allWindows, func(item wayfireOverviewItem) bool {
		return item.address == addr
	})
	o.windows = slices.DeleteFunc(o.windows, func(item wayfireOverviewItem) bool {
		return item.address == addr
	})
	if len(o.windows) == 0 {
		if len(o.allWindows) == 0 {
			s.closeWayfireOverview(false)
			return
		}
	}
	if o.selectedIndex >= len(o.windows) {
		o.selectedIndex = max(0, len(o.windows)-1)
	}
	s.renderWayfireOverview()
}

func (s *shellUI) closeWayfireOverview(restore bool) {
	o := &s.wfOverview
	if !o.open {
		return
	}
	o.open = false
	s.overview.st.Open = false
	s.syncOverviewDocks()

	for _, scrim := range o.scrims {
		if scrim != nil {
			scrim.Destroy()
			scrim.Unref()
		}
	}
	o.scrims = nil

	if o.win != nil {
		o.win.Destroy()
		o.refs.Release()
		o.win.Unref()
		o.win = nil
	}
	o.cardWidgets = nil
	o.wsWidgets = nil
	o.windows = nil
	o.allWindows = nil
}
