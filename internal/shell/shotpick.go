package shell

import (
	"encoding/json"
	"math"
	"slices"
	"strconv"

	"github.com/lyricat/inua/internal/hypr"
)

// The screenshot tool's Window mode shows every window on every workspace
// as a grid of live pictures, grouped by workspace, to take one whole
// whether it is shown or not.

// PickWindow is a window to pick, as its group lists it.
type PickWindow struct {
	Address string
	Title   string
	Class   string
	W, H    float64 // its size, logical pixels
}

// PickGroup is a workspace's windows, the most recently focused first.
type PickGroup struct {
	ID      int
	Name    string
	Shown   bool // shown on a monitor now
	Windows []PickWindow
}

// pickClient is what PickGroups reads of a client.
type pickClient struct {
	Address        string     `json:"address"`
	Title          string     `json:"title"`
	Class          string     `json:"class"`
	Size           [2]float64 `json:"size"`
	Mapped         bool       `json:"mapped"`
	Hidden         bool       `json:"hidden"`
	FocusHistoryID int        `json:"focusHistoryID"`
	Workspace      struct {
		ID   int    `json:"id"`
		Name string `json:"name"`
	} `json:"workspace"`
}

// PickGroups reads Hyprland's clients (j/clients) into the groups to pick
// from: each workspace with a window, by its ID (special workspaces after
// the others), the ones in shown marked.
func PickGroups(clients []byte, shown []int) ([]PickGroup, error) {
	var raw []pickClient
	if err := json.Unmarshal(clients, &raw); err != nil {
		return nil, err
	}
	slices.SortStableFunc(raw, func(a, b pickClient) int { return a.FocusHistoryID - b.FocusHistoryID })
	var groups []PickGroup
	for _, c := range raw {
		if !c.Mapped || c.Hidden || c.Size[0] <= 0 || c.Size[1] <= 0 || c.Workspace.ID == 0 {
			continue
		}
		i := slices.IndexFunc(groups, func(g PickGroup) bool { return g.ID == c.Workspace.ID })
		if i < 0 {
			name := c.Workspace.Name
			if name == "" {
				name = strconv.Itoa(c.Workspace.ID)
			}
			groups = append(groups, PickGroup{ID: c.Workspace.ID, Name: name, Shown: slices.Contains(shown, c.Workspace.ID)})
			i = len(groups) - 1
		}
		groups[i].Windows = append(groups[i].Windows, PickWindow{
			Address: hypr.NormalizeAddress(c.Address), Title: c.Title, Class: c.Class, W: c.Size[0], H: c.Size[1],
		})
	}
	// Special workspaces (negative IDs) after the others, each in order.
	slices.SortFunc(groups, func(a, b PickGroup) int {
		if (a.ID < 0) != (b.ID < 0) {
			if a.ID < 0 {
				return 1
			}
			return -1
		}
		if a.ID < 0 {
			return b.ID - a.ID
		}
		return a.ID - b.ID
	})
	return groups, nil
}

// Tile is a card's place in a justified grid.
type Tile struct{ X, Y, W, H float64 }

// Justify lays cards of the given aspect ratios (width / height) out in
// rows as wide as width, gap apart, each row as tall as it must be for its
// cards to fill it, about target high: the row ends when the next card
// would make it lower than target. The last row keeps target's height
// rather than stretch, centred; no row is taller than max. It returns
// each card's tile and the grid's height.
func Justify(aspects []float64, width, target, max, gap float64) ([]Tile, float64) {
	tiles := make([]Tile, len(aspects))
	y := 0.0
	for start := 0; start < len(aspects); {
		// Take cards until the row, at target height, is wider than width.
		end, sum := start, 0.0
		for end < len(aspects) {
			a := clampAspect(aspects[end])
			if end > start && (sum+a)*target+float64(end-start)*gap > width {
				break
			}
			sum += a
			end++
		}
		gaps := float64(end-start-1) * gap
		h := (width - gaps) / sum
		if end == len(aspects) && h > target {
			h = target // the last row: not stretched to fill
		}
		h = math.Min(h, max)
		x := 0.0
		if used := sum*h + gaps; used < width-1 {
			x = (width - used) / 2 // a row short of the width: centred
		}
		for i := start; i < end; i++ {
			w := clampAspect(aspects[i]) * h
			tiles[i] = Tile{X: x, Y: y, W: w, H: h}
			x += w + gap
		}
		y += h + gap
		start = end
	}
	if len(aspects) > 0 {
		y -= gap
	}
	return tiles, y
}

// clampAspect keeps a very wide or very tall window from taking a row, or
// none of it, alone.
func clampAspect(a float64) float64 {
	if math.IsNaN(a) || a <= 0 {
		return 1
	}
	return math.Max(0.5, math.Min(a, 3))
}
