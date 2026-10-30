package checkersnet

import (
	"context"
	"net/http/httptest"
	"strings"
	"sync"
	"testing"
	"time"

	"github.com/gorilla/websocket"

	"github.com/lyricat/inua/internal/games/gameai"
	"github.com/lyricat/inua/internal/games/gamerelay"
)

// fakeAI is the user's AI as a lobby offers it.
type fakeAI struct {
	profiles []string
	asked    chan string
}

func (a *fakeAI) Choose(_ context.Context, profile, _, _ string, _ []string) (int, error) {
	select {
	case a.asked <- profile:
	default:
	}
	return 0, nil
}

func (a *fakeAI) Profiles() []string { return a.profiles }

// unattended opens a game as a lobby does, on a test server; a browser
// joins it.
func unattended(t *testing.T, ai gameai.AI) *browser {
	t.Helper()
	var mu sync.Mutex
	run := func(f func()) { mu.Lock(); defer mu.Unlock(); f() }
	h, st, end := Unattended(run, func(gamerelay.Status) {}, ai)
	t.Cleanup(end)
	srv := httptest.NewServer(h)
	t.Cleanup(srv.Close)
	ws, _, err := websocket.DefaultDialer.Dial("ws"+strings.TrimPrefix(srv.URL, "http")+"/ws", nil)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { ws.Close() })
	b := &browser{t, ws}
	b.send(inMsg{T: "join", Code: st.Code, Name: "Ann"})
	b.expect("hello", nil)
	return b
}

// A game a lobby hosts offers its lead the AI for a seat when the lobby
// has one that answers, and the AI plays the seat.
func TestUnattendedAI(t *testing.T) {
	ai := &fakeAI{profiles: []string{"quick", "deep"}, asked: make(chan string, 1)}
	ann := unattended(t, ai)
	var m lobbyMsg
	ann.until("lobby", func(d []byte) bool { m = lobbyOf(d); return m.Lead })
	if !m.AI || len(m.Profiles) != 2 {
		t.Fatalf("the AI not offered: %+v", m)
	}
	ann.send(inMsg{T: "seat", Index: 1, Kind: "ai", Profile: "deep"})
	ann.until("lobby", func(d []byte) bool { m = lobbyOf(d); return m.Seats[1].Kind == "ai" })
	if m.Seats[1].Profile != "deep" || m.Why != "" {
		t.Errorf("seat %+v, why %q", m.Seats[1], m.Why)
	}
	ann.send(inMsg{T: "start"})
	ann.expect("start", nil)
	ann.ws.Close() // Ann goes: the computer plays for her, then the AI its turn
	select {
	case p := <-ai.asked:
		if p != "deep" {
			t.Errorf("asked %q", p)
		}
	case <-time.After(10 * time.Second):
		t.Fatal("the AI was not asked")
	}
}

// Without an AI, or with one not answering yet, the lead has the
// computer only.
func TestUnattendedNoAI(t *testing.T) {
	for name, ai := range map[string]gameai.AI{"none": nil, "not answering": &fakeAI{}} {
		t.Run(name, func(t *testing.T) {
			ann := unattended(t, ai)
			var m lobbyMsg
			ann.until("lobby", func(d []byte) bool { m = lobbyOf(d); return m.Lead })
			if m.AI {
				t.Errorf("the AI offered: %+v", m)
			}
			ann.send(inMsg{T: "seat", Index: 1, Kind: "ai"})
			ann.send(inMsg{T: "seat", Index: 1, Kind: "computer", Level: 2})
			ann.until("lobby", func(d []byte) bool { m = lobbyOf(d); return m.Seats[1].Kind != "open" })
			if m.Seats[1].Kind != "computer" {
				t.Errorf("seat %+v", m.Seats[1])
			}
		})
	}
}
