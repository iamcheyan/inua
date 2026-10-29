package shell

import (
	"math"
	"testing"
)

func TestDropEnds(t *testing.T) {
	for _, c := range []struct {
		u     float64
		open  bool
		shown float64
	}{
		{0, true, 0}, {1, true, 1}, {0, false, 1}, {1, false, 0},
	} {
		d := DropAt(c.u, c.open)
		if math.Abs(d.Shown-c.shown) > 1e-9 {
			t.Errorf("DropAt(%v, %v).Shown = %v, want %v", c.u, c.open, d.Shown, c.shown)
		}
		if c.shown == 1 && (math.Abs(d.ScaleX-1) > 1e-9 || math.Abs(d.ScaleY-1) > 1e-9) {
			t.Errorf("DropAt(%v, %v) = %+v, want it at rest", c.u, c.open, d)
		}
	}
}

// The panel never leaves the bar nor goes past its height, stretches a
// little at most, and no frame jumps.
func TestDropSoft(t *testing.T) {
	for _, open := range []bool{true, false} {
		prev := DropAt(0, open)
		stretched := false
		for i := 1; i <= 1000; i++ {
			d := DropAt(float64(i)/1000, open)
			if d.Shown < 0 || d.Shown > 1 {
				t.Fatalf("open %v at %d: shown %v", open, i, d.Shown)
			}
			if math.Abs(d.ScaleY-1) > dropStretch+1e-9 || math.Abs(d.ScaleX-1) > dropStretch {
				t.Fatalf("open %v at %d: stretched %+v", open, i, d)
			}
			stretched = stretched || d.ScaleY > 1.02
			for _, v := range []float64{d.Shown - prev.Shown, d.ScaleX - prev.ScaleX, d.ScaleY - prev.ScaleY} {
				if math.Abs(v) > 0.01 {
					t.Fatalf("open %v at %d: jumps from %+v to %+v", open, i, prev, d)
				}
			}
			prev = d
		}
		if !stretched {
			t.Errorf("open %v: never stretched", open)
		}
	}
}

// A width on its way starts at the old one, ends at the new, and moves
// only towards it.
func TestDropWidth(t *testing.T) {
	for _, c := range [][2]float64{{380, 520}, {520, 380}} {
		from, to := c[0], c[1]
		if got := DropWidth(from, to, 0); got != from {
			t.Errorf("DropWidth(%v, %v, 0) = %v", from, to, got)
		}
		if got := DropWidth(from, to, 1.5); got != to {
			t.Errorf("DropWidth(%v, %v, 1.5) = %v", from, to, got)
		}
		prev := from
		for i := 1; i <= 100; i++ {
			w := DropWidth(from, to, float64(i)/100)
			if (to-from)*(w-prev) < 0 {
				t.Fatalf("DropWidth(%v, %v) went back at %d: %v after %v", from, to, i, w, prev)
			}
			prev = w
		}
	}
}
