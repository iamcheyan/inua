"""inua's icons, third batch: Color Picker, VM, Workshop, and the games
(Game Lobby, Chinese Checkers, Minesweeper, Small Fortune, Space Pinball)."""

import math
import random

from lib import (brass, felt, glare, icon, leather, mark, paper, polar, shadow, small, steel, text_path, tile, wood)


def rot(deg, cx, cy):
    return f"rotate({deg:g} {cx:g} {cy:g})"


def arc_text(ic, s, cx, cy, r, mid_deg, size, font="sans-semibold", spacing=0.0, **kw):
    """A line of text along a circle (centre cx, cy; radius r to the
    baseline), centred on the angle mid_deg (0 up, clockwise), reading
    left to right over the top."""
    widths = [text_path(c, 0, 0, size, font)[1] for c in s]
    total = sum(widths) + spacing * (len(s) - 1)
    deg = mid_deg - math.degrees(total / r) / 2
    for c, w in zip(s, widths):
        mid = deg + math.degrees(w / 2 / r)
        x, y = polar(cx, cy, r, mid)
        if c != " ":
            ic.text(c, x, y, size, font=font, anchor="middle", transform=rot(mid, x, y), **kw)
        deg += math.degrees((w + spacing) / r)


def heart(ic, x, y, s, **kw):
    """A heart (the suit), s px wide, centred on x, y."""
    ic.path("M0 .45C-.1 .3-.5 .1-.5-.15C-.5-.38-.3-.48-.15-.45C-.05-.43 0-.35 0-.3"
            "C0-.35 .05-.43 .15-.45C.3-.48 .5-.38 .5-.15C.5 .1 .1 .3 0 .45Z",
            transform=f"translate({x:g} {y:g}) scale({s:g})", **kw)


def star(cx, cy, r_out, r_in, n=5, turn=0):
    pts = []
    for i in range(n * 2):
        pts.append(polar(cx, cy, r_out if i % 2 == 0 else r_in, turn + i * 180 / n))
    return pts


# --- Color Picker: a glass eyedropper over a fan of colour chips ---------------

CHIPS = [  # name, number, three tints from the rivet out
    ("Plum", "INUA 3015", ("#C9A9D6", "#9D6DB4", "#6E3F86")),
    ("Lapis", "INUA 2463", ("#9DBCE6", "#4F86CC", "#2463AE")),
    ("Jade", "INUA 5520", ("#A8DCC0", "#5BB58A", "#2E8A5F")),
    ("Saffron", "INUA 1358", ("#FBE0A6", "#F6BE5A", "#E99A24")),
    ("Vermilion", "INUA 1664", ("#F6B3A2", "#E8704F", "#C8402B")),
]


@icon("ColorPicker")
def colorpicker(ic):
    tile(ic, "#8B827A", "#4A433D")
    shadow(ic, 128, 214, 98, 12)
    px, py = 60, 198  # the rivet
    angles = [-74, -56, -38, -20, -2]
    card = ic.lin([(0, "#FFFFFF"), (1, "#E9E5DC")], 0, -19, 0, 19, units="userSpaceOnUse")
    for (name, num, tints), a in zip(reversed(CHIPS), angles):
        with ic.g(transform=f"translate({px} {py}) rotate({a})"):
            ic.rect(-12, -17, 180, 38, rx=6, fill="#000", opacity=0.18)
            ic.rect(-14, -19, 180, 38, rx=6, fill=card)
            for i, t in enumerate(tints):
                ic.rect(14 + i * 32, -15, 31, 30, fill=t)
            ic.rect(14, -15, 95, 2, fill="#fff", opacity=0.25)
            ic.text(name, 114, -2, 9, font="sans-semibold", fill="#2E2B27")
            ic.text(num, 114, 9, 6.4, font="mono", fill="#6A665D")
            ic.line(-12, -18.2, 164, -18.2, stroke="#fff", stroke_width=1.2, opacity=0.9)
    ic.circle(px, py, 7, fill=brass(ic))
    ic.circle(px, py, 2.5, fill="#5A4016")
    # the eyedropper: its tip on Lapis's deepest chip, the bulb up to the right
    tx, ty = polar(px, py, 96, 70)
    ink = "#2463AE"
    tube = "M0 -2.4L20 -7.5H76V7.5H20L0 2.4Z"
    bulb = "M83 -8C91 -9 93 -13 105 -13C117 -13 124 -8 124 0C124 8 117 13 105 13C93 13 91 9 83 8Z"
    with ic.g(transform=f"translate({tx + 7:.1f} {ty + 6:.1f}) rotate(-52)", fill="#1E1A16", opacity=0.3):
        ic.path(tube)
        ic.rect(74, -9.5, 10, 19)
        ic.path(bulb)
    with ic.g(transform=f"translate({tx:.1f} {ty:.1f}) rotate(-52)"):
        glass = ic.lin([(0, "#FFFFFF", 0.6), (0.35, "#FFFFFF", 0.15), (1, "#FFFFFF", 0.35)], 0, -8, 0, 8, units="userSpaceOnUse")
        ic.path("M0 -1.6L20 -6.5H50V6.5H20L0 1.6Z", fill=ink)
        ic.ellipse(50, 0, 2, 6.5, fill="#4F86CC")
        ic.path(tube, fill=glass, stroke="#fff", stroke_opacity=0.75, stroke_width=1)
        ic.line(22, -4.6, 73, -4.6, stroke="#fff", stroke_width=1.6, stroke_linecap="round", opacity=0.9)
        for i, x in enumerate(range(30, 72, 7)):
            ic.line(x, 7.5, x, 7.5 - (5 if i % 2 == 0 else 3), stroke="#fff", stroke_width=0.8, opacity=0.8)
        ic.rect(74, -9.5, 10, 19, rx=2, fill=ic.lin([(0, "#E8EBEE"), (0.5, "#A9B0B8"), (1, "#4E545B")], 0, -9.5, 0, 9.5, units="userSpaceOnUse"))
        ic.line(77, -9.5, 77, 9.5, stroke="#4E545B", stroke_width=0.8)
        ic.line(81, -9.5, 81, 9.5, stroke="#4E545B", stroke_width=0.8)
        rubber = ic.lin([(0, "#4A4442"), (0.3, "#24201F"), (1, "#0E0C0B")], 0, -13, 0, 13, units="userSpaceOnUse")
        ic.path(bulb, fill=rubber)
        ic.path("M93 -9.5C99 -11.2 105 -11 113 -10.6", stroke="#fff", stroke_width=2, stroke_linecap="round", fill="none", opacity=0.4)
    ic.circle(tx + 0.5, ty + 1.5, 3, fill=ink)
    ic.circle(tx - 0.4, ty + 0.6, 0.9, fill="#fff", opacity=0.7)


@small("ColorPicker")
def colorpicker16(ic):
    tile(ic, "#8B827A", "#4A433D")
    for c, a in (("#C8402B", -70), ("#F6BE5A", -46), ("#2463AE", -22), ("#9D6DB4", 0)):
        ic.rect(0, -2, 11, 4, rx=0.8, fill=c, transform=f"translate(3 12.5) rotate({a})")
    ic.line(9, 9.5, 13.5, 3, stroke="#F4F4F2", stroke_width=1.6, stroke_linecap="round")
    ic.line(12.4, 4.6, 14, 2.3, stroke="#1E1B1A", stroke_width=2.4, stroke_linecap="round")


# --- VM: an open shipping box, a small computer inside ----------------------

def up_arrow(ic, x, y, h, fill):
    w = h * 0.55
    ic.path(f"M{x:g} {y:g}l{w / 2:g} {h * 0.42:g}h{-w * 0.28:g}v{h * 0.58:g}h{-w * 0.44:g}v{-h * 0.58:g}h{-w * 0.28:g}z", fill=fill)


@icon("VM")
def vm(ic):
    tile(ic, "#8E6F4E", "#4B3622")
    shadow(ic, 130, 214, 100, 12)
    kraft = paper(ic, "kraft")
    dark = paper(ic, "kraft-dark")
    # inside: the back wall and the back flap, leant back
    ic.poly([(78, 100), (214, 100), (226, 52), (90, 56)], fill=ic.lin([(0, "#E8C27C"), (1, "#C99A52")]))
    ic.line(90, 56.5, 225, 52.5, stroke="#FBE6B8", stroke_width=1.5)
    ic.poly([(78, 100), (214, 100), (186, 118), (48, 118)], fill="#7A5427")
    # the left flap, open out to the left
    ic.poly([(48, 118), (78, 100), (50, 74), (20, 92)], fill=ic.lin([(0, "#F3D493"), (1, "#D1A35A")], 0, 0, 1, 1))
    ic.line(20.5, 92, 50, 74.5, stroke="#FFF1CF", stroke_width=1.5)
    # the computer, standing in the box
    body = ic.lin([(0, "#F1EBDD"), (0.6, "#DDD3BF"), (1, "#BFB39A")], 0, 0, 1, 1)
    ic.rect(86, 42, 92, 92, rx=9, fill="#000", opacity=0.25, transform="translate(4 3)")
    ic.rect(86, 42, 92, 92, rx=9, fill=body)
    ic.rect(86.75, 42.75, 90.5, 90.5, rx=8.25, fill="none", stroke="#fff", stroke_opacity=0.6, stroke_width=1.5)
    ic.rect(95, 50, 74, 54, rx=5, fill="#4F4A42")
    ic.rect(99, 54, 66, 46, rx=3, fill=ic.lin([(0, "#3F6E8E"), (1, "#1F3C55")]))
    ic.rect(99, 54, 66, 6, fill="#0E1A24", opacity=0.75)
    ic.text("inua", 102, 58.6, 4.4, font="mono-semibold", fill="#E9EEF2")
    ic.circle(160, 57, 1.2, fill="#7CF7A6")
    ic.rect(106, 66, 40, 26, rx=2, fill="#F3F1EC")
    ic.rect(106, 66, 40, 5, rx=2, fill="#D9D4CA")
    ic.text("$ uname", 109, 78, 5, font="mono", fill="#3A3A3A")
    ic.text("Linux vm", 109, 85.5, 5, font="mono", fill="#3A3A3A")
    ic.path("M99 57a3 3 0 0 1 3-3h40L118 100H102a3 3 0 0 1-3-3z", fill="#fff", opacity=0.12)
    ic.rect(140, 112, 26, 3, rx=1.5, fill="#4F4A42")
    # packing peanuts
    for x, y, a in ((60, 116, 20), (74, 112, -30), (176, 114, 40), (188, 109, -10), (198, 112, 60), (168, 118, -50)):
        ic.ellipse(x, y, 6, 3.4, fill="#F7F1E1", transform=rot(a, x, y))
        ic.ellipse(x - 1, y - 1, 3, 1.2, fill="#fff", transform=rot(a, x, y))
    # the right side, the front, the front flap folded down
    ic.poly([(186, 118), (214, 100), (214, 186), (186, 206)], fill=dark)
    ic.poly([(186, 118), (214, 100), (230, 108), (202, 128)], fill=ic.lin([(0, "#D9AE66"), (1, "#B3843F")]))
    ic.rect(48, 118, 138, 88, fill=kraft)
    ic.line(48, 118.8, 186, 118.8, stroke="#FFF1CF", stroke_width=1.6)
    ic.line(186, 118, 186, 206, stroke="#7C5520", stroke_opacity=0.5, stroke_width=1.2)
    # tape, cut where the box was opened
    ic.path("M108 118h20v34l-3 2-3-2-3 2-3-2-3 2-3-2-2 2z", fill="#E9D6A6", opacity=0.85)
    ic.path("M110 118v34", stroke="#fff", stroke_opacity=0.5, stroke_width=1.2)
    # THIS SIDE UP, its arrows, a label
    ink = "#3E2A16"
    up_arrow(ic, 64, 132, 22, ink)
    up_arrow(ic, 80, 132, 22, ink)
    ic.text("THIS SIDE UP", 56, 168, 9.2, font="sans-bold", spacing=0.4, fill=ink, opacity=0.9)
    ic.rect(56, 176, 54, 1.6, fill=ink, opacity=0.6)
    ic.rect(136, 158, 44, 40, rx=2, fill="#FBF9F3", transform=rot(-3, 158, 178))
    with ic.g(transform=rot(-3, 158, 178)):
        ic.text("VM-01", 140, 168, 8, font="mono-semibold", fill="#24221F")
        ic.text("4 vCPU", 140, 177, 5.6, font="mono", fill="#55534E")
        ic.text("8 GB", 140, 184, 5.6, font="mono", fill="#55534E")
        for i, w in enumerate((1, 2, 1, 1, 3, 1, 2, 1, 1, 2, 1, 3, 1)):
            ic.rect(140 + sum((1, 2, 1, 1, 3, 1, 2, 1, 1, 2, 1, 3, 1)[:i]) * 1.2 + i * 0.9, 187, w * 0.9, 7, fill="#24221F")
    ic.line(48, 205, 186, 205, stroke="#7C5520", stroke_opacity=0.35, stroke_width=2)


@small("VM")
def vm16(ic):
    tile(ic, "#8E6F4E", "#4B3622")
    ic.rect(5, 2.5, 7, 6.5, rx=1, fill="#ECE5D6")
    ic.rect(6, 3.5, 5, 3.5, rx=0.4, fill="#2E5878")
    ic.poly([(3, 8), (13, 8), (14, 7), (4, 7)], fill="#7A5427")
    ic.rect(2.5, 8, 9.5, 5.5, fill="#E0B56C")
    ic.poly([(12, 8), (13.5, 7), (13.5, 12.5), (12, 13.5)], fill="#A87A38")
    ic.rect(6.5, 8, 2, 2.5, fill="#F6E8C4")


# --- Workshop: a pegboard, a crossed wrench and screwdriver --------------------

def wrench(ic, ln=64):
    """A combination wrench along x, centred on 0: open end at +x, ring at -x."""
    g = ic.lin([(0, "#E3E6EA"), (0.5, "#A9B0B8"), (1, "#5D636B")], 0, -9, 0, 9, units="userSpaceOnUse")
    gh = ic.lin([(0, "#E3E6EA"), (0.5, "#A9B0B8"), (1, "#5D636B")], 0, -17, 0, 17, units="userSpaceOnUse")
    hx = ln + 6
    s = math.sqrt(17 ** 2 - 6 ** 2)
    jaw = (f"M{hx + s:.1f} -6H{hx - 4}A6 6 0 0 0 {hx - 4} 6H{hx + s:.1f}A17 17 0 1 1 {hx + s:.1f} -6Z")
    ring = f"M{-hx + 15} 0A15 15 0 1 1 {-hx - 15} 0A15 15 0 1 1 {-hx + 15} 0ZM{-hx + 8} 0A8 8 0 1 0 {-hx - 8} 0A8 8 0 1 0 {-hx + 8} 0Z"
    handle = f"M{-hx + 8} -7L{hx - 8} -6L{hx - 8} 6L{-hx + 8} 7Z"
    return g, gh, jaw, ring, handle


def draw_wrench(ic, cx, cy, deg):
    g, gh, jaw, ring, handle = wrench(ic)
    with ic.g(transform=f"translate({cx} {cy}) rotate({deg})"):
        with ic.g(transform="translate(3 4)", fill="#2A1A0C", opacity=0.3):
            ic.path(handle)
            ic.path(jaw)
            ic.path(ring, fill_rule="evenodd")
        for d in (handle, jaw, ring):
            ic.path(d, fill="none", stroke="#FFF6E0", stroke_opacity=0.6, stroke_width=7, stroke_linejoin="round")
        ic.path(handle, fill=g)
        ic.path(jaw, fill=gh)
        ic.path(ring, fill=gh, fill_rule="evenodd")
        ic.rect(-40, -2.5, 80, 5, rx=2.5, fill="#7D848C", opacity=0.6)
        ic.text("INUA 13", 0, 2.2, 5.4, font="mono-semibold", anchor="middle", fill="#E8EBEE")
        ic.line(-50, -5.6, 50, -5, stroke="#fff", stroke_width=1, opacity=0.8)


def draw_screwdriver(ic, cx, cy, deg):
    shaft = ic.lin([(0, "#F0F2F4"), (0.5, "#A9B0B8"), (1, "#4E545B")], 0, -3.5, 0, 3.5, units="userSpaceOnUse")
    handle = ic.lin([(0, "#F58A5E"), (0.35, "#D8452E"), (1, "#7A1A10")], 0, -12, 0, 12, units="userSpaceOnUse")
    h = "M-80 -9A4 4 0 0 1 -76 -12H-20A6 6 0 0 1 -14 -6V6A6 6 0 0 1 -20 12H-76A4 4 0 0 1 -80 9Z"
    sh = "M-14 -3.5H66L76 -1.2V1.2L66 3.5H-14Z"
    with ic.g(transform=f"translate({cx} {cy}) rotate({deg})"):
        with ic.g(transform="translate(-3 4)", fill="#2A1A0C", opacity=0.3):
            ic.path(h)
            ic.path(sh)
        for d in (h, sh):
            ic.path(d, fill="none", stroke="#FFF6E0", stroke_opacity=0.6, stroke_width=7, stroke_linejoin="round")
        ic.path(sh, fill=shaft)
        ic.line(-12, -2, 66, -2, stroke="#fff", stroke_width=0.9, opacity=0.8)
        ic.path(h, fill=handle)
        for y in (-6, 0, 6):
            ic.line(-72, y, -24, y, stroke="#5E120A", stroke_width=1.6, stroke_linecap="round", opacity=0.5)
        ic.line(-74, -9.5, -20, -9.5, stroke="#FFC2A6", stroke_width=1.6, stroke_linecap="round", opacity=0.7)
        ic.rect(-18, -8, 6, 16, rx=1.5, fill=steel(ic, horizontal=False))


def peg(ic, x, y):
    ic.circle(x + 1.5, y + 2, 3.4, fill="#000", opacity=0.3)
    ic.circle(x, y, 3.4, fill=steel(ic, horizontal=False))
    ic.circle(x - 0.8, y - 0.8, 1.2, fill="#fff", opacity=0.7)


@icon("Workshop")
def workshop(ic):
    tile(ic, "#7E5A3A", "#3E2817")
    shadow(ic, 128, 214, 100, 11)
    ic.rect(28, 30, 200, 180, rx=10, fill="#2A1A0C", opacity=0.35, transform="translate(3 4)")
    ic.rect(28, 30, 200, 180, rx=10, fill=ic.lin([(0, "#DDB57F"), (1, "#B98A53")], 0, 0, 1, 1))
    holes = ic.define('<pattern id="{id}" x="38" y="40" width="16" height="16" patternUnits="userSpaceOnUse">'
                      '<circle cx="8" cy="8" r="2.4" fill="#5B3A1A" opacity=".75"/>'
                      '<path d="M9.9 6.6A2.4 2.4 0 0 1 6.6 9.9" stroke="#FFF1D6" stroke-width=".8" fill="none" opacity=".55"/>'
                      '</pattern>', "p")
    ic.rect(32, 34, 192, 172, rx=7, fill=f"url(#{holes})")
    ic.rect(29, 31, 198, 178, rx=9, fill="none", stroke="#FCE3B8", stroke_opacity=0.7, stroke_width=2)
    # the pencil, on two hooks
    with ic.g(transform="translate(0 0)"):
        ic.rect(72, 50, 110, 10, fill="#000", opacity=0.25, transform="translate(2 3)")
        ic.path("M72 50L54 55L72 60Z", fill="#E8C392")
        ic.path("M54 55L60 53.3V56.7Z", fill="#2E2B28")
        ic.rect(72, 50, 104, 10, fill="#F2B632")
        ic.rect(72, 50, 104, 3.3, fill="#FBD56B")
        ic.rect(72, 56.7, 104, 3.3, fill="#C88A16")
        ic.rect(176, 50, 10, 10, fill=steel(ic, horizontal=False))
        ic.path("M186 50h6a4 4 0 0 1 4 4v2a4 4 0 0 1-4 4h-6z", fill="#E58A8A")
        ic.text("INUA  HB", 92, 58, 6, font="mono-semibold", spacing=0.5, fill="#1F4A2E")
    for x in (96, 160):
        ic.path(f"M{x} 66v-4a3 3 0 0 0-3-3", stroke="#8E959D", stroke_width=2.4, fill="none", stroke_linecap="round")
        ic.circle(x, 66.5, 2.6, fill=steel(ic, horizontal=False))
    # the crossed tools, resting on pegs
    draw_wrench(ic, 128, 122, 36)
    draw_screwdriver(ic, 128, 122, 144)
    for x, y in ((80, 96), (176, 96)):
        peg(ic, x, y)
    # the ruler
    ic.rect(42, 172, 172, 24, rx=2, fill="#000", opacity=0.25, transform="translate(2 3)")
    ic.rect(42, 172, 172, 24, rx=2, fill=ic.lin([(0, "#F4E2BC"), (1, "#D7BC88")]))
    ic.line(42, 172.8, 214, 172.8, stroke="#fff", stroke_width=1.5, opacity=0.8)
    ticks = []
    for i in range(0, 81):
        x = 48 + i * 2
        h = 9 if i % 10 == 0 else 6 if i % 5 == 0 else 3.5
        ticks.append(f"M{x} 172v{h}")
    ic.path("".join(ticks), stroke="#3A2A16", stroke_width=0.7)
    for n in range(0, 8):
        ic.text(str(n), 48 + n * 20, 191, 7, font="mono-semibold", anchor="middle", fill="#3A2A16")
    ic.text("cm", 210, 191, 6, font="mono", anchor="end", fill="#6A5232")
    ic.circle(44.5, 184, 1.5, fill="#6A5232")


@small("Workshop")
def workshop16(ic):
    tile(ic, "#7E5A3A", "#3E2817")
    ic.rect(2, 2, 12, 12, rx=1, fill="#D2A66D")
    for x in (4, 8, 12):
        for y in (4, 8, 12):
            ic.circle(x, y, 0.45, fill="#5B3A1A")
    ic.line(4, 4, 12, 12, stroke="#A9B0B8", stroke_width=1.6, stroke_linecap="round")
    ic.circle(4, 4, 1.5, fill="#A9B0B8")
    ic.line(12, 4, 8.5, 7.5, stroke="#D8452E", stroke_width=2.4, stroke_linecap="round")
    ic.line(8.5, 7.5, 4.5, 11.5, stroke="#D7DBDF", stroke_width=1, stroke_linecap="round")


# --- Game Lobby: a corner of a card table, cards fanned, chips ----------------

def card(ic, rank, x, y, w=50, h=72, big=False):
    red = "#C8372D"
    ic.rect(x, y, w, h, rx=5, fill=ic.lin([(0, "#FFFFFF"), (1, "#ECE7DC")], 0, 0, 1, 1), stroke="#000", stroke_opacity=0.12)
    ic.text(rank, x + 8, y + 15, 12, font="sans-semibold", anchor="middle", fill=red)
    heart(ic, x + 8, y + 22, 8, fill=red)
    if big:
        heart(ic, x + w / 2, y + h / 2 + 4, 26, fill=red)
        ic.text(rank, x + w - 8, y + h - 15, 12, font="sans-semibold", anchor="middle", fill=red, transform=rot(180, x + w - 8, y + h - 19))


@icon("GameLobby")
def gamelobby(ic):
    tile(ic, "#2A6A48", "#0E3321")
    shadow(ic, 128, 214, 102, 12)
    # the table: a padded rail round the felt
    ic.rect(22, 30, 212, 182, rx=40, fill=leather(ic, "#5A3424", "#24120A"))
    ic.rect(23, 31, 210, 180, rx=39, fill="none", stroke="#C98C66", stroke_opacity=0.35, stroke_width=2)
    ic.rect(28, 36, 200, 170, rx=34, fill="none", stroke="#D9A56E", stroke_opacity=0.35, stroke_width=1, stroke_dasharray="3 2.5")
    ic.rect(36, 44, 184, 154, rx=26, fill=felt(ic, "#3A9A63", "#185C38"))
    ic.path("M36 70a26 26 0 0 1 26-26h158", fill="none", stroke="#000", stroke_opacity=0.35, stroke_width=3)
    gold = "#E2BE68"
    ic.path("M54 138A170 170 0 0 1 202 138", fill="none", stroke=gold, stroke_opacity=0.7, stroke_width=1.5)
    arc_text(ic, "TABLE 3 · PAYS 3 TO 2", 128, 238, 168, 0, 8, font="sans-semibold", spacing=0.8, fill=gold, opacity=0.85)
    # chips: a stack and two loose
    def chip_stack(cx, base, n, colours):
        for i in range(n):
            y = base - i * 5.5
            c = colours[i % len(colours)]
            ic.path(f"M{cx - 20} {y}v5.5a20 7.5 0 0 0 40 0v-5.5z", fill=c)
            ic.path(f"M{cx - 20} {y}v5.5a20 7.5 0 0 0 40 0v-5.5z", fill=ic.lin([(0, "#fff", 0.25), (0.5, "#fff", 0), (1, "#000", 0.35)], 0, 0, 1, 0))
            for dx in (-14, -2, 10):
                ic.rect(cx + dx, y + 1, 4, 4.5 if dx != -14 else 4, fill="#F4EFE4", opacity=0.9)
        y = base - (n - 1) * 5.5
        c = colours[(n - 1) % len(colours)]
        ic.ellipse(cx, y, 20, 7.5, fill=c)
        ic.ellipse(cx, y, 20, 7.5, fill="none", stroke="#F4EFE4", stroke_width=3, stroke_dasharray="4 6.5")
        ic.ellipse(cx, y, 13, 4.8, fill="none", stroke="#F4EFE4", stroke_opacity=0.7, stroke_width=0.8)
        ic.text("25", cx, y + 2.6, 7, font="sans-bold", anchor="middle", fill="#F4EFE4", transform=f"translate({cx} {y}) scale(1 .6) translate({-cx} {-y})")
    ic.ellipse(184, 172, 26, 10, fill="#000", opacity=0.3)
    chip_stack(182, 160, 7, ["#C8372D", "#C8372D", "#1E1E20", "#C8372D", "#2463AE", "#C8372D", "#C8372D"])
    chip_stack(150, 186, 2, ["#2E8A5F", "#1E1E20"])
    # the hand: a royal flush in hearts, fanned
    px, py = 96, 200
    for i, (rank, a) in enumerate((("10", -36), ("J", -18), ("Q", 0), ("K", 18), ("A", 36))):
        with ic.g(transform=rot(a, px, py)):
            ic.rect(px - 25, py - 112, 50, 72, rx=5, fill="#000", opacity=0.18, transform="translate(2 3)")
            card(ic, rank, px - 25, py - 112, big=(rank == "A"))


@small("GameLobby")
def gamelobby16(ic):
    tile(ic, "#2A6A48", "#0E3321")
    ic.rect(3, 4, 6, 8.5, rx=0.8, fill="#E9E4D8", transform=rot(-15, 6, 8))
    ic.rect(5.5, 3.5, 6, 8.5, rx=0.8, fill="#FFFFFF", transform=rot(10, 8.5, 8))
    ic.circle(8.6, 7.6, 1.6, fill="#C8372D")
    ic.ellipse(11.5, 12.5, 3, 1.5, fill="#7A1A10")
    ic.ellipse(11.5, 11.7, 3, 1.5, fill="#C8372D")


# --- Chinese Checkers: a star board in wood, marbles in six colours -----------

def cc_holes(s, cx, cy):
    """The 121 holes of the star, as (x, y, region): region 0..5 for the
    six points (top, upper right, lower right, bottom, lower left, upper
    left), None for the centre."""
    h = s * math.sqrt(3) / 2
    out = []
    for j in range(17):
        up = j + 1 if j <= 12 else 0
        down = 17 - j if j >= 4 else 0
        n = max(up, down)
        for i in range(n):
            x = cx + (i - (n - 1) / 2) * s
            y = cy + (j - 8) * h
            k = i - (n - 1) / 2  # from the middle of the row, in holes
            if j <= 3:
                reg = 0
            elif j >= 13:
                reg = 3
            elif j <= 7 and abs(k) > (j + 1 - 1) / 2:
                reg = 1 if k > 0 else 5
            elif j >= 9 and abs(k) > (17 - j - 1) / 2:
                reg = 2 if k > 0 else 4
            else:
                reg = None
            out.append((x, y, reg))
    return out


MARBLES = ["#D23A2C", "#F0B232", "#2E9A58", "#2B6FC4", "#7A4AB2", "#F2EEE4"]


@icon("ChineseCheckers")
def chinesecheckers(ic):
    tile(ic, "#6E4A30", "#331F12")
    shadow(ic, 128, 216, 96, 12)
    cx, cy, r = 128, 120, 100
    ic.ellipse(cx, cy + 7, r, r, fill="#4A2A12")
    ic.circle(cx, cy, r, fill=ic.rad([(0, "#E9C48E"), (0.7, "#CF9A5C"), (1, "#A86F38")], cx=0.38, cy=0.32, r=0.8))
    grain = ic.clip(f'<circle cx="{cx}" cy="{cy}" r="{r}"/>')
    with ic.g(clip_path=grain, fill="none", stroke="#8A5626", stroke_opacity=0.18, stroke_width=1.2):
        for k in range(-5, 6):
            ic.path(f"M20 {cy + k * 17}C80 {cy + k * 17 - 10} 150 {cy + k * 17 + 12} 240 {cy + k * 17 - 4}")
    ic.circle(cx, cy, r - 1, fill="none", stroke="#FFF0D4", stroke_opacity=0.5, stroke_width=2)
    ic.circle(cx, cy, r - 6, fill="none", stroke="#7A4A20", stroke_opacity=0.35, stroke_width=1)
    s = 12.6
    h = s * math.sqrt(3) / 2
    # the six points, painted
    R = 8 * h + 6
    tri = [polar(cx, cy, R, a) for a in range(0, 360, 60)]
    inner = [polar(cx, cy, 4 * s + 4, a + 30) for a in range(0, 360, 60)]
    paint = ["#D23A2C", "#E9A322", "#2E9A58", "#2B6FC4", "#7A4AB2", "#E8E0CF"]
    for i in range(6):
        a, b = inner[(i - 1) % 6], inner[i]
        ic.poly([a, tri[i], b], fill=paint[i], opacity=0.42, stroke=paint[i], stroke_width=2, stroke_linejoin="round")
    ic.poly([p for i in range(6) for p in (tri[i], inner[i])], fill="none", stroke="#7A4A20", stroke_opacity=0.45, stroke_width=1.2, stroke_linejoin="round")
    holes = cc_holes(s, cx, cy)
    for x, y, _ in holes:
        ic.circle(x, y, 2.6, fill="#5A3416")
        ic.circle(x + 0.5, y + 0.6, 2.2, fill="#3A1F0A")
    grads = [ic.rad([(0, "#fff", 0.95), (0.25, c), (1, _shade(c))], cx=0.35, cy=0.3, r=0.75) for c in MARBLES]
    moved = {(0, 9): (cx - 0.5 * s, cy - 3 * h), (3, 2): (cx + s, cy + 2 * h), (5, 9): (cx - 2 * s, cy - 0 * h),
             (1, 9): (cx + 1.5 * s, cy - h)}
    counts = [0] * 6
    marbles = []
    for x, y, reg in holes:
        if reg is None:
            continue
        key = (reg, counts[reg])
        counts[reg] += 1
        if key in moved:
            x, y = moved[key]
        marbles.append((y, x, reg))
    for y, x, reg in sorted(marbles):
        ic.circle(x + 1.2, y + 1.8, 5.4, fill="#2A1404", opacity=0.35)
        ic.circle(x, y, 5.4, fill=grads[reg])


def _shade(c):
    r, g, b = (int(c[i:i + 2], 16) for i in (1, 3, 5))
    return "#{:02X}{:02X}{:02X}".format(int(r * 0.45), int(g * 0.45), int(b * 0.45))


@small("ChineseCheckers")
def chinesecheckers16(ic):
    tile(ic, "#6E4A30", "#331F12")
    ic.circle(8, 8, 6.4, fill="#D6A468")
    for i, c in enumerate(MARBLES):
        x, y = polar(8, 8, 4.2, i * 60)
        ic.circle(x, y, 1.25, fill=c)
    ic.circle(8, 8, 0.9, fill="#5A3416")


# --- Minesweeper: a raised grid of tiles, a flag, numbers, one sea mine -------

NUM_COLOURS = {1: "#2B5FD9", 2: "#2E8B3E", 3: "#D2392B"}


def flag(ic, x, y, k=1.0):
    """A red flag on a stand, its foot centred at x, y."""
    ic.rect(x - 8 * k, y - 3 * k, 16 * k, 3 * k, rx=1 * k, fill="#1E1F21")
    ic.rect(x - 4.5 * k, y - 6 * k, 9 * k, 3 * k, rx=1 * k, fill="#2E3033")
    ic.rect(x - 0.9 * k, y - 22 * k, 1.8 * k, 16 * k, fill="#2E3033")
    ic.path(f"M{x + 0.9 * k:g} {y - 23 * k:g}L{x - 12 * k:g} {y - 17.5 * k:g}L{x + 0.9 * k:g} {y - 12 * k:g}Z", fill="#D8352A")
    ic.path(f"M{x - 0.4 * k:g} {y - 21.4 * k:g}L{x - 8 * k:g} {y - 18 * k:g}", stroke="#FF8A7A", stroke_width=1 * k, opacity=0.8)


def sea_mine(ic, x, y, r):
    for a in range(0, 360, 45):
        ax, ay = polar(x, y, r + 3.5, a)
        ic.line(x, y, ax, ay, stroke="#1B1C1E", stroke_width=2.6)
        ic.circle(ax, ay, 2.1, fill="#1B1C1E")
    ic.circle(x, y, r, fill=ic.rad([(0, "#6B7078"), (0.45, "#2A2C30"), (1, "#0C0D0F")], cx=0.35, cy=0.3, r=0.75))
    ic.circle(x - r * 0.35, y - r * 0.38, r * 0.25, fill="#fff", opacity=0.7)


def led(ic, x, y, digits):
    """A red LED counter: three digits, their unlit 8s behind."""
    ic.rect(x, y, 40, 20, rx=2, fill="#120606")
    ic.text("888", x + 37, y + 16.5, 17, font="mono-semibold", anchor="end", fill="#FF3B2A", opacity=0.12)
    ic.text(digits, x + 37, y + 16.5, 17, font="mono-semibold", anchor="end", fill="#FF4A36")


@icon("Minesweeper")
def minesweeper(ic):
    tile(ic, "#6C7768", "#2E362C")
    shadow(ic, 128, 218, 98, 12)
    n, pitch, t = 5, 31, 29
    w = n * pitch - 2
    x0, y0 = 128 - w / 2, 62
    bx, by, bw, bh = x0 - 12, 22, w + 24, y0 + w + 12 - 22
    # the case
    ic.rect(bx, by, bw, bh, rx=12, fill="#252A24", transform="translate(0 6)")
    ic.rect(bx, by, bw, bh, rx=12, fill=ic.lin([(0, "#9AA396"), (1, "#5A6357")], 0, 0, 1, 1))
    ic.rect(bx + 1, by + 1, bw - 2, bh - 2, rx=11, fill="none", stroke="#fff", stroke_opacity=0.4, stroke_width=2)
    for sx, sy in ((bx + 7, by + 7), (bx + bw - 7, by + 7), (bx + 7, by + bh - 7), (bx + bw - 7, by + bh - 7)):
        ic.circle(sx, sy, 2.4, fill=steel(ic, horizontal=False))
        ic.line(sx - 1.4, sy - 1.4, sx + 1.4, sy + 1.4, stroke="#4E545B", stroke_width=0.8)
    # the counters and the button between them
    ic.rect(x0 - 4, 30, w + 8, 26, rx=4, fill="#3E453C")
    ic.path(f"M{x0 - 4} 56h{w + 8}v-26", fill="none", stroke="#fff", stroke_opacity=0.3, stroke_width=1.5)
    led(ic, x0, 33, "004")
    led(ic, x0 + w - 40, 33, "071")
    ic.circle(128, 43, 10.5, fill=ic.lin([(0, "#E2E5DD"), (1, "#9AA196")], 0, 0, 1, 1))
    ic.circle(128, 43, 7.5, fill=ic.rad([(0, "#FFE680"), (1, "#E3A91E")], cx=0.38, cy=0.32, r=0.75))
    ic.circle(125.4, 41.4, 1, fill="#3A2A08")
    ic.circle(130.6, 41.4, 1, fill="#3A2A08")
    ic.path("M124.6 45a4 3.4 0 0 0 6.8 0", fill="none", stroke="#3A2A08", stroke_width=1.1, stroke_linecap="round")
    # the field
    ic.rect(x0 - 4, y0 - 4, w + 8, w + 8, rx=4, fill="#3E453C")
    ic.path(f"M{x0 - 4} {y0 + w + 4}h{w + 8}v{-(w + 8)}", fill="none", stroke="#fff", stroke_opacity=0.3, stroke_width=1.5)
    mines = {(0, 1), (0, 3), (0, 4), (1, 4), (4, 0), (3, 4)}
    revealed = {(r, c) for r in range(1, 4) for c in range(0, 4)} | {(4, 1), (4, 2), (4, 3), (0, 3)}
    flags = {(4, 0), (1, 4)}
    up = ic.lin([(0, "#E8EAE3"), (1, "#C3C8BD")], 0, 0, 1, 1)
    flat = ic.lin([(0, "#A3A99E"), (1, "#B4B9AE")])
    for r in range(n):
        for c in range(n):
            x, y = x0 + c * pitch, y0 + r * pitch
            if (r, c) in revealed:
                boom = (r, c) in mines
                ic.rect(x, y, t, t, rx=2, fill="#C8392C" if boom else flat)
                ic.path(f"M{x} {y + t}V{y + 2}a2 2 0 0 1 2-2H{x + t}", fill="none", stroke="#000", stroke_opacity=0.28, stroke_width=2)
                if boom:
                    sea_mine(ic, x + t / 2, y + t / 2, 7.5)
                    continue
                k = sum((rr, cc) in mines for rr in (r - 1, r, r + 1) for cc in (c - 1, c, c + 1))
                if k:
                    ic.text(str(k), x + t / 2, y + 21.5, 19, font="sans-bold", anchor="middle", fill=NUM_COLOURS.get(k, "#7A2A7A"))
            else:
                ic.rect(x + 1, y + 2.5, t, t, rx=3, fill="#1E231D", opacity=0.6)
                ic.rect(x, y, t, t, rx=3, fill=up)
                ic.path(f"M{x + 1.5} {y + t - 3}V{y + 3}a2 2 0 0 1 2-2H{x + t - 3}", fill="none", stroke="#fff", stroke_width=2.5, stroke_linecap="round", opacity=0.9)
                ic.path(f"M{x + 3} {y + t - 1.3}H{x + t - 3}a2 2 0 0 0 2-2V{y + 3}", fill="none", stroke="#6F7768", stroke_width=2.5, stroke_linecap="round")
                if (r, c) in flags:
                    flag(ic, x + t / 2 + 3.5, y + t - 4, 1.0)


@small("Minesweeper")
def minesweeper16(ic):
    tile(ic, "#6C7768", "#2E362C")
    ic.rect(1.6, 1.6, 12.8, 12.8, rx=1, fill="#3E453C")
    for r in range(3):
        for c in range(3):
            x, y = 2.2 + c * 4, 2.2 + r * 4
            if (r, c) in ((1, 0), (1, 1)):
                ic.rect(x, y, 3.6, 3.6, fill="#A9AFA4")
            elif (r, c) == (2, 1):
                ic.rect(x, y, 3.6, 3.6, fill="#C8392C")
                ic.circle(x + 1.8, y + 1.8, 1.2, fill="#141516")
            else:
                ic.rect(x, y, 3.6, 3.6, rx=0.4, fill="#E3E6DE")
                ic.path(f"M{x + 3.6} {y}v3.6h-3.6", fill="none", stroke="#7D8578", stroke_width=0.5)
    ic.rect(3.6, 6.8, 0.9, 2.4, fill="#2B5FD9")
    ic.path("M11.6 2.7V5.5", stroke="#1E1F21", stroke_width=0.6)
    ic.path("M11.9 2.6L9 3.8L11.9 5Z", fill="#D8352A")


# --- Small Fortune: two ivory dice on washi banknotes, "10 KAN" ---------------

PIPS = {
    1: [(.5, .5)],
    2: [(.27, .27), (.73, .73)],
    3: [(.25, .25), (.5, .5), (.75, .75)],
    4: [(.27, .27), (.73, .27), (.27, .73), (.73, .73)],
    5: [(.25, .25), (.75, .25), (.5, .5), (.25, .75), (.75, .75)],
    6: [(.28, .24), (.28, .5), (.28, .76), (.72, .24), (.72, .5), (.72, .76)],
}


def die(ic, cx, cy, a, top, left, right):
    """An ivory die seen from above a corner: (cx, cy) is the near top
    corner, a the edge; top, left and right are the faces' numbers."""
    k = 0.866 * a
    lx, ly = cx - k, cy - a / 2
    hexa = [(cx, cy - a), (cx + k, cy - a / 2), (cx + k, cy + a / 2), (cx, cy + a), (cx - k, cy + a / 2), (cx - k, cy - a / 2)]
    ic.poly([(x + 5, y + 6) for x, y in hexa], fill="#2A1C08", opacity=0.3, stroke="#2A1C08", stroke_width=a * 0.16, stroke_linejoin="round", stroke_opacity=0.3)
    ic.poly(hexa, fill="#CFC2A3", stroke="#CFC2A3", stroke_width=a * 0.16, stroke_linejoin="round")
    faces = (
        (f"matrix({k:.3f} {a / 2:.3f} {k:.3f} {-a / 2:.3f} {lx:.2f} {ly:.2f})", top, ("#FFFEF8", "#EEE6D2")),
        (f"matrix({k:.3f} {a / 2:.3f} 0 {a:.3f} {lx:.2f} {ly:.2f})", left, ("#ECE3CC", "#D3C6A6")),
        (f"matrix({k:.3f} {-a / 2:.3f} 0 {a:.3f} {cx:.2f} {cy:.2f})", right, ("#C9B994", "#A8966F")),
    )
    for m, n, (l, d) in faces:
        with ic.g(transform=m):
            ic.rect(0.03, 0.03, 0.94, 0.94, rx=0.16, fill=ic.lin([(0, l), (1, d)], 0, 0, 1, 1))
            for px, py in PIPS[n]:
                if n == 1:
                    ic.circle(px, py, 0.17, fill="#B32A22")
                    ic.circle(px + 0.02, py + 0.025, 0.13, fill="#D9473A")
                else:
                    ic.circle(px, py, 0.085, fill="#2A2420")
    ic.path(f"M{lx + 2:.1f} {ly - 1:.1f}L{cx - 2:.1f} {cy - a + 1:.1f}", stroke="#fff", stroke_width=1.6, stroke_linecap="round", opacity=0.9)


def note(ic, x, y, ink, serial):
    w, h = 176, 94
    ic.rect(x, y, w, h, rx=2, fill=paper(ic, "washi"))
    ic.line(x + 1, y + 0.8, x + w - 1, y + 0.8, stroke="#fff", stroke_width=1.5)
    for i in range(7):
        fx, fy = x + 14 + i * 23, y + 10 + (i * 37) % 70
        ic.path(f"M{fx} {fy}c4-3 8 2 12-1", fill="none", stroke="#9C8E72", stroke_opacity=0.35, stroke_width=0.8)
    ic.rect(x + 6, y + 6, w - 12, h - 12, rx=1, fill="none", stroke=ink, stroke_width=2.2)
    ic.rect(x + 10, y + 10, w - 20, h - 20, fill="none", stroke=ink, stroke_width=0.7, stroke_dasharray="1.5 1.5")
    rx_, ry_ = x + w - 40, y + h / 2
    for rr in (22, 17, 12):
        ic.circle(rx_, ry_, rr, fill="none", stroke=ink, stroke_opacity=0.5, stroke_width=0.8, stroke_dasharray="2.5 1.2")
    mark(ic, rx_ - 9, ry_ - 9, 18, fill=ink, opacity=0.7)
    ic.text("BANK OF INUA", x + 16, y + 23, 7, font="sans-semibold", spacing=0.9, fill=ink)
    ic.text("10", x + 15, y + 54, 30, font="sans-bold", fill=ink)
    ic.text("KAN", x + 17, y + 69, 12, font="sans-condensed", spacing=2.5, fill=ink)
    ic.text(serial, x + 16, y + 80, 6, font="mono", spacing=0.5, fill="#55534E")
    ic.rect(x + 66, y + 32, 18, 18, rx=2, fill="#C8372D", opacity=0.85)
    ic.rect(x + 68.5, y + 34.5, 13, 13, rx=1, fill="none", stroke="#F7F2E7", stroke_width=1.1)
    ic.text("10", x + 75, y + 44.5, 7, font="mono-semibold", anchor="middle", fill="#F7F2E7")


@icon("SmallFortune")
def smallfortune(ic):
    tile(ic, "#B89140", "#6A4C15")
    shadow(ic, 126, 200, 100, 12)
    with ic.g(transform=rot(-9, 122, 106)):
        ic.rect(34, 60, 176, 94, rx=2, fill="#3A2A08", opacity=0.3, transform="translate(3 4)")
        note(ic, 34, 60, "#B5432F", "No. 0412 KN")
    with ic.g(transform=rot(4, 128, 140)):
        ic.rect(36, 96, 176, 94, rx=2, fill="#3A2A08", opacity=0.3, transform="translate(3 4)")
        note(ic, 36, 96, "#2E4A7A", "No. 0417 KN")
    die(ic, 162, 106, 38, 1, 2, 3)
    die(ic, 200, 150, 32, 6, 5, 4)


@small("SmallFortune")
def smallfortune16(ic):
    tile(ic, "#B89140", "#6A4C15")
    ic.rect(1.5, 6, 11, 7, rx=0.4, fill="#F2ECDF", transform=rot(-8, 7, 9.5))
    ic.rect(3, 7.5, 3, 3, fill="#2E4A7A", transform=rot(-8, 7, 9.5))
    ic.poly([(11, 3), (14, 4.6), (14, 8.4), (11, 10), (8, 8.4), (8, 4.6)], fill="#D3C6A6")
    ic.poly([(11, 3), (14, 4.6), (11, 6.2), (8, 4.6)], fill="#FFFDF4")
    ic.poly([(11, 6.2), (14, 4.6), (14, 8.4), (11, 10)], fill="#B3A27C")
    ic.circle(11, 4.6, 0.8, fill="#C8372D")


# --- Space Pinball: a playfield, chrome ball, flippers, bumpers, stars --------

def flipper(ic, px, py, tx, ty):
    a = math.degrees(math.atan2(ty - py, tx - px))
    ln = math.hypot(tx - px, ty - py)
    d = f"M0 -7A7 7 0 0 0 0 7L{ln:.1f} 3.6A3.6 3.6 0 0 0 {ln:.1f} -3.6Z"
    with ic.g(transform=f"translate({px} {py}) rotate({a:.1f})"):
        ic.path(d, fill="#000", opacity=0.35, transform="translate(1.5 3)")
        ic.path(d, fill="#D8352A")
        ic.path("M1 -5A5 5 0 0 0 1 5L" + f"{ln - 1:.1f} 2L{ln - 1:.1f} -2Z", fill="#F5F2EA")
        ic.circle(0, 0, 2, fill="#9AA1A9")


def bumper(ic, x, y, cap):
    ic.circle(x + 2, y + 4, 15, fill="#000", opacity=0.35)
    ic.circle(x, y, 15, fill="#E9ECEF")
    ic.circle(x, y, 15, fill="none", stroke="#8A9199", stroke_width=1)
    ic.circle(x, y, 12.5, fill=ic.rad([(0, "#F8F9FA"), (1, "#8A9199")], cx=0.35, cy=0.3, r=0.8))
    ic.circle(x, y, 10, fill=ic.rad([(0, "#fff", 0.9), (0.3, cap), (1, _shade(cap))], cx=0.35, cy=0.3, r=0.8))
    ic.poly(star(x, y, 6, 2.6), fill="#FFF6D8", opacity=0.9)


@icon("SpacePinball")
def spacepinball(ic):
    tile(ic, "#2E3F7E", "#0D1534")
    shadow(ic, 128, 218, 88, 11)
    outer = "M44 214V84C44 46 82 22 128 22C174 22 212 46 212 84V214Z"
    field = "M52 210V86C52 54 86 30 128 30C170 30 204 54 204 86V210Z"
    ic.path(outer, fill=ic.lin([(0, "#C8CDD3"), (0.5, "#7C838C"), (1, "#3E444C")], 0, 0, 1, 1))
    ic.path("M45 210V84C45 47 83 23 128 23", fill="none", stroke="#fff", stroke_opacity=0.7, stroke_width=1.5)
    ic.path(field, fill=ic.rad([(0, "#2A2F7A"), (0.6, "#141848"), (1, "#070A22")], cx=0.45, cy=0.35, r=0.8))
    fclip = ic.clip(f'<path d="{field}"/>')
    with ic.g(clip_path=fclip):
        ic.circle(92, 74, 46, fill=ic.rad([(0, "#7A3FA8", 0.55), (1, "#7A3FA8", 0)]))
        ic.circle(170, 150, 40, fill=ic.rad([(0, "#2E8FB0", 0.4), (1, "#2E8FB0", 0)]))
        rnd = random.Random(7)
        for _ in range(70):
            ic.circle(rnd.uniform(52, 204), rnd.uniform(30, 210), rnd.choice((0.5, 0.7, 0.9, 1.2)), fill="#fff", opacity=rnd.uniform(0.35, 0.95))
        for sx, sy in ((70, 120), (186, 58), (110, 160)):
            ic.poly(star(sx, sy, 4, 1.1, 4), fill="#fff", opacity=0.9)
        # a ringed planet
        ic.circle(176, 104, 13, fill=ic.rad([(0, "#F6C36A"), (1, "#B0582A")], cx=0.35, cy=0.3, r=0.8))
        ic.ellipse(176, 104, 22, 5, fill="none", stroke="#F2DDB0", stroke_width=2, transform=rot(-18, 176, 104), opacity=0.85)
    # top lanes
    for x in (102, 128, 154):
        ic.rect(x - 2, 40, 4, 22, rx=2, fill=steel(ic, horizontal=True))
    for x in (115, 141):
        ic.circle(x, 56, 4.5, fill="#F2C45C", opacity=0.9)
    ic.text("ORBIT", 128, 74, 7, font="mono-semibold", anchor="middle", spacing=1.5, fill="#9FD8FF")
    # bumpers
    bumper(ic, 100, 98, "#E0463A")
    bumper(ic, 156, 98, "#F2B232")
    bumper(ic, 128, 132, "#3FA0E0")
    # inserts and their legend
    for i, y in enumerate((150, 159, 168)):
        ic.path(f"M128 {y - 6}l6 7h-12z", fill="#F2C45C", opacity=0.95 if i == 0 else 0.45)
    ic.text("EXTRA BALL", 128, 180, 6, font="mono-semibold", anchor="middle", spacing=0.6, fill="#F2C45C", opacity=0.8)
    # slingshots and the flippers
    for sgn, x in ((1, 64), (-1, 192)):
        ic.poly([(x, 142), (x, 170), (x + sgn * 20, 178)], fill="#EDEFF2")
        ic.line(x + sgn * 2, 146, x + sgn * 18, 175, stroke="#D8352A", stroke_width=3, stroke_linecap="round")
        ic.line(x, 178, x + sgn * 22, 190, stroke="#C3C8CE", stroke_width=3, stroke_linecap="round")
    flipper(ic, 86, 190, 117, 199)
    flipper(ic, 170, 190, 139, 199)
    # the apron, printed
    ic.path("M52 210V196H104L114 204H142L152 196H204V210Z", fill="#000", opacity=0.35, transform="translate(0 -2)")
    ic.path("M52 210V198H104L114 206H142L152 198H204V210Z", fill=ic.lin([(0, "#E9ECEF"), (1, "#9AA1A9")]))
    ic.path("M52 198.6H104L114 206.6H142L152 198.6H204", fill="none", stroke="#fff", stroke_width=1)
    ic.text("SPACE", 78, 207, 6.5, font="sans-bold", anchor="middle", spacing=0.6, fill="#2E3F7E")
    ic.text("PINBALL", 178, 207, 6.5, font="sans-bold", anchor="middle", spacing=0.6, fill="#2E3F7E")
    # the glass over it
    ic.path("M52 210V86C52 54 86 30 128 30H150L60 210Z", fill=glare(ic, 0.8))
    # the ball
    ic.ellipse(152, 166, 10, 4, fill="#000", opacity=0.4)
    ic.circle(150, 158, 9.5, fill=ic.rad([(0, "#FFFFFF"), (0.35, "#D9DDE2"), (0.7, "#6C737C"), (1, "#2A2E35")], cx=0.38, cy=0.32, r=0.75))
    ic.path("M141 160a9.5 9.5 0 0 0 18 0a12 6 0 0 1-18 0z", fill="#1C2250", opacity=0.6)
    ic.circle(146.5, 154, 2.6, fill="#fff")


@small("SpacePinball")
def spacepinball16(ic):
    tile(ic, "#2E3F7E", "#0D1534")
    ic.path("M3 14V6C3 3.5 5.2 2 8 2C10.8 2 13 3.5 13 6V14Z", fill="#9AA1A9")
    ic.path("M4 14V6C4 4 5.7 3 8 3C10.3 3 12 4 12 6V14Z", fill="#141848")
    ic.circle(8, 6.2, 1.6, fill="#E0463A")
    ic.circle(9.5, 9.3, 1.2, fill="#E9ECEF")
    ic.line(4.6, 12, 7, 13, stroke="#F5F2EA", stroke_width=1.1, stroke_linecap="round")
    ic.line(11.4, 12, 9, 13, stroke="#F5F2EA", stroke_width=1.1, stroke_linecap="round")
