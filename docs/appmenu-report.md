# Global application menu: state, evidence, and limits

The top bar shows the focused application's menu. This records what each part
does, what was measured on the real desktop, and what is deliberately not
covered.

## How an application publishes its menu

`internal/appui/menu.go` builds one `GMenu` for the window's own menu bar and
publishes the same tree as `com.canonical.dbusmenu`, under a well-known name of
its own:

```
io.github.lyricat.Inua.Menu.p<PID>.w<N>     object /io/github/lyricat/Inua/MenuBar
```

`internal/dbusmenu` implements the protocol: `GetLayout`, `GetGroupProperties`,
`GetProperty`, `Event`, `AboutToShow`, `AboutToShowGroup`, and the `Version` /
`Status` / `TextDirection` / `IconThemePath` properties. A submenu is a node
with children; the window's own `GtkPopoverMenuBar` and the published tree come
from the same `[]MenuGroup`, so the two cannot drift.

## How the shell finds it

`internal/appmenu/client.go` tries, in order:

1. **`com.canonical.AppMenu.Registrar`** — the de-facto protocol (KDE, Unity,
   Mavernix). Its association key is an **X11 window ID**, so it covers Qt and
   XWayland applications.
2. **inua's own names** — the shell asks the bus which of those names belong to
   the focused process, by the owner's Unix PID. This is how a native Wayland
   GTK4 window gets a global menu without pretending a PID is an XID.
3. **AT-SPI** — last, and only when the tree has at least one labelled item.
   Plain GTK4 answers with a skeleton (a menu bar with unnamed items); taking
   that at face value used to put blank buttons in the bar and hide the real
   menu.

A process that owns **more than one** menu name (several windows) shows no
global menu: without a per-window identity the shell cannot tell which window
is focused, and showing the wrong window's commands is worse than showing none.

## What GTK and GNOME do

- **GTK3** can export a menubar through `appmenu-gtk-module` on X11, which is
  what feeds the Canonical registrar.
- **GTK4** has no export mechanism at all — `gtk_application_dbus_register()`
  registers nothing, no `_GTK_MENUBAR_OBJECT_PATH` property is set, and no GTK4
  appmenu module exists. A GTK4 application that wants a global menu has to
  publish dbusmenu itself, which is what inua's apps now do.
- **GNOME Shell** has no global-menu service and its applications publish
  nothing, so they correctly show no menu.

## Measured on the real desktop (hx90, Hyprland, one 1280x1024 output)

For each application: start it, read its published tree from the session bus,
and record the labels. This is the exact data the bar renders.

| Application | Published menu |
| --- | --- |
| Clock | View | World clocks | Alarms | Stopwatch | Timer |
| Calculator | 編集 | Copy result | 歴史 |
| Calendar | View | 今日 |
| Weather | View | 更新 | 場所 |
| Stocks | View | 更新 | Find a stock |
| Color Picker | 編集 | Pick a color | 履歴をクリアする |
| System Monitor | View | Processes | システム |
| Tailscale | View | 更新 | デバイス | このデバイス |
| Pass | ファイル | 新しいエントリー | Add store | 検索 |
| GPG | View | 暗号化 | 復号 | キー |
| Music | ファイル | ファイルを開く | ファイルを追加 | プレイリストを読み込む | プレイリストを保存 | Play or pause | Next track |
| Video | ファイル | ビデオを開く | Play or pause | Fullscreen |

Interface, end to end (screenshots in `docs/appmenu-evidence/`):

- the focused Clock window puts **View** in the bar, right of its title;
- clicking it opens a panel hanging under the bar with the four items above;
- clicking **Timer** switches the app to its timer page — the click travels
  bar -> dbusmenu `Event` -> the window's `GAction` -> the app;
- `dolphin-cascade.png` shows a submenu opened *beside* its item, level with
  it: the cascade, for an application that has a real second level.

## Fixed while proving it

| Symptom | Cause |
| --- | --- |
| No menu at all | The published name had two dots (Menu..p...), which is not a valid D-Bus name |
| Every light app's window went blank | `menuWindow` appended the window's child before detaching it; GTK refuses a second parent and the content vanished |
| Blank buttons in the bar | The AT-SPI skeleton (unnamed menubar) was accepted before the real menu |
| Games crashed at startup | `frame.go` took `root`/`help` from the builder *after* `u.Close()`; `game.blp` also had no `root` object |
| Menu measured at 12x2 px | The test hook measured before layout; it now waits for the bar to lay out |

## Not claimed

- No screenshot here shows a second-level submenu of an inua application. The
  Terminal's `View -> Font` is wired (the one nested menu in inua's own apps),
  but the cascade picture in this repository is Dolphin's.
- Multi-window inua applications (Files, Mail, Terminal with several windows)
  intentionally show no global menu.
- Games, Files, Mail and the Terminal were checked by starting them and reading
  their published trees; their bar rendering was not photographed one by one.
