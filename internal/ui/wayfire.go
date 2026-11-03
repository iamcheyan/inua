package ui

import (
	"context"
	"log"
	"maps"
	"slices"
	"strings"
	"time"

	"github.com/lyricat/inua/internal/compositor"
	"github.com/lyricat/inua/internal/gtkx"
	"github.com/lyricat/inua/internal/hypr"
	"github.com/lyricat/inua/internal/wayfire"
)

// startWayfire follows Wayfire's IPC view list for the Dock and window
// launcher. Its view IDs are what focus and close take.
func (s *shellUI) startWayfire() {
	client, err := wayfire.FromEnv()
	if err != nil {
		log.Printf("wayfire: %v", err)
		return
	}
	s.wayfire = client
	go followWayfire(client, func(snapshot compositor.Snapshot) {
		gtkx.Post(func() { s.applyWayfireSnapshot(snapshot) })
	})
}

func followWayfire(client *wayfire.Client, update func(compositor.Snapshot)) {
	ctx := context.Background()
	if _, err := client.Methods(ctx); err != nil {
		log.Printf("wayfire: %v", err)
	}
	refresh := func() {
		snapshot, err := client.Windows(ctx)
		if err != nil {
			log.Printf("wayfire: windows: %v", err)
			return
		}
		update(snapshot)
	}
	refresh()
	events, err := client.Events(ctx)
	if err != nil {
		log.Printf("wayfire: events: %v", err)
	}
	ticker := time.NewTicker(2 * time.Second)
	defer ticker.Stop()
	for {
		select {
		case _, ok := <-events:
			if !ok {
				events = nil
			}
			refresh()
		case <-ticker.C:
			refresh()
		}
	}
}

func (s *shellUI) applyWayfireSnapshot(snapshot compositor.Snapshot) {
	oldPID := focusedPID(s.snap)
	oldActive := s.snap.ActiveToplevel
	s.windowSnap = wayfireSnapshot(snapshot)
	s.snap = s.windowSnap
	if s.snap.ActiveToplevel != "" {
		s.recordWayfireFocus(s.snap.ActiveToplevel)
		// Only when focus moves: a picture is worth keeping until then,
		// and grim captures the whole output.
		if s.snap.ActiveToplevel != oldActive {
			s.captureWayfireThumbnail(s.snap.ActiveToplevel)
		}
	}
	maps.DeleteFunc(s.wfThumbs, func(address, _ string) bool {
		return !slices.ContainsFunc(s.windowSnap.Toplevels, func(t hypr.Toplevel) bool { return t.Address == address })
	})
	if s.menu.open && s.menu.pid != focusedPID(s.snap) {
		s.closeMenu()
	}
	if oldPID != focusedPID(s.snap) {
		s.syncAppMenu()
	}
	for _, b := range s.bars {
		b.setHypr(s, s.snap)
	}
	s.launcher.st.SetConnected(true)
	s.launcher.st.SetSnapshot(s.windowSnap)
	s.renderDocks()
	s.syncLauncher()
}

func wayfireSnapshot(snapshot compositor.Snapshot) hypr.Snapshot {
	out := hypr.Snapshot{
		ActiveToplevel: snapshot.ActiveToplevel,
		FocusedMonitor: snapshot.FocusedMonitor,
	}
	origins := map[string][2]float64{}
	for _, monitor := range snapshot.Monitors {
		origins[monitor.Name] = [2]float64{float64(monitor.X), float64(monitor.Y)}
		out.Monitors = append(out.Monitors, hypr.Monitor{
			ID: monitor.ID, Name: monitor.Name, Description: monitor.Description,
			X: monitor.X, Y: monitor.Y, Width: monitor.Width, Height: monitor.Height,
			Scale: monitor.Scale, Focused: monitor.Focused, ActiveWorkspaceID: monitor.ActiveWorkspaceID,
			Raw: map[string]any{"wayfire": true},
		})
	}
	for _, workspace := range snapshot.Workspaces {
		out.Workspaces = append(out.Workspaces, hypr.Workspace{
			ID: workspace.ID, Name: workspace.Name, Monitor: workspace.Monitor,
			Active: workspace.Active, Focused: workspace.Focused,
			HasFullscreen: workspace.HasFullscreen, Urgent: workspace.Urgent,
		})
	}
	toplevels := slices.Clone(snapshot.Toplevels)
	active := func(t compositor.Toplevel) bool {
		return t.Activated || t.Address == snapshot.ActiveToplevel
	}
	slices.SortStableFunc(toplevels, func(a, b compositor.Toplevel) int {
		if active(a) != active(b) {
			if active(a) {
				return -1
			}
			return 1
		}
		return strings.Compare(a.Address, b.Address)
	})
	for i, toplevel := range toplevels {
		history := i + 1
		if active(toplevel) {
			history = 0
			if out.ActiveToplevel == "" {
				out.ActiveToplevel = toplevel.Address
			}
		}
		origin := origins[toplevel.Monitor]
		out.Toplevels = append(out.Toplevels, hypr.Toplevel{
			Address: toplevel.Address, PID: toplevel.PID, Title: toplevel.Title,
			Class: toplevel.Class, WorkspaceID: toplevel.WorkspaceID, Monitor: toplevel.Monitor,
			Activated: active(toplevel),
			Raw: map[string]any{
				"focusHistoryID": float64(history),
				"geometry":       []any{origin[0] + float64(toplevel.GeometryX), origin[1] + float64(toplevel.GeometryY), float64(toplevel.GeometryWidth), float64(toplevel.GeometryHeight)},
			},
		})
	}
	return out
}

func (s *shellUI) focusWayfireWindow(address string) {
	client := s.wayfire
	if client == nil {
		log.Printf("wayfire: cannot focus %s without the IPC socket", address)
		return
	}
	go func() {
		ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
		defer cancel()
		if err := client.FocusWindow(ctx, address); err != nil {
			log.Printf("wayfire: focus %s: %v", address, err)
		}
	}()
}

func (s *shellUI) closeWayfireWindow(address string) {
	client := s.wayfire
	if client == nil {
		if strings.HasPrefix(address, "wf:") {
			log.Printf("wayfire: cannot close %s without the IPC socket", address)
			return
		}
		s.dispatch("closewindow address:" + address)
		return
	}
	go func() {
		ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
		defer cancel()
		if err := client.CloseWindow(ctx, address); err != nil {
			log.Printf("wayfire: close %s: %v", address, err)
		}
	}()
}

func (s *shellUI) recordWayfireFocus(address string) {
	if address == "" {
		return
	}
	s.wayfireMRU = slices.DeleteFunc(s.wayfireMRU, func(a string) bool { return a == address })
	s.wayfireMRU = append([]string{address}, s.wayfireMRU...)
}

// captureWayfireThumbnail waits for the compositor to finish focusing a
// window, then keeps that window's own picture for the dock preview.
func (s *shellUI) captureWayfireThumbnail(address string) {
	if address == "" {
		return
	}
	if s.wfThumbs == nil {
		s.wfThumbs = map[string]string{}
	}
	if s.wfThumbBusy == nil {
		s.wfThumbBusy = map[string]bool{}
	}
	if s.wfThumbBusy[address] {
		return
	}
	s.wfThumbBusy[address] = true
	snapshot := s.snap
	time.AfterFunc(350*time.Millisecond, func() {
		go func() {
			ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
			defer cancel()
			path := ""
			var err error
			for _, window := range snapshot.Toplevels {
				if window.Address != address {
					continue
				}
				var paths []string
				paths, err = s.windowThumbnails(ctx, snapshot, []hypr.Toplevel{window}, dockPreviewThumbWidth, dockPreviewThumbHeight)
				if err == nil && len(paths) == 1 {
					path = paths[0]
				}
				break
			}
			gtkx.Post(func() {
				s.wfThumbBusy[address] = false
				if path != "" {
					s.wfThumbs[address] = path
				}
			})
		}()
	})
}
