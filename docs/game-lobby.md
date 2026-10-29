# The game lobby

`inua-game-lobby` is a page of tables on the internet where people join
Small Fortune and Chinese Checkers games hosted in inua. The games keep
running on the desktops that host them; the lobby lists them and passes
each browser's traffic to the right desktop. A desktop dials the lobby,
so it needs no address others can reach and no open port.

## Playing

- **Hosting.** In the game's setup, turn on **At a lobby** and give the
  lobby's address (`lobby.example.org`; `?key=…` after it when the lobby
  asks for a key). The game takes the first free table, and the setup
  shows the table's link and QR code. **On the network** can stay on as
  well. The address is kept in `~/.local/share/inua/game-lobby.json`.
- **Joining.** Open the lobby, pick a table and **Join** (or **Watch**).
  That opens the table's game page, the same page as on the network.
- **Game Lobby window.** The dock drawer's **Game Lobby** (Play; `inua-games
  game-lobby`) shows a lobby's tables as they change. **Join** and
  **Watch** open a table in the browser; a free table's **Small Fortune**
  and **Chinese Checkers** buttons start that game here with **At a
  lobby** on, set to take that table (`inua-games -lobby ADDRESS
  -lobby-table N GAME`). If the game is already open, it comes forward as
  it is.
- **Setting up.** Only a desktop opens a game. When no one plays at the
  host's screen, the first to join from a browser sets the game up and
  starts it: in Chinese Checkers the seats, teams and rule; in Small
  Fortune the city, rounds, starting money, dice, building the day you
  buy and the computer players. If they leave, the next visitor does.
- **Drops.** A desktop that loses its connection dials again and gets its
  table back within 30 seconds. Browsers reconnect on their own, and the
  computer plays for anyone gone more than 15 seconds.

## Running a lobby

```sh
inua-game-lobby -addr :7340 -tables 8
```

| Flag | |
| --- | --- |
| `-addr` | Where to listen (`:7340`). |
| `-tables` | How many tables (8). |
| `-key-file` | A file holding the key a desktop must give to host. Without one, any desktop may. |
| `-public-url` | The lobby's address as visitors open it, when a proxy puts it under a path (`https://example.org/games`). |
| `-lang` | The pages' language; the environment's by default. |

It serves plain HTTP. Put it behind a proxy that adds TLS and passes
WebSockets on, for example Caddy:

```
lobby.example.org {
	reverse_proxy 127.0.0.1:7340
}
```

The proxy must keep the `Host` header: the game pages check that a
WebSocket comes from their own page.

## How it works

| Path | |
| --- | --- |
| `/` | The lobby's page; `/ws` keeps it up to date. |
| `/host` | A desktop's WebSocket. |
| `/t/N/…` | Table N's game, passed to its desktop. |

A desktop's WebSocket carries many streams (`internal/games/gamerelay`).
Binary messages are frames: a kind (open, data, close, credit), the
stream's number and its bytes. Each stream has its own 256 KiB window, so
a slow browser holds up only itself. Text messages are about the table:
the desktop's `hello` (its key, and a token to get its table back), the
lobby's `table` (its number and link) or `bye` (a wrong key, no free
table), and the desktop's `status` (the game, the code, the seats, room
left, who sets it up), which is what the lobby's page shows.

Each stream is a `net.Conn`. The lobby proxies a browser's request with
`httputil.ReverseProxy` over a new stream, WebSockets included, and the
desktop serves it with the game's own handler (`checkersnet.Host.Handler`,
`fortunenet.Host.Handler`), the same one the network uses.

The lobby holds no games and stores nothing. The join code is in the
table's link, so anyone at the lobby can join a game with an open seat;
the host can send a visitor away.
