package checkersnet

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"

	"github.com/gorilla/websocket"

	"github.com/lyricat/inua/internal/games/gamerelay"
	"github.com/lyricat/inua/internal/games/lobby"
)

// A game published at a lobby: a browser joins it under the table's path,
// leads its setup, and the lobby lists it.
func TestThroughLobby(t *testing.T) {
	x := newTestHost(t, Options{Players: 2})
	srv := httptest.NewServer(lobby.New(lobby.Options{}).Handler())
	defer srv.Close()
	ready := make(chan struct{}, 8)
	p, err := gamerelay.Publish(srv.URL, x.Handler(), func() { ready <- struct{}{} })
	if err != nil {
		t.Fatal(err)
	}
	defer p.Close()
	select {
	case <-ready:
	case <-time.After(5 * time.Second):
		t.Fatal("no table")
	}
	if n, _, err := p.Table(); n != 1 {
		t.Fatalf("table %d, %v", n, err)
	}
	ws, _, err := websocket.DefaultDialer.Dial("ws"+strings.TrimPrefix(srv.URL, "http")+"/t/1/ws", http.Header{"Origin": {srv.URL}})
	if err != nil {
		t.Fatal(err)
	}
	defer ws.Close()
	ann := &browser{t, ws}
	var code string
	x.do(func() { code = x.Code })
	ann.send(inMsg{T: "join", Code: code, Name: "Ann"})
	var hello helloMsg
	ann.expect("hello", &hello)
	if hello.Seat != 0 {
		t.Fatalf("seat %d", hello.Seat)
	}
	ann.until("lobby", func(d []byte) bool { return lobbyOf(d).Lead })
	var st gamerelay.Status
	x.do(func() { st = x.Status() })
	if st.Game != "chinese-checkers" || st.State != "lobby" || st.Lead != "Ann" || st.Room != 1 {
		t.Errorf("status %+v", st)
	}
}
