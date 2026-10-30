package shell

import (
	"math"
	"testing"
)

func TestPickGroups(t *testing.T) {
	clients := []byte(`[
		{"address":"0xa","title":"Mail","class":"mail","size":[800,600],"mapped":true,"focusHistoryID":2,"workspace":{"id":3,"name":"3"}},
		{"address":"0xb","title":"Term","class":"term","size":[400,300],"mapped":true,"focusHistoryID":0,"workspace":{"id":1,"name":"1"}},
		{"address":"0xc","title":"Notes","class":"notes","size":[500,500],"mapped":true,"focusHistoryID":1,"workspace":{"id":3,"name":"3"}},
		{"address":"0xd","title":"Scratch","class":"x","size":[300,300],"mapped":true,"focusHistoryID":3,"workspace":{"id":-98,"name":"special:scratch"}},
		{"address":"0xe","title":"Gone","class":"x","size":[300,300],"mapped":false,"workspace":{"id":2,"name":"2"}},
		{"address":"0xf","title":"Hidden","class":"x","size":[300,300],"mapped":true,"hidden":true,"workspace":{"id":2,"name":"2"}}
	]`)
	groups, err := PickGroups(clients, []int{1})
	if err != nil {
		t.Fatal(err)
	}
	ids := []int{}
	for _, g := range groups {
		ids = append(ids, g.ID)
	}
	if len(groups) != 3 || ids[0] != 1 || ids[1] != 3 || ids[2] != -98 {
		t.Fatalf("groups %v", ids)
	}
	if !groups[0].Shown || groups[1].Shown {
		t.Error("shown workspaces")
	}
	// The most recently focused first.
	if w := groups[1].Windows; len(w) != 2 || w[0].Title != "Notes" || w[1].Title != "Mail" {
		t.Errorf("workspace 3: %+v", w)
	}
}

// Rows fill the width; cards keep their shape; the last row is not
// stretched.
func TestJustify(t *testing.T) {
	aspects := []float64{16.0 / 9, 4.0 / 3, 1, 16.0 / 9, 0.75}
	tiles, height := Justify(aspects, 1000, 200, 320, 10)
	rows := map[float64][]Tile{}
	for i, tl := range tiles {
		if math.Abs(tl.W/tl.H-clampAspect(aspects[i])) > 1e-9 {
			t.Errorf("card %d lost its shape: %+v", i, tl)
		}
		rows[tl.Y] = append(rows[tl.Y], tl)
	}
	if len(rows) < 2 {
		t.Fatalf("one row: %+v", tiles)
	}
	last := tiles[len(tiles)-1]
	lastRow := rows[last.Y]
	if left, right := lastRow[0].X, 1000-(last.X+last.W); math.Abs(left-right) > 1e-6 {
		t.Errorf("the last row is not centred: %v | %v", left, right)
	}
	for y, row := range rows {
		end := row[len(row)-1]
		if y != last.Y && math.Abs(end.X+end.W-1000) > 1e-6 {
			t.Errorf("row at %v ends at %v", y, end.X+end.W)
		}
	}
	if last.H > 200 {
		t.Errorf("the last row stretched: %+v", last)
	}
	if math.Abs(height-(last.Y+last.H)) > 1e-9 {
		t.Errorf("height %v", height)
	}
	if tiles, h := Justify(nil, 1000, 200, 320, 10); len(tiles) != 0 || h != 0 {
		t.Error("nothing to lay out")
	}
}

// A single very wide window does not take the whole row's height away.
func TestJustifyWide(t *testing.T) {
	tiles, _ := Justify([]float64{20}, 1000, 200, 320, 10)
	if tiles[0].W/tiles[0].H != 3 {
		t.Errorf("not clamped: %+v", tiles[0])
	}
}
