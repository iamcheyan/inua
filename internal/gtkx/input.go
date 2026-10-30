package gtkx

import (
	"sync"

	"codeberg.org/puregotk/purego"
	"codeberg.org/puregotk/puregotk/v4/gtk"
)

// The calls an input region needs; puregotk has no cairo_region_create.
var inputRegion struct {
	once    sync.Once
	create  func() uintptr
	rect    func(r *regionRect) uintptr
	union   func(region uintptr, r *regionRect)
	destroy func(r uintptr)
	set     func(surface, region uintptr)
}

// regionRect is cairo_rectangle_int_t.
type regionRect struct{ X, Y, Width, Height int32 }

// PassInput lets the pointer through a window to what is under it. The
// window must be realized; GTK keeps the region until it is set again.
func PassInput(w *gtk.Window) { passInput(w, nil) }

// PassInputRects limits input to the given rectangles in window coordinates.
func PassInputRects(w *gtk.Window, rects ...[4]int) {
	p := &inputRegion
	p.once.Do(func() {
		cairo, err := Open("libcairo.so.2")
		if err != nil {
			panic("gtkx: " + err.Error())
		}
		gtk4, err := Open("libgtk-4.so.1")
		if err != nil {
			panic("gtkx: " + err.Error())
		}
		purego.RegisterLibFunc(&p.create, cairo, "cairo_region_create")
		purego.RegisterLibFunc(&p.rect, cairo, "cairo_region_create_rectangle")
		purego.RegisterLibFunc(&p.union, cairo, "cairo_region_union_rectangle")
		purego.RegisterLibFunc(&p.destroy, cairo, "cairo_region_destroy")
		purego.RegisterLibFunc(&p.set, gtk4, "gdk_surface_set_input_region")
	})
	surface := w.GetSurface()
	if surface == nil {
		return
	}
	region := p.create()
	for _, r := range rects {
		rr := regionRect{int32(r[0]), int32(r[1]), int32(r[2]), int32(r[3])}
		p.union(region, &rr)
	}
	p.set(surface.GoPointer(), region)
	p.destroy(region)
}

// PassInputBut is PassInput but for a rectangle of the window, in its
// coordinates, which keeps the pointer: a card's, around which is only
// its shadow.
func PassInputBut(w *gtk.Window, x, y, width, height int) {
	passInput(w, &regionRect{int32(x), int32(y), int32(width), int32(height)})
}

func passInput(w *gtk.Window, keep *regionRect) {
	p := &inputRegion
	p.once.Do(func() {
		cairo, err := Open("libcairo.so.2")
		if err != nil {
			panic("gtkx: " + err.Error())
		}
		gtk4, err := Open("libgtk-4.so.1")
		if err != nil {
			panic("gtkx: " + err.Error())
		}
		purego.RegisterLibFunc(&p.create, cairo, "cairo_region_create")
		purego.RegisterLibFunc(&p.rect, cairo, "cairo_region_create_rectangle")
		purego.RegisterLibFunc(&p.destroy, cairo, "cairo_region_destroy")
		purego.RegisterLibFunc(&p.set, gtk4, "gdk_surface_set_input_region")
	})
	surface := w.GetSurface()
	if surface == nil {
		return
	}
	var r uintptr
	if keep != nil {
		r = p.rect(keep)
	} else {
		r = p.create()
	}
	p.set(surface.GoPointer(), r)
	p.destroy(r)
}
