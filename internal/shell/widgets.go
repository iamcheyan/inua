package shell

import "math"

// WidgetCell is the widget page's grid in pixels: a widget's top left
// corner is at a column and a row of it.
const WidgetCell = 60

// Cell is the column (or row) nearest to a position in pixels, never
// before the first.
func Cell(px float64) int { return max(0, int(math.Round(px/WidgetCell))) }

// Span is how many columns (or rows) a size in pixels covers.
func Span(px int) int { return max(1, (px+WidgetCell-1)/WidgetCell) }

// GridRect is a widget's place on the grid: its corner and its span.
type GridRect struct{ Column, Row, Columns, Rows int }

// Overlaps reports whether a and b share a cell.
func (a GridRect) Overlaps(b GridRect) bool {
	return a.Column < b.Column+b.Columns && b.Column < a.Column+a.Columns &&
		a.Row < b.Row+b.Rows && b.Row < a.Row+a.Rows
}

// Fits reports whether r overlaps none of others.
func (r GridRect) Fits(others []GridRect) bool {
	for _, o := range others {
		if r.Overlaps(o) {
			return false
		}
	}
	return true
}

// FreeSpot is the first place, row by row, for a widget of columns ×
// rows within the page's first width columns that overlaps none of
// taken; below them all when the rows above are full.
func FreeSpot(taken []GridRect, columns, rows, width int) GridRect {
	r := GridRect{Columns: columns, Rows: rows}
	bottom := 0
	for _, t := range taken {
		bottom = max(bottom, t.Row+t.Rows)
	}
	for r.Row = 0; r.Row <= bottom; r.Row++ {
		for r.Column = 0; r.Column+columns <= max(width, columns); r.Column++ {
			if r.Fits(taken) {
				return r
			}
		}
	}
	r.Column = 0
	return r
}
