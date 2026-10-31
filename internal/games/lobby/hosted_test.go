package lobby

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
	"sync"
	"testing"
	"time"

	"github.com/gorilla/websocket"

	"github.com/lyricat/inua/internal/games/checkersnet"
	"github.com/lyricat/inua/internal/games/fortunenet"
	"github.com/lyricat/inua/internal/games/gameai"
	"github.com/lyricat/inua/internal/games/gamerelay"
)

// newGame asks the lobby for a game at a table, as the page does.
func newGame(t *testing.T, srv *httptest.Server, game string, table int) (int, map[string]any) {
	t.Helper()
	b, _ := json.Marshal(map[string]any{"game": game, "table": table})
	req, _ := http.NewRequest("POST", srv.URL+"/new", bytes.NewReader(b))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Origin", srv.URL)
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()
	var m map[string]any
	json.NewDecoder(resp.Body).Decode(&m)
	return resp.StatusCode, m
}

// watchUntil follows the lobby's tables until ok holds of them.
func watchUntil(t *testing.T, srv *httptest.Server, ok func(Tables) bool) Tables {
	t.Helper()
	ws, _, err := websocket.DefaultDialer.Dial("ws"+strings.TrimPrefix(srv.URL, "http")+"/ws", nil)
	if err != nil {
		t.Fatal(err)
	}
	defer ws.Close()
	ws.SetReadDeadline(time.Now().Add(5 * time.Second))
	for {
		var m Tables
		if err := ws.ReadJSON(&m); err != nil {
			t.Fatal(err)
		}
		if ok(m) {
			return m
		}
	}
}

// visitor is a browser at a table's game.
type visitor struct {
	t  *testing.T
	ws *websocket.Conn
}

func visit(t *testing.T, srv *httptest.Server, table string) *visitor {
	t.Helper()
	ws, _, err := websocket.DefaultDialer.Dial("ws"+strings.TrimPrefix(srv.URL, "http")+"/t/"+table+"/ws",
		http.Header{"Origin": {srv.URL}})
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { ws.Close() })
	ws.SetReadDeadline(time.Now().Add(5 * time.Second))
	return &visitor{t, ws}
}

// until reads messages until one of kind ty satisfies ok.
func (v *visitor) until(ty string, ok func(map[string]any) bool) map[string]any {
	v.t.Helper()
	for {
		var m map[string]any
		if err := v.ws.ReadJSON(&m); err != nil {
			v.t.Fatalf("waiting for %s: %v", ty, err)
		}
		if m["t"] == ty && ok(m) {
			return m
		}
	}
}

var both = []Game{
	{Name: "small-fortune", Open: fortunenet.Unattended},
	{Name: "chinese-checkers", Open: checkersnet.Unattended},
}

// A visitor opens a game at a free table: the lobby hosts it, the
// visitor who comes first sets it up, a desktop is seated elsewhere, and
// once everyone has left for Idle the table is free again.
func TestVisitorGame(t *testing.T) {
	for _, name := range []string{"chinese-checkers", "small-fortune"} {
		t.Run(name, func(t *testing.T) {
			srv, _ := newLobby(t, Options{Tables: 3, Games: both, Idle: 300 * time.Millisecond})
			if m := watchUntil(t, srv, func(Tables) bool { return true }); len(m.Games) != 2 {
				t.Fatalf("games %v", m.Games)
			}
			status, m := newGame(t, srv, name, 2)
			url, _ := m["url"].(string)
			if status != 200 || !strings.HasPrefix(url, "t/2/#") {
				t.Fatalf("%d %v", status, m)
			}
			code := strings.TrimPrefix(url, "t/2/#")
			watchUntil(t, srv, func(m Tables) bool {
				st := m.Tables[1].Status
				return m.Tables[1].Lobby && st != nil && st.Game == name && st.Code == code && st.State == "lobby"
			})
			if status, _ := newGame(t, srv, "small-fortune", 2); status != http.StatusConflict {
				t.Errorf("a second game at table 2: %d", status)
			}
			// A desktop asking for the table has another.
			ready := make(chan struct{}, 8)
			p, err := gamerelay.PublishAt(srv.URL, 2, game, func() { ready <- struct{}{} })
			if err != nil {
				t.Fatal(err)
			}
			defer p.Close()
			for n := 0; n == 0; {
				select {
				case <-ready:
					n, _, _ = p.Table()
					if n == 2 {
						t.Fatal("a desktop took the lobby's table")
					}
				case <-time.After(5 * time.Second):
					t.Fatal("no table")
				}
			}

			if code, body := get(t, srv.URL+"/t/2/"); code != 200 || !strings.Contains(body, "<html") {
				t.Errorf("the game's page: %d", code)
			}
			ann := visit(t, srv, "2")
			ann.ws.WriteJSON(map[string]any{"t": "join", "code": code, "name": "Ann"})
			if hello := ann.until("hello", func(map[string]any) bool { return true }); hello["seat"] != 0.0 {
				t.Fatalf("hello %v", hello)
			}
			ann.until("lobby", func(m map[string]any) bool { return m["lead"] == true })
			watchUntil(t, srv, func(m Tables) bool { st := m.Tables[1].Status; return st != nil && st.Lead == "Ann" })

			// Everyone leaves: the table is free after Idle, not before.
			ann.ws.Close()
			time.Sleep(100 * time.Millisecond)
			if c, _ := get(t, srv.URL+"/t/2/"); c != 200 {
				t.Errorf("freed too soon: %d", c)
			}
			watchUntil(t, srv, func(m Tables) bool { return m.Tables[1].Status == nil && !m.Tables[1].Lobby })
			if c, _ := get(t, srv.URL+"/t/2/"); c != http.StatusNotFound {
				t.Errorf("a freed table: %d", c)
			}
			if status, _ := newGame(t, srv, name, 2); status != 200 {
				t.Errorf("a game again at the freed table: %d", status)
			}
		})
	}
}

// fake is a game the lobby hosts in tests: the test game's handler, and
// how it stands as the test says.
type fake struct {
	mu      sync.Mutex
	changed func(gamerelay.Status)
	ended   int
}

func (f *fake) open(run func(func()), changed func(gamerelay.Status), _ gameai.AI) (http.Handler, gamerelay.Status, func()) {
	f.mu.Lock()
	f.changed = changed
	f.mu.Unlock()
	return game, gamerelay.Status{Game: "small-fortune", Code: "ABC", State: "lobby"}, func() {
		f.mu.Lock()
		f.ended++
		f.mu.Unlock()
	}
}

func (f *fake) say(st gamerelay.Status) {
	f.mu.Lock()
	changed := f.changed
	f.mu.Unlock()
	changed(st)
}

func (f *fake) endedN() int {
	f.mu.Lock()
	defer f.mu.Unlock()
	return f.ended
}

// A game over is freed after Over even with someone still at it; a game
// still played is not; one no one comes to is freed after Idle.
func TestVisitorGameEnds(t *testing.T) {
	f := &fake{}
	srv, _ := newLobby(t, Options{Tables: 2, Games: []Game{{Name: "small-fortune", Open: f.open}},
		Idle: 300 * time.Millisecond, Over: 300 * time.Millisecond})
	if status, _ := newGame(t, srv, "small-fortune", 1); status != 200 {
		t.Fatalf("%d", status)
	}
	v := visit(t, srv, "1")
	f.say(gamerelay.Status{Game: "small-fortune", Code: "ABC", State: "playing"})
	time.Sleep(500 * time.Millisecond)
	if f.endedN() != 0 {
		t.Fatal("a game played with someone at it ended")
	}
	f.say(gamerelay.Status{Game: "small-fortune", Code: "ABC", State: "over"})
	watchUntil(t, srv, func(m Tables) bool { return m.Tables[0].Status == nil })
	if f.endedN() != 1 {
		t.Errorf("ended %d times", f.endedN())
	}
	v.ws.Close()

	// No one comes.
	if status, _ := newGame(t, srv, "small-fortune", 2); status != 200 {
		t.Fatalf("%d", status)
	}
	watchUntil(t, srv, func(m Tables) bool { return m.Tables[1].Status == nil })
	if f.endedN() != 2 {
		t.Errorf("ended %d times", f.endedN())
	}
}

// Without games to host, or from a page elsewhere, or as a form, a
// visitor opens none.
func TestVisitorGameRefused(t *testing.T) {
	srv, _ := newLobby(t, Options{})
	if status, _ := newGame(t, srv, "small-fortune", 1); status != http.StatusForbidden {
		t.Errorf("a lobby without games: %d", status)
	}
	if m := watchUntil(t, srv, func(Tables) bool { return true }); m.Games != nil {
		t.Errorf("games %v", m.Games)
	}

	srv, _ = newLobby(t, Options{Tables: 2, Games: both})
	if status, _ := newGame(t, srv, "go", 1); status != http.StatusBadRequest {
		t.Errorf("an unknown game: %d", status)
	}
	if status, _ := newGame(t, srv, "small-fortune", 3); status != http.StatusConflict {
		t.Errorf("no table 3: %d", status)
	}
	req, _ := http.NewRequest("POST", srv.URL+"/new", strings.NewReader(`{"game":"small-fortune","table":1}`))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Origin", "http://elsewhere.example")
	if resp, err := http.DefaultClient.Do(req); err != nil || resp.StatusCode != http.StatusForbidden {
		t.Errorf("from elsewhere: %v %v", resp.Status, err)
	}
	resp, err := http.Post(srv.URL+"/new", "application/x-www-form-urlencoded", strings.NewReader("game=small-fortune&table=1"))
	if err != nil || resp.StatusCode != http.StatusUnsupportedMediaType {
		t.Errorf("a form: %v %v", resp.Status, err)
	}
	if m := watchUntil(t, srv, func(Tables) bool { return true }); m.Tables[0].Status != nil {
		t.Errorf("a game opened: %+v", m.Tables[0].Status)
	}
}

// fakeAI is the user's AI as a lobby run with -ai has it.
type fakeAI struct{}

func (fakeAI) Choose(context.Context, string, string, string, []string) (int, error) { return 0, nil }
func (fakeAI) Profiles() []string                                                    { return []string{"quick"} }

// With the user's AI, the setup of a game the lobby hosts offers AI
// players (Small Fortune) or seats (Chinese Checkers); without, it does
// not.
func TestVisitorGameAI(t *testing.T) {
	offered := map[string]func(map[string]any) bool{
		"small-fortune":    func(m map[string]any) bool { return m["maxAIs"].(float64) > 0 },
		"chinese-checkers": func(m map[string]any) bool { return m["ai"] == true },
	}
	for _, ai := range []gameai.AI{fakeAI{}, nil} {
		for name, offers := range offered {
			t.Run(fmt.Sprintf("%s/ai=%v", name, ai != nil), func(t *testing.T) {
				srv, _ := newLobby(t, Options{Tables: 1, Games: both, AI: ai})
				_, m := newGame(t, srv, name, 1)
				code := strings.TrimPrefix(m["url"].(string), "t/1/#")
				ann := visit(t, srv, "1")
				ann.ws.WriteJSON(map[string]any{"t": "join", "code": code, "name": "Ann"})
				lobby := ann.until("lobby", func(m map[string]any) bool { return m["lead"] == true })
				if offers(lobby) != (ai != nil) {
					t.Errorf("AI offered: %v, want %v", offers(lobby), ai != nil)
				}
			})
		}
	}
}
