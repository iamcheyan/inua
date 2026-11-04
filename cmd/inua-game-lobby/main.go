// Command inua-game-lobby is a lobby for inua's network games
// (docs/game-lobby.md): a row of tables that desktops publish their Small
// Fortune or Chinese Checkers game at, and the page visitors join them
// from. The games run on the desktops, and the lobby passes the browsers'
// traffic on; a visitor may also open a game at a free table, which the
// lobby then hosts itself, with the user's AI among its players when run
// with -ai. It needs no GTK and no desktop.
package main

import (
	"bytes"
	"context"
	"flag"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/lyricat/inua/internal/games/checkersnet"
	"github.com/lyricat/inua/internal/games/fortunenet"
	"github.com/lyricat/inua/internal/games/gameai"
	"github.com/lyricat/inua/internal/games/lobby"
	"github.com/lyricat/inua/internal/i18n"
)

func main() {
	addr := flag.String("addr", ":7340", "where to listen")
	tables := flag.Int("tables", 8, "how many tables")
	keyFile := flag.String("key-file", "", "a file holding the key a desktop must give to publish a game (none: any desktop may)")
	desktopsOnly := flag.Bool("desktops-only", false, "only desktops open games: a visitor may not open one at a free table")
	ai := flag.Bool("ai", false, "let the games the lobby hosts have AI players: the user's AI, through inua-assistant --answer")
	public := flag.String("public-url", "", "the lobby's address as visitors open it, when a proxy puts it under another (https://example.org/games)")
	lang := flag.String("lang", "", "the pages' language (default: the environment's)")
	flag.Parse()
	i18n.Init(*lang)
	key := ""
	if *keyFile != "" {
		b, err := os.ReadFile(*keyFile)
		if err != nil {
			log.Fatalf("inua-game-lobby: %v", err)
		}
		key = string(bytes.TrimSpace(b))
	}
	var assistant gameai.AI // none: computer players only
	if *ai && !*desktopsOnly {
		assistant = gameai.NewAssistant(func(ctx context.Context) (gameai.Chooser, []string, error) {
			c, profiles, err := gameai.Launch(ctx)
			if err != nil {
				log.Printf("inua-game-lobby: the AI cannot play: %v", err)
			} else {
				log.Printf("inua-game-lobby: the AI plays, with the profiles %s", strings.Join(profiles, ", "))
			}
			return c, profiles, err
		})
	}
	var games []lobby.Game
	if !*desktopsOnly {
		games = []lobby.Game{
			{Name: "small-fortune", Open: fortunenet.Unattended},
			{Name: "chinese-checkers", Open: checkersnet.Unattended},
		}
	}
	l := lobby.New(lobby.Options{Tables: *tables, Key: key, PublicURL: *public, Games: games, AI: assistant})
	srv := &http.Server{Addr: *addr, Handler: l.Handler(), ReadHeaderTimeout: 10 * time.Second}
	log.Printf("inua-game-lobby: %d tables at %s", *tables, *addr)
	log.Fatal(srv.ListenAndServe())
}
