package ui

import (
	"testing"
)

func TestRecordWayfireFocus(t *testing.T) {
	s := &shellUI{}
	s.recordWayfireFocus("wf:1")
	s.recordWayfireFocus("wf:2")
	s.recordWayfireFocus("wf:3")
	s.recordWayfireFocus("wf:2") // move wf:2 to front

	if len(s.wayfireMRU) != 3 {
		t.Fatalf("expected 3 items, got %d", len(s.wayfireMRU))
	}
	if s.wayfireMRU[0] != "wf:2" {
		t.Errorf("expected wf:2 at front, got %s", s.wayfireMRU[0])
	}
	if s.wayfireMRU[1] != "wf:3" {
		t.Errorf("expected wf:3 at index 1, got %s", s.wayfireMRU[1])
	}
	if s.wayfireMRU[2] != "wf:1" {
		t.Errorf("expected wf:1 at index 2, got %s", s.wayfireMRU[2])
	}
}

func TestWayfireSwitcherStep(t *testing.T) {
	s := &shellUI{
		wfSwitcher: wayfireSwitcher{
			open: true,
			windows: []wayfireOverviewItem{
				{address: "wf:1", title: "Firefox"},
				{address: "wf:2", title: "Ghostty"},
				{address: "wf:3", title: "Code"},
			},
			selectedIndex: 0,
		},
	}

	// Step forward
	s.stepWayfireSwitcher(1)
	if s.wfSwitcher.selectedIndex != 1 {
		t.Errorf("expected index 1, got %d", s.wfSwitcher.selectedIndex)
	}

	// Step backward
	s.stepWayfireSwitcher(-1)
	if s.wfSwitcher.selectedIndex != 0 {
		t.Errorf("expected index 0, got %d", s.wfSwitcher.selectedIndex)
	}

	// Step backward wraps around
	s.stepWayfireSwitcher(-1)
	if s.wfSwitcher.selectedIndex != 2 {
		t.Errorf("expected index 2, got %d", s.wfSwitcher.selectedIndex)
	}
}

func TestWayfireWorkspaceAssignment(t *testing.T) {
	s := &shellUI{
		wayfireWinWorkspaces: make(map[string]int),
	}
	s.moveWayfireWindowToWorkspace("wf:10", 3)
	if s.wayfireWinWorkspaces["wf:10"] != 3 {
		t.Errorf("expected wf:10 assigned to workspace 3, got %d", s.wayfireWinWorkspaces["wf:10"])
	}
}

func TestWayfireMRUSwap1And2(t *testing.T) {
	s := &shellUI{}
	// Windows opened in order: wf:1, wf:2, wf:3
	s.recordWayfireFocus("wf:1")
	s.recordWayfireFocus("wf:2")
	s.recordWayfireFocus("wf:3") // currently focused

	// MRU order: wf:3 (active), wf:2 (previous), wf:1 (older)
	if s.wayfireMRU[0] != "wf:3" || s.wayfireMRU[1] != "wf:2" || s.wayfireMRU[2] != "wf:1" {
		t.Fatalf("unexpected initial MRU: %v", s.wayfireMRU)
	}

	// User presses Alt+Tab: previous window is at index 1 (wf:2)
	target := s.wayfireMRU[1] // "wf:2"
	s.recordWayfireFocus(target)
	if s.wayfireMRU[0] != "wf:2" || s.wayfireMRU[1] != "wf:3" || s.wayfireMRU[2] != "wf:1" {
		t.Fatalf("expected wf:2 at front and wf:3 at index 1, got %v", s.wayfireMRU)
	}

	// User presses Alt+Tab again: previous window is now at index 1 (wf:3)
	target2 := s.wayfireMRU[1] // "wf:3"
	s.recordWayfireFocus(target2)
	if s.wayfireMRU[0] != "wf:3" || s.wayfireMRU[1] != "wf:2" || s.wayfireMRU[2] != "wf:1" {
		t.Fatalf("expected wf:3 at front and wf:2 at index 1, got %v", s.wayfireMRU)
	}

	// Repeated switching continues swapping #1 and #2
	s.recordWayfireFocus(s.wayfireMRU[1])
	if s.wayfireMRU[0] != "wf:2" || s.wayfireMRU[1] != "wf:3" {
		t.Fatalf("expected wf:2 and wf:3 to swap again, got %v", s.wayfireMRU)
	}
}
