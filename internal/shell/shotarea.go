package shell

// The screenshot tool's area stays after it is dragged out: its corners
// and edges resize it, its inside moves it, a click inside takes it. The
// tool opens with the area it had last, on the same monitor.

// AreaPart is where on an area the pointer is.
type AreaPart int

const (
	AreaOutside AreaPart = iota
	AreaInside
	AreaN
	AreaS
	AreaE
	AreaW
	AreaNE
	AreaNW
	AreaSE
	AreaSW
)

// areaGrip is how far either side of an edge, in logical pixels, takes
// the edge rather than the inside or the outside.
const areaGrip = 8

// AreaMin is the least width and height an area is resized to.
const AreaMin = 8

// HitArea is the part of r under (x, y): a corner, an edge, the inside, or
// outside it. An area too small to tell its parts apart is all corner
// from outside: it grows rather than moves.
func HitArea(r Rect, x, y float64) AreaPart {
	if r.Empty() {
		return AreaOutside
	}
	near := func(v, edge float64) bool { return v >= edge-areaGrip && v <= edge+areaGrip }
	inX := x >= r.X-areaGrip && x <= r.X+r.W+areaGrip
	inY := y >= r.Y-areaGrip && y <= r.Y+r.H+areaGrip
	if !inX || !inY {
		return AreaOutside
	}
	n, s := near(y, r.Y), near(y, r.Y+r.H)
	w, e := near(x, r.X), near(x, r.X+r.W)
	switch {
	case n && w:
		return AreaNW
	case n && e:
		return AreaNE
	case s && w:
		return AreaSW
	case s && e:
		return AreaSE
	case n:
		return AreaN
	case s:
		return AreaS
	case w:
		return AreaW
	case e:
		return AreaE
	case r.Contains(x, y):
		return AreaInside
	}
	return AreaOutside
}

// AdjustArea is r with part dragged by (dx, dy), kept on a monitor of the
// given size: the inside moves it whole, an edge or a corner moves those
// sides, never past the other side less AreaMin.
func AdjustArea(r Rect, part AreaPart, dx, dy, w, h float64) Rect {
	if part == AreaInside {
		r.X = max(0, min(r.X+dx, w-r.W))
		r.Y = max(0, min(r.Y+dy, h-r.H))
		return r
	}
	x0, y0, x1, y1 := r.X, r.Y, r.X+r.W, r.Y+r.H
	switch part {
	case AreaN, AreaNE, AreaNW:
		y0 = max(0, min(y0+dy, y1-AreaMin))
	case AreaS, AreaSE, AreaSW:
		y1 = min(h, max(y1+dy, y0+AreaMin))
	}
	switch part {
	case AreaW, AreaNW, AreaSW:
		x0 = max(0, min(x0+dx, x1-AreaMin))
	case AreaE, AreaNE, AreaSE:
		x1 = min(w, max(x1+dx, x0+AreaMin))
	}
	return Rect{X: x0, Y: y0, W: x1 - x0, H: y1 - y0}
}

// NearAreaMiddle says (x, y) is at the area's middle, where its camera
// shows: within a circle of a quarter of its shorter side, 26 to 60 px.
func NearAreaMiddle(r Rect, x, y float64) bool {
	if r.Empty() {
		return false
	}
	radius := max(26, min(60, min(r.W, r.H)/4))
	dx, dy := x-(r.X+r.W/2), y-(r.Y+r.H/2)
	return dx*dx+dy*dy <= radius*radius
}

// AreaCursor is the pointer's cursor name over a part.
func AreaCursor(part AreaPart) string {
	return map[AreaPart]string{
		AreaInside: "move",
		AreaN:      "n-resize", AreaS: "s-resize", AreaE: "e-resize", AreaW: "w-resize",
		AreaNE: "ne-resize", AreaNW: "nw-resize", AreaSE: "se-resize", AreaSW: "sw-resize",
	}[part]
}

// LastArea is the area the tool had last, and its monitor.
type LastArea struct {
	Monitor string `json:"monitor"`
	Rect
}

// FitArea is a remembered area on a monitor of the given size: kept on
// it, or none when nothing of it is left there.
func FitArea(r Rect, w, h float64) (Rect, bool) {
	x0, y0 := max(0, r.X), max(0, r.Y)
	x1, y1 := min(w, r.X+r.W), min(h, r.Y+r.H)
	fit := Rect{X: x0, Y: y0, W: x1 - x0, H: y1 - y0}
	return fit, !fit.Empty()
}
