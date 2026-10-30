package viewer

import (
	"image"
	"image/draw"
)

// Upright is img as Viewer shows it: mirrored first when mirror is set,
// then turned a quarter clockwise turns times (as Orientation and the
// turns asked for give them), in pixels of its own.
func Upright(img image.Image, turns int, mirror bool) *image.RGBA {
	b := img.Bounds()
	src := image.NewRGBA(image.Rect(0, 0, b.Dx(), b.Dy()))
	draw.Draw(src, src.Bounds(), img, b.Min, draw.Src)
	turns = ((turns % 4) + 4) % 4
	if turns == 0 && !mirror {
		return src
	}
	w, h := b.Dx(), b.Dy()
	ow, oh := w, h
	if turns%2 == 1 {
		ow, oh = h, w
	}
	out := image.NewRGBA(image.Rect(0, 0, ow, oh))
	for y := range h {
		for x := range w {
			px, py, cw, ch := x, y, w, h
			if mirror {
				px = w - 1 - px
			}
			for range turns {
				px, py, cw, ch = ch-1-py, px, ch, cw // a quarter turn clockwise, y down
			}
			i, o := src.PixOffset(x, y), out.PixOffset(px, py)
			copy(out.Pix[o:o+4], src.Pix[i:i+4])
		}
	}
	return out
}
