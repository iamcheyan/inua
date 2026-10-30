// Command inua-games runs one of inua's light games, each its own app
// with its own window: inua-games minesweeper | space-pinball |
// small-fortune | chinese-checkers | game-lobby.
package main

import (
	"flag"
	"fmt"
	"os"
	"slices"
	"strings"

	"github.com/lyricat/inua/internal/appui"
	"github.com/lyricat/inua/internal/gamesui"
)

func main() {
	uiDir := flag.String("ui-dir", "", "read layouts and styles from this directory instead of the embedded copy")
	lobbyAddr := flag.String("lobby", "", "open the game's setup set to host at this game lobby")
	lobbyTable := flag.Int("lobby-table", 0, "with -lobby, the table to host at when it is free")
	flag.Usage = func() {
		fmt.Fprintln(os.Stderr, "usage: inua-games [-ui-dir DIR] [-lobby ADDRESS [-lobby-table N]] GAME")
		fmt.Fprintln(os.Stderr, "games: "+strings.Join(gamesui.Names(), ", "))
	}
	flag.Parse()
	if flag.NArg() != 1 || !slices.Contains(gamesui.Names(), flag.Arg(0)) {
		flag.Usage()
		os.Exit(2)
	}
	gamesui.HostAt(*lobbyAddr, *lobbyTable)
	gamesui.Register()
	os.Exit(appui.Run(flag.Arg(0), nil, *uiDir))
}
