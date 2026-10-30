package uikit

import (
	"sync"
	"unsafe"

	"codeberg.org/puregotk/purego"
	"codeberg.org/puregotk/puregotk/v4/gdk"
	"codeberg.org/puregotk/puregotk/v4/gobject"
	"codeberg.org/puregotk/puregotk/v4/gobject/types"
	"codeberg.org/puregotk/puregotk/v4/graphene"
	"codeberg.org/puregotk/puregotk/v4/gsk"
	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/gtkx"
)

// MenuAt is where a menu opens: under its trigger or above it, with an
// arrow at the trigger's middle, or at the pointer, without one.
type MenuAt int

const (
	Below MenuAt = iota
	Above
	AtPointer
)

// Radius is the menus' corners, style.radius: the shell and the apps set it
// with their style.
var Radius = 4

// A menu's frame draws its bubble round what it holds: the dock drawer's
// glass and hairline (BubblePath), the floating cards' shadow, and the
// arrow at its trigger. It keeps room round the card for the shadow and,
// on the trigger's side, for the arrow.
const (
	frameShadow = 14 // room for the shadow
	frameNear   = 3  // between the arrow's tip and the trigger
	frameInside = 6  // between the card's edge and the items
)

type frame struct {
	pop    *gtk.Popover
	canvas *gtk.Widget
	child  *gtk.Widget
	glass  *gtk.Widget // of no size, its colour the glass (style.css, .menu-frame-glass)
	at     MenuAt
}

var frames struct {
	once sync.Once
	isA  func(uintptr, types.GType) bool
	mu   sync.Mutex
	by   map[uintptr]*frame // by popover
}

// onMenuMap wraps what a menu holds in its frame, if it was set after
// Menu, and restarts its growing: GTK plays a CSS animation when the style
// first has it, so a popover kept between opens (Files', Mail's) would
// grow only once. Each show trades its animation for its twin of another
// name (grow-a, grow-b), which GTK starts afresh.
var onMenuMap = func(w gtk.Widget) {
	if f := frameOf(w.GoPointer()); f != nil {
		f.wrap()
	}
	if w.HasCssClass("grow-a") {
		w.RemoveCssClass("grow-a")
		w.AddCssClass("grow-b")
		return
	}
	w.RemoveCssClass("grow-b")
	w.AddCssClass("grow-a")
}

// onMenuDestroy lets a menu's frame go with it.
var onMenuDestroy = func(w gtk.Widget) {
	frames.mu.Lock()
	f := frames.by[w.GoPointer()]
	delete(frames.by, w.GoPointer())
	frames.mu.Unlock()
	if f != nil && f.canvas != nil {
		gtkx.ForgetCanvas(f.canvas)
	}
}

func frameOf(pop uintptr) *frame {
	frames.mu.Lock()
	defer frames.mu.Unlock()
	return frames.by[pop]
}

// Menu gives pop the look and motion of design/ui.md's menus: the glass
// in a hairline with the floating cards' shadow, corners of Radius and an
// arrow joined to the card by arcs, as the dock drawer's, growing out of
// where it opens; its items `.menu-item`. A GtkPopoverMenu keeps GTK's
// frame: its child is its own (NewMenu makes menus of items instead).
func Menu(pop *gtk.Popover, at MenuAt) {
	pop.AddCssClass("glass-menu")
	pop.SetHasArrow(false)
	switch at {
	case Below:
		pop.SetPosition(gtk.PosBottomValue)
	case Above:
		pop.AddCssClass("above")
		pop.SetPosition(gtk.PosTopValue)
	case AtPointer:
		pop.AddCssClass("at-pointer")
	}
	pop.ConnectMap(&onMenuMap)
	frames.once.Do(func() {
		h, err := gtkx.Open("libgobject-2.0.so.0")
		if err != nil {
			panic("uikit: " + err.Error())
		}
		// Keep the native pointer as uintptr across the FFI boundary.
		purego.RegisterLibFunc(&frames.isA, h, "g_type_check_instance_is_a")
	})
	if frames.isA(pop.GoPointer(), gtk.PopoverMenuGLibType()) {
		pop.AddCssClass("gtk-frame") // style.css: GTK's frame, in the glass
		return
	}
	f := &frame{pop: pop, at: at}
	frames.mu.Lock()
	if frames.by == nil {
		frames.by = map[uintptr]*frame{}
	}
	frames.by[pop.GoPointer()] = f
	frames.mu.Unlock()
	pop.ConnectDestroy(&onMenuDestroy)
	f.wrap()
}

// wrap puts the popover's child in the frame, once.
func (f *frame) wrap() {
	child := f.pop.GetChild()
	if child == nil || (f.canvas != nil && child.GoPointer() == f.canvas.GoPointer()) {
		return
	}
	if f.canvas != nil {
		gtkx.ForgetCanvas(f.canvas) // the child was set again
	}
	child.Ref()
	f.pop.SetChild(nil)
	f.child = child
	f.canvas = gtkx.NewCanvas(&gtkx.Canvas{Snapshot: f.snapshot, Allocate: f.allocate, Measure: f.measure})
	f.canvas.AddCssClass("menu-frame")
	child.SetParent(f.canvas)
	child.Unref() // the frame holds it
	glass := gtk.NewBox(gtk.OrientationHorizontalValue, 0)
	glass.AddCssClass("menu-frame-glass")
	glass.SetCanTarget(false)
	glass.SetParent(f.canvas)
	f.glass = &glass.Widget
	glass.Unref()
	f.pop.SetChild(f.canvas)
}

// side is where the arrow is: at the trigger, or none at the pointer.
func (f *frame) side() string {
	switch f.at {
	case Below:
		return "top"
	case Above:
		return "bottom"
	}
	return ""
}

// edges are the room round the card: left and right, above and below.
func (f *frame) edges() (side, top, bottom int) {
	side, top, bottom = frameShadow, frameShadow/2, frameShadow
	switch f.side() {
	case "top":
		top = frameNear + BubbleArrow
	case "bottom":
		bottom = frameNear + BubbleArrow
	}
	return
}

func (f *frame) measure(_ *gtk.Widget, o gtk.Orientation, forSize int) (int, int) {
	side, top, bottom := f.edges()
	var m, n int32
	if o == gtk.OrientationHorizontalValue {
		if forSize >= 0 {
			forSize = max(0, forSize-top-bottom-2*frameInside)
		}
		f.child.Measure(o, int32(forSize), &m, &n, nil, nil)
		extra := 2*side + 2*frameInside
		return int(m) + extra, int(n) + extra
	}
	if forSize >= 0 {
		forSize = max(0, forSize-2*side-2*frameInside)
	}
	f.child.Measure(o, int32(forSize), &m, &n, nil, nil)
	extra := top + bottom + 2*frameInside
	return int(m) + extra, int(n) + extra
}

// card is the bubble's box in the frame.
func (f *frame) card() (x, y, w, h float64) {
	side, top, bottom := f.edges()
	W, H := float64(f.canvas.GetWidth()), float64(f.canvas.GetHeight())
	return float64(side), float64(top), W - 2*float64(side), H - float64(top+bottom)
}

func (f *frame) allocate(_ *gtk.Widget, width, height int) {
	side, top, bottom := f.edges()
	w := max(0, width-2*side-2*frameInside)
	h := max(0, height-top-bottom-2*frameInside)
	t := gsk.NewTransform().Translate(&graphene.Point{X: float32(side + frameInside), Y: float32(top + frameInside)})
	f.child.Allocate(int32(w), int32(h), -1, t)
	f.glass.Allocate(0, 0, -1, nil)
}

// tip is where the trigger's middle is along the card's top or bottom, in
// the frame: the popup's place beside its parent's surface, from GTK.
func (f *frame) tip(cardX, cardW float64) float64 {
	middle := cardX + cardW/2
	parent := f.pop.GetParent()
	surface := f.pop.GetSurface()
	if parent == nil || surface == nil {
		return middle
	}
	var r gdk.Rectangle
	if !f.pop.GetPointingTo(&r) {
		r = gdk.Rectangle{Width: parent.GetWidth(), Height: parent.GetHeight()}
	}
	native := parent.GetNative()
	if native == nil {
		return middle
	}
	defer (&gobject.Object{Ptr: native.Ptr}).Unref() // GetNative returned a new reference
	root := gtk.WidgetNewFromInternalPtr(native.Ptr)
	var pb, fb graphene.Rect
	if !parent.ComputeBounds(root, &pb) || !f.canvas.ComputeBounds(&f.pop.Widget, &fb) {
		return middle
	}
	var nx, ny, px, py float64
	native.GetSurfaceTransform(&nx, &ny)
	f.pop.GetSurfaceTransform(&px, &py)
	popup := gdk.PopupBase{Ptr: surface.Ptr}
	trigger := nx + float64((*[4]float32)(unsafe.Pointer(&pb))[0]) + float64(r.X) + float64(r.Width)/2
	at := trigger - float64(popup.GetPositionX()) - px - float64((*[4]float32)(unsafe.Pointer(&fb))[0])
	return max(cardX, min(at, cardX+cardW))
}

func (f *frame) snapshot(_ *gtk.Widget, s *gtk.Snapshot) {
	x, y, w, h := f.card()
	if w <= 0 || h <= 0 {
		return
	}
	var glass, line gdk.RGBA
	f.glass.GetColor(&glass)
	f.canvas.GetColor(&line)
	r := float64(Radius)
	side := f.side()
	tip := x + w/2
	if side != "" {
		tip = f.tip(x, w)
	}
	shadow := gdk.RGBA{Alpha: 0.24}
	s.AppendOutsetShadow(RoundedRect(x, y, w, h, r), &shadow, 0, 4, 0, frameShadow-2)
	fill := BubblePath(x, y, w, h, r, side, tip)
	s.AppendFill(fill, gsk.FillRuleWindingValue, &glass)
	fill.Unref()
	stroke := gsk.NewStroke(1)
	edge := BubblePath(x+0.5, y+0.5, w-1, h-1, max(0, r-0.5), side, tip) // half a pixel in, so its pixels are whole
	s.AppendStroke(edge, stroke, &line)
	edge.Unref()
	stroke.Free()
	f.canvas.SnapshotChild(f.child, s)
}
