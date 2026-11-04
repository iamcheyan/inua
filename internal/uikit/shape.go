package uikit

import (
	"math"
	"unsafe"

	"codeberg.org/puregotk/puregotk/v4/gsk"
)

// The bubble's arrow (design/ui.md, Menus): how far it stands out from the
// card, the radius of the arcs that join it to the card's edge, as the
// arcs join a panel to the bar, and the radius of its tip.
const (
	BubbleArrow = 10
	BubbleJoin  = 12.0
	BubbleTip   = 3.0
)

// BubblePath is the dock drawer's and every menu's outline: the box x, y,
// w, h with corners of r, and the arrow on its side ("top", "right",
// "bottom", "left", or "" for none) pointing at tip, along that side, as
// nearly as the corners allow. It goes round clockwise from the top left
// corner.
func BubblePath(x, y, w, h, r float64, side string, tip float64) *gsk.Path {
	reach := float64(BubbleArrow) + BubbleJoin*(math.Sqrt2-1) // the arrow's half width at its base
	along := func(v, lo, hi float64) float64 { return max(lo+r+reach, min(v, hi-r-reach)) }
	pb := gsk.NewPathBuilder()
	pb.MoveTo(f32(x), f32(y+r))
	Arc(pb, x+r, y+r, r, 180, 270)
	if side == "top" {
		at := along(tip, x, x+w)
		caret(pb, func(u, v float64) (float64, float64) { return at + u, y - v })
	}
	Arc(pb, x+w-r, y+r, r, 270, 360)
	if side == "right" {
		at := along(tip, y, y+h)
		caret(pb, func(u, v float64) (float64, float64) { return x + w + v, at + u })
	}
	Arc(pb, x+w-r, y+h-r, r, 0, 90)
	if side == "bottom" {
		at := along(tip, x, x+w)
		caret(pb, func(u, v float64) (float64, float64) { return at - u, y + h + v })
	}
	Arc(pb, x+r, y+h-r, r, 90, 180)
	if side == "left" {
		at := along(tip, y, y+h)
		caret(pb, func(u, v float64) (float64, float64) { return x - v, at - u })
	}
	pb.Close()
	return pb.FreeToPath()
}

// caret draws the arrow, going on along the card's edge: at, through to,
// u along the edge the way the outline goes and v out from it, with the
// arrow's middle at u 0. Its sides are at 45°; an arc on each joins it to
// the edge, and its tip is round.
func caret(pb *gsk.PathBuilder, at func(u, v float64) (float64, float64)) {
	a, f, t := float64(BubbleArrow), BubbleJoin, BubbleTip
	q := 1 / math.Sqrt2
	// A curve from p to e, leaving p along dp and reaching e along de,
	// a circle's arc that turns by turn degrees.
	bend := func(pu, pv, du, dv, eu, ev, eu2, ev2, r, turn float64) {
		k := 4.0 / 3 * math.Tan(turn*math.Pi/180/4) * r
		x0, y0 := at(pu, pv)
		x1, y1 := at(pu+k*du, pv+k*dv)
		x2, y2 := at(eu-k*eu2, ev-k*ev2)
		x3, y3 := at(eu, ev)
		pb.LineTo(f32(x0), f32(y0))
		pb.CubicTo(f32(x1), f32(y1), f32(x2), f32(y2), f32(x3), f32(y3))
	}
	// Into the arrow: off the edge onto its first side, which goes out
	// along (q, q).
	c := -a - f*(math.Sqrt2-1)
	bend(c, 0, 1, 0, c+f*q, f-f*q, q, q, f, 45)
	// Round the tip, from the first side onto the second, along (q, -q).
	tv := a - t*math.Sqrt2
	bend(-t*q, tv+t*q, q, q, t*q, tv+t*q, q, -q, t, 90)
	// Off the second side back onto the edge.
	c = a + f*(math.Sqrt2-1)
	bend(c-f*q, f-f*q, q, -q, c, 0, 1, 0, f, 45)
}

// Arc goes round the circle about cx, cy from angle a0 to a1, in degrees
// clockwise from the right as the screen's y runs down, as a cubic; a
// quarter at most. It does nothing for a radius under half a pixel.
func Arc(pb *gsk.PathBuilder, cx, cy, r, a0, a1 float64) {
	if r < 0.5 {
		return
	}
	t0, t1 := a0*math.Pi/180, a1*math.Pi/180
	k := 4.0 / 3 * math.Tan((t1-t0)/4) * r
	x0, y0 := cx+r*math.Cos(t0), cy+r*math.Sin(t0)
	x1, y1 := cx+r*math.Cos(t1), cy+r*math.Sin(t1)
	pb.LineTo(f32(x0), f32(y0))
	pb.CubicTo(f32(x0-k*math.Sin(t0)), f32(y0+k*math.Cos(t0)), f32(x1+k*math.Sin(t1)), f32(y1-k*math.Cos(t1)), f32(x1), f32(y1))
}

// RoundedRect is a box with every corner rounded by r, for a shadow.
// puregotk declares GskRoundedRect with pointer fields; the C struct is
// twelve floats: the bounds, then each corner's width and height from the
// top left round.
func RoundedRect(x, y, w, h, r float64) *gsk.RoundedRect {
	q := float32(r)
	v := new([12]float32)
	*v = [12]float32{float32(x), float32(y), float32(w), float32(h), q, q, q, q, q, q, q, q}
	return (*gsk.RoundedRect)(unsafe.Pointer(v))
}

func f32(v float64) float32 { return float32(v) }
