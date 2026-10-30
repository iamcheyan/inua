"""The soft drawings of writing and notes: ONLYOFFICE, WPS Office, Notion,
Standard Notes, Zettlr, Typora, Mark Text, Xournal++, Rnote, Apostrophe,
Planner. The same objects as drawings/apps_t2_writing.py, about half the
detail, no text."""

from lib import bar, soft, soft_shadow, tile, two

BRASS = ("#E2B45E", "#B88433")
STEEL = ("#AEB4BB", "#8D949C")
PAPER = ("#FFFFFF", "#ECE8DF")
CREAM = ("#FBF6EA", "#EDE5D3")


def _pts(pts):
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"


def _slab(ic, cx, cy, hw, hh, t, top, side):
    L, T, R, B = (cx - hw, cy), (cx, cy - hh), (cx + hw, cy), (cx, cy + hh)
    ic.path(_pts([L, B, (B[0], B[1] + t), (L[0], L[1] + t)]), fill=side[0])
    ic.path(_pts([B, R, (R[0], R[1] + t), (B[0], B[1] + t)]), fill=side[1])
    ic.path(_pts([L, T, R, B]), fill=two(ic, *top))


@soft("onlyoffice")
def onlyoffice(ic):
    tile(ic, "#4A5058", "#20242A")
    soft_shadow(ic, 128, 210, 100, 14)
    cx, hw, hh, t = 128, 88, 44, 14
    _slab(ic, cx, 160, hw, hh, t, ("#FF7A5C", "#E8503E"), ("#C23A2C", "#8E2618"))
    _slab(ic, cx, 130, hw, hh, t, ("#B4D95A", "#8CBA34"), ("#7AA428", "#526F1A"))
    _slab(ic, cx, 100, hw, hh, t, ("#7FD6F4", "#45B2E2"), ("#3B9FD0", "#22709A"))
    with ic.g(transform=f"matrix(0.88 -0.44 0.88 0.44 {cx - hw} 100)"):
        ic.rect(14, 10, 70, 76, rx=5, fill="#FFFFFF")
        ic.rect(14, 10, 70, 16, rx=5, fill="#E2483A")
        ic.rect(14, 20, 70, 6, fill="#E2483A")
        for i, w in enumerate((44, 56, 50, 36)):
            bar(ic, 22, 36 + i * 11, w, 6, fill="#9AA1A9")


def _doc(ic, colour):
    ic.rect(0, 0, 92, 122, rx=7, fill=two(ic, *PAPER))
    ic.path("M7 0H85a7 7 0 0 1 7 7V26H0V7a7 7 0 0 1 7-7z", fill=colour)
    for i, w in enumerate((70, 58, 72, 50, 64)):
        bar(ic, 10, 38 + i * 13, w, 6, fill="#C9CDD3")


@soft("wps-office")
def wps(ic):
    tile(ic, "#2D3E66", "#121C3A")
    soft_shadow(ic, 128, 214, 96, 12)
    with ic.g(transform="translate(54 66) rotate(-12 46 140)"):
        _doc(ic, "#E8672A")
    with ic.g(transform="translate(116 66) rotate(12 46 140)"):
        _doc(ic, "#1E9E5A")
    with ic.g(transform="translate(82 46)"):
        _doc(ic, "#2B6CDB")
    bx, by = 112, 118
    ic.rect(bx, by, 72, 72, rx=20, fill=two(ic, "#FF5A4E", "#CC2420"))
    ic.path(f"M{bx + 15} {by + 22}L{bx + 26} {by + 52}L{bx + 36} {by + 32}L{bx + 46} {by + 52}L{bx + 57} {by + 22}",
            fill="none", stroke="#fff", stroke_width=10, stroke_linecap="round", stroke_linejoin="round")
    ic.rect(bx + 26, by - 14, 20, 26, rx=5, fill=two(ic, *STEEL))
    ic.rect(bx + 30, by - 10, 12, 6, rx=3, fill="#4A5058")


def _notion_n(ic, x, y, s, stroke):
    k = s / 100
    ic.path(f"M{x + 14 * k} {y}H{x + 90 * k}a10 10 0 0 1 {10 * k} {10 * k}V{y + 90 * k}a10 10 0 0 1 "
            f"{-10 * k} {10 * k}H{x + 18 * k}a10 10 0 0 1 {-8 * k} {-4 * k}L{x + 2 * k} {y + 82 * k}"
            f"a10 10 0 0 1 {-2 * k} {-6 * k}V{y + 12 * k}a10 10 0 0 1 {14 * k} {-12 * k}z",
            fill="#FFFFFF", stroke=stroke, stroke_width=9 * k, stroke_linejoin="round")
    n = [(26, 30), (46, 30), (70, 66), (70, 40), (64, 38), (64, 30), (86, 30), (86, 38), (80, 40), (80, 88),
         (70, 88), (40, 44), (40, 76), (46, 78), (46, 86), (24, 86), (24, 78), (30, 76), (30, 40), (26, 38)]
    ic.path(_pts([(x + px * k, y + py * k) for px, py in n]), fill=stroke)


@soft("notion")
def notion(ic):
    tile(ic, "#77746E", "#34322E")
    soft_shadow(ic, 134, 210, 98, 13)
    fx0, fx1, fy0, fy1, dx, dy = 52, 168, 86, 202, 38, -32
    ic.path(_pts([(fx1, fy0), (fx1 + dx, fy0 + dy), (fx1 + dx, fy1 + dy), (fx1, fy1)]), fill="#C9C5BC")
    ic.path(_pts([(fx1, fy1 - 40), (fx1 + dx, fy1 - 40 + dy), (fx1 + dx, fy1 + dy), (fx1, fy1)]), fill="#1C1C1E")
    ic.path(_pts([(fx0, fy0), (fx0 + dx, fy0 + dy), (fx1 + dx, fy0 + dy), (fx1, fy0)]), fill="#FFFFFF")
    ic.path("M96 76L176 58", stroke="#2A2A2E", stroke_width=9, stroke_linecap="round")
    ic.rect(fx0, fy0, fx1 - fx0, fy1 - fy0, fill=two(ic, "#FBFAF7", "#E4E1DA"))
    ic.rect(fx0, fy1 - 40, fx1 - fx0, 40, fill="#1E1E20")
    _notion_n(ic, 76, 100, 70, "#111111")


SN = "#086DD6"


@soft("standard-notes")
def standard_notes(ic):
    tile(ic, "#3D5878", "#1A2A40")
    soft_shadow(ic, 126, 214, 90, 12)
    with ic.g(transform="rotate(-4 128 128)"):
        ic.rect(52, 34, 148, 182, rx=8, fill="#B08A5A")
        for y, c in ((70, "#3A93F0"), (106, SN), (142, "#0752A6")):
            ic.rect(182, y, 26, 28, rx=7, fill=c)
        ic.rect(54, 46, 140, 164, rx=5, fill=two(ic, *PAPER))
        bar(ic, 64, 70, 84, 10, fill="#1B2B40")
        for i, w in enumerate((100, 86, 70)):
            bar(ic, 64, 94 + i * 16, w, 7, fill="#7F93AE")
        ic.rect(144, 152, 34, 34, rx=10, fill=SN, transform="rotate(-10 161 169)")
        for j, w in enumerate((20, 14, 20)):
            bar(ic, 151, 159 + j * 7, w, 4, fill="#fff", transform="rotate(-10 161 169)")
        ic.rect(50, 30, 152, 26, rx=6, fill=two(ic, "#3A93F0", "#0658B0"))
        bar(ic, 82, 39, 88, 7, fill="#fff", opacity=0.9)


@soft("zettlr")
def zettlr(ic):
    tile(ic, "#3A5160", "#17242E")
    soft_shadow(ic, 128, 214, 98, 12)
    ic.rect(58, 80, 140, 40, rx=4, fill="#0E6446")
    cards = [(54, 72, "#1CB27E"), (72, 156, "#E25A47"), (90, 100, "#3A93F0")]
    for i, (y, tx, tc) in enumerate(cards):
        x0 = 52 + i * 3
        w = 152 - i * 6
        ic.path(f"M{tx} {y + 2}V{y - 10}a6 6 0 0 1 6-6h{30}a6 6 0 0 1 6 6V{y + 2}z", fill=tc)
        ic.rect(x0, y, w, 90, rx=5, fill="#E8E0CE" if i < 2 else "#FBF6EA")
    bar(ic, 66, 102, 56, 6, fill="#A49E91")
    ic.path("M36 120H220L214 204a10 10 0 0 1-10 9H52a10 10 0 0 1-10-9z", fill=two(ic, "#34C68E", "#12885E"))
    ic.rect(90, 138, 76, 34, rx=5, fill=two(ic, *BRASS))
    ic.rect(96, 144, 64, 22, rx=3, fill="#FFFDF7")
    bar(ic, 104, 152, 48, 6, fill="#1F3A30")
    ic.path("M108 182h40v8a8 8 0 0 1-8 8h-24a8 8 0 0 1-8-8z", fill=two(ic, *BRASS))


@soft("typora")
def typora(ic):
    tile(ic, "#6E4B36", "#33200F")
    soft_shadow(ic, 128, 214, 84, 11)
    with ic.g(transform="rotate(-5 128 80)"):
        ic.rect(48, 22, 160, 110, rx=6, fill=two(ic, *CREAM))
        bar(ic, 60, 34, 64, 10, fill="#2A2622")
        bar(ic, 60, 54, 96, 7, fill="#8C8880")
        bar(ic, 60, 68, 80, 7, fill="#8C8880")
    cx, cy, rx, ry, h = 128, 116, 78, 46, 26
    ic.rect(cx - 9, cy + 20, 18, 66, fill="#8D949C")
    ic.rect(cx - 50, 194, 100, 14, rx=7, fill="#2C2F33")
    ic.path(f"M{cx - rx - 6} {cy}V{cy + h}A{rx + 6} {ry + 4} 0 0 0 {cx + rx + 6} {cy + h}V{cy}z",
            fill="#8D949C")
    ic.ellipse(cx, cy, rx + 6, ry + 4, fill=two(ic, "#D4D9DE", "#9AA1A9"))
    ic.ellipse(cx, cy, rx, ry, fill=two(ic, "#2E2E34", "#141416"))
    with ic.g(transform=f"translate({cx} {cy}) scale(1 {ry / rx:.3f})"):
        ic.path("M-30 -42H30V-20H22L18 -28H8V36L18 40V46H-18V40L-8 36V-28H-18L-22 -20H-30z", fill="#F7F5EF",
                stroke="#F7F5EF", stroke_width=3, stroke_linejoin="round")


def _md_mark(ic, x, y, w, h, colour, sw):
    ic.rect(x, y, w, h, rx=h * 0.2, fill="none", stroke=colour, stroke_width=sw)
    p = w / 10
    ic.path(f"M{x + p * 1.4} {y + h * 0.76}V{y + h * 0.26}L{x + p * 2.9} {y + h * 0.5}L{x + p * 4.4} {y + h * 0.26}"
            f"V{y + h * 0.76}", fill="none", stroke=colour, stroke_width=sw * 1.3, stroke_linejoin="round",
            stroke_linecap="round")
    ic.line(x + p * 7.2, y + h * 0.24, x + p * 7.2, y + h * 0.56, stroke=colour, stroke_width=sw * 1.3,
            stroke_linecap="round")
    ic.path(f"M{x + p * 5.8} {y + h * 0.5}H{x + p * 8.6}L{x + p * 7.2} {y + h * 0.8}z", fill=colour,
            stroke=colour, stroke_width=sw * 0.6, stroke_linejoin="round")


@soft("marktext")
def marktext(ic):
    tile(ic, "#4D4F8E", "#22244F")
    soft_shadow(ic, 120, 214, 98, 12)
    ink = "#1F3C88"
    with ic.g(transform="rotate(-6 110 120)"):
        ic.rect(36, 30, 140, 180, rx=7, fill=two(ic, *PAPER))
        bar(ic, 48, 46, 76, 10, fill="#24292F")
        for i, w in enumerate((60, 68, 56)):
            bar(ic, 48, 70 + i * 15, w, 7, fill="#8C939C")
        ic.rect(48, 114, 5, 18, rx=2.5, fill="#B0B7C0")
        bar(ic, 60, 120, 44, 7, fill="#B0B7C0")
        with ic.g(transform="rotate(-8 92 172)", opacity=0.85):
            _md_mark(ic, 56, 150, 74, 42, ink, 5)
    sx = 190
    ic.rect(sx - 34, 182, 68, 10, rx=3, fill="#1B1B1E")
    ic.rect(sx - 36, 150, 72, 34, rx=7, fill=two(ic, "#D9A06A", "#A86A36"))
    ic.path(f"M{sx - 10} 150V112h20v38z", fill="#9C6634")
    ic.ellipse(sx, 98, 25, 21, fill=two(ic, "#E0A870", "#A86A36"))


def _stylus(ic, x, y, deg, length, body, band, tip="#1E2024"):
    with ic.g(transform=f"translate({x} {y}) rotate({deg})"):
        ic.path("M0 0L16 -6V6z", fill=tip)
        ic.rect(16, -7, length - 16, 14, rx=7, fill=body)
        ic.rect(length - 46, -7, 9, 14, fill=band)


@soft("xournalpp")
def xournalpp(ic):
    tile(ic, "#7E3A4A", "#3A1520")
    soft_shadow(ic, 128, 214, 96, 12)
    ic.rect(38, 38, 180, 176, rx=10, fill=two(ic, "#2B4A7E", "#18304E"))
    ic.rect(40, 40, 172, 168, rx=6, fill=two(ic, *PAPER))
    for i in range(6):
        ic.line(40, 82 + i * 22, 212, 82 + i * 22, stroke="#6E9BD6", stroke_opacity=0.4, stroke_width=2)
    ic.line(66, 46, 66, 208, stroke="#E25A47", stroke_opacity=0.6, stroke_width=2.5)
    bar(ic, 74, 62, 96, 9, fill="#1F3C88")
    bar(ic, 74, 86, 60, 8, fill="#1F3C88", opacity=0.75)
    ic.line(80, 168, 160, 168, stroke="#2A2C30", stroke_width=3, stroke_linecap="round")
    ic.line(120, 110, 120, 192, stroke="#2A2C30", stroke_width=3, stroke_linecap="round")
    ic.path("M92 116Q120 216 148 116", fill="none", stroke="#E25A47", stroke_width=5, stroke_linecap="round")
    for i in range(8):
        x = 56 + i * 21
        ic.path(f"M{x - 1} 48C{x - 4} 40 {x - 2} 32 {x + 4} 32", fill="none", stroke="#C3C8CE",
                stroke_width=4.5, stroke_linecap="round")
    _stylus(ic, 150, 140, -38, 112, two(ic, "#5A626E", "#2A2E34"), "#E8672A")


@soft("rnote")
def rnote(ic):
    tile(ic, "#2F6E7C", "#123640")
    soft_shadow(ic, 128, 210, 104, 13)
    ic.rect(24, 52, 208, 154, rx=22, fill=two(ic, "#3A3D42", "#1E2024"))
    ic.rect(36, 64, 184, 130, rx=10, fill="#FBFAF6")
    ic.rect(86, 70, 84, 16, rx=8, fill="#E2E6EC")
    for i, c in enumerate(("#1C71D8", "#E66100", "#2EC27E", "#3D3846")):
        ic.circle(97 + i * 15, 78, 5, fill=c)
    ic.path("M54 150C60 112 104 104 112 132S82 176 104 168S150 116 168 132", fill="none", stroke="#1C71D8",
            stroke_width=7, stroke_linecap="round", stroke_linejoin="round")
    ic.path("M56 178Q78 164 100 178T144 178", fill="none", stroke="#E66100", stroke_width=5.5,
            stroke_linecap="round")
    ic.rect(156, 96, 40, 28, rx=6, fill="#A8E6C6", transform="rotate(8 176 110)")
    _stylus(ic, 168, 132, -54, 104, two(ic, "#F4F5F7", "#BFC4CB"), "#1C71D8", tip="#3D3846")


INK = "#2B1F66"


@soft("apostrophe")
def apostrophe(ic):
    tile(ic, "#5B3F86", "#2A1A4C")
    soft_shadow(ic, 128, 214, 98, 12)
    with ic.g(transform="rotate(5 128 150)"):
        ic.rect(34, 96, 168, 118, rx=7, fill=two(ic, *CREAM))
        bar(ic, 48, 112, 70, 9, fill="#2A2622")
        for i, w in enumerate((104, 96, 64)):
            bar(ic, 48, 136 + i * 20, w, 8, fill=INK, opacity=0.8)
    drop = "M150 140c11 0 17 8 15 19c-2 12-12 22-24 26c-2 1-3-1-1-2c7-5 11-10 11-15c-7 0-12-5-12-12c0-9 5-16 11-16z"
    ic.path(drop, transform="translate(-14 12) translate(152 162) scale(1.3) translate(-152 -162)",
            fill=two(ic, "#4A3AA0", "#1E1450"))
    with ic.g(transform="translate(144 140) rotate(-56) scale(0.66)"):
        ic.path("M0 0L30 -10Q36 0 30 10z", fill=two(ic, *BRASS))
        ic.rect(30, -9, 26, 18, rx=4, fill="#1E1E22")
        body = two(ic, "#8A66CC", "#4A2C84")
        ic.rect(56, -12, 108, 24, rx=6, fill=body)
        ic.rect(162, -13, 5, 26, fill="#E2B45E")
        ic.rect(166, -13, 54, 26, rx=12, fill=body)
        ic.rect(176, -19, 42, 7, rx=3.5, fill="#E2B45E")


@soft("planner")
def planner(ic):
    tile(ic, "#B07A2A", "#5E3A0C")
    soft_shadow(ic, 128, 214, 104, 12)
    ic.rect(22, 44, 212, 166, rx=14, fill=two(ic, "#3E5E94", "#22406E"))
    ic.path("M38 54H124V202H38a6 6 0 0 1-6-6V60a6 6 0 0 1 6-6z", fill=two(ic, *CREAM))
    ic.path("M132 54H218a6 6 0 0 1 6 6V196a6 6 0 0 1-6 6H132z", fill=two(ic, *CREAM))
    ic.rect(40, 64, 30, 28, rx=6, fill="#C8372D")
    bar(ic, 78, 68, 36, 7, fill="#2A2622")
    bar(ic, 78, 82, 26, 6, fill="#A49E91")
    for i in range(4):
        ic.line(40, 112 + i * 22, 118, 112 + i * 22, stroke="#C9BFA8", stroke_width=2)
    ic.rect(54, 116, 58, 20, rx=5, fill="#3E5E94", opacity=0.25)
    bar(ic, 62, 122, 36, 7, fill="#1C3460")
    bar(ic, 150, 66, 44, 9, fill="#2A2622")
    for i, done in enumerate((True, True, False, False)):
        y = 98 + i * 24
        ic.rect(148, y - 8, 15, 15, rx=4, fill="#fff", stroke="#4E4A44", stroke_width=2.2)
        bar(ic, 170, y - 3, 38 - (i % 2) * 8, 7, fill="#B0A898" if done else "#2A2622")
        if done:
            ic.path(f"M151 {y - 2}l4 5 10-13", fill="none", stroke="#2E8B57", stroke_width=4,
                    stroke_linecap="round", stroke_linejoin="round")
    for y in (74, 104, 152, 182):
        ic.ellipse(128, y, 14, 5.5, fill="none", stroke="#BFC5CC", stroke_width=4.5)
    ic.path("M96 190V222l6-6 6 6V190z", fill="#C8372D")
