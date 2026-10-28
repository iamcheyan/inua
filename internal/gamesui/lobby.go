package gamesui

import (
	"net/http"
	"strings"

	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/apps/store"
	"github.com/lyricat/inua/internal/games/gamerelay"
	"github.com/lyricat/inua/internal/gtkx"
	"github.com/lyricat/inua/internal/i18n"
)

// A game at a lobby (inua-game-lobby, docs/game-lobby.md): the game stays
// here and takes a table there, where others join it from a browser. The
// lobby's address is the user's, kept with the games' data.

type lobbyPrefs struct {
	Address string `json:"address"`
}

func lobbyAddress() string {
	var p lobbyPrefs
	store.Load("game-lobby", &p)
	return p.Address
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
	pub, err := gamerelay.Publish(addr, h, func() { gtkx.Post(changed) })
	if err == nil && addr != lobbyAddress() {
		store.Save("game-lobby", lobbyPrefs{addr})
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
