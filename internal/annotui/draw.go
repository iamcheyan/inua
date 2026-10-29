package annotui

import (
	"fmt"
	"image"
	"math"
	"strconv"
	"unsafe"

	"codeberg.org/puregotk/puregotk/v4/gdk"
	"codeberg.org/puregotk/puregotk/v4/glib"
	"codeberg.org/puregotk/puregotk/v4/graphene"
	"codeberg.org/puregotk/puregotk/v4/gsk"
	"codeberg.org/puregotk/puregotk/v4/gtk"
	"codeberg.org/puregotk/puregotk/v4/pango"

	"github.com/lyricat/inua/internal/annotate"
)

// The shapes as GSK draws them, in the image's pixels: the layer scales
// them to the view, Render draws them at full size.

func (e *Editor) snapshot(s *gtk.Snapshot) {
	s.Save()
	s.Translate(&graphene.Point{X: float32(e.ox), Y: float32(e.oy)})
	s.Scale(float32(e.scale), float32(e.scale))
	e.drawShapes(s)
	s.Restore()
}

// drawShapes draws every shape, and the one being drawn, clipped to the
// image.
func (e *Editor) drawShapes(s *gtk.Snapshot) {
	b := e.bounds
	s.PushClip(rect(float32(b.Min.X), float32(b.Min.Y), float32(b.Dx()), float32(b.Dy())))
	for i, sh := range e.Doc.Shapes() {
		e.drawShape(s, sh, e.Doc.StepNumber(i))
	}
	if e.cur != nil {
		e.drawShape(s, *e.cur, 0)
	}
	s.Pop()
}

func (e *Editor) drawShape(s *gtk.Snapshot, sh annotate.Shape, step int) {
	ink := annotate.Inks[sh.Ink]
	col := gdk.RGBA{Red: float32(ink.R), Green: float32(ink.G), Blue: float32(ink.B), Alpha: 1}
	z := e.sizes
	switch sh.Tool {
	case annotate.Arrow:
		a, b := sh.Points[0], sh.Points[1]
		l, r := annotate.ArrowHead(a, b, z.Line)
		// The line ends inside the head, so its round end does not show
		// past the tip.
		mid := annotate.Point{X: (l.X + r.X) / 2, Y: (l.Y + r.Y) / 2}
		stroke(s, line([]annotate.Point{a, mid}), z.Line, &col, gsk.LineCapRoundValue)
		pb := gsk.NewPathBuilder()
		pb.MoveTo(f32(b.X), f32(b.Y))
		pb.LineTo(f32(l.X), f32(l.Y))
		pb.LineTo(f32(r.X), f32(r.Y))
		pb.Close()
		head := pb.FreeToPath()
		s.AppendFill(head, gsk.FillRuleWindingValue, &col)
		stroke(s, head, z.Line/2, &col, gsk.LineCapRoundValue) // its corners a little round
	case annotate.Rect:
		r := box(sh.Points[0], sh.Points[1])
		pb := gsk.NewPathBuilder()
		pb.AddRect(rect(f32(r.X), f32(r.Y), f32(r.W), f32(r.H)))
		stroke(s, pb.FreeToPath(), z.Line, &col, gsk.LineCapSquareValue)
	case annotate.Pen:
		stroke(s, line(sh.Points), z.Line, &col, gsk.LineCapRoundValue)
	case annotate.Highlight:
		marker := col
		marker.Alpha = 0.38
		stroke(s, line(sh.Points), z.Marker, &marker, gsk.LineCapRoundValue)
	case annotate.Text:
		e.drawText(s, sh.Text, sh.Points[0], &col, ink)
	case annotate.Step:
		e.drawStep(s, sh.Points[0], step, &col, ink)
	case annotate.Pixelate:
		e.drawPixelated(s, sh)
	}
}

// line is a path through the points; one point is a dot.
func line(ps []annotate.Point) *gsk.Path {
	pb := gsk.NewPathBuilder()
	pb.MoveTo(f32(ps[0].X), f32(ps[0].Y))
	if len(ps) == 1 {
		pb.LineTo(f32(ps[0].X)+0.01, f32(ps[0].Y))
	}
	for _, p := range ps[1:] {
		pb.LineTo(f32(p.X), f32(p.Y))
	}
	return pb.FreeToPath()
}

// stroke draws a path with round joins; it takes the path.
func stroke(s *gtk.Snapshot, p *gsk.Path, width float64, c *gdk.RGBA, cap gsk.LineCap) {
	st := gsk.NewStroke(f32(width))
	st.SetLineCap(cap)
	st.SetLineJoin(gsk.LineJoinRoundValue)
	s.AppendStroke(p, st, c)
	st.Free()
	p.Unref()
}

// halo is the colour drawn round text and a step's number so they read on
// any picture: black round a light ink, white round a dark one.
func halo(ink annotate.Ink) (gdk.RGBA, bool) {
	light := 0.2126*ink.R+0.7152*ink.G+0.0722*ink.B > 0.6
	if light {
		return gdk.RGBA{Alpha: 0.85}, true
	}
	return gdk.RGBA{Red: 1, Green: 1, Blue: 1, Alpha: 0.9}, false
}

func (e *Editor) layout(text string, px float64) *pango.Layout {
	l := e.canvas.CreatePangoLayout(text)
	fd := pango.FontDescriptionFromString("IBM Plex Sans, Zen Kaku Gothic New, sans-serif Bold")
	fd.SetAbsoluteSize(px * float64(pango.SCALE))
	l.SetFontDescription(fd)
	fd.Free()
	return l
}

func (e *Editor) drawText(s *gtk.Snapshot, text string, at annotate.Point, col *gdk.RGBA, ink annotate.Ink) {
	l := e.layout(text, e.sizes.Text)
	defer l.Unref()
	s.Save()
	s.Translate(&graphene.Point{X: f32(at.X), Y: f32(at.Y)})
	pb := gsk.NewPathBuilder()
	pb.AddLayout(l)
	p := pb.FreeToPath()
	h, _ := halo(ink)
	stroke(s, p.Ref(), math.Max(2, e.sizes.Text/7), &h, gsk.LineCapRoundValue)
	s.AppendFill(p, gsk.FillRuleWindingValue, col)
	p.Unref()
	s.Restore()
}

// drawStep is a disc of the ink with the number in it, ringed in the
// number's colour.
func (e *Editor) drawStep(s *gtk.Snapshot, at annotate.Point, n int, col *gdk.RGBA, ink annotate.Ink) {
	if n == 0 {
		n = e.Doc.NextStep()
	}
	r := e.sizes.Step
	pb := gsk.NewPathBuilder()
	pb.AddCircle(&graphene.Point{X: f32(at.X), Y: f32(at.Y)}, f32(r))
	disc := pb.FreeToPath()
	s.AppendFill(disc, gsk.FillRuleWindingValue, col)
	ring, light := halo(ink)
	stroke(s, disc, math.Max(1.5, r/8), &ring, gsk.LineCapRoundValue)
	number := gdk.RGBA{Red: 1, Green: 1, Blue: 1, Alpha: 1}
	if light {
		number = gdk.RGBA{Red: 0.08, Green: 0.08, Blue: 0.09, Alpha: 1}
	}
	l := e.layout(strconv.Itoa(n), r*1.1)
	defer l.Unref()
	var ink2, logical pango.Rectangle
	l.GetPixelExtents(&ink2, &logical)
	s.Save()
	s.Translate(&graphene.Point{X: f32(at.X) - float32(ink2.X+ink2.Width/2), Y: f32(at.Y) - float32(ink2.Y+ink2.Height/2)})
	s.AppendLayout(l, &number)
	s.Restore()
}

// drawPixelated draws a pixelated area's blocks, made once.
func (e *Editor) drawPixelated(s *gtk.Snapshot, sh annotate.Shape) {
	if e.src == nil {
		return
	}
	r := annotate.Box(sh.Points[0], sh.Points[1], e.bounds)
	if r.Empty() {
		return
	}
	k := pixelKey{r, int(e.sizes.Block)}
	t := e.pixels[k]
	if t == nil {
		t = rgbaTexture(annotate.Pixelated(e.src, r, k.block))
		e.pixels[k] = t
	}
	s.AppendTexture(t, rect(float32(r.Min.X), float32(r.Min.Y), float32(r.Dx()), float32(r.Dy())))
}

type frect struct{ X, Y, W, H float64 }

func box(a, b annotate.Point) frect {
	return frect{math.Min(a.X, b.X), math.Min(a.Y, b.Y), math.Abs(b.X - a.X), math.Abs(b.Y - a.Y)}
}

// Render draws the image base with the annotations over it, the part crop
// of it at full size, with renderer: a new texture, to save or copy.
func (e *Editor) Render(renderer *gsk.Renderer, base *gdk.Texture, crop image.Rectangle) (*gdk.Texture, error) {
	s := gtk.NewSnapshot()
	s.Translate(&graphene.Point{X: -float32(crop.Min.X), Y: -float32(crop.Min.Y)})
	s.AppendTexture(base, rect(0, 0, float32(base.GetWidth()), float32(base.GetHeight())))
	e.drawShapes(s)
	node := s.FreeToNode()
	if node == nil {
		return nil, fmt.Errorf("nothing drawn")
	}
	defer node.Unref()
	tex := renderer.RenderTexture(node, rect(0, 0, float32(crop.Dx()), float32(crop.Dy())))
	if tex == nil {
		return nil, fmt.Errorf("rendering failed")
	}
	return tex, nil
}

// rgbaTexture makes a texture of RGBA pixels.
func rgbaTexture(px *image.RGBA) *gdk.Texture {
	b := glib.NewBytes(px.Pix, uint(len(px.Pix)))
	tex := gdk.NewMemoryTexture(int32(px.Rect.Dx()), int32(px.Rect.Dy()), gdk.MemoryR8g8b8a8PremultipliedValue, b, uint(px.Stride))
	b.Unref()
	return &tex.Texture
}

// rect builds a graphene_rect_t, which puregotk declares with two pointer
// fields; the C struct is four floats of the same size.
func rect(x, y, w, h float32) *graphene.Rect {
	var r graphene.Rect
	*(*[4]float32)(unsafe.Pointer(&r)) = [4]float32{x, y, w, h}
	return &r
}

func f32(v float64) float32 { return float32(v) }
