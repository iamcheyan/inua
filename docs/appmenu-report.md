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

1. **`com.canonical.AppMenu.Registrar`** — the de-facto protocol (Unity,
   Mavernix). Its association key is an **X11 window ID**, so it covers Qt and
   XWayland applications that register with it.
2. **KDE's own export** — a KDE application (Dolphin, Kate, Konsole) publishes
   `com.canonical.dbusmenu` at `/MenuBar/N` **on its own well-known name**
   (`org.kde.dolphin-280254`), one child of `/MenuBar` per window. KDE does not
   use the Canonical registrar, and its applications are native Wayland, so
   this is the only place their menu is. The child is found by introspecting
   `/MenuBar`, not guessed: KDE numbers it after the window.
3. **inua's own names** — the shell asks the bus which of those names belong to
   the focused process, by the owner's Unix PID. This is how a native Wayland
   GTK4 window gets a global menu without pretending a PID is an XID.
4. **AT-SPI** — last. It is what browsers offer: Firefox and Chromium expose a
   menubar of labelled sections (`File`, `Edit`, …), while plain GTK4 answers
   with a skeleton (a menu bar with unnamed items). A menu counts only when it
   has a section with items under it, so the skeleton and a browser's
   not-yet-filled sections never put empty buttons in the bar.

A process that owns **more than one** menu name (several windows) shows no
global menu: without a per-window identity the shell cannot tell which window
is focused, and showing the wrong window's commands is worse than showing none.

The bar names the application, not the window: its icon, its name, then its
menus, the same way for every application. The window's own title stays in
the overview, where the window is what matters.

## What each toolkit offers

| Application | Where its menu comes from |
| --- | --- |
| inua's own apps (Files, Mail, Terminal, the light apps, the games) | dbusmenu, published by `internal/appui` (below) |
| Dolphin, Kate, Konsole (KDE, native Wayland) | `com.canonical.dbusmenu` at `/MenuBar/N` on `org.kde.<app>-<pid>` |
| Firefox | AT-SPI: a menubar of sections; the items appear when a section opens |
| Chromium, Chrome | AT-SPI, the same shape as Firefox |
| VS Code | AT-SPI exposes one menu ("その他"), not the bar's sections: no global menu |
| other GTK4 apps | nothing to publish; their menu bar is inside the window |

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


## The rest of the applications

Same method, same session bus.

| Application | Published menu |
| --- | --- |
| Minesweeper | ゲーム / 新しいゲーム / 小・9×9 / 中・16×16 / 大・30×16 / Help / 遊び方 |
| Space Pinball | ゲーム / 新しいゲーム / 一時停止 / Toggle sound / Help / 遊び方 |
| Small Fortune | ゲーム / 最初からやり直す / 図鑑 / メニューに戻る / Toggle sound / Help / 遊び方 |
| Chinese Checkers | ゲーム / 新しいゲーム / 設定し直す / Help / 遊び方 |
| Files | ファイル / 新しい窓 / New Tab / 新規フォルダー… / 新規ファイル… / 開く / アプリケーションで開く… / ウィンドウを閉じる / 編集 / 元に戻す / 切り取る / コピー / 貼り付け / 完全に削除… / Select All / Invert Selection / View / 戻る / 転送 / 上へ / 再読み込み / 検索 / List / Grid / 列 / 隠しファイル / 詳細 / Help / Keyboard Shortcuts |
| Mail | ファイル / 新規メッセージ / 設定 / メッセージ / 返信 / 全員に返信 / 転送 / アーカイブ / ゴミ箱に移動 / 未読にする / View / 検索 / Toggle Sidebar |
| Terminal | ターミナル / 設定 / ターミナルホストを再起動 / やめる / シェル / … / 編集 / … / View / … / **フォント** / Larger Font / Smaller Font / Reset Font / 窓 / … / Help / … |

The Terminal is the one inua application with a real second level: `View` holds a
`フォント` submenu with three commands, published as a node with children and
opened beside its row by the bar's cascade.

## What runs

`nixos-rebuild switch` builds inua from this checkout; the machine now runs the
switched generation, and every application above was started from it.

## Desktop applications read on the real session

Read from the live session, through the client the bar uses, with each
application focused. These are the trees the bar renders.

| Application | Source | What the bar showed |
| --- | --- | --- |
| Dolphin | KDE `/MenuBar/2` | ファイル / 編集 / 表示 / 移動 / ツール / 設定 / ヘルプ, each with its items (20, 19, 23, 7, 5, 8, 10) |
| Kate | AT-SPI | ファイル / 編集 / Selection / 表示 / 移動 / Projects / LSP Client / セッション / ツール / 設定 / ヘルプ |
| Chrome | AT-SPI | ファイル / 編集 / 表示 / 履歴 / ツール / プロファイル / ヘルプ |
| Firefox | AT-SPI | File / Edit / View / History / Bookmarks / Profiles / Tools / Help |
| VS Code | AT-SPI | none: one "その他" menu, not the bar's sections |

## Fixed in this pass

| Symptom | Cause |
| --- | --- |
| A KDE application (Dolphin, Kate) showed no menu | Inua only asked the Canonical registrar; KDE publishes at `/MenuBar/N` on its own name, which was never read |
| A browser showed no menu | AT-SPI's name and role are *properties* there, and inua read only the legacy methods; and `DoAction` sent a `uint32` index where the bus's signature is `i` (`int32`), so every call failed |
| A browser's sections came out empty, or as blank buttons | Labelled `role=33` sections were spliced in as if they were Qt's unnamed popup nodes; and a menu was accepted with no items under it |
| The bar jumped to the dock's edge while a menu was open, and the menu drew over the window instead of under the bar | The menu raised the bar to the **overlay** layer while the dock stayed on **top**; Hyprland reserves space in layer order, so the dock took its width first and the bar was laid out after it. The menu now hangs in the bar's own layer (`top`) |
| The bar showed the window's title, not the application | It now shows the application: its icon, its name, then its menus, the same format for every application |
| Reopening a menu crashed the shell (SIGSEGV in `g_object_ref`) | Closing a panel moved its key controller out of the bar without holding a reference; the controller was freed and the next open moved a dead object |

## Not claimed

- No screenshot here shows a second-level submenu of an inua application. The
  Terminal's `View -> Font` is wired (the one nested menu in inua's own apps),
  but the cascade picture in this repository is Dolphin's.
- Multi-window inua applications (Files, Mail, Terminal with several windows)
  intentionally show no global menu.
- The bar rendering was photographed for the Clock only; the other
  applications were checked by reading the trees they publish.
