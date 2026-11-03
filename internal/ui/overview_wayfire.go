package ui

import (
	"context"
	"fmt"
	"log"
	"os"
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
	"github.com/lyricat/inua/internal/hypr"
	"github.com/lyricat/inua/internal/i18n"
	"github.com/lyricat/inua/internal/layershell"
)

// How large the overview draws each window's picture, and what it asks the
// compositor for: a little larger than the card so the crop stays sharp.
const (
	wayfireTileThumbW = 320
	wayfireTileThumbH = 180
	wayfireThumbW     = 640
	wayfireThumbH     = 360
)

type wayfireOverview struct {
	open          bool
	win           *gtk.ApplicationWindow
	scrims        []*gtk.ApplicationWindow
	focusedMon    string
	allWindows    []wayfireOverviewItem
	windows       []wayfireOverviewItem
	selectedIndex int
	workspacesBox *gtk.Box
	windowsBox    *gtk.Box
	scroll        *gtk.ScrolledWindow
	refs          gtkx.Scope
	// pending holds each window's picture view until its capture arrives.
	pending map[string]*gtk.Picture

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
	if s.wfOverview.open || s.wfSwitcher.open {
		return
	}
	s.closeClipboard()
	s.closePasswords()

	if s.cfg.Overview.Style == "icons" {
		s.openWayfireSwitcher(0)
		return
	}

	o := &s.wfOverview
	o.open = true
	s.overview.st.Open = true
	s.syncOverviewDocks()

	focusedMon := s.snap.FocusedMonitor
	if focusedMon == "" && len(s.snap.Monitors) > 0 {
		focusedMon = s.snap.Monitors[0].Name
	}
	o.focusedMon = focusedMon

	o.pending = make(map[string]*gtk.Picture)

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

	// Top Workspaces Bar. gtkx.Append unsinks and drops the reference it
	// is handed, so the box keeps one of its own for every render.
	workspacesBox := gtk.NewBox(gtk.OrientationHorizontalValue, 16)
	workspacesBox.AddCssClass("wayfire-workspaces-bar")
	workspacesBox.SetHalign(gtk.AlignCenterValue)
	workspacesBox.Ref()
	o.refs.Track(&workspacesBox.Widget)
	o.workspacesBox = workspacesBox
	gtkx.Append(root, &workspacesBox.Widget)

	// Middle Windows Row (Scrolled)
	scroll := gtk.NewScrolledWindow()
	o.scroll = scroll
	scroll.AddCssClass("wayfire-windows-scroll")
	scroll.SetPolicy(gtk.PolicyAutomaticValue, gtk.PolicyNeverValue)
	scroll.SetPropagateNaturalHeight(true)
	scroll.SetVexpand(true)
	scroll.SetHexpand(true)

	windowsBox := gtk.NewBox(gtk.OrientationHorizontalValue, 18)
	windowsBox.AddCssClass("wayfire-windows-row")
	windowsBox.SetHalign(gtk.AlignCenterValue)
	windowsBox.SetValign(gtk.AlignCenterValue)
	windowsBox.Ref()
	o.refs.Track(&windowsBox.Widget)
	o.windowsBox = windowsBox
	scroll.SetChild(&windowsBox.Widget)
	gtkx.Append(root, &scroll.Widget)

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
	// Unparent, then drop: the cards' own widgets are also held by a Fixed
	// or an Overlay, so a bare Unref here would dispose one still parented.
	for _, box := range []*gtk.Box{o.workspacesBox, o.windowsBox} {
		for child := box.GetFirstChild(); child != nil; child = box.GetFirstChild() {
			child.Unparent()
			child.Unref()
		}
	}

	activeWS := s.currentWayfireActiveWorkspace()

	// 1. The workspaces. With thumbnails, each is the wallpaper with its
	// windows drawn where they sit; with icons, a plain card of the
	// applications' icons, as the Mac's Mission Control shows them.
	activeMon := s.snap.FocusedMonitor
	if activeMon == "" && len(s.snap.Monitors) > 0 {
		activeMon = s.snap.Monitors[0].Name
	}
	wsW, wsH := wayfireWorkspaceThumbSize(s.snap.Monitors, activeMon)
	iconsOnly := s.cfg.Overview.Style == "icons"
	for i := 1; i <= 4; i++ {
		card := gtk.NewOverlay()
		card.SetName(fmt.Sprintf("workspace:%d", i))
		card.AddCssClass("wayfire-workspace-thumb")
		if iconsOnly {
			card.AddCssClass("icons")
		}
		card.SetSizeRequest(wsW, wsH)
		if i == activeWS {
			card.AddCssClass("active")
		}

		click := gtk.NewGestureClick()
		click.ConnectReleased(&o.onWorkspaceClick)
		card.AddController(&click.EventController)

		drop := gtk.NewDropTarget(types.GType(gobject.TypeStringVal), gdk.ActionMoveValue)
		drop.ConnectMotion(&o.onDropMotion)
		drop.ConnectLeave(&o.onDropLeave)
		drop.ConnectDrop(&o.onDrop)
		card.AddController(&drop.EventController)

		inWs := 0
		for _, it := range o.allWindows {
			if it.workspaceID == i {
				inWs++
			}
		}
		if iconsOnly {
			grid := wayfireWorkspaceIcons(o.allWindows, i, wsW, wsH)
			card.SetChild(&grid.Widget)
			grid.Unref()
		} else {
			wall := gtk.NewPicture()
			wall.AddCssClass("wayfire-workspace-wallpaper")
			wall.SetContentFit(gtk.ContentFitCoverValue)
			wall.SetCanShrink(true)
			if path := s.overviewWallpaper(); path != "" {
				if setPictureFile(wall, path) != nil {
					log.Printf("wayfire overview: wallpaper %s", path)
				}
			}
			card.SetChild(&wall.Widget)
			wall.Unref()

			board := *gtk.NewFixed()
			card.AddOverlay(&board.Widget)
			for _, it := range o.allWindows {
				if it.workspaceID != i {
					continue
				}
				s.addWayfireOverviewWindow(&board, it, wsW, wsH)
			}
			board.Unref()
		}

		head := gtk.NewBox(gtk.OrientationHorizontalValue, 6)
		head.AddCssClass("wayfire-workspace-head")
		head.SetHalign(gtk.AlignStartValue)
		head.SetValign(gtk.AlignStartValue)
		numLbl := gtk.NewLabel(strconv.Itoa(i))
		numLbl.AddCssClass("wayfire-workspace-num")
		gtkx.Append(head, &numLbl.Widget)
		if inWs > 0 {
			countLbl := gtk.NewLabel(i18n.Nf("%d window", "%d windows", inWs, inWs))
			countLbl.AddCssClass("wayfire-workspace-count")
			gtkx.Append(head, &countLbl.Widget)
		}
		card.AddOverlay(&head.Widget)
		head.Unref()

		cardWidget := &card.Widget
		gtkx.Append(o.workspacesBox, cardWidget)
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
		gtkx.Append(o.windowsBox, &empty.Widget)
		return
	}

	// 3. Arrange windows horizontally from left to right (从左到右排列)
	for i, it := range o.windows {
		tile := s.buildWayfireWindowTile(it)
		if i == o.selectedIndex {
			tile.AddCssClass("selected")
		}
		// gtkx.Append unsinks and releases what it is handed; the tree
		// holds the card from here, so ask the map for it by address
		// rather than keeping a wrapper of our own.
		tileWidget := &tile.Widget
		gtkx.Append(o.windowsBox, tileWidget)
	}

	s.captureWayfireOverviewThumbs(o)
}

// captureWayfireOverviewThumbs fills in the pictures of the windows on show.
// One frame per output serves every window on it: windowThumbnails cuts each
// window out of the same capture, so a handful of cards costs one grim run
// per monitor. A window that has a picture already keeps it, which is the
// one taken while it was on top.
func (s *shellUI) captureWayfireOverviewThumbs(o *wayfireOverview) {
	if s.cfg.Overview.Style == "icons" || len(o.pending) == 0 {
		return
	}
	var wanted []hypr.Toplevel
	for _, window := range s.snap.Toplevels {
		if _, ok := o.pending[window.Address]; ok {
			wanted = append(wanted, window)
		}
	}
	if len(wanted) == 0 {
		return
	}
	snapshot := s.snap
	// The overview covers the desktop it photographs: take the frame with
	// it out of the way, then put it back before the pictures are pinned to
	// the cards.
	o.win.SetVisible(false)
	go func() {
		// One frame turn: a layer surface hidden this frame is gone from
		// the next capture.
		time.Sleep(120 * time.Millisecond)
		ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()
		paths, err := s.windowThumbnails(ctx, snapshot, wanted, wayfireThumbW, wayfireThumbH)
		if err != nil {
			log.Printf("wayfire overview: capture: %v", err)
		}
		gtkx.Post(func() {
			if !o.open {
				return
			}
			o.win.SetVisible(true)
			if err != nil {
				return
			}
			for i, window := range wanted {
				if i >= len(paths) || paths[i] == "" {
					continue
				}
				address := window.Address
				s.wfThumbs[address] = paths[i]
				if picture := o.pending[address]; picture != nil {
					if setPictureFile(picture, paths[i]) == nil {
						delete(o.pending, address)
					}
				}
			}
		})
	}()
}

// overviewWallpaper is the picture behind a workspace's thumbnail: the
// wallpaper the desktop shows, or "" when a theme's texture stands in for it.
func (s *shellUI) overviewWallpaper() string {
	if !s.cfg.Background.Enable {
		return ""
	}
	if s.cfg.Background.Generate {
		return s.shownPicture()
	}
	if path := s.cfg.ImagePath(); path != "" {
		if _, err := os.Stat(path); err == nil {
			return path
		}
	}
	return ""
}

// wayfireWorkspaceThumbSize is how large a workspace's picture is drawn in
// the overview bar: the monitor's shape, wide enough to read a window.
func wayfireWorkspaceThumbSize(monitors []hypr.Monitor, name string) (int32, int32) {
	w, h := 1920.0, 1080.0
	for _, mon := range monitors {
		if mon.Name != name || mon.Width <= 0 || mon.Height <= 0 {
			continue
		}
		scale := max(mon.Scale, 1)
		w, h = float64(mon.Width)/scale, float64(mon.Height)/scale
	}
	const thumbW = 260.0
	return int32(thumbW), int32(thumbW * h / w)
}

// addWayfireOverviewWindow puts a window's picture where the window sits on
// its workspace's thumbnail. A window that has no capture yet keeps its
// place, drawn as its application's icon.
func (s *shellUI) addWayfireOverviewWindow(board *gtk.Fixed, it wayfireOverviewItem, cardW, cardH int32) {
	x, y, w, h := s.wayfireOverviewWindowRect(it, cardW, cardH)
	cell := gtk.NewOverlay()
	cell.AddCssClass("wayfire-workspace-window")
	cell.SetSizeRequest(w, h)
	cell.SetCanTarget(false)
	if path := s.wfThumbs[it.address]; path != "" {
		pic := gtk.NewPicture()
		pic.SetContentFit(gtk.ContentFitCoverValue)
		pic.SetCanShrink(true)
		if setPictureFile(pic, path) != nil {
			log.Printf("wayfire overview: window picture %s", path)
		}
		cell.SetChild(&pic.Widget)
		pic.Unref()
	} else {
		icon := gtk.NewImage()
		setIcon(icon, it.icon)
		icon.SetPixelSize(28)
		icon.AddCssClass("wayfire-workspace-window-icon")
		cell.SetChild(&icon.Widget)
		icon.Unref()
	}
	board.Put(&cell.Widget, float64(x), float64(y))
	cell.Unref()
}

// wayfireOverviewWindowRect maps a window's compositor geometry onto its
// workspace's thumbnail, which is the whole monitor.
func (s *shellUI) wayfireOverviewWindowRect(it wayfireOverviewItem, cardW, cardH int32) (x, y, w, h int32) {
	var mon hypr.Monitor
	found := false
	for _, candidate := range s.snap.Monitors {
		if candidate.Name == it.monitor {
			mon, found = candidate, true
			break
		}
	}
	if !found || mon.Width <= 0 || mon.Height <= 0 {
		return 0, 0, cardW, cardH
	}
	var gx, gy, gw, gh float64
	for _, window := range s.snap.Toplevels {
		if window.Address != it.address {
			continue
		}
		if geometry, ok := window.Raw["geometry"].([]any); ok && len(geometry) >= 4 {
			gx, _ = geometry[0].(float64)
			gy, _ = geometry[1].(float64)
			gw, _ = geometry[2].(float64)
			gh, _ = geometry[3].(float64)
		}
		break
	}
	if gw <= 0 || gh <= 0 {
		return 0, 0, cardW, cardH
	}
	scaleX := float64(cardW) / float64(mon.Width)
	scaleY := float64(cardH) / float64(mon.Height)
	x = int32(max(0, (gx-float64(mon.X))*scaleX))
	y = int32(max(0, (gy-float64(mon.Y))*scaleY))
	w = int32(max(16, min(gw*scaleX, float64(cardW-x))))
	h = int32(max(12, min(gh*scaleY, float64(cardH-y))))
	return x, y, w, h
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

	titleLbl := gtk.NewLabel(it.title)
	titleLbl.AddCssClass("wayfire-tile-app")
	titleLbl.SetHalign(gtk.AlignStartValue)
	titleLbl.SetHexpand(true)
	titleLbl.SetEllipsize(pango.EllipsizeEndValue)
	setTooltip(titleLbl.GoPointer(), it.title)
	titleLbl.SetCanTarget(false)
	gtkx.Append(topBar, &titleLbl.Widget)

	closeBtn := gtk.NewButton()
	closeBtn.SetName("wf-close:" + it.address)
	closeBtn.SetLabel("×")
	closeBtn.AddCssClass("wayfire-card-close")
	setTooltip(closeBtn.GoPointer(), i18n.T("Close window"))
	closeBtn.SetValign(gtk.AlignStartValue)
	closeBtn.ConnectClicked(&s.wfOverview.onCardClose)
	gtkx.Append(topBar, &closeBtn.Widget)

	gtkx.Append(tile, &topBar.Widget)

	// The window's own picture; its application's icon stands in until the
	// capture arrives. In icon style the icon is the card, with no capture
	// behind it: Wayfire cannot photograph a covered window.
	stage := gtk.NewOverlay()
	stage.AddCssClass("wayfire-tile-stage")
	stage.SetSizeRequest(wayfireTileThumbW, wayfireTileThumbH)
	stage.SetCanTarget(false)
	if s.cfg.Overview.Style == "icons" {
		iconOnly := gtk.NewImage()
		setIcon(iconOnly, it.icon)
		iconOnly.SetPixelSize(56)
		iconOnly.AddCssClass("wayfire-tile-icon")
		stage.SetChild(&iconOnly.Widget)
	} else {
		picture := gtk.NewPicture()
		picture.AddCssClass("wayfire-tile-thumb")
		picture.SetContentFit(gtk.ContentFitCoverValue)
		picture.SetCanShrink(true)
		picture.SetCanTarget(false)
		iconPlaceholder := gtk.NewImage()
		setIcon(iconPlaceholder, it.icon)
		iconPlaceholder.SetPixelSize(48)
		iconPlaceholder.AddCssClass("wayfire-tile-icon")
		iconPlaceholder.SetCanTarget(false)
		if path := s.wfThumbs[it.address]; path != "" {
			if setPictureFile(picture, path) != nil {
				log.Printf("wayfire overview: window picture %s", path)
			}
		} else {
			stage.SetChild(&iconPlaceholder.Widget)
			stage.AddOverlay(&picture.Widget)
			s.wfOverview.pending[it.address] = picture
		}
	}
	gtkx.Append(tile, &stage.Widget)

	// The application, under its window.
	appLbl := gtk.NewLabel(it.appName)
	appLbl.AddCssClass("wayfire-tile-app-sub")
	appLbl.SetHalign(gtk.AlignStartValue)
	appLbl.SetEllipsize(pango.EllipsizeEndValue)
	appLbl.SetCanTarget(false)
	gtkx.Append(tile, &appLbl.Widget)

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

// wayfireWorkspaceIcons draws a workspace's applications as icons in a
// grid, the same card with no capture behind it.
func wayfireWorkspaceIcons(items []wayfireOverviewItem, workspace int, w, h int32) *gtk.FlowBox {
	flow := gtk.NewFlowBox()
	flow.SetSelectionMode(gtk.SelectionNoneValue)
	flow.SetHomogeneous(true)
	flow.SetMaxChildrenPerLine(4)
	flow.SetColumnSpacing(8)
	flow.SetRowSpacing(8)
	flow.SetHalign(gtk.AlignCenterValue)
	flow.SetValign(gtk.AlignCenterValue)
	flow.SetSizeRequest(w, h)
	shown := 0
	for _, it := range items {
		if it.workspaceID != workspace {
			continue
		}
		img := gtk.NewImage()
		setIcon(img, it.icon)
		img.SetPixelSize(36)
		img.SetSizeRequest(48, 48)
		img.SetCanTarget(false)
		flow.Append(&img.Widget)
		shown++
	}
	if shown == 0 {
		empty := gtk.NewImage()
		setIcon(empty, "view-grid-symbolic")
		empty.SetPixelSize(24)
		empty.AddCssClass("wayfire-workspace-empty-icon")
		flow.Append(&empty.Widget)
	}
	return flow
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

// selectWayfireOverviewIndex moves the selection and draws it again: the
// cards belong to the window's tree, so the overview does not keep their
// wrappers, and a render is the one place that knows where each one is.
func (s *shellUI) selectWayfireOverviewIndex(idx int) {
	o := &s.wfOverview
	if idx < 0 || idx >= len(o.windows) || idx == o.selectedIndex {
		return
	}
	o.selectedIndex = idx
	s.renderWayfireOverview()
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
	if s.wfSwitcher.open {
		s.closeWayfireSwitcher(restore)
	}
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
	o.windows = nil
	o.allWindows = nil
}
