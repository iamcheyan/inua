package shell

import "testing"

func TestCellSpan(t *testing.T) {
	for px, want := range map[float64]int{0: 0, 29: 0, 31: 1, 60: 1, 359: 6, -60: 0} {
		if got := Cell(px); got != want {
			t.Errorf("Cell(%v) = %d, want %d", px, got, want)
		}
	}
	for px, want := range map[int]int{0: 1, 1: 1, 60: 1, 61: 2, 336: 6} {
		if got := Span(px); got != want {
			t.Errorf("Span(%d) = %d, want %d", px, got, want)
		}
	}
}

func TestGridRect(t *testing.T) {
	a := GridRect{0, 0, 9, 8}
	for _, c := range []struct {
		b    GridRect
		want bool
	}{
		{GridRect{9, 0, 9, 8}, false}, // side by side
		{GridRect{0, 8, 9, 8}, false}, // one under the other
		{GridRect{8, 7, 2, 2}, true},  // a corner shared
		{GridRect{2, 2, 1, 1}, true},  // inside
	} {
		if got := a.Overlaps(c.b); got != c.want || c.b.Overlaps(a) != c.want {
			t.Errorf("%v and %v: %v", a, c.b, got)
		}
	}
	if !a.Fits(nil) || a.Fits([]GridRect{{9, 0, 9, 8}, {3, 3, 1, 1}}) {
		t.Error("Fits")
	}
}

func TestFreeSpot(t *testing.T) {
	taken := []GridRect{{0, 0, 9, 8}, {9, 0, 9, 8}}
	// Room beside them on a page 30 columns wide; none on one of 20, so
	// under them.
	if got := FreeSpot(taken, 9, 9, 30); got != (GridRect{18, 0, 9, 9}) {
		t.Errorf("wide: %v", got)
	}
	if got := FreeSpot(taken, 9, 9, 20); got != (GridRect{0, 8, 9, 9}) {
		t.Errorf("narrow: %v", got)
	}
	// A gap between two is taken when the widget fits it.
	taken = []GridRect{{0, 0, 9, 8}, {20, 0, 9, 8}}
	if got := FreeSpot(taken, 9, 9, 30); got != (GridRect{9, 0, 9, 9}) {
		t.Errorf("gap: %v", got)
	}
	if got := FreeSpot(nil, 9, 9, 4); got != (GridRect{0, 0, 9, 9}) {
		t.Errorf("a page narrower than the widget: %v", got)
	}
}
