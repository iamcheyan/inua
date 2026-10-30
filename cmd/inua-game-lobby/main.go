// Command inua-game-lobby is a lobby for inua's network games
// (docs/game-lobby.md): a row of tables that desktops publish their Small
// Fortune or Chinese Checkers game at, and the page visitors join them
// from. The games run on the desktops; the lobby passes the browsers'
// traffic on. It needs no GTK and no desktop.
package main

import (
	"bytes"
	"flag"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/lyricat/inua/internal/games/lobby"
	"github.com/lyricat/inua/internal/i18n"
)

func main() {
	addr := flag.String("addr", ":7340", "where to listen")
	tables := flag.Int("tables", 8, "how many tables")
	keyFile := flag.String("key-file", "", "a file holding the key a desktop must give to publish a game (none: any desktop may)")
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
	l := lobby.New(lobby.Options{Tables: *tables, Key: key, PublicURL: *public})
	srv := &http.Server{Addr: *addr, Handler: l.Handler(), ReadHeaderTimeout: 10 * time.Second}
	log.Printf("inua-game-lobby: %d tables at %s", *tables, *addr)
	log.Fatal(srv.ListenAndServe())
}
