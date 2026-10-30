// Package lobby is inua-game-lobby: a fixed row of tables a desktop
// publishes its game at (gamerelay.Publish), and the page visitors see
// them on. The game keeps running on the desktop; the lobby passes each
// browser's requests to it under /t/N/, over the desktop's own
// connection, so the desktop needs no address others can reach. A visitor
// may also open a game at a free table, which the lobby then hosts itself
// (Options.Games).
package lobby

import (
	"crypto/rand"
	"crypto/subtle"
	"embed"
	"encoding/base64"
	"encoding/json"
	"io/fs"
	"net/http"
	"net/http/httputil"
	"regexp"
	"slices"
	"strconv"
	"strings"
	"sync"
	"time"
	"unicode/utf8"

	"github.com/gorilla/websocket"

	"github.com/lyricat/inua/internal/games/gameai"
	"github.com/lyricat/inua/internal/games/gamerelay"
	"github.com/lyricat/inua/internal/games/gameweb"
	"github.com/lyricat/inua/internal/i18n"
)

// web is the lobby's page.
//
//go:embed web
var web embed.FS

// Options set up a Lobby.
type Options struct {
	// Tables is how many tables there are.
	Tables int
	// Key, when set, is what a desktop must give to publish a game.
	Key string
	// PublicURL is where visitors open the lobby, for the links a desktop
	// shows; "" for the address each desktop dialled.
	PublicURL string
	// Hold is how long a table stays its desktop's after the connection
	// drops, for it to come back.
	Hold time.Duration
	// Games are the games a visitor may open at a free table, which the
	// lobby then hosts itself; none, only desktops open games.
	Games []Game
	// AI is the user's AI, for the one who sets up a game the lobby hosts
	// to give it players (inua-game-lobby -ai); nil, computer players
	// only. A public lobby has none: its visitors would spend the user's.
	AI gameai.AI
	// Idle is how long a game the lobby hosts stays with no browser at its
	// table (2 minutes); Over, how long once it is over and not started
	// again (10 minutes). Then the table is free.
	Idle, Over time.Duration
}

// MaxWatchers is how many browsers may follow the lobby page at once.
const MaxWatchers = 2000

// Lobby holds the tables.
type Lobby struct {
	opt      Options
	mu       sync.Mutex
	tables   []*table
	watchers map[*gameweb.Client]bool
}

// table is a table: free, a desktop's game, or one the lobby hosts.
type table struct {
	n      int
	sess   *gamerelay.Session // nil while free, or held after a drop
	proxy  http.Handler
	token  string            // what its desktop has it back with
	status *gamerelay.Status // nil until the desktop says
	held   *time.Timer
	own    *hosted // the lobby's own game; nil for a desktop's
}

// free reports whether a game may open at the table.
func (t *table) free() bool { return t.sess == nil && t.token == "" && t.own == nil }

// New opens the lobby.
func New(opt Options) *Lobby {
	if opt.Tables <= 0 {
		opt.Tables = 8
	}
	if opt.Hold <= 0 {
		opt.Hold = 30 * time.Second
	}
	if opt.Idle <= 0 {
		opt.Idle = 2 * time.Minute
	}
	if opt.Over <= 0 {
		opt.Over = 10 * time.Minute
	}
	l := &Lobby{opt: opt, watchers: map[*gameweb.Client]bool{}}
	for i := range opt.Tables {
		l.tables = append(l.tables, &table{n: i + 1})
	}
	return l
}

// Handler serves the lobby: its page at /, the tables' list at /ws,
// desktops at /host, a visitor's new game at /new, and each table's game
// at /t/N/.
func (l *Lobby) Handler() http.Handler {
	page, _ := fs.Sub(web, "web")
	mux := http.NewServeMux()
	mux.Handle("/", gameweb.Files(page))
	mux.HandleFunc("/texts.json", func(w http.ResponseWriter, _ *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(webTexts())
	})
	mux.HandleFunc("/ws", l.serveWatch)
	mux.HandleFunc("/host", l.serveHost)
	mux.HandleFunc("POST /new", l.serveNew)
	mux.HandleFunc("/t/{n}", func(w http.ResponseWriter, r *http.Request) {
		http.Redirect(w, r, r.PathValue("n")+"/", http.StatusMovedPermanently)
	})
	mux.HandleFunc("/t/{n}/{rest...}", l.serveTable)
	return mux
}

// serveTable passes a browser's request on to the table's game: its
// desktop's, or the lobby's own.
func (l *Lobby) serveTable(w http.ResponseWriter, r *http.Request) {
	n, _ := strconv.Atoi(r.PathValue("n"))
	var proxy http.Handler
	l.mu.Lock()
	if n >= 1 && n <= len(l.tables) {
		proxy = l.tables[n-1].proxy
	}
	l.mu.Unlock()
	if proxy == nil {
		w.Header().Set("Content-Type", "text/plain; charset=utf-8")
		w.WriteHeader(http.StatusNotFound)
		w.Write([]byte(i18n.T("No game is at this table now.") + "\n"))
		return
	}
	proxy.ServeHTTP(w, r)
}

// proxyTo passes requests on over a desktop's session: the path after
// /t/N, the browser's own Host so the game's same-origin check holds.
func proxyTo(sess *gamerelay.Session) (http.Handler, func()) {
	tr := &http.Transport{DialContext: sess.Dial, MaxIdleConnsPerHost: 16, IdleConnTimeout: 30 * time.Second,
		ResponseHeaderTimeout: 45 * time.Second} // a picture is drawn on the desktop first
	rp := &httputil.ReverseProxy{
		Rewrite: func(pr *httputil.ProxyRequest) {
			pr.Out.URL.Scheme, pr.Out.URL.Host = "http", "table"
			pr.Out.URL.Path, pr.Out.URL.RawPath = "/"+pr.In.PathValue("rest"), ""
			pr.Out.Host = pr.In.Host
		},
		Transport: tr,
		ErrorHandler: func(w http.ResponseWriter, _ *http.Request, _ error) {
			w.Header().Set("Content-Type", "text/plain; charset=utf-8")
			w.WriteHeader(http.StatusBadGateway)
			w.Write([]byte(i18n.T("The table's host does not answer.") + "\n"))
		},
	}
	return rp, tr.CloseIdleConnections
}

// upgrader takes a desktop's WebSocket: a browser's page elsewhere may not
// open one (gorilla's same-origin check; a desktop sends no Origin).
var upgrader = websocket.Upgrader{ReadBufferSize: 64 << 10, WriteBufferSize: 64 << 10}

// serveHost seats a desktop's game at a table for as long as its
// connection lasts, and a while after for it to come back.
func (l *Lobby) serveHost(w http.ResponseWriter, r *http.Request) {
	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		return
	}
	sess := gamerelay.NewSession(ws, false)
	defer sess.Close()
	var hello gamerelay.Control
	select {
	case b := <-sess.Control():
		if json.Unmarshal(b, &hello) != nil || hello.T != "hello" {
			return
		}
	case <-sess.Done():
		return
	case <-time.After(15 * time.Second):
		return
	}
	bye := func(why string) {
		b, _ := json.Marshal(gamerelay.Control{T: "bye", Text: why})
		sess.SendControl(b)
	}
	if l.opt.Key != "" && subtle.ConstantTimeCompare([]byte(hello.Key), []byte(l.opt.Key)) != 1 {
		bye(gamerelay.ByeKey)
		return
	}
	t := l.seat(sess, hello.Token, hello.Table)
	if t == nil {
		bye(gamerelay.ByeFull)
		return
	}
	b, _ := json.Marshal(gamerelay.Control{T: "table", Table: t.n, Token: t.token, URL: l.tableURL(r, t.n)})
	sess.SendControl(b)
	for {
		select {
		case b := <-sess.Control():
			var m gamerelay.Control
			if json.Unmarshal(b, &m) == nil && m.T == "status" && m.Status != nil {
				st := clean(*m.Status)
				l.mu.Lock()
				if t.sess == sess {
					t.status = &st
				}
				l.mu.Unlock()
				l.changed()
			}
		case <-sess.Done():
			l.drop(t, sess)
			return
		}
	}
}

// seat gives a desktop its table: the one its token held, else the one it
// wants if free, else the first free; nil when none is.
func (l *Lobby) seat(sess *gamerelay.Session, token string, want int) *table {
	proxy, closeIdle := proxyTo(sess)
	go func() { <-sess.Done(); closeIdle() }()
	l.mu.Lock()
	var t *table
	for _, x := range l.tables {
		if token != "" && x.token == token {
			t = x
			if x.sess != nil { // back before the lobby saw the old connection go
				go x.sess.Close()
			}
			break
		}
	}
	if t == nil && want >= 1 && want <= len(l.tables) && l.tables[want-1].free() {
		t = l.tables[want-1]
		t.token, t.status = newToken(), nil
	}
	if t == nil {
		for _, x := range l.tables {
			if x.free() {
				t = x
				t.token, t.status = newToken(), nil
				break
			}
		}
	}
	if t != nil {
		if t.held != nil {
			t.held.Stop()
			t.held = nil
		}
		t.sess, t.proxy = sess, proxy
	}
	l.mu.Unlock()
	if t != nil {
		l.changed()
	}
	return t
}

// drop: the desktop's connection ended. The table stays its own for Hold,
// then is free.
func (l *Lobby) drop(t *table, sess *gamerelay.Session) {
	l.mu.Lock()
	if t.sess != sess {
		l.mu.Unlock()
		return
	}
	t.sess, t.proxy = nil, nil
	token := t.token
	t.held = time.AfterFunc(l.opt.Hold, func() {
		l.mu.Lock()
		if t.sess == nil && t.token == token {
			t.token, t.status, t.held = "", nil, nil
		}
		l.mu.Unlock()
		l.changed()
	})
	l.mu.Unlock()
	l.changed()
}

// tableURL is a table's page, as visitors open it.
func (l *Lobby) tableURL(r *http.Request, n int) string {
	base := strings.TrimSuffix(l.opt.PublicURL, "/")
	if base == "" {
		scheme := "http"
		if r.TLS != nil || r.Header.Get("X-Forwarded-Proto") == "https" {
			scheme = "https"
		}
		base = scheme + "://" + r.Host + strings.TrimSuffix(r.URL.Path, "/host")
	}
	return base + "/t/" + strconv.Itoa(n) + "/"
}

// Table is a table as the lobby's page and its watchers see it: free when
// Status is nil and not Away.
type Table struct {
	N      int               `json:"n"`
	Away   bool              `json:"away"`            // its desktop's connection dropped
	Lobby  bool              `json:"lobby,omitempty"` // the lobby hosts its game
	Status *gamerelay.Status `json:"status"`
}

// Tables is what a watcher is sent each time a table changes.
type Tables struct {
	T      string  `json:"t"` // "tables"
	Tables []Table `json:"tables"`
	// Games are the games a visitor may open at a free table (Options.Games).
	Games []string `json:"games,omitempty"`
}

func (l *Lobby) tablesMsg() Tables {
	l.mu.Lock()
	defer l.mu.Unlock()
	out := make([]Table, len(l.tables))
	for i, t := range l.tables {
		out[i] = Table{N: t.n, Away: t.sess == nil && t.token != "", Lobby: t.own != nil, Status: t.status}
	}
	var games []string
	for _, g := range l.opt.Games {
		games = append(games, g.Name)
	}
	return Tables{"tables", out, games}
}

// serveWatch keeps a browser's lobby page up to date.
func (l *Lobby) serveWatch(w http.ResponseWriter, r *http.Request) {
	l.mu.Lock()
	full := len(l.watchers) >= MaxWatchers
	l.mu.Unlock()
	if full {
		http.Error(w, "busy", http.StatusServiceUnavailable)
		return
	}
	c, err := gameweb.Accept(w, r)
	if err != nil {
		return
	}
	l.mu.Lock()
	l.watchers[c] = true
	l.mu.Unlock()
	c.Send(l.tablesMsg())
	var m any
	for c.Read(&m) == nil {
	}
	c.Close()
	l.mu.Lock()
	delete(l.watchers, c)
	l.mu.Unlock()
}

// changed tells every page the tables.
func (l *Lobby) changed() {
	m := l.tablesMsg()
	l.mu.Lock()
	watchers := make([]*gameweb.Client, 0, len(l.watchers))
	for c := range l.watchers {
		watchers = append(watchers, c)
	}
	l.mu.Unlock()
	for _, c := range watchers {
		c.Send(m)
	}
}

var codeRe = regexp.MustCompile(`^[A-Z0-9]{0,8}$`)

// clean keeps of a desktop's status what the page may show.
func clean(st gamerelay.Status) gamerelay.Status {
	if !slices.Contains([]string{"small-fortune", "chinese-checkers"}, st.Game) {
		st.Game = ""
	}
	if !codeRe.MatchString(st.Code) {
		st.Code = ""
	}
	if !slices.Contains([]string{"lobby", "playing", "over"}, st.State) {
		st.State = "lobby"
	}
	st.Seats = st.Seats[:min(len(st.Seats), 6)]
	for i, s := range st.Seats {
		s.Name = cleanName(s.Name)
		if !slices.Contains([]string{"open", "local", "visitor", "computer", "ai"}, s.Kind) {
			s.Kind = "open"
		}
		st.Seats[i] = s
	}
	st.Room = max(0, min(st.Room, 6))
	st.Lead = cleanName(st.Lead)
	return st
}

// cleanName is a name as the page shows it: one line, at most 20 letters.
func cleanName(name string) string {
	name = strings.Join(strings.Fields(name), " ")
	for utf8.RuneCountInString(name) > 20 {
		_, n := utf8.DecodeLastRuneInString(name)
		name = name[:len(name)-n]
	}
	return name
}

func newToken() string {
	b := make([]byte, 18)
	rand.Read(b)
	return base64.RawURLEncoding.EncodeToString(b)
}
