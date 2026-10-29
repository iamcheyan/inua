package viewer

import (
	"image"
	"image/color"
	"testing"
)

// A 2×1 image, red then blue: turned and mirrored, the colours land where
// Viewer draws them.
func TestUpright(t *testing.T) {
	red, blue := color.RGBA{255, 0, 0, 255}, color.RGBA{0, 0, 255, 255}
	img := image.NewRGBA(image.Rect(0, 0, 2, 1))
	img.SetRGBA(0, 0, red)
	img.SetRGBA(1, 0, blue)
	for _, c := range []struct {
		turns  int
		mirror bool
		w, h   int
		first  color.RGBA // at (0, 0)
	}{
		{0, false, 2, 1, red},
		{0, true, 2, 1, blue},
		{1, false, 1, 2, red}, // turned clockwise: red on top
		{2, false, 2, 1, blue},
		{3, false, 1, 2, blue},
		{1, true, 1, 2, blue},
	} {
		out := Upright(img, c.turns, c.mirror)
		if out.Bounds().Dx() != c.w || out.Bounds().Dy() != c.h || out.RGBAAt(0, 0) != c.first {
			t.Errorf("turns %d mirror %v: %v, (0,0) %v", c.turns, c.mirror, out.Bounds(), out.RGBAAt(0, 0))
		}
	}
}
