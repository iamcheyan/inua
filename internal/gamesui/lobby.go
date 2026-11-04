package gamesui

import (
	"net/http"
	"strings"

	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/apps/store"
	"github.com/lyricat/inua/internal/games/gamerelay"
	"github.com/lyricat/inua/internal/games/lobbyservice"
	"github.com/lyricat/inua/internal/gtkx"
	"github.com/lyricat/inua/internal/i18n"
)

// A game at a lobby (inua-game-lobby, docs/game-lobby.md): the game stays
// here and takes a table there, where others join it from a browser. The
// lobby's address is the user's, kept with the games' data, and so is
// where the lobby the Game Lobby window runs here listens.

type lobbyPrefs struct {
	Address string              `json:"address"`
	Host    lobbyservice.Config `json:"host,omitzero"`
}

func lobbyAddress() string {
	if hostAt.addr != "" {
		return hostAt.addr
	}
	var p lobbyPrefs
	store.Load("game-lobby", &p)
	return p.Address
}

func saveLobbyAddress(addr string) {
	var p lobbyPrefs
	store.Load("game-lobby", &p)
	p.Address = addr
	store.Save("game-lobby", p)
}

// hostAt is the lobby and table inua-games was started to host its game
// at (HostAt): the Game Lobby window's Host buttons.
var hostAt struct {
	addr  string
	table int
	open  bool // the setup is still to open with At a lobby on
}

// HostAt starts the game set to host at a lobby's table: its setup opens
// with At a lobby on, at addr, and the game asks for table when it takes
// one (any free one when that is taken).
func HostAt(addr string, table int) {
	hostAt.addr, hostAt.table, hostAt.open = strings.TrimSpace(addr), table, addr != ""
}

// lobbyFirst reports, once, whether the setup opens with At a lobby on.
func lobbyFirst() bool {
	on := hostAt.open
	hostAt.open = false
	return on
}

// lobbyEntry is where the user gives the lobby's address; activate runs
// on Enter.
func lobbyEntry(activate *func(gtk.Entry)) *gtk.Entry {
	e := gtk.NewEntry()
	e.SetText(lobbyAddress())
	e.SetPlaceholderText(i18n.T("The lobby's address"))
	e.SetTooltipText(i18n.T("As the lobby's host gave it: lobby.example.org, with ?key=… when it asks for a key."))
	e.SetHexpand(true)
	e.ConnectActivate(activate)
	return e
}

// publish publishes a game's handler at the lobby at addr, and keeps the
// address; changed runs on the main thread each time its table changes.
func publish(addr string, h http.Handler, changed func()) (*gamerelay.Publication, error) {
	addr = strings.TrimSpace(addr)
	table := 0
	if addr == hostAt.addr {
		table, hostAt.table = hostAt.table, 0 // once: a table again is any table
	}
	pub, err := gamerelay.PublishAt(addr, table, h, func() { gtkx.Post(changed) })
	if err == nil {
		var p lobbyPrefs
		if store.Load("game-lobby", &p); p.Address != addr {
			saveLobbyAddress(addr)
		}
	}
	return pub, err
}

// lobbyState is what the screen says of a game at a lobby: its table's
// link with the code, or why it has none yet.
func lobbyState(pub *gamerelay.Publication, code string) (link, note string) {
	n, url, err := pub.Table()
	switch {
	case n > 0:
		return url + "#" + code, i18n.Tf("At table %d of the lobby.", n)
	case err != nil:
		return "", i18n.Tf("Not at the lobby: %v", err)
	}
	return "", i18n.T("Connecting to the lobby…")
}
