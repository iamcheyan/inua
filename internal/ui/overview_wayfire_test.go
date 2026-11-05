package ui

import (
	"image"
	"testing"

	"github.com/lyricat/inua/internal/compositor"
)

// The overview's pictures are cut from the output's frame: the window's
// place, moved by the output's, scaled, and kept inside the frame.
func TestCropWindow(t *testing.T) {
	frame := image.NewRGBA(image.Rect(0, 0, 400, 300))
	out := compositor.Output{Name: "HDMI-1", X: 100, Y: 50, Width: 200, Height: 150, Scale: 2}
	for _, tc := range []struct {
		name    string
		win     compositor.Rect
		wantW   int
		wantH   int
		wantNil bool
	}{
		{name: "inside", win: compositor.Rect{X: 110, Y: 60, W: 50, H: 30}, wantW: 100, wantH: 60},
		{name: "over the left edge", win: compositor.Rect{X: 90, Y: 60, W: 50, H: 30}, wantW: 80, wantH: 60},
		{name: "over the right edge", win: compositor.Rect{X: 250, Y: 60, W: 100, H: 30}, wantW: 100, wantH: 60},
		{name: "larger than the output", win: compositor.Rect{X: 0, Y: 0, W: 1000, H: 1000}, wantW: 400, wantH: 300},
		{name: "empty", win: compositor.Rect{X: 110, Y: 60, W: 0, H: 30}, wantNil: true},
	} {
		got := cropWindow(frame, out, tc.win)
		if tc.wantNil {
			if got != nil {
				t.Errorf("%s: got %v, want nothing", tc.name, got.Bounds())
			}
			continue
		}
		if got == nil {
			t.Fatalf("%s: nothing", tc.name)
		}
		b := got.Bounds()
		if b.Dx() > tc.wantW || b.Dy() > tc.wantH {
			t.Errorf("%s: %dx%d, want at most %dx%d", tc.name, b.Dx(), b.Dy(), tc.wantW, tc.wantH)
		}
		if b.Dx() != tc.wantW || b.Dy() != tc.wantH {
			t.Errorf("%s: %dx%d, want %dx%d", tc.name, b.Dx(), b.Dy(), tc.wantW, tc.wantH)
		}
	}
}
