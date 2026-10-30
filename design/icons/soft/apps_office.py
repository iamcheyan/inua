"""The soft drawings of the office batch (drawings/apps_office.py):
LibreOffice and its Writer, Calc, Impress and Draw; Zotero, calibre,
Okular, Document Viewer, Logseq, Joplin, Obsidian and Foliate. The same
objects, about half the detail, no text."""

from lib import bar, soft, soft_shadow, tile, two

# each document's colour: the folded corner's light and dark, the tile's
LO = {
    "writer": ("#6DB7F7", "#1A5FB4", "#2F65A0", "#122C4E"),
    "calc": ("#93DB6A", "#2A8A2A", "#2E7A3E", "#0F3818"),
    "impress": ("#FFAA62", "#D2521C", "#A84E28", "#52200C"),
    "draw": ("#FFDC62", "#D69808", "#9A7220", "#4A3408"),
    "start": ("#5FD24A", "#14900A", "#3A4652", "#161D24"),
}
PAPER = ("#FFFFFF", "#ECE8DF")


def _page(ic, x, y, w, h, fold, tab, fill=None):
    """A sheet, its top right corner folded over in the document's colour."""
    ic.path(f"M{x + 6} {y}h{w - fold - 6}l{fold} {fold}v{h - fold - 6}a6 6 0 0 1 -6 6h{-(w - 12)}"
            f"a6 6 0 0 1 -6 -6v{-(h - 12)}a6 6 0 0 1 6 -6z", fill=fill or two(ic, *PAPER))
    ic.path(f"M{x + w - fold} {y}v{fold - 6}a6 6 0 0 0 6 6h{fold - 6}z", fill=two(ic, LO[tab][0], LO[tab][1]))


def _lo_mark(ic, x, y, s, colour, sw):
    w, f = s * 0.78, s * 0.3
    ic.path(f"M{x} {y}h{w - f}l{f} {f}v{s - f}h{-w}z", fill="none", stroke=colour, stroke_width=sw,
            stroke_linejoin="round")
    ic.path(f"M{x + w - f} {y}v{f}h{f}z", fill=colour, stroke=colour, stroke_width=sw * 0.6, stroke_linejoin="round")


@soft("libreoffice-startcenter")
def libreoffice(ic):
    tile(ic, LO["start"][2], LO["start"][3])
    soft_shadow(ic, 128, 216, 98, 12)
    for tab, deg in (("draw", -27), ("impress", -10), ("calc", 10), ("writer", 27)):
        with ic.g(transform=f"rotate({deg} 128 230)"):
            _page(ic, 84, 50, 88, 118, 24, tab)
            for i, wl in enumerate((52, 40)):
                bar(ic, 94, 82 + i * 14, wl, 7, fill="#CFC9BD")
    _page(ic, 70, 62, 116, 152, 30, "start")
    _lo_mark(ic, 108, 96, 48, "#1A9A12", 8)
    for tab, x in (("writer", 90), ("calc", 110), ("impress", 130), ("draw", 150)):
        ic.rect(x, 176, 16, 16, rx=4, fill=LO[tab][1])


@soft("libreoffice-writer")
def writer(ic):
    tile(ic, LO["writer"][2], LO["writer"][3])
    soft_shadow(ic, 128, 216, 88, 11)
    with ic.g(transform="rotate(-6 128 130)"):
        ic.rect(58, 38, 140, 174, rx=6, fill="#EDE5D3")
    _page(ic, 56, 34, 146, 178, 34, "writer")
    bar(ic, 72, 56, 54, 12, fill="#1C3556")
    for i, w in enumerate((108, 96, 104, 80)):
        bar(ic, 72, 84 + i * 16, w, 8, fill="#B9B4AA")
    ic.path("M74 186c6-14 12-14 14-4s8 6 12-6 10 0 12 4", fill="none", stroke="#1A5FB4", stroke_width=5,
            stroke_linecap="round", stroke_linejoin="round")
    # the pen, across the page's corner
    with ic.g(transform="rotate(-34 176 178)"):
        ic.path("M120 182 l-20 -5 a2 2 0 0 0 0 10 z", fill=two(ic, "#E2B45E", "#B88433"))
        ic.rect(118, 174, 112, 16, rx=8, fill=two(ic, "#3D78C8", "#123A78"))
        ic.rect(180, 173, 8, 18, fill=two(ic, "#E2B45E", "#B88433"))


@soft("libreoffice-calc")
def calc(ic):
    tile(ic, LO["calc"][2], LO["calc"][3])
    soft_shadow(ic, 128, 216, 96, 12)
    with ic.g(transform="rotate(5 128 130)"):
        ic.rect(44, 42, 172, 164, rx=6, fill="#EDE5D3")
    _page(ic, 36, 38, 184, 170, 30, "calc")
    ic.rect(50, 52, 130, 16, rx=5, fill="#E6EDE0")
    bar(ic, 58, 57, 70, 6, fill="#7A9A70")
    # the grid: a header row, the rows and three columns
    x0, y0, rh = 50, 80, 22
    ic.rect(x0, y0, 156, 16, rx=4, fill="#CFE8C2")
    for r in range(5):
        y = y0 + 22 + r * rh
        bar(ic, 58, y + 6, 30 if r % 2 else 38, 8, fill="#8C887F")
        bar(ic, 112, y + 6, 32, 8, fill="#B9B4AA")
        bar(ic, 164, y + 6, 32, 8, fill="#B9B4AA")
    for x in (102, 154):
        ic.rect(x, y0, 3, 22 + 5 * rh, fill="#D6DDCF")
    # the selected sum
    ty = y0 + 22 + 4 * rh
    ic.rect(152, ty - 2, 56, rh, rx=4, fill="#E3F2DA", stroke="#1E7A1E", stroke_width=4)
    bar(ic, 164, ty + 5, 32, 8, fill="#1E7A1E")
    ic.rect(203, ty + rh - 7, 10, 10, rx=2, fill="#1E7A1E", stroke="#fff", stroke_width=2)


@soft("libreoffice-impress")
def impress(ic):
    tile(ic, LO["impress"][2], LO["impress"][3])
    soft_shadow(ic, 128, 218, 92, 10)
    leg = two(ic, "#A06A3C", "#5E3A18")
    ic.path("M122 30h12l4 186h-20z", fill=leg)
    ic.path("M96 140h14l-30 78h-14z", fill=leg)
    ic.path("M146 140h14l30 78h-14z", fill=leg)
    ic.circle(128, 34, 7, fill=two(ic, "#E2B45E", "#B88433"))
    _page(ic, 30, 40, 196, 122, 28, "impress")
    bar(ic, 46, 56, 92, 14, fill="#3A1A0A")
    for i, h in enumerate((22, 34, 46, 60)):
        ic.rect(48 + i * 20, 150 - h, 15, h, rx=3, fill="#D2521C" if i == 3 else "#ECC4A8")
    for i in range(3):
        y = 92 + i * 18
        ic.rect(134, y, 9, 9, rx=2, fill="#D2521C")
        bar(ic, 150, y + 1, 54 if i != 1 else 42, 7, fill="#B9B4AA")
    # the ledge it stands on
    ic.rect(22, 158, 212, 14, rx=5, fill=two(ic, "#C99260", "#8A5A2C"))


@soft("libreoffice-draw")
def draw(ic):
    tile(ic, LO["draw"][2], LO["draw"][3])
    soft_shadow(ic, 128, 216, 94, 12)
    _page(ic, 40, 36, 176, 174, 30, "draw")
    ic.circle(96, 102, 32, fill=two(ic, "#FFE38A", "#F2B416"), stroke="#8A5F00", stroke_width=4)
    ic.path("M122 148 L158 86 L194 148 Z", fill=two(ic, "#7FB8F0", "#3584E4"), stroke="#1A4F94",
            stroke_width=4, stroke_linejoin="round")
    ic.path("M58 188 C 84 140, 124 206, 150 168 S 196 150, 204 178", fill="none", stroke="#2E2D2A",
            stroke_width=5, stroke_linecap="round")
    ic.line(150, 168, 170, 140, stroke="#1A5FB4", stroke_width=3)
    ic.circle(170, 140, 5, fill="#fff", stroke="#1A5FB4", stroke_width=3)
    for x, y in ((58, 188), (150, 168)):
        ic.rect(x - 6, y - 6, 12, 12, rx=3, fill="#1A5FB4" if x == 150 else "#fff", stroke="#1A5FB4", stroke_width=3)
    # the pencil
    with ic.g(transform="rotate(-48 176 180)"):
        ic.path("M134 176 l-22 7.5 22 7.5z", fill="#EBC795")
        ic.path("M120 180.7 l-8 2.8 8 2.8z", fill="#2A2C30")
        ic.rect(132, 176, 86, 15, rx=2, fill=two(ic, "#FFD65A", "#E09E10"))
        ic.rect(216, 176, 20, 15, rx=5, fill="#E77A8A")


@soft("zotero")
def zotero(ic):
    tile(ic, "#6E3236", "#2E1214")
    soft_shadow(ic, 128, 216, 96, 12)
    for deg, c in ((-7, "#D8D0BF"), (4, "#E6DFD0")):
        with ic.g(transform=f"rotate({deg} 128 128)"):
            ic.rect(52, 40, 152, 168, rx=6, fill=c)
    ic.rect(50, 36, 156, 172, rx=6, fill=two(ic, *PAPER))
    bar(ic, 66, 62, 82, 12, fill="#2A1A1C")
    bar(ic, 66, 80, 64, 12, fill="#2A1A1C")
    bar(ic, 66, 100, 48, 7, fill="#9A7A7C")
    for col in (66, 132):
        for i in range(4):
            bar(ic, col, 120 + i * 13, 54 if i != 3 else 36, 7, fill="#CCC6BB")
    ic.rect(66, 178, 62, 16, rx=5, fill="#F4DCDE")
    # the paper clip
    ic.path("M58 24 v32 a7 7 0 0 0 14 0 v-26 a4 4 0 0 0 -8 0 v22", fill="none", stroke=two(ic, "#AEB4BB", "#8D949C"),
            stroke_width=4, stroke_linecap="round")
    # the bookmark, its Z
    ic.path("M164 22h38v96l-19 -13 -19 13z", fill=two(ic, "#E8484F", "#B0202C"))
    ic.path("M170 52h26v7l-16 24h16v8h-28v-7l16 -24h-14z", fill="#FFF6F2")


@soft("calibre")
def calibre(ic):
    tile(ic, "#5A4636", "#241A12")
    soft_shadow(ic, 128, 218, 104, 11)
    ic.rect(26, 40, 204, 172, rx=12, fill=two(ic, "#B47A46", "#6E4420"))
    ic.rect(40, 54, 176, 142, rx=5, fill="#2E1E12")
    books = [(44, 22, 128, "#A33A30"), (66, 18, 110, "#2E4F7E"), (84, 24, 134, "#4E6A3A"),
             (108, 16, 102, "#D9B470"), (124, 22, 122, "#3A2E4E"), (146, 20, 114, "#2F6E6A"),
             (166, 22, 130, "#8E4A2A")]
    for x, w, h, c in books:
        y = 196 - h
        ic.rect(x, y, w, h, rx=3, fill=c)
        ic.rect(x, y + 12, w, 5, fill="#E8C27A", opacity=0.8)
    with ic.g(transform="rotate(16 214 196)"):
        ic.rect(194, 78, 22, 118, rx=3, fill="#B04A30")
        ic.rect(194, 90, 22, 5, fill="#E8C27A", opacity=0.8)
    ic.rect(26, 192, 204, 20, rx=6, fill=two(ic, "#C99260", "#8A5A2C"))
    ic.rect(104, 196, 48, 12, rx=4, fill=two(ic, "#E2B45E", "#B88433"))


@soft("okular")
def okular(ic):
    tile(ic, "#2E6690", "#0F2A40")
    soft_shadow(ic, 128, 216, 96, 12)
    with ic.g(transform="rotate(-5 128 128)"):
        ic.rect(46, 34, 148, 178, rx=6, fill=two(ic, *PAPER))
        ic.path("M52 34h6v178h-6a6 6 0 0 1 -6 -6v-166a6 6 0 0 1 6 -6z", fill="#3DAEE9")
        bar(ic, 64, 52, 66, 13, fill="#1C2A3A")
        bar(ic, 64, 72, 82, 7, fill="#3D5A78")
        for i in range(3):
            bar(ic, 64, 92 + i * 14, 110 if i != 2 else 60, 7, fill="#CCC9C2")
        for i in range(3):
            bar(ic, 64, 160 + i * 14, 110 if i != 2 else 76, 7, fill="#CCC9C2")
    cx, cy, r = 156, 132, 40
    with ic.g(transform=f"rotate(-45 {cx} {cy})"):
        ic.rect(cx - 7, cy + r, 14, 14, rx=3, fill=two(ic, "#AEB4BB", "#8D949C"))
        ic.rect(cx - 10, cy + r + 12, 20, 58, rx=10, fill="#1E2226")
    lens = ic.clip(f'<circle cx="{cx}" cy="{cy}" r="{r}"/>')
    with ic.g(clip_path=lens):
        ic.circle(cx, cy, r, fill="#F2F7FB")
        bar(ic, cx - 56, cy - 26, 70, 16, fill="#1C2A3A")
        bar(ic, cx - 56, cy - 2, 96, 10, fill="#C3C1BA")
        bar(ic, cx - 56, cy + 16, 80, 10, fill="#C3C1BA")
    ic.circle(cx, cy, r + 5, fill="none", stroke=two(ic, "#4A525C", "#1E2226"), stroke_width=10)


@soft("papers")
def papers(ic):
    tile(ic, "#4F5D6E", "#1F2731")
    soft_shadow(ic, 128, 216, 96, 12)
    with ic.g(transform="rotate(6 128 128)"):
        ic.rect(52, 38, 152, 174, rx=6, fill="#EDE5D3")
    ic.rect(48, 34, 156, 178, rx=6, fill=two(ic, *PAPER))
    ic.path("M54 34h144a6 6 0 0 1 6 6v6H48v-6a6 6 0 0 1 6 -6z", fill="#E2574A")
    bar(ic, 64, 60, 36, 6, fill="#C2402F")
    bar(ic, 64, 74, 70, 14, fill="#1E2630")
    bar(ic, 64, 94, 50, 14, fill="#1E2630")
    ic.circle(174, 86, 18, fill="#E8E2D6")
    ic.path("M174 86V68a18 18 0 0 1 16.4 25.3z", fill="#E2574A")
    ic.path("M174 86l16.4 7.3a18 18 0 0 1 -10.8 10z", fill="#F2A33A")
    for i in range(3):
        bar(ic, 64, 164 + i * 14, 124 if i != 2 else 70, 7, fill="#CCC9C2")
    # the bar magnifier across a line
    with ic.g(transform="rotate(-8 128 134)"):
        ic.rect(24, 116, 208, 38, rx=10, fill="#DCEAF4", stroke="#7F93A8", stroke_width=4)
        bar(ic, 40, 128, 150, 11, fill="#2E3640")
        ic.rect(26, 146, 204, 6, fill="#E2574A")


@soft("logseq")
def logseq(ic):
    tile(ic, "#0E4A58", "#03191F")
    soft_shadow(ic, 128, 218, 98, 11)
    ic.rect(34, 30, 186, 184, rx=16, fill=two(ic, "#1E5C68", "#0A3A44"))
    ic.rect(44, 40, 166, 166, rx=7, fill="#E2DAC8")
    ic.rect(42, 38, 164, 164, rx=7, fill=two(ic, "#FFFDF7", "#F1EADB"))
    bar(ic, 58, 52, 92, 13, fill="#0B3A44")
    for lvl, y, w in ((0, 84, 90), (1, 104, 72), (1, 124, 60), (0, 148, 84)):
        x = 64 + lvl * 18
        ic.circle(x, y, 6, fill="#DCD5C6")
        ic.circle(x, y, 3.2, fill="#4A5A5E")
        bar(ic, x + 12, y - 3.5, w, 7, fill="#7A8486" if lvl else "#2E3A3C")
    ic.line(64, 90, 64, 142, stroke="#C9C1B0", stroke_width=2)
    # a task, done
    ic.rect(58, 172, 14, 14, rx=4, fill="#1E7F8C")
    ic.path("M61.5 179l3 3 4.5-6", fill="none", stroke="#fff", stroke_width=2.4, stroke_linecap="round",
            stroke_linejoin="round")
    bar(ic, 80, 175.5, 54, 7, fill="#9AA4A6")
    ic.path("M140 198v20l6-5 6 5v-20z", fill="#2AA0AE")
    # the badge, its mark
    cx, cy = 194, 184
    ic.circle(cx, cy, 24, fill=two(ic, "#E2B45E", "#B88433"))
    ic.circle(cx, cy, 19, fill="#0E4A58")
    ic.ellipse(cx + 3, cy + 3.5, 10, 6.4, fill="none", stroke="#9FDCDC", stroke_width=4,
               transform=f"rotate(-28 {cx + 3} {cy + 3.5})")
    ic.ellipse(cx - 6.5, cy - 7, 5, 3.4, fill="#9FDCDC", transform=f"rotate(-28 {cx - 6.5} {cy - 7})")


@soft("joplin")
def joplin(ic):
    tile(ic, "#24508A", "#0B2042")
    soft_shadow(ic, 128, 218, 92, 12)
    with ic.g(transform="rotate(-4 128 128)"):
        ic.rect(56, 50, 152, 164, rx=12, fill="#E2DAC8")
        ic.rect(50, 44, 152, 166, rx=12, fill=two(ic, "#3A97F0", "#0A5CB4"))
        # the label and its J
        ic.rect(72, 92, 108, 74, rx=10, fill=two(ic, *PAPER))
        ic.rect(82, 104, 34, 34, rx=9, fill="#1071D3")
        ic.path("M103 112v12a6.5 6.5 0 0 1 -13 0", fill="none", stroke="#fff", stroke_width=5.5, stroke_linecap="round")
        bar(ic, 124, 112, 44, 9, fill="#123A6E")
        bar(ic, 82, 148, 70, 6, fill="#9FB4CC")
        # the wire coil
        for i in range(8):
            x = 66 + i * 17
            ic.path(f"M{x - 2} 56 c0 -10 7 -16 7 -16", fill="none", stroke=two(ic, "#D6DBE0", "#8D949C"),
                    stroke_width=4.5, stroke_linecap="round")
        ic.rect(184, 44, 9, 166, fill="#1A1E24")


@soft("obsidian")
def obsidian(ic):
    tile(ic, "#2E1F48", "#0C0716")
    soft_shadow(ic, 128, 214, 76, 11)
    A, B, C, D, E, F = (134, 24), (190, 72), (200, 150), (150, 212), (82, 196), (58, 112)
    P, Q = (122, 98), (148, 158)
    for pts, light, dark in (((A, P, F), "#E2D4FF", "#A27CF4"), ((A, B, P), "#B794FF", "#7C4CE8"),
                             ((B, C, Q, P), "#7B47E0", "#4A1CA8"), ((F, P, Q, E), "#9A6CF2", "#5A28B8"),
                             ((C, D, Q), "#3A1388", "#24095A"), ((D, E, Q), "#5826B8", "#2E0E6E")):
        ic.poly(pts, fill=two(ic, light, dark), stroke="#1A0838", stroke_opacity=0.3, stroke_width=1.5,
                stroke_linejoin="round")
    ic.poly(((190, 212), (202, 194), (216, 204), (208, 214)), fill="#7C4CE8")


@soft("foliate")
def foliate(ic):
    tile(ic, "#36447E", "#13193A")
    soft_shadow(ic, 128, 212, 104, 11)
    ic.path("M22 72 C60 64 104 70 128 80 C152 70 196 64 234 72 V202 C196 196 152 200 128 210 C104 200 60 196 22 202Z",
            fill=two(ic, "#9A3A2E", "#6E2218"))
    ic.path("M128 88 C104 76 66 70 30 74 V194 C66 190 104 194 128 206 C152 194 190 190 226 194 V74 C190 70 152 76 128 88Z",
            fill="#D6CDB8")
    ic.path("M128 84 C104 70 66 64 32 70 V190 C66 184 104 188 128 200Z", fill=two(ic, "#FFFDF6", "#F1EADB"))
    ic.path("M128 84 C152 70 190 64 224 70 V190 C190 184 152 188 128 200Z", fill=two(ic, "#F6F1E6", "#E7E0CF"))
    bar(ic, 58, 92, 36, 6, fill="#9A3A2E")
    bar(ic, 52, 106, 50, 11, fill="#2A2420")
    for i in range(5):
        bar(ic, 44, 130 + i * 12, 70 if i != 4 else 46, 6, fill="#C3BBAA")
    for i in range(8):
        bar(ic, 140, 86 + i * 12, 72 if i not in (3, 7) else 46, 6, fill="#C3BBAA")
    ic.path("M131 84 C133 120 128 160 136 202 L139 222 L134 216 L129 223 L130 204 C124 160 128 120 126 85Z",
            fill="#3E62C8")
