package fortunenet

import (
	"bytes"
	"crypto/sha256"
	"embed"
	"encoding/hex"
	"fmt"
	"io/fs"
	"net"
	"net/http"
	"regexp"
	"strings"
	"time"

	samples "github.com/lyricat/inua/config"
	"github.com/lyricat/inua/internal/games"
	"github.com/lyricat/inua/internal/games/gameai"
	"github.com/lyricat/inua/internal/games/gamerelay"
	"github.com/lyricat/inua/internal/games/gameweb"
	"github.com/lyricat/inua/internal/i18n"
)

// web is the page visitors play on.
//
//go:embed web
var web embed.FS

// DefaultAddr is where a Host listens unless told otherwise: every
// address of this computer, on a port of its own.
const DefaultAddr = ":7341"

type server struct {
	http *http.Server
	port int
}

// Serve listens on addr (DefaultAddr; another port when it is taken)
// for browsers: the page at /, the game at /ws. Called where the Host
// lives, once.
func (h *Host) Serve(addr string) error {
	ln, err := net.Listen("tcp", addr)
	if err != nil && addr == DefaultAddr {
		ln, err = net.Listen("tcp", ":0")
	}
	if err != nil {
		return err
	}
	h.srv = &server{http: &http.Server{Handler: h.Handler(), ReadHeaderTimeout: 10 * time.Second}, port: ln.Addr().(*net.TCPAddr).Port}
	go h.srv.http.Serve(ln)
	return nil
}

// Handler serves browsers the page at /, the game at /ws, the board's
// pictures: Serve's, and a lobby's through a relay (gamerelay.Publish).
func (h *Host) Handler() http.Handler {
	mux := http.NewServeMux()
	page, _ := fs.Sub(web, "web")
	mux.Handle("/", gameweb.Files(page))
	mux.Handle("/vendor/", gameweb.Vendor())
	mux.HandleFunc("/ws", h.serveWS)
	mux.HandleFunc("/board.jpg", h.servePrint)
	mux.HandleFunc("/texts.json", serveTexts)
	mux.HandleFunc("/art/", h.serveArt)
	mux.HandleFunc("/icons/", serveIcon)
	return mux
}

// Port is the port the Host listens on; 0 before Serve.
func (h *Host) Port() int {
	if h.srv == nil {
		return 0
	}
	return h.srv.port
}

// URLs are the addresses visitors open, one for each of this computer's
// addresses on the local network, with the code.
func (h *Host) URLs() []string { return gameweb.URLs(h.Port(), h.Code) }

// Close stops the game: the timers, every browser, the server. Called
// where the Host lives.
func (h *Host) Close() {
	h.closed = true
	if h.ai != nil {
		h.ai.Stop()
	}
	if h.cpu != nil {
		h.cpu.Stop()
	}
	for _, s := range h.Seats {
		if s.gone != nil {
			s.gone.Stop()
		}
	}
	for c := range h.clients {
		c.Close()
	}
	h.clients = map[*gameweb.Client]bool{}
	if h.srv != nil {
		go h.srv.http.Close()
	}
}

func (h *Host) serveWS(w http.ResponseWriter, r *http.Request) {
	c, err := gameweb.Accept(w, r)
	if err != nil {
		return
	}
	joined := false
	for {
		var m inMsg
		if err := c.Read(&m); err != nil {
			break
		}
		switch {
		case m.T == "join" && !joined:
			joined = true
			h.opt.Run(func() {
				if !h.closed {
					h.join(c, m)
				}
			})
		case m.T == "act" && joined:
			h.opt.Run(func() {
				if h.clients[c] && c.Seat >= 0 {
					h.Act(c.Seat, m.Action)
				}
			})
		case joined:
			h.opt.Run(func() {
				if h.clients[c] {
					h.fromLead(c, m)
				}
			})
		}
	}
	c.Close()
	h.opt.Run(func() { h.leave(c) })
}

// servePrint serves the board's print, drawn by the host's screen the
// first time it is asked for.
func (h *Host) servePrint(w http.ResponseWriter, r *http.Request) {
	ch := make(chan []byte, 1)
	h.opt.Run(func() {
		if h.print == nil && h.Game != nil && h.opt.Print != nil && !h.closed {
			h.print = h.opt.Print(h.Game.City)
		}
		ch <- h.print
	})
	var b []byte
	select {
	case b = <-ch:
	case <-time.After(30 * time.Second):
	case <-r.Context().Done():
		return
	}
	if b == nil {
		http.NotFound(w, r)
		return
	}
	w.Header().Set("Content-Type", "image/jpeg")
	w.Header().Set("Cache-Control", "no-cache")
	w.Write(b)
}

// artName is a picture the page may ask for (Options.Art).
var artName = regexp.MustCompile(`^(card-\d{1,2}(-price)?|card-back|sign-\d{1,3}|(house|hotel)-[01]-[0-3]|piece-\d{1,3})$`)

// serveArt serves a picture of the game's, drawn by the host's screen the
// first time it is asked for: /art/NAME.png.
func (h *Host) serveArt(w http.ResponseWriter, r *http.Request) {
	name := strings.TrimSuffix(strings.TrimPrefix(r.URL.Path, "/art/"), ".png")
	if !artName.MatchString(name) {
		http.NotFound(w, r)
		return
	}
	ch := make(chan *Picture, 1)
	h.opt.Run(func() {
		pic, ok := h.art[name]
		if !ok && h.Game != nil && h.opt.Art != nil && !h.closed {
			pic = h.opt.Art(h.Game.City, name)
			if h.art == nil {
				h.art = map[string]*Picture{}
			}
			h.art[name] = pic
		}
		ch <- pic
	})
	var pic *Picture
	select {
	case pic = <-ch:
	case <-time.After(30 * time.Second):
	case <-r.Context().Done():
		return
	}
	if pic == nil || pic.PNG == nil {
		http.NotFound(w, r)
		return
	}
	b := pic.PNG
	if pic.W > 0 { // a piece standing on the board: its size and foot
		w.Header().Set("X-Piece", fmt.Sprintf("%.2f %.2f %.2f %.2f", pic.W, pic.H, pic.FootX, pic.Dv))
	}
	sum := sha256.Sum256(b)
	w.Header().Set("ETag", `"`+hex.EncodeToString(sum[:8])+`"`)
	w.Header().Set("Cache-Control", "no-cache")
	http.ServeContent(w, r, name+".png", time.Time{}, bytes.NewReader(b))
}

var iconName = regexp.MustCompile(`^(fortune-[a-z]+|audio-volume-(high|muted))\.svg$`)

// serveIcon serves one of the game's icons, the shell's own in Phosphor's
// bold weight (inua's sample icon set): /icons/fortune-house.svg. The
// regular weight's hairlines all but vanish in a browser at their size.
func serveIcon(w http.ResponseWriter, r *http.Request) {
	name := strings.TrimPrefix(r.URL.Path, "/icons/")
	if !iconName.MatchString(name) {
		http.NotFound(w, r)
		return
	}
	b, err := fs.ReadFile(samples.FS, samples.IconSet+"/"+strings.TrimSuffix(name, ".svg")+"-symbolic.svg")
	if err != nil {
		http.NotFound(w, r)
		return
	}
	w.Header().Set("Content-Type", "image/svg+xml")
	w.Header().Set("Cache-Control", "max-age=86400")
	w.Write(b)
}

// Status is the game as a lobby lists it: before the game, the people,
// the computer players asked for and the seats open.
func (h *Host) Status() gamerelay.Status {
	st := gamerelay.Status{Game: "small-fortune", Code: h.Code, State: "lobby", Room: h.Room()}
	switch {
	case h.Game != nil && h.Game.Phase == games.PhaseOver:
		st.State = "over"
	case h.Game != nil:
		st.State = "playing"
	}
	for _, s := range h.seatMsgs() {
		st.Seats = append(st.Seats, gamerelay.Seat{Name: s.Name, Kind: s.Kind, Here: s.Here})
	}
	if h.Game == nil {
		for _, name := range h.Settings.AIs {
			st.Seats = append(st.Seats, gamerelay.Seat{Name: name, Kind: "ai", Here: true})
		}
		for i := range h.Settings.Rivals {
			name := games.Rivals[min(i, len(games.Rivals)-1)].Name
			if i < len(h.Settings.RivalNames) && h.Settings.RivalNames[i] != "" {
				name = h.Settings.RivalNames[i]
			}
			st.Seats = append(st.Seats, gamerelay.Seat{Name: i18n.T(name), Kind: "computer", Here: true})
		}
		for range st.Room {
			st.Seats = append(st.Seats, gamerelay.Seat{Kind: "open"})
		}
	}
	if l := h.Lead(); l >= 0 {
		st.Lead = h.Seats[l].Name
	}
	return st
}

// Unattended opens a game with no one at a host's screen, for a lobby to
// host itself (inua-game-lobby): the first visitor sets it up and starts
// it, on a plain board, with AI players when ai answers (nil: computer
// players only). run runs what changes the game, one at a time; changed
// is told, from there, how it stands each time that changes. It returns
// the game's handler, how it stands now, and what ends it.
func Unattended(run func(func()), changed func(gamerelay.Status), ai gameai.AI) (http.Handler, gamerelay.Status, func()) {
	var h *Host
	h = NewHost(Options{
		Settings: games.DefaultFortune,
		LeadAI:   ai,
		Run:      run,
		Changed: func() {
			if h != nil { // not while NewHost sets the seats out
				changed(h.Status())
			}
		},
		Seed: uint64(time.Now().UnixNano()),
	})
	return h.Handler(), h.Status(), func() { run(h.Close) }
}
