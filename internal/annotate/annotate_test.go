package annotate

import (
	"image"
	"image/color"
	"math"
	"testing"
)

func TestUndoRedo(t *testing.T) {
	var d Doc
	d.Add(Shape{Tool: Arrow})
	d.Add(Shape{Tool: Rect})
	if !d.Undo() || len(d.Shapes()) != 1 || !d.CanRedo() {
		t.Fatalf("undo: %+v", d)
	}
	if !d.Redo() || len(d.Shapes()) != 2 || d.Shapes()[1].Tool != Rect {
		t.Fatalf("redo: %+v", d)
	}
	d.Undo()
	d.Add(Shape{Tool: Pen}) // a new shape: the undone one is gone
	if d.CanRedo() || d.Redo() {
		t.Error("redo after a new shape")
	}
	d.Undo()
	d.Undo()
	if d.Undo() || !d.Empty() {
		t.Error("undo past the first")
	}
}

// Steps count in the order they were made, whatever is between them, and
// close up when one is undone.
func TestSteps(t *testing.T) {
	var d Doc
	d.Add(Shape{Tool: Step})
	d.Add(Shape{Tool: Arrow})
	if d.NextStep() != 2 {
		t.Errorf("next step %d", d.NextStep())
	}
	d.Add(Shape{Tool: Step})
	if d.StepNumber(0) != 1 || d.StepNumber(2) != 2 {
		t.Errorf("numbers %d %d", d.StepNumber(0), d.StepNumber(2))
	}
	d.Undo()
	if d.NextStep() != 2 {
		t.Errorf("after undo, next step %d", d.NextStep())
	}
}

// The head's ends are as far behind the tip as the head is long, on
// either side of the line.
func TestArrowHead(t *testing.T) {
	l, r := ArrowHead(Point{0, 0}, Point{100, 0}, 4)
	for _, p := range []Point{l, r} {
		if d := math.Hypot(p.X-100, p.Y); math.Abs(d-20) > 1e-9 {
			t.Errorf("head length %v", d)
		}
	}
	if l.Y*r.Y >= 0 {
		t.Errorf("ends on one side: %v %v", l, r)
	}
	// A short arrow's head is half of it.
	l, _ = ArrowHead(Point{0, 0}, Point{10, 0}, 4)
	if d := math.Hypot(l.X-10, l.Y); math.Abs(d-5) > 1e-9 {
		t.Errorf("short head %v", d)
	}
	if a, b := ArrowHead(Point{5, 5}, Point{5, 5}, 4); a != b {
		t.Error("an arrow of no length has a head")
	}
}

func TestBox(t *testing.T) {
	b := Box(Point{50.5, 80}, Point{10.2, -5}, image.Rect(0, 0, 40, 100))
	if b != image.Rect(10, 0, 40, 80) {
		t.Errorf("box %v", b)
	}
}

// Each block is one colour, the average of its pixels; the image around
// is left out.
func TestPixelated(t *testing.T) {
	src := image.NewRGBA(image.Rect(0, 0, 4, 2))
	for x := 0; x < 4; x++ {
		v := uint8(0)
		if x%2 == 1 {
			v = 200
		}
		for y := 0; y < 2; y++ {
			src.Set(x, y, color.RGBA{v, v, v, 255})
		}
	}
	out := Pixelated(src, image.Rect(0, 0, 4, 2), 2)
	if out.Bounds() != image.Rect(0, 0, 4, 2) {
		t.Fatalf("bounds %v", out.Bounds())
	}
	for x := 0; x < 4; x++ {
		if c := out.RGBAAt(x, 0); c.R != 100 || c.A != 255 {
			t.Errorf("pixel %d: %v", x, c)
		}
	}
}

func TestSizesFor(t *testing.T) {
	small, large := SizesFor(800, 600), SizesFor(3840, 2160)
	if !(large.Line > small.Line && large.Text > small.Text && small.Line >= 3) {
		t.Errorf("sizes %+v %+v", small, large)
	}
}
