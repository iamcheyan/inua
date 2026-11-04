package lobby

import (
	"encoding/json"
	"mime"
	"net/http"
	"net/url"
	"strconv"
	"sync"
	"time"

	"github.com/gorilla/websocket"

	"github.com/lyricat/inua/internal/games/gameai"
	"github.com/lyricat/inua/internal/games/gamerelay"
	"github.com/lyricat/inua/internal/i18n"
)

// Game is a game the lobby may host itself, at a free table a visitor
// opens it at.
type Game struct {
	// Name is the game as a Status names it: "small-fortune",
	// "chinese-checkers".
	Name string
	// Open opens a game with no one at a host's screen: run runs what
	// changes it, one at a time; changed is told, from there, how it
	// stands each time that changes; ai, when not nil, may play in it
	// (Options.AI). It returns the game's handler, how it stands now and
	// what ends it (fortunenet.Unattended, checkersnet.Unattended).
	Open func(run func(func()), changed func(gamerelay.Status), ai gameai.AI) (http.Handler, gamerelay.Status, func())
}

// hosted is a game the lobby hosts at a table, until no browser has been
// at it for Idle, or it has been over for Over.
type hosted struct {
	end   func()
	conns int  // browsers at the table's game (its WebSockets)
	over  bool // the game is over
	wait  string
	timer *time.Timer // frees the table, for wait: "idle" or "over"
	gen   int         // which timer is the current one
}

// serveNew opens a visitor's game at a free table: {"game", "table"}
// in, {"table", "url"} out, url the table's page with its code, relative
// to the lobby's.
func (l *Lobby) serveNew(w http.ResponseWriter, r *http.Request) {
	reply := func(status int, v any) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(status)
		json.NewEncoder(w).Encode(v)
	}
	fail := func(status int, text string) { reply(status, map[string]string{"error": text}) }
	if len(l.opt.Games) == 0 {
		fail(http.StatusForbidden, i18n.T("Only a host opens games at this lobby."))
		return
	}
	// A page elsewhere may not open games here: a form cannot send JSON,
	// and a script's request says where it comes from.
	if ct, _, _ := mime.ParseMediaType(r.Header.Get("Content-Type")); ct != "application/json" {
		fail(http.StatusUnsupportedMediaType, "application/json")
		return
	}
	if o := r.Header.Get("Origin"); o != "" {
		if u, err := url.Parse(o); err != nil || u.Host != r.Host {
			fail(http.StatusForbidden, i18n.T("A page elsewhere may not open games here."))
			return
		}
	}
	var req struct {
		Game  string `json:"game"`
		Table int    `json:"table"`
	}
	if json.NewDecoder(http.MaxBytesReader(w, r.Body, 1<<10)).Decode(&req) != nil {
		fail(http.StatusBadRequest, i18n.T("The lobby does not host that game."))
		return
	}
	var game *Game
	for i := range l.opt.Games {
		if l.opt.Games[i].Name == req.Game {
			game = &l.opt.Games[i]
		}
	}
	if game == nil {
		fail(http.StatusBadRequest, i18n.T("The lobby does not host that game."))
		return
	}
	code, ok := l.host(*game, req.Table)
	if !ok {
		fail(http.StatusConflict, i18n.T("Someone took this table first."))
		return
	}
	reply(http.StatusOK, map[string]any{"table": req.Table, "url": "t/" + strconv.Itoa(req.Table) + "/#" + code})
}

// host opens game at table n when it is free, hosted here; its join code.
func (l *Lobby) host(game Game, n int) (string, bool) {
	own := &hosted{}
	l.mu.Lock()
	if n < 1 || n > len(l.tables) || !l.tables[n-1].free() {
		l.mu.Unlock()
		return "", false
	}
	t := l.tables[n-1]
	t.own, t.status = own, nil // the table is taken while the game opens
	l.mu.Unlock()

	var mu sync.Mutex
	run := func(f func()) {
		mu.Lock()
		defer mu.Unlock()
		f()
	}
	h, st, end := game.Open(run, func(st gamerelay.Status) { l.hostedStatus(t, own, st) }, l.opt.AI)
	st = clean(st)
	l.mu.Lock()
	own.end = end
	t.proxy = l.hostedProxy(t, own, h)
	if t.status == nil { // unless the game told already
		t.status = &st
	}
	l.arm(t)
	l.mu.Unlock()
	l.changed()
	return st.Code, true
}

// hostedStatus: the lobby's own game at t says how it stands.
func (l *Lobby) hostedStatus(t *table, own *hosted, st gamerelay.Status) {
	st = clean(st)
	l.mu.Lock()
	if t.own != own {
		l.mu.Unlock()
		return
	}
	t.status = &st
	own.over = st.State == "over"
	if own.end != nil {
		l.arm(t)
	}
	l.mu.Unlock()
	l.changed()
}

// hostedProxy serves the table's path to the lobby's own game, counting
// the browsers at it.
func (l *Lobby) hostedProxy(t *table, own *hosted, h http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		r2 := r.Clone(r.Context())
		r2.URL.Path, r2.URL.RawPath = "/"+r.PathValue("rest"), ""
		if websocket.IsWebSocketUpgrade(r) {
			l.browsers(t, own, 1)
			defer l.browsers(t, own, -1)
		}
		h.ServeHTTP(w, r2)
	})
}

// browsers counts a browser come to the lobby's own game at t, or gone.
func (l *Lobby) browsers(t *table, own *hosted, d int) {
	l.mu.Lock()
	defer l.mu.Unlock()
	if t.own == own {
		own.conns += d
		l.arm(t)
	}
}

// arm sets the timer that frees a table the lobby hosts a game at: Idle
// once no browser is at it, Over once its game is over. Called with mu
// held.
func (l *Lobby) arm(t *table) {
	own := t.own
	wait, after := "", time.Duration(0)
	switch {
	case own.conns <= 0:
		wait, after = "idle", l.opt.Idle
	case own.over:
		wait, after = "over", l.opt.Over
	}
	if wait == own.wait {
		return
	}
	own.wait = wait
	own.gen++
	if own.timer != nil {
		own.timer.Stop()
		own.timer = nil
	}
	if wait == "" {
		return
	}
	gen := own.gen
	own.timer = time.AfterFunc(after, func() {
		l.mu.Lock()
		if t.own != own || own.gen != gen {
			l.mu.Unlock()
			return
		}
		t.own, t.proxy, t.status = nil, nil, nil
		l.mu.Unlock()
		own.end()
		l.changed()
	})
}
