"""Soft drawings of inua's apps, first batch: Calendar, Weather, Viewer,
Video, Screenshot, Settings, Launcher, Assistant. The same objects as
drawings/inua_a.py, about half the detail, no text."""

import math

from lib import bar, mark, polar, soft, soft_shadow, tile, two

INK = "#2A2C30"


def _gear(cx, cy, ro, ri, n, phase=0.0):
    p = 360 / n
    pts = []
    for i in range(n):
        a = phase + i * p
        pts += [polar(cx, cy, ri, a), polar(cx, cy, ro, a + p * 0.14), polar(cx, cy, ro, a + p * 0.46),
                polar(cx, cy, ri, a + p * 0.6)]
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"


@soft("Calendar")
def calendar(ic):
    tile(ic, "#9A4A3A", "#592318")
    soft_shadow(ic, 128, 216, 94, 12)
    ic.rect(40, 40, 176, 176, rx=14, fill=two(ic, "#3A3430", "#1E1A18"))
    ic.rect(48, 62, 160, 144, rx=7, fill="#D9D0BE")
    ic.rect(48, 56, 160, 146, rx=7, fill=two(ic, "#FCF9F2", "#ECE4D3"))
    ic.path("M48 63a7 7 0 0 1 7-7h146a7 7 0 0 1 7 7v33H48z", fill=two(ic, "#E0483A", "#B42A1F"))
    bar(ic, 92, 74, 72, 10, fill="#FFF6EC")
    # 30, as two bold strokes
    num = dict(fill="none", stroke="#24211E", stroke_width=14, stroke_linecap="round", stroke_linejoin="round")
    ic.path("M90 124C95 112 122 110 122 128C122 138 114 142 106 142C116 142 125 148 125 159C125 176 96 178 89 165", **num)
    ic.ellipse(153, 144, 15, 27, **num)
    bar(ic, 108, 186, 40, 7, fill="#B42A1F")
    for x in (70, 94, 162, 186):
        ic.ellipse(x, 62, 5, 3.5, fill="#1A1614")
        ic.path(f"M{x - 4} 62V46a4 4 0 0 1 8 0V62", fill="none", stroke="#C3C8CE", stroke_width=5,
                stroke_linecap="round")


@soft("Weather")
def weather(ic):
    tile(ic, "#4F8FC4", "#22547E")
    cx, cy = 128, 122
    soft_shadow(ic, 128, 218, 86, 11)
    ic.circle(cx, cy, 100, fill=two(ic, "#B47A48", "#6A3E1E"))
    ic.circle(cx, cy, 88, fill=two(ic, "#E2B45E", "#B88433"))
    ic.circle(cx, cy, 77, fill=two(ic, "#FFFDF7", "#EDE5D3"))
    (x0, y0), (x1, y1) = polar(cx, cy, 58, -120), polar(cx, cy, 58, 120)
    ic.path(f"M{x0:.1f} {y0:.1f}A58 58 0 1 1 {x1:.1f} {y1:.1f}", fill="none", stroke=INK, stroke_width=2.5,
            stroke_linecap="round", opacity=0.5)
    for k in range(13):
        big = k % 4 == 0
        ic.rect(cx - (3.5 if big else 2), cy - 72, 7 if big else 4, 16 if big else 10, rx=2,
                fill=INK, transform=f"rotate({-120 + k * 20} {cx} {cy})")
    # RAIN, CHANGE, FAIR
    for a0, a1 in ((-78, -48), (-20, 20), (50, 76)):
        (x0, y0), (x1, y1) = polar(cx, cy, 38, a0), polar(cx, cy, 38, a1)
        ic.path(f"M{x0:.1f} {y0:.1f}A38 38 0 0 1 {x1:.1f} {y1:.1f}", fill="none", stroke="#8C887F", stroke_width=7,
                stroke_linecap="round")
    ic.rect(cx - 2, cy - 70, 4, 70, rx=2, fill="#B98A3C", transform=f"rotate(12 {cx} {cy})")
    with ic.g(transform=f"rotate(30 {cx} {cy})"):
        ic.path(f"M{cx - 4.5} {cy + 22}L{cx} {cy - 68}L{cx + 4.5} {cy + 22}z", fill="#1E2A3E",
                stroke="#1E2A3E", stroke_width=2, stroke_linejoin="round")
    ic.circle(cx, cy, 9, fill=two(ic, "#E2B45E", "#B88433"))


def _photo(ic):
    """The photograph's picture, in the frame x 50..190, y 56..160."""
    ic.rect(50, 56, 140, 70, fill=two(ic, "#86B6DB", "#DCE9EC"))
    ic.circle(160, 76, 8, fill="#FFF5D6")
    ic.path("M50 124L118 64L134 78L148 70L190 108V126H50z", fill="#55687D")
    ic.path("M105 76L118 64L134 78L148 70L160 80L148 84L134 88L122 80L112 87z", fill="#F7FAFC")
    ic.rect(50, 124, 140, 36, fill=two(ic, "#5D88A6", "#2E5570"))


@soft("Viewer")
def viewer(ic):
    tile(ic, "#2E7A78", "#11403F")
    soft_shadow(ic, 120, 210, 98, 12)
    with ic.g(transform="rotate(-5 120 120)"):
        ic.path("M46 46h154v124l-30 30H46a6 6 0 0 1-6-6V52a6 6 0 0 1 6-6z", fill=two(ic, "#FFFFFF", "#ECE8DF"))
        _photo(ic)
        bar(ic, 54, 177, 70, 7, fill="#A49E91")
        ic.path("M200 170L170 200Q176 181 200 170Z", fill="#D8D2C6")
    lx, ly, lr = 116, 96, 34
    ic.circle(lx, ly, lr + 7, fill=two(ic, "#4F535A", "#1E2024"))
    lens = ic.clip(f'<circle cx="{lx}" cy="{ly}" r="{lr}"/>')
    with ic.g(clip_path=lens):
        with ic.g(transform=f"translate({lx} {ly}) scale(1.9) translate(-120 -80) rotate(-5 120 120)"):
            _photo(ic)


def _stripes(ic, x, y, w, h):
    clip = ic.clip(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4"/>')
    with ic.g(clip_path=clip):
        ic.rect(x, y, w, h, fill="#1B1C1F")
        for k in range(-1, int(w / 32) + 2):
            sx = x + k * 32
            ic.poly([(sx, y + h), (sx + 16, y + h), (sx + 16 + h * 0.7, y), (sx + h * 0.7, y)], fill="#F3F1EC")


@soft("Video")
def video(ic):
    tile(ic, "#B43344", "#651420")
    soft_shadow(ic, 128, 216, 98, 12)
    chalk = "#F1EFE8"
    ic.rect(34, 96, 188, 112, rx=12, fill=two(ic, "#3F4349", "#24272B"))
    _stripes(ic, 34, 80, 188, 20)
    rule = dict(stroke=chalk, stroke_opacity=0.45, stroke_width=2.5, stroke_linecap="round")
    ic.line(44, 140, 212, 140, **rule)
    ic.line(44, 176, 212, 176, **rule)
    ic.line(100, 140, 100, 176, **rule)
    ic.line(158, 140, 158, 176, **rule)
    bar(ic, 84, 116, 88, 11, fill=chalk)
    bar(ic, 56, 156, 30, 9, fill=chalk)
    bar(ic, 122, 156, 14, 9, fill=chalk)
    bar(ic, 180, 156, 14, 9, fill=chalk)
    bar(ic, 46, 188, 48, 8, fill=chalk, opacity=0.8)
    bar(ic, 142, 188, 40, 8, fill=chalk, opacity=0.8)
    with ic.g(transform="rotate(-16 38 80)"):
        _stripes(ic, 34, 60, 188, 20)
    ic.circle(40, 80, 8, fill=two(ic, "#D4D8DD", "#8D949C"))
    ic.circle(40, 80, 3, fill="#3A3E44")


@soft("Screenshot")
def screenshot(ic):
    tile(ic, "#B8607A", "#6A2440")
    soft_shadow(ic, 128, 210, 104, 12)
    steel = two(ic, "#D4D8DD", "#9AA1A9")
    ic.rect(50, 66, 30, 22, rx=5, fill=steel)
    ic.rect(150, 60, 44, 28, rx=6, fill=steel)
    ic.rect(200, 72, 14, 16, rx=4, fill=steel)
    ic.rect(26, 82, 204, 108, rx=18, fill=two(ic, "#2E2F33", "#141517"))
    ic.path("M26 100a18 18 0 0 1 18-18h168a18 18 0 0 1 18 18v18H26z", fill=two(ic, "#EEF0F2", "#AEB4BB"))
    ic.rect(38, 91, 30, 18, rx=5, fill="#2A3A46")
    ic.rect(80, 93, 22, 14, rx=4, fill="#F3F1EC")
    ic.rect(186, 91, 28, 18, rx=5, fill="#2A3A46")
    lx, ly = 128, 146
    ic.circle(lx, ly, 54, fill=two(ic, "#E3E6EA", "#8D949C"))
    ic.circle(lx, ly, 47, fill="#26282C")
    ic.circle(lx, ly, 36, fill=two(ic, "#D4D8DD", "#8D949C"))
    ic.circle(lx, ly, 25, fill="#0C0D0F")
    ic.circle(lx, ly, 20, fill=two(ic, "#3C3B6A", "#0A0E1C"))
    ic.circle(lx - 7, ly - 8, 5, fill="#fff", opacity=0.5)


@soft("Settings")
def settings(ic):
    tile(ic, "#66717D", "#333B44")
    soft_shadow(ic, 124, 214, 96, 12)
    hole = "#4A525C"
    ax, ay, bx, by = 102, 142, 170, 76
    dist = math.hypot(bx - ax, ay - by)
    ang = math.degrees(math.atan2(bx - ax, ay - by))
    ra, rb = 56 * dist / 92, 36 * dist / 92
    # the big gear, brass, 14 teeth
    ic.path(_gear(ax, ay, ra + 6, ra - 6, 14, ang - 0.3 * 360 / 14), fill=two(ic, "#E2B45E", "#B88433"))
    ic.circle(ax, ay, 44, fill="#B88433", opacity=0.5)
    for k in range(4):
        hx, hy = polar(ax, ay, 29, 45 + k * 90)
        ic.circle(hx, hy, 8.5, fill=hole)
    ic.circle(ax, ay, 19, fill=two(ic, "#E2B45E", "#C8963F"))
    ic.circle(ax, ay, 10, fill="#1E2024")
    ic.rect(ax - 3, ay - 15, 6, 7, rx=1.5, fill="#1E2024")
    # the small gear, steel, 9 teeth
    ic.path(_gear(bx, by, rb + 6, rb - 6, 9, ang + 180 - 0.8 * 360 / 9), fill=two(ic, "#D4D8DD", "#8D949C"))
    ic.circle(bx, by, 25, fill="#8D949C", opacity=0.45)
    ic.circle(bx, by, 15, fill=two(ic, "#D4D8DD", "#AEB4BB"))
    ic.circle(bx, by, 7, fill="#1E2024")
    ic.rect(bx - 2.5, by - 11, 5, 6, rx=1.5, fill="#1E2024")


TILES = [
    ("#557797", "folder"), ("#3D79A6", "env"), ("#22282D", "term"),
    ("#9A4A3A", "cal"), ("#7A4C8E", "disc"), ("#C27236", "calc"),
    ("#2E4468", "clock"), ("#2E7A78", "photo"), ("#B43344", "clap"),
]


def _tiles(ic):
    """Nine app tiles, 40 px each, in a 3 x 3 grid from (58, 46)."""
    for i, (col, glyph) in enumerate(TILES):
        x = 58 + (i % 3) * 50
        y = 46 + (i // 3) * 50
        ic.rect(x, y, 40, 40, rx=11, fill=col)
        cx, cy = x + 20, y + 20
        if glyph == "folder":
            ic.rect(cx - 12, cy - 7, 24, 16, rx=3, fill="#EDC67A")
        elif glyph == "env":
            ic.rect(cx - 12, cy - 8, 24, 16, rx=3, fill="#F6F1E6")
            ic.circle(cx, cy + 1, 3.5, fill="#B53523")
        elif glyph == "term":
            ic.path(f"M{cx - 9} {cy - 6}l6 5-6 5", fill="none", stroke="#7CF7A6", stroke_width=3.2,
                    stroke_linecap="round", stroke_linejoin="round")
            ic.rect(cx, cy + 2, 8, 3.5, rx=1, fill="#7CF7A6")
        elif glyph == "cal":
            ic.rect(cx - 11, cy - 11, 22, 22, rx=3, fill="#F7F2E7")
            ic.path(f"M{cx - 11} {cy - 8}a3 3 0 0 1 3-3h16a3 3 0 0 1 3 3v4h-22z", fill="#D23B2E")
        elif glyph == "disc":
            ic.circle(cx, cy, 13, fill="#141416")
            ic.circle(cx, cy, 5, fill="#E2B04A")
        elif glyph == "calc":
            ic.rect(cx - 9, cy - 13, 18, 26, rx=3.5, fill="#2A2C30")
            ic.rect(cx - 6, cy - 10, 12, 6, rx=1.5, fill="#B9C7A5")
        elif glyph == "clock":
            ic.circle(cx, cy, 13, fill="#D1A04F")
            ic.circle(cx, cy, 10, fill="#FBF7EC")
            ic.path(f"M{cx - 4} {cy - 3}L{cx} {cy}L{cx + 4} {cy - 6}", fill="none", stroke=INK, stroke_width=2,
                    stroke_linecap="round", stroke_linejoin="round")
        elif glyph == "photo":
            ic.rect(cx - 12, cy - 10, 24, 20, rx=2, fill="#fff")
            ic.path(f"M{cx - 9} {cy + 6}l7-9 5 5 3-2 4 6z", fill="#4D6075")
        elif glyph == "clap":
            ic.rect(cx - 12, cy - 4, 24, 15, rx=2.5, fill="#2A2C30")
            ic.path(f"M{cx - 12} {cy - 7}l23-6 1 4-23 6z", fill="#F1EFE8")


@soft("Launcher")
def launcher(ic):
    tile(ic, "#4B4FA6", "#22245E")
    soft_shadow(ic, 128, 216, 98, 12)
    ic.rect(46, 34, 164, 164, rx=26, fill=two(ic, "#ECE9F4", "#C2BDD4"))
    _tiles(ic)
    lx, ly, lr = 116, 104, 42
    ic.path(f"M{lx + 50} {ly + 50}L{lx + 84} {ly + 84}", stroke=two(ic, "#9A5A30", "#5A3016"), stroke_width=20,
            stroke_linecap="round")
    ic.path(f"M{lx + 34} {ly + 34}L{lx + 53} {ly + 53}", stroke="#B88433", stroke_width=16)
    lens = ic.clip(f'<circle cx="{lx}" cy="{ly}" r="{lr}"/>')
    with ic.g(clip_path=lens):
        ic.rect(lx - lr, ly - lr, lr * 2, lr * 2, fill="#E6E2EF")
        with ic.g(transform=f"translate({lx} {ly}) scale(1.4) translate({-lx} {-ly})"):
            _tiles(ic)
    ic.circle(lx, ly, lr + 5, fill="none", stroke=two(ic, "#E2B45E", "#B88433"), stroke_width=11)


@soft("Assistant")
def assistant(ic):
    tile(ic, "#7650A8", "#3A2266")
    soft_shadow(ic, 128, 214, 104, 12)
    ic.path("M28 178v14a100 20 0 0 0 200 0v-14z", fill="#1A1512")
    ic.ellipse(128, 178, 100, 20, fill=two(ic, "#4A3E36", "#2A2420"))
    steel = two(ic, "#D4D8DD", "#9AA1A9")
    ic.rect(122, 50, 12, 30, rx=3, fill=steel)
    ic.ellipse(128, 48, 19, 7, fill=two(ic, "#EEF0F2", "#AEB4BB"))
    ic.path("M46 176C46 116 84 76 128 76C172 76 210 116 210 176Z", fill=two(ic, "#EDC77E", "#B07E2E"))
    ic.path("M44 174a84 12 0 0 0 168 0v5a84 12 0 0 1-168 0z", fill="#9A6E28")
    mark(ic, 100, 106, 56, fill="#8A6020", opacity=0.85)
