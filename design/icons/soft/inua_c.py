"""Soft drawings of inua's third batch: Color Picker, VM, Workshop, and
the games (Game Lobby, Chinese Checkers, Minesweeper, Small Fortune, Space
Pinball). The same objects as drawings/inua_c.py, about half the detail,
no text."""

import math
import random

from lib import bar, mark, polar, soft, soft_shadow, tile, two

STEEL = ("#D4D8DD", "#9AA1A9")
BRASS = ("#E2B45E", "#B88433")


def rot(deg, cx, cy):
    return f"rotate({deg:g} {cx:g} {cy:g})"


def shade(c, k=0.55):
    r, g, b = (int(c[i:i + 2], 16) for i in (1, 3, 5))
    return "#{:02X}{:02X}{:02X}".format(int(r * k), int(g * k), int(b * k))


def heart(ic, x, y, s, **kw):
    ic.path("M0 .45C-.1 .3-.5 .1-.5-.15C-.5-.38-.3-.48-.15-.45C-.05-.43 0-.35 0-.3"
            "C0-.35 .05-.43 .15-.45C.3-.48 .5-.38 .5-.15C.5 .1 .1 .3 0 .45Z",
            transform=f"translate({x:g} {y:g}) scale({s:g})", **kw)


def star(cx, cy, r_out, r_in, n=5, turn=0):
    return [polar(cx, cy, r_out if i % 2 == 0 else r_in, turn + i * 180 / n) for i in range(n * 2)]


CHIPS = [
    ("#C9A9D6", "#9D6DB4", "#6E3F86"),
    ("#9DBCE6", "#4F86CC", "#2463AE"),
    ("#A8DCC0", "#5BB58A", "#2E8A5F"),
    ("#FBE0A6", "#F6BE5A", "#E99A24"),
    ("#F6B3A2", "#E8704F", "#C8402B"),
]


@soft("ColorPicker")
def colorpicker(ic):
    tile(ic, "#8B827A", "#4A433D")
    soft_shadow(ic, 128, 214, 98, 12)
    px, py = 60, 198
    for tints, a in zip(reversed(CHIPS), (-74, -56, -38, -20, -2)):
        with ic.g(transform=f"translate({px} {py}) rotate({a})"):
            ic.rect(-14, -19, 180, 38, rx=8, fill="#FBF9F4")
            ic.path("M14 -15H109V15H14z", fill=tints[1])
            ic.rect(14, -15, 32, 30, fill=tints[0])
            ic.rect(77, -15, 32, 30, fill=tints[2])
            bar(ic, 116, -9, 36, 7, fill="#2E2B27")
            bar(ic, 116, 3, 24, 5, fill="#A49E91")
    ic.circle(px, py, 8, fill=two(ic, *BRASS))
    ic.circle(px, py, 3, fill="#5A4016")
    tx, ty = polar(px, py, 96, 70)
    ink = "#2463AE"
    with ic.g(transform=f"translate({tx:.1f} {ty:.1f}) rotate(-52)"):
        ic.path("M0 -3L20 -8H76V8H20L0 3Z", fill="#F4F6F8", stroke="#F4F6F8", stroke_width=2,
                stroke_linejoin="round")
        ic.path("M0 -2L20 -6.5H50V6.5H20L0 2Z", fill=ink)
        ic.rect(74, -10, 11, 20, rx=3, fill=two(ic, *STEEL))
        ic.path("M83 -8C91 -9 93 -13 105 -13C117 -13 124 -8 124 0C124 8 117 13 105 13C93 13 91 9 83 8Z",
                fill=two(ic, "#3A3432", "#141110"))
    ic.circle(tx + 0.5, ty + 1.5, 3.5, fill=ink)


def up_arrow(ic, x, y, h, fill):
    w = h * 0.55
    ic.path(f"M{x:g} {y:g}l{w / 2:g} {h * 0.42:g}h{-w * 0.28:g}v{h * 0.58:g}h{-w * 0.44:g}v{-h * 0.58:g}"
            f"h{-w * 0.28:g}z", fill=fill, stroke=fill, stroke_width=1.5, stroke_linejoin="round")


@soft("VM")
def vm(ic):
    tile(ic, "#8E6F4E", "#4B3622")
    soft_shadow(ic, 130, 214, 100, 12)
    ic.poly([(78, 100), (214, 100), (226, 52), (90, 56)], fill=two(ic, "#E8C27C", "#C99A52"))
    ic.poly([(78, 100), (214, 100), (186, 118), (48, 118)], fill="#7A5427")
    ic.poly([(48, 118), (78, 100), (50, 74), (20, 92)], fill=two(ic, "#F3D493", "#D6AA62"))
    ic.rect(86, 42, 92, 92, rx=12, fill=two(ic, "#F1EBDD", "#CFC4AD"))
    ic.rect(95, 50, 74, 54, rx=7, fill="#4F4A42")
    ic.rect(99, 54, 66, 46, rx=4, fill=two(ic, "#3F6E8E", "#1F3C55"))
    ic.rect(106, 66, 40, 26, rx=4, fill="#F3F1EC")
    bar(ic, 111, 73, 22, 5, fill="#3A3A3A")
    bar(ic, 111, 82, 28, 5, fill="#8C887F")
    ic.rect(140, 112, 26, 4, rx=2, fill="#4F4A42")
    for x, y, a in ((62, 115, 20), (178, 113, 40), (194, 110, -10)):
        ic.ellipse(x, y, 7, 4, fill="#F7F1E1", transform=rot(a, x, y))
    ic.poly([(186, 118), (214, 100), (214, 186), (186, 206)], fill=two(ic, "#C99C50", "#9C7231"))
    ic.poly([(186, 118), (214, 100), (230, 108), (202, 128)], fill=two(ic, "#D9AE66", "#B3843F"))
    ic.rect(48, 118, 138, 88, rx=3, fill=two(ic, "#F3D493", "#D5A85E"))
    ic.rect(108, 118, 20, 34, fill="#EADBB2", opacity=0.9)
    ink = "#3E2A16"
    up_arrow(ic, 64, 132, 22, ink)
    up_arrow(ic, 80, 132, 22, ink)
    bar(ic, 56, 162, 54, 8, fill=ink, opacity=0.85)
    with ic.g(transform=rot(-3, 158, 178)):
        ic.rect(136, 158, 44, 40, rx=4, fill="#FBF9F3")
        bar(ic, 141, 164, 28, 7, fill="#24221F")
        bar(ic, 141, 175, 20, 4, fill="#8C887F")
        ic.rect(141, 184, 33, 8, rx=1, fill="#24221F")


def wrench(ic, cx, cy, deg):
    hx = 70
    s = math.sqrt(17 ** 2 - 6 ** 2)
    jaw = f"M{hx + s:.1f} -6H{hx - 4}A6 6 0 0 0 {hx - 4} 6H{hx + s:.1f}A17 17 0 1 1 {hx + s:.1f} -6Z"
    ring = (f"M{-hx + 15} 0A15 15 0 1 1 {-hx - 15} 0A15 15 0 1 1 {-hx + 15} 0Z"
            f"M{-hx + 8} 0A8 8 0 1 0 {-hx - 8} 0A8 8 0 1 0 {-hx + 8} 0Z")
    handle = f"M{-hx + 8} -7.5L{hx - 8} -6.5L{hx - 8} 6.5L{-hx + 8} 7.5Z"
    with ic.g(transform=f"translate({cx} {cy}) rotate({deg})", fill="#A3AAB2"):
        ic.path(handle)
        ic.path(jaw)
        ic.path(ring, fill_rule="evenodd")


def screwdriver(ic, cx, cy, deg):
    with ic.g(transform=f"translate({cx} {cy}) rotate({deg})"):
        ic.path("M-14 -4H66L76 -1.5V1.5L66 4H-14Z", fill="#C3C8CE")
        ic.rect(-80, -12, 66, 24, rx=7, fill="#D8452E")
        ic.rect(-80, -12, 66, 9, rx=4.5, fill="#EE6A4A")
        ic.rect(-18, -8, 7, 16, rx=2, fill="#AEB4BB")


@soft("Workshop")
def workshop(ic):
    tile(ic, "#7E5A3A", "#3E2817")
    soft_shadow(ic, 128, 214, 100, 11)
    ic.rect(28, 30, 200, 180, rx=14, fill=two(ic, "#DDB57F", "#BC8E57"))
    for x in range(48, 214, 20):
        for y in range(46, 200, 20):
            ic.circle(x, y, 3, fill="#7A5430", opacity=0.45)
    ic.path("M72 49L52 55L72 61Z", fill="#E8C392", stroke="#E8C392", stroke_width=2, stroke_linejoin="round")
    ic.path("M52 55L59 53V57Z", fill="#2E2B28", stroke="#2E2B28", stroke_width=2, stroke_linejoin="round")
    ic.rect(72, 49, 104, 12, fill=two(ic, "#FBD56B", "#D9961C"))
    ic.rect(176, 49, 10, 12, fill=two(ic, *STEEL))
    ic.path("M186 49h6a6 6 0 0 1 6 6v0a6 6 0 0 1-6 6h-6z", fill="#E58A8A")
    wrench(ic, 128, 122, 36)
    screwdriver(ic, 128, 122, 144)
    for x, y in ((80, 96), (176, 96)):
        ic.circle(x, y, 4.5, fill=two(ic, *STEEL))
    ic.rect(42, 172, 172, 24, rx=4, fill=two(ic, "#F4E2BC", "#DCC291"))
    for i in range(17):
        ic.rect(47 + i * 10, 172, 2, 10 if i % 2 == 0 else 6, rx=1, fill="#3A2A16")


@soft("GameLobby")
def gamelobby(ic):
    tile(ic, "#2A6A48", "#0E3321")
    soft_shadow(ic, 128, 214, 102, 12)
    ic.rect(22, 30, 212, 182, rx=44, fill=two(ic, "#5A3424", "#2E180E"))
    ic.rect(36, 44, 184, 154, rx=28, fill=two(ic, "#3A9A63", "#1E6640"))
    ic.path("M54 138A170 170 0 0 1 202 138", fill="none", stroke="#E2BE68", stroke_opacity=0.7, stroke_width=2.5)
    for cx, base, cols in ((182, 160, ["#C8372D", "#1E1E20", "#C8372D", "#2463AE", "#C8372D"]),
                           (150, 186, ["#2E8A5F", "#1E1E20"])):
        for i, c in enumerate(cols):
            y = base - i * 7
            ic.path(f"M{cx - 20} {y}v7a20 7.5 0 0 0 40 0v-7z", fill=shade(c, 0.8))
        y = base - (len(cols) - 1) * 7
        ic.ellipse(cx, y, 20, 7.5, fill=cols[-1])
        ic.ellipse(cx, y, 17, 6, fill="none", stroke="#F4EFE4", stroke_width=3, stroke_dasharray="5 6")
    red = "#C8372D"
    px, py = 96, 200
    for a in (-36, -18, 0, 18, 36):
        with ic.g(transform=rot(a, px, py)):
            x, y = px - 25, py - 112
            ic.rect(x, y, 50, 72, rx=7, fill=two(ic, "#FFFFFF", "#ECE7DC"), stroke="#1E3A2A", stroke_opacity=0.25,
                    stroke_width=1.5)
            bar(ic, x + 5, y + 6, 8, 6, fill=red)
            heart(ic, x + 9, y + 20, 9, fill=red)
            if a == 36:
                heart(ic, x + 25, y + 40, 28, fill=red)


def cc_holes(s, cx, cy):
    h = s * math.sqrt(3) / 2
    out = []
    for j in range(17):
        up = j + 1 if j <= 12 else 0
        down = 17 - j if j >= 4 else 0
        n = max(up, down)
        for i in range(n):
            x = cx + (i - (n - 1) / 2) * s
            y = cy + (j - 8) * h
            k = i - (n - 1) / 2
            if j <= 3:
                reg = 0
            elif j >= 13:
                reg = 3
            elif j <= 7 and abs(k) > j / 2:
                reg = 1 if k > 0 else 5
            elif j >= 9 and abs(k) > (16 - j) / 2:
                reg = 2 if k > 0 else 4
            else:
                reg = None
            out.append((x, y, reg))
    return out


MARBLES = ["#D23A2C", "#F0B232", "#2E9A58", "#2B6FC4", "#7A4AB2", "#F2EEE4"]


@soft("ChineseCheckers")
def chinesecheckers(ic):
    tile(ic, "#6E4A30", "#331F12")
    soft_shadow(ic, 128, 216, 96, 12)
    cx, cy, r = 128, 120, 100
    ic.circle(cx, cy + 6, r, fill="#5A3418")
    ic.circle(cx, cy, r, fill=two(ic, "#E6C08A", "#C08B4F"))
    s = 12.6
    h = s * math.sqrt(3) / 2
    R = 8 * h + 6
    tri = [polar(cx, cy, R, a) for a in range(0, 360, 60)]
    inner = [polar(cx, cy, 4 * s + 4, a + 30) for a in range(0, 360, 60)]
    paint = ["#D23A2C", "#E9A322", "#2E9A58", "#2B6FC4", "#7A4AB2", "#E8E0CF"]
    for i in range(6):
        ic.poly([inner[(i - 1) % 6], tri[i], inner[i]], fill=paint[i], opacity=0.4, stroke=paint[i],
                stroke_width=4, stroke_linejoin="round")
    holes = cc_holes(s, cx, cy)
    for x, y, reg in holes:
        if reg is None:
            ic.circle(x, y, 2.6, fill="#6A3E1A")
    moved = {(0, 9): (cx - 0.5 * s, cy - 3 * h), (3, 2): (cx + s, cy + 2 * h), (5, 9): (cx - 2 * s, cy),
             (1, 9): (cx + 1.5 * s, cy - h)}
    grads = [two(ic, c, shade(c)) for c in MARBLES]
    counts = [0] * 6
    marbles = []
    for x, y, reg in holes:
        if reg is None:
            continue
        key = (reg, counts[reg])
        counts[reg] += 1
        if key in moved:
            ic.circle(x, y, 2.6, fill="#6A3E1A")
            x, y = moved[key]
        marbles.append((y, x, reg))
    for y, x, reg in sorted(marbles):
        ic.circle(x, y, 5.6, fill=grads[reg])


NUMS = {  # a digit as one bold stroke, in a box 12 wide, 18 high, from its top left
    1: "M3 4L7 1V17",
    2: "M1 5C1 0 11 0 11 5C11 9 1 13 1 17H11",
    3: "M1 2C4 0 11 0 11 4.5C11 8 7 9 5 9C8 9 11 10 11 13.5C11 18 3 18 1 16",
}
NUM_COLOURS = {1: "#2B5FD9", 2: "#2E8B3E", 3: "#D2392B"}


def flag(ic, x, y):
    ic.rect(x - 8, y - 4, 16, 4, rx=2, fill="#1E1F21")
    ic.rect(x - 1.2, y - 22, 2.4, 19, rx=1.2, fill="#2E3033")
    ic.path(f"M{x + 1} {y - 23}L{x - 12} {y - 17.5}L{x + 1} {y - 12}Z", fill="#D8352A", stroke="#D8352A",
            stroke_width=2, stroke_linejoin="round")


@soft("Minesweeper")
def minesweeper(ic):
    tile(ic, "#6C7768", "#2E362C")
    soft_shadow(ic, 128, 218, 98, 12)
    n, pitch, t = 5, 31, 29
    w = n * pitch - 2
    x0, y0 = 128 - w / 2, 62
    bx, by, bw, bh = x0 - 12, 22, w + 24, y0 + w + 12 - 22
    ic.rect(bx, by, bw, bh, rx=16, fill=two(ic, "#9AA396", "#5E6759"))
    ic.rect(x0 - 4, 30, w + 8, 26, rx=6, fill="#3E453C")
    for lx in (x0, x0 + w - 40):
        ic.rect(lx, 33, 40, 20, rx=4, fill="#120606")
        for k in range(3):
            ic.rect(lx + 5 + k * 11, 37, 8, 12, rx=2, fill="#FF4A36", opacity=0.35 if k == 0 else 1)
    ic.circle(128, 43, 10.5, fill="#D5D9D0")
    ic.circle(128, 43, 8, fill=two(ic, "#FFE680", "#E3A91E"))
    ic.circle(125.2, 41.2, 1.3, fill="#3A2A08")
    ic.circle(130.8, 41.2, 1.3, fill="#3A2A08")
    ic.path("M124.4 45a4 3.4 0 0 0 7.2 0", fill="none", stroke="#3A2A08", stroke_width=1.5, stroke_linecap="round")
    ic.rect(x0 - 4, y0 - 4, w + 8, w + 8, rx=6, fill="#3E453C")
    mines = {(0, 1), (0, 3), (0, 4), (1, 4), (4, 0), (3, 4)}
    revealed = {(r, c) for r in range(1, 4) for c in range(0, 4)} | {(4, 1), (4, 2), (4, 3), (0, 3)}
    flags = {(4, 0), (1, 4)}
    up = two(ic, "#EEF0EA", "#CBD0C5")
    for r in range(n):
        for c in range(n):
            x, y = x0 + c * pitch, y0 + r * pitch
            if (r, c) in revealed:
                boom = (r, c) in mines
                ic.rect(x, y, t, t, rx=3, fill="#C8392C" if boom else "#A8AEA3")
                if boom:
                    mx, my = x + t / 2, y + t / 2
                    for a in range(0, 360, 45):
                        ax, ay = polar(mx, my, 11, a)
                        ic.line(mx, my, ax, ay, stroke="#1B1C1E", stroke_width=3, stroke_linecap="round")
                    ic.circle(mx, my, 7.5, fill="#1B1C1E")
                    continue
                k = sum((rr, cc) in mines for rr in (r - 1, r, r + 1) for cc in (c - 1, c, c + 1))
                if k:
                    ic.path(NUMS[k], fill="none", stroke=NUM_COLOURS[k], stroke_width=4.2, stroke_linecap="round",
                            stroke_linejoin="round", transform=f"translate({x + t / 2 - 6:g} {y + 5.5:g})")
            else:
                ic.rect(x, y + 2.5, t, t, rx=4, fill="#596254")
                ic.rect(x, y, t, t, rx=4, fill=up)
                if (r, c) in flags:
                    flag(ic, x + t / 2 + 3.5, y + t - 4)


PIPS = {
    1: [(.5, .5)],
    2: [(.27, .27), (.73, .73)],
    3: [(.25, .25), (.5, .5), (.75, .75)],
    4: [(.27, .27), (.73, .27), (.27, .73), (.73, .73)],
    5: [(.25, .25), (.75, .25), (.5, .5), (.25, .75), (.75, .75)],
    6: [(.28, .24), (.28, .5), (.28, .76), (.72, .24), (.72, .5), (.72, .76)],
}


def die(ic, cx, cy, a, top, left, right):
    k = 0.866 * a
    lx, ly = cx - k, cy - a / 2
    hexa = [(cx, cy - a), (cx + k, cy - a / 2), (cx + k, cy + a / 2), (cx, cy + a), (cx - k, cy + a / 2),
            (cx - k, cy - a / 2)]
    ic.poly(hexa, fill="#CFC2A3", stroke="#CFC2A3", stroke_width=a * 0.18, stroke_linejoin="round")
    faces = (
        (f"matrix({k:.3f} {a / 2:.3f} {k:.3f} {-a / 2:.3f} {lx:.2f} {ly:.2f})", top, "#FCF8EC"),
        (f"matrix({k:.3f} {a / 2:.3f} 0 {a:.3f} {lx:.2f} {ly:.2f})", left, "#E2D7BC"),
        (f"matrix({k:.3f} {-a / 2:.3f} 0 {a:.3f} {cx:.2f} {cy:.2f})", right, "#BFAE88"),
    )
    for m, num, col in faces:
        with ic.g(transform=m):
            ic.rect(0.03, 0.03, 0.94, 0.94, rx=0.18, fill=col)
            for px, py in PIPS[num]:
                ic.circle(px, py, 0.17 if num == 1 else 0.095, fill="#C2352A" if num == 1 else "#2A2420")


def note(ic, x, y, ink, seal=True):
    w, h = 176, 94
    ic.rect(x, y, w, h, rx=4, fill=two(ic, "#F7F2E7", "#DDD5C4"))
    ic.rect(x + 7, y + 7, w - 14, h - 14, rx=3, fill="none", stroke=ink, stroke_width=3)
    rx_, ry_ = x + w - 40, y + h / 2
    ic.circle(rx_, ry_, 20, fill="none", stroke=ink, stroke_opacity=0.4, stroke_width=2.5)
    if seal:
        mark(ic, rx_ - 10, ry_ - 10, 20, fill=ink, opacity=0.75)
    bar(ic, x + 16, y + 16, 58, 6, fill=ink)
    num = dict(fill="none", stroke=ink, stroke_width=6.5, stroke_linecap="round", stroke_linejoin="round")
    ic.path(f"M{x + 17} {y + 34}L{x + 23} {y + 30}V{y + 54}", **num)
    ic.ellipse(x + 40, y + 42, 8, 12, **num)
    bar(ic, x + 17, y + 63, 34, 8, fill=ink)
    ic.rect(x + 66, y + 32, 18, 18, rx=4, fill="#C8372D", opacity=0.85)


@soft("SmallFortune")
def smallfortune(ic):
    tile(ic, "#B89140", "#6A4C15")
    soft_shadow(ic, 126, 200, 100, 12)
    with ic.g(transform=rot(-9, 122, 106)):
        note(ic, 34, 60, "#B5432F", seal=False)
    with ic.g(transform=rot(4, 128, 140)):
        note(ic, 36, 96, "#2E4A7A")
    die(ic, 162, 106, 38, 1, 2, 3)
    die(ic, 200, 150, 32, 6, 5, 4)


def flipper(ic, px, py, tx, ty):
    a = math.degrees(math.atan2(ty - py, tx - px))
    ln = math.hypot(tx - px, ty - py)
    with ic.g(transform=f"translate({px} {py}) rotate({a:.1f})"):
        ic.path(f"M0 -7.5A7.5 7.5 0 0 0 0 7.5L{ln:.1f} 4A4 4 0 0 0 {ln:.1f} -4Z", fill="#D8352A")
        ic.circle(0, 0, 2.5, fill="#F5F2EA")


def bumper(ic, x, y, cap):
    ic.circle(x, y, 15, fill="#E9ECEF")
    ic.circle(x, y, 11, fill=two(ic, cap, shade(cap, 0.7)))
    ic.poly(star(x, y, 6.5, 2.8), fill="#FFF6D8")


@soft("SpacePinball")
def spacepinball(ic):
    tile(ic, "#2E3F7E", "#0D1534")
    soft_shadow(ic, 128, 218, 88, 11)
    ic.path("M44 214V84C44 46 82 22 128 22C174 22 212 46 212 84V214Z", fill=two(ic, "#C8CDD3", "#6E757E"))
    field = "M52 210V86C52 54 86 30 128 30C170 30 204 54 204 86V210Z"
    ic.path(field, fill=two(ic, "#262B72", "#0A0D2A"))
    rnd = random.Random(7)
    for _ in range(18):
        ic.circle(rnd.uniform(60, 196), rnd.uniform(44, 186), rnd.choice((1, 1.4)), fill="#fff",
                  opacity=rnd.uniform(0.4, 0.9))
    for sx, sy in ((70, 120), (186, 58)):
        ic.poly(star(sx, sy, 5, 1.5, 4), fill="#fff")
    ic.circle(176, 104, 13, fill=two(ic, "#F6C36A", "#B0582A"))
    ic.ellipse(176, 104, 23, 5.5, fill="none", stroke="#F2DDB0", stroke_width=2.5, transform=rot(-18, 176, 104))
    for x in (102, 128, 154):
        ic.rect(x - 2.5, 40, 5, 22, rx=2.5, fill="#C3C8CE")
    for x in (115, 141):
        ic.circle(x, 56, 5, fill="#F2C45C")
    bumper(ic, 100, 98, "#E0463A")
    bumper(ic, 156, 98, "#F2B232")
    bumper(ic, 128, 132, "#3FA0E0")
    for i, y in enumerate((150, 160, 170)):
        ic.path(f"M128 {y - 6}l7 8h-14z", fill="#F2C45C", opacity=1 if i == 0 else 0.5, stroke="#F2C45C",
                stroke_width=1.5, stroke_linejoin="round", stroke_opacity=1 if i == 0 else 0.5)
    for sgn, x in ((1, 64), (-1, 192)):
        ic.poly([(x, 142), (x, 170), (x + sgn * 20, 178)], fill="#EDEFF2", stroke="#EDEFF2", stroke_width=3,
                stroke_linejoin="round")
        ic.line(x + sgn * 3, 148, x + sgn * 17, 174, stroke="#D8352A", stroke_width=3.5, stroke_linecap="round")
    flipper(ic, 86, 190, 117, 199)
    flipper(ic, 170, 190, 139, 199)
    ic.path("M52 210V198H104L114 206H142L152 198H204V210Z", fill=two(ic, "#E9ECEF", "#AEB4BB"))
    bar(ic, 62, 201, 32, 5, fill="#2E3F7E")
    bar(ic, 162, 201, 32, 5, fill="#2E3F7E")
    ic.circle(150, 158, 10, fill=two(ic, "#F4F6F8", "#7C838C"))
    ic.circle(146.5, 154.5, 3, fill="#fff")
