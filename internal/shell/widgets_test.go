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
	// Apart: a clear cell from each other, across and corner to corner.
	for _, c := range []struct {
		b    GridRect
		want bool
	}{
		{GridRect{9, 0, 6, 4}, false}, // touching at the side
		{GridRect{10, 0, 6, 4}, true}, // a column between
		{GridRect{0, 8, 6, 4}, false}, // touching under it
		{GridRect{0, 9, 6, 4}, true},  // a row between
		{GridRect{9, 8, 2, 2}, false}, // corner to corner
		{GridRect{10, 9, 2, 2}, true}, // a cell between the corners
		{GridRect{2, 2, 1, 1}, false}, // inside
	} {
		if got := c.b.Apart([]GridRect{a}); got != c.want {
			t.Errorf("%v apart from %v: %v", c.b, a, got)
		}
	}
	if !a.Apart(nil) {
		t.Error("apart from none")
	}
}

func TestFreeSpot(t *testing.T) {
	taken := []GridRect{{0, 0, 6, 5}, {7, 0, 6, 5}}
	// Room beside them on a page 20 columns wide, a column clear; none
	// on one of 18, so under them, a row clear.
	if got := FreeSpot(taken, 6, 4, 20); got != (GridRect{14, 0, 6, 4}) {
		t.Errorf("wide: %v", got)
	}
	if got := FreeSpot(taken, 6, 4, 18); got != (GridRect{0, 6, 6, 4}) {
		t.Errorf("narrow: %v", got)
	}
	// A gap between two is taken when the widget fits it with a column
	// clear on each side.
	taken = []GridRect{{0, 0, 6, 5}, {15, 0, 6, 5}}
	if got := FreeSpot(taken, 6, 4, 24); got != (GridRect{7, 0, 6, 4}) {
		t.Errorf("gap: %v", got)
	}
	taken = []GridRect{{0, 0, 6, 5}, {13, 0, 6, 5}}
	if got := FreeSpot(taken, 6, 4, 20); got != (GridRect{0, 6, 6, 4}) {
		t.Errorf("a gap too narrow: %v", got)
	}
	if got := FreeSpot(nil, 6, 4, 4); got != (GridRect{0, 0, 6, 4}) {
		t.Errorf("a page narrower than the widget: %v", got)
	}
}
