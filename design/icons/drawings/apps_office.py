"""The inua-objects theme, office batch: LibreOffice and its Writer, Calc,
Impress and Draw; Zotero, calibre, Okular, Logseq, Joplin, Obsidian,
Foliate and Document Viewer (docs/feat/object-icons.md, Part 2)."""

from lib import (brass, glare, graphite, icon, leather, paper, shadow, small, steel, tile, wood)


# --- shared: LibreOffice's documents ----------------------------------------

# each document's colour: the folded corner's light and dark, the tile's
LO = {
    "writer": ("#6DB7F7", "#1A5FB4", "#2F65A0", "#122C4E"),
    "calc": ("#93DB6A", "#2A8A2A", "#2E7A3E", "#0F3818"),
    "impress": ("#FFAA62", "#D2521C", "#A84E28", "#52200C"),
    "draw": ("#FFDC62", "#D69808", "#9A7220", "#4A3408"),
    "start": ("#5FD24A", "#14900A", "#3A4652", "#161D24"),
}


def _page(ic, x, y, w, h, fold, fill, tab=None, outline=0.08):
    """A sheet with its top right corner folded over, the fold in the
    document's colour (tab: a key of LO)."""
    ic.path(f"M{x} {y}h{w - fold}l{fold} {fold}v{h - fold}h{-w}z", fill=fill,
            stroke="#000", stroke_opacity=outline)
    ic.line(x + 1, y + 0.8, x + w - fold - 1, y + 0.8, stroke="#fff", stroke_width=1.2, opacity=0.9)
    if tab:
        light, dark = LO[tab][0], LO[tab][1]
        ic.path(f"M{x + w - fold} {y}l{fold} {fold}h{-fold * 0.8}l{-fold * 0.2} {-fold * 0.2}z",
                fill="#000", opacity=0.10, transform="translate(-1.5 2)")
        ic.path(f"M{x + w - fold} {y}v{fold - 3}a3 3 0 0 0 3 3h{fold - 3}z",
                fill=ic.lin([(0, light), (1, dark)], 0, 0, 1, 1))
        ic.path(f"M{x + w - fold + 1} {y + 2}v{fold - 6}", stroke="#fff", stroke_opacity=0.45, stroke_width=1)


def _lo_mark(ic, x, y, s, colour, width=None):
    """LibreOffice's document mark, simplified: a page's outline with its
    corner folded, s px tall, its top left at (x, y)."""
    w = s * 0.78
    f = s * 0.3
    sw = width or s * 0.1
    ic.path(f"M{x} {y}h{w - f}l{f} {f}v{s - f}h{-w}z", fill="none", stroke=colour, stroke_width=sw,
            stroke_linejoin="round")
    ic.path(f"M{x + w - f} {y}v{f}h{f}z", fill=colour, stroke=colour, stroke_width=sw * 0.6, stroke_linejoin="round")


def _small_page(ic, tab, tile_=True):
    light, dark, top, bottom = LO[tab]
    if tile_:
        tile(ic, top, bottom)
    ic.path("M3.5 2h6l3 3v9h-9z", fill="#F7F5F0")
    ic.path("M9.5 2v3h3z", fill=dark)


# --- LibreOffice: its four documents fanned out, the start page in front -----

@icon("libreoffice-startcenter", kind="app", title="LibreOffice", names=[
    "libreoffice", "libreoffice-main", "libreoffice-startcenter", "libreoffice7.3-main",
    "libreoffice7.3-startcenter", "libreoffice7.4-main", "libreoffice7.4-startcenter", "libreoffice7.5-main",
    "libreoffice7.5-startcenter", "libreoffice7.6-main", "libreoffice7.6-startcenter",
    "org.libreoffice.LibreOffice.startcenter"])
def libreoffice(ic):
    tile(ic, LO["start"][2], LO["start"][3])
    shadow(ic, 128, 214, 98, 12)
    for tab, deg in (("draw", -27), ("impress", -10), ("calc", 10), ("writer", 27)):
        with ic.g(transform=f"rotate({deg} 128 230)"):
            ic.rect(84, 50, 88, 118, fill="#000", opacity=0.12, transform="translate(2 3)")
            _page(ic, 84, 50, 88, 118, 22, paper(ic, "white"), tab)
            for i, wl in enumerate((52, 60, 44, 58, 36)):
                ic.rect(94, 80 + i * 9, wl, 3, rx=1.5, fill="#B9B4AA")
    ic.rect(74, 66, 108, 146, fill="#000", opacity=0.16, transform="translate(3 4)")
    _page(ic, 74, 66, 108, 146, 26, ic.lin([(0, "#FFFFFF"), (1, "#E9E5DC")]), "start")
    _lo_mark(ic, 108.6, 98.4, 46, "#0E6E08", 5.2)
    _lo_mark(ic, 107.4, 97.2, 46, "#8AE77A", 5.2)
    _lo_mark(ic, 108, 98, 46, "#1A9A12", 5.2)
    ic.text("LibreOffice", 128, 170, 13.5, font="sans-semibold", anchor="middle", fill="#2C3A2A")
    ic.text("START CENTER", 128, 183, 5.6, font="mono", anchor="middle", spacing=1.2, fill="#7C786F")
    for i, (tab, x) in enumerate((("writer", 98), ("calc", 115), ("impress", 132), ("draw", 149))):
        ic.rect(x, 191, 10, 10, rx=2, fill=LO[tab][1])
        ic.rect(x + 1.5, 192, 7, 1.2, rx=0.6, fill="#fff", opacity=0.45)


@small("libreoffice-startcenter")
def libreoffice16(ic):
    tile(ic, LO["start"][2], LO["start"][3])
    for tab, deg in (("draw", -24), ("writer", 24)):
        ic.path("M5 3h5l2 2v8H5z", fill=LO[tab][1], transform=f"rotate({deg} 8.5 14)")
    ic.path("M4 3h6l2.5 2.5V14H4z", fill="#F7F5F0")
    ic.path("M10 3v2.5h2.5z", fill=LO["start"][1])
    ic.path("M6 6.2h2.6l1.2 1.2v4H6z", fill="none", stroke="#1A9A12", stroke_width=1)


# --- Writer: a letter, typed, and a fountain pen ----------------------------

@icon("libreoffice-writer", kind="app", title="LibreOffice Writer", names=[
    "libreoffice-writer", "libreoffice7.3-writer", "libreoffice7.4-writer", "libreoffice7.5-writer",
    "libreoffice7.6-writer", "org.libreoffice.LibreOffice.writer"])
def writer(ic):
    tile(ic, LO["writer"][2], LO["writer"][3])
    shadow(ic, 128, 214, 88, 11)
    with ic.g(transform="rotate(-6 128 130)"):
        ic.rect(58, 38, 140, 174, rx=2, fill=paper(ic, "cream"), stroke="#000", stroke_opacity=0.08)
    ic.rect(56, 34, 146, 178, fill="#000", opacity=0.14, transform="translate(3 3)")
    _page(ic, 56, 34, 146, 178, 32, paper(ic, "white"), "writer")
    ic.text("Lyon, 30 October 2026", 70, 54, 6.4, font="mono", fill="#8C887F")
    ic.text("Dear Ada,", 70, 80, 12, font="sans-semibold", fill="#1C3556")
    body = ("Thank you for the drafts. The", "chapter on the engine reads", "beautifully now; I have marked",
            "two small changes in the margin", "and one table to set again.")
    for i, s in enumerate(body):
        ic.text(s, 70, 97 + i * 11, 7.3, fill="#4E4C47")
    ic.text("Yours ever,", 70, 165, 7.3, fill="#4E4C47")
    ic.text("Mary", 72, 186, 20, font="hand", fill="#1A5FB4")
    _lo_mark(ic, 182, 194, 10, "#1A5FB4", 1.3)
    # the pen, across the page's corner
    with ic.g(transform="rotate(-34 176 178)"):
        ic.rect(118, 176, 112, 12, rx=6, fill="#000", opacity=0.22, transform="translate(3 6)")
        ic.path("M118 182 l-16 -3.2 a1.2 1.2 0 0 0 0 6.4 z", fill=brass(ic))
        ic.line(103, 182, 112, 182, stroke="#5A3A10", stroke_width=0.8)
        ic.rect(116, 177.5, 6, 9, rx=1.5, fill="#1B1E24")
        ic.rect(120, 176, 108, 12, rx=6, fill=ic.lin([(0, "#4A86D8"), (0.35, "#1E4F9A"), (1, "#0A2550")]))
        ic.rect(180, 175.5, 6, 13, fill=brass(ic, 0, 0, 0, 1))
        ic.rect(186, 174.8, 42, 14.4, rx=7, fill=ic.lin([(0, "#3D78C8"), (0.35, "#173F80"), (1, "#081C40")]))
        ic.rect(192, 172, 30, 4, rx=2, fill=brass(ic, 0, 0, 0, 1))
        ic.rect(124, 178, 98, 1.6, rx=0.8, fill="#fff", opacity=0.35)


@small("libreoffice-writer")
def writer16(ic):
    _small_page(ic, "writer")
    for y, w in ((6.5, 5), (8.5, 6), (10.5, 4.5)):
        ic.rect(5, y, w, 0.9, fill="#5A6E8A")


# --- Calc: a ledger, its sum selected --------------------------------------

@icon("libreoffice-calc", kind="app", title="LibreOffice Calc", names=[
    "libreoffice-calc", "libreoffice7.3-calc", "libreoffice7.4-calc", "libreoffice7.5-calc",
    "libreoffice7.6-calc", "org.libreoffice.LibreOffice.calc"])
def calc(ic):
    tile(ic, LO["calc"][2], LO["calc"][3])
    shadow(ic, 128, 214, 96, 12)
    with ic.g(transform="rotate(5 128 130)"):
        ic.rect(44, 42, 172, 164, rx=2, fill=paper(ic, "cream"), stroke="#000", stroke_opacity=0.08)
    ic.rect(36, 38, 184, 170, fill="#000", opacity=0.14, transform="translate(3 3)")
    _page(ic, 36, 38, 184, 170, 28, paper(ic, "white"), "calc")
    # the formula bar
    ic.rect(46, 48, 140, 14, rx=2, fill="#F1F4EE", stroke="#C9D3C2", stroke_width=0.8)
    ic.text("fx", 51, 58.5, 7.5, font="sans-semibold", fill="#2A8A2A")
    ic.line(62, 50, 62, 60, stroke="#C9D3C2")
    ic.text("=SUM(C2:C5)", 67, 58.5, 7.5, font="mono-semibold", fill="#3B3A36")
    # the grid
    x0, cols, y0, rh = 46, (46, 58, 120, 166, 212), 70, 15
    ic.rect(x0, y0, 166, 12, fill="#DCEFD2")
    ic.rect(x0, y0 + 12, 12, rh * 8, fill="#EEF4EA")
    for i, c in enumerate(("A", "B", "C")):
        ic.text(c, (cols[i + 1] + cols[i + 2]) / 2, y0 + 9, 6.5, font="sans-semibold", anchor="middle", fill="#3E6A34")
    rows = [("Budget", "Q3", "Q4"), ("Rent", "1,200.00", "1,200.00"), ("Power", "84.20", "96.10"),
            ("Books", "42.00", "18.50"), ("Travel", "310.00", "475.00"), ("Total", "1,636.20", "1,789.60")]
    for r in range(8):
        y = y0 + 12 + r * rh
        ic.text(str(r + 1), 52, y + 10.5, 5.8, font="mono", anchor="middle", fill="#7A8574")
        if r < len(rows):
            bold = r in (0, 5)
            a, b, c = rows[r]
            ic.text(a, 61, y + 10.5, 7, font="sans-semibold" if bold else "sans", fill="#2E2D2A")
            for v, xr in ((b, 163), (c, 209)):
                ic.text(v, xr, y + 10.5, 6.6, font="mono-semibold" if bold else "mono", anchor="end", fill="#2E2D2A")
    for x in cols:
        ic.line(x, y0, x, y0 + 12 + rh * 8, stroke="#C9D3C2", stroke_width=0.8)
    for r in range(10):
        ic.line(x0, y0 + (0 if r == 0 else 12 + (r - 1) * rh), 212, y0 + (0 if r == 0 else 12 + (r - 1) * rh),
                stroke="#C9D3C2", stroke_width=0.8)
    ty = y0 + 12 + 5 * rh
    ic.line(58, ty - 1.5, 212, ty - 1.5, stroke="#2E2D2A", stroke_width=0.7)
    # the selected cell, its fill handle
    ic.rect(166, ty, 46, rh, fill="#2A8A2A", opacity=0.08)
    ic.rect(166, ty, 46, rh, fill="none", stroke="#1E7A1E", stroke_width=2)
    ic.rect(209.5, ty + rh - 2.5, 5, 5, fill="#1E7A1E", stroke="#fff", stroke_width=1)
    ic.rect(166, y0, 46, 12, fill="#2A8A2A", opacity=0.18)
    ic.rect(x0, ty, 12, rh, fill="#2A8A2A", opacity=0.18)
    _lo_mark(ic, 202, 192, 10, "#2A8A2A", 1.3)


@small("libreoffice-calc")
def calc16(ic):
    _small_page(ic, "calc")
    ic.rect(4.5, 6, 7, 6.5, fill="none", stroke="#8FA488", stroke_width=0.6)
    ic.line(7.5, 6, 7.5, 12.5, stroke="#8FA488", stroke_width=0.6)
    for y in (8.2, 10.4):
        ic.line(4.5, y, 11.5, y, stroke="#8FA488", stroke_width=0.6)
    ic.rect(7.5, 10.4, 4, 2.1, fill="none", stroke="#1E7A1E", stroke_width=0.9)


# --- Impress: a slide on an easel -------------------------------------------

@icon("libreoffice-impress", kind="app", title="LibreOffice Impress", names=[
    "libreoffice-impress", "libreoffice7.3-impress", "libreoffice7.4-impress", "libreoffice7.5-impress",
    "libreoffice7.6-impress", "org.libreoffice.LibreOffice.impress"])
def impress(ic):
    tile(ic, LO["impress"][2], LO["impress"][3])
    shadow(ic, 128, 216, 92, 10)
    leg = wood(ic, "#B07A48", "#5E3A18")
    ic.path("M124 30h8l3 186h-14z", fill=wood(ic, "#7A5232", "#3E2410"))
    ic.path("M98 140h10l-30 78h-10z", fill=leg)
    ic.path("M148 140h10l30 78h-10z", fill=leg)
    ic.line(99, 141, 70, 217, stroke="#E8C08A", stroke_opacity=0.5)
    ic.circle(128, 34, 5, fill=brass(ic))
    # the slide
    ic.rect(30, 40, 196, 122, fill="#000", opacity=0.2, transform="translate(3 4)")
    _page(ic, 30, 40, 196, 122, 26, paper(ic, "white"), "impress")
    ic.text("Q4 Roadmap", 44, 66, 16, font="sans-bold", fill="#3A1A0A")
    ic.text("Board review · 30 October", 44, 78, 6.4, font="mono", fill="#8C887F")
    ic.line(44, 86, 196, 86, stroke="#D2521C", stroke_width=1.5, opacity=0.8)
    bar = ic.lin([(0, "#FFAA62"), (1, "#D2521C")])
    for i, h in enumerate((18, 28, 38, 50)):
        ic.rect(46 + i * 18, 150 - h, 13, h, rx=1.5, fill=bar if i == 3 else "#E7C1A8")
    ic.line(42, 150.5, 120, 150.5, stroke="#6A665D", stroke_width=1)
    ic.text("+38%", 106.5, 96, 7, font="mono-semibold", anchor="middle", fill="#D2521C")
    for i, s in enumerate(("Ship the new reader", "Open a Lyon office", "Hire two editors")):
        y = 106 + i * 15
        ic.rect(132, y - 5.5, 5, 5, rx=1, fill="#D2521C")
        ic.text(s, 142, y, 7.2, fill="#3B3A36")
    _lo_mark(ic, 208, 146, 10, "#D2521C", 1.3)
    # the ledge it stands on
    ic.rect(24, 160, 208, 9, rx=2, fill=wood(ic, "#C99260", "#6E4420"))
    ic.line(26, 160.8, 230, 160.8, stroke="#F2D2A6", stroke_opacity=0.6, stroke_width=1.2)
    ic.rect(52, 155, 16, 5, rx=1.5, fill="#EDEAE2")
    ic.rect(72, 155.5, 12, 4.5, rx=1.5, fill="#D2521C")


@small("libreoffice-impress")
def impress16(ic):
    tile(ic, LO["impress"][2], LO["impress"][3])
    ic.path("M7.4 9h1.2l-.2 5.5h-.8z M5 9h1.2l-2 5H3z M9.8 9H11l2 5h-1.2z", fill="#C48A55")
    ic.rect(1.5, 2.5, 13, 8, fill="#F7F5F0")
    ic.path("M11.5 2.5h3v3z", fill=LO["impress"][1])
    for i, h in enumerate((2, 3, 4.5)):
        ic.rect(3.2 + i * 2, 9 - h, 1.4, h, fill="#D2521C" if i == 2 else "#E6B394")
    ic.rect(9, 5, 3.5, 0.9, fill="#8C887F")
    ic.rect(9, 7, 3, 0.9, fill="#8C887F")


# --- Draw: a drawing sheet, a curve being edited, and a pencil ---------------

@icon("libreoffice-draw", kind="app", title="LibreOffice Draw", names=[
    "libreoffice-draw", "libreoffice7.3-draw", "libreoffice7.4-draw", "libreoffice7.5-draw",
    "libreoffice7.6-draw", "org.libreoffice.LibreOffice.draw"])
def draw(ic):
    tile(ic, LO["draw"][2], LO["draw"][3])
    shadow(ic, 128, 214, 94, 12)
    ic.rect(40, 36, 176, 174, fill="#000", opacity=0.14, transform="translate(3 3)")
    _page(ic, 40, 36, 176, 174, 28, paper(ic, "white"), "draw")
    # a light grid
    grid = ic.define('<pattern id="{id}" width="12" height="12" patternUnits="userSpaceOnUse" x="4" y="0">'
                     '<path d="M12 0V12H0" fill="none" stroke="#C8D2DC" stroke-width=".6"/></pattern>', "p")
    ic.path("M48 46h132l26 26v128H48z", fill=f"url(#{grid})", opacity=0.8)
    # shapes
    ic.circle(96, 102, 32, fill=ic.lin([(0, "#FFE38A"), (1, "#F2B416")]), stroke="#8A5F00", stroke_width=2)
    ic.path("M120 150 L158 86 L196 150 Z", fill=ic.lin([(0, "#7FB8F0"), (1, "#3584E4")]), stroke="#1A4F94",
            stroke_width=2, stroke_linejoin="round", opacity=0.92)
    # the curve, selected: its points and handles
    ic.path("M58 190 C 84 140, 124 206, 150 168 S 196 150, 204 178", fill="none", stroke="#2E2D2A",
            stroke_width=2.6, stroke_linecap="round")
    for (x1, y1), (x2, y2) in (((150, 168), (130, 196)), ((150, 168), (170, 140))):
        ic.line(x1, y1, x2, y2, stroke="#1A5FB4", stroke_width=1)
        ic.circle(x2, y2, 3, fill="#fff", stroke="#1A5FB4", stroke_width=1.2)
    for x, y in ((58, 190), (150, 168), (204, 178)):
        ic.rect(x - 3.5, y - 3.5, 7, 7, fill="#1A5FB4" if (x, y) == (150, 168) else "#fff",
                stroke="#1A5FB4", stroke_width=1.3)
    # the circle's frame
    ic.rect(62, 68, 68, 68, fill="none", stroke="#1A5FB4", stroke_width=0.9, stroke_dasharray="3 2")
    for x in (62, 96, 130):
        for y in (68, 102, 136):
            if (x, y) != (96, 102):
                ic.rect(x - 2.5, y - 2.5, 5, 5, fill="#fff", stroke="#1A5FB4", stroke_width=1)
    _lo_mark(ic, 198, 190, 10, "#C88A00", 1.3)
    # the pencil
    with ic.g(transform="rotate(-48 176 180)"):
        ic.rect(132, 178, 100, 11, rx=2, fill="#000", opacity=0.22, transform="translate(4 7)")
        ic.path("M132 178 l-18 5.5 18 5.5z", fill="#EBC795")
        ic.path("M120 181.7 l-6 1.8 6 1.8z", fill="#2A2C30")
        ic.rect(132, 178, 86, 11, fill=ic.lin([(0, "#FFE07A"), (0.45, "#F2B416"), (1, "#B07A00")]))
        ic.line(132, 181.7, 218, 181.7, stroke="#000", stroke_opacity=0.12)
        ic.line(132, 185.3, 218, 185.3, stroke="#000", stroke_opacity=0.12)
        ic.rect(218, 177.5, 9, 12, fill=steel(ic, False))
        ic.rect(227, 178, 9, 11, rx=3, fill="#E77A8A")


@small("libreoffice-draw")
def draw16(ic):
    _small_page(ic, "draw")
    ic.circle(7, 8.5, 2.3, fill="#F2B416", stroke="#8A5F00", stroke_width=0.6)
    ic.path("M7.5 13 L10 8.5 L12.5 13z", fill="#3584E4")


# --- Zotero: an article on a stack of papers, a red Z bookmark ---------------

@icon("zotero", kind="app", title="Zotero", names=["org.zotero.Zotero", "zotero"])
def zotero(ic):
    tile(ic, "#6E3236", "#2E1214")
    shadow(ic, 128, 214, 96, 12)
    for deg, c in ((-7, "#D8D0BF"), (4, "#E6DFD0"), (-2, "#EFEADF")):
        with ic.g(transform=f"rotate({deg} 128 128)"):
            ic.rect(52, 40, 152, 168, rx=2, fill=c, stroke="#000", stroke_opacity=0.08)
    ic.rect(50, 36, 156, 172, rx=2, fill="#000", opacity=0.12, transform="translate(2 3)")
    ic.rect(50, 36, 156, 172, rx=2, fill=paper(ic, "white"))
    ic.line(52, 36.8, 204, 36.8, stroke="#fff", stroke_width=1.2)
    ic.text("PROC. LONDON MATH. SOC.", 74, 54, 5.6, font="mono", spacing=0.4, fill="#8C887F")
    ic.text("On Computable", 74, 76, 11.5, font="sans-bold", fill="#2A1A1C")
    ic.text("Numbers · 1936", 74, 90, 11.5, font="sans-bold", fill="#2A1A1C")
    ic.text("A. M. Turing", 74, 104, 7.5, font="sans-medium", fill="#5A3A3C")
    ic.line(64, 112, 192, 112, stroke="#CC2936", stroke_width=1, opacity=0.6)
    for col in (64, 132):
        for i in range(7):
            w = 58 if i not in (3, 6) else 40
            ic.rect(col, 120 + i * 8, w, 3, rx=1.5, fill="#BDB8AE")
    ic.rect(64, 180, 60, 14, rx=3, fill="#F4E4E5")
    ic.text("Cited by 14,212", 68, 190, 6.2, font="mono-semibold", fill="#A0202C")
    # the paper clip
    ic.path("M56 26 v30 a6 6 0 0 0 12 0 v-26 a3.5 3.5 0 0 0 -7 0 v22", fill="none", stroke="#000",
            stroke_opacity=0.25, stroke_width=3, stroke_linecap="round", transform="translate(1.5 2)")
    ic.path("M56 26 v30 a6 6 0 0 0 12 0 v-26 a3.5 3.5 0 0 0 -7 0 v22", fill="none", stroke=steel(ic),
            stroke_width=2.6, stroke_linecap="round")
    # the bookmark, over the top edge, its Z
    ic.add('<g transform="translate(10 0)">')
    ic.path("M156 24h34v94l-17 -12 -17 12z", fill="#000", opacity=0.22, transform="translate(3 4)")
    ic.path("M156 24h34v94l-17 -12 -17 12z", fill=ic.lin([(0, "#E8484F"), (0.5, "#CC2936"), (1, "#8E1620")], 0, 0, 1, 0))
    ic.path("M156 24h34v12h-34z", fill="#000", opacity=0.18)
    ic.line(157, 37, 189, 37, stroke="#FF8A8F", stroke_opacity=0.6)
    ic.path("M160.5 52h25v6l-17 26h17v7h-26.5v-6l17 -26h-15.5z", fill="#7A1018", opacity=0.6, transform="translate(0.8 1)")
    ic.path("M160.5 52h25v6l-17 26h17v7h-26.5v-6l17 -26h-15.5z", fill="#FFF6F2")
    ic.add("</g>")


@small("zotero")
def zotero16(ic):
    tile(ic, "#6E3236", "#2E1214")
    ic.rect(3.5, 3, 9.5, 11, rx=0.5, fill="#E6DFD0", transform="rotate(-6 8 8)")
    ic.rect(3, 3, 9.5, 11, rx=0.5, fill="#FBFAF6")
    ic.path("M7.5 1h6v10l-3-2-3 2z", fill="#CC2936")
    ic.path("M8.7 3.2h3.6l-3.6 4.6h3.6", fill="none", stroke="#fff", stroke_width=1.1, stroke_linejoin="round")


# --- calibre: a bookshelf ----------------------------------------------------

@icon("calibre", kind="app", title="calibre", names=[
    "accessories-ebook-reader", "bookreader", "calibre", "calibre-gui", "com.calibre_ebook.calibre",
    "gnome-books", "lrfviewer", "org.gnome.Books"])
def calibre(ic):
    tile(ic, "#5A4636", "#241A12")
    shadow(ic, 128, 216, 104, 11)
    # the case
    ic.rect(26, 40, 204, 172, rx=6, fill=wood(ic, "#B47A46", "#5E3818"))
    ic.rect(38, 52, 180, 142, rx=2, fill=ic.lin([(0, "#2A1A10"), (1, "#3E2818")]))
    ic.line(28, 41, 228, 41, stroke="#F0C894", stroke_opacity=0.55, stroke_width=1.5)
    ic.line(27, 42, 27, 210, stroke="#F0C894", stroke_opacity=0.35)
    # the books, each spine: x, width, height, colour, band, title
    books = [(42, 20, 128, ("#A33A30", "#5E1A14"), "#E8C27A", "ODYSSEY"),
             (62, 16, 112, ("#2E4F7E", "#16294A"), "#D8D2C2", "DUNE"),
             (78, 24, 134, ("#4E6A3A", "#26381A"), "#E8C27A", "MIDDLEMARCH"),
             (102, 14, 104, ("#D9B470", "#9A7430"), "#5A3A10", ""),
             (116, 20, 122, ("#3A2E4E", "#1C1428"), "#E8C27A", "ULYSSES"),
             (136, 18, 116, ("#2F6E6A", "#14403C"), "#F0E6D0", "EMMA"),
             (154, 22, 130, ("#8E4A2A", "#4A2210"), "#E8C27A", "WALDEN")]
    for x, w, h, (c1, c2), band, title in books:
        y = 194 - h
        ic.rect(x, y, w, h, rx=1.5, fill=ic.lin([(0, c1), (0.55, c2), (1, c2)], 0, 0, 1, 0))
        ic.rect(x + 1.5, y + 1, 2, h - 2, fill="#fff", opacity=0.14)
        ic.rect(x, y + 10, w, 3, fill=band, opacity=0.85)
        ic.rect(x, y + h - 14, w, 3, fill=band, opacity=0.85)
        if title:
            with ic.g(transform=f"rotate(-90 {x + w / 2} {y + h / 2})"):
                ic.text(title, x + w / 2, y + h / 2 + 2.4, 6.8, font="sans-condensed", anchor="middle",
                        spacing=0.6, fill=band)
    # one leaning on the rest
    with ic.g(transform="rotate(16 214 194)"):
        ic.rect(194, 76, 20, 118, rx=1.5, fill=ic.lin([(0, "#C9563A"), (0.55, "#8A2A18"), (1, "#8A2A18")], 0, 0, 1, 0))
        ic.rect(195.5, 77, 2, 116, fill="#fff", opacity=0.14)
        ic.rect(194, 86, 20, 3, fill="#E8C27A", opacity=0.85)
        ic.rect(194, 176, 20, 3, fill="#E8C27A", opacity=0.85)
    ic.rect(38, 52, 180, 8, fill="#000", opacity=0.3)
    # the shelf's front, its brass label
    ic.rect(26, 194, 204, 18, rx=3, fill=wood(ic, "#C48A55", "#7A4A22"))
    ic.line(28, 194.8, 228, 194.8, stroke="#F6D8A8", stroke_opacity=0.7, stroke_width=1.5)
    ic.rect(100, 197.5, 56, 11, rx=2, fill=brass(ic))
    ic.rect(100, 197.5, 56, 11, rx=2, fill="none", stroke="#5A3A10", stroke_opacity=0.5, stroke_width=0.8)
    ic.text("calibre", 128, 206, 8.5, font="sans-semibold", anchor="middle", fill="#4A300A")
    for x in (103.5, 152.5):
        ic.circle(x, 203, 1.2, fill="#7E5A20")


@small("calibre")
def calibre16(ic):
    tile(ic, "#5A4636", "#241A12")
    ic.rect(1.5, 2.5, 13, 11, rx=0.8, fill="#9A6234")
    ic.rect(2.5, 3.5, 11, 8, fill="#2A1A10")
    for x, h, c in ((3, 7, "#A33A30"), (5, 6, "#2E4F7E"), (7, 7.5, "#4E6A3A"), (9, 5.5, "#D9B470"), (11, 6.5, "#2F6E6A")):
        ic.rect(x, 11.5 - h, 1.8, h, fill=c)
    ic.rect(1.5, 11.5, 13, 2, fill="#C48A55")


# --- Okular: a page under a round reading glass -----------------------------

def _okular_page(ic):
    ic.text("Lecture 7", 60, 58, 13, font="sans-bold", fill="#1C2A3A")
    ic.text("Eigenvalues and the", 60, 72, 7.5, font="sans-medium", fill="#3D5A78")
    ic.text("shape of a matrix", 60, 81, 7.5, font="sans-medium", fill="#3D5A78")
    for i in range(5):
        ic.rect(60, 92 + i * 8, 120 if i != 4 else 70, 3, rx=1.5, fill="#C3C1BA")
    ic.text("Av = λv", 152, 140, 12, font="sans-medium", anchor="middle", fill="#1C2A3A")
    for i in range(4):
        ic.rect(60, 160 + i * 8, 120 if i != 3 else 86, 3, rx=1.5, fill="#C3C1BA")


@icon("okular", kind="app", title="Okular", names=["okular", "org.kde.okular"])
def okular(ic):
    tile(ic, "#2E6690", "#0F2A40")
    shadow(ic, 128, 214, 96, 12)
    with ic.g(transform="rotate(-5 128 128)"):
        ic.rect(46, 34, 148, 178, rx=2, fill="#000", opacity=0.14, transform="translate(3 3)")
        ic.rect(46, 34, 148, 178, rx=2, fill=paper(ic, "white"))
        ic.line(48, 34.8, 192, 34.8, stroke="#fff", stroke_width=1.2)
        ic.rect(46, 34, 6, 178, fill="#3DAEE9", opacity=0.9)
        _okular_page(ic)
        ic.text("7 / 42", 182, 204, 5.8, font="mono", anchor="end", fill="#8C887F")
    cx, cy, r = 156, 132, 42
    # the handle
    with ic.g(transform=f"rotate(-45 {cx} {cy})"):
        ic.rect(cx - 8, cy + r + 2, 16, 66, rx=8, fill="#000", opacity=0.25, transform="translate(-6 6)")
        ic.rect(cx - 6, cy + r - 2, 12, 16, rx=2, fill=steel(ic))
        ic.rect(cx - 8, cy + r + 12, 16, 58, rx=8, fill=ic.lin([(0, "#3A4048"), (0.4, "#1E2226"), (1, "#0C0E10")], 0, 0, 1, 0))
        ic.rect(cx - 5.5, cy + r + 15, 3, 50, rx=1.5, fill="#fff", opacity=0.18)
    ic.circle(cx + 4, cy + 6, r + 7, fill="#000", opacity=0.2)
    # the lens, the page enlarged in it
    lens = ic.clip(f'<circle cx="{cx}" cy="{cy}" r="{r}"/>')
    with ic.g(clip_path=lens):
        ic.circle(cx, cy, r, fill="#FBFAF6")
        with ic.g(transform=f"translate({cx} {cy}) scale(1.7) translate({-cx} {-cy}) rotate(-5 128 128)"):
            ic.rect(30, 30, 200, 200, fill="#FFFFFF")
            _okular_page(ic)
        ic.circle(cx, cy, r, fill="#7FC4F0", opacity=0.14)
        ic.circle(cx, cy, r, fill=glare(ic, 1.6))
    ic.circle(cx, cy, r + 3.5, fill="none", stroke=ic.lin([(0, "#5A626C"), (0.5, "#2A2E34"), (1, "#0E1012")], 0, 0, 1, 1),
              stroke_width=8)
    ic.circle(cx, cy, r + 7, fill="none", stroke="#fff", stroke_opacity=0.18, stroke_width=1)
    ic.path(f"M{cx - 30} {cy - 14} a32 32 0 0 1 24 -24", fill="none", stroke="#fff", stroke_opacity=0.7,
            stroke_width=3, stroke_linecap="round")


@small("okular")
def okular16(ic):
    tile(ic, "#2E6690", "#0F2A40")
    ic.rect(2, 1.8, 9, 12, rx=0.5, fill="#F7F5F0")
    ic.rect(2, 1.8, 1.2, 12, fill="#3DAEE9")
    ic.line(11, 11, 14, 14, stroke="#1E2226", stroke_width=2, stroke_linecap="round")
    ic.circle(9, 9, 3.4, fill="#D8EDFA", stroke="#2A2E34", stroke_width=1.2)


# --- Document Viewer: a report, a bar magnifier across a line ----------------

def _papers_page(ic):
    ic.text("ANNUAL REPORT", 62, 64, 6, font="mono-semibold", spacing=1.2, fill="#C2402F")
    ic.text("The Year in", 62, 84, 15, font="sans-bold", fill="#1E2630")
    ic.text("Review", 62, 101, 15, font="sans-bold", fill="#1E2630")
    ic.text("Readers grew by a third.", 62, 136, 8, font="sans-medium", fill="#2E3640")
    for i in range(3):
        ic.rect(62, 112 + i * 7, 128 if i != 2 else 88, 2.6, rx=1.3, fill="#C3C1BA")
    for i in range(5):
        ic.rect(62, 148 + i * 7, 128 if i != 4 else 60, 2.6, rx=1.3, fill="#C3C1BA")


@icon("papers", kind="app", title="Document Viewer", names=["evince", "org.gnome.Evince", "org.gnome.Papers", "papers"])
def papers(ic):
    tile(ic, "#4F5D6E", "#1F2731")
    shadow(ic, 128, 214, 96, 12)
    with ic.g(transform="rotate(6 128 128)"):
        ic.rect(52, 38, 152, 174, rx=3, fill=paper(ic, "cream"), stroke="#000", stroke_opacity=0.08)
    ic.rect(48, 34, 156, 178, rx=3, fill="#000", opacity=0.14, transform="translate(3 3)")
    ic.rect(48, 34, 156, 178, rx=3, fill=paper(ic, "white"))
    ic.path("M48 37a3 3 0 0 1 3-3h150a3 3 0 0 1 3 3v6H48z", fill="#E2574A")
    ic.line(50, 34.8, 202, 34.8, stroke="#FF9A8E", stroke_width=1)
    _papers_page(ic)
    # the pie in the margin
    ic.circle(172, 84, 16, fill="#E8E2D6")
    ic.path("M172 84V68a16 16 0 0 1 14.6 22.5z", fill="#E2574A")
    ic.path("M172 84l14.6 6.5a16 16 0 0 1 -9.6 9z", fill="#F2A33A")
    ic.text("p. 12", 192, 204, 6, font="mono", anchor="end", fill="#8C887F")
    # the bar magnifier, lying across the line
    with ic.g(transform="rotate(-8 128 134)"):
        ic.rect(24, 118, 208, 34, rx=6, fill="#000", opacity=0.22, transform="translate(3 7)")
        bar = ic.clip('<rect x="24" y="118" width="208" height="34" rx="6"/>')
        with ic.g(clip_path=bar):
            ic.rect(24, 118, 208, 34, fill="#FFFFFF", opacity=0.55)
            with ic.g(transform="rotate(8 128 134) translate(118 133) scale(1.5) translate(-112 -133)"):
                ic.rect(30, 30, 200, 200, fill="#FFFFFF")
                _papers_page(ic)
            ic.rect(24, 118, 208, 34, fill="#BFE0F5", opacity=0.22)
            ic.rect(24, 118, 208, 34, fill=ic.lin([(0, "#fff", 0.75), (0.22, "#fff", 0.1), (0.6, "#000", 0),
                                                    (1, "#0A2A40", 0.35)]))
        ic.rect(24, 118, 208, 34, rx=6, fill="none", stroke="#7F93A8", stroke_width=2.4)
        ic.rect(24, 146, 208, 6, fill="#E2574A", opacity=0.85)
        ic.line(30, 119.5, 226, 119.5, stroke="#fff", stroke_width=1.6, opacity=0.9)
        ic.line(30, 151.3, 226, 151.3, stroke="#000", stroke_opacity=0.25)


@small("papers")
def papers16(ic):
    tile(ic, "#4F5D6E", "#1F2731")
    ic.rect(3, 1.5, 10, 13, rx=0.5, fill="#F7F5F0")
    ic.rect(3, 1.5, 10, 1.5, fill="#E2574A")
    ic.rect(4.5, 4.5, 5, 1.2, fill="#1E2630")
    ic.rect(1.5, 8, 13, 3.5, rx=0.8, fill="#BFD6EA", transform="rotate(-8 8 9.75)")
    ic.rect(1.5, 10.5, 13, 1, fill="#E2574A", transform="rotate(-8 8 9.75)")


# --- Logseq: a journal, its day as an outline --------------------------------

@icon("logseq", kind="app", title="Logseq", names=["com.logseq.Logseq", "logseq"])
def logseq(ic):
    tile(ic, "#0E4A58", "#03191F")
    shadow(ic, 128, 216, 98, 11)
    ic.rect(34, 30, 186, 184, rx=10, fill=leather(ic, "#1E5C68", "#062A32"))
    ic.rect(35, 31, 184, 182, rx=9, fill="none", stroke="#fff", stroke_opacity=0.12, stroke_width=1.5)
    for i in range(3, 0, -1):
        ic.rect(42, 38 + i, 164 + i, 166, rx=3, fill=("#D6CDB8", "#E2DAC8", "#ECE5D6")[i - 1])
    ic.rect(42, 38, 164, 166, rx=3, fill=paper(ic, "cream"))
    ic.text("Oct 30th, 2026", 58, 62, 13, font="sans-semibold", fill="#0B3A44")
    ic.line(58, 70, 190, 70, stroke="#0B3A44", stroke_opacity=0.2)
    lines = [(0, 88, "Ship the icon theme", None), (1, 104, "draw the office batch", None),
             (1, 120, "check every 16 px", None), (2, 136, "#icons  [[design]]", "#1E7F8C"),
             (0, 154, "Read twenty pages", None), (1, 170, "Walden, chapter 3", None)]
    for lvl, y, s, col in lines:
        x = 64 + lvl * 16
        ic.circle(x, y - 3, 4.6, fill="#DCD5C6")
        ic.circle(x, y - 3, 2.4, fill="#4A5A5E")
        ic.text(s, x + 9, y, 7.8, font="sans-medium" if col else "sans", fill=col or "#2E3A3C")
    for lvl, y1, y2 in ((0, 92, 168), (1, 124, 134)):
        ic.line(64 + lvl * 16, y1, 64 + lvl * 16, y2, stroke="#C9C1B0", stroke_width=1)
    # the ribbon, out of the bottom
    ic.path("M140 200v18l5-4 5 4v-18z", fill=ic.lin([(0, "#2AA0AE"), (1, "#14606A")], 0, 0, 1, 0))
    # a task, done
    ic.rect(59.5, 181, 9, 9, rx=2, fill="#1E7F8C")
    ic.path("M61.8 185.6l2 2 3.2-4", fill="none", stroke="#fff", stroke_width=1.4, stroke_linecap="round",
            stroke_linejoin="round")
    ic.text("DONE", 73, 188.5, 7.2, font="mono-semibold", fill="#1E7F8C")
    ic.text("call the printer", 96, 188.5, 7.8, fill="#7A8486")
    ic.line(96, 185.8, 158, 185.8, stroke="#7A8486", stroke_width=0.8)
    # the badge, enamel, its mark
    cx, cy = 194, 186
    ic.circle(cx + 1.5, cy + 2.5, 22, fill="#000", opacity=0.3)
    ic.circle(cx, cy, 22, fill=brass(ic))
    ic.circle(cx, cy, 18.5, fill=ic.rad([(0, "#0E4A58"), (1, "#032028")], cx=0.4, cy=0.35, r=0.75))
    ic.ellipse(cx + 3, cy + 3.5, 10, 6.4, fill="none", stroke="#9FDCDC", stroke_width=3.2,
               transform=f"rotate(-28 {cx + 3} {cy + 3.5})")
    ic.ellipse(cx - 6.5, cy - 7, 4.6, 3, fill="#9FDCDC", transform=f"rotate(-28 {cx - 6.5} {cy - 7})")
    ic.path(f"M{cx - 15} {cy - 6} a17 17 0 0 1 10 -10", fill="none", stroke="#fff", stroke_opacity=0.35, stroke_width=1.5,
            stroke_linecap="round")


@small("logseq")
def logseq16(ic):
    tile(ic, "#0E4A58", "#03191F")
    ic.rect(2, 1.8, 12, 12.4, rx=1, fill="#1E5C68")
    ic.rect(2.8, 2.5, 10.4, 11, rx=0.5, fill="#F4EFE4")
    for x, y, w in ((4.5, 5, 6), (6.5, 7.5, 5), (4.5, 10, 6)):
        ic.circle(x, y, 0.9, fill="#1E7F8C")
        ic.rect(x + 1.6, y - 0.5, w - 1.6, 1, fill="#8A9496")


# --- Joplin: a blue spiral notebook -----------------------------------------

@icon("joplin", kind="app", title="Joplin", names=[
    "appimagekit-joplin", "joplin", "joplin-desktop", "net.cozic.joplin_desktop", "org.joplinapp.joplin"])
def joplin(ic):
    tile(ic, "#24508A", "#0B2042")
    shadow(ic, 128, 216, 92, 12)
    with ic.g(transform="rotate(-4 128 128)"):
        ic.rect(52, 46, 156, 168, rx=8, fill="#000", opacity=0.2, transform="translate(3 4)")
        ic.rect(56, 50, 152, 164, rx=8, fill="#E2DAC8")
        ic.rect(54, 48, 152, 164, rx=8, fill="#F2ECDF")
        ic.rect(50, 44, 152, 166, rx=8, fill=ic.lin([(0, "#3A97F0"), (0.6, "#1071D3"), (1, "#0A4E9E")], 0, 0, 1, 1))
        ic.rect(51, 45, 150, 164, rx=7, fill="none", stroke="#fff", stroke_opacity=0.2, stroke_width=1.5)
        # the label and its J
        ic.rect(72, 92, 108, 74, rx=6, fill="#000", opacity=0.18, transform="translate(1.5 2)")
        ic.rect(72, 92, 108, 74, rx=6, fill=paper(ic, "white"))
        ic.rect(80, 102, 34, 34, rx=8, fill=ic.lin([(0, "#2F8BEB"), (1, "#0D5DB8")]))
        ic.path("M101 109v13a6.5 6.5 0 0 1 -13 0", fill="none", stroke="#fff", stroke_width=4.4, stroke_linecap="round")
        ic.circle(101, 109, 0.1, fill="#fff")
        ic.text("Notes", 120, 124, 17, font="hand", fill="#123A6E")
        ic.line(82, 146, 170, 146, stroke="#9FB4CC", stroke_width=0.8)
        ic.text("Oct 2026 · Trips", 82, 157, 6.4, font="mono", fill="#6A7280")
        # the wire coil along the top
        for i in range(12):
            x = 62 + i * 12
            ic.circle(x, 54, 2.6, fill="#0A2A50")
            ic.path(f"M{x - 1} 55 c0 -10 6 -14 6 -14", fill="none", stroke="#1A1C20", stroke_width=3.4,
                    stroke_linecap="round", opacity=0.35, transform="translate(1 1.5)")
            ic.path(f"M{x - 1} 55 c0 -10 6 -14 6 -14", fill="none", stroke=steel(ic), stroke_width=2.6,
                    stroke_linecap="round")
        # the elastic band
        ic.rect(184, 44, 7, 166, fill=ic.lin([(0, "#2A2E36"), (1, "#121418")], 0, 0, 1, 0))
        ic.line(185, 44, 185, 210, stroke="#fff", stroke_opacity=0.15)


@small("joplin")
def joplin16(ic):
    tile(ic, "#24508A", "#0B2042")
    ic.rect(3, 3, 10.5, 11.5, rx=1, fill="#1071D3")
    for x in (4.5, 6.5, 8.5, 10.5, 12.5):
        ic.rect(x - 0.4, 1.8, 0.9, 2.4, rx=0.4, fill="#C3C8CE")
    ic.rect(5, 6.5, 6.5, 5, rx=0.6, fill="#FBFAF6")
    ic.path("M8.8 7.5v2a1.4 1.4 0 0 1-2.8 0", fill="none", stroke="#1071D3", stroke_width=1)


# --- Obsidian: the black-purple crystal --------------------------------------

@icon("obsidian", kind="app", title="Obsidian", names=["appimagekit-obsidian", "md.obsidian.Obsidian", "obsidian"])
def obsidian(ic):
    tile(ic, "#2E1F48", "#0C0716")
    shadow(ic, 128, 212, 76, 11)
    A, B, C, D, E, F = (134, 24), (190, 72), (200, 150), (150, 212), (82, 196), (58, 112)
    P, Q = (122, 98), (148, 158)

    def facet(pts, stops, x1=0, y1=0, x2=1, y2=1):
        ic.poly(pts, fill=ic.lin(stops, x1, y1, x2, y2), stroke="#1A0838", stroke_opacity=0.25,
                stroke_width=0.8, stroke_linejoin="round")

    facet((A, P, F), [(0, "#E2D4FF"), (1, "#A27CF4")])
    facet((A, B, P), [(0, "#B794FF"), (1, "#7C4CE8")])
    facet((B, C, Q, P), [(0, "#7B47E0"), (1, "#3E1594")])
    facet((F, P, Q, E), [(0, "#9A6CF2"), (1, "#4E1FA8")])
    facet((C, D, Q), [(0, "#3A1388"), (1, "#1C0848")])
    facet((D, E, Q), [(0, "#5826B8"), (1, "#24095A")])
    # light on the upper edges, the facet lines catching it
    ic.poly((F, A, B), close=False, fill="none", stroke="#fff", stroke_opacity=0.55, stroke_width=1.8,
            stroke_linejoin="round", stroke_linecap="round")
    ic.poly((A, P, Q), close=False, fill="none", stroke="#EBDDFF", stroke_opacity=0.5, stroke_width=1.2,
            stroke_linejoin="round")
    ic.line(*F, *P, stroke="#EBDDFF", stroke_opacity=0.4, stroke_width=1)
    ic.poly(((126, 40), (114, 86), (78, 112)), fill="#fff", opacity=0.22)
    ic.path("M172 92 l6 26", stroke="#D8C6FF", stroke_opacity=0.5, stroke_width=1.6, stroke_linecap="round")
    ic.poly((E, D, (150, 214), (82, 198)), fill="#0A0418", opacity=0.6)
    # its glow on the desk, and a chip at its foot
    ic.ellipse(140, 212, 46, 5, fill=ic.rad([(0, "#9A6CF2", 0.45), (1, "#9A6CF2", 0)]))
    ic.ellipse(204, 213, 14, 3, fill="#000", opacity=0.35)
    ic.poly(((190, 210), (202, 194), (216, 204), (208, 214)), fill="#2A0E5C")
    ic.poly(((190, 210), (202, 194), (204, 207)), fill="#A27CF4")
    ic.poly(((202, 194), (216, 204), (204, 207)), fill="#5826B8")
    ic.poly(((86, 150), (104, 126), (98, 168)), fill="#fff", opacity=0.08)
    ic.circle(134, 26, 2.2, fill="#fff", opacity=0.9)
    ic.path("M134 18v16M126 26h16", stroke="#fff", stroke_opacity=0.6, stroke_width=1, stroke_linecap="round")


@small("obsidian")
def obsidian16(ic):
    tile(ic, "#2E1F48", "#0C0716")
    ic.poly(((8.4, 1.5), (12, 4.5), (12.6, 9.5), (9.4, 14), (5, 12.8), (3.6, 7)), fill="#5A28C0")
    ic.poly(((8.4, 1.5), (7.6, 6.2), (3.6, 7)), fill="#D6C2FF")
    ic.poly(((8.4, 1.5), (12, 4.5), (7.6, 6.2)), fill="#9A6CF2")
    ic.poly(((12.6, 9.5), (9.4, 14), (9.3, 10)), fill="#24095A")


# --- Foliate: an open book, its ribbon ---------------------------------------

@icon("foliate", kind="app", title="Foliate", names=["com.github.johnfactotum.Foliate", "foliate"])
def foliate(ic):
    tile(ic, "#36447E", "#13193A")
    shadow(ic, 128, 210, 104, 11)
    # the cover under the pages
    ic.path("M22 72 C60 64 104 70 128 80 C152 70 196 64 234 72 V200 C196 194 152 198 128 208 C104 198 60 194 22 200Z",
            fill=leather(ic, "#9A3A2E", "#4E1812"))
    # page edges, left and right
    for i, c in ((4, "#C9C0AC"), (2, "#DCD4C2")):
        ic.path(f"M128 {84 + i} C104 {72 + i} 66 {66 + i} {30 + i * 0.5} {70 + i} V{190 + i} C66 {186 + i} 104 {190 + i} 128 {200 + i}Z", fill=c)
        ic.path(f"M128 {84 + i} C152 {72 + i} 190 {66 + i} {226 - i * 0.5} {70 + i} V{190 + i} C190 {186 + i} 152 {190 + i} 128 {200 + i}Z", fill=c)
    ic.path("M128 84 C104 70 66 64 32 70 V190 C66 184 104 188 128 200Z",
            fill=ic.lin([(0, "#FFFDF6"), (0.8, "#F1EADB"), (1, "#D9CFBA")], 0, 0, 1, 0))
    ic.path("M128 84 C152 70 190 64 224 70 V190 C190 184 152 188 128 200Z",
            fill=ic.lin([(0, "#D9CFBA"), (0.15, "#F3EDE0"), (1, "#E7E0CF")], 0, 0, 1, 0))
    ic.line(33, 71, 33, 189, stroke="#fff", stroke_width=1.2, opacity=0.8)
    # the left page: a chapter's opening
    ic.text("CHAPTER 1", 76, 94, 6, font="mono-semibold", anchor="middle", spacing=1.4, fill="#9A3A2E")
    ic.text("Loomings", 76, 110, 12, font="sans-semibold", anchor="middle", fill="#2A2420")
    ic.text("Call me Ishmael. Some", 44, 128, 7, fill="#3A3430")
    ic.text("years ago, never mind", 44, 138, 7, fill="#3A3430")
    ic.text("how long precisely,", 44, 148, 7, fill="#3A3430")
    for i in range(3):
        ic.rect(44, 154 + i * 8, 70 if i != 2 else 48, 2.6, rx=1.3, fill="#C3BBAA")
    # the right page
    for i in range(12):
        ic.rect(140, 86 + i * 8 - (0 if i else 0), 72 if i not in (5, 11) else 44, 2.6, rx=1.3, fill="#C3BBAA")
    ic.text("17", 176, 188, 6, font="mono", anchor="middle", fill="#8C887F")
    # the spine's shade and the ribbon
    ic.path("M120 80 C124 82 126 83 128 84 V200 C126 198 123 196 120 195Z", fill="#000", opacity=0.08)
    ic.path("M128 84 C130 83 132 82 138 79 V196 C134 197 131 198 128 200Z", fill="#000", opacity=0.1)
    ic.path("M131 84 C133 120 128 160 136 202 L139 222 L134 216 L129 223 L130 204 C124 160 128 120 126 85Z",
            fill=ic.lin([(0, "#3E62C8"), (1, "#22388A")], 0, 0, 1, 0))


@small("foliate")
def foliate16(ic):
    tile(ic, "#36447E", "#13193A")
    ic.path("M1.5 4.5 C4 4 6.5 4.5 8 5.3 C9.5 4.5 12 4 14.5 4.5 V13 C12 12.5 9.5 13 8 13.8 C6.5 13 4 12.5 1.5 13Z", fill="#9A3A2E")
    ic.path("M8 5.3 C6.5 4.3 4.5 3.9 2.5 4.1 V12 C4.5 11.8 6.5 12.2 8 13Z", fill="#FBF7EC")
    ic.path("M8 5.3 C9.5 4.3 11.5 3.9 13.5 4.1 V12 C11.5 11.8 9.5 12.2 8 13Z", fill="#EDE5D3")
    ic.rect(8.2, 8, 1, 7, fill="#3E62C8")
