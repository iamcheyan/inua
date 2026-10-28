package gamerelay

import (
	"context"
	"encoding/json"
	"errors"
	"net"
	"net/http"
	"net/url"
	"strings"
	"sync"
	"time"

	"github.com/gorilla/websocket"

	"github.com/lyricat/inua/internal/i18n"
)

// Status is a table's game as the lobby shows it.
type Status struct {
	Game  string `json:"game"`  // "small-fortune", "chinese-checkers"
	Code  string `json:"code"`  // what visitors join with
	State string `json:"state"` // "lobby", "playing", "over"
	Seats []Seat `json:"seats"`
	Room  int    `json:"room"` // how many more may join the lobby
	Lead  string `json:"lead"` // the visitor who sets the game up, if a visitor does
}

// Seat is a player at a table.
type Seat struct {
	Name string `json:"name"`
	Kind string `json:"kind"` // local, visitor, computer, ai, open
	Here bool   `json:"here"`
}

// Control is what the lobby and a desktop say to each other about the
// table, as text messages: the desktop's hello and its game's status, the
// lobby's table, or why it turned the desktop away.
type Control struct {
	T string `json:"t"` // hello, status, table, bye
	// Text is why a bye: "key" (the lobby wants another key), "full" (no
	// table free).
	Key    string  `json:"key,omitempty"`
	Token  string  `json:"token,omitempty"` // a table to have back, after a drop
	Table  int     `json:"table,omitempty"`
	URL    string  `json:"url,omitempty"`
	Text   string  `json:"text,omitempty"`
	Status *Status `json:"status,omitempty"`
}

// Publication is a game published at a lobby: it keeps the connection
// up, dialling again after a drop, and serves the game's handler to the
// browsers the lobby passes on.
type Publication struct {
	lobby, key string
	handler    http.Handler
	notify     func()
	cancel     context.CancelFunc
	nudge      chan struct{} // the status changed

	mu     sync.Mutex
	status *Status
	sess   *Session
	table  int
	url    string
	token  string
	err    error
	ended  bool // turned away for good
}

// Publish publishes a game's handler at the lobby at addr (a lobby's
// address as the user gives it: lobby.example.org, http://…, with
// ?key=… when the lobby asks for one). notify is called, on a goroutine
// of the Publication's, each time Table changes.
func Publish(addr string, h http.Handler, notify func()) (*Publication, error) {
	u, key, err := HostURL(addr)
	if err != nil {
		return nil, err
	}
	ctx, cancel := context.WithCancel(context.Background())
	p := &Publication{lobby: u, key: key, handler: h, notify: notify, cancel: cancel, nudge: make(chan struct{}, 1)}
	go p.run(ctx)
	return p, nil
}

// HostURL is the WebSocket a desktop dials at a lobby's address, and the
// key in it: https unless it says http, or names a port or a local
// address.
func HostURL(addr string) (string, string, error) {
	addr = strings.TrimSpace(addr)
	if addr == "" {
		return "", "", errors.New(i18n.T("Give the lobby's address."))
	}
	if !strings.Contains(addr, "://") {
		scheme := "https://"
		host := strings.Split(addr, "/")[0]
		if h, _, err := net.SplitHostPort(host); err == nil {
			host, scheme = h, "http://"
		}
		if host == "localhost" || net.ParseIP(host) != nil {
			scheme = "http://"
		}
		addr = scheme + addr
	}
	u, err := url.Parse(addr)
	if err != nil || u.Host == "" {
		return "", "", errors.New(i18n.Tf("%s is not a lobby's address.", addr))
	}
	switch u.Scheme {
	case "http", "ws":
		u.Scheme = "ws"
	case "https", "wss":
		u.Scheme = "wss"
	default:
		return "", "", errors.New(i18n.Tf("%s is not a lobby's address.", addr))
	}
	key := u.Query().Get("key")
	u.Path = strings.TrimSuffix(u.Path, "/") + "/host"
	u.RawQuery, u.Fragment = "", ""
	return u.String(), key, nil
}

// Table is the table the game is at and its page, or why it is at none:
// 0 while connecting.
func (p *Publication) Table() (int, string, error) {
	p.mu.Lock()
	defer p.mu.Unlock()
	return p.table, p.url, p.err
}

// Set tells the lobby how the game stands, soon after; it does not wait
// for the network.
func (p *Publication) Set(st Status) {
	p.mu.Lock()
	p.status = &st
	p.mu.Unlock()
	select {
	case p.nudge <- struct{}{}:
	default:
	}
}

// Close takes the game off the lobby.
func (p *Publication) Close() {
	p.cancel()
	p.mu.Lock()
	sess := p.sess
	p.mu.Unlock()
	if sess != nil {
		sess.Close()
	}
}

func (p *Publication) run(ctx context.Context) {
	wait := time.Second
	for ctx.Err() == nil {
		start := time.Now()
		err := p.once(ctx)
		p.mu.Lock()
		p.sess, p.table, p.url, p.err = nil, 0, "", err
		ended := p.ended
		p.mu.Unlock()
		if ctx.Err() != nil {
			return
		}
		p.notify()
		if ended {
			return
		}
		if time.Since(start) > time.Minute {
			wait = time.Second
		}
		select {
		case <-time.After(wait):
		case <-ctx.Done():
			return
		}
		wait = min(wait*2, 30*time.Second)
	}
}

// once is one connection to the lobby, until it drops.
func (p *Publication) once(ctx context.Context) error {
	d := websocket.Dialer{HandshakeTimeout: 15 * time.Second, Proxy: http.ProxyFromEnvironment}
	ws, resp, err := d.DialContext(ctx, p.lobby, nil)
	if err != nil {
		if resp != nil && resp.StatusCode == http.StatusNotFound {
			return errors.New(i18n.T("There is no lobby at this address."))
		}
		return err
	}
	sess := NewSession(ws, true)
	defer sess.Close()
	p.mu.Lock()
	hello := Control{T: "hello", Key: p.key, Token: p.token}
	p.mu.Unlock()
	b, _ := json.Marshal(hello)
	if err := sess.SendControl(b); err != nil {
		return err
	}
	srv := &http.Server{Handler: p.handler, ReadHeaderTimeout: 10 * time.Second}
	go srv.Serve(sess)
	defer srv.Close()
	for {
		select {
		case <-ctx.Done():
			return ctx.Err()
		case <-sess.Done():
			return errors.New(i18n.T("The connection to the lobby was lost."))
		case <-p.nudge:
			p.mu.Lock()
			seated := p.sess == sess
			p.mu.Unlock()
			if seated {
				p.sendStatus(sess)
			}
		case b := <-sess.Control():
			var m Control
			if json.Unmarshal(b, &m) != nil {
				continue
			}
			switch m.T {
			case "table":
				p.mu.Lock()
				p.sess, p.table, p.url, p.token, p.err = sess, m.Table, m.URL, m.Token, nil
				p.mu.Unlock()
				p.sendStatus(sess)
				p.notify()
			case "bye":
				p.mu.Lock()
				p.ended = true
				p.mu.Unlock()
				return byeError(m.Text)
			}
		}
	}
}

// Why the lobby turns a desktop away (Control.Text of a bye).
const (
	ByeKey  = "key"
	ByeFull = "full"
)

func byeError(why string) error {
	switch why {
	case ByeKey:
		return errors.New(i18n.T("The lobby asks for another key."))
	case ByeFull:
		return errors.New(i18n.T("Every table at the lobby is taken."))
	}
	return errors.New(i18n.T("The lobby turned the game away."))
}

// sendStatus tells the lobby the game's latest status, if any.
func (p *Publication) sendStatus(sess *Session) {
	p.mu.Lock()
	st := p.status
	p.mu.Unlock()
	if st != nil {
		b, _ := json.Marshal(Control{T: "status", Status: st})
		sess.SendControl(b)
	}
}
