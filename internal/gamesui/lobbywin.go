package gamesui

import (
	"context"
	"encoding/json"
	"fmt"
	"html"
	"os"
	"strconv"
	"strings"
	"time"

	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/apps/store"
	"github.com/lyricat/inua/internal/desktop"
	"github.com/lyricat/inua/internal/games/gamerelay"
	"github.com/lyricat/inua/internal/games/lobby"
	"github.com/lyricat/inua/internal/gtkx"
	"github.com/lyricat/inua/internal/i18n"
)

// The Game Lobby window: the tables of an inua-game-lobby as they change,
// each with its game and players. Join and Watch open the table's page in
// the browser; a free table's Host buttons start Small Fortune or Chinese
// Checkers set to take that table. Above them, a lobby can run on this
// computer (lobbyhost.go), and the window then shows its tables.

type lobbyRoom struct {
	f      *frame
	addr   *gtk.Entry
	open   *gtk.Button
	flow   *gtk.FlowBox
	cancel context.CancelFunc
	gen    int    // the connection the tables shown came from
	shown  string // the tables shown, as JSON: built again only when they change
	at     string // the address connected to
	host   *lobbyHost

	onAddr    func(gtk.Entry)
	onConnect func(gtk.Button)
	onOpen    func(gtk.Button)
	onAct     func(gtk.Button)
}

func (p *lobbyRoom) setup(f *frame) {
	p.f = f
	f.win.SetDefaultSize(1040, 760)
	f.restart.SetVisible(false)
	p.hostSection(f)

	row := gtk.NewBox(gtk.OrientationHorizontalValue, 8)
	row.AddCssClass("lobby-address")
	p.onAddr = func(gtk.Entry) { p.reset() }
	p.addr = lobbyEntry(&p.onAddr)
	gtkx.Append(row, &p.addr.Widget)
	p.onConnect = func(gtk.Button) { p.reset() }
	connect := button(i18n.T("Connect"), &p.onConnect)
	gtkx.Append(row, &connect.Widget)
	p.onOpen = func(gtk.Button) {
		if u, err := gamerelay.PageURL(p.at, "/"); err == nil {
			p.browse(u)
		}
	}
	p.open = button(i18n.T("Open in the browser"), &p.onOpen)
	gtkx.Append(row, &p.open.Widget)
	gtkx.Append(&f.body, &row.Widget)

	p.flow = gtk.NewFlowBox()
	p.flow.AddCssClass("lobby-tables")
	p.flow.SetSelectionMode(gtk.SelectionNoneValue)
	p.flow.SetHomogeneous(true)
	p.flow.SetMinChildrenPerLine(1)
	p.flow.SetMaxChildrenPerLine(4)
	p.flow.SetColumnSpacing(12)
	p.flow.SetRowSpacing(12)
	p.flow.SetValign(gtk.AlignStartValue)
	sw := gtk.NewScrolledWindow()
	sw.SetPolicy(gtk.PolicyNeverValue, gtk.PolicyAutomaticValue)
	sw.SetVexpand(true)
	sw.SetChild(&p.flow.Widget)
	gtkx.Append(&f.body, &sw.Widget)

	p.onAct = func(b gtk.Button) { p.act(b.GetName()) }
}

// reset connects to the lobby at the address given, dropping the last
// connection; it tries again while the window is open.
func (p *lobbyRoom) reset() {
	if p.cancel != nil {
		p.cancel()
		p.cancel = nil
	}
	p.gen++
	p.shown = ""
	p.flow.RemoveAll()
	p.at = strings.TrimSpace(p.addr.GetText())
	p.open.SetSensitive(false)
	if p.at == "" {
		p.f.say(i18n.T("Give the address of a game lobby to see its tables."), "")
		p.addr.GrabFocus()
		return
	}
	if _, err := gamerelay.WatchURL(p.at); err != nil {
		p.f.say(err.Error(), "bad")
		return
	}
	p.f.say(i18n.T("Connecting to the lobby…"), "")
	ctx, cancel := context.WithCancel(context.Background())
	p.cancel = cancel
	gen, addr := p.gen, p.at
	go func() {
		wait := time.Second
		for ctx.Err() == nil {
			start := time.Now()
			err := lobby.Watch(ctx, addr, func(ts []lobby.Table) {
				gtkx.Post(func() {
					if gen == p.gen {
						p.show(ts)
					}
				})
			})
			if ctx.Err() != nil {
				return
			}
			if time.Since(start) > time.Minute {
				wait = time.Second
			}
			gtkx.Post(func() {
				if gen == p.gen {
					p.f.say(i18n.Tf("The lobby cannot be reached: %v. Trying again…", err), "bad")
					if addr == p.host.local {
						p.host.refresh() // the lobby run here: how it stands
					}
				}
			})
			select {
			case <-time.After(wait):
			case <-ctx.Done():
				return
			}
			wait = min(wait*2, 15*time.Second)
		}
	}()
}

func (p *lobbyRoom) redraw() {}

// show shows the tables, when they changed.
func (p *lobbyRoom) show(ts []lobby.Table) {
	var prefs lobbyPrefs
	if store.Load("game-lobby", &prefs); prefs.Address != p.at && p.at != p.host.local {
		saveLobbyAddress(p.at) // it is a lobby: keep it, as hosting does; not the one run here, which goes
	}
	p.open.SetSensitive(true)
	playing, free := 0, 0
	for _, t := range ts {
		switch {
		case t.Status != nil:
			playing++
		case !t.Away:
			free++
		}
	}
	p.f.say(i18n.Tf("Games at %d of %d tables; %d free.", playing, len(ts), free), "")
	b, _ := json.Marshal(ts)
	if string(b) == p.shown {
		return
	}
	p.shown = string(b)
	p.flow.RemoveAll()
	for _, t := range ts {
		card := p.card(t)
		p.flow.Append(&card.Widget)
	}
}

// gameTitles are the games a table may hold, by their command names.
var gameTitles = map[string]string{"small-fortune": i18n.M("Small Fortune"), "chinese-checkers": i18n.M("Chinese Checkers")}

// card is a table: its number and state, its game and players, and what
// can be done there.
func (p *lobbyRoom) card(t lobby.Table) *gtk.Box {
	box := gtk.NewBox(gtk.OrientationVerticalValue, 8)
	box.AddCssClass("lobby-table")
	head := gtk.NewBox(gtk.OrientationHorizontalValue, 8)
	k := gtk.NewLabel(i18n.Tf("TABLE %d", t.N))
	k.AddCssClass("kicker")
	k.SetXalign(0)
	k.SetHexpand(true)
	gtkx.Append(head, &k.Widget)
	state := gtk.NewLabel("")
	state.AddCssClass("lobby-state")
	state.SetEllipsize(3) // end
	gtkx.Append(head, &state.Widget)
	gtkx.Append(box, &head.Widget)
	title := gtk.NewLabel("")
	title.AddCssClass("fortune-card-title")
	title.SetXalign(0)
	gtkx.Append(box, &title.Widget)
	note := func(text string) {
		l := gtk.NewLabel(text)
		l.AddCssClass("fortune-city-sub")
		l.SetXalign(0)
		l.SetWrap(true)
		gtkx.Append(box, &l.Widget)
	}
	acts := gtk.NewBox(gtk.OrientationHorizontalValue, 6)
	acts.AddCssClass("lobby-acts")
	act := func(label, name string, primary bool) {
		b := button(label, &p.onAct)
		b.SetName(name)
		b.SetHexpand(true)
		if primary {
			b.RemoveCssClass("outlined")
			b.AddCssClass("primary")
		}
		gtkx.Append(acts, &b.Widget)
	}
	spacer := gtk.NewBox(gtk.OrientationVerticalValue, 0)
	spacer.SetVexpand(true)

	st := t.Status
	if t.Away {
		box.AddCssClass("away")
		state.SetText(i18n.T("Reconnecting…"))
		state.AddCssClass("waiting")
	}
	switch {
	case st == nil && t.Away:
		note(i18n.T("The host’s connection dropped: waiting for it to come back…"))
		gtkx.Append(box, &spacer.Widget)
		return box
	case st == nil:
		box.AddCssClass("free")
		title.SetText(i18n.T("Free"))
		note(i18n.T("Host a game here: it opens set to this table."))
		gtkx.Append(box, &spacer.Widget)
		n := strconv.Itoa(t.N)
		act(i18n.T("Small Fortune"), "host:"+n+":small-fortune", false)
		act(i18n.T("Chinese Checkers"), "host:"+n+":chinese-checkers", false)
		gtkx.Append(box, &acts.Widget)
		return box
	}
	title.SetText(i18n.T(gameTitles[st.Game]))
	if t.Away {
		note(i18n.T("The host’s connection dropped: waiting for it to come back…"))
	} else {
		switch st.State {
		case "lobby":
			state.SetText(i18n.T("Waiting to start"))
			if st.Room > 0 {
				state.SetText(i18n.Tf("Open seats: %d", st.Room))
				state.AddCssClass("open")
			}
		case "playing":
			state.SetText(i18n.T("Playing"))
		case "over":
			state.SetText(i18n.T("Over"))
		}
	}
	kinds := map[string]string{"local": i18n.T("at the host's screen"), "visitor": i18n.T("in a browser"),
		"computer": i18n.T("computer"), "ai": i18n.T("AI")}
	for _, s := range st.Seats {
		r := gtk.NewBox(gtk.OrientationHorizontalValue, 8)
		r.AddCssClass("lobby-seat")
		name := gtk.NewLabel("")
		name.SetXalign(0)
		name.SetHexpand(true)
		name.SetEllipsize(3)
		switch {
		case s.Kind == "open":
			r.AddCssClass("open")
			name.SetMarkup("○  " + html.EscapeString(i18n.T("Open seat")))
		default:
			name.SetMarkup("●  " + html.EscapeString(s.Name))
			if s.Kind == "local" || s.Kind == "visitor" {
				r.AddCssClass("person")
			}
			if s.Kind == "visitor" && !s.Here {
				r.AddCssClass("gone")
			}
		}
		gtkx.Append(r, &name.Widget)
		if s.Kind != "open" {
			kind := gtk.NewLabel(kinds[s.Kind])
			kind.AddCssClass("fortune-city-sub")
			gtkx.Append(r, &kind.Widget)
		}
		gtkx.Append(box, &r.Widget)
	}
	if st.Lead != "" {
		note(i18n.Tf("%s sets up the game", st.Lead))
	}
	gtkx.Append(box, &spacer.Widget)
	page := fmt.Sprintf("%d#%s", t.N, st.Code)
	if st.State == "lobby" && st.Room > 0 && !t.Away {
		act(i18n.T("Join"), "page:"+page, true)
	}
	act(i18n.T("Watch"), "page:"+page, false)
	gtkx.Append(box, &acts.Widget)
	return box
}

// act does what a card's button is for: "page:N#CODE" opens the table's
// page, "host:N:GAME" starts the game set to host at table N.
func (p *lobbyRoom) act(name string) {
	kind, rest, _ := strings.Cut(name, ":")
	switch kind {
	case "page":
		n, code, _ := strings.Cut(rest, "#")
		if u, err := gamerelay.PageURL(p.at, "/t/"+n+"/"); err == nil {
			p.browse(u + "#" + code)
		}
	case "host":
		n, game, _ := strings.Cut(rest, ":")
		self, err := os.Executable()
		if err != nil {
			self = "inua-games"
		}
		if err := desktop.Spawn([]string{self, "-lobby", p.at, "-lobby-table", n, game}, ""); err != nil {
			p.f.say(err.Error(), "bad")
		}
	}
}

// browse opens a page in the browser.
func (p *lobbyRoom) browse(url string) {
	if err := desktop.Spawn([]string{"xdg-open", url}, ""); err != nil {
		p.f.say(i18n.Tf("The browser could not be opened: %v", err), "bad")
	}
}
