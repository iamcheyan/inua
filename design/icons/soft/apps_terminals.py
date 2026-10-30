"""The soft drawings of the terminals: Alacritty, kitty, GNOME Terminal,
Konsole, WezTerm, Ghostty, foot, XTerm, btop++, htop. The objects of
drawings/apps_terminals.py with about half the detail, no text."""

from lib import bar, soft, soft_shadow, tile, two


def _prompt(ic, x, y, s, color, width=None):
    """A chevron and a cursor block, its top left at (x, y), s tall."""
    ic.path(f"M{x} {y} L{x + s * 0.5:.1f} {y + s * 0.5:.1f} L{x} {y + s}", fill="none", stroke=color,
            stroke_width=width or s * 0.24, stroke_linecap="round", stroke_linejoin="round")
    ic.rect(x + s * 0.9, y + s * 0.6, s * 0.8, s * 0.4, rx=s * 0.1, fill=color)


@soft("Alacritty")
def alacritty(ic):
    tile(ic, "#4A3A33", "#1E1613")
    soft_shadow(ic, 128, 214, 102, 12)
    ic.path("M78 116V46c0-8 6-14 14-14h82c8 0 12 6 12 12v72z", fill=two(ic, "#FFFDF7", "#F1EADB"))
    bar(ic, 90, 48, 60, fill="#3C3732")
    bar(ic, 90, 62, 36, fill="#D9732A")
    bar(ic, 90, 76, 64, fill="#A49E91")
    bar(ic, 90, 90, 30, fill="#D9732A")
    ic.rect(42, 104, 172, 50, rx=16, fill=two(ic, "#FBB052", "#D9701E"))
    ic.rect(60, 106, 136, 16, rx=8, fill="#1E1C1A")
    for x in (52, 204):
        ic.circle(x, 114, 9, fill="#2E2C2A")
    ic.rect(102, 128, 52, 20, rx=6, fill="#2B201A")
    ic.path("M128 131 L139 145 H133.5 L128 138 L122.5 145 H117 Z", fill="#FBC062")
    ic.path("M44 150h168a10 10 0 0 1 10 8l8 38a8 8 0 0 1-8 10H34a8 8 0 0 1-8-10l8-38a10 10 0 0 1 10-8z",
            fill=two(ic, "#E8802E", "#A04A16"))
    for y, x0, n in ((166, 56, 8), (182, 48, 9)):
        for i in range(n):
            ic.circle(x0 + i * 20, y, 7, fill="#F1E8D6")
    ic.rect(92, 194, 72, 8, rx=4, fill="#F1E8D6")


@soft("kitty")
def kitty(ic):
    tile(ic, "#B5803F", "#6A4119")
    soft_shadow(ic, 128, 210, 84, 12)
    glaze = two(ic, "#8A9099", "#4A4F57")
    ic.path("M168 202c22 2 40-6 40-26 0-14-10-20-18-16", fill="none", stroke="#4A4F57", stroke_width=14,
            stroke_linecap="round")
    ic.path("M128 104c-34 0-58 44-58 88 0 10 8 15 20 15h76c12 0 20-5 20-15 0-44-24-88-58-88z", fill=glaze)
    ic.path("M128 128c-14 0-24 22-24 46 0 14 8 24 24 24s24-10 24-24c0-24-10-46-24-46z", fill="#F4EFE6")
    for x in (112, 144):
        ic.ellipse(x, 201, 14, 8, fill="#FBF7EF")
    for s in (1, -1):
        ic.path(f"M{128 - s * 44} 84 L{128 - s * 44} 36 Q{128 - s * 43} 30 {128 - s * 38} 34 L{128 - s * 12} 56 Z",
                fill="#7D838C", stroke="#7D838C", stroke_width=4, stroke_linejoin="round")
        ic.path(f"M{128 - s * 37} 72 L{128 - s * 37} 46 L{128 - s * 21} 60 Z", fill="#E7A6A0")
    ic.ellipse(128, 90, 50, 40, fill=two(ic, "#8A9099", "#6A7078"))
    for x in (108, 148):
        ic.ellipse(x, 90, 10, 11, fill="#C9E26A")
        ic.ellipse(x, 90, 3.5, 9, fill="#14161A")
    ic.path("M121 104h14l-7 7z", fill="#E58C86", stroke="#E58C86", stroke_linejoin="round", stroke_width=3)
    ic.path("M92 124c22 10 50 10 72 0", fill="none", stroke="#C8372D", stroke_width=8, stroke_linecap="round")
    ic.circle(128, 142, 11, fill=two(ic, "#E2B45E", "#B88433"))


@soft("org.gnome.Terminal")
def gnome_terminal(ic):
    tile(ic, "#56606B", "#262C33")
    soft_shadow(ic, 128, 214, 86, 11)
    ic.path("M104 176h48l8 26h-64z", fill="#A9A59D")
    ic.rect(76, 196, 104, 14, rx=7, fill=two(ic, "#E4E1DA", "#B4B0A8"))
    ic.rect(30, 32, 196, 154, rx=24, fill=two(ic, "#F2F0EB", "#C9C5BD"))
    ic.rect(44, 44, 168, 116, rx=16, fill="#A9A59D")
    ic.rect(50, 50, 156, 104, rx=16, fill=two(ic, "#2A3138", "#12161A"))
    bar(ic, 66, 66, 40, 8, fill="#E6EBEF")
    bar(ic, 66, 82, 70, 8, fill="#8FB8E8")
    bar(ic, 66, 98, 52, 8, fill="#8FB8E8")
    _prompt(ic, 68, 116, 22, "#F2F5F7")
    for x in (176, 192):
        ic.circle(x, 172, 5, fill="#A9A59D")
    ic.circle(208, 172, 3.5, fill="#5FD38A")


@soft("konsole")
def konsole(ic):
    tile(ic, "#2F6EA8", "#143A62")
    soft_shadow(ic, 128, 212, 108, 11)
    ic.rect(46, 36, 164, 124, rx=12, fill=two(ic, "#3A4148", "#1A1E22"))
    sx, sy, sw, sh = 54, 46, 148, 106
    ic.rect(sx, sy, sw, sh, rx=4, fill="#232629")
    ic.path(f"M{sx} {sy + 16}V{sy + 4}a4 4 0 0 1 4-4h{sw - 8}a4 4 0 0 1 4 4v12z", fill="#31363B")
    ic.rect(sx + 3, sy + 3, 50, 13, rx=3, fill="#232629")
    ic.rect(sx + 3, sy + 3, 50, 3, rx=1.5, fill="#3DAEE9")
    bar(ic, sx + 10, sy + 26, 64, 7, fill="#FCFCFC")
    bar(ic, sx + 10, sy + 40, 50, 7, fill="#3DAEE9")
    bar(ic, sx + 10, sy + 54, 44, 7, fill="#1CDC9A")
    _prompt(ic, sx + 10, sy + 70, 18, "#FCFCFC")
    ic.path("M46 158h164l22 38a6 6 0 0 1-5 9H29a6 6 0 0 1-5-9z", fill=two(ic, "#DDE3EA", "#A3ADB8"))
    for y, x0, x1, n in ((164, 42, 214, 10), (174, 36, 220, 10), (184, 30, 226, 11)):
        w = (x1 - x0) / n
        for i in range(n):
            ic.rect(x0 + i * w + 2, y, w - 4, 7, rx=2, fill="#2B3036")
    ic.rect(104, 194, 48, 8, rx=3, fill="#8C97A3")


@soft("wezterm")
def wezterm(ic):
    tile(ic, "#4C3672", "#20143A")
    soft_shadow(ic, 128, 214, 100, 11)
    ic.rect(54, 34, 142, 152, rx=8, fill=two(ic, "#8A72B8", "#9A5A9E"), opacity=0.65)
    ic.rect(55, 35, 140, 150, rx=7, fill="none", stroke="#E9DDFF", stroke_width=2.5, opacity=0.8)
    ic.path("M68 50l6 20 6-14 6 14 6-20", fill="none", stroke="#fff", stroke_width=5,
            stroke_linecap="round", stroke_linejoin="round")
    bar(ic, 104, 56, 40, 7, fill="#fff", opacity=0.7)
    bar(ic, 68, 88, 84, 7, fill="#F2E9FF")
    bar(ic, 68, 102, 56, 7, fill="#FF8BD1")
    bar(ic, 68, 116, 70, 7, fill="#B9A2FF")
    bar(ic, 68, 130, 60, 7, fill="#7FE3D8")
    _prompt(ic, 68, 146, 16, "#FF8BD1")
    ic.rect(34, 182, 188, 26, rx=10, fill=two(ic, "#A06E46", "#5A3418"))
    ic.rect(52, 182, 152, 5, rx=2.5, fill="#FFB3E2")


def _ghost(cx, top, w, bottom, n=4, dip=9):
    l, r = cx - w / 2, cx + w / 2
    seg = w / n
    d = f"M{l} {bottom}V{top + w / 2}A{w / 2} {w / 2} 0 0 1 {r} {top + w / 2}V{bottom}"
    for i in range(n):
        x1 = r - i * seg
        d += (f"Q{x1 - seg / 4:.1f} {bottom + dip} {x1 - seg / 2:.1f} {bottom}"
              f"Q{x1 - seg * 3 / 4:.1f} {bottom - dip * 0.6:.1f} {x1 - seg:.1f} {bottom}")
    return d + "Z"


@soft("ghostty")
def ghostty(ic):
    tile(ic, "#3D5BC4", "#16245E")
    soft_shadow(ic, 128, 214, 70, 10)
    ic.path(_ghost(128, 30, 132, 178), fill=two(ic, "#FFFFFF", "#C9D3F0"))
    ic.path("M92 88 L112 104 L92 120", fill="none", stroke="#1B2453", stroke_width=12, stroke_linecap="round",
            stroke_linejoin="round")
    ic.rect(128, 109, 34, 12, rx=4, fill="#1B2453")
    ic.ellipse(104, 142, 11, 6, fill="#F4A3B4", opacity=0.6)
    ic.ellipse(160, 142, 11, 6, fill="#F4A3B4", opacity=0.6)


_SOLE = "M118 194c-18 0-24-16-22-36 2-18-6-30-4-50 2-18 16-26 32-24 20 2 32 12 32 30 0 20-10 30-12 48-2 20-8 32-26 32z"
_TOES = ((106, 68, 12, 14), (128, 61, 8.5, 10), (143, 65, 7.5, 9), (155, 74, 7, 8))


@soft("foot")
def foot(ic):
    tile(ic, "#3F7A72", "#183C38")
    soft_shadow(ic, 128, 214, 96, 12)
    with ic.g(transform="rotate(-5 128 124)"):
        ic.rect(42, 28, 172, 184, rx=20, fill=two(ic, "#F6F1E6", "#DCD3C1"))
        with ic.g(transform="rotate(8 128 124) translate(-2 4)"):
            ic.path(_SOLE, fill="#7A6E58")
            for x, y, rx, ry in _TOES:
                ic.ellipse(x, y, rx, ry, fill="#7A6E58")
        ic.circle(186, 186, 14, fill="none", stroke="#A04A34", stroke_width=3)
        ic.path("M180 180l6 6-6 6", fill="none", stroke="#A04A34", stroke_width=3.5, stroke_linecap="round",
                stroke_linejoin="round")
        ic.rect(188, 189, 7, 3.5, rx=1.5, fill="#A04A34")


@soft("xterm")
def xterm(ic):
    tile(ic, "#4F4A3E", "#211E17")
    soft_shadow(ic, 128, 214, 104, 11)
    cream = two(ic, "#F1EAD6", "#C9BFA4")
    ic.rect(42, 30, 172, 134, rx=14, fill=cream)
    ic.rect(54, 44, 148, 104, rx=12, fill="#3A352C")
    ic.rect(60, 50, 136, 92, rx=14, fill=two(ic, "#2A1C08", "#0D0803"))
    a = "#FFB43C"
    for y, w in ((62, 56), (76, 44), (90, 64), (104, 76)):
        bar(ic, 72, y, w, 7, fill=a, opacity=0.7)
    _prompt(ic, 72, 118, 14, "#FFC75E")
    ic.rect(56, 151, 26, 10, rx=3, fill="#3A352C")
    ic.path("M62 153l4 3-4 3h3.5l2.5-2 2.5 2h3.5l-4-3 4-3h-3.5l-2.5 2-2.5-2z", fill="#E8DFC8")
    ic.circle(200, 156, 3, fill=a)
    ic.path("M44 172h168l14 28a6 6 0 0 1-5 8H35a6 6 0 0 1-5-8z", fill=cream)
    for r, (y, x0, x1, n) in enumerate(((177, 50, 206, 10), (188, 44, 212, 11))):
        w = (x1 - x0) / n
        for i in range(n):
            ic.rect(x0 + i * w + 1.5, y, w - 3, 8, rx=2, fill="#5A5446")
    ic.rect(92, 199, 72, 6, rx=3, fill="#5A5446")


@soft("btop")
def btop(ic):
    tile(ic, "#34474C", "#121C1F")
    soft_shadow(ic, 128, 214, 104, 11)
    ic.path("M54 62V46a12 12 0 0 1 12-12h124a12 12 0 0 1 12 12v16", fill="none", stroke="#2A2D31", stroke_width=9,
            stroke_linecap="round")
    for x in (46, 194):
        ic.rect(x, 192, 16, 14, rx=4, fill="#1E2023")
    ic.rect(28, 54, 200, 144, rx=16, fill=two(ic, "#E3E7EB", "#A9B1B9"))
    ic.rect(38, 64, 144, 124, rx=8, fill="#24272B")
    sx, sy, sw = 43, 69, 134
    ic.rect(sx, sy, sw, 114, rx=5, fill="#0A0B0C")
    ic.rect(sx + 4, sy + 5, sw - 8, 62, rx=6, fill="none", stroke="#556D59", stroke_width=2)
    hs = (8, 14, 22, 30, 20, 34, 42, 30, 24, 36, 44, 32, 20, 26)
    gx0, gy0, step = sx + 9, sy + 62, (sw - 18) / (len(hs) - 1)
    d = f"M{gx0} {gy0}" + "".join(f"L{gx0 + i * step:.1f} {gy0 - h}" for i, h in enumerate(hs)) + \
        f"L{gx0 + (len(hs) - 1) * step:.1f} {gy0}Z"
    ic.path(d, fill=ic.lin([(0, "#F2E266"), (1, "#50F095")], 0, sy + 16, 0, gy0, units="userSpaceOnUse"),
            stroke_linejoin="round")
    by = sy + 74
    for i, (w, c) in enumerate(((36, "#4897D4"), (24, "#50F095"), (42, "#9D4DD0"))):
        bar(ic, sx + 6, by + i * 12, 50, 6, fill="#232528")
        bar(ic, sx + 6, by + i * 12, w, 6, fill=c)
    for i, w in enumerate((44, 38, 30)):
        bar(ic, sx + 70, by + i * 12, w, 6, fill="#C7C7C7")
    for y, a in ((88, 40), (128, -30)):
        ic.circle(204, y, 13, fill="#2A2D31")
        ic.circle(204, y, 9, fill=two(ic, "#AEB4BB", "#8D949C"))
        ic.rect(202.5, y - 9, 3, 7, rx=1.5, fill="#E33B2E", transform=f"rotate({a} 204 {y})")
    ic.rect(193, 156, 22, 12, rx=4, fill="#2A2D31")
    ic.rect(203, 158, 10, 8, rx=3, fill="#50F095")


@soft("htop")
def htop(ic):
    tile(ic, "#2F5E43", "#122A1C")
    soft_shadow(ic, 128, 210, 112, 11)
    for x0 in (24, 206):
        ic.rect(x0, 56, 26, 140, rx=6, fill=two(ic, "#AEB4BB", "#8D949C"))
        ic.rect(x0 + 8, 84, 10, 84, rx=5, fill="#2A2D31")
    ic.rect(48, 50, 160, 152, rx=8, fill=two(ic, "#2E3338", "#14171A"))
    sx, sy, sw, sh = 55, 58, 146, 124
    ic.rect(sx, sy, sw, sh, rx=5, fill="#0C1014")
    meters = (((28, "#3FCF5A"), (10, "#E24B42")), ((16, "#3FCF5A"), (8, "#E24B42"), (6, "#4F84E8")),
              ((40, "#3FCF5A"), (12, "#4F84E8"), (24, "#E8C547")), ((6, "#E24B42"),))
    for i, parts in enumerate(meters):
        y = sy + 8 + i * 10
        bar(ic, sx + 6, y, 12, 6, fill="#59C9E4")
        bar(ic, sx + 22, y, 96, 6, fill="#1E2428")
        x = sx + 22
        for k, (w, c) in enumerate(parts):
            ic.rect(x, y, w, 6, rx=3 if len(parts) == 1 or k == 0 else 0, fill=c)
            x += w
        bar(ic, sx + 124, y, 16, 6, fill="#9AA4AD")
    hy = sy + 50
    ic.rect(sx, hy, sw, 10, fill="#3FA34D")
    for i in range(4):
        y = hy + 14 + i * 11
        if i == 1:
            ic.rect(sx, y - 2, sw, 10, fill="#4FB7D6")
        bar(ic, sx + 6, y, 24, 6, fill="#0C1014" if i == 1 else "#D9DEE2")
        bar(ic, sx + 40, y, 50 - i * 6, 6, fill="#0C1014" if i == 1 else "#D9DEE2")
    fy = sy + sh - 11
    for k, x in enumerate((sx + 4, sx + 40, sx + 76, sx + 112)):
        ic.rect(x, fy, 30, 8, rx=2, fill="#4FB7D6")
    bar(ic, 60, 190, 26, 6, fill="#3FCF5A")
    ic.circle(196, 192, 3.5, fill="#3FCF5A")
