package lobby

import (
	"encoding/json"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"

	"github.com/gorilla/websocket"

	"github.com/lyricat/inua/internal/games/gamerelay"
	"github.com/lyricat/inua/internal/games/gameweb"
)

// game is a desktop's game as the tests publish it: a page, and a
// WebSocket that echoes.
var game = func() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("page " + r.URL.Path + " " + r.URL.RawQuery))
	})
	mux.HandleFunc("/ws", func(w http.ResponseWriter, r *http.Request) {
		c, err := gameweb.Accept(w, r) // the games' own, with its same-origin check
		if err != nil {
			return
		}
		var m any
		for c.Read(&m) == nil {
			c.Send(m)
		}
		c.Close()
	})
	return mux
}()

func newLobby(t *testing.T, opt Options) (*httptest.Server, *Lobby) {
	t.Helper()
	l := New(opt)
	srv := httptest.NewServer(l.Handler())
	t.Cleanup(srv.Close)
	return srv, l
}

// publish publishes the test game and waits for its table.
func publish(t *testing.T, srv *httptest.Server, key string) (*gamerelay.Publication, int, string, error) {
	t.Helper()
	return publishTo(t, srv, key, make(chan struct{}, 8))
}

func publishTo(t *testing.T, srv *httptest.Server, key string, notified chan struct{}) (*gamerelay.Publication, int, string, error) {
	t.Helper()
	addr := srv.URL
	if key != "" {
		addr += "/?key=" + key
	}
	p, err := gamerelay.Publish(addr, game, func() { notified <- struct{}{} })
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(p.Close)
	for {
		select {
		case <-notified:
			if n, url, err := p.Table(); n > 0 || err != nil {
				return p, n, url, err
			}
		case <-time.After(5 * time.Second):
			t.Fatal("no table")
		}
	}
}

func get(t *testing.T, url string) (int, string) {
	t.Helper()
	resp, err := http.Get(url)
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()
	b, _ := io.ReadAll(resp.Body)
	return resp.StatusCode, string(b)
}

// A published game is at the first table; its page and its WebSocket
// pass through the lobby.
func TestPublish(t *testing.T) {
	srv, _ := newLobby(t, Options{Tables: 2})
	p, n, url, err := publish(t, srv, "")
	if err != nil || n != 1 || url != srv.URL+"/t/1/" {
		t.Fatalf("table %d at %s, %v", n, url, err)
	}
	if code, body := get(t, srv.URL+"/t/1/art/x.png?y=1"); code != 200 || body != "page /art/x.png y=1" {
		t.Errorf("%d %q", code, body)
	}
	if code, _ := get(t, srv.URL+"/t/2/"); code != http.StatusNotFound {
		t.Errorf("a free table: %d", code)
	}
	resp, err := http.Get(srv.URL + "/t/1")
	if err != nil || resp.Request.URL.Path != "/t/1/" {
		t.Errorf("not sent to /t/1/: %v", err)
	}
	ws, _, err := websocket.DefaultDialer.Dial("ws"+strings.TrimPrefix(srv.URL, "http")+"/t/1/ws",
		http.Header{"Origin": {srv.URL}})
	if err != nil {
		t.Fatal(err)
	}
	defer ws.Close()
	ws.WriteJSON(map[string]string{"t": "hi"})
	var m map[string]string
	if err := ws.ReadJSON(&m); err != nil || m["t"] != "hi" {
		t.Errorf("echo %v, %v", m, err)
	}
	if _, _, err := websocket.DefaultDialer.Dial("ws"+strings.TrimPrefix(srv.URL, "http")+"/t/1/ws",
		http.Header{"Origin": {"http://elsewhere.example"}}); err == nil {
		t.Error("a page elsewhere opened the game's WebSocket")
	}

	// The status shows on the lobby's page.
	page, _, err := websocket.DefaultDialer.Dial("ws"+strings.TrimPrefix(srv.URL, "http")+"/ws", nil)
	if err != nil {
		t.Fatal(err)
	}
	defer page.Close()
	p.Set(gamerelay.Status{Game: "chinese-checkers", Code: "AB12", State: "lobby", Room: 9,
		Seats: []gamerelay.Seat{{Name: "  Ann\n  Lee ", Kind: "local", Here: true}, {Kind: "robot"}}})
	page.SetReadDeadline(time.Now().Add(5 * time.Second))
	for {
		var tm struct {
			Tables []tableMsg `json:"tables"`
		}
		if err := page.ReadJSON(&tm); err != nil {
			t.Fatal(err)
		}
		if st := tm.Tables[0].Status; st != nil {
			if st.Code != "AB12" || st.Room != 6 || st.Seats[0].Name != "Ann Lee" || st.Seats[1].Kind != "open" {
				t.Errorf("status %+v", st)
			}
			break
		}
	}
}

// A desktop gone keeps its table for a while, and has it back.
func TestReconnect(t *testing.T) {
	srv, l := newLobby(t, Options{Tables: 2, Hold: time.Minute})
	notified := make(chan struct{}, 8)
	p1, n1, _, _ := publishTo(t, srv, "", notified)
	_, n2, _, _ := publish(t, srv, "")
	if n1 != 1 || n2 != 2 {
		t.Fatalf("tables %d, %d", n1, n2)
	}
	if _, _, _, err := publish(t, srv, ""); err == nil {
		t.Error("a third game at two tables")
	}
	// Drop the first desktop's connection: it dials again.
	l.mu.Lock()
	sess := l.tables[0].sess
	l.mu.Unlock()
	sess.Close()
	deadline := time.After(10 * time.Second)
	dropped := false
	for {
		select {
		case <-notified:
			n, _, _ := p1.Table()
			switch {
			case n == 0:
				dropped = true
			case n == 1 && dropped:
				return
			default:
				t.Fatalf("back at table %d", n)
			}
		case <-deadline:
			t.Fatal("not back")
		}
	}
}

// With a key, a desktop without it is turned away for good.
func TestKey(t *testing.T) {
	srv, _ := newLobby(t, Options{Key: "sesame"})
	if _, _, _, err := publish(t, srv, "wrong"); err == nil {
		t.Error("published with the wrong key")
	}
	if _, n, _, err := publish(t, srv, "sesame"); n != 1 || err != nil {
		t.Errorf("table %d, %v", n, err)
	}
}

func TestTexts(t *testing.T) {
	srv, _ := newLobby(t, Options{})
	_, body := get(t, srv.URL+"/texts.json")
	var m map[string]any
	if json.Unmarshal([]byte(body), &m) != nil || m["title"] == nil {
		t.Errorf("texts %s", body)
	}
	if code, body := get(t, srv.URL+"/"); code != 200 || !strings.Contains(body, "lobby.js") {
		t.Errorf("page %d", code)
	}
}
