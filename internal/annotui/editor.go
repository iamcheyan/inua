// Package annotui draws annotations (internal/annotate) over an image and
// takes the pointer to make them: the screenshot tool's area and Viewer's
// images share it. The host puts the layer over the image, tells it where
// the image is (SetView), shows its toolbar, and renders the image with
// its annotations at full size when it is done (Render).
package annotui

import (
	"image"
	"math"

	"codeberg.org/puregotk/puregotk/v4/gdk"
	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/annotate"
	"github.com/lyricat/inua/internal/gtkx"
)

// Editor is the annotations of one image and the layer that draws them.
type Editor struct {
	Doc annotate.Doc

	src    image.Image     // the image, for pixelating; nil: pixelate is not offered
	bounds image.Rectangle // where shapes may go, in the image's pixels
	sizes  annotate.Sizes
	tool   annotate.Tool // "": the pointer is the host's
	ink    int

	// The view: the image's point (x, y) is at (ox + x*scale, oy +
	// y*scale) on the layer.
	ox, oy, scale float64
	fit           bool // the view follows the layer: the whole image, centred

	canvas  *gtk.Widget
	cur     *annotate.Shape // being drawn
	pixels  map[pixelKey]*gdk.Texture
	bar     *toolbar
	textPop *gtk.Popover
	text    *gtk.Entry
	textAt  annotate.Point

	// Changed is told after each change to the shapes, the tool or the
	// ink: the host saves, shows Save, or redraws what it must.
	Changed func()

	onDragBegin, onDragUpdate, onDragEnd func(gtk.GestureDrag, float64, float64)
	onTextEnter                          func(gtk.Entry)
	onTextKey                            func(gtk.EventControllerKey, uint32, uint32, gdk.ModifierType) bool
	x0, y0                               float64
}

// pixelKey is a pixelated area, as made: its box and its blocks.
type pixelKey struct {
	r     image.Rectangle
	block int
}

// New is an editor for an image of the given size; src, when given, is the
// image itself, for pixelating, its bounds those of the image.
// The sizes are those of the whole image, whatever part of it bounds
// leaves to draw on.
func New(src image.Image, size image.Rectangle) *Editor {
	e := &Editor{src: src, bounds: size, sizes: annotate.SizesFor(size.Dx(), size.Dy()), scale: 1, pixels: map[pixelKey]*gdk.Texture{}}
	e.canvas = gtkx.NewCanvas(&gtkx.Canvas{
		Snapshot: func(_ *gtk.Widget, s *gtk.Snapshot) { e.snapshot(s) },
		Allocate: func(_ *gtk.Widget, w, h int) { e.allocated(w, h) },
	})
	e.canvas.SetCanTarget(false)
	e.canvas.SetCursorFromName("crosshair")

	drag := gtk.NewGestureDrag()
	drag.SetButton(1)
	e.onDragBegin = func(g gtk.GestureDrag, x, y float64) {
		if e.tool == "" {
			g.SetState(gtk.EventSequenceDeniedValue)
			return
		}
		g.SetState(gtk.EventSequenceClaimedValue)
		e.x0, e.y0 = x, y
		p := e.toImage(x, y)
		switch e.tool {
		case annotate.Text:
			e.askText(p, x, y)
		case annotate.Step:
			e.add(annotate.Shape{Tool: annotate.Step, Ink: e.ink, Points: []annotate.Point{p}})
		default:
			e.cur = &annotate.Shape{Tool: e.tool, Ink: e.ink, Points: []annotate.Point{p, p}}
		}
	}
	e.onDragUpdate = func(_ gtk.GestureDrag, dx, dy float64) {
		if e.cur == nil {
			return
		}
		p := e.toImage(e.x0+dx, e.y0+dy)
		switch e.cur.Tool {
		case annotate.Pen, annotate.Highlight:
			if last := e.cur.Points[len(e.cur.Points)-1]; math.Hypot(p.X-last.X, p.Y-last.Y) >= 1.5/e.scale {
				e.cur.Points = append(e.cur.Points, p)
			}
		default:
			e.cur.Points[1] = p
		}
		e.canvas.QueueDraw()
	}
	e.onDragEnd = func(gtk.GestureDrag, float64, float64) {
		s := e.cur
		e.cur = nil
		if s == nil {
			return
		}
		a, b := s.Points[0], s.Points[len(s.Points)-1]
		if s.Tool != annotate.Pen && s.Tool != annotate.Highlight && math.Hypot(b.X-a.X, b.Y-a.Y) < 3/e.scale {
			e.canvas.QueueDraw() // a click: nothing made
			return
		}
		e.add(*s)
	}
	drag.ConnectDragBegin(&e.onDragBegin)
	drag.ConnectDragUpdate(&e.onDragUpdate)
	drag.ConnectDragEnd(&e.onDragEnd)
	e.canvas.AddController(&drag.EventController)
	e.bar = newToolbar(e)
	return e
}

// SetSource gives the editor the image's pixels, for pixelating, once they
// are read.
func (e *Editor) SetSource(src image.Image) {
	e.src = src
	e.bar.sync()
}

// SetBounds limits where shapes may go and show, in the image's pixels.
func (e *Editor) SetBounds(r image.Rectangle) {
	if r == e.bounds {
		return
	}
	e.bounds = r
	e.canvas.QueueDraw()
}

// Layer is the widget to put over the image, as large as the view.
func (e *Editor) Layer() *gtk.Widget { return e.canvas }

// Toolbar is the tools, the inks, undo and redo, for the host to place;
// it may add its own buttons at the end.
func (e *Editor) Toolbar() *gtk.Box { return e.bar.box }

// SetView says where the image is on the layer: its top left at (ox, oy),
// scale layer pixels to its pixel.
func (e *Editor) SetView(ox, oy, scale float64) {
	if ox == e.ox && oy == e.oy && scale == e.scale {
		return
	}
	e.ox, e.oy, e.scale = ox, oy, scale
	e.canvas.QueueDraw()
}

// Fit has the view follow the layer's size: the whole image in it,
// centred, as a GtkPicture under it fitting its image ("contain") shows
// it.
func (e *Editor) Fit() {
	e.fit = true
	e.allocated(int(e.canvas.GetWidth()), int(e.canvas.GetHeight()))
}

func (e *Editor) allocated(w, h int) {
	if !e.fit || w <= 0 || h <= 0 {
		return
	}
	iw, ih := float64(e.bounds.Dx()), float64(e.bounds.Dy())
	scale := math.Min(float64(w)/iw, float64(h)/ih)
	e.SetView((float64(w)-iw*scale)/2-float64(e.bounds.Min.X)*scale, (float64(h)-ih*scale)/2-float64(e.bounds.Min.Y)*scale, scale)
}

// Typing says the words of a text are being typed: the host's keys wait.
func (e *Editor) Typing() bool { return e.textPop != nil && e.textPop.GetVisible() }

// Busy says a shape is being drawn now.
func (e *Editor) Busy() bool { return e.cur != nil }

// Tool is the tool chosen, "" for none.
func (e *Editor) Tool() annotate.Tool { return e.tool }

// SetTool chooses a tool; "" leaves the pointer to the host.
func (e *Editor) SetTool(t annotate.Tool) {
	if t == annotate.Pixelate && e.src == nil {
		t = "" // its pixels are not read yet
	}
	if e.textPop != nil && t != annotate.Text {
		e.textPop.Popdown()
	}
	e.tool = t
	e.canvas.SetCanTarget(t != "")
	e.bar.sync()
	e.changed()
}

// Undo and Redo take the last shape away, and put it back.
func (e *Editor) Undo() {
	if e.Doc.Undo() {
		e.after()
	}
}

func (e *Editor) Redo() {
	if e.Doc.Redo() {
		e.after()
	}
}

// Clear takes every shape away, the tool with them.
func (e *Editor) Clear() {
	e.Doc.Clear()
	e.cur = nil
	e.tool = ""
	e.canvas.SetCanTarget(false)
	e.after()
}

// Free lets the editor's textures and callbacks go with its widgets.
func (e *Editor) Free() {
	for k, t := range e.pixels {
		t.Unref()
		delete(e.pixels, k)
	}
	if e.textPop != nil {
		e.textPop.Unparent()
		e.textPop = nil
	}
	gtkx.ForgetCanvas(e.canvas)
}

func (e *Editor) add(s annotate.Shape) {
	e.Doc.Add(s)
	e.after()
}

func (e *Editor) after() {
	e.canvas.QueueDraw()
	e.bar.sync()
	e.changed()
}

func (e *Editor) changed() {
	if e.Changed != nil {
		e.Changed()
	}
}

// toImage is a layer point in the image's pixels, kept on the image.
func (e *Editor) toImage(x, y float64) annotate.Point {
	px := (x - e.ox) / e.scale
	py := (y - e.oy) / e.scale
	b := e.bounds
	return annotate.Point{
		X: math.Max(float64(b.Min.X), math.Min(px, float64(b.Max.X))),
		Y: math.Max(float64(b.Min.Y), math.Min(py, float64(b.Max.Y))),
	}
}

// askText asks for the words of a text at p, in an entry over the layer
// at (x, y); Enter puts them there, Escape or clicking away does not.
func (e *Editor) askText(p annotate.Point, x, y float64) {
	if e.textPop == nil {
		e.textPop = gtk.NewPopover()
		e.textPop.AddCssClass("annot-text-pop")
		e.textPop.SetHasArrow(false)
		e.textPop.SetPosition(gtk.PosBottomValue)
		e.text = gtk.NewEntry()
		e.text.SetWidthChars(24)
		e.textPop.SetChild(&e.text.Widget)
		e.textPop.SetParent(e.canvas)
		e.onTextEnter = func(gtk.Entry) {
			if t := e.text.GetText(); t != "" {
				e.add(annotate.Shape{Tool: annotate.Text, Ink: e.ink, Points: []annotate.Point{e.textAt}, Text: t})
			}
			e.textPop.Popdown()
		}
		e.text.ConnectActivate(&e.onTextEnter)
		keys := gtk.NewEventControllerKey()
		e.onTextKey = func(_ gtk.EventControllerKey, keyval, _ uint32, _ gdk.ModifierType) bool {
			if int32(keyval) == gdk.KEY_Escape {
				e.textPop.Popdown()
				return true
			}
			return false
		}
		keys.ConnectKeyPressed(&e.onTextKey)
		e.text.AddController(&keys.EventController)
	}
	e.textAt = p
	e.text.SetText("")
	e.textPop.SetPointingTo(&gdk.Rectangle{X: int32(x), Y: int32(y), Width: 1, Height: 1})
	e.textPop.Popup()
	e.text.GrabFocus()
}
