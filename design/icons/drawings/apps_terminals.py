"""The theme's terminals: Alacritty, kitty, GNOME Terminal (the generic
terminal), Konsole, WezTerm, Ghostty, foot, XTerm, btop++, htop
(docs/feat/object-icons.md, Part 2). Each a different object, so none
looks like inua's own Term (a black-glass screen on a stand)."""

from lib import (brass, glare, graphite, icon, paper, shadow, small, steel, tile, wood)


def _scan(ic, x, y, w, h, rx, opacity=0.45):
    """A CRT's scanlines over a screen."""
    p = ic.define('<pattern id="{id}" width="4" height="3" patternUnits="userSpaceOnUse">'
                  '<rect width="4" height="1" fill="#000" opacity=".35"/></pattern>', "p")
    ic.rect(x, y, w, h, rx=rx, fill=f"url(#{p})", opacity=opacity)


def _prompt(ic, x, y, size, color, width=None):
    """A prompt drawn as shapes: a chevron and a cursor block, its top
    left at (x, y), size px tall."""
    s = size
    ic.path(f"M{x} {y} L{x + s * 0.5:.1f} {y + s * 0.5:.1f} L{x} {y + s}", fill="none", stroke=color,
            stroke_width=width or s * 0.19, stroke_linecap="round", stroke_linejoin="round")
    ic.rect(x + s * 0.95, y + s * 0.02, s * 0.58, s * 0.96, fill=color)


# --- Alacritty: a teletype in orange enamel, a config printed on its paper ----

@icon("Alacritty", kind="app", names=["Alacritty", "com.alacritty.Alacritty"], title="Alacritty")
def alacritty(ic):
    tile(ic, "#4A3A33", "#1E1613")
    shadow(ic, 128, 214, 102, 12)
    # the paper, out of the platen and curling over at the top
    ic.path("M78 116V44c0-8 4-12 12-12h86c6 0 10 4 10 10v74z", fill=paper(ic, "cream"))
    ic.path("M90 32h86c6 0 10 4 10 10v2c0-5-4-7-9-7H90c-6 0-10 3-12 7 0-8 4-12 12-12z", fill="#fff", opacity=0.8)
    ic.line(86, 33, 86, 116, stroke="#000", stroke_opacity=0.05, stroke_width=1.2)
    ink = dict(font="mono-semibold", fill="#3C3732")
    ic.text("$ cat alacritty.toml", 88, 54, 7.4, **ink)
    ic.text("[window]", 88, 66, 7.4, font="mono-semibold", fill="#B9581A")
    ic.text("opacity = 0.96", 88, 77, 7.4, **ink)
    ic.text("[font]", 88, 89, 7.4, font="mono-semibold", fill="#B9581A")
    ic.text("size = 11.5", 88, 100, 7.4, **ink)
    # the upper housing and its platen
    orange = ic.lin([(0, "#FBC062"), (0.45, "#F08A2A"), (1, "#B9561A")], 0, 0, 0.3, 1)
    ic.rect(42, 104, 172, 50, rx=14, fill=orange)
    ic.rect(42.75, 104.75, 170.5, 48.5, rx=13.25, fill="none", stroke="#FFE2B0", stroke_opacity=0.5, stroke_width=1.5)
    ic.rect(60, 106, 136, 15, rx=7.5, fill=ic.lin([(0, "#55504B"), (0.5, "#1B1917"), (1, "#0B0A09")]))
    ic.rect(66, 108, 124, 2, rx=1, fill="#fff", opacity=0.22)
    for x in (52, 204):
        ic.circle(x, 113.5, 8, fill=graphite(ic))
        ic.circle(x - 1.5, 112, 3, fill="#fff", opacity=0.18)
    # the mark: an A, its two legs and a step, pressed into a dark plate
    ic.rect(104, 128, 48, 19, rx=4, fill="#2B201A")
    ic.rect(104, 128, 48, 1.2, rx=0.6, fill="#000", opacity=0.4)
    ic.path("M128 131 L138.5 144 H133.5 L128 137 L122.5 144 H117.5 Z", fill="#FBC062")
    ic.path("M128 139.5 L131 144 H125 Z", fill="#F08A2A")
    # the keyboard deck
    deck = ic.lin([(0, "#E0782A"), (1, "#8E3F12")])
    ic.path("M44 150h168a8 8 0 0 1 8 7l8 40a8 8 0 0 1-8 9H36a8 8 0 0 1-8-9l8-40a8 8 0 0 1 8-7z", fill=deck)
    ic.path("M46 151.5h164", stroke="#FFD49A", stroke_opacity=0.5, stroke_width=1.5)
    rows = ((163, 11, 56), (177, 11, 52), (191, 11, 60))
    for y, n, x0 in rows:
        for i in range(n):
            x = x0 + i * 14 + (y - 163) * 0.0
            ic.circle(x + 0.6, y + 1.6, 5.4, fill="#4A1E06", opacity=0.6)
            ic.circle(x, y, 5.4, fill=ic.rad([(0, "#FFFBF0"), (1, "#D9CDB6")], cx=0.38, cy=0.32, r=0.7) if i == 0 else "#F1E8D6")
            ic.circle(x, y, 5.4, fill="none", stroke="#3A2A1C", stroke_opacity=0.35, stroke_width=0.8)
    ic.rect(98, 199, 60, 6, rx=3, fill="#F1E8D6")


@small("Alacritty")
def alacritty16(ic):
    tile(ic, "#4A3A33", "#1E1613")
    ic.rect(4.5, 2, 7, 6, rx=0.5, fill="#F7F2E6")
    ic.rect(2.5, 7, 11, 3.5, rx=1, fill="#F08A2A")
    ic.rect(4, 7.2, 8, 1.2, rx=0.6, fill="#1B1917")
    ic.path("M2.2 10.5h11.6l.8 3h-13.2z", fill="#B9561A")
    for x in (4, 6, 8, 10, 12):
        ic.circle(x, 12, 0.6, fill="#F1E8D6")


# --- kitty: a grey ceramic cat, sitting, a tag on its collar -----------------

@icon("kitty", kind="app", names=["kitty", "appimagekit-kitty"], title="kitty")
def kitty(ic):
    tile(ic, "#B5803F", "#6A4119")
    shadow(ic, 128, 210, 84, 12)
    glaze = ic.rad([(0, "#9EA4AD"), (0.55, "#646A73"), (1, "#30343A")], cx=0.32, cy=0.25, r=0.85)
    # tail, curled round the front
    ic.path("M168 202c22 2 40-6 40-26 0-14-10-20-18-16", fill="none", stroke="#3B3F46", stroke_width=13,
            stroke_linecap="round")
    ic.path("M168 202c22 2 40-6 40-26 0-14-10-20-18-16", fill="none", stroke="#7A8089", stroke_width=5,
            stroke_linecap="round", opacity=0.5, transform="translate(-2 -2)")
    # body
    ic.path("M128 104c-34 0-58 44-58 88 0 10 8 15 20 15h76c12 0 20-5 20-15 0-44-24-88-58-88z", fill=glaze)
    ic.path("M128 128c-14 0-24 22-24 46 0 14 8 24 24 24s24-10 24-24c0-24-10-46-24-46z",
            fill=ic.lin([(0, "#FBF7EF"), (1, "#D9D2C4")]))
    # front paws
    for x in (112, 144):
        ic.ellipse(x, 201, 13, 7.5, fill=ic.lin([(0, "#FFFDF8"), (1, "#D5CDBE")]))
        ic.path(f"M{x - 4} 198v5M{x + 4} 198v5", stroke="#9E978A", stroke_width=1.2, stroke_linecap="round")
    # head and ears
    for s in (1, -1):
        ic.path(f"M{128 - s * 44} 84 L{128 - s * 44} 34 Q{128 - s * 43} 30 {128 - s * 39} 33 L{128 - s * 12} 56 Z",
                fill="#555B63" if s == -1 else "#7D838C")
        ic.path(f"M{128 - s * 37} 72 L{128 - s * 37} 44 L{128 - s * 19} 60 Z", fill="#E7A6A0", opacity=0.85)
    ic.ellipse(128, 90, 50, 40, fill=glaze)
    ic.ellipse(110, 68, 22, 10, fill="#fff", opacity=0.2, transform="rotate(-18 110 68)")
    # eyes, nose, mouth, whiskers
    for x in (108, 148):
        ic.ellipse(x, 90, 10, 11, fill=ic.rad([(0, "#E9F59A"), (1, "#8DB43A")], cx=0.45, cy=0.4, r=0.7))
        ic.ellipse(x, 90, 2.6, 9, fill="#14161A")
        ic.circle(x - 3.5, 85.5, 2.3, fill="#fff", opacity=0.9)
    ic.path("M122 104h12l-6 6z", fill="#E58C86", stroke="#E58C86", stroke_linejoin="round", stroke_width=2)
    ic.path("M128 110v4c-2 4-7 4-9 1M128 114c2 4 7 4 9 1", fill="none", stroke="#2A2D32", stroke_width=1.6,
            stroke_linecap="round")
    for s in (1, -1):
        for dy, ang in ((-2, -4), (3, 4)):
            ic.line(128 - s * 26, 106 + dy, 128 - s * 58, 102 + dy + ang * 2, stroke="#F4F1EA", stroke_width=1.2,
                    stroke_linecap="round", opacity=0.85)
    # collar and its brass tag, a prompt stamped on it
    ic.path("M92 124c22 10 50 10 72 0", fill="none", stroke="#C8372D", stroke_width=6, stroke_linecap="round")
    ic.path("M93 122.5c22 9.5 49 9.5 70 0", fill="none", stroke="#F08C80", stroke_width=1.2, opacity=0.6)
    ic.circle(128, 141, 10, fill=brass(ic))
    ic.circle(128, 141, 10, fill="none", stroke="#6B4A14", stroke_opacity=0.5)
    ic.path("M122.5 136.5l4.5 4.5-4.5 4.5", fill="none", stroke="#5A3E10", stroke_width=1.8, stroke_linecap="round",
            stroke_linejoin="round")
    ic.rect(128.5, 143.5, 6, 2, fill="#5A3E10")


@small("kitty")
def kitty16(ic):
    tile(ic, "#B5803F", "#6A4119")
    ic.path("M8 7c-2.6 0-4 3.2-4 6.5h8C12 10.2 10.6 7 8 7z", fill="#5E646C")
    ic.path("M3.9 6V1.4L7 3.6zM12.1 6V1.4L9 3.6z", fill="#7A8089")
    ic.ellipse(8, 6, 4.2, 3.4, fill="#7A8089")
    ic.circle(6.4, 6, 0.9, fill="#D8EC7A")
    ic.circle(9.6, 6, 0.9, fill="#D8EC7A")
    ic.rect(6.5, 12, 3, 1.5, rx=0.6, fill="#F4EFE4")


# --- GNOME Terminal: the generic terminal, a pale grey CRT monitor ------------

@icon("org.gnome.Terminal", kind="app", title="GNOME Terminal", names=[
    "org.gnome.Terminal", "gnome-terminal", "utilities-terminal", "terminal", "Terminal", "terminal-tango",
    "Etermutilities-terminal", "bash", "deepin-terminal", "gksu-debian", "gnome-eterm", "gnome-term", "hotwire",
    "lxterminal", "openterm", "org.xfce.terminal", "org.xfce.terminalemulator", "roxterm", "terminology", "tilda",
    "xconsole", "xfce-terminal"])
def gnome_terminal(ic):
    tile(ic, "#56606B", "#262C33")
    shadow(ic, 128, 214, 86, 11)
    # stand
    ic.path("M104 176h48l8 26h-64z", fill=ic.lin([(0, "#BDB9B1"), (1, "#8E8A82")]))
    ic.rect(76, 198, 104, 12, rx=6, fill=ic.lin([(0, "#E4E1DA"), (1, "#A9A59D")]))
    ic.rect(80, 198.5, 96, 1.5, rx=0.75, fill="#fff", opacity=0.6)
    # case
    ic.rect(30, 32, 196, 154, rx=20, fill=ic.lin([(0, "#F2F0EB"), (0.5, "#DCD9D2"), (1, "#B4B0A8")], 0, 0, 0.4, 1))
    ic.rect(30.75, 32.75, 194.5, 152.5, rx=19.25, fill="none", stroke="#fff", stroke_opacity=0.7, stroke_width=1.5)
    # the screen's well and the tube's glass, a little domed
    ic.rect(44, 44, 168, 116, rx=14, fill=ic.lin([(0, "#8F8B84"), (1, "#C9C5BD")]))
    tube = ic.rad([(0, "#2C343C"), (0.7, "#161B20"), (1, "#0A0D10")], cx=0.4, cy=0.4, r=0.75)
    ic.rect(50, 50, 156, 104, rx=16, fill=tube)
    t = dict(font="mono-semibold", fill="#E6EBEF", opacity=0.82)
    ic.text("~$ ls", 64, 72, 10, **t)
    ic.text("Documents  Music", 64, 86, 10, font="mono", fill="#8FB8E8", opacity=0.9)
    ic.text("Pictures   notes.txt", 64, 100, 10, font="mono", fill="#8FB8E8", opacity=0.9)
    _prompt(ic, 66, 116, 18, "#F2F5F7")
    _scan(ic, 50, 50, 156, 104, 16, 0.35)
    ic.path("M50 66a16 16 0 0 1 16-16h84L76 154H66a16 16 0 0 1-16-16z", fill=glare(ic))
    # chin: a vent, the power lamp and two knobs
    for i in range(6):
        ic.rect(48 + i * 7, 168, 4, 9, rx=2, fill="#8E8A82", opacity=0.55)
    ic.circle(176, 172.5, 4.2, fill="#B4B0A8")
    ic.circle(190, 172.5, 4.2, fill="#B4B0A8")
    ic.circle(175, 171.5, 1.4, fill="#fff", opacity=0.7)
    ic.circle(189, 171.5, 1.4, fill="#fff", opacity=0.7)
    ic.circle(206, 172.5, 2.4, fill="#5FD38A")
    ic.circle(206, 172.5, 4.5, fill="#5FD38A", opacity=0.2)


@small("org.gnome.Terminal")
def gnome_terminal16(ic):
    tile(ic, "#56606B", "#262C33")
    ic.rect(6, 12, 4, 1.8, fill="#A9A59D")
    ic.rect(1.8, 2.2, 12.4, 10.2, rx=1.6, fill="#E4E1DA")
    ic.rect(3, 3.4, 10, 7.2, rx=1.2, fill="#161B20")
    ic.path("M4.6 5.2 L6.5 7 L4.6 8.8", fill="none", stroke="#F2F5F7", stroke_width=1.1, stroke_linecap="round",
            stroke_linejoin="round")
    ic.rect(7.4, 8, 3, 1, fill="#F2F5F7")


# --- Konsole: an open laptop in KDE blue, Konsole's tabs on its screen ---------

@icon("konsole", kind="app", names=["konsole", "org.kde.konsole", "org.kde.qmlkonsole"], title="Konsole")
def konsole(ic):
    tile(ic, "#2F6EA8", "#143A62")
    shadow(ic, 128, 212, 108, 11)
    # lid
    ic.rect(46, 36, 164, 122, rx=10, fill=ic.lin([(0, "#3A4148"), (1, "#1A1E22")]))
    ic.rect(46.75, 36.75, 162.5, 120.5, rx=9.25, fill="none", stroke="#fff", stroke_opacity=0.14, stroke_width=1.5)
    ic.circle(128, 42, 1.6, fill="#0A0C0E")
    sx, sy, sw, sh = 54, 47, 148, 103
    ic.rect(sx, sy, sw, sh, fill="#232629")
    # Konsole's window: a tab bar, then the terminal
    ic.rect(sx, sy, sw, 13, fill="#31363B")
    ic.rect(sx + 2, sy + 2, 46, 11, rx=1.5, fill="#232629")
    ic.rect(sx + 2, sy + 2, 46, 1.6, fill="#3DAEE9")
    ic.text("~ : zsh", sx + 8, sy + 10.5, 6.6, font="sans-semibold", fill="#FCFCFC")
    ic.text("build", sx + 58, sy + 10.5, 6.6, font="sans-semibold", fill="#A1A9B1")
    t = dict(font="mono-semibold", fill="#FCFCFC", opacity=0.9)
    ic.text("~ $ make -j8", sx + 7, sy + 28, 8, **t)
    ic.text("[ 97%] Linking", sx + 7, sy + 40, 8, font="mono", fill="#3DAEE9")
    ic.text("[100%] Built", sx + 7, sy + 52, 8, font="mono", fill="#1CDC9A")
    ic.text("~ $ ./build/app &", sx + 7, sy + 64, 8, **t)
    ic.text("~ $", sx + 7, sy + 80, 8, **t)
    ic.rect(sx + 28, sy + 73, 5.5, 9, fill="#FCFCFC")
    ic.path(f"M{sx} {sy}h70L{sx + 22} {sy + sh}h-22z", fill=glare(ic, 0.8))
    # deck, in perspective: wider at the front
    ic.path("M46 158h164l22 38a6 6 0 0 1-5 9H29a6 6 0 0 1-5-9z",
            fill=ic.lin([(0, "#DDE3EA"), (0.6, "#B7C0CA"), (1, "#8994A1")]))
    ic.path("M46 158.8h164", stroke="#fff", stroke_width=1.6, opacity=0.8)
    ic.path("M24.5 199h207", stroke="#5F6A77", stroke_width=1.5, opacity=0.6)
    key = "#2B3036"
    rows = ((162, 42, 214, 12), (169, 38, 218, 12), (176, 34, 222, 12), (183, 30, 226, 11))
    for y, x0, x1, n in rows:
        w = (x1 - x0) / n
        for i in range(n):
            ic.rect(x0 + i * w + 1.5, y, w - 3, 5, rx=1, fill=key)
    ic.rect(104, 190.5, 48, 8, rx=2, fill="#A7B1BC", stroke="#7D8895", stroke_width=0.8)
    # the badge: a prompt on blue enamel
    ic.rect(196, 189, 18, 9, rx=2.5, fill="#1D99F3")
    ic.path("M200 191l3 2.5-3 2.5", fill="none", stroke="#fff", stroke_width=1.2, stroke_linecap="round",
            stroke_linejoin="round")
    ic.rect(204.5, 195, 5, 1.4, fill="#fff")


@small("konsole")
def konsole16(ic):
    tile(ic, "#2F6EA8", "#143A62")
    ic.rect(3, 2.5, 10, 7.8, rx=0.8, fill="#2A2F35")
    ic.rect(3.8, 3.3, 8.4, 1.3, fill="#3DAEE9")
    ic.path("M4.8 6 L6.3 7.2 L4.8 8.4", fill="none", stroke="#FCFCFC", stroke_width=0.9, stroke_linecap="round",
            stroke_linejoin="round")
    ic.path("M3 10.3h10l1.6 2.8H1.4z", fill="#C9D1DA")


# --- WezTerm: a slab of clear glass in a walnut base, its text glowing ---------

@icon("wezterm", kind="app", names=["wezterm"], title="WezTerm")
def wezterm(ic):
    tile(ic, "#4C3672", "#20143A")
    shadow(ic, 128, 214, 100, 11)
    # glass, lit from the base like an edge-lit sign: its edge to the right,
    # then its face, a glow rising from the slot
    ic.path("M196 38l6 4v140h-6z", fill=ic.lin([(0, "#fff", 0.35), (1, "#FF8BD1", 0.5)]))
    ic.rect(54, 34, 142, 148, rx=5, fill=ic.lin([(0, "#fff", 0.2), (1, "#C9B8FF", 0.08)], 0, 0, 1, 1))
    ic.rect(54, 120, 142, 62, fill=ic.lin([(0, "#FF8BD1", 0), (1, "#FF8BD1", 0.3)]))
    ic.rect(54.75, 34.75, 140.5, 146.5, rx=4.25, fill="none", stroke=ic.lin([(0, "#fff", 0.7), (1, "#FFB3E2", 0.8)]),
            stroke_width=1.5)
    # the mark, a W, cut into the glass
    ic.path("M66 48l5 18 5-12 5 12 5-18", fill="none", stroke="#fff", stroke_opacity=0.85, stroke_width=3.2,
            stroke_linecap="round", stroke_linejoin="round")
    ic.text("WezTerm", 94, 63, 9, font="sans-semibold", fill="#fff", opacity=0.75)
    # the text, glowing in the glass
    ic.text("$ wezterm ssh devbox", 66, 92, 8, font="mono-semibold", fill="#F2E9FF", opacity=0.9)
    ic.text("> cargo build", 66, 106, 8, font="mono-semibold", fill="#FF8BD1")
    ic.text("Compiling term 0.9", 66, 120, 8, font="mono", fill="#B9A2FF")
    ic.text("Finished release", 66, 134, 8, font="mono", fill="#7FE3D8")
    ic.text("$", 66, 152, 8, font="mono-semibold", fill="#F2E9FF")
    ic.rect(74, 145, 5, 8.5, fill="#FF8BD1")
    ic.path("M56 38h70L72 180H56z", fill=glare(ic, 1.1))
    # walnut base, the slab set in its slot
    ic.path("M40 182h176l6 6v14a6 6 0 0 1-6 6H40a6 6 0 0 1-6-6v-14z", fill=wood(ic, "#9A6A44", "#4E2E16"))
    ic.path("M40 182h176l6 6H34z", fill="#C49067")
    ic.rect(52, 182, 152, 4, rx=1, fill="#2A170A", opacity=0.8)
    ic.rect(56, 182.5, 144, 1.6, rx=0.8, fill="#FFB3E2", opacity=0.9)
    ic.line(36, 189.5, 220, 189.5, stroke="#fff", stroke_opacity=0.15)
    for y in (195, 201):
        ic.path(f"M38 {y}c40-2 90 2 140-1s30 1 42 0", fill="none", stroke="#2A170A", stroke_opacity=0.25)


@small("wezterm")
def wezterm16(ic):
    tile(ic, "#4C3672", "#20143A")
    ic.rect(3.5, 2, 9, 10.5, rx=0.6, fill="#D8CCFF", opacity=0.3)
    ic.rect(3.5, 2, 9, 10.5, rx=0.6, fill="none", stroke="#fff", stroke_opacity=0.7, stroke_width=0.6)
    ic.rect(5, 5, 6, 1, fill="#FF8BD1")
    ic.rect(5, 7.5, 4, 1, fill="#B9A2FF")
    ic.rect(2, 12, 12, 2.5, rx=0.6, fill="#8A5A36")


# --- Ghostty: a little porcelain ghost, a prompt for a face --------------------

def _ghost(cx, top, w, bottom, n=4, dip=9):
    """A ghost's outline: a dome, straight sides, n scallops at the hem."""
    l, r = cx - w / 2, cx + w / 2
    seg = w / n
    d = f"M{l} {bottom}V{top + w / 2}A{w / 2} {w / 2} 0 0 1 {r} {top + w / 2}V{bottom}"
    for i in range(n):
        x1 = r - i * seg
        d += f"Q{x1 - seg / 4:.1f} {bottom + dip} {x1 - seg / 2:.1f} {bottom}Q{x1 - seg * 3 / 4:.1f} {bottom - dip * 0.6:.1f} {x1 - seg:.1f} {bottom}"
    return d + "Z"


@icon("ghostty", kind="app", names=["ghostty", "com.mitchellh.ghostty"], title="Ghostty")
def ghostty(ic):
    tile(ic, "#3D5BC4", "#16245E")
    shadow(ic, 128, 216, 64, 9, 0.8)
    d = _ghost(128, 30, 132, 178)
    ic.path(d, fill="#0E1A4A", opacity=0.35, transform="translate(5 6)")
    ic.path(d, fill=ic.rad([(0, "#FFFFFF"), (0.6, "#E9EEFB"), (1, "#AEBBE3")], cx=0.35, cy=0.25, r=0.85))
    ic.path(d, fill=ic.lin([(0.45, "#3D5BC4", 0), (1, "#3D5BC4", 0.28)], 0, 0, 1, 0.3))
    ic.path(d, fill="none", stroke="#fff", stroke_opacity=0.6, stroke_width=1.5)
    # the face: a chevron and a cursor, in dark glaze
    ic.path("M92 88 L112 104 L92 120", fill="none", stroke="#1B2453", stroke_width=10, stroke_linecap="round",
            stroke_linejoin="round")
    ic.rect(130, 110, 32, 10, rx=3, fill="#1B2453")
    ic.ellipse(104, 140, 10, 5, fill="#F4A3B4", opacity=0.45)
    ic.ellipse(160, 140, 10, 5, fill="#F4A3B4", opacity=0.45)
    ic.ellipse(98, 58, 20, 11, fill="#fff", opacity=0.75, transform="rotate(-30 98 58)")


@small("ghostty")
def ghostty16(ic):
    tile(ic, "#3D5BC4", "#16245E")
    ic.path(_ghost(8, 2, 9, 12.5, 3, 1.4), fill="#F2F5FD")
    ic.path("M5.5 5.8 L7 7 L5.5 8.2", fill="none", stroke="#1B2453", stroke_width=1, stroke_linecap="round",
            stroke_linejoin="round")
    ic.rect(8.3, 7.6, 2.4, 0.9, fill="#1B2453")


# --- foot: a footprint pressed into a plaster tablet, a prompt stamped by it ----

_SOLE = ("M118 194c-18 0-24-16-22-36 2-18-6-30-4-50 2-18 16-26 32-24 20 2 32 12 32 30 0 20-10 30-12 48-2 20-8 32-26 32z")
_TOES = ((106, 68, 11, 13), (128, 62, 7.5, 9), (143, 66, 6.5, 8), (155, 74, 6, 7), (164, 86, 5.5, 6.5))


def _foot(ic, dx=0, dy=0, **kw):
    t = f"translate({dx} {dy})"
    ic.path(_SOLE, transform=t, **kw)
    for x, y, rx, ry in _TOES:
        ic.ellipse(x + dx, y + dy, rx, ry, **kw)


@icon("foot", kind="app", names=["foot"], title="foot")
def foot(ic):
    tile(ic, "#3F7A72", "#183C38")
    shadow(ic, 128, 214, 96, 12)
    with ic.g(transform="rotate(-5 128 124)"):
        ic.rect(42, 34, 172, 182, rx=16, fill="#A79B85")
        ic.rect(42, 28, 172, 182, rx=16, fill=ic.lin([(0, "#F6F1E6"), (1, "#D8CFBD")], 0, 0, 1, 1))
        ic.rect(42.75, 28.75, 170.5, 180.5, rx=15.25, fill="none", stroke="#fff", stroke_opacity=0.8, stroke_width=1.5)
        with ic.g(transform="rotate(8 128 124) translate(-2 4)"):
            _foot(ic, 1.6, 1.6, fill="#FFFFFF", opacity=0.9)
            _foot(ic, fill="#6E624E")
            shape = _SOLE
            inner = f'<path d="{shape}"/>' + "".join(
                f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}"/>' for x, y, rx, ry in _TOES)
            with ic.g(clip_path=ic.clip(inner)):
                _foot(ic, 2.6, 3.2, fill=ic.lin([(0, "#BDB29C"), (1, "#D6CCB8")]))
        # the stamp: a prompt in a ring, pressed in by the heel
        ic.circle(186, 186, 13, fill="none", stroke="#8F3F2C", stroke_width=1.8, opacity=0.8)
        ic.path("M179.5 180.5l5.5 5.5-5.5 5.5", fill="none", stroke="#8F3F2C", stroke_width=2.2, stroke_linecap="round",
                stroke_linejoin="round", opacity=0.85)
        ic.rect(187, 189.5, 7, 2.4, fill="#8F3F2C", opacity=0.85)


@small("foot")
def foot16(ic):
    tile(ic, "#3F7A72", "#183C38")
    ic.rect(2.5, 1.8, 11, 12.4, rx=1.4, fill="#EFE8DA")
    ic.path("M7.6 13c-1.4 0-1.8-1.2-1.7-2.6.1-1.4-.5-2.2-.3-3.6.2-1.3 1.1-1.9 2.3-1.8 1.4.1 2.2.9 2.2 2.1 0 1.4-.7 2.1-.8 3.4-.2 1.5-.6 2.5-1.7 2.5z",
            fill="#6E624E")
    ic.circle(6.4, 4.2, 0.95, fill="#6E624E")
    ic.circle(8, 3.6, 0.7, fill="#6E624E")
    ic.circle(9.2, 4, 0.6, fill="#6E624E")
    ic.circle(10.1, 4.8, 0.55, fill="#6E624E")


# --- XTerm: a cream video terminal and its keyboard, amber on the tube ---------

@icon("xterm", kind="app", title="XTerm", names=[
    "xterm", "utilities-x-terminal", "xterm-color", "xterm-color_48x48", "gnome-xterm", "mini.xterm", "urxvt",
    "urxvt_48x48"])
def xterm(ic):
    tile(ic, "#4F4A3E", "#211E17")
    shadow(ic, 128, 214, 104, 11)
    cream = ic.lin([(0, "#F1EAD6"), (0.5, "#DCD2B8"), (1, "#ADA38A")], 0, 0, 0.4, 1)
    # the case, deeper at the back: a lighter top band
    ic.path("M52 30h152a10 10 0 0 1 10 10v116a8 8 0 0 1-8 8H50a8 8 0 0 1-8-8V40a10 10 0 0 1 10-10z", fill=cream)
    ic.path("M52 30h152a10 10 0 0 1 10 10v2H42v-2a10 10 0 0 1 10-10z", fill="#fff", opacity=0.45)
    ic.rect(54, 44, 148, 104, rx=10, fill="#3A352C")
    ic.rect(60, 50, 136, 92, rx=12, fill=ic.rad([(0, "#2E1E08"), (1, "#0D0803")], cx=0.4, cy=0.4, r=0.8))
    a = dict(font="mono-semibold", fill="#FFB43C")
    ic.text("$ uname -sr", 70, 68, 9, **a, opacity=0.75)
    ic.text("Linux 6.8.0", 70, 81, 9, **a, opacity=0.75)
    ic.text("$ echo $TERM", 70, 94, 9, **a, opacity=0.75)
    ic.text("xterm-256color", 70, 107, 9, **a, opacity=0.75)
    ic.text("$", 70, 124, 9, **a)
    ic.rect(79, 116, 6.5, 10, fill="#FFC75E")
    _scan(ic, 60, 50, 136, 92, 12, 0.5)
    ic.path("M60 62a12 12 0 0 1 12-12h70L84 142H72a12 12 0 0 1-12-12z", fill=glare(ic))
    # the X, its thick and thin strokes, a badge on the chin
    ic.rect(56, 151, 24, 9, rx=2, fill="#3A352C")
    ic.path("M61 152.5l4 3-4 3h3l2.5-1.9 2.5 1.9h3.4l-4.4-3 4.4-3h-3.2l-2.3 1.7-2.3-1.7z", fill="#E8DFC8")
    ic.text("VIDEO TERMINAL", 86, 158.5, 5.6, font="mono-semibold", spacing=0.8, fill="#7A715C")
    ic.circle(200, 155.5, 2.2, fill="#FFB43C")
    # the keyboard, a low wedge
    ic.path("M44 172h168l14 28a6 6 0 0 1-5 8H35a6 6 0 0 1-5-8z", fill=cream)
    ic.path("M44 172.8h168", stroke="#fff", stroke_width=1.6, opacity=0.6)
    for r, (y, x0, x1) in enumerate(((176, 48, 208), (184, 44, 212), (192, 40, 216))):
        n = 14 if r < 2 else 15
        w = (x1 - x0) / n
        for i in range(n):
            ic.rect(x0 + i * w + 1, y, w - 2, 6, rx=1.2, fill="#7B735F" if i in (0, n - 1) else "#5A5446")
            ic.rect(x0 + i * w + 1.6, y + 0.4, w - 3.2, 1, rx=0.5, fill="#fff", opacity=0.25)
    ic.rect(92, 200, 72, 5, rx=1.5, fill="#5A5446")


@small("xterm")
def xterm16(ic):
    tile(ic, "#4F4A3E", "#211E17")
    ic.rect(2.5, 1.8, 11, 9, rx=1, fill="#E4DBC3")
    ic.rect(3.6, 2.9, 8.8, 6.4, rx=0.8, fill="#1E1406")
    ic.rect(4.6, 4.2, 4.5, 0.9, fill="#FFB43C")
    ic.rect(4.6, 6.4, 2, 1.4, fill="#FFB43C")
    ic.path("M2.6 11.6h10.8l1.2 2.6H1.4z", fill="#D3C9AE")


# --- btop++: a bench instrument, btop's cpu graph on its screen ---------------

@icon("btop", kind="app", names=["btop"], title="btop++")
def btop(ic):
    tile(ic, "#34474C", "#121C1F")
    shadow(ic, 128, 214, 104, 11)
    # carrying bail
    ic.path("M54 62V44a10 10 0 0 1 10-10h128a10 10 0 0 1 10 10v18", fill="none", stroke="#2A2D31", stroke_width=7,
            stroke_linecap="round")
    ic.path("M56 58V44a8 8 0 0 1 8-8h128a8 8 0 0 1 8 8v14", fill="none", stroke="#fff", stroke_opacity=0.18,
            stroke_width=1.5)
    # case and feet
    for x in (46, 194):
        ic.rect(x, 194, 16, 12, rx=3, fill="#1E2023")
    ic.rect(28, 54, 200, 144, rx=12, fill=ic.lin([(0, "#E3E7EB"), (0.5, "#C2C9CF"), (1, "#8C959E")], 0, 0, 0.4, 1))
    ic.rect(28.75, 54.75, 198.5, 142.5, rx=11.25, fill="none", stroke="#fff", stroke_opacity=0.7, stroke_width=1.5)
    for y in (58, 194):
        ic.rect(36, y - 2, 184, 2, fill="#000", opacity=0.08)
    # screen
    ic.rect(38, 64, 144, 124, rx=6, fill="#24272B")
    sx, sy, sw, sh = 43, 69, 134, 114
    ic.rect(sx, sy, sw, sh, rx=3, fill="#0A0B0C")
    # the cpu box: its graph, green to yellow to red, in braille dots
    ic.rect(sx + 3, sy + 4, sw - 6, 64, rx=4, fill="none", stroke="#556D59", stroke_width=1.2)
    ic.rect(sx + 9, sy + 1, 18, 6, fill="#0A0B0C")
    ic.text("cpu", sx + 11, sy + 6.6, 7, font="mono-semibold", fill="#EE7F7F")
    heat = ic.lin([(0, "#50F095"), (0.55, "#F2E266"), (1, "#FA1E1E")], 0, sy + 64, 0, sy + 14, units="userSpaceOnUse")
    hs = (8, 14, 10, 22, 30, 18, 26, 40, 34, 46, 30, 24, 36, 28, 20, 32, 44, 38, 26, 16, 22, 30, 34, 24, 18, 28)
    gx0, gy0, step = sx + 7, sy + 64, (sw - 14) / (len(hs) - 1)
    pts = [(gx0 + i * step, gy0 - h) for i, h in enumerate(hs)]
    d = f"M{gx0} {gy0}" + "".join(f"L{x:.1f} {y}" for x, y in pts) + f"L{gx0 + (len(hs) - 1) * step:.1f} {gy0}Z"
    ic.path(d, fill=heat)
    dots = ic.define('<pattern id="{id}" width="3" height="3" patternUnits="userSpaceOnUse">'
                     '<path d="M0 0h3v1H1v2H0z" fill="#0A0B0C"/></pattern>', "p")
    ic.rect(gx0 - 1, sy + 12, sw - 12, 53, fill=f"url(#{dots})")
    # mem and proc boxes
    by = sy + 72
    ic.rect(sx + 3, by, 58, 38, rx=4, fill="none", stroke="#6C6C4B", stroke_width=1.2)
    ic.rect(sx + 9, by - 3, 18, 6, fill="#0A0B0C")
    ic.text("mem", sx + 11, by + 2.6, 7, font="mono-semibold", fill="#EE7F7F")
    for i, (w, c1, c2) in enumerate(((34, "#4897D4", "#B5E685"), (22, "#50F095", "#F2E266"), (40, "#9D4DD0", "#FFA2C9"))):
        y = by + 9 + i * 9
        ic.rect(sx + 8, y, 46, 4, fill="#232528")
        ic.rect(sx + 8, y, w, 4, fill=ic.lin([(0, c1), (1, c2)], 0, 0, 1, 0))
    ic.rect(sx + 65, by, 66, 38, rx=4, fill="none", stroke="#805252", stroke_width=1.2)
    ic.rect(sx + 71, by - 3, 22, 6, fill="#0A0B0C")
    ic.text("proc", sx + 73, by + 2.6, 7, font="mono-semibold", fill="#EE7F7F")
    for i, (name, c) in enumerate((("firefox", "#E6E6E6"), ("hyprland", "#C7C7C7"), ("btop", "#A6A6A6"))):
        ic.text(name, sx + 70, by + 13 + i * 9, 6.4, font="mono", fill=c)
        ic.rect(sx + 112, by + 9 + i * 9, 14 - i * 4, 4, fill=("#F2E266", "#50F095", "#50F095")[i])
    ic.path(f"M{sx} {sy}h60L{sx + 18} {sy + sh}H{sx}z", fill=glare(ic, 0.6))
    # knobs, a switch, and the maker's name
    for y in (88, 128):
        ic.circle(205, y + 1.5, 13, fill="#000", opacity=0.25)
        ic.circle(204, y, 13, fill=graphite(ic))
        ic.circle(204, y, 9, fill=steel(ic, horizontal=False))
        ic.rect(203, y - 9, 2, 6, rx=1, fill="#E33B2E", transform=f"rotate({40 if y == 88 else -30} 204 {y})")
    ic.rect(193, 156, 22, 10, rx=3, fill="#2A2D31")
    ic.rect(203, 157.5, 10, 7, rx=2, fill="#50F095")
    ic.text("btop++", 204, 182, 7.5, font="mono-semibold", anchor="middle", fill="#454B52")


@small("btop")
def btop16(ic):
    tile(ic, "#34474C", "#121C1F")
    ic.rect(1.5, 3, 13, 10.5, rx=1.2, fill="#C9CFD5")
    ic.rect(2.5, 4, 9, 8.5, rx=0.6, fill="#0A0B0C")
    ic.path("M3 11.5L4.5 9 6 10 7.5 6.5 9 8.5 11 5.5V11.5z", fill="#F2E266")
    ic.path("M3 11.5L4.5 9.6 6 10.5 7.5 8.6 9 9.6 11 8.4V11.5z", fill="#50F095")
    ic.circle(13, 6, 1, fill="#2A2D31")
    ic.circle(13, 9.5, 1, fill="#2A2D31")


# --- htop: a rack monitor, htop's meters and process list on it ---------------

@icon("htop", kind="app", names=["htop"], title="htop")
def htop(ic):
    tile(ic, "#2F5E43", "#122A1C")
    shadow(ic, 128, 210, 112, 11)
    # the rack unit: ears with handles, a black body between
    for x0 in (24, 206):
        ic.rect(x0, 56, 26, 140, rx=4, fill=steel(ic))
        ic.rect(x0 + 0.75, 56.75, 24.5, 138.5, rx=3.25, fill="none", stroke="#fff", stroke_opacity=0.3, stroke_width=1.5)
        cx = x0 + 13
        for y in (68, 184):
            ic.circle(cx, y, 3.6, fill="#3A3F45")
            ic.circle(cx - 0.6, y - 0.6, 1.4, fill="#fff", opacity=0.5)
        ic.rect(cx - 6, 84, 12, 6, rx=2, fill="#2A2D31")
        ic.rect(cx - 6, 162, 12, 6, rx=2, fill="#2A2D31")
        ic.rect(cx - 4, 86, 8, 80, rx=4, fill=graphite(ic))
        ic.rect(cx - 2.5, 90, 2, 72, rx=1, fill="#fff", opacity=0.2)
    ic.rect(48, 50, 160, 152, rx=6, fill=ic.lin([(0, "#3A3F45"), (0.1, "#25292D"), (1, "#121417")]))
    ic.rect(48.75, 50.75, 158.5, 150.5, rx=5.25, fill="none", stroke="#fff", stroke_opacity=0.14, stroke_width=1.5)
    sx, sy, sw, sh = 55, 58, 146, 124
    ic.rect(sx - 1, sy - 1, sw + 2, sh + 2, rx=4, fill="#060708")
    ic.rect(sx, sy, sw, sh, rx=3, fill="#0C1014")
    # meters: CPUs, memory, swap
    fs = 6.4
    m = dict(font="mono-semibold", fill="#59C9E4")
    meters = (("1", ((28, "#3FCF5A"), (10, "#E24B42"))), ("2", ((16, "#3FCF5A"), (6, "#E24B42"), (4, "#4F84E8"))),
              ("Mem", ((44, "#3FCF5A"), (10, "#4F84E8"), (26, "#E8C547"))), ("Swp", ((4, "#E24B42"),)))
    for i, (lab, parts) in enumerate(meters):
        y = sy + 12 + i * 10
        ic.text(lab, sx + 17, y, fs, anchor="end", **m)
        ic.text("[", sx + 18, y, fs, font="mono-semibold", fill="#EDEDED")
        ic.text("]", sx + 120, y, fs, font="mono-semibold", fill="#EDEDED")
        x = sx + 23
        for w, c in parts:
            n = int(w / 2)
            ic.path("".join(f"M{x + k * 2 + 0.6:.1f} {y - 5.2}v5.6" for k in range(n)), stroke=c, stroke_width=1.1)
            x += n * 2
    for i, v in enumerate(("41%", "27%", "4.1G", "12M")):
        ic.text(v, sx + sw - 3, sy + 12 + i * 10, fs, anchor="end", font="mono", fill="#9AA4AD")
    # the process list: its green header, a cyan selection
    hy = sy + 50
    ic.rect(sx, hy, sw, 9, fill="#3FA34D")
    ic.text("  PID USER    CPU% COMMAND", sx + 2, hy + 7, fs, font="mono-semibold", fill="#0C1014")
    rows = (("  812 root     4.2 Xwayland", None), (" 1337 user     3.1 firefox", "#4FB7D6"),
            (" 2048 user     0.7 htop", None), ("  401 root     0.3 systemd", None))
    for i, (row, bg) in enumerate(rows):
        y = hy + 17 + i * 9
        if bg:
            ic.rect(sx, y - 7, sw, 9, fill=bg)
        ic.text(row, sx + 2, y, fs, font="mono", fill="#0C1014" if bg else "#D9DEE2")
    # function keys
    fy = sy + sh - 4
    x = sx + 2
    for k, word in (("F1", "Help"), ("F2", "Setup"), ("F3", "Search"), ("F10", "Quit")):
        x += ic.text(k, x, fy, 6, font="mono-semibold", fill="#EDEDED")
        ic.rect(x, fy - 6, len(word) * 3.6 + 2, 8, fill="#4FB7D6")
        ic.text(word, x + 1, fy, 6, font="mono", fill="#0C1014")
        x += len(word) * 3.6 + 5
    ic.path(f"M{sx} {sy}h64L{sx + 20} {sy + sh}H{sx}z", fill=glare(ic, 0.5))
    # the maker's strip, under the screen
    ic.text("htop", 60, 196, 8, font="mono-semibold", fill="#3FCF5A", opacity=0.9)
    ic.circle(196, 192, 2.2, fill="#3FCF5A")
    ic.circle(196, 192, 4.5, fill="#3FCF5A", opacity=0.2)


@small("htop")
def htop16(ic):
    tile(ic, "#2F5E43", "#122A1C")
    ic.rect(0.8, 3, 14.4, 10, rx=0.8, fill="#AEB4BB")
    ic.rect(2.5, 2.6, 11, 10.8, rx=0.8, fill="#1E2226")
    ic.rect(3.4, 3.6, 9.2, 8.8, rx=0.4, fill="#0C1014")
    ic.rect(4, 4.5, 5, 1, fill="#3FCF5A")
    ic.rect(9, 4.5, 2, 1, fill="#E24B42")
    ic.rect(4, 6.3, 3.5, 1, fill="#3FCF5A")
    ic.rect(3.4, 8.2, 9.2, 1.2, fill="#3FA34D")
    ic.rect(3.4, 10.2, 9.2, 1, fill="#4FB7D6")
