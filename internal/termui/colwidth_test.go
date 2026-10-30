package termui

import "testing"

// A column's width kept is within its limits; none kept is its first.
func TestColWidth(t *testing.T) {
	for _, c := range []struct{ col, w, want int }{
		{0, 0, 232}, {1, 0, 312},
		{0, 300, 300}, {0, 40, 180}, {0, 900, 420},
		{1, 100, 220}, {1, 700, 560},
	} {
		if got := colWidth(c.col, c.w); got != c.want {
			t.Errorf("colWidth(%d, %d) = %d, want %d", c.col, c.w, got, c.want)
		}
	}
}
