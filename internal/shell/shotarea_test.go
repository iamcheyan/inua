package shell

import "testing"

func TestHitArea(t *testing.T) {
	r := Rect{X: 100, Y: 100, W: 200, H: 100}
	for _, c := range []struct {
		x, y float64
		want AreaPart
	}{
		{50, 50, AreaOutside},
		{200, 150, AreaInside},
		{100, 100, AreaNW}, {300, 100, AreaNE}, {100, 200, AreaSW}, {304, 205, AreaSE},
		{200, 96, AreaN}, {200, 203, AreaS}, {97, 150, AreaW}, {300, 150, AreaE},
		{200, 80, AreaOutside}, {320, 150, AreaOutside},
	} {
		if got := HitArea(r, c.x, c.y); got != c.want {
			t.Errorf("HitArea(%v, %v) = %v, want %v", c.x, c.y, got, c.want)
		}
	}
	if got := HitArea(Rect{}, 0, 0); got != AreaOutside {
		t.Errorf("no area: %v", got)
	}
}

// Moved, it stays on the monitor; resized, an edge stops short of the
// other side, and the screen's edges hold.
func TestAdjustArea(t *testing.T) {
	r := Rect{X: 100, Y: 100, W: 200, H: 100}
	for _, c := range []struct {
		name   string
		part   AreaPart
		dx, dy float64
		want   Rect
	}{
		{"move", AreaInside, 50, -20, Rect{150, 80, 200, 100}},
		{"move past the edge", AreaInside, -500, 900, Rect{0, 500, 200, 100}},
		{"east", AreaE, 40, 30, Rect{100, 100, 240, 100}},
		{"north-west", AreaNW, -30, 20, Rect{70, 120, 230, 80}},
		{"west past the east", AreaW, 400, 0, Rect{292, 100, 8, 100}},
		{"south past the screen", AreaS, 0, 900, Rect{100, 100, 200, 500}},
	} {
		if got := AdjustArea(r, c.part, c.dx, c.dy, 800, 600); got != c.want {
			t.Errorf("%s: %+v, want %+v", c.name, got, c.want)
		}
	}
}

func TestFitArea(t *testing.T) {
	if got, ok := FitArea(Rect{700, 500, 300, 300}, 800, 600); !ok || got != (Rect{700, 500, 100, 100}) {
		t.Errorf("partly off: %+v %v", got, ok)
	}
	if _, ok := FitArea(Rect{900, 700, 100, 100}, 800, 600); ok {
		t.Error("an area off the monitor is kept")
	}
}

func TestNearAreaMiddle(t *testing.T) {
	r := Rect{X: 0, Y: 0, W: 400, H: 200}
	if !NearAreaMiddle(r, 210, 110) || NearAreaMiddle(r, 300, 100) || NearAreaMiddle(Rect{}, 0, 0) {
		t.Error("the middle is misplaced")
	}
}
