# The game lobby

`inua-game-lobby` is a page of tables on the internet where people join
Small Fortune and Chinese Checkers games hosted in inua. The games keep
running on the desktops that host them; the lobby lists them and passes
each browser's traffic to the right desktop. A desktop dials the lobby,
so it needs no address others can reach and no open port. A visitor can
also open a game at a free table with no desktop at all: the lobby then
hosts it itself.

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
- **A lobby on this computer.** The Game Lobby window's **Run a lobby on
  this computer** runs `inua-game-lobby` as a systemd user service
  (`inua-game-lobby.service`, restarted when it fails), so its games go
  on when the window closes. It listens on port 7340 of **This network**
  (every address of this computer) or of **Tailscale** (its Tailscale
  address only, for the devices on the tailnet); the choice is kept in
  `game-lobby.json`. While it runs the window shows the address others
  open with its QR code, and its tables; it shows the service's state
  (off, starting, listening, failed) and, when it fails, the
  `journalctl --user -u inua-game-lobby.service` that says why. The
  service runs as the user with `-ai`, so the games it hosts may have AI
  players. It is not started again at login.
- **Opening a game from the page.** A free table has a button for each
  game. It opens that game there, hosted by the lobby, and takes the
  visitor to its page to join it like any other; others join from the
  lobby. Small Fortune starts with two computer players, Chinese Checkers
  with two open seats, and the setup can change both. Small Fortune is on
  a plain board there: the board's print and pictures are drawn by a
  desktop. The table is free again once no browser has had the game open
  for 2 minutes, or 10 minutes after the game is over if no one starts it
  again. `-desktops-only` turns this off.
- **Setting up.** When no one plays at the host's screen (always, in a
  game the lobby hosts), the first to join from a browser sets the game up
  and starts it: in Chinese Checkers the seats, teams and rule; in Small
  Fortune the city, rounds, starting money, dice, building the day you
  buy and the computer players. If they leave, the next visitor does.
- **The AI.** Where the host can ask the user's AI (Settings → AI,
  through `inua-assistant --answer`), the setup in the browser offers it
  beside the computer: **AI players** in Small Fortune, each asking the
  default profile, and an **AI** seat with a profile in Chinese Checkers.
  A desktop whose game no one plays at its screen starts the AI for this;
  a lobby does with `-ai`. When the AI is not there the setup offers the
  computer only, and when it does not answer in a game the computer plays
  that turn, and after three such turns the rest of the game.
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
| `-key-file` | A file holding the key a desktop must give to host. Without one, any desktop may. Visitors opening a game from the page need none. |
| `-desktops-only` | Only desktops open games: free tables have no buttons, and the lobby hosts none itself. |
| `-ai` | The games the lobby hosts may have AI players: the user's AI, through `inua-assistant --answer`, started with the lobby and again when it ends. The lobby must run as that user, with their session's bus for the keyring; off by default, so a public lobby's visitors do not spend the user's AI. |
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
| `/new` | A visitor's new game: a POST of `{"game", "table"}` in JSON from the lobby's own page, answered with the table's link and code. |
| `/t/N/…` | Table N's game, passed to its desktop or to the lobby's own. |

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

A game the lobby hosts runs in the lobby's process with the same code a
desktop runs (`fortunenet.Unattended`, `checkersnet.Unattended`: a host
with no one at its screen), and the table's requests go straight to its
handler. The lobby counts the WebSockets open to it to know when everyone
has left, and ends the game when it frees the table. A desktop asking for
that table is given another. With `-ai`, the lobby keeps one
`inua-assistant --answer` for all its games (`internal/games/gameai`):
started at once, offered while it answers, started again at most once a
minute when it could not start or has ended; its games' AI players are
played by the desktop's own code (`fortuneai`, `checkersai`).

The Game Lobby window's own lobby is a transient systemd user unit
(`internal/games/lobbyservice`): `systemd-run --user
--unit=inua-game-lobby.service --property=Restart=on-failure`, with the
session's `XDG_RUNTIME_DIR`, `DBUS_SESSION_BUS_ADDRESS`, `PATH` and
language, running `inua-game-lobby -addr ADDR -public-url URL -ai`; the
public URL is this computer's address on its home network, or its
Tailscale address, for the links desktops are given. The window reads
its state with `systemctl --user show` and connects to it at
`127.0.0.1:7340` (on the tailnet, at the Tailscale address).

The lobby stores nothing, and holds no games but those visitors open. The
join code is in the table's link, so anyone at the lobby can join a game
with an open seat; a desktop's host can send a visitor away.
