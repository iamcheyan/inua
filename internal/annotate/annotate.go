// Package annotate is what is drawn over a screenshot or an image to point
// at its parts: arrows, rectangles, freehand lines, text, a highlighter,
// pixelated areas and numbered steps, in the image's own pixels, with undo
// and redo. It does not import GTK: internal/annotui draws it and takes
// the pointer.
package annotate

import (
	"image"
	"image/color"
	"math"
)

// Tool is what a drag or a click on the image makes.
type Tool string

const (
	Arrow     Tool = "arrow"
	Rect      Tool = "rect"
	Pen       Tool = "pen"
	Text      Tool = "text"
	Highlight Tool = "highlight"
	Pixelate  Tool = "pixelate"
	Step      Tool = "step"
)

// Tools are the tools in the toolbar's order.
var Tools = []Tool{Arrow, Rect, Pen, Highlight, Text, Step, Pixelate}

// Point is a place in the image's pixels.
type Point struct{ X, Y float64 }

// Ink is a colour annotations are drawn in: part of the picture, so the
// same whatever the theme.
type Ink struct{ R, G, B float64 }

// Inks are the colours to choose from, the first the default: red, amber,
// green, blue, white and black.
var Inks = []Ink{
	{0.93, 0.26, 0.21},
	{0.98, 0.75, 0.18},
	{0.20, 0.72, 0.42},
	{0.18, 0.49, 0.95},
	{1, 1, 1},
	{0.08, 0.08, 0.09},
}

// Shape is one annotation. An arrow, a rectangle and a pixelated area are
// two points, from where the drag began to where it ended; a line (pen or
// highlighter) every point it went through; text and a step one point,
// text with its words.
type Shape struct {
	Tool   Tool
	Ink    int // into Inks
	Points []Point
	Text   string
}

// Doc is the annotations of one image, in the order they were made.
type Doc struct {
	shapes []Shape
	undone []Shape // the last undone last
}

// Add adds a shape; what was undone cannot be redone after it.
func (d *Doc) Add(s Shape) {
	d.shapes = append(d.shapes, s)
	d.undone = nil
}

// Undo takes the last shape away, to redo; it reports whether there was one.
func (d *Doc) Undo() bool {
	if len(d.shapes) == 0 {
		return false
	}
	d.undone = append(d.undone, d.shapes[len(d.shapes)-1])
	d.shapes = d.shapes[:len(d.shapes)-1]
	return true
}

// Redo puts back the last shape undone.
func (d *Doc) Redo() bool {
	if len(d.undone) == 0 {
		return false
	}
	d.shapes = append(d.shapes, d.undone[len(d.undone)-1])
	d.undone = d.undone[:len(d.undone)-1]
	return true
}

func (d *Doc) Shapes() []Shape { return d.shapes }
func (d *Doc) Empty() bool     { return len(d.shapes) == 0 }
func (d *Doc) CanUndo() bool   { return len(d.shapes) > 0 }
func (d *Doc) CanRedo() bool   { return len(d.undone) > 0 }

// Clear takes every shape away, for good.
func (d *Doc) Clear() { d.shapes, d.undone = nil, nil }

// NextStep is the number the next step will show: one more than the steps
// there are.
func (d *Doc) NextStep() int {
	n := 1
	for _, s := range d.shapes {
		if s.Tool == Step {
			n++
		}
	}
	return n
}

// StepNumber is the number shape i shows, a step: its place among the
// steps.
func (d *Doc) StepNumber(i int) int {
	n := 0
	for _, s := range d.shapes[:i+1] {
		if s.Tool == Step {
			n++
		}
	}
	return n
}

// Sizes are what an image of a given size draws its annotations at, in
// its pixels: the width of a line, of the highlighter, the size of text,
// a step's radius and a pixelated area's blocks. A large screenshot draws
// them larger, so they read the same once it is shown smaller.
type Sizes struct {
	Line, Marker, Text, Step, Block float64
}

// SizesFor is the sizes for an image w × h pixels.
func SizesFor(w, h int) Sizes {
	short := float64(min(w, h))
	line := math.Max(3, math.Round(short/280))
	return Sizes{
		Line:   line,
		Marker: line * 5,
		Text:   math.Max(16, math.Round(short/40)),
		Step:   math.Max(13, math.Round(short/70)),
		Block:  math.Max(8, math.Round(short/90)),
	}
}

// ArrowHead is the two ends of an arrow's head at b, for a line from a of
// the given width: as long as the line is wide, five times, and no longer
// than half the line.
func ArrowHead(a, b Point, width float64) (Point, Point) {
	dx, dy := b.X-a.X, b.Y-a.Y
	length := math.Hypot(dx, dy)
	if length == 0 {
		return b, b
	}
	head := math.Min(width*5, length/2)
	ux, uy := dx/length, dy/length
	const spread = 0.5 // radians either side of the line
	cos, sin := math.Cos(spread), math.Sin(spread)
	back := func(s float64) Point {
		rx := -ux*cos - uy*sin*s
		ry := -uy*cos + ux*sin*s
		return Point{b.X + rx*head, b.Y + ry*head}
	}
	return back(1), back(-1)
}

// Box is the rectangle two points span, as whole pixels, kept inside
// bounds.
func Box(a, b Point, bounds image.Rectangle) image.Rectangle {
	r := image.Rect(int(math.Floor(math.Min(a.X, b.X))), int(math.Floor(math.Min(a.Y, b.Y))),
		int(math.Ceil(math.Max(a.X, b.X))), int(math.Ceil(math.Max(a.Y, b.Y))))
	return r.Intersect(bounds)
}

// Pixelated is the part r of src made into blocks of block pixels, each
// the average of its pixels; r's own size, at r's place. Nothing in the
// blocks says what was under them.
func Pixelated(src image.Image, r image.Rectangle, block int) *image.RGBA {
	r = r.Intersect(src.Bounds())
	out := image.NewRGBA(r)
	if block < 1 {
		block = 1
	}
	for by := r.Min.Y; by < r.Max.Y; by += block {
		for bx := r.Min.X; bx < r.Max.X; bx += block {
			cell := image.Rect(bx, by, min(bx+block, r.Max.X), min(by+block, r.Max.Y))
			var sr, sg, sb, sa, n uint64
			for y := cell.Min.Y; y < cell.Max.Y; y++ {
				for x := cell.Min.X; x < cell.Max.X; x++ {
					cr, cg, cb, ca := src.At(x, y).RGBA()
					sr, sg, sb, sa = sr+uint64(cr), sg+uint64(cg), sb+uint64(cb), sa+uint64(ca)
					n++
				}
			}
			c := color.RGBA64{R: uint16(sr / n), G: uint16(sg / n), B: uint16(sb / n), A: uint16(sa / n)}
			for y := cell.Min.Y; y < cell.Max.Y; y++ {
				for x := cell.Min.X; x < cell.Max.X; x++ {
					out.Set(x, y, c)
				}
			}
		}
	}
	return out
}
