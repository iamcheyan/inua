"""The inua-objects theme, writing and notes: ONLYOFFICE, WPS Office,
Notion, Standard Notes, Zettlr, Typora, Mark Text, Xournal++, Rnote,
Apostrophe and Planner (docs/feat/object-icons.md, Part 2).

The family: ONLYOFFICE its three layers as coloured slabs, a document on
top; WPS a fan of its three documents clipped with the red badge; Notion a
memo cube with the black-ruled N printed on it; Standard Notes a gum-top
notepad with blue index tabs; Zettlr a green card index box; Typora a
typewriter key; Mark Text a page and the rubber stamp that printed M-down
on it; Xournal++ a stylus on a ruled, wire-bound journal; Rnote a stylus
sketching on a tablet; Apostrophe a fountain pen shedding an apostrophe of
ink; Planner an open ring planner, today's tasks ticked."""

from lib import brass, glare, graphite, icon, paper, shadow, small, steel, tile, wood


def _pts(pts):
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"


# --- ONLYOFFICE: three coloured layers, a document on the top one ------------

def _slab(ic, cx, cy, hw, hh, t, top, side):
    L, T, R, B = (cx - hw, cy), (cx, cy - hh), (cx + hw, cy), (cx, cy + hh)
    ic.path(_pts([L, B, (B[0], B[1] + t), (L[0], L[1] + t)]), fill=ic.lin([(0, side[0]), (1, side[1])], 0, 0, 1, 0))
    ic.path(_pts([B, R, (R[0], R[1] + t), (B[0], B[1] + t)]), fill=ic.lin([(0, side[1]), (1, side[2])], 0, 0, 1, 0))
    ic.path(_pts([L, T, R, B]), fill=ic.lin([(0, top[0]), (1, top[1])], 0, 0, 1, 1))
    ic.path(f"M{L[0] + 2} {L[1]}L{T[0]} {T[1] + 1}L{R[0] - 2} {R[1]}", fill="none", stroke="#fff",
            stroke_opacity=0.45, stroke_width=1.5, stroke_linejoin="round")
    ic.line(L[0], L[1] + 0.5, B[0], B[1] + 0.5, stroke="#fff", stroke_opacity=0.25)


@icon("onlyoffice", kind="app", title="ONLYOFFICE",
      names=["asc-de", "onlyoffice", "onlyoffice-desktopeditors", "org.onlyoffice.desktopeditors"])
def onlyoffice(ic):
    tile(ic, "#4A5058", "#20242A")
    shadow(ic, 128, 210, 100, 14)
    cx, hw, hh, t = 128, 88, 44, 13
    _slab(ic, cx, 160, hw, hh, t, ("#FF7A5C", "#E2483A"), ("#C23A2C", "#9E2C20", "#7A1E14"))
    _slab(ic, cx, 130, hw, hh, t, ("#B4D95A", "#86B52E"), ("#7AA428", "#5E8420", "#456416"))
    _slab(ic, cx, 100, hw, hh, t, ("#7FD6F4", "#3FAEE0"), ("#3B9FD0", "#2A7FAE", "#1C5F86"))
    # the dark seams between the layers, as on the mark
    for y in (130, 160):
        ic.path(f"M{cx - hw} {y - 17}L{cx} {y + 27}L{cx + hw} {y - 17}", fill="none", stroke="#000",
                stroke_opacity=0.18, stroke_width=1)
    # a document lying on the top layer
    with ic.g(transform=f"matrix(0.88 -0.44 0.88 0.44 {cx - hw} 100)"):
        ic.rect(17, 13, 70, 76, rx=2, fill="#000", opacity=0.18)
        ic.rect(14, 10, 70, 76, rx=2, fill=paper(ic, "white"))
        ic.rect(14, 10, 70, 14, rx=2, fill="#E2483A")
        ic.text("Q4 report", 20, 37, 10, font="sans-bold", fill="#2A2C30")
        for i, w in enumerate((56, 50, 58, 40, 52)):
            ic.rect(20, 44 + i * 7.5, w, 2.6, rx=1, fill="#9AA1A9")
        ic.rect(60, 70, 18, 10, fill="#86B52E")
        ic.rect(68, 64, 10, 16, fill="#3FAEE0")


@small("onlyoffice")
def onlyoffice16(ic):
    tile(ic, "#4A5058", "#20242A")
    for cy, top, side in ((10.4, "#F25A44", "#9E2C20"), (8, "#9CC63F", "#5E8420"), (5.6, "#5BC3EC", "#2A7FAE")):
        ic.path(f"M2 {cy}L8 {cy + 3}L14 {cy}V{cy + 1.2}L8 {cy + 4.2}L2 {cy + 1.2}z", fill=side)
        ic.path(f"M2 {cy}L8 {cy - 3}L14 {cy}L8 {cy + 3}z", fill=top)
    ic.path("M5.5 5.6L8 4.3L10.5 5.6L8 6.9z", fill="#fff")


# --- WPS Office: its three documents fanned, the red badge clipped on --------

def _doc(ic, colour, letter, title):
    ic.rect(3, 4, 92, 122, rx=4, fill="#000", opacity=0.22)
    ic.rect(0, 0, 92, 122, rx=4, fill=paper(ic, "white"))
    ic.rect(0, 0, 92, 26, rx=4, fill=colour)
    ic.rect(0, 20, 92, 6, fill=colour)
    ic.text(letter, 10, 20, 18, font="sans-bold", fill="#fff")
    ic.text(title, 84, 17, 7, font="sans-semibold", anchor="end", fill="#fff", opacity=0.9)
    for i, w in enumerate((70, 62, 72, 50, 66, 58)):
        ic.rect(10, 38 + i * 9, w, 3, rx=1.5, fill="#C9CDD3")


@icon("wps-office", kind="app", title="WPS Office", names=["com.wps.Office", "wps-office", "wps-office2019-kprometheus"])
def wps(ic):
    tile(ic, "#2D3E66", "#121C3A")
    shadow(ic, 128, 214, 96, 12)
    with ic.g(transform="translate(54 66) rotate(-12 46 140)"):
        _doc(ic, "#E8672A", "P", "SLIDES")
    with ic.g(transform="translate(116 66) rotate(12 46 140)"):
        _doc(ic, "#1E9E5A", "S", "SHEETS")
        ic.rect(10, 38, 72, 54, fill="#fff")
        for r in range(6):
            ic.line(10, 38 + r * 9, 82, 38 + r * 9, stroke="#9BC9AE", stroke_width=0.8)
        for c in range(4):
            ic.line(10 + c * 24, 38, 10 + c * 24, 92, stroke="#9BC9AE", stroke_width=0.8)
    with ic.g(transform="translate(82 46)"):
        _doc(ic, "#2B6CDB", "W", "WRITER")
    # the clip and the red badge, its W in white
    bx, by = 112, 118
    ic.rect(bx + 3, by + 5, 72, 72, rx=18, fill="#000", opacity=0.3)
    ic.rect(bx, by, 72, 72, rx=18, fill=ic.lin([(0, "#FF5A4E"), (1, "#C21E1A")], 0, 0, 1, 1))
    ic.rect(bx + 0.75, by + 0.75, 70.5, 70.5, rx=17.25, fill="none", stroke="#fff", stroke_opacity=0.4,
            stroke_width=1.5)
    ic.rect(bx + 0.75, by + 0.75, 70.5, 70.5, rx=17.25, fill="none", stroke="#6A0A08", stroke_opacity=0.35,
            stroke_width=1.5, transform="translate(0.8 1)")
    w = f"M{bx + 15} {by + 22}L{bx + 26} {by + 52}L{bx + 36} {by + 32}L{bx + 46} {by + 52}L{bx + 57} {by + 22}"
    ic.path(w, fill="none", stroke="#7A0E0B", stroke_opacity=0.5, stroke_width=8, stroke_linecap="round",
            stroke_linejoin="round", transform="translate(1 1.5)")
    ic.path(w, fill="none", stroke="#fff", stroke_width=8, stroke_linecap="round", stroke_linejoin="round")
    ic.path(f"M{bx + 6} {by + 18}a14 14 0 0 1 14-12h30", fill="none", stroke="#fff", stroke_opacity=0.5,
            stroke_width=2, stroke_linecap="round")
    # the steel clip holding it to the documents
    ic.rect(bx + 26, by - 14, 20, 26, rx=4, fill="#000", opacity=0.25, transform="translate(1.5 2)")
    ic.rect(bx + 26, by - 14, 20, 26, rx=4, fill=steel(ic))
    ic.rect(bx + 30, by - 10, 12, 6, rx=2, fill="#4A5058")


@small("wps-office")
def wps16(ic):
    tile(ic, "#2D3E66", "#121C3A")
    ic.rect(1.6, 3.6, 6, 8, rx=0.6, fill="#E8672A", transform="rotate(-14 4.6 11)")
    ic.rect(8.4, 3.6, 6, 8, rx=0.6, fill="#1E9E5A", transform="rotate(14 11.4 11)")
    ic.rect(4.6, 2, 6.4, 8.6, rx=0.6, fill="#F4F6FA")
    ic.rect(4.6, 2, 6.4, 2, rx=0.6, fill="#2B6CDB")
    ic.rect(7, 7.6, 7, 7, rx=1.8, fill="#E2312B")
    ic.path("M8.4 9.4L9.4 12.4L10.5 10.4L11.6 12.4L12.6 9.4", fill="none", stroke="#fff", stroke_width=1,
            stroke_linecap="round", stroke_linejoin="round")


# --- Notion: a memo cube, white sheets over black, the N printed on it -------

def _notion_n(ic, x, y, s, stroke):
    """The black-ruled box and its serif N, s px square at (x, y)."""
    k = s / 100
    ic.rect(x + 3 * k, y + 4 * k, 96 * k, 96 * k, rx=10 * k, fill="#000", opacity=0.18)
    ic.path(f"M{x + 14 * k} {y}H{x + 90 * k}a10 10 0 0 1 {10 * k} {10 * k}V{y + 90 * k}a10 10 0 0 1 "
            f"{-10 * k} {10 * k}H{x + 18 * k}a10 10 0 0 1 {-8 * k} {-4 * k}L{x + 2 * k} {y + 82 * k}"
            f"a10 10 0 0 1 {-2 * k} {-6 * k}V{y + 12 * k}a10 10 0 0 1 {14 * k} {-12 * k}z",
            fill="#FFFFFF", stroke=stroke, stroke_width=7 * k, stroke_linejoin="round")
    ic.path(f"M{x + 6 * k} {y + 14 * k}L{x + 18 * k} {y + 22 * k}H{x + 92 * k}", fill="none", stroke=stroke,
            stroke_width=5 * k, stroke_linejoin="round")
    n = [(26, 32), (46, 32), (70, 68), (70, 40), (64, 38), (64, 32), (84, 32), (84, 38), (78, 40), (78, 86),
         (70, 86), (40, 42), (40, 76), (46, 78), (46, 84), (26, 84), (26, 78), (32, 76), (32, 40), (26, 38)]
    ic.path(_pts([(x + px * k, y + py * k) for px, py in n]), fill=stroke)


@icon("notion", kind="app", title="Notion", names=["Notion", "notion", "notion-app", "notion-app-enhanced"])
def notion(ic):
    tile(ic, "#77746E", "#34322E")
    shadow(ic, 134, 210, 98, 13)
    fx0, fx1, fy0, fy1, dx, dy = 52, 168, 86, 202, 38, -32
    # the right side: the sheets' edges, black ones at the foot
    side = [(fx1, fy0), (fx1 + dx, fy0 + dy), (fx1 + dx, fy1 + dy), (fx1, fy1)]
    ic.path(_pts(side), fill=ic.lin([(0, "#D9D6CF"), (1, "#B3AFA6")]))
    ic.path(_pts([(fx1, fy1 - 40), (fx1 + dx, fy1 - 40 + dy), (fx1 + dx, fy1 + dy), (fx1, fy1)]), fill="#1C1C1E")
    for i in range(1, 26):
        y = fy0 + i * 4.4
        if y > fy1 - 40:
            col, op = "#fff", 0.10
        else:
            col, op = "#000", 0.14
        ic.line(fx1, y, fx1 + dx, y + dy, stroke=col, stroke_opacity=op, stroke_width=0.8)
    # the top: today's sheet
    top = [(fx0, fy0), (fx0 + dx, fy0 + dy), (fx1 + dx, fy0 + dy), (fx1, fy0)]
    ic.path(_pts(top), fill=ic.lin([(0, "#FFFFFF"), (1, "#EDEBE6")], 0, 0, 1, 1))
    # a black pen lying across it
    ic.path("M96 76L176 58", stroke="#000", stroke_opacity=0.18, stroke_width=8, stroke_linecap="round",
            transform="translate(2 4)")
    ic.path("M96 76L176 58", stroke=ic.lin([(0, "#55575C"), (1, "#0E0E10")], 0, 0, 0, 1), stroke_width=7,
            stroke_linecap="round")
    ic.path("M96 76L88 78", stroke="#C9CDD3", stroke_width=3, stroke_linecap="round")
    ic.path("M100 73.5L170 57.8", stroke="#fff", stroke_opacity=0.35, stroke_width=1.2, stroke_linecap="round")
    ic.path(f"M{fx0 + 1} {fy0}L{fx0 + dx} {fy0 + dy + 1}H{fx1 + dx - 1}", fill="none", stroke="#fff",
            stroke_width=1.5, stroke_opacity=0.9)
    # the front: white sheets over black, the N printed across them
    ic.rect(fx0, fy0, fx1 - fx0, fy1 - fy0, fill=ic.lin([(0, "#FBFAF7"), (1, "#E4E1DA")], 0, 0, 1, 1))
    ic.rect(fx0, fy1 - 40, fx1 - fx0, 40, fill=ic.lin([(0, "#2A2A2C"), (1, "#121214")]))
    for i in range(1, 26):
        y = fy0 + i * 4.4
        dark = y > fy1 - 40
        ic.line(fx0, y, fx1, y, stroke="#fff" if dark else "#000", stroke_opacity=0.08 if dark else 0.07,
                stroke_width=0.8)
    ic.line(fx0 + 0.75, fy0, fx0 + 0.75, fy1, stroke="#fff", stroke_width=1.5, stroke_opacity=0.8)
    ic.line(fx0, fy0, fx1, fy0, stroke="#000", stroke_opacity=0.12)
    _notion_n(ic, 76, 100, 70, "#111111")
    ic.text("NOTION", (fx0 + fx1) / 2, 194, 9, font="sans-bold", anchor="middle", spacing=3, fill="#FFFFFF",
            opacity=0.85)


@small("notion")
def notion16(ic):
    tile(ic, "#77746E", "#34322E")
    ic.path("M3 5.5L5.5 3H14L11.5 5.5z", fill="#FFFFFF")
    ic.path("M11.5 5.5L14 3V11.5L11.5 14z", fill="#B3AFA6")
    ic.rect(3, 5.5, 8.5, 8.5, fill="#F4F2EE")
    ic.rect(3, 12.4, 8.5, 1.6, fill="#1C1C1E")
    ic.rect(3.9, 6.3, 6.7, 5.6, rx=0.8, fill="#fff", stroke="#111", stroke_width=0.9)
    ic.path("M5.4 10.6V7.6L9.1 10.6V7.6", fill="none", stroke="#111", stroke_width=1.1)


# --- Standard Notes: a gum-top notepad, blue binding and index tabs ---------

SN = "#086DD6"


@icon("standard-notes", kind="app", title="Standard Notes",
      names=["appimagekit-standard-notes", "notes", "org.standardnotes.standardnotes", "standard-notes"])
def standard_notes(ic):
    tile(ic, "#3D5878", "#1A2A40")
    shadow(ic, 126, 214, 90, 12)
    with ic.g(transform="rotate(-4 128 128)"):
        # the card back and the sheets under the top one
        ic.rect(52, 34, 148, 182, rx=6, fill=paper(ic, "kraft-dark"))
        for i, c in ((3, "#CFC9BD"), (2, "#DCD7CC"), (1, "#E8E4DB")):
            ic.rect(54, 46, 140, 164 + i * 1.6, rx=3, fill=c)
        # the index tabs on the right, out from between the sheets
        for i, (y, c) in enumerate(((70, "#3A93F0"), (106, SN), (142, "#0752A6"))):
            ic.rect(186, y + 2, 22, 28, rx=5, fill="#000", opacity=0.2)
            ic.rect(184, y, 22, 28, rx=5, fill=ic.lin([(0, c), (1, "#043E80")], 0, 0, 1, 1))
            ic.line(200, y + 6, 200, y + 22, stroke="#fff", stroke_opacity=0.6, stroke_width=2,
                    stroke_linecap="round")
        # the top sheet, ruled, a note on it
        ic.rect(54, 46, 140, 164, rx=3, fill=paper(ic, "white"))
        for i in range(10):
            ic.line(62, 92 + i * 11, 186, 92 + i * 11, stroke="#7FA7D9", stroke_opacity=0.45, stroke_width=0.8)
        ic.text("Private notes", 64, 87, 15, font="sans-semibold", fill="#1B2B40")
        ic.text("Passport no. in safe", 64, 100, 12, font="hand", fill="#2A3A55")
        ic.text("Wi-Fi: blue heron 42", 64, 111, 12, font="hand", fill="#2A3A55")
        ic.text("Call Dr. Ito, Tue", 64, 122, 12, font="hand", fill="#2A3A55")
        # the stamp: the blue mark in a ring
        with ic.g(transform="rotate(-10 160 168)", opacity=0.85):
            ic.circle(160, 168, 22, fill="none", stroke=SN, stroke_width=2.4)
            ic.rect(147, 155, 26, 26, rx=7, fill=SN)
            for j, w in enumerate((16, 12, 16)):
                ic.rect(152, 161 + j * 5.5, w, 2.6, rx=1.3, fill="#fff")
        # the gum binding along the top, blue, the name on it
        ic.rect(50, 30, 152, 24, rx=4, fill="#000", opacity=0.25, transform="translate(0 2)")
        ic.rect(50, 30, 152, 24, rx=4, fill=ic.lin([(0, "#3A93F0"), (1, "#0552A6")]))
        ic.line(54, 31.5, 198, 31.5, stroke="#fff", stroke_opacity=0.45, stroke_width=1.5)
        ic.text("STANDARD NOTES", 126, 46, 9, font="sans-bold", anchor="middle", spacing=2.2, fill="#fff")


@small("standard-notes")
def standard_notes16(ic):
    tile(ic, "#3D5878", "#1A2A40")
    ic.rect(12, 5, 2.4, 2.6, rx=0.6, fill="#3A93F0")
    ic.rect(12, 8.6, 2.4, 2.6, rx=0.6, fill="#0752A6")
    ic.rect(3, 3, 9.6, 11, rx=0.6, fill="#FFFFFF")
    ic.rect(2.6, 2, 10.4, 2.6, rx=0.6, fill=SN)
    for y in (6.6, 8.6, 10.6):
        ic.rect(4.4, y, 6.6, 0.8, fill="#7FA7D9")


# --- Zettlr: a card index box, green enamel, cards and tabs standing --------

@icon("zettlr", kind="app", title="Zettlr", names=["Zettlr", "appimagekit-zettlr", "com.zettlr.Zettlr", "zettlr"])
def zettlr(ic):
    tile(ic, "#3A5160", "#17242E")
    shadow(ic, 128, 214, 98, 12)
    # the box's inside: back wall and the far side
    ic.path("M44 112L58 92H198L212 112z", fill="#0C5A3E")
    ic.rect(58, 80, 140, 32, fill=ic.lin([(0, "#147A54"), (1, "#0C5A3E")]))
    ic.line(58, 80.75, 198, 80.75, stroke="#7FF0C0", stroke_opacity=0.5, stroke_width=1.5)
    # the cards, back to front, each a tab
    cards = [(56, 140, "#E6A23C", None), (66, 72, "#1CB27E", "Z"), (76, 160, "#E25A47", None),
             (86, 100, "#3A93F0", "17a"), (96, 58, "#B9B2A3", None)]
    for i, (y, tx, tc, label) in enumerate(cards):
        x0 = 52 + i * 2
        w = 152 - i * 4
        ic.rect(x0, y + 2, w, 90, rx=3, fill="#000", opacity=0.18)
        ic.rect(x0, y, w, 90, rx=3, fill=paper(ic, "cream"))
        ic.path(f"M{tx} {y + 1}V{y - 12}a4 4 0 0 1 4-4h{30}a4 4 0 0 1 4 4V{y + 1}z", fill=tc)
        if label == "Z":
            ic.text("Z", tx + 19, y - 1, 14, font="sans-bold", anchor="middle", fill="#fff")
        elif label:
            ic.text(label, tx + 19, y - 1.5, 9, font="mono-semibold", anchor="middle", fill="#fff")
        ic.line(x0 + 1, y + 0.75, x0 + w - 1, y + 0.75, stroke="#fff", stroke_opacity=0.9)
        if i == len(cards) - 1:
            ic.text("202610301142", x0 + 8, y + 14, 7, font="mono-semibold", fill="#7A7468")
            ic.text("#idea", x0 + w - 8, y + 15, 13, font="hand", anchor="end", fill="#1F3A30")
    # the front of the box, green enamel, a brass label holder and pull
    ic.path("M36 120H220L214 206a8 8 0 0 1-8 7H50a8 8 0 0 1-8-7z",
            fill=ic.lin([(0, "#3CCB93"), (0.5, "#1CB27E"), (1, "#0E7A54")]))
    ic.path("M36 120H220L219 132H37z", fill="#fff", opacity=0.14)
    ic.line(37, 120.75, 219, 120.75, stroke="#B8FFE0", stroke_width=1.5, stroke_opacity=0.8)
    ic.line(48, 206, 208, 206, stroke="#000", stroke_opacity=0.2, stroke_width=2)
    ic.rect(90, 138, 76, 34, rx=3, fill=brass(ic))
    ic.rect(95, 143, 66, 24, rx=1.5, fill=paper(ic, "white"))
    ic.text("Zettelkasten", 128, 160, 14, font="hand", anchor="middle", fill="#1F3A30")
    ic.path("M110 182h36v8a6 6 0 0 1-6 6h-24a6 6 0 0 1-6-6z", fill="#0B4A33", opacity=0.6, transform="translate(1 2)")
    ic.path("M110 182h36v8a6 6 0 0 1-6 6h-24a6 6 0 0 1-6-6z", fill=brass(ic))
    ic.circle(96, 155, 2, fill="#7E5A20")
    ic.circle(160, 155, 2, fill="#7E5A20")


@small("zettlr")
def zettlr16(ic):
    tile(ic, "#3A5160", "#17242E")
    ic.rect(3.5, 3.4, 9, 7, rx=0.4, fill="#F4EEE2")
    ic.rect(5, 2.2, 3, 1.6, rx=0.4, fill="#1CB27E")
    ic.rect(4.5, 5, 9, 6, rx=0.4, fill="#FCF8EF")
    ic.rect(9, 3.8, 3, 1.6, rx=0.4, fill="#E25A47")
    ic.path("M2 8.5H14L13.5 13.5H2.5z", fill="#1CB27E")
    ic.rect(6, 9.6, 4, 2, rx=0.3, fill="#E9C77A")


# --- Typora: a typewriter key, its T, on a typed page ------------------------

@icon("typora", kind="app", title="Typora", names=["io.typora.Typora", "typora"])
def typora(ic):
    tile(ic, "#6E4B36", "#33200F")
    shadow(ic, 128, 214, 84, 11)
    # the typed page behind
    with ic.g(transform="rotate(-5 128 80)"):
        ic.rect(48, 22, 160, 110, rx=2, fill="#000", opacity=0.25, transform="translate(3 4)")
        ic.rect(48, 22, 160, 110, rx=2, fill=paper(ic, "cream"))
        ic.text("# Typora", 60, 44, 13, font="mono-semibold", fill="#2A2622")
        ic.text("What you see is", 60, 60, 9.5, font="mono", fill="#4E4A44")
        ic.text("what you mean.", 60, 72, 9.5, font="mono", fill="#4E4A44")
    cx, cy, rx, ry, h = 128, 116, 78, 46, 26
    # the stem down to the lever, and the lever's slot
    ic.rect(cx - 9, cy + 20, 18, 66, fill=steel(ic))
    ic.rect(cx - 50, 196, 100, 12, rx=6, fill=graphite(ic))
    ic.rect(cx - 50, 196, 100, 3, rx=1.5, fill="#fff", opacity=0.15)
    ic.rect(cx - 9, 190, 18, 8, fill="#000", opacity=0.35)
    # the chrome ring: its side, then its rim
    ic.path(f"M{cx - rx - 6} {cy}V{cy + h}A{rx + 6} {ry + 4} 0 0 0 {cx + rx + 6} {cy + h}V{cy}z",
            fill=ic.lin([(0, "#5D636B"), (0.25, "#E2E6EA"), (0.55, "#8A9099"), (1, "#3E4248")], 0, 0, 1, 0))
    ic.ellipse(cx, cy + h, rx + 6, ry + 4, fill="none", stroke="#000", stroke_opacity=0.25, stroke_width=1)
    ic.ellipse(cx, cy, rx + 6, ry + 4, fill=ic.lin([(0, "#F2F4F6"), (0.5, "#A9AFB7"), (1, "#5D636B")], 0, 0, 1, 1))
    # the black glass top and its letter
    ic.ellipse(cx, cy + 2, rx, ry, fill="#000", opacity=0.4)
    ic.ellipse(cx, cy, rx, ry, fill=ic.rad([(0, "#3A3A40"), (0.7, "#151518"), (1, "#060607")], cx=0.4, cy=0.35,
                                           r=0.75))
    with ic.g(transform=f"translate({cx} {cy}) scale(1 {ry / rx:.3f})"):
        ic.path("M-30 -42H30V-20H22L18 -28H8V36L18 40V46H-18V40L-8 36V-28H-18L-22 -20H-30z", fill="#000",
                opacity=0.5, transform="translate(1.5 2)")
        ic.path("M-30 -42H30V-20H22L18 -28H8V36L18 40V46H-18V40L-8 36V-28H-18L-22 -20H-30z", fill="#F7F5EF")
    ic.path(f"M{cx - rx + 10} {cy - 12}A{rx} {ry} 0 0 1 {cx + 10} {cy - ry + 1}"
            f"A{rx - 6} {ry - 6} 0 0 0 {cx - rx + 10} {cy - 12}z", fill="#fff", opacity=0.35)
    ic.ellipse(cx, cy, rx, ry, fill=glare(ic, 0.8))


@small("typora")
def typora16(ic):
    tile(ic, "#6E4B36", "#33200F")
    ic.rect(7, 9, 2, 4, fill="#9AA1A9")
    ic.rect(4, 12.6, 8, 1.4, rx=0.7, fill="#2A2C30")
    ic.path("M1.6 6.8V8.6A6.4 4 0 0 0 14.4 8.6V6.8z", fill="#8A9099")
    ic.ellipse(8, 6.8, 6.4, 4, fill="#D4D8DD")
    ic.ellipse(8, 6.8, 5.4, 3.3, fill="#111113")
    ic.path("M5.6 4.8H10.4M8 4.8V9", fill="none", stroke="#F7F5EF", stroke_width=1.4)


# --- Mark Text: a page of Markdown and the stamp that printed M-down on it ---

def _md_mark(ic, x, y, w, h, colour, sw):
    ic.rect(x, y, w, h, rx=h * 0.18, fill="none", stroke=colour, stroke_width=sw)
    p = w / 10
    ic.path(f"M{x + p * 1.4} {y + h * 0.76}V{y + h * 0.26}L{x + p * 2.9} {y + h * 0.5}L{x + p * 4.4} {y + h * 0.26}"
            f"V{y + h * 0.76}", fill="none", stroke=colour, stroke_width=sw * 1.3, stroke_linejoin="round",
            stroke_linecap="round")
    ic.line(x + p * 7.2, y + h * 0.24, x + p * 7.2, y + h * 0.56, stroke=colour, stroke_width=sw * 1.3,
            stroke_linecap="round")
    ic.path(f"M{x + p * 5.8} {y + h * 0.5}H{x + p * 8.6}L{x + p * 7.2} {y + h * 0.8}z", fill=colour,
            stroke=colour, stroke_width=sw * 0.6, stroke_linejoin="round")


@icon("marktext", kind="app", title="Mark Text", names=["com.github.marktext.marktext", "marktext"])
def marktext(ic):
    tile(ic, "#4D4F8E", "#22244F")
    shadow(ic, 120, 214, 98, 12)
    ink = "#1F3C88"
    with ic.g(transform="rotate(-6 110 120)"):
        ic.rect(36, 30, 140, 180, rx=3, fill="#000", opacity=0.25, transform="translate(3 4)")
        ic.rect(36, 30, 140, 180, rx=3, fill=paper(ic, "white"))
        ic.line(37, 30.75, 175, 30.75, stroke="#fff", stroke_width=1.5)
        ic.text("# Mark Text", 48, 56, 13, font="mono-semibold", fill="#24292F")
        ic.text("- [x] draft", 48, 76, 9.5, font="mono", fill="#57606A")
        ic.text("- [ ] tables", 48, 90, 9.5, font="mono", fill="#57606A")
        ic.text("**bold** _it_", 48, 106, 9.5, font="mono", fill="#57606A")
        ic.rect(48, 116, 3, 16, fill="#B0B7C0")
        ic.text("> a quote", 56, 128, 9.5, font="mono", fill="#8A929C")
        # the impression, a little uneven
        with ic.g(transform="rotate(-8 92 172)", opacity=0.82):
            _md_mark(ic, 56, 150, 74, 42, ink, 4)
    # the stamp, standing to the right: rubber, wooden block, knob
    sx = 190
    ic.rect(sx - 34, 182, 68, 8, rx=2, fill="#1B1B1E")
    ic.rect(sx - 32, 188, 64, 4, rx=1, fill=ink, opacity=0.9)
    ic.rect(sx - 36, 150, 72, 34, rx=4, fill=wood(ic, "#D9A06A", "#8A5428"))
    ic.line(sx - 34, 151.5, sx + 34, 151.5, stroke="#FFE3C0", stroke_opacity=0.7, stroke_width=1.5)
    for k in range(3):
        ic.path(f"M{sx - 32} {160 + k * 8}q30 {-4 + k * 2} 64 0", fill="none", stroke="#6A3C18",
                stroke_opacity=0.25)
    # the stamp's face, printed on its block
    ic.rect(sx - 22, 158, 44, 18, rx=2, fill="#fff", opacity=0.85)
    _md_mark(ic, sx - 18, 160.5, 36, 13, ink, 1.6)
    ic.path(f"M{sx - 9} 150V112h18v38z", fill=wood(ic, "#C48A55", "#6E3E18"))
    ic.ellipse(sx, 98, 24, 20, fill=wood(ic, "#E0A870", "#7A4A22"))
    ic.ellipse(sx - 7, 90, 9, 6, fill="#fff", opacity=0.35, transform=f"rotate(-25 {sx - 7} 90)")


@small("marktext")
def marktext16(ic):
    tile(ic, "#4D4F8E", "#22244F")
    ic.rect(2, 2, 9, 12, rx=0.5, fill="#FFFFFF", transform="rotate(-6 6.5 8)")
    ic.rect(3, 9, 7, 3.8, rx=0.6, fill="none", stroke="#1F3C88", stroke_width=0.8, transform="rotate(-8 6.5 11)")
    ic.path("M4 12V10L5.2 11.1L6.4 10V12", fill="none", stroke="#1F3C88", stroke_width=0.7,
            transform="rotate(-8 6.5 11)")
    ic.rect(10.5, 8.4, 4.4, 3, rx=0.4, fill="#B47A48")
    ic.rect(12, 6, 1.4, 2.6, fill="#8A5428")
    ic.circle(12.7, 5.2, 1.6, fill="#D9A06A")


# --- Xournal++: a wire-bound journal, a lecture note, a stylus on it --------

def _stylus(ic, x, y, deg, length, body, band, tip="#1E2024"):
    """A stylus lying from its tip at (x, y) at deg, length px long."""
    with ic.g(transform=f"translate({x} {y}) rotate({deg})"):
        ic.path(f"M2 6H{length}V18H2z", fill="#000", opacity=0.25)
        ic.path("M0 0L16 -5V5z", fill=tip)
        ic.rect(16, -6, length - 16, 12, rx=6, fill=body)
        ic.rect(16, -6, 8, 12, fill="#2A2C30")
        ic.rect(length - 46, -6, 8, 12, fill=band)
        ic.rect(20, -4.5, length - 26, 2.4, rx=1.2, fill="#fff", opacity=0.35)


@icon("xournalpp", kind="app", title="Xournal++", names=["com.github.xournalpp.xournalpp", "xournal", "xournalpp"])
def xournalpp(ic):
    tile(ic, "#7E3A4A", "#3A1520")
    shadow(ic, 128, 214, 96, 12)
    # the cover behind and the page
    ic.rect(38, 38, 180, 176, rx=6, fill=ic.lin([(0, "#2B4A7E"), (1, "#152846")], 0, 0, 1, 1))
    ic.rect(40, 40, 172, 168, rx=3, fill=paper(ic, "white"))
    for i in range(12):
        ic.line(40, 76 + i * 11, 212, 76 + i * 11, stroke="#6E9BD6", stroke_opacity=0.5, stroke_width=0.8)
    ic.line(66, 50, 66, 208, stroke="#E25A47", stroke_opacity=0.7, stroke_width=1)
    hand = dict(font="hand", fill="#1F3C88")
    ic.text("Lecture 7: curves", 72, 72, 16, **hand)
    ic.text("f(x) = x² - 4", 72, 95, 15, **hand)
    # a sketched parabola on axes
    ic.line(80, 168, 160, 168, stroke="#2A2C30", stroke_width=1.4)
    ic.line(120, 108, 120, 192, stroke="#2A2C30", stroke_width=1.4)
    ic.path("M92 116Q120 216 148 116", fill="none", stroke="#E25A47", stroke_width=2.4, stroke_linecap="round")
    ic.text("x", 164, 172, 13, **hand)
    # the wire binding along the top
    for i in range(11):
        x = 54 + i * 15
        ic.circle(x, 48, 2.6, fill="#2A2C30")
        ic.path(f"M{x - 1} 48C{x - 4} 40 {x - 2} 32 {x + 3} 32", fill="none", stroke="#000", stroke_opacity=0.3,
                stroke_width=3.4, transform="translate(1 1)")
        ic.path(f"M{x - 1} 48C{x - 4} 40 {x - 2} 32 {x + 3} 32", fill="none", stroke=steel(ic, False),
                stroke_width=2.6, stroke_linecap="round")
    # the stylus, tip on the curve
    _stylus(ic, 150, 140, -38, 112, ic.lin([(0, "#6A7280"), (0.5, "#3A3F48"), (1, "#1E2024")], 0, 0, 0, 1),
            "#E8672A")


@small("xournalpp")
def xournalpp16(ic):
    tile(ic, "#7E3A4A", "#3A1520")
    ic.rect(2.4, 3, 11.2, 11, rx=0.6, fill="#FFFFFF")
    for y in (6.5, 8.5, 10.5, 12.5):
        ic.line(2.4, y, 13.6, y, stroke="#6E9BD6", stroke_width=0.5)
    ic.line(4, 3, 4, 14, stroke="#E25A47", stroke_width=0.5)
    for x in (4, 6.5, 9, 11.5):
        ic.rect(x - 0.4, 1.8, 0.8, 2.4, rx=0.4, fill="#9AA1A9")
    ic.path("M8.6 10.6L13.8 5.2", stroke="#3A3F48", stroke_width=1.8, stroke_linecap="round")
    ic.path("M8.6 10.6L7.6 11.6", stroke="#1E2024", stroke_width=1, stroke_linecap="round")


# --- Rnote: a tablet, a pen sketch on its dotted canvas, the stylus ----------

@icon("rnote", kind="app", title="Rnote", names=["com.github.flxzt.rnote", "rnote"])
def rnote(ic):
    tile(ic, "#2F6E7C", "#123640")
    shadow(ic, 128, 210, 104, 13)
    ic.rect(24, 52, 208, 154, rx=18, fill="#0A0B0D", transform="translate(2 3)")
    ic.rect(24, 52, 208, 154, rx=18, fill=graphite(ic))
    ic.rect(24.75, 52.75, 206.5, 152.5, rx=17.25, fill="none", stroke="#fff", stroke_opacity=0.18,
            stroke_width=1.5)
    ic.rect(36, 64, 184, 130, rx=6, fill="#FBFAF6")
    dots = ic.define('<pattern id="{id}" width="10" height="10" patternUnits="userSpaceOnUse" x="36" y="64">'
                     '<circle cx="5" cy="5" r=".9" fill="#9AA6B8"/></pattern>', "p")
    ic.rect(36, 64, 184, 130, rx=6, fill=f"url(#{dots})")
    # the toolbar along the top of the canvas
    ic.rect(88, 70, 80, 14, rx=7, fill="#E7EAF0")
    for i, c in enumerate(("#1C71D8", "#E66100", "#2EC27E", "#3D3846")):
        ic.circle(98 + i * 14, 77, 4, fill=c)
    ic.circle(98, 77, 5.6, fill="none", stroke="#1C71D8", stroke_width=1)
    # the sketch: a loop of blue, an orange wave, a shape
    ic.path("M54 150C60 112 104 104 112 132S82 176 104 168S150 116 168 132", fill="none", stroke="#1C71D8",
            stroke_width=4.5, stroke_linecap="round", stroke_linejoin="round")
    ic.path("M56 178Q78 164 100 178T144 178", fill="none", stroke="#E66100", stroke_width=3.5,
            stroke_linecap="round")
    ic.rect(156, 96, 40, 28, rx=4, fill="#2EC27E", opacity=0.3, stroke="#26A269", stroke_width=2,
            transform="rotate(8 176 110)")
    ic.path("M36 70a6 6 0 0 1 6-6h80L60 194H42a6 6 0 0 1-6-6z", fill=glare(ic, 0.6))
    ic.circle(226, 129, 2, fill="#2A2C30")
    # the stylus, its tip where the blue line ends
    _stylus(ic, 168, 132, -54, 104, ic.lin([(0, "#F4F5F7"), (0.6, "#C9CDD3"), (1, "#8A9099")], 0, 0, 0, 1),
            "#1C71D8", tip="#3D3846")


@small("rnote")
def rnote16(ic):
    tile(ic, "#2F6E7C", "#123640")
    ic.rect(1.5, 3.5, 13, 10, rx=1.4, fill="#2A2C30")
    ic.rect(2.6, 4.6, 10.8, 7.8, rx=0.5, fill="#FBFAF6")
    ic.path("M4 10.5C4.5 7 7.5 6.5 8 8.5S7 11 9.5 9.5", fill="none", stroke="#1C71D8", stroke_width=1,
            stroke_linecap="round")
    ic.path("M9.6 9.4L13.6 3.4", stroke="#D4D8DD", stroke_width=1.6, stroke_linecap="round")


# --- Apostrophe: a fountain pen, an apostrophe of ink falling from it --------

INK = "#2B1F66"


@icon("apostrophe", kind="app", title="Apostrophe", names=["apostrophe", "org.gnome.gitlab.somas.Apostrophe"])
def apostrophe(ic):
    tile(ic, "#5B3F86", "#2A1A4C")
    shadow(ic, 128, 214, 98, 12)
    # the sheet under it
    with ic.g(transform="rotate(5 128 150)"):
        ic.rect(34, 96, 168, 118, rx=2, fill="#000", opacity=0.25, transform="translate(3 4)")
        ic.rect(34, 96, 168, 118, rx=2, fill=paper(ic, "cream"))
        ic.text("Chapter One", 48, 124, 13, font="sans-semibold", fill="#2A2622")
        ic.text("It was the night", 48, 146, 17, font="hand", fill=INK)
        ic.text("before the storm", 48, 168, 17, font="hand", fill=INK)
        ic.text("and nobody", 48, 190, 17, font="hand", fill=INK)
    # the drop, an apostrophe, and the little splash it left
    ic.ellipse(142, 204, 12, 3, fill=INK, opacity=0.35)
    drop = "M150 140c11 0 17 8 15 19c-2 12-12 22-24 26c-2 1-3-1-1-2c7-5 11-10 11-15c-7 0-12-5-12-12c0-9 5-16 11-16z"
    ic.path(drop, fill="#000", opacity=0.25, transform="translate(-12 15) translate(152 162) scale(1.3) translate(-152 -162)")
    ic.path(drop, transform="translate(-14 12) translate(152 162) scale(1.3) translate(-152 -162)", fill=ic.rad([(0, "#5A4AB0"), (0.6, INK), (1, "#140C3A")], cx=0.35, cy=0.3, r=0.75))
    ic.ellipse(131, 162, 5, 7.5, fill="#fff", opacity=0.45, transform="rotate(25 133 162)")
    # the pen, its nib over the drop
    with ic.g(transform="translate(144 140) rotate(-56) scale(0.66)"):
        ic.path("M8 14H200V30H8z", fill="#000", opacity=0.2)
        ic.path("M0 0L30 -9Q35 0 30 9z", fill=ic.lin([(0, "#F6DDA0"), (0.5, "#C99645"), (1, "#7E5A20")], 0, 0, 0, 1))
        ic.line(3, 0, 26, 0, stroke="#5A3E10", stroke_width=1)
        ic.circle(25, 0, 1.8, fill="#5A3E10")
        ic.rect(30, -8, 24, 16, rx=3, fill=ic.lin([(0, "#4A4A52"), (0.4, "#1E1E22"), (1, "#0A0A0C")], 0, 0, 0, 1))
        ic.rect(54, -10.5, 5, 21, fill=brass(ic, 0, 0, 0, 1))
        body = ic.lin([(0, "#A98AE0"), (0.3, "#6A44B0"), (0.75, "#3E2470"), (1, "#24123F")], 0, 0, 0, 1)
        ic.rect(58, -11, 104, 22, rx=4, fill=body)
        ic.rect(162, -12, 4, 24, fill=brass(ic, 0, 0, 0, 1))
        ic.rect(166, -12, 52, 24, rx=10, fill=body)
        ic.rect(176, -16, 40, 5, rx=2.5, fill=brass(ic, 0, 0, 0, 1))
        ic.rect(64, -8, 150, 3, rx=1.5, fill="#fff", opacity=0.35)


@small("apostrophe")
def apostrophe16(ic):
    tile(ic, "#5B3F86", "#2A1A4C")
    ic.rect(2, 8, 11, 6, rx=0.4, fill="#F7F2E7", transform="rotate(5 8 11)")
    ic.path("M9 7.6L14.4 1.8", stroke="#6A44B0", stroke_width=2.6, stroke_linecap="round")
    ic.path("M9 7.6L7.6 9", stroke="#D2A458", stroke_width=1.4, stroke_linecap="round")
    ic.path("M7.4 10c1 0 1.6.8 1.4 1.8c-.2 1.1-1.1 2-2.2 2.4c-.3 0 0-.3 0-.3c.6-.4.9-.8 1-1.3c-.6 0-1.1-.5-1.1-1.1"
            "c0-.8.4-1.5.9-1.5z", fill=INK)


# --- Planner: an open ring planner, today's page and its ticked tasks -------

@icon("planner", kind="app", title="Planner",
      names=["agenda", "calligraplan", "calligraplanner", "calligraplanwork", "com.github.georgekap1an.chores",
             "evolution-tasks", "gnome-planner", "io.github.alainm23.planify", "korganizer", "plan", "planify",
             "planner", "planwork"])
def planner(ic):
    tile(ic, "#B07A2A", "#5E3A0C")
    shadow(ic, 128, 214, 104, 12)
    # the leather cover, open
    ic.rect(22, 44, 212, 166, rx=10, fill=ic.lin([(0, "#3E5E94"), (1, "#1C3460")], 0, 0, 1, 1))
    ic.rect(22.75, 44.75, 210.5, 164.5, rx=9.25, fill="none", stroke="#fff", stroke_opacity=0.2,
            stroke_width=1.5)
    ic.rect(28, 50, 200, 154, rx=6, fill="none", stroke="#9DB4DA", stroke_opacity=0.5, stroke_dasharray="3 2.5")
    # the two pages
    ic.path("M32 54H124V202H38a6 6 0 0 1-6-6z", fill=paper(ic, "cream"))
    ic.path("M132 54H224V196a6 6 0 0 1-6 6H132z", fill=paper(ic, "cream"))
    ic.rect(112, 54, 12, 148, fill=ic.lin([(0, "#000", 0), (1, "#000", 0.12)], 0, 0, 1, 0))
    ic.rect(132, 54, 12, 148, fill=ic.lin([(0, "#000", 0.12), (1, "#000", 0)], 0, 0, 1, 0))
    # the left page: today, the hours
    ic.text("30", 38, 92, 32, font="sans-bold", spacing=-1, fill="#C8372D")
    ic.text("FRIDAY", 76, 76, 8.5, font="mono-semibold", spacing=0.3, fill="#2A2622")
    ic.text("OCTOBER", 76, 88, 7, font="mono", spacing=0.2, fill="#8C887F")
    for i, h in enumerate(("09", "10", "11", "12", "13", "14", "15")):
        y = 112 + i * 13
        ic.line(40, y, 118, y, stroke="#B7AD98", stroke_width=0.8)
        ic.text(h, 40, y - 3, 7, font="mono", fill="#8C887F")
    ic.rect(56, 115, 56, 22, rx=3, fill="#3E5E94", opacity=0.2)
    ic.rect(56, 115, 3, 22, rx=1.5, fill="#3E5E94")
    ic.text("Standup", 62, 129, 13, font="hand", fill="#1C3460")
    ic.text("Lunch", 60, 168, 13, font="hand", fill="#4E4A44")
    # the right page: the tasks
    ic.text("To do", 150, 78, 14, font="sans-semibold", fill="#2A2622")
    tasks = [("Draft", True), ("Train", True), ("Bank", False), ("Plants", False)]
    for i, (t, done) in enumerate(tasks):
        y = 104 + i * 24
        ic.rect(150, y - 11, 13, 13, rx=2, fill="#fff", stroke="#4E4A44", stroke_width=1.4)
        ic.text(t, 170, y, 16, font="hand", fill="#8C887F" if done else "#2A2622")
        if done:
            ic.path(f"M152 {y - 5}l4 5 10-13", fill="none", stroke="#2E8B57", stroke_width=2.8,
                    stroke_linecap="round", stroke_linejoin="round")
    # the rings
    for y in (74, 104, 152, 182):
        ic.ellipse(128, y, 14, 5, fill="none", stroke="#000", stroke_opacity=0.3, stroke_width=4,
                   transform="translate(1 2)")
        ic.ellipse(128, y, 14, 5, fill="none", stroke=steel(ic), stroke_width=3)
        ic.path(f"M116 {y - 2}a14 5 0 0 1 12 -3", fill="none", stroke="#fff", stroke_opacity=0.7)
    # the ribbon marker
    ic.path("M96 190V222l6-6 6 6V190z", fill="#C8372D")
    ic.path("M96 190V222l6-6 6 6V190z", fill=ic.lin([(0, "#fff", 0.2), (1, "#000", 0.2)], 0, 0, 1, 0))


@small("planner")
def planner16(ic):
    tile(ic, "#B07A2A", "#5E3A0C")
    ic.rect(1.4, 3, 13.2, 10.6, rx=1, fill="#2E4A7A")
    ic.rect(2.2, 3.6, 5.6, 9.4, fill="#F7F2E7")
    ic.rect(8.2, 3.6, 5.6, 9.4, fill="#F7F2E7")
    ic.rect(3, 4.6, 3, 2, fill="#C8372D")
    for y in (5.4, 8, 10.6):
        ic.rect(9, y, 1.6, 1.6, fill="none", stroke="#4E4A44", stroke_width=0.5)
    ic.path("M9.2 5.8l.6.8 1.4-1.6M9.2 8.4l.6.8 1.4-1.6", fill="none", stroke="#2E8B57", stroke_width=0.7)
    for y in (4.6, 7.4, 10.4):
        ic.rect(7.2, y, 1.6, 0.8, rx=0.4, fill="#C3C8CE")
