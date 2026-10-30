"""The inua-objects theme, money and words: GnuCash, KMyMoney, HomeBank,
Anki, GoldenDict and Dialect (docs/feat/object-icons.md, Part 2)."""

from lib import brass, glare, icon, leather, paper, polar, shadow, small, tile


def _star(cx, cy, ro, ri, n=5, phase=0):
    pts = []
    for i in range(n * 2):
        pts.append(polar(cx, cy, ro if i % 2 == 0 else ri, phase + i * 180 / n))
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"


def _coin(ic, cx, cy, rx, ry, edge=4, label=None):
    """A gold coin lying on the desk, seen a little from above."""
    ic.ellipse(cx, cy + edge, rx, ry, fill="#7E5A20")
    ic.rect(cx - rx, cy, rx * 2, edge, fill=ic.lin([(0, "#9A6E28"), (0.4, "#E2B860"), (1, "#7E5A20")], 0, 0, 1, 0))
    ic.ellipse(cx, cy, rx, ry, fill=brass(ic))
    ic.ellipse(cx, cy, rx * 0.8, ry * 0.8, fill="none", stroke="#7E5A20", stroke_opacity=0.5, stroke_width=0.8)
    if label:
        with ic.g(transform=f"translate({cx} {cy}) scale(1 {ry / rx:.3f})"):
            ic.text(label, 0, rx * 0.3, rx * 0.9, font="sans-bold", anchor="middle", fill="#7E5A20", opacity=0.8)


# --- GnuCash: an open account ledger, its green G stamped in ----------------

def _ledger_page(dy, side):
    """One page of the open ledger, its top and bottom curving to the gutter."""
    if side < 0:
        return (f"M128 {64 + dy}C100 {52 + dy} 64 {50 + dy} 32 {56 + dy}V{196 + dy}"
                f"C64 {190 + dy} 100 {192 + dy} 128 {202 + dy}Z")
    return (f"M128 {64 + dy}C156 {52 + dy} 192 {50 + dy} 224 {56 + dy}V{196 + dy}"
            f"C192 {190 + dy} 156 {192 + dy} 128 {202 + dy}Z")


@icon("gnucash", kind="app", title="GnuCash", names=[
    "gnucash", "gnucash-icon", "org.gnucash.GnuCash", "org.kde.skrooge", "skrooge"])
def gnucash(ic):
    tile(ic, "#4A7658", "#1A3624")
    shadow(ic, 128, 212, 106, 12)
    # the cloth cover under the pages
    ic.path("M20 62a8 8 0 0 1 8-8h72q20 0 28 8q8-8 28-8h72a8 8 0 0 1 8 8v138a8 8 0 0 1-8 8H28a8 8 0 0 1-8-8z",
            fill=ic.lin([(0, "#2F7A44"), (1, "#123C20")], 0, 0, 1, 1))
    ic.path("M28 54.8h72q20 0 28 8q8-8 28-8h72", fill="none", stroke="#9FE0AE", stroke_opacity=0.35, stroke_width=1.2)
    ic.rect(20, 196, 216, 12, rx=6, fill="#000", opacity=0.18)
    # the pages under today's
    for dy, c in ((6, "#C9C0AA"), (4, "#D9D1BE"), (2, "#E6DFCD")):
        ic.path(_ledger_page(dy, -1), fill=c)
        ic.path(_ledger_page(dy, 1), fill=c)
    ic.path(_ledger_page(0, -1), fill=ic.lin([(0, "#FFFDF6"), (1, "#EDE5D2")], 0, 0, 1, 1))
    ic.path(_ledger_page(0, 1), fill=ic.lin([(0, "#FBF7EC"), (1, "#E4DBC6")], 0, 0, 1, 1))
    pages = ic.clip(f'<path d="{_ledger_page(0, -1)}"/><path d="{_ledger_page(0, 1)}"/>')
    with ic.g(clip_path=pages):
        for y in range(82, 192, 10):
            ic.line(30, y, 226, y, stroke="#7FA6C9", stroke_opacity=0.55, stroke_width=0.8)
        for x in (54, 172, 174.5):
            ic.line(x, 60, x, 204, stroke="#D0473A", stroke_opacity=0.55, stroke_width=0.8)
        ic.line(30, 82, 226, 82, stroke="#D0473A", stroke_opacity=0.6, stroke_width=1)
        # the gutter
        ic.rect(108, 40, 40, 170, fill=ic.lin([(0, "#000", 0), (0.5, "#000", 0.22), (1, "#000", 0)], 0, 0, 1, 0))
    ink, red = "#2A3A30", "#B8362A"
    ic.text("Checking", 38, 76, 9.5, font="sans-semibold", fill="#1E5A30")
    ic.text("Oct", 216, 76, 7, font="mono", anchor="end", fill="#8C887F")
    rows = [("Salary", "2,840.00"), ("Rent", "-1,150.00"), ("Groceries", "-84.20"), ("Power", "-61.75"),
            ("Transfer", "300.00")]
    for i, (what, amount) in enumerate(rows):
        y = 90 + i * 10
        ic.text(what, 58, y, 7, fill=ink)
        ic.text("R" if i < 3 else "c", 163, y, 6, font="mono", anchor="middle", fill="#8C887F")
        ic.text(amount, 216, y, 6.4, font="mono", anchor="end", fill=red if amount[0] == "-" else ink)
    ic.line(176, 134, 217, 134, stroke=ink, stroke_width=0.7)
    ic.line(176, 136.4, 217, 136.4, stroke=ink, stroke_width=0.7)
    ic.text("1,844.05", 216, 150, 7.5, font="mono-semibold", anchor="end", fill="#1E5A30")
    # the ribbon, out of the gutter and over the foot
    rib = "M122 64 L130 64 L124 216 L119 211 L114 216 Z"
    ic.path(rib, fill="#000", opacity=0.15, transform="translate(2 2)")
    ic.path(rib, fill=ic.lin([(0, "#F2C45C"), (1, "#B8841E")], 0, 0, 1, 0))
    # GnuCash's green G, an enamel stamp pressed on the left page
    cx, cy = 80, 166
    ic.circle(cx + 2, cy + 3, 25, fill="#000", opacity=0.2)
    ic.circle(cx, cy, 25, fill=ic.rad([(0, "#6FD27A"), (0.6, "#2E9A44"), (1, "#14602A")], cx=0.38, cy=0.32, r=0.75))
    ic.circle(cx, cy, 21, fill="none", stroke="#E9F8EA", stroke_opacity=0.85, stroke_width=1.6)
    ic.text("G", cx + 0.9, cy + 12.4, 34, font="sans-bold", anchor="middle", fill="#0E4A1E", opacity=0.6)
    ic.text("G", cx, cy + 11.4, 34, font="sans-bold", anchor="middle", fill="#FFFFFF")
    ic.ellipse(cx - 10, cy - 13, 9, 4, fill="#fff", opacity=0.35, transform=f"rotate(-30 {cx - 10} {cy - 13})")


@small("gnucash")
def gnucash16(ic):
    tile(ic, "#4A7658", "#1A3624")
    ic.rect(1.5, 3.5, 13, 10, rx=1, fill="#1F6A34")
    ic.path("M8 4.5 Q5 3.5 2.3 4V12.5Q5 12 8 13z", fill="#FBF7EC")
    ic.path("M8 4.5 Q11 3.5 13.7 4V12.5Q11 12 8 13z", fill="#E9E2D0")
    for y in (6.5, 8.5, 10.5):
        ic.line(9, y, 13, y, stroke="#7FA6C9", stroke_width=0.6)
    ic.circle(5, 8.5, 2.6, fill="#2E9A44")
    ic.path("M6.2 7.6 A1.5 1.5 0 1 0 6.4 9 H5.2", fill="none", stroke="#fff", stroke_width=0.8)


# --- KMyMoney: a leather coin purse on a kiss lock, coins by it --------------

@icon("kmymoney", kind="app", title="KMyMoney", names=["kmymoney", "org.kde.kmymoney"])
def kmymoney(ic):
    tile(ic, "#3A6F8C", "#15344A")
    shadow(ic, 124, 210, 100, 12)
    body = "M60 104 Q128 70 196 104 C218 134 220 172 206 198 Q128 216 50 198 C36 172 38 134 60 104 Z"
    # a folded note, put in in a hurry
    with ic.g(transform="rotate(-14 150 80)"):
        ic.rect(118, 50, 74, 60, rx=2, fill=ic.lin([(0, "#BFE0B0"), (1, "#7FB27A")], 0, 0, 1, 1))
        ic.rect(122, 54, 66, 52, rx=1, fill="none", stroke="#3E7A40", stroke_opacity=0.6, stroke_width=1)
        ic.circle(170, 70, 9, fill="none", stroke="#3E7A40", stroke_opacity=0.6, stroke_width=1.2)
        ic.text("20", 130, 70, 11, font="sans-bold", fill="#2E6A34")
        ic.line(118, 51, 192, 51, stroke="#fff", stroke_opacity=0.6)
    ic.path(body, fill="#000", opacity=0.2, transform="translate(2 3)")
    ic.path(body, fill=leather(ic, "#E8A05C", "#8A4416"))
    purse = ic.clip(f'<path d="{body}"/>')
    with ic.g(clip_path=purse):
        ic.ellipse(86, 118, 46, 24, fill="#fff", opacity=0.14, transform="rotate(-18 86 118)")
        ic.path("M40 186 Q128 204 220 186 V220 H40z", fill="#000", opacity=0.16)
        # the soft folds of the leather
        ic.path("M74 196 Q86 160 82 124", fill="none", stroke="#7A3A12", stroke_opacity=0.25, stroke_width=3)
        ic.path("M182 196 Q172 160 178 124", fill="none", stroke="#7A3A12", stroke_opacity=0.25, stroke_width=3)
    # the stitching under the frame and round the base
    ic.path("M66 114 Q128 84 190 114", fill="none", stroke="#FCE1B8", stroke_opacity=0.75, stroke_width=1.4,
            stroke_dasharray="4 3")
    ic.path("M58 190 Q128 206 198 190", fill="none", stroke="#FCE1B8", stroke_opacity=0.45, stroke_width=1.4,
            stroke_dasharray="4 3")
    # the brass frame and its kiss lock
    ic.path("M58 104 Q128 68 198 104", fill="none", stroke="#5A3A10", stroke_opacity=0.5, stroke_width=8,
            stroke_linecap="round", transform="translate(1 2.5)")
    ic.path("M58 104 Q128 68 198 104", fill="none", stroke=brass(ic, 0, 0, 0, 1), stroke_width=7,
            stroke_linecap="round")
    ic.path("M60 100.5 Q128 66 196 100.5", fill="none", stroke="#FFF2CC", stroke_opacity=0.7, stroke_width=1.2)
    for x in (58, 198):
        ic.circle(x, 104, 5.5, fill=brass(ic))
        ic.circle(x, 104, 1.6, fill="#5A3A10")
    for x in (120.5, 135.5):
        ic.rect(x - 2, 78, 4, 9, fill=brass(ic, 0, 0, 1, 0))
        ic.circle(x + 1, 74, 7.5, fill="#000", opacity=0.25)
        ic.circle(x, 72, 7.5, fill=ic.rad([(0, "#FFF0C0"), (0.45, "#D6A450"), (1, "#7E5A20")], cx=0.35, cy=0.3, r=0.75))
    # KMyMoney's name pressed into the leather
    with ic.g(transform="translate(128 150)"):
        ic.rect(-44, -19, 88, 38, rx=19, fill="#7A3A12", opacity=0.18)
        ic.rect(-44, -19, 88, 38, rx=19, fill="none", stroke="#5A2608", stroke_opacity=0.6, stroke_width=1.8)
        ic.rect(-43, -18, 88, 38, rx=19, fill="none", stroke="#FFD6A8", stroke_opacity=0.45, stroke_width=1)
        ic.text("KMyMoney", 0.8, 5.6, 14, font="sans-bold", anchor="middle", fill="#FFD6A8", opacity=0.5)
        ic.text("KMyMoney", 0, 4.8, 14, font="sans-bold", anchor="middle", fill="#5A2608", opacity=0.85)
    # the coins out on the desk
    for i in range(4):
        _coin(ic, 204, 208 - i * 6, 22, 8, 5, "1" if i == 3 else None)
    _coin(ic, 54, 206, 19, 7, 4, "€")


@small("kmymoney")
def kmymoney16(ic):
    tile(ic, "#3A6F8C", "#15344A")
    ic.rect(8, 2.5, 5, 4.5, rx=0.4, fill="#9FD08E", transform="rotate(-14 10.5 4.7)")
    ic.path("M3.5 6.5 Q8 4 12.5 6.5 C14 8.5 14 11 13 13 Q8 14.2 3 13 C2 11 2 8.5 3.5 6.5z", fill="#D98A46")
    ic.path("M3.3 6.6 Q8 3.8 12.7 6.6", fill="none", stroke="#E9C070", stroke_width=1.1, stroke_linecap="round")
    ic.circle(7.3, 4.2, 1.1, fill="#E9C070")
    ic.circle(8.7, 4.2, 1.1, fill="#E9C070")
    ic.ellipse(12.5, 13.3, 2.4, 1, fill="#E2B04A")


# --- HomeBank: a glazed piggy bank, a coin going in -------------------------

@icon("homebank", kind="app", title="HomeBank", names=["fr.free.Homebank", "homebank"])
def homebank(ic):
    tile(ic, "#7A4466", "#35162C")
    shadow(ic, 128, 210, 96, 11)
    glaze = ic.rad([(0, "#FFC4A0"), (0.55, "#F07A52"), (1, "#A8402A")], cx=0.36, cy=0.3, r=0.8)
    far = "#B4472C"
    # far legs and ear
    for x in (66, 158):
        ic.rect(x, 168, 22, 34, rx=7, fill=far)
    ic.path("M170 88 L188 58 Q196 70 196 96 Z", fill=far)
    # tail
    ic.path("M46 126 c-10 -2 -14 -12 -7 -16 c8 -4 11 7 3 10 c-6 2 -12 -1 -13 -7", fill="none", stroke="#D8603E",
            stroke_width=4, stroke_linecap="round")
    # near legs
    for x in (82, 174):
        ic.rect(x, 172, 24, 36, rx=8, fill=ic.lin([(0, "#F48C62"), (1, "#B04A2C")], 0, 0, 1, 0))
        ic.ellipse(x + 12, 206, 11, 3, fill="#7A2C18", opacity=0.6)
    # the body
    ic.ellipse(128, 134, 86, 60, fill=glaze)
    ic.ellipse(128, 134, 86, 60, fill="none", stroke="#7A2C18", stroke_opacity=0.25, stroke_width=1.5)
    # near ear
    ic.path("M152 92 L172 54 Q186 70 184 98 Z", fill=ic.lin([(0, "#FFB08A"), (1, "#E0683E")], 0, 0, 1, 1))
    ic.path("M160 90 L172 64 Q180 76 178 94 Z", fill="#F59A9A", opacity=0.75)
    # the snout, its face toward us a little
    ic.ellipse(214, 140, 12, 18, fill="#B4472C")
    ic.ellipse(212, 139, 11.5, 17.5, fill=ic.lin([(0, "#FFB898"), (1, "#E07650")], 0, 0, 1, 1))
    ic.ellipse(210, 132, 2.6, 4, fill="#7A2414")
    ic.ellipse(210, 147, 2.6, 4, fill="#7A2414")
    ic.ellipse(188, 112, 4, 5, fill="#2A120C")
    ic.circle(186.8, 110.5, 1.4, fill="#fff")
    ic.ellipse(188, 140, 10, 6.5, fill="#FF8E8E", opacity=0.4)
    # HomeBank, painted on its side: a little house and the name
    paint = "#FFF4E8"
    ic.path("M100 128 L118 112 L136 128 V146 H100 Z", fill=paint)
    ic.rect(113, 132, 10, 14, rx=1, fill="#D8603E")
    ic.rect(127, 113, 5, 9, fill=paint)
    ic.text("HomeBank", 118, 166, 13, font="sans-bold", anchor="middle", fill=paint)
    # the glaze's light
    ic.ellipse(86, 100, 30, 10, fill="#fff", opacity=0.38, transform="rotate(-24 86 100)")
    ic.ellipse(68, 124, 5, 12, fill="#fff", opacity=0.25, transform="rotate(10 68 124)")
    # the slot and the coin half in it
    ic.ellipse(118, 78.5, 24, 5.5, fill="#5A1E10")
    coin = ic.clip('<rect x="80" y="20" width="80" height="78.5"/>')
    with ic.g(clip_path=coin):
        ic.circle(118, 58, 22, fill="#7E5A20")
        ic.circle(116, 56, 22, fill=brass(ic))
        ic.circle(116, 56, 17, fill="none", stroke="#7E5A20", stroke_opacity=0.5, stroke_width=1.2)
        ic.text("€", 116, 66, 26, font="sans-bold", anchor="middle", fill="#7E5A20", opacity=0.75)
        ic.path("M100 44a20 20 0 0 1 14-9 22 22 0 0 0-14 9z", fill="#fff", opacity=0.6)
    ic.path("M95 80 Q118 88 141 80", fill="none", stroke="#FFC8A8", stroke_opacity=0.7, stroke_width=1.6)


@small("homebank")
def homebank16(ic):
    tile(ic, "#7A4466", "#35162C")
    ic.rect(4, 10.5, 2, 3, rx=0.6, fill="#C25236")
    ic.rect(10, 10.5, 2, 3, rx=0.6, fill="#C25236")
    ic.ellipse(7.8, 8.6, 5.6, 4, fill="#F07A52")
    ic.path("M10.5 5.6 L11.8 3.4 L12.6 6.2z", fill="#F07A52")
    ic.ellipse(13.6, 8.8, 1, 1.5, fill="#E06A44")
    ic.circle(11.6, 7.5, 0.5, fill="#2A120C")
    ic.rect(6, 2.5, 3.4, 3.4, rx=1.7, fill="#E2B04A")
    ic.rect(5.2, 4.6, 5, 0.9, rx=0.45, fill="#5A1E10")


# --- Anki: a stack of flash cards, the gold star on the front one ------------

@icon("anki", kind="app", title="Anki", names=["anki", "net.ankiweb.Anki"])
def anki(ic):
    tile(ic, "#4B6CA2", "#1D325C")
    shadow(ic, 128, 212, 98, 12)
    # the cards behind: Anki's blue one, then the answer
    with ic.g(transform="rotate(-11 128 128)"):
        ic.rect(40, 52, 172, 112, rx=6, fill="#000", opacity=0.18, transform="translate(2 3)")
        ic.rect(40, 52, 172, 112, rx=6, fill=ic.lin([(0, "#8DB8EE"), (1, "#3E78C8")], 0, 0, 1, 1))
        ic.rect(52, 62, 148, 92, rx=3, fill="none", stroke="#fff", stroke_opacity=0.4, stroke_width=1.2,
                stroke_dasharray="3 3")
    with ic.g(transform="rotate(-4 128 128)"):
        ic.rect(42, 70, 172, 112, rx=6, fill="#000", opacity=0.16, transform="translate(2 3)")
        ic.rect(42, 70, 172, 112, rx=6, fill=paper(ic, "cream"))
        ic.text("short-lived, fleeting", 56, 92, 15, font="hand", fill="#2463AE")
    # the front card: an index card, the question on it
    with ic.g(transform="rotate(4 128 150)"):
        ic.rect(44, 100, 174, 112, rx=6, fill="#000", opacity=0.2, transform="translate(2 4)")
        ic.rect(44, 100, 174, 112, rx=6, fill=paper(ic, "white"))
        ic.line(45, 100.8, 217, 100.8, stroke="#fff", stroke_width=1.5)
        ic.line(44, 122, 218, 122, stroke="#D0473A", stroke_opacity=0.7, stroke_width=1.2)
        for y in (136, 150, 164, 178):
            ic.line(44, y, 218, y, stroke="#7FA6C9", stroke_opacity=0.4, stroke_width=0.8)
        ic.text("ENGLISH · adj.", 56, 116, 6.2, font="mono", spacing=0.6, fill="#8C887F")
        ic.text("ephemeral", 128, 160, 25, font="sans-semibold", anchor="middle", fill="#1D325C")
        # the four answers along the foot
        for i, (word, c) in enumerate((("Again", "#D0473A"), ("Hard", "#8C887F"), ("Good", "#2E9A44"),
                                       ("Easy", "#2463AE"))):
            x = 58 + i * 38
            ic.rect(x, 184, 32, 14, rx=7, fill=c)
            ic.rect(x + 4, 185, 24, 1.2, rx=0.6, fill="#fff", opacity=0.4)
            ic.text(word, x + 16, 194, 7, font="sans-semibold", anchor="middle", fill="#fff")
    # the star, a gold sticker on the corner
    cx, cy = 196, 92
    ic.path(_star(cx + 2, cy + 3, 26, 11.5), fill="#000", opacity=0.25)
    ic.path(_star(cx, cy, 26, 11.5), fill=ic.lin([(0, "#FFE59A"), (0.5, "#F2B83A"), (1, "#C07E12")], 0, 0, 1, 1))
    ic.path(_star(cx, cy, 26, 11.5), fill="none", stroke="#8A5A0C", stroke_opacity=0.5, stroke_width=1,
            stroke_linejoin="round")
    ic.path(_star(cx, cy, 15, 6.6), fill="none", stroke="#FFF6D6", stroke_opacity=0.6, stroke_width=1)
    ic.path(f"M{cx - 14} {cy - 6}L{cx - 4} {cy - 6}L{cx} {cy - 18}z", fill="#fff", opacity=0.35)


@small("anki")
def anki16(ic):
    tile(ic, "#4B6CA2", "#1D325C")
    ic.rect(2, 3, 10, 7, rx=0.8, fill="#6FA2E4", transform="rotate(-10 7 6.5)")
    ic.rect(3, 6, 11, 7.5, rx=0.8, fill="#FFFFFF", transform="rotate(4 8.5 10)")
    ic.line(4.5, 10.3, 12, 10.8, stroke="#1D325C", stroke_width=1)
    ic.path(_star(11.8, 5, 3.6, 1.6), fill="#F2B83A")


# --- GoldenDict: a thick dictionary, gilt edges, thumb-indexed ----------------

@icon("goldendict", kind="app", title="GoldenDict", names=[
    "aarddict", "accessories-dictionary", "artha", "com.github.lainsce.palaura", "dictionary", "flegita",
    "gnome-dictionary", "goldendict", "io.github.xiaoyifang.goldendict_ng", "org.goldendict.GoldenDict",
    "org.xfce.Dictionary", "palaura", "xfce4-dict"])
def goldendict(ic):
    tile(ic, "#3E4C60", "#161E2A")
    shadow(ic, 136, 212, 88, 11)
    dx, dy = 16, -12
    x0, y0, x1, y1 = 52, 40, 188, 210
    # the back board, then the gilt page block's top and fore edge
    ic.path(f"M{x0 + dx} {y0 + dy}H{x1 + dx}a4 4 0 0 1 4 4V{y1 + dy}L{x1} {y1}V{y0}z", fill="#3A0C0A")
    gilt = ic.lin([(0, "#FFF0B8"), (0.4, "#E8B848"), (1, "#9A6A18")], 0, 0, 1, 1)
    ic.path(f"M{x0 + 4} {y0}L{x0 + 4 + dx - 2} {y0 + dy + 2}H{x1 + dx - 2}L{x1} {y0}z", fill=gilt)
    ic.path(f"M{x1} {y0}L{x1 + dx - 2} {y0 + dy + 2}V{y1 + dy - 4}L{x1} {y1 - 2}z",
            fill=ic.lin([(0, "#F2C860"), (0.5, "#C8962E"), (1, "#7E5410")]))
    for k in range(1, 6):
        f = k / 6
        ic.line(x1 + f * (dx - 2), y0 + f * (dy + 2), x1 + f * (dx - 2), y1 - 2 + f * (dy - 2),
                stroke="#7E5410", stroke_opacity=0.25, stroke_width=0.6)
        ic.line(x0 + 4 + f * (dx - 2), y0 + f * (dy + 2), x1 + f * (dx - 2), y0 + f * (dy + 2),
                stroke="#9A6A18", stroke_opacity=0.3, stroke_width=0.6)
    # the front board, red leather
    ic.rect(x0, y0, x1 - x0, y1 - y0, rx=4, fill=leather(ic, "#B23A30", "#5A1410"))
    ic.line(x0 + 3, y0 + 0.8, x1 - 2, y0 + 0.8, stroke="#FFB8A0", stroke_opacity=0.5, stroke_width=1.5)
    ic.line(x0 + 0.8, y0 + 3, x0 + 0.8, y1 - 3, stroke="#FFB8A0", stroke_opacity=0.3, stroke_width=1.5)
    # the hinge by the spine
    ic.rect(x0 + 10, y0, 3, y1 - y0, fill="#3A0C0A", opacity=0.45)
    ic.line(x0 + 14, y0 + 2, x0 + 14, y1 - 2, stroke="#FFB8A0", stroke_opacity=0.25)
    # gold tooling
    g = brass(ic)
    ic.rect(x0 + 22, y0 + 12, x1 - x0 - 34, y1 - y0 - 24, rx=2, fill="none", stroke=g, stroke_width=1.6)
    ic.rect(x0 + 26, y0 + 16, x1 - x0 - 42, y1 - y0 - 32, rx=1, fill="none", stroke=g, stroke_width=0.7)
    mid = (x0 + 22 + x1 - 12) / 2
    ic.text("DICTIONARY", mid + 0.6, 79.6, 11, font="sans-semibold", anchor="middle", spacing=1.6, fill="#3A0C0A",
            opacity=0.6)
    ic.text("DICTIONARY", mid, 79, 11, font="sans-semibold", anchor="middle", spacing=1.6, fill=g)
    ic.line(mid - 26, 88, mid + 26, 88, stroke=g, stroke_width=0.8)
    # GoldenDict's mark: a gold medallion, an open book in it
    cy = 128
    ic.circle(mid + 1, cy + 1.5, 24, fill="#3A0C0A", opacity=0.5)
    ic.circle(mid, cy, 24, fill=brass(ic))
    ic.circle(mid, cy, 19.5, fill="none", stroke="#7E5A20", stroke_opacity=0.6, stroke_width=1)
    ic.path(f"M{mid} {cy - 4}q-8 -6 -15 -3v15q7 -3 15 3z M{mid} {cy - 4}q8 -6 15 -3v15q-7 -3 -15 3z",
            fill="#FFF4D0", stroke="#7E5A20", stroke_width=1.2, stroke_linejoin="round")
    ic.line(mid, cy - 4, mid, cy + 11, stroke="#7E5A20", stroke_width=1)
    ic.path(f"M{mid - 16} {cy - 14}a20 20 0 0 1 14 -8 22 22 0 0 0 -14 8z", fill="#fff", opacity=0.6)
    ic.text("GoldenDict", mid, 176, 10, font="sans-semibold", anchor="middle", fill=g)
    ic.text("ENGLISH · 2026", mid, 188, 5.4, font="mono", anchor="middle", spacing=1, fill="#E8B848", opacity=0.7)
    # the thumb index cut into the fore edge
    for i, letter in enumerate("AFLRW"):
        y = 62 + i * 30
        ic.path(f"M{x1} {y - 8}a8 8 0 0 0 0 16z", fill="#2A0806")
        ic.rect(x1 - 4.5, y - 4.5, 4.5, 9, fill="#E8B848")
        ic.text(letter, x1 - 2.3, y + 2.2, 6, font="sans-bold", anchor="middle", fill="#2A0806")
        ic.path(f"M{x1} {y + 8}a8 8 0 0 1 -8 -8", fill="none", stroke="#FFB8A0", stroke_opacity=0.35)
    # the ribbon from the foot
    ic.path(f"M144 {y1}h8l1 14l-5 -4l-5 4z", fill=ic.lin([(0, "#F2C45C"), (1, "#B8841E")], 0, 0, 1, 0))


@small("goldendict")
def goldendict16(ic):
    tile(ic, "#3E4C60", "#161E2A")
    ic.path("M4.5 3L6 2H13.5V12.5L12 14z", fill="#3A0C0A")
    ic.path("M12 3L13.5 2V12.5L12 14z", fill="#E8B848")
    ic.rect(3, 3, 9, 11, rx=0.6, fill="#A8322A")
    ic.circle(7.5, 8, 2.2, fill="#E8B848")
    ic.rect(11, 5, 1, 2, fill="#E8B848")
    ic.rect(11, 9, 1, 2, fill="#E8B848")


# --- Dialect: two speech cards, one in each script --------------------------

def _wen(ic, x, y, s, **kw):
    """文 (the font has none): its four strokes in an s px box at (x, y)."""
    def p(u, v):
        return f"{x + u * s:.1f} {y + v * s:.1f}"
    d = (f"M{p(0.46, 0.02)}L{p(0.54, 0.14)}"
         f"M{p(0.08, 0.27)}L{p(0.92, 0.27)}"
         f"M{p(0.72, 0.27)}Q{p(0.6, 0.72)} {p(0.08, 0.96)}"
         f"M{p(0.3, 0.27)}Q{p(0.42, 0.72)} {p(0.94, 0.96)}")
    ic.path(d, fill="none", stroke_width=s * 0.1, stroke_linecap="round", stroke_linejoin="round", **kw)


def _bubble(x, y, w, h, tail):
    """A speech card: a rounded card, its tail at the bottom left or right."""
    r = 16
    if tail < 0:
        t = f"H{x + 40}l-20 22l2-22H{x + r}"
        return (f"M{x + r} {y}H{x + w - r}a{r} {r} 0 0 1 {r} {r}V{y + h - r}a{r} {r} 0 0 1 {-r} {r}"
                f"{t}a{r} {r} 0 0 1 {-r} {-r}V{y + r}a{r} {r} 0 0 1 {r} {-r}z")
    return (f"M{x + r} {y}H{x + w - r}a{r} {r} 0 0 1 {r} {r}V{y + h - r}a{r} {r} 0 0 1 {-r} {r}"
            f"H{x + w - 2}l-2 22l-20 -22H{x + r}a{r} {r} 0 0 1 {-r} {-r}V{y + r}a{r} {r} 0 0 1 {r} {-r}z")


@icon("dialect", kind="app", title="Dialect", names=["app.drey.Dialect", "com.github.gi_lom.dialect", "dialect"])
def dialect(ic):
    tile(ic, "#2E5584", "#10243E")
    shadow(ic, 128, 214, 100, 12)
    back = _bubble(28, 44, 140, 96, -1)
    with ic.g(transform="rotate(-6 98 92)"):
        ic.path(back, fill="#000", opacity=0.22, transform="translate(2 4)")
        ic.path(back, fill="#C9C3B6", transform="translate(0 2.5)")
        ic.path(back, fill=paper(ic, "white"))
        ic.line(44, 44.8, 152, 44.8, stroke="#fff", stroke_width=1.5)
        ic.text("Hello", 98, 100, 32, font="sans-semibold", anchor="middle", fill="#1A3A64")
        ic.text("ENGLISH", 98, 120, 6.5, font="mono", anchor="middle", spacing=1.6, fill="#8C887F")
    front = _bubble(90, 104, 140, 92, 1)
    with ic.g(transform="rotate(5 160 150)"):
        ic.path(front, fill="#000", opacity=0.28, transform="translate(2 4)")
        ic.path(front, fill="#174E98", transform="translate(0 2.5)")
        ic.path(front, fill=ic.lin([(0, "#62A8F4"), (1, "#2A6CCC")], 0, 0, 1, 1))
        ic.line(106, 104.8, 214, 104.8, stroke="#CFE4FF", stroke_opacity=0.8, stroke_width=1.5)
        _wen(ic, 112, 120, 46, stroke="#0E3A78", opacity=0.45, transform="translate(1 1.5)")
        _wen(ic, 112, 120, 46, stroke="#FFFFFF")
        ic.text("Привет", 168, 146, 14, font="sans-semibold", anchor="start", fill="#FFFFFF", opacity=0.92)
        ic.text("CHINESE", 168, 160, 5.6, font="mono", spacing=1.2, fill="#D6E8FF")
        ic.text("RUSSIAN", 168, 168, 5.6, font="mono", spacing=1.2, fill="#D6E8FF", opacity=0.7)
    # the swap button between them
    cx, cy = 58, 182
    ic.circle(cx + 1.5, cy + 3, 19, fill="#000", opacity=0.25)
    ic.circle(cx, cy, 19, fill=ic.lin([(0, "#FFFFFF"), (1, "#D6D2C8")], 0, 0, 1, 1))
    ic.circle(cx, cy, 15, fill=ic.lin([(0, "#3E8EE8"), (1, "#1A5AB4")], 0, 0, 1, 1))
    ar = dict(fill="none", stroke="#fff", stroke_width=2.2, stroke_linecap="round", stroke_linejoin="round")
    ic.path(f"M{cx - 7} {cy - 3.5}H{cx + 7}M{cx + 3} {cy - 7.5}l4 4l-4 4", **ar)
    ic.path(f"M{cx + 7} {cy + 4.5}H{cx - 7}M{cx - 3} {cy + 0.5}l-4 4l4 4", **ar)
    ic.circle(cx, cy, 15, fill=glare(ic, 0.8))


@small("dialect")
def dialect16(ic):
    tile(ic, "#2E5584", "#10243E")
    ic.path("M3 2.5h7a1.5 1.5 0 0 1 1.5 1.5v3.5a1.5 1.5 0 0 1-1.5 1.5H5.5l-2 2v-2H3a1.5 1.5 0 0 1-1.5-1.5V4A1.5 1.5 0 0 1 3 2.5z",
            fill="#FFFFFF")
    ic.rect(3.5, 5, 5, 1.2, rx=0.6, fill="#1A3A64")
    ic.path("M6.5 7h7a1.5 1.5 0 0 1 1.5 1.5V12a1.5 1.5 0 0 1-1.5 1.5H13v2l-2-2H6.5A1.5 1.5 0 0 1 5 12V8.5A1.5 1.5 0 0 1 6.5 7z",
            fill="#3E8EE8")
    ic.path("M8 9.3h4M10 9.3l-1.4 3M10 9.3l1.4 3", fill="none", stroke="#fff", stroke_width=0.8, stroke_linecap="round")
