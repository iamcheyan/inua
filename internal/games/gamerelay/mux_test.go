package gamerelay

import (
	"bytes"
	"crypto/rand"
	"errors"
	"io"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"sync"
	"testing"
	"time"

	"github.com/gorilla/websocket"
)

// pair is two ends of a session: the lobby's (it accepted the WebSocket)
// and the desktop's (it dialled).
func pair(t *testing.T) (lobby, desk *Session) {
	t.Helper()
	got := make(chan *Session, 1)
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ws, err := (&websocket.Upgrader{}).Upgrade(w, r, nil)
		if err != nil {
			t.Error(err)
			return
		}
		got <- NewSession(ws, false)
	}))
	t.Cleanup(srv.Close)
	ws, _, err := websocket.DefaultDialer.Dial("ws"+strings.TrimPrefix(srv.URL, "http"), nil)
	if err != nil {
		t.Fatal(err)
	}
	desk = NewSession(ws, true)
	lobby = <-got
	t.Cleanup(func() { lobby.Close(); desk.Close() })
	return lobby, desk
}

// Streams opened at either end carry bytes both ways, and a close reads as
// the end.
func TestStreams(t *testing.T) {
	lobby, desk := pair(t)
	go func() { // the desktop echoes
		for {
			c, err := desk.Accept()
			if err != nil {
				return
			}
			go func() { io.Copy(c, c); c.Close() }()
		}
	}()
	var wg sync.WaitGroup
	for range 20 {
		wg.Add(1)
		go func() {
			defer wg.Done()
			c, err := lobby.Open()
			if err != nil {
				t.Error(err)
				return
			}
			want := make([]byte, 700<<10) // more than a window
			rand.Read(want)
			go func() { c.Write(want) }()
			got := make([]byte, len(want))
			if _, err := io.ReadFull(c, got); err != nil {
				t.Error(err)
			}
			if !bytes.Equal(got, want) {
				t.Error("the echo differs")
			}
			c.Close()
		}()
	}
	wg.Wait()
}

// A stream no one reads holds up only itself.
func TestSlowReader(t *testing.T) {
	lobby, desk := pair(t)
	accepted := make(chan io.ReadWriteCloser, 2)
	go func() {
		for {
			c, err := desk.Accept()
			if err != nil {
				return
			}
			accepted <- c
		}
	}()
	slow, _ := lobby.Open()
	<-accepted
	big := make([]byte, 2*window)
	wrote := make(chan struct{})
	go func() { slow.Write(big); close(wrote) }() // blocks: nobody reads
	fast, _ := lobby.Open()
	other := <-accepted
	go fast.Write([]byte("hello"))
	b := make([]byte, 5)
	if _, err := io.ReadFull(other, b); err != nil || string(b) != "hello" {
		t.Fatalf("read %q, %v", b, err)
	}
	select {
	case <-wrote:
		t.Fatal("wrote more than the window to a reader that reads nothing")
	case <-time.After(50 * time.Millisecond):
	}
}

// Closing either end reads as EOF at the other; the session's end ends
// every stream.
func TestClose(t *testing.T) {
	lobby, desk := pair(t)
	c, _ := lobby.Open()
	d, _ := desk.Accept()
	c.Write([]byte("bye"))
	c.Close()
	if b, err := io.ReadAll(d); string(b) != "bye" || err != nil {
		t.Fatalf("read %q, %v", b, err)
	}
	if _, err := d.Write([]byte("x")); err == nil {
		t.Error("wrote to a closed stream")
	}
	e, _ := desk.Open()
	f, _ := lobby.Accept()
	desk.Close()
	if _, err := e.Read(make([]byte, 1)); err == nil {
		t.Error("read from a stream of a closed session")
	}
	f.SetReadDeadline(time.Now().Add(5 * time.Second))
	if _, err := f.Read(make([]byte, 1)); err == nil || errors.Is(err, os.ErrDeadlineExceeded) {
		t.Errorf("the other end's stream: %v", err)
	}
	if _, err := lobby.Open(); err == nil {
		select {
		case <-lobby.Done():
		case <-time.After(5 * time.Second):
			t.Error("the session lived on after the other end closed")
		}
	}
}

// A read past its deadline returns a timeout, and reads again after the
// deadline is moved.
func TestDeadline(t *testing.T) {
	lobby, desk := pair(t)
	c, _ := lobby.Open()
	d, _ := desk.Accept()
	d.SetReadDeadline(time.Now().Add(20 * time.Millisecond))
	if _, err := d.Read(make([]byte, 1)); !errors.Is(err, os.ErrDeadlineExceeded) {
		t.Fatalf("read: %v", err)
	}
	d.SetReadDeadline(time.Time{})
	c.Write([]byte("x"))
	if n, err := d.Read(make([]byte, 1)); n != 1 || err != nil {
		t.Fatalf("read %d, %v", n, err)
	}
}

// Text messages pass beside the streams.
func TestControl(t *testing.T) {
	lobby, desk := pair(t)
	desk.SendControl([]byte(`{"t":"hello"}`))
	select {
	case b := <-lobby.Control():
		if string(b) != `{"t":"hello"}` {
			t.Errorf("got %s", b)
		}
	case <-time.After(5 * time.Second):
		t.Fatal("no control message")
	}
}

// HTTP runs over the streams: the desktop serves, the lobby asks.
func TestHTTP(t *testing.T) {
	lobby, desk := pair(t)
	srv := &http.Server{Handler: http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("path " + r.URL.Path))
	})}
	go srv.Serve(desk)
	defer srv.Close()
	client := &http.Client{Transport: &http.Transport{DialContext: lobby.Dial}}
	for range 3 {
		resp, err := client.Get("http://table/x")
		if err != nil {
			t.Fatal(err)
		}
		b, _ := io.ReadAll(resp.Body)
		resp.Body.Close()
		if string(b) != "path /x" {
			t.Errorf("got %q", b)
		}
	}
}

func TestHostURL(t *testing.T) {
	for in, want := range map[string]string{
		"lobby.example.org":            "wss://lobby.example.org/host",
		"https://lobby.example.org/":   "wss://lobby.example.org/host",
		"http://example.org/games":     "ws://example.org/games/host",
		"127.0.0.1:7340":               "ws://127.0.0.1:7340/host",
		"localhost":                    "ws://localhost/host",
		"games.example.org:8443/x?y#z": "ws://games.example.org:8443/x/host",
	} {
		if got, _, err := HostURL(in); got != want || err != nil {
			t.Errorf("%s: %s, %v", in, got, err)
		}
	}
	if _, key, _ := HostURL("lobby.example.org/?key=open%20sesame"); key != "open sesame" {
		t.Errorf("key %q", key)
	}
	for _, in := range []string{"", "ftp://x", "http://"} {
		if _, _, err := HostURL(in); err == nil {
			t.Errorf("%q: no error", in)
		}
	}
}
