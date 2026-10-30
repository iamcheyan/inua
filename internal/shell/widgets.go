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

// Apart reports whether r keeps a clear cell from each of others, across
// and corner to corner: no two widgets touch.
func (r GridRect) Apart(others []GridRect) bool {
	for _, o := range others {
		if r.Overlaps(GridRect{o.Column - 1, o.Row - 1, o.Columns + 2, o.Rows + 2}) {
			return false
		}
	}
	return true
}

// FreeSpot is the first place, row by row, for a widget of columns ×
// rows within the page's first width columns apart from all of taken;
// below them all when the rows above are full.
func FreeSpot(taken []GridRect, columns, rows, width int) GridRect {
	r := GridRect{Columns: columns, Rows: rows}
	bottom := 0
	for _, t := range taken {
		bottom = max(bottom, t.Row+t.Rows)
	}
	for r.Row = 0; r.Row < bottom; r.Row++ {
		for r.Column = 0; r.Column+columns <= max(width, columns); r.Column++ {
			if r.Apart(taken) {
				return r
			}
		}
	}
	r.Column, r.Row = 0, bottom
	if len(taken) > 0 {
		r.Row++ // a row clear under them
	}
	return r
}
