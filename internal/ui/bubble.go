package ui

import (
	"math"
	"time"

	"codeberg.org/puregotk/puregotk/v4/gdk"
	"codeberg.org/puregotk/puregotk/v4/glib"
	"codeberg.org/puregotk/puregotk/v4/graphene"
	"codeberg.org/puregotk/puregotk/v4/gsk"
	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/gtkx"
	"github.com/lyricat/inua/internal/uikit"
)

// bubble is the dock's drawer as a Dock folder opens on macOS: the card on
// glass of its own, a little way from the dock, with an arrow at the
// button it opened from. It grows out of the arrow's tip as it fades in,
// and shrinks back into it. The canvas fills the drawer's window and
// draws the glass, the arrow and the shadow round the card.
type bubble struct {
	canvas *gtk.Widget
	card   *gtk.Widget

	side       string  // the card's side the arrow is on: bottom, top, left or right
	tipX, tipY float64 // where the arrow points, in the window
	least      float64 // the least y of the card's top, under the bar
	radius     float64
	x, y, w, h float64 // the card's box
	glass      gdk.RGBA
	line       gdk.RGBA

	u       float64 // 0 hidden to 1 shown
	opening bool
	moving  bool
	last    time.Time
	tick    uint32
	gone    func()

	onTick     gtk.TickCallback
	onTickDone glib.DestroyNotify
}

const (
	bubbleArrow   = uikit.BubbleArrow // how far the arrow stands out from the card
	bubbleGap     = 5                 // between the arrow's tip and the dock
	bubbleOpenMS  = 200               // growing out of the tip
	bubbleCloseMS = 140               // and back into it
	bubbleFrom    = 0.55              // the size it grows from
)

// newBubble puts card in a canvas, the drawer window's whole content.
func newBubble(card *gtk.Widget, side string, tipX, tipY, least, radius float64) *bubble {
	b := &bubble{card: card, side: side, tipX: tipX, tipY: tipY, least: least, radius: radius}
	b.canvas = gtkx.NewCanvas(&gtkx.Canvas{Snapshot: b.snapshot, Allocate: b.allocate})
	b.canvas.SetHexpand(true)
	b.canvas.SetVexpand(true)
	card.SetParent(b.canvas)
	b.onTick = func(uintptr, uintptr, uintptr) bool { return b.step() }
	b.onTickDone = func(uintptr) { b.tick = 0 }
	return b
}

// colors reads the dock's glass and border from the theme, once the
// canvas is in a window.
func (b *bubble) colors() {
	sc := b.canvas.GetStyleContext()
	if !sc.LookupColor("glass", &b.glass) {
		b.glass = gdk.RGBA{Red: 0.95, Green: 0.95, Blue: 0.96, Alpha: 0.92}
	}
	if !sc.LookupColor("line", &b.line) {
		b.line = gdk.RGBA{Red: 0.5, Green: 0.5, Blue: 0.55, Alpha: 0.5}
	}
	b.line.Alpha *= 0.9 // as the dock's: alpha(@line, 0.9)
}

// forget lets the canvas go with its window.
func (b *bubble) forget() { gtkx.ForgetCanvas(b.canvas) }

// open grows the bubble out of its tip; with animations off it is there
// at once.
func (b *bubble) open() {
	b.colors()
	b.opening = true
	if !gtk.SettingsGetDefault().GetPropertyGtkEnableAnimations() {
		b.u = 1
		b.canvas.QueueDraw()
		return
	}
	b.u = 0
	b.start()
}

// close shrinks it back into its tip and calls gone once it is.
func (b *bubble) close(gone func()) {
	b.opening = false
	b.gone = gone
	if !gtk.SettingsGetDefault().GetPropertyGtkEnableAnimations() || b.u <= 0 {
		b.gone = nil
		gone()
		return
	}
	b.start()
}

func (b *bubble) start() {
	b.moving = true
	b.last = time.Now()
	if b.tick == 0 {
		b.tick = b.canvas.AddTickCallback(&b.onTick, 0, &b.onTickDone)
	}
}

// step moves it on a frame; a slow frame moves it on one frame's time at
// most, so it never jumps.
func (b *bubble) step() bool {
	now := time.Now()
	dt := min(float64(now.Sub(b.last).Milliseconds()), 34)
	b.last = now
	if b.opening {
		b.u = min(1, b.u+dt/bubbleOpenMS)
	} else {
		b.u = max(0, b.u-dt/bubbleCloseMS)
	}
	b.canvas.QueueDraw()
	if b.opening && b.u >= 1 {
		b.moving = false
		return false
	}
	if !b.opening && b.u <= 0 {
		b.moving = false
		if gone := b.gone; gone != nil {
			b.gone = nil
			gone()
		}
		return false
	}
	return true
}

// allocate places the card at its natural size beside the arrow, inside
// the window.
func (b *bubble) allocate(_ *gtk.Widget, width, height int) {
	var w, h int32
	b.card.Measure(gtk.OrientationHorizontalValue, -1, nil, &w, nil, nil)
	b.card.Measure(gtk.OrientationVerticalValue, w, nil, &h, nil, nil)
	b.w, b.h = float64(w), float64(h)
	clamp := func(v, lo, hi float64) float64 { return math.Round(max(lo, min(v, hi))) }
	W, H := float64(width), float64(height)
	switch b.side {
	case "top":
		b.x = clamp(b.tipX-b.w/2, drawerGap, W-drawerGap-b.w)
		b.y = math.Round(b.tipY + bubbleArrow)
	case "left":
		b.x = math.Round(b.tipX + bubbleArrow)
		b.y = clamp(b.tipY-b.h/2, b.least, H-drawerGap-b.h)
	case "right":
		b.x = math.Round(b.tipX - bubbleArrow - b.w)
		b.y = clamp(b.tipY-b.h/2, b.least, H-drawerGap-b.h)
	default: // bottom
		b.x = clamp(b.tipX-b.w/2, drawerGap, W-drawerGap-b.w)
		b.y = math.Round(b.tipY - bubbleArrow - b.h)
	}
	t := gsk.NewTransform().Translate(&graphene.Point{X: float32(b.x), Y: float32(b.y)})
	b.card.Allocate(w, h, -1, t)
}

func (b *bubble) snapshot(_ *gtk.Widget, s *gtk.Snapshot) {
	if b.u <= 0 {
		return
	}
	e := 1 - math.Pow(1-b.u, 3) // quick, then settling
	k := float32(bubbleFrom + (1-bubbleFrom)*e)
	tip := graphene.Point{X: float32(b.tipX), Y: float32(b.tipY)}
	s.Save()
	s.Translate(&tip)
	s.Scale(k, k)
	s.Translate(&graphene.Point{X: -tip.X, Y: -tip.Y})
	s.PushOpacity(min(1, e*1.3))

	shadow := gdk.RGBA{Alpha: 0.22}
	s.AppendOutsetShadow(uikit.RoundedRect(b.x, b.y, b.w, b.h, b.radius), &shadow, 0, 6, 0, 24)
	fill := b.path(0)
	s.AppendFill(fill, gsk.FillRuleWindingValue, &b.glass)
	fill.Unref()
	stroke := gsk.NewStroke(1)
	edge := b.path(0.5) // half a pixel in, so its pixels are whole
	s.AppendStroke(edge, stroke, &b.line)
	edge.Unref()
	stroke.Free()
	b.canvas.SnapshotChild(b.card, s)

	s.Pop()
	s.Restore()
}

// path is the card's rounded box with the arrow on its side, inset by in
// (uikit.BubblePath).
func (b *bubble) path(in float64) *gsk.Path {
	tip := b.tipX
	if b.side == "left" || b.side == "right" {
		tip = b.tipY
	}
	return uikit.BubblePath(b.x+in, b.y+in, b.w-2*in, b.h-2*in, max(0, b.radius-in), b.side, tip)
}
