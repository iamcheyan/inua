"""Soft drawings, money and words: GnuCash, KMyMoney, HomeBank, Anki,
GoldenDict, Dialect. The same objects as drawings/apps_t2_money.py, about
half the detail, no text."""

from lib import bar, polar, soft, soft_shadow, tile, two


def _star(cx, cy, ro, ri, n=5, phase=0):
    pts = [polar(cx, cy, ro if i % 2 == 0 else ri, phase + i * 180 / n) for i in range(n * 2)]
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"


def _coin(ic, cx, cy, rx, ry, edge=5):
    ic.ellipse(cx, cy + edge, rx, ry, fill="#9A6E28")
    ic.rect(cx - rx, cy, rx * 2, edge, fill="#9A6E28")
    ic.ellipse(cx, cy, rx, ry, fill=two(ic, "#F2CC78", "#C8963E"))


def _page(dy, side):
    if side < 0:
        return (f"M128 {64 + dy}C100 {52 + dy} 64 {50 + dy} 32 {56 + dy}V{196 + dy}"
                f"C64 {190 + dy} 100 {192 + dy} 128 {202 + dy}Z")
    return (f"M128 {64 + dy}C156 {52 + dy} 192 {50 + dy} 224 {56 + dy}V{196 + dy}"
            f"C192 {190 + dy} 156 {192 + dy} 128 {202 + dy}Z")


@soft("gnucash")
def gnucash(ic):
    tile(ic, "#4A7658", "#1A3624")
    soft_shadow(ic, 128, 212, 106, 12)
    ic.path("M20 64a10 10 0 0 1 10-10h70q20 0 28 8q8-8 28-8h70a10 10 0 0 1 10 10v134a10 10 0 0 1-10 10H30"
            "a10 10 0 0 1-10-10z", fill=two(ic, "#2F7A44", "#17482A"))
    for side in (-1, 1):
        ic.path(_page(5, side), fill="#D2C9B4")
    ic.path(_page(0, -1), fill=two(ic, "#FFFDF6", "#EDE5D2"))
    ic.path(_page(0, 1), fill=two(ic, "#FBF7EC", "#E4DBC6"))
    # the account: a heading, the entries, the balance
    bar(ic, 40, 70, 52, 8, fill="#1E5A30")
    for i in range(5):
        y = 88 + i * 13
        bar(ic, 46, y, (58, 40, 50, 34, 46)[i], 6, fill="#2A3A30", opacity=0.55)
        w = (44, 52, 30, 30, 38)[i]
        bar(ic, 212 - w, y, w, 6, fill="#B8362A" if i in (1, 2, 3) else "#2A3A30", opacity=0.75)
    ic.rect(170, 154, 42, 3, rx=1.5, fill="#2A3A30")
    bar(ic, 168, 162, 44, 8, fill="#1E5A30")
    # the ribbon
    ic.path("M121 64h10l-6 152l-5-5l-5 5z", fill=two(ic, "#F2C45C", "#C89428"))
    # the green G stamp
    cx, cy = 80, 164
    ic.circle(cx, cy, 26, fill=two(ic, "#4CC060", "#1E7A36"))
    p, q = polar(cx, cy, 12, 48), polar(cx, cy, 12, 92)
    ic.path(f"M{p[0]:.1f} {p[1]:.1f}A12 12 0 1 0 {q[0]:.1f} {q[1]:.1f}H{cx + 1}", fill="none", stroke="#FFFFFF",
            stroke_width=6, stroke_linecap="round", stroke_linejoin="round")


@soft("kmymoney")
def kmymoney(ic):
    tile(ic, "#3A6F8C", "#15344A")
    soft_shadow(ic, 124, 212, 100, 12)
    # a note, put in in a hurry
    with ic.g(transform="rotate(-14 150 80)"):
        ic.rect(118, 50, 74, 60, rx=5, fill=two(ic, "#BFE0B0", "#8CBC84"))
        ic.circle(170, 72, 10, fill="none", stroke="#3E7A40", stroke_opacity=0.6, stroke_width=3)
        bar(ic, 128, 62, 22, 9, fill="#2E6A34", opacity=0.8)
    # the purse
    ic.path("M60 104Q128 70 196 104C218 134 220 172 206 198Q128 216 50 198C36 172 38 134 60 104Z",
            fill=two(ic, "#E8A05C", "#A85A22"))
    ic.path("M58 104Q128 68 198 104", fill="none", stroke=two(ic, "#E2B45E", "#B88433"), stroke_width=9,
            stroke_linecap="round")
    for x in (120.5, 135.5):
        ic.rect(x - 2.5, 76, 5, 10, fill="#B88433")
        ic.circle(x, 72, 8, fill=two(ic, "#F2CC78", "#B88433"))
    # its name pressed in
    ic.rect(84, 131, 88, 38, rx=19, fill="#7A3A12", opacity=0.25)
    bar(ic, 102, 145, 52, 10, fill="#5A2608", opacity=0.7)
    # coins on the desk
    for i in range(4):
        _coin(ic, 204, 208 - i * 7, 22, 8)
    _coin(ic, 54, 206, 19, 7, 4)


@soft("homebank")
def homebank(ic):
    tile(ic, "#7A4466", "#35162C")
    soft_shadow(ic, 128, 212, 96, 11)
    far = "#B4472C"
    for x in (66, 158):
        ic.rect(x, 168, 22, 34, rx=9, fill=far)
    ic.path("M170 88L188 58Q196 70 196 96Z", fill=far, stroke=far, stroke_width=4, stroke_linejoin="round")
    ic.path("M46 126c-10-2-14-12-7-16c8-4 11 7 3 10c-6 2-12-1-13-7", fill="none", stroke="#D8603E",
            stroke_width=6, stroke_linecap="round")
    for x in (82, 174):
        ic.rect(x, 172, 24, 36, rx=10, fill="#D86440")
    ic.ellipse(128, 134, 86, 60, fill=two(ic, "#FFA27A", "#D8603E"))
    ic.path("M152 92L172 54Q186 70 184 98Z", fill="#F59A72", stroke="#F59A72", stroke_width=4, stroke_linejoin="round")
    # the snout and the eye
    ic.ellipse(214, 140, 12, 18, fill="#B4472C")
    ic.ellipse(212, 139, 11.5, 17.5, fill="#F49A78")
    ic.ellipse(210, 132, 3, 4.5, fill="#7A2414")
    ic.ellipse(210, 147, 3, 4.5, fill="#7A2414")
    ic.ellipse(188, 112, 5, 6, fill="#2A120C")
    # HomeBank painted on its side
    paint = "#FFF4E8"
    ic.path("M100 128L118 112L136 128V146H100Z", fill=paint, stroke=paint, stroke_width=3, stroke_linejoin="round")
    ic.rect(113, 132, 10, 14, rx=2, fill="#D8603E")
    bar(ic, 88, 156, 60, 9, fill=paint)
    # the slot, the coin half in it
    ic.ellipse(118, 78.5, 24, 6, fill="#5A1E10")
    with ic.g(clip_path=ic.clip('<rect x="80" y="20" width="80" height="78.5"/>')):
        ic.circle(116, 56, 22, fill=two(ic, "#F2CC78", "#C8963E"))
        ic.circle(116, 56, 15, fill="none", stroke="#9A6E28", stroke_opacity=0.5, stroke_width=3)


@soft("anki")
def anki(ic):
    tile(ic, "#4B6CA2", "#1D325C")
    soft_shadow(ic, 128, 214, 98, 12)
    with ic.g(transform="rotate(-11 128 128)"):
        ic.rect(40, 52, 172, 112, rx=10, fill=two(ic, "#8DB8EE", "#4A82D0"))
    with ic.g(transform="rotate(-4 128 128)"):
        ic.rect(42, 70, 172, 112, rx=10, fill=two(ic, "#FCF9F2", "#E8E0CF"))
        bar(ic, 58, 84, 96, 8, fill="#2463AE", opacity=0.75)
    with ic.g(transform="rotate(4 128 150)"):
        ic.rect(44, 100, 174, 112, rx=10, fill=two(ic, "#FFFFFF", "#ECE8DF"))
        ic.rect(44, 121, 174, 2.5, fill="#D0473A", opacity=0.7)
        bar(ic, 58, 109, 48, 6, fill="#A49E91")
        bar(ic, 74, 144, 108, 16, fill="#1D325C")
        for i, c in enumerate(("#D0473A", "#8C887F", "#2E9A44", "#2463AE")):
            ic.rect(58 + i * 38, 182, 32, 16, rx=8, fill=c)
    cx, cy = 196, 92
    ic.path(_star(cx, cy, 27, 12), fill=two(ic, "#FFDA7A", "#E09A22"), stroke="#F0B440", stroke_width=3,
            stroke_linejoin="round")


@soft("goldendict")
def goldendict(ic):
    tile(ic, "#3E4C60", "#161E2A")
    soft_shadow(ic, 136, 212, 88, 11)
    dx, dy = 16, -12
    x0, y0, x1, y1 = 52, 40, 188, 210
    # the back board and the gilt page block
    ic.path(f"M{x0 + dx} {y0 + dy}H{x1 + dx}a6 6 0 0 1 6 6V{y1 + dy}L{x1} {y1}V{y0}z", fill="#3A0C0A")
    ic.path(f"M{x0 + 4} {y0}L{x0 + 2 + dx} {y0 + dy + 2}H{x1 + dx - 2}L{x1} {y0}z", fill="#F2D27A")
    ic.path(f"M{x1} {y0}L{x1 + dx - 2} {y0 + dy + 2}V{y1 + dy - 4}L{x1} {y1 - 2}z", fill=two(ic, "#E8B848", "#A87A20"))
    # the front board, red leather, gold tooling
    ic.rect(x0, y0, x1 - x0, y1 - y0, rx=8, fill=two(ic, "#B23A30", "#781C16"))
    ic.rect(x0 + 10, y0, 4, y1 - y0, fill="#3A0C0A", opacity=0.4)
    gold = two(ic, "#E2B45E", "#B88433")
    ic.rect(x0 + 22, y0 + 12, x1 - x0 - 34, y1 - y0 - 24, rx=5, fill="none", stroke="#D8A850", stroke_width=2.5)
    mid = (x0 + 22 + x1 - 12) / 2
    bar(ic, mid - 32, 70, 64, 9, fill="#E8B848")
    # the medallion, an open book in it
    cy = 128
    ic.circle(mid, cy, 25, fill=gold)
    ic.path(f"M{mid} {cy - 5}q-9 -6 -16 -3v16q7 -3 16 3z M{mid} {cy - 5}q9 -6 16 -3v16q-7 -3 -16 3z",
            fill="#FFF4D0", stroke="#7E5A20", stroke_width=2, stroke_linejoin="round")
    bar(ic, mid - 28, 170, 56, 8, fill="#E8B848")
    # the thumb index
    for i in range(5):
        y = 62 + i * 30
        ic.path(f"M{x1} {y - 9}a9 9 0 0 0 0 18z", fill="#2A0806")
        ic.rect(x1 - 5, y - 5, 5, 10, rx=1.5, fill="#E8B848")
    ic.path(f"M144 {y1}h9v15l-4.5-4l-4.5 4z", fill=two(ic, "#F2C45C", "#C89428"))


def _wen(ic, x, y, s, **kw):
    """文, as four strokes in an s px box at (x, y)."""
    def p(u, v):
        return f"{x + u * s:.1f} {y + v * s:.1f}"
    ic.path(f"M{p(0.46, 0.02)}L{p(0.54, 0.14)}M{p(0.08, 0.27)}L{p(0.92, 0.27)}"
            f"M{p(0.72, 0.27)}Q{p(0.6, 0.72)} {p(0.08, 0.96)}M{p(0.3, 0.27)}Q{p(0.42, 0.72)} {p(0.94, 0.96)}",
            fill="none", stroke_width=s * 0.13, stroke_linecap="round", stroke_linejoin="round", **kw)


def _bubble(x, y, w, h, tail):
    r = 20
    if tail < 0:
        t = f"H{x + 44}l-20 22l2-22H{x + r}"
        return (f"M{x + r} {y}H{x + w - r}a{r} {r} 0 0 1 {r} {r}V{y + h - r}a{r} {r} 0 0 1 {-r} {r}"
                f"{t}a{r} {r} 0 0 1 {-r} {-r}V{y + r}a{r} {r} 0 0 1 {r} {-r}z")
    return (f"M{x + r} {y}H{x + w - r}a{r} {r} 0 0 1 {r} {r}V{y + h - r}a{r} {r} 0 0 1 {-r} {r}"
            f"H{x + w - 4}l-2 22l-20 -22H{x + r}a{r} {r} 0 0 1 {-r} {-r}V{y + r}a{r} {r} 0 0 1 {r} {-r}z")


@soft("dialect")
def dialect(ic):
    tile(ic, "#2E5584", "#10243E")
    soft_shadow(ic, 128, 214, 100, 12)
    back = _bubble(28, 44, 140, 96, -1)
    with ic.g(transform="rotate(-6 98 92)"):
        ic.path(back, fill="#C9C3B6", transform="translate(0 3)")
        ic.path(back, fill=two(ic, "#FFFFFF", "#ECE8DF"))
        bar(ic, 58, 78, 80, 16, fill="#1A3A64")
        bar(ic, 74, 104, 48, 6, fill="#A49E91")
    front = _bubble(90, 104, 140, 92, 1)
    with ic.g(transform="rotate(5 160 150)"):
        ic.path(front, fill="#174E98", transform="translate(0 3)")
        ic.path(front, fill=two(ic, "#62A8F4", "#2A6CCC"))
        _wen(ic, 110, 120, 48, stroke="#FFFFFF")
        bar(ic, 168, 132, 46, 10, fill="#FFFFFF", opacity=0.9)
        bar(ic, 168, 150, 30, 6, fill="#D6E8FF", opacity=0.8)
    # the swap button
    cx, cy = 58, 182
    ic.circle(cx, cy, 20, fill=two(ic, "#FFFFFF", "#DCD8CE"))
    ic.circle(cx, cy, 15, fill=two(ic, "#3E8EE8", "#1A5AB4"))
    ar = dict(fill="none", stroke="#fff", stroke_width=3, stroke_linecap="round", stroke_linejoin="round")
    ic.path(f"M{cx - 7} {cy - 3.5}H{cx + 7}M{cx + 3} {cy - 7.5}l4 4l-4 4", **ar)
    ic.path(f"M{cx + 7} {cy + 4.5}H{cx - 7}M{cx - 3} {cy + 0.5}l-4 4l4 4", **ar)
