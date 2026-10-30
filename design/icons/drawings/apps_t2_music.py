"""The inua-objects theme, music and audio apps (t2-music): Rhythmbox,
Lollypop, Amberol, Elisa, Strawberry, Shortwave, Podcasts, Cozy,
EasyEffects, Volume Control, Helvum, Ardour, LMMS, MuseScore, REAPER, TIDAL
(docs/feat/object-icons.md, Part 2). Each is its own object in the brand's
colours; inua's Music (a record and sleeve) is not repeated."""

import math

from lib import (brass, glare, graphite, icon, leather, paper, polar, shadow, small, steel, tile, wood)


# --- shared parts ----------------------------------------------------------

def _screw(ic, x, y, r=2.6, deg=35):
    ic.circle(x, y, r, fill=steel(ic, False))
    ic.circle(x, y, r, fill="none", stroke="#000", stroke_opacity=0.35, stroke_width=0.6)
    a, b = polar(x, y, r * 0.8, deg), polar(x, y, r * 0.8, deg + 180)
    ic.line(a[0], a[1], b[0], b[1], stroke="#2A2C30", stroke_width=0.8)


def _knob(ic, cx, cy, r, deg=0, face=None, rim="#141518", pointer="#F1F1EF", ring=None):
    """A round knob from above: its shadow, a knurled skirt, a face lit from
    the top left, and a pointer at deg (0 up)."""
    ic.circle(cx + r * 0.12, cy + r * 0.2, r * 1.04, fill="#000", opacity=0.35)
    ic.circle(cx, cy, r, fill=rim)
    if r >= 9:
        ic.circle(cx, cy, r - 0.8, fill="none", stroke="#fff", stroke_opacity=0.16, stroke_width=1.4,
                  stroke_dasharray="1.2 1.6")
    ic.circle(cx, cy, r * 0.8, fill=face or ic.rad([(0, "#5A5E66"), (1, "#202226")], cx=0.35, cy=0.3, r=0.8))
    ic.circle(cx - r * 0.04, cy - r * 0.04, r * 0.8, fill="none", stroke="#fff", stroke_opacity=0.22,
              stroke_width=max(0.6, r * 0.05))
    if ring:
        ic.circle(cx, cy, r * 0.8, fill="none", stroke=ring, stroke_width=max(0.8, r * 0.08))
    a, b = polar(cx, cy, r * 0.25, deg), polar(cx, cy, r * 0.72, deg)
    ic.line(a[0], a[1], b[0], b[1], stroke=pointer, stroke_width=max(0.9, r * 0.1), stroke_linecap="round")


def _note(ic, x, y, s, **kw):
    """An eighth note, its head's centre at (x, y), s its head's width."""
    h = s * 0.5
    ic.ellipse(x, y, h, h * 0.72, transform=f"rotate(-22 {x} {y})", **kw)
    sx = x + h * 0.86
    ic.rect(sx - s * 0.09, y - s * 2.1, s * 0.18, s * 2.1, **kw)
    ic.path(f"M{sx:.1f} {y - s * 2.1:.1f}c{s * 0.1:.1f} {s * 0.5:.1f} {s * 0.9:.1f} {s * 0.6:.1f} {s * 0.6:.1f} "
            f"{s * 1.3:.1f}c{s * 0.05:.1f} {-s * 0.55:.1f} {-s * 0.4:.1f} {-s * 0.7:.1f} {-s * 0.6:.1f} "
            f"{-s * 0.75:.1f}z", **kw)


def _leds(ic, x, y, w, h, n, lit, horizontal=False, gap=1.2):
    """A meter of n LED segments, lit up to lit: green, amber, red."""
    for k in range(n):
        f = k / (n - 1)
        col = "#5BE07A" if f < 0.65 else "#F2C14A" if f < 0.88 else "#F0533F"
        on = k < lit
        if horizontal:
            sw = (w - gap * (n - 1)) / n
            ic.rect(x + k * (sw + gap), y, sw, h, rx=0.6, fill=col if on else "#2A2C30", opacity=1 if on else 0.9)
        else:
            sh = (h - gap * (n - 1)) / n
            ic.rect(x, y + h - (k + 1) * sh - k * gap, w, sh, rx=0.6, fill=col if on else "#2A2C30")


# --- Rhythmbox: a bookshelf speaker, its orange cone -------------------------

def _driver(ic, cx, cy, r, cone):
    ic.circle(cx, cy, r + 3, fill=ic.lin([(0, "#0B0B0C"), (1, "#3A3B40")], 0, 0, 1, 1))
    ic.circle(cx, cy, r, fill=ic.lin([(0, "#55575E"), (1, "#1C1D20")], 0, 0, 1, 1))
    ic.circle(cx, cy, r * 0.9, fill=ic.rad([(0, "#1A1A1C"), (0.85, "#2E2F33"), (1, "#121214")]))
    ic.circle(cx - 0.8, cy - 0.8, r * 0.86, fill="none", stroke="#fff", stroke_opacity=0.18,
              stroke_width=max(1, r * 0.04), stroke_dasharray=f"{r * 1.6:.0f} {r * 8:.0f}",
              transform=f"rotate(200 {cx} {cy})")
    ic.circle(cx, cy, r * 0.76, fill=cone)
    for k in (0.62, 0.5):
        ic.circle(cx, cy, r * k, fill="none", stroke="#7A3208", stroke_opacity=0.18, stroke_width=1)
    ic.circle(cx, cy, r * 0.76, fill="none", stroke="#000", stroke_opacity=0.25)
    ic.circle(cx, cy, r * 0.3, fill=ic.rad([(0, "#FFE2A0"), (0.7, "#F2A23A"), (1, "#C86414")], cx=0.38, cy=0.32,
                                            r=0.75))
    ic.circle(cx, cy, r * 0.3, fill="none", stroke="#6A2A06", stroke_opacity=0.35)
    ic.ellipse(cx - r * 0.1, cy - r * 0.13, r * 0.11, r * 0.06, fill="#fff", opacity=0.6,
               transform=f"rotate(-35 {cx - r * 0.1} {cy - r * 0.13})")
    for d in (45, 135, 225, 315):
        x, y = polar(cx, cy, r + 0.2, d)
        ic.circle(x, y, max(1.2, r * 0.045), fill="#8A8F97")


@icon("rhythmbox", kind="app", names=["org.gnome.Rhythmbox", "org.gnome.Rhythmbox3", "rhythmbox"],
      title="Rhythmbox")
def rhythmbox(ic):
    tile(ic, "#D67A2E", "#7A3410")
    shadow(ic, 128, 214, 78, 11)
    # the cabinet, walnut
    ic.rect(60, 24, 136, 192, rx=12, fill=wood(ic, "#6E4428", "#2A170B"))
    ic.rect(60.75, 24.75, 134.5, 190.5, rx=11.25, fill="none", stroke="#fff", stroke_opacity=0.16, stroke_width=1.5)
    # the baffle
    ic.rect(70, 34, 116, 172, rx=7, fill=ic.lin([(0, "#2E2F33"), (1, "#141416")]))
    ic.line(72, 34.8, 184, 34.8, stroke="#fff", stroke_opacity=0.12)
    cone = ic.rad([(0, "#FFC266"), (0.55, "#F08A24"), (1, "#A9480C")], cx=0.38, cy=0.32, r=0.8)
    _driver(ic, 128, 70, 17, ic.rad([(0, "#FFE7B8"), (0.6, "#E0A050"), (1, "#8A4A10")], cx=0.38, cy=0.32, r=0.8))
    _driver(ic, 128, 142, 45, cone)
    # the maker's name at the foot
    ic.text("rhythmbox", 128, 202, 8, font="sans-semibold", anchor="middle", spacing=0.4, fill="#F0A050")
    for x, y in ((78, 42), (178, 42), (78, 198), (178, 198)):
        _screw(ic, x, y, 2.4)


@small("rhythmbox")
def rhythmbox16(ic):
    tile(ic, "#D67A2E", "#7A3410")
    ic.rect(3.5, 1.5, 9, 13, rx=1, fill="#3A2414")
    ic.rect(4.3, 2.3, 7.4, 11.4, rx=0.6, fill="#1C1C1F")
    ic.circle(8, 4.4, 1.3, fill="#E0A050")
    ic.circle(8, 9.6, 3.3, fill="#2E2F33")
    ic.circle(8, 9.6, 2.6, fill="#F08A24")
    ic.circle(8, 9.6, 0.9, fill="#FFD27A")


# --- Lollypop: a swirled lollipop, a tag on its ribbon -----------------------

def _spiral(cx, cy, r0, r1, turns, phase):
    pts = []
    n = int(turns * 60)
    for k in range(n + 1):
        t = k / n
        x, y = polar(cx, cy, r0 + (r1 - r0) * t, phase + t * turns * 360)
        pts.append(f"{x:.1f} {y:.1f}")
    return "M" + "L".join(pts)


@icon("lollypop", kind="app", names=["lollypop", "org.gnome.Lollypop"], title="Lollypop")
def lollypop(ic):
    tile(ic, "#3FA0B6", "#17566A")
    shadow(ic, 136, 216, 62, 9)
    cx, cy, r = 118, 96, 68
    # the stick
    ic.line(132, 150, 166, 214, stroke="#000", stroke_opacity=0.25, stroke_width=11, stroke_linecap="round",
            transform="translate(3 3)")
    ic.line(132, 150, 166, 214, stroke=ic.lin([(0, "#FFFFFF"), (1, "#D9D2C2")], 0, 0, 1, 0, units=None),
            stroke_width=10, stroke_linecap="round")
    ic.line(130, 152, 163, 213, stroke="#fff", stroke_opacity=0.8, stroke_width=2.5, stroke_linecap="round")
    ic.line(136, 150, 169, 211, stroke="#A49C8C", stroke_opacity=0.6, stroke_width=2, stroke_linecap="round")
    # the candy
    ic.circle(cx + 3, cy + 5, r, fill="#000", opacity=0.25)
    ic.circle(cx, cy, r, fill=ic.rad([(0, "#FF9CC2"), (0.7, "#E8488A"), (1, "#A81C56")], cx=0.38, cy=0.34, r=0.75))
    clip = ic.clip(f'<circle cx="{cx}" cy="{cy}" r="{r - 1}"/>')
    with ic.g(clip_path=clip):
        ic.path(_spiral(cx, cy, 2, r + 14, 3.2, 0), fill="none", stroke="#FFF6FA", stroke_width=11,
                stroke_linecap="round", opacity=0.95)
        ic.path(_spiral(cx, cy, 2, r + 14, 3.2, 180), fill="none", stroke="#FFC23D", stroke_width=8,
                stroke_linecap="round")
        ic.circle(cx, cy, r, fill=ic.rad([(0, "#fff", 0), (0.6, "#000", 0), (1, "#4A0A28", 0.45)],
                                         cx=0.36, cy=0.32, r=0.75))
    ic.circle(cx, cy, r, fill="none", stroke="#7A1240", stroke_opacity=0.5, stroke_width=1.5)
    ic.ellipse(cx - 30, cy - 34, 22, 11, fill="#fff", opacity=0.55, transform=f"rotate(-40 {cx - 30} {cy - 34})")
    ic.ellipse(cx - 42, cy - 12, 4, 7, fill="#fff", opacity=0.35, transform=f"rotate(-20 {cx - 42} {cy - 12})")
    # the ribbon, tied where the stick meets the candy, and its tag
    bx, by = 140, 166
    ic.path(f"M{bx} {by}l-12 24l7 -3l4 6z", fill="#6A30B0")
    ic.path(f"M{bx} {by}l14 21l-7 0l-1 7z", fill="#7A3FC8")
    ic.path(f"M{bx} {by}c-10 -14 -28 -14 -26 -1c1 9 16 8 26 1z", fill="#8A4ADA")
    ic.path(f"M{bx} {by}c10 -14 28 -14 26 -1c-1 9 -16 8 -26 1z", fill="#9A5AE8")
    ic.path(f"M{bx - 4} {by - 1}c-6 -7 -15 -8 -18 -3", fill="none", stroke="#4A1A8A", stroke_opacity=0.5,
            stroke_width=1.2)
    ic.path(f"M{bx + 4} {by - 1}c6 -7 15 -8 18 -3", fill="none", stroke="#4A1A8A", stroke_opacity=0.5,
            stroke_width=1.2)
    ic.path(f"M{bx - 22} {by - 6}c3 -6 10 -7 15 -3", fill="none", stroke="#fff", stroke_opacity=0.45, stroke_width=1.4,
            stroke_linecap="round")
    ic.ellipse(bx, by, 5, 5.5, fill="#6A30B0")
    ic.ellipse(bx - 1.2, by - 1.6, 2, 1.6, fill="#fff", opacity=0.35)
    with ic.g(transform=f"rotate(14 {bx + 20} {by + 10})"):
        ic.line(bx + 2, by + 2, bx + 22, by + 12, stroke="#F4EEE2", stroke_width=1)
        ic.path(f"M{bx + 22} {by + 6}h40a3 3 0 0 1 3 3v12a3 3 0 0 1-3 3h-40l-6 -9z", fill=paper(ic, "cream"))
        ic.circle(bx + 21, by + 15, 1.6, fill="#C9BFA9")
        ic.text("lollypop", bx + 44, by + 19, 11, font="hand", anchor="middle", fill="#8A2A5A")


@small("lollypop")
def lollypop16(ic):
    tile(ic, "#3FA0B6", "#17566A")
    ic.line(8.6, 9, 11, 14, stroke="#F4EEE2", stroke_width=1.3, stroke_linecap="round")
    ic.circle(7.4, 6.4, 4.8, fill="#E8488A")
    ic.path(_spiral(7.4, 6.4, 0.4, 4.6, 1.6, 0), fill="none", stroke="#FFF6FA", stroke_width=1.1)
    ic.circle(5.8, 4.6, 0.9, fill="#fff", opacity=0.6)


# --- Amberol: a little jukebox, its tubes glowing amber ----------------------

@icon("amberol", kind="app", names=["amberol", "io.bassi.Amberol"], title="Amberol")
def amberol(ic):
    tile(ic, "#6A2E40", "#2C0E1A")
    shadow(ic, 128, 216, 82, 11)
    cx, cy = 128, 100
    amber = ic.lin([(0, "#FFE6A0"), (0.5, "#FFB43A"), (1, "#E0741A")])
    # the cabinet
    body = f"M56 210V{cy}A72 72 0 0 1 200 {cy}V210z"
    ic.path(body, fill=wood(ic, "#7A4426", "#2E1508"))
    ic.path(body, fill="none", stroke="#fff", stroke_opacity=0.14, stroke_width=1.5)
    # the arch of light between chrome bands
    ic.path(f"M66 210V{cy}A62 62 0 0 1 190 {cy}V210", fill="none", stroke=steel(ic), stroke_width=16)
    ic.path(f"M66 210V{cy}A62 62 0 0 1 190 {cy}V210", fill="none", stroke=amber, stroke_width=10)
    ic.path(f"M63 206V{cy}A65 65 0 0 1 120 35.5", fill="none", stroke="#fff", stroke_opacity=0.55, stroke_width=1.6)
    for y in range(116, 206, 12):
        ic.line(61, y, 71, y, stroke="#9A4A10", stroke_opacity=0.5)
        ic.line(185, y, 195, y, stroke="#9A4A10", stroke_opacity=0.5)
    # the dome window, the record inside
    win = f"M76 {cy + 8}V{cy}A52 52 0 0 1 180 {cy}V{cy + 8}z"
    ic.path(win, fill=ic.rad([(0, "#4A2210"), (1, "#140804")], cx=0.5, cy=0.8, r=0.8))
    wclip = ic.clip(f'<path d="{win}"/>')
    with ic.g(clip_path=wclip):
        ic.ellipse(128, 104, 44, 12, fill="#0C0C0D")
        ic.ellipse(128, 102, 44, 12, fill="#1A1A1C")
        for k in (36, 28):
            ic.ellipse(128, 102, k, k * 0.27, fill="none", stroke="#fff", stroke_opacity=0.08)
        ic.ellipse(128, 102, 13, 3.6, fill="#FFB43A")
        ic.path("M168 70 l-24 30", stroke=steel(ic), stroke_width=3, stroke_linecap="round")
        ic.circle(168, 70, 4, fill=steel(ic, False))
    ic.path(win, fill=glare(ic, 1.2))
    ic.path(f"M84 {cy}A44 44 0 0 1 116 58", fill="none", stroke="#fff", stroke_opacity=0.45, stroke_width=2,
            stroke_linecap="round")
    # the title strips
    ic.rect(76, 110, 104, 38, rx=3, fill="#1A0C06")
    for k, (code, song) in enumerate((("A1", "AMBER WAVES"), ("A2", "SLOW BLOOM"), ("B1", "HONEY, LATE"))):
        y = 113 + k * 11.5
        ic.rect(79, y, 98, 9.5, rx=1.2, fill=paper(ic, "cream"))
        ic.text(code, 83, y + 7.2, 6.5, font="mono-semibold", fill="#C0561A")
        ic.text(song, 95, y + 7.2, 6.2, font="sans-semibold", fill="#3A2A20")
    # the grille, lit from behind
    ic.rect(76, 154, 104, 46, rx=4, fill=ic.rad([(0, "#FFD27A"), (0.6, "#F08A24"), (1, "#8A3A0A")], cx=0.5,
                                                    cy=0.4, r=0.7))
    for x in range(82, 180, 8):
        ic.rect(x, 154, 3.4, 46, fill=steel(ic))
    ic.rect(76, 154, 104, 46, rx=4, fill="none", stroke="#000", stroke_opacity=0.35)
    # the plate and the buttons
    ic.rect(100, 150, 56, 9, rx=2, fill=brass(ic))
    ic.text("AMBEROL", 128, 157.4, 6.4, font="mono-semibold", anchor="middle", spacing=1.2, fill="#4A2E10")
    ic.rect(56, 204, 144, 8, rx=2, fill="#1A0A04")


@small("amberol")
def amberol16(ic):
    tile(ic, "#6A2E40", "#2C0E1A")
    ic.path("M3 14V6.5A5 5 0 0 1 13 6.5V14z", fill="#5A2E14")
    ic.path("M4 14V6.5A4 4 0 0 1 12 6.5V14", fill="none", stroke="#FFB43A", stroke_width=1.2)
    ic.path("M5.4 7.6V6.6A2.6 2.6 0 0 1 10.6 6.6V7.6z", fill="#1A0C06")
    ic.rect(5.4, 9.6, 5.2, 3.4, rx=0.4, fill="#F7A23A")
    ic.rect(6.6, 9.6, 0.7, 3.4, fill="#C3C8CE")
    ic.rect(8.7, 9.6, 0.7, 3.4, fill="#C3C8CE")


# --- Elisa: a music box, lid open, its comb and cylinder --------------------

@icon("elisa", kind="app", names=["elisa", "org.kde.elisa"], title="Elisa")
def elisa(ic):
    tile(ic, "#3E3A86", "#17143E")
    shadow(ic, 128, 214, 96, 12)
    # the lid, standing open behind
    ic.path("M54 114L64 34a6 6 0 0 1 6-5h116a6 6 0 0 1 6 5l10 80z", fill=wood(ic, "#A86A3C", "#5A3014"))
    ic.path("M64 110L72 42h112l8 68z", fill=ic.rad([(0, "#3E8ED8"), (0.7, "#1F4E9A"), (1, "#14306A")],
                                                  cx=0.4, cy=0.3, r=0.9))
    ic.path("M64 110L72 42h112l8 68z", fill="none", stroke="#E8C682", stroke_opacity=0.6, stroke_width=1.2)
    # the enamel badge on the lining: a disc and a note
    ic.circle(128, 74, 22, fill="#0E1E44", opacity=0.5, transform="translate(1.5 2)")
    ic.circle(128, 74, 22, fill=brass(ic))
    ic.circle(128, 74, 18, fill=ic.lin([(0, "#5FD3F0"), (0.5, "#3A8AE8"), (1, "#6A4AD0")], 0, 0, 1, 1))
    _note(ic, 124, 82, 9, fill="#fff")
    ic.ellipse(120, 64, 7, 3, fill="#fff", opacity=0.4, transform="rotate(-30 120 64)")
    # the top of the box, its well and the movement inside
    ic.path("M46 114h164l8 34H38z", fill=wood(ic, "#D8A06A", "#9A6030"))
    ic.path("M58 118h140l5 26H53z", fill="#2A1A0E")
    ic.path("M60 120h136", stroke="#000", stroke_opacity=0.4, stroke_width=2)
    ic.rect(72, 121, 84, 10, rx=5, fill=steel(ic, False))
    for k in range(18):
        x = 76 + k * 4.4
        ic.circle(x, 123 + (k * 7 % 5) * 1.4, 0.8, fill="#3A3E44")
    ic.rect(68, 122, 4, 8, rx=1, fill=brass(ic))
    ic.rect(156, 122, 4, 8, rx=1, fill=brass(ic))
    ic.path("M72 132h84l2 9H70z", fill=brass(ic))
    for k in range(16):
        x = 75 + k * 5
        ic.line(x, 132, x, 141, stroke="#6A4A14", stroke_width=0.9)
    ic.rect(166, 122, 22, 18, rx=3, fill=brass(ic))
    ic.circle(177, 131, 5.5, fill=steel(ic, False))
    ic.path("M196 118l5 26", stroke="#fff", stroke_opacity=0.12)
    ic.line(40, 147, 216, 147, stroke="#FFE3B8", stroke_opacity=0.6, stroke_width=1.5)
    # the front
    ic.rect(38, 148, 180, 58, rx=4, fill=wood(ic, "#C48A55", "#6A3C18"))
    for y in (160, 176, 194):
        ic.path(f"M40 {y} q44 -5 88 0 t88 -1", fill="none", stroke="#4A2A10", stroke_opacity=0.18, stroke_width=1.2)
    ic.rect(38, 148, 180, 58, rx=4, fill="none", stroke="#000", stroke_opacity=0.2)
    ic.rect(100, 166, 56, 22, rx=3, fill=brass(ic))
    ic.rect(100, 166, 56, 22, rx=3, fill="none", stroke="#5A3A10", stroke_opacity=0.5)
    ic.text("ELISA", 128, 181.5, 10, font="sans-semibold", anchor="middle", spacing=2.2, fill="#4A2E10")
    # the winding key on the side
    ic.rect(218, 172, 6, 6, fill=brass(ic))
    ic.path("M224 175c0-10 10-12 10-4v8c0 8-10 6-10-4z", fill=brass(ic))
    ic.path("M225.5 172c1-5 6-6 7-2", fill="none", stroke="#fff", stroke_opacity=0.5)


@small("elisa")
def elisa16(ic):
    tile(ic, "#3E3A86", "#17143E")
    ic.path("M3.4 7.5L4.2 2.5h7.6l.8 5z", fill="#8A5428")
    ic.path("M4.4 7.2L5 3.3h6l.6 3.9z", fill="#3A8AE8")
    ic.path("M2.8 7.5h10.4l.6 2H2.2z", fill="#D8A06A")
    ic.rect(2.2, 9.5, 11.6, 4.5, rx=0.5, fill="#B47A48")
    ic.rect(6.4, 10.8, 3.2, 1.6, rx=0.3, fill="#E8C682")


# --- Strawberry: a strawberry --------------------------------------------------

@icon("strawberry", kind="app", names=["org.strawberrymusicplayer.strawberry", "strawberry"], title="Strawberry")
def strawberry(ic):
    tile(ic, "#3A4C72", "#162240")
    shadow(ic, 128, 214, 64, 10)
    berry = ("M128 212C90 200 52 150 56 108C59 80 88 68 128 76C168 68 197 80 200 108C204 150 166 200 128 212z")
    ic.path(berry, fill="#000", opacity=0.25, transform="translate(3 4)")
    ic.path(berry, fill=ic.rad([(0, "#FF7A6A"), (0.5, "#E52C2C"), (1, "#8E0E18")], cx=0.38, cy=0.3, r=0.8))
    clip = ic.clip(f'<path d="{berry}"/>')
    with ic.g(clip_path=clip):
        # the seeds, each in its dimple
        for row in range(8):
            y = 98 + row * 14.5
            t = (y - 108) / 104
            hw = 70 * (1 - max(0, t) ** 1.6) - 10
            off = 0 if row % 2 else 8.5
            x = 128 - hw + off
            while x <= 128 + hw:
                ic.ellipse(x + 0.8, y + 1.2, 3.2, 4.2, fill="#7A0A14", opacity=0.45)
                ic.ellipse(x, y, 1.9, 3, fill="#FFE07A", transform=f"rotate({(x - 128) * 0.35:.0f} {x:.1f} {y:.1f})")
                ic.ellipse(x - 0.4, y - 1, 0.7, 1, fill="#fff", opacity=0.6)
                x += 17
        ic.path(berry, fill=ic.rad([(0, "#fff", 0), (0.65, "#000", 0), (1, "#3A0006", 0.4)], cx=0.4, cy=0.35,
                                   r=0.7))
    ic.path("M78 104c4-12 18-18 30-16", fill="none", stroke="#fff", stroke_opacity=0.5, stroke_width=4,
            stroke_linecap="round")
    # the calyx and the stem
    leaf = ic.lin([(0, "#7ACB4A"), (1, "#2E7A22")], 0, 0, 1, 1)
    for deg, ln in ((-112, 40), (-70, 36), (-28, 30), (28, 30), (70, 36), (112, 40), (-150, 26), (150, 26)):
        tx, ty = polar(128, 80, ln, deg)
        mx, my = polar(128, 80, ln * 0.55, deg)
        lx, ly = polar(mx, my, ln * 0.22, deg - 90)
        rx_, ry_ = polar(mx, my, ln * 0.22, deg + 90)
        ic.path(f"M128 80Q{lx:.1f} {ly:.1f} {tx:.1f} {ty:.1f}Q{rx_:.1f} {ry_:.1f} 128 80z", fill=leaf,
                stroke="#1E5A16", stroke_width=0.8)
        ic.path(f"M128 80L{mx:.1f} {my:.1f}", stroke="#B8E890", stroke_opacity=0.5, stroke_width=1)
    ic.path("M128 82c0-14 2-28 12-40", fill="none", stroke="#2E6A1C", stroke_width=7, stroke_linecap="round")
    ic.path("M127 80c0-14 2-27 12-39", fill="none", stroke="#8AD05A", stroke_width=2, stroke_linecap="round",
            opacity=0.7)


@small("strawberry")
def strawberry16(ic):
    tile(ic, "#3A4C72", "#162240")
    ic.path("M8 14C5.4 13 3 9.8 3.4 7C3.7 5.2 5.6 4.6 8 5.1C10.4 4.6 12.3 5.2 12.6 7C13 9.8 10.6 13 8 14z",
            fill="#E52C2C")
    for x, y in ((6, 7.4), (10, 7.4), (8, 9), (6.6, 11), (9.4, 11)):
        ic.circle(x, y, 0.45, fill="#FFE07A")
    ic.path("M4.6 5.4L8 4.4L11.4 5.4L9.6 3.6L8 2L6.4 3.6z", fill="#4AA83A")


# --- Shortwave: a portable shortwave radio ----------------------------------

@icon("shortwave", kind="app", names=["de.haeckerfelix.Shortwave", "shortwave"], title="Shortwave")
def shortwave(ic):
    tile(ic, "#2F6C9A", "#12345A")
    shadow(ic, 128, 216, 98, 11)
    # the antenna, pulled out
    for (x1, y1, x2, y2, w) in ((196, 92, 203, 66, 6), (203, 66, 210, 42, 4.6), (210, 42, 217, 20, 3.4)):
        ic.line(x1, y1, x2, y2, stroke="#5D636B", stroke_width=w, stroke_linecap="round")
        ic.line(x1 - w * 0.2, y1, x2 - w * 0.2, y2, stroke="#E6E9ED", stroke_width=w * 0.35, stroke_linecap="round")
    ic.circle(217, 19, 3.6, fill=steel(ic, False))
    # the handle
    ic.path("M64 92V70a10 10 0 0 1 10-10h68a10 10 0 0 1 10 10v22", fill="none", stroke="#2A1A12", stroke_width=9)
    ic.path("M64 90V70a10 10 0 0 1 10-10h68", fill="none", stroke="#6A4430", stroke_width=3, opacity=0.7)
    for x in (64, 152):
        ic.rect(x - 7, 82, 14, 12, rx=3, fill=steel(ic, False))
    # the case
    ic.rect(32, 88, 192, 120, rx=16, fill=ic.lin([(0, "#F7F1E2"), (1, "#C9BC9E")], 0, 0, 1, 1))
    ic.rect(32.75, 88.75, 190.5, 118.5, rx=15.25, fill="none", stroke="#fff", stroke_width=1.5, opacity=0.8)
    ic.rect(32, 196, 192, 12, rx=6, fill="#000", opacity=0.08)
    ic.rect(38, 94, 180, 108, rx=11, fill="none", stroke=steel(ic), stroke_width=2.4)
    # the speaker
    holes = ic.define('<pattern id="{id}" width="6" height="6" patternUnits="userSpaceOnUse">'
                      '<circle cx="3" cy="3" r="1.6" fill="#1E2328"/></pattern>', "p")
    ic.circle(84, 150, 39, fill="#E0D6BE")
    ic.circle(84, 150, 39, fill="none", stroke="#000", stroke_opacity=0.15, stroke_width=2)
    ic.circle(84, 150, 35, fill=f"url(#{holes})")
    ic.circle(84, 150, 39, fill=ic.rad([(0, "#fff", 0), (0.7, "#000", 0), (1, "#000", 0.18)], cx=0.4, cy=0.35))
    ic.text("SHORTWAVE", 84, 106.5, 6, font="mono-semibold", anchor="middle", spacing=1.2, fill="#2F6C9A")
    # the dial
    ic.rect(130, 104, 82, 54, rx=5, fill="#1C2A38")
    ic.rect(133, 107, 76, 48, rx=3, fill=ic.lin([(0, "#FFF4D6"), (1, "#F2D9A0")]))
    ink = "#22303E"
    for row, (band, nums) in enumerate((("SW", ("6", "7", "9", "11", "13")), ("MW", ("53", "70", "100", "160")))):
        y = 118 + row * 16
        ic.text(band, 137, y + 1, 6, font="mono-semibold", fill="#C0392B")
        ic.line(150, y + 4, 205, y + 4, stroke=ink, stroke_width=0.8)
        for k in range(23):
            x = 150 + k * 2.5
            ic.line(x, y + 4, x, y + (1 if k % 5 == 0 else 2.4), stroke=ink, stroke_width=0.6)
        for k, n in enumerate(nums):
            ic.text(n, 154 + k * (48 / (len(nums) - 1)), y - 1, 5.5, font="mono", anchor="middle", fill=ink)
    ic.text("MHz", 205, 150, 5, font="mono", anchor="end", fill=ink)
    ic.line(176, 108, 176, 154, stroke="#D0281C", stroke_width=1.6)
    ic.rect(130, 104, 82, 54, rx=5, fill=glare(ic, 1.2))
    # the knobs and band buttons
    _knob(ic, 150, 182, 12, -40, face=ic.rad([(0, "#E6E9ED"), (1, "#8A9098")], cx=0.35, cy=0.3, r=0.8),
          rim="#3A4048", pointer="#2F6C9A")
    _knob(ic, 192, 182, 12, 70, face=ic.rad([(0, "#E6E9ED"), (1, "#8A9098")], cx=0.35, cy=0.3, r=0.8),
          rim="#3A4048", pointer="#2F6C9A")
    ic.text("TUNE", 150, 202, 4.6, font="mono", anchor="middle", fill="#6A6458")
    ic.text("VOL", 192, 202, 4.6, font="mono", anchor="middle", fill="#6A6458")


@small("shortwave")
def shortwave16(ic):
    tile(ic, "#2F6C9A", "#12345A")
    ic.line(11.5, 6, 13.6, 1.4, stroke="#C3C8CE", stroke_width=0.7, stroke_linecap="round")
    ic.rect(1.8, 5.6, 12.4, 8.4, rx=1.4, fill="#EFE7D2")
    ic.circle(5.4, 9.8, 2.6, fill="#3A3E44")
    ic.rect(8.6, 7, 4.2, 3, rx=0.4, fill="#F2D9A0")
    ic.line(10.8, 7, 10.8, 10, stroke="#D0281C", stroke_width=0.5)
    ic.circle(10.7, 12, 0.9, fill="#8A9098")


# --- Podcasts: a studio microphone on its desk stand -------------------------

@icon("podcasts", kind="app", names=["gnome-podcasts", "org.gnome.Podcasts", "podcasts"], title="Podcasts")
def podcasts(ic):
    tile(ic, "#4E2C82", "#1C0C3A")
    shadow(ic, 128, 214, 66, 10)
    # the stand
    ic.ellipse(128, 206, 50, 11, fill="#141518")
    ic.ellipse(128, 203, 50, 11, fill=ic.lin([(0, "#6A6E76"), (1, "#26282C")], 0, 0, 1, 1))
    ic.ellipse(126, 200, 40, 7, fill="none", stroke="#fff", stroke_opacity=0.18)
    ic.rect(122, 150, 12, 54, fill=steel(ic))
    ic.ellipse(128, 202, 9, 3, fill="#141518")
    # the yoke
    ic.path("M84 98v34a44 44 0 0 0 88 0v-34", fill="none", stroke="#000", stroke_opacity=0.3, stroke_width=8,
            transform="translate(2 3)")
    ic.path("M84 98v34a44 44 0 0 0 88 0v-34", fill="none", stroke=steel(ic), stroke_width=7)
    # the body
    ic.rect(96, 24, 64, 144, rx=32, fill="#000", opacity=0.3, transform="translate(3 4)")
    body = ic.lin([(0, "#B686F0"), (0.45, "#8A52D8"), (1, "#4E2290")], 0, 0, 1, 0)
    ic.rect(96, 24, 64, 144, rx=32, fill=body)
    # the grille
    mesh = ic.define('<pattern id="{id}" width="5" height="5" patternUnits="userSpaceOnUse" '
                     'patternTransform="rotate(45)"><rect width="5" height="5" fill="#9AA1A9"/>'
                     '<path d="M0 0H5M0 0V5" stroke="#3A3E44" stroke-width="1.4"/></pattern>', "p")
    grille = "M96 92V56a32 32 0 0 1 64 0v36z"
    ic.path(grille, fill=f"url(#{mesh})")
    ic.path(grille, fill=ic.lin([(0, "#fff", 0.35), (0.4, "#fff", 0), (1, "#000", 0.4)], 0, 0, 1, 0))
    ic.path("M104 62a24 24 0 0 1 18-28", fill="none", stroke="#fff", stroke_opacity=0.55, stroke_width=3,
            stroke_linecap="round")
    ic.rect(94, 90, 68, 10, rx=2, fill=steel(ic))
    ic.line(95, 91, 161, 91, stroke="#fff", stroke_opacity=0.6)
    # the badge: a dot and its waves, pressed into a disc
    ic.circle(128, 126, 13, fill="#3A1470", opacity=0.6)
    ic.circle(128, 126, 12, fill=ic.lin([(0, "#F4ECFF"), (1, "#C9B2EE")], 0, 0, 1, 1))
    ic.circle(128, 126, 2.6, fill="#6E44A8")
    for r in (5.5, 8.5):
        for a0 in (-50, 130):
            p1, p2 = polar(128, 126, r, a0), polar(128, 126, r, a0 + 100)
            ic.path(f"M{p1[0]:.1f} {p1[1]:.1f}A{r} {r} 0 0 1 {p2[0]:.1f} {p2[1]:.1f}", fill="none",
                    stroke="#6E44A8", stroke_width=1.6, stroke_linecap="round")
    ic.line(104, 110, 104, 152, stroke="#fff", stroke_opacity=0.35, stroke_width=3, stroke_linecap="round")
    # the yoke's knobs
    for x in (84, 172):
        ic.circle(x, 100, 8, fill="#1C1D20")
        ic.circle(x, 100, 6, fill=ic.rad([(0, "#6A6E76"), (1, "#26282C")], cx=0.35, cy=0.3, r=0.8))


@small("podcasts")
def podcasts16(ic):
    tile(ic, "#4E2C82", "#1C0C3A")
    ic.path("M4.6 7v1.5a3.4 3.4 0 0 0 6.8 0V7", fill="none", stroke="#C3C8CE", stroke_width=0.8)
    ic.rect(7.4, 11, 1.2, 2.5, fill="#9AA1A9")
    ic.ellipse(8, 13.8, 3.2, 0.9, fill="#3A3E44")
    ic.rect(5.6, 1.6, 4.8, 9.6, rx=2.4, fill="#8A52D8")
    ic.path("M5.6 6V4a2.4 2.4 0 0 1 4.8 0v2z", fill="#B4BAC2")


# --- Cozy: an audiobook with headphones over it ------------------------------

@icon("cozy", kind="app", names=["com.github.geigi.cozy", "cozy"], title="Cozy")
def cozy(ic):
    tile(ic, "#2E5C58", "#10302C")
    shadow(ic, 128, 214, 90, 11)
    # the book: pages at the side, then the cover
    ic.rect(80, 54, 116, 154, rx=4, fill=paper(ic, "cream"))
    for x in range(184, 196, 2):
        ic.line(x, 58, x, 204, stroke="#B8AC92", stroke_opacity=0.6, stroke_width=0.6)
    cover = leather(ic, "#E8864A", "#963A14")
    ic.rect(68, 48, 118, 160, rx=5, fill=cover)
    ic.rect(68, 48, 16, 160, rx=5, fill="#7A2E0E", opacity=0.6)
    ic.line(84.5, 50, 84.5, 206, stroke="#FFC79A", stroke_opacity=0.35)
    ic.rect(68.75, 48.75, 116.5, 158.5, rx=4.25, fill="none", stroke="#FFD2AA", stroke_opacity=0.35,
            stroke_width=1.5)
    ic.rect(94, 92, 80, 98, rx=3, fill="none", stroke="#5A1E06", stroke_opacity=0.45, stroke_width=1.5,
            transform="translate(0.8 0.8)")
    ic.rect(94, 92, 80, 98, rx=3, fill="none", stroke="#FFD9A8", stroke_opacity=0.7, stroke_width=1.2)
    ic.text("Cozy", 134.8, 147.8, 30, font="hand", anchor="middle", fill="#5A1E06", opacity=0.5)
    ic.text("Cozy", 134, 147, 30, font="hand", anchor="middle", fill="#FFE2B8")
    ic.text("UNABRIDGED", 134, 166, 5.5, font="mono-semibold", anchor="middle", spacing=1.2, fill="#FFD9A8",
            opacity=0.85)
    ic.text("12 h 40 min", 134, 178, 5.5, font="mono", anchor="middle", fill="#FFD9A8", opacity=0.75)
    # the headphones, the band across the cover's top
    band = "M50 132C46 66 92 58 128 58C164 58 210 66 206 132"
    ic.path(band, fill="none", stroke="#000", stroke_opacity=0.3, stroke_width=13, transform="translate(2 4)")
    ic.path(band, fill="none", stroke="#26282C", stroke_width=12)
    ic.path(band, fill="none", stroke="#5A5E66", stroke_width=4, transform="translate(-1 -3)", opacity=0.8)
    ic.path("M92 64C108 59 148 59 164 64", fill="none", stroke="#C9A27A", stroke_width=6, stroke_linecap="round")
    for side, x in ((-1, 50), (1, 206)):
        ic.rect(x - 6, 118, 12, 18, rx=3, fill=steel(ic))
        cup = ic.lin([(0, "#55575E"), (1, "#1A1B1E")], 0, 0, 1, 1)
        ic.rect(x - 16, 130, 32, 52, rx=14, fill="#000", opacity=0.3, transform="translate(2 4)")
        ic.rect(x - 16, 130, 32, 52, rx=14, fill=cup)
        ic.rect(x - 16, 130, 32, 52, rx=14, fill="none", stroke="#fff", stroke_opacity=0.15)
        cx = x - side * 12
        ic.rect(cx - 6, 134, 12, 44, rx=6, fill=ic.lin([(0, "#E8B88A"), (1, "#A06A3A")], 0, 0, 1, 1))
        ic.circle(x + side * 1, 156, 7, fill="#E8864A")
        ic.circle(x + side * 1, 156, 7, fill="none", stroke="#000", stroke_opacity=0.3)
    ic.path("M50 182c2 14 18 22 40 22", fill="none", stroke="#1A1B1E", stroke_width=3, stroke_linecap="round")


@small("cozy")
def cozy16(ic):
    tile(ic, "#2E5C58", "#10302C")
    ic.rect(4.4, 3.2, 7.6, 10.6, rx=0.6, fill="#D8743A")
    ic.rect(4.4, 3.2, 1.2, 10.6, fill="#963A14")
    ic.path("M2.8 9C2.6 4.4 5 4 8 4S13.4 4.4 13.2 9", fill="none", stroke="#B4BAC2", stroke_width=1.2)
    ic.rect(1.4, 8, 2.8, 4.6, rx=1.1, fill="#1E2024")
    ic.rect(11.8, 8, 2.8, 4.6, rx=1.1, fill="#1E2024")
    ic.circle(2.8, 10.3, 0.7, fill="#E8864A")
    ic.circle(13.2, 10.3, 0.7, fill="#E8864A")


# --- EasyEffects: a rack of effects, an equaliser on top --------------------

@icon("easyeffects", kind="app",
      names=["com.github.wwmm.easyeffects", "com.github.wwmm.pulseeffects", "easyeffects", "pulseeffects"],
      title="EasyEffects")
def easyeffects(ic):
    tile(ic, "#24406A", "#0C1A30")
    shadow(ic, 128, 216, 96, 10)
    # the rack's rails
    for x in (30, 212):
        ic.rect(x, 26, 14, 186, rx=2, fill=steel(ic))
        for y in range(32, 210, 9):
            ic.rect(x + 4.5, y, 5, 4, rx=1, fill="#2A2C30")
    # three units
    units = ((34, 70), (108, 42), (154, 54))
    for y, h in units:
        ic.rect(26, y + 2, 204, h, rx=3, fill="#000", opacity=0.35)
        ic.rect(26, y, 204, h - 2, rx=3, fill=ic.lin([(0, "#3C4048"), (1, "#1C1E22")]))
        ic.line(28, y + 0.8, 228, y + 0.8, stroke="#fff", stroke_opacity=0.25)
        for x in (33, 223):
            _screw(ic, x, y + 6, 2.4)
            _screw(ic, x, y + h - 8, 2.4)
    cyan = "#4FD0F0"
    # the equaliser
    ic.text("EasyEffects", 44, 46, 7, font="sans-semibold", fill="#E6E9ED")
    ic.text("EQUALIZER", 212, 46, 5.5, font="mono-semibold", anchor="end", spacing=1, fill=cyan)
    curve = (4, 7, 9, 6, 2, -2, 0, 5, 8, 6)
    for k, (f, g) in enumerate(zip(("31", "63", "125", "250", "500", "1k", "2k", "4k", "8k", "16k"), curve)):
        x = 54 + k * 16.6
        ic.rect(x - 1.2, 54, 2.4, 34, rx=1.2, fill="#0A0B0D")
        y = 71 - g * 1.7
        ic.rect(x - 5, y - 3, 10, 6, rx=1.2, fill="#000", opacity=0.4, transform="translate(0.8 1.2)")
        ic.rect(x - 5, y - 3, 10, 6, rx=1.2, fill=ic.lin([(0, "#E6E9ED"), (1, "#8A9098")]))
        ic.line(x - 3.5, y, x + 3.5, y, stroke=cyan, stroke_width=1.4)
        ic.text(f, x, 99, 4.6, font="mono", anchor="middle", fill="#9AA1A9")
    pts = " ".join(f"{54 + k * 16.6:.1f} {71 - g * 1.7:.1f}" for k, g in enumerate(curve))
    ic.path("M" + pts.replace(" ", " ", 1), fill="none", stroke=cyan, stroke_opacity=0.35, stroke_width=1.2)
    # the limiter: two meters and its knobs
    ic.text("LIMITER", 44, 122, 5.5, font="mono-semibold", spacing=1, fill=cyan)
    _leds(ic, 44, 127, 96, 5, 16, 11, horizontal=True)
    _leds(ic, 44, 135, 96, 5, 16, 9, horizontal=True)
    for k, d in enumerate((-60, 20, 90)):
        _knob(ic, 162 + k * 22, 128, 8, d, ring=cyan)
    # the screen: a waveform
    ic.rect(44, 162, 92, 38, rx=3, fill="#06131A")
    wave = "M48 181" + "".join(
        f"L{48 + i * 2:.0f} {181 - 12 * math.sin(i * 0.42) * math.exp(-((i - 21) / 16) ** 2):.1f}" for i in range(43))
    ic.path(wave, fill="none", stroke=cyan, stroke_width=1.4)
    ic.line(48, 181, 132, 181, stroke=cyan, stroke_opacity=0.25)
    ic.rect(44, 162, 92, 38, rx=3, fill=glare(ic))
    for k, d in enumerate((-110, -20)):
        _knob(ic, 166 + k * 34, 180, 13, d, ring=cyan)
    ic.circle(212, 166, 2, fill="#5BE07A")


@small("easyeffects")
def easyeffects16(ic):
    tile(ic, "#24406A", "#0C1A30")
    ic.rect(1.6, 2, 12.8, 12, rx=0.8, fill="#2A2D33")
    ic.rect(1.6, 9, 12.8, 0.6, fill="#0C0D10")
    for k, g in enumerate((1, 2.5, 1.5, -1, 1, 2.4)):
        x = 3.4 + k * 1.85
        ic.rect(x - 0.25, 3, 0.5, 5, fill="#0C0D10")
        ic.rect(x - 0.7, 5.2 - g * 0.8, 1.4, 1, rx=0.2, fill="#4FD0F0")
    ic.rect(3, 11, 6, 1.2, fill="#5BE07A")
    ic.circle(11.6, 11.6, 1.3, fill="#8A9098")


# --- Volume Control: a big volume knob on a panel ----------------------------

@icon("pavucontrol", kind="app", names=[
    "alsamixergui", "cs-sound", "epulse", "gnome-alsamixer-icon", "gnome-mixer", "gnome-settings-sound",
    "gnome-sound-properties", "gnome-volume-control", "indicator-sound-switcher", "kcmsound", "kmix",
    "litesoundsglob", "multimedia-volume-control", "mx-system-sounds", "org.pulseaudio.pavucontrol", "pasystray",
    "pavucontrol", "phonon-gstreamer", "pnmixer", "preferences-desktop-sound", "preferences-desktop-text-to-speech",
    "preferences-sound", "unity-sound-panel", "wxlame", "xfce-sound", "xfce4-mixer", "xfce4-pulseaudio-plugin",
    "xfce4-sound", "yast-sound"], title="Volume Control")
def pavucontrol(ic):
    tile(ic, "#56606E", "#222831")
    shadow(ic, 128, 214, 96, 11)
    cx, cy = 128, 120
    ic.rect(32, 30, 192, 182, rx=16, fill="#000", opacity=0.3, transform="translate(2 4)")
    ic.rect(32, 30, 192, 182, rx=16, fill=ic.lin([(0, "#F4EFE4"), (1, "#CFC6B2")], 0, 0, 1, 1))
    ic.rect(32.75, 30.75, 190.5, 180.5, rx=15.25, fill="none", stroke="#fff", stroke_width=1.5, opacity=0.8)
    # the rising wedge, green to red
    n = 27
    for k in range(n):
        d0 = -135 + k * 10
        f = k / (n - 1)
        col = "#3FAE5A" if f < 0.6 else "#E8B43A" if f < 0.85 else "#D8442E"
        ro = 70 + 14 * f
        p1, p2, p3, p4 = polar(cx, cy, 66, d0), polar(cx, cy, ro, d0), polar(cx, cy, ro, d0 + 7), \
            polar(cx, cy, 66, d0 + 7)
        ic.poly([p1, p2, p3, p4], fill=col, opacity=1 if k <= 18 else 0.3)
    for v in range(0, 11, 2):
        x, y = polar(cx, cy, 92 - (0 if v < 10 else -2), -135 + v * 26.8)
        ic.text(str(v), x, y + 3.5, 9, font="sans-semibold", anchor="middle", fill="#3A3E44")
    ic.text("VOLUME", cx, 204, 8, font="mono-semibold", anchor="middle", spacing=2, fill="#3A3E44")
    # the knob
    ic.circle(cx + 4, cy + 7, 58, fill="#000", opacity=0.35)
    ic.circle(cx, cy, 58, fill="#141518")
    ic.circle(cx, cy, 56.5, fill="none", stroke="#5A5E66", stroke_width=3, stroke_dasharray="1.6 2.4")
    ic.circle(cx, cy, 48, fill=ic.lin([(0, "#3A3D44"), (1, "#0E0F11")], 0, 0, 1, 1))
    ic.circle(cx, cy, 40, fill=ic.rad([(0, "#F2F4F6"), (0.6, "#B4BAC2"), (1, "#6A7078")], cx=0.38, cy=0.32, r=0.8))
    for r in range(8, 40, 4):
        ic.circle(cx, cy, r, fill="none", stroke="#000", stroke_opacity=0.05)
    ic.circle(cx, cy, 40, fill="none", stroke="#000", stroke_opacity=0.3, stroke_width=1.5)
    deg = -135 + 18 * 10 + 4
    with ic.g(transform=f"rotate({deg} {cx} {cy})"):
        ic.rect(cx - 3, cy - 56, 6, 20, rx=3, fill="#F1F1EF")
        ic.circle(cx, cy - 28, 4, fill="#2A2C30", opacity=0.75)
    ic.path(f"M{cx - 44} {cy - 8}a46 46 0 0 1 36 -38", fill="none", stroke="#fff", stroke_opacity=0.25,
            stroke_width=3, stroke_linecap="round")
    for x, y in ((44, 42), (212, 42), (44, 200), (212, 200)):
        _screw(ic, x, y, 3)


@small("pavucontrol")
def pavucontrol16(ic):
    tile(ic, "#56606E", "#222831")
    for k in range(7):
        d = -135 + k * 45
        x, y = polar(8, 8, 6.2, d)
        ic.circle(x, y, 0.55 + k * 0.08, fill="#3FAE5A" if k < 4 else "#E8B43A" if k < 6 else "#D8442E")
    ic.circle(8, 8, 4.6, fill="#141518")
    ic.circle(8, 8, 3.2, fill="#C3C8CE")
    ic.line(8, 8, 10.6, 5.6, stroke="#141518", stroke_width=1, stroke_linecap="round")


# --- Helvum: a patch bay, cables between its jacks --------------------------

def _plug(ic, x, y, col):
    ic.rect(x - 5, y + 2, 10, 14, rx=2, fill="#000", opacity=0.35, transform="translate(1.5 2)")
    ic.rect(x - 4, y - 2, 8, 6, fill=steel(ic))
    ic.rect(x - 5, y + 2, 10, 16, rx=2.5, fill=col)
    ic.rect(x - 3.6, y + 3, 2.2, 13, rx=1.1, fill="#fff", opacity=0.35)
    for k in range(3):
        ic.line(x - 5, y + 9 + k * 2.6, x + 5, y + 9 + k * 2.6, stroke="#000", stroke_opacity=0.25)


@icon("helvum", kind="app", names=["helvum", "org.pipewire.Helvum"], title="Helvum")
def helvum(ic):
    tile(ic, "#2F5E78", "#10283A")
    shadow(ic, 128, 220, 98, 10)
    ic.add('<g transform="translate(0 12)">')  # the whole bay, a little lower
    # the panel
    ic.rect(22, 50, 212, 104, rx=6, fill="#000", opacity=0.35, transform="translate(2 4)")
    ic.rect(22, 50, 212, 104, rx=6, fill=ic.lin([(0, "#3C4048"), (1, "#16181B")]))
    ic.line(26, 51, 230, 51, stroke="#fff", stroke_opacity=0.28)
    for x in (30, 226):
        for y in (60, 144):
            ic.rect(x - 4, y - 2.5, 8, 5, rx=2.5, fill="#0A0B0D")
    ic.text("HELVUM", 40, 63, 6, font="mono-semibold", spacing=1.4, fill="#E6E9ED")
    ic.text("PIPEWIRE PATCH", 216, 63, 5, font="mono", anchor="end", spacing=0.8, fill="#9AA1A9")
    xs = [48 + k * 26.6 for k in range(7)]
    for row, (y, lab) in enumerate(((94, "OUT"), (132, "IN"))):
        ic.rect(36, y - 18, 184, 30, rx=3, fill="#000", opacity=0.18)
        for k, x in enumerate(xs):
            ic.text(f"{lab} {k + 1}", x, y - 11, 4.6, font="mono", anchor="middle", fill="#B4BAC2")
            ic.circle(x, y, 7, fill=steel(ic, False))
            ic.circle(x, y, 7, fill="none", stroke="#000", stroke_opacity=0.4)
            ic.circle(x, y, 3.6, fill="#050506")
            ic.ellipse(x - 2.6, y - 3.6, 2.5, 1.2, fill="#fff", opacity=0.5, transform=f"rotate(-30 {x - 2.6} {y - 3.6})")
    # the cables, sagging in front
    cables = (("#4A8BE8", xs[0], 94, xs[3], 132, 214),
              ("#B07AF0", xs[2], 94, xs[6], 132, 222),
              ("#3CC8A8", xs[5], 94, xs[1], 132, 230))
    for col, x1, y1, x2, y2, sag in cables:
        d = f"M{x1:.1f} {y1 + 18}C{x1:.1f} {sag} {x2:.1f} {sag} {x2:.1f} {y2 + 18}"
        ic.path(d, fill="none", stroke="#000", stroke_opacity=0.3, stroke_width=6.5, transform="translate(2 3)")
        ic.path(d, fill="none", stroke=col, stroke_width=5.5)
        ic.path(d, fill="none", stroke="#fff", stroke_opacity=0.35, stroke_width=1.4, transform="translate(-1 -1)")
    for col, x1, y1, x2, y2, _ in cables:
        _plug(ic, x1, y1, col)
        _plug(ic, x2, y2, col)
    ic.add("</g>")


@small("helvum")
def helvum16(ic):
    tile(ic, "#2F5E78", "#10283A")
    ic.rect(1.4, 3, 13.2, 7.6, rx=0.8, fill="#2A2D33")
    for x in (3.6, 6.2, 8.8, 11.4):
        ic.circle(x, 5, 0.9, fill="#C3C8CE")
        ic.circle(x, 8.4, 0.9, fill="#C3C8CE")
    ic.path("M3.6 5C3.6 15 11.4 15 11.4 8.4", fill="none", stroke="#4A8BE8", stroke_width=1)
    ic.path("M8.8 5C8.8 14 6.2 14 6.2 8.4", fill="none", stroke="#B07AF0", stroke_width=1)


# --- Ardour: a mixing desk, its meters lit ---------------------------------

@icon("ardour", kind="app", names=["Ardour-Ardour_6.0.0", "Ardour-Ardour_6.5.0", "Ardour-Ardour_8.0.0", "ardour",
                                   "ardour6", "ardour7", "ardour8", "org.ardour.Ardour"], title="Ardour")
def ardour(ic):
    tile(ic, "#8E3028", "#3C0E0A")
    shadow(ic, 128, 216, 104, 11)
    red = "#E8402E"
    # the meter bridge
    ic.rect(44, 30, 168, 44, rx=5, fill=ic.lin([(0, "#3A3D44"), (1, "#18191C")]))
    ic.line(47, 30.8, 209, 30.8, stroke="#fff", stroke_opacity=0.25)
    ic.rect(50, 36, 156, 32, rx=2, fill="#0A0B0D")
    levels = (9, 12, 7, 11, 5, 13)
    for k, lv in enumerate(levels):
        x = 56 + k * 22
        _leds(ic, x, 39, 5, 26, 14, lv, gap=0.8)
        _leds(ic, x + 7, 39, 5, 26, 14, max(0, lv - 2), gap=0.8)
    ic.rect(190, 39, 13, 26, rx=1.5, fill=red)
    ic.text("A", 196.5, 57, 12, font="sans-bold", anchor="middle", fill="#fff")
    # the desk, sloping toward us
    ic.path("M40 76H216L232 202H24z", fill=ic.lin([(0, "#4A4E56"), (1, "#22242A")]))
    ic.path("M40 76H216", stroke="#fff", stroke_opacity=0.3, stroke_width=1.5)
    ic.path("M24 202H232v8a4 4 0 0 1-4 4H28a4 4 0 0 1-4-4z", fill="#141518")
    ic.line(24, 202.5, 232, 202.5, stroke="#fff", stroke_opacity=0.2)
    ic.path("M40 76L24 202", stroke="#fff", stroke_opacity=0.18, stroke_width=1.5)
    # six strips: two knobs, a mute, a fader
    for k in range(6):
        t = k / 5
        x = 54 + k * 29.6
        ic.line(x + 14.8, 80, x + 14.8 + (t - 0.5) * 12, 198, stroke="#000", stroke_opacity=0.25)
        master = k == 5
        _knob(ic, x, 90, 6.5, -40 + k * 22, ring=red if master else "#E6E9ED")
        _knob(ic, x + (t - 0.5) * 2, 108, 6.5, 50 - k * 18, ring="#F2C14A")
        ic.rect(x - 6 + (t - 0.5) * 3, 120, 12, 7, rx=1.5, fill=red if k in (2, 5) else "#5A5E66")
        sx = x + (t - 0.5) * 6
        ic.rect(sx - 1.6, 134, 3.2, 56, rx=1.6, fill="#08090A")
        for j in range(7):
            ic.line(sx - 6, 137 + j * 8.5, sx - 3.5, 137 + j * 8.5, stroke="#9AA1A9", stroke_width=0.6)
        fy = (170, 150, 160, 144, 176, 152)[k]
        ic.rect(sx - 7, fy - 5 + 2, 14, 12, rx=2, fill="#000", opacity=0.45)
        cap = ic.lin([(0, "#FF8A6E"), (1, "#B42A1A")]) if master else ic.lin([(0, "#F1F1EF"), (1, "#9AA1A9")])
        ic.rect(sx - 7, fy - 5, 14, 11, rx=2, fill=cap)
        ic.line(sx - 6, fy, sx + 6, fy, stroke="#1A1B1E", stroke_width=1.2)
    ic.text("ARDOUR", 128, 211, 5.5, font="mono-semibold", anchor="middle", spacing=2, fill="#9AA1A9")


@small("ardour")
def ardour16(ic):
    tile(ic, "#8E3028", "#3C0E0A")
    ic.rect(3, 1.6, 10, 3, rx=0.4, fill="#141518")
    for k, h in enumerate((2, 1.4, 2.4, 1.8)):
        ic.rect(4 + k * 2.2, 4.2 - h, 1, h, fill="#5BE07A")
    ic.path("M2.6 5H13.4L14.4 13.8H1.6z", fill="#3A3D44")
    for k, y in enumerate((10, 8, 11, 9)):
        x = 4 + k * 2.6
        ic.rect(x - 0.2, 6.5, 0.4, 6.4, fill="#0A0B0D")
        ic.rect(x - 0.9, y, 1.8, 1.2, rx=0.2, fill="#E8402E" if k == 3 else "#E6E9ED")


# --- LMMS: a synthesiser, its knobs and keys ---------------------------------

@icon("lmms", kind="app", names=["io.lmms.LMMS", "lmms"], title="LMMS")
def lmms(ic):
    tile(ic, "#2E8A5C", "#0E3C24")
    shadow(ic, 128, 206, 108, 11)
    green = "#4FE08A"
    ic.rect(20, 66, 216, 134, rx=10, fill="#000", opacity=0.3, transform="translate(2 4)")
    # the wooden cheeks and the case
    ic.rect(20, 66, 216, 134, rx=10, fill=wood(ic, "#B47A48", "#5E3518"))
    ic.rect(34, 66, 188, 134, fill=ic.lin([(0, "#3A3D44"), (1, "#16171A")]))
    ic.line(34, 67, 222, 67, stroke="#fff", stroke_opacity=0.3)
    ic.rect(20.75, 66.75, 214.5, 132.5, rx=9.25, fill="none", stroke="#fff", stroke_opacity=0.14, stroke_width=1.5)
    # the screen
    ic.rect(42, 76, 58, 38, rx=3, fill="#06140C")
    ic.text("LMMS", 48, 90, 9, font="mono-semibold", fill=green)
    saw = "M48 106" + "".join(f"l7 -10l0 10" for _ in range(6))
    ic.path(saw, fill="none", stroke=green, stroke_width=1.2, stroke_linejoin="round")
    ic.rect(42, 76, 58, 38, rx=3, fill=glare(ic))
    # the knobs, in two rows
    labels = (("CUT", "RES", "ENV", "LFO"), ("ATK", "DEC", "SUS", "REL"))
    for r, row in enumerate(labels):
        for k, lab in enumerate(row):
            x, y = 116 + k * 26, 84 + r * 26
            _knob(ic, x, y, 8, (-110, -30, 40, 100, -80, 10, 70, -50)[r * 4 + k], ring=green)
            ic.text(lab, x, y + 15, 4.6, font="mono", anchor="middle", fill="#9AA1A9")
    ic.circle(46, 124, 2, fill=green)
    ic.text("SYNTH", 52, 126, 5, font="mono", fill="#9AA1A9")
    # the keys
    kx, ky, kw, kh = 36, 136, 184, 58
    ic.rect(kx - 2, ky - 2, kw + 4, kh + 4, rx=2, fill="#0A0B0D")
    n = 14
    w = kw / n
    for i in range(n):
        ic.rect(kx + i * w + 0.5, ky, w - 1, kh, rx=1.6, fill=ic.lin([(0, "#FFFFFF"), (0.85, "#E8E3D8"),
                                                                        (1, "#BEB6A6")]))
    for i in range(n - 1):
        if i % 7 in (2, 6):
            continue
        bx = kx + (i + 1) * w - w * 0.3
        ic.rect(bx, ky, w * 0.6, kh * 0.6, rx=1.2, fill=ic.lin([(0, "#3A3D44"), (1, "#0A0B0D")]))
        ic.rect(bx + 1, ky + kh * 0.6 - 4, w * 0.6 - 2, 3, rx=1, fill="#fff", opacity=0.18)
    ic.rect(kx, ky, kw, 3, fill="#000", opacity=0.4)


@small("lmms")
def lmms16(ic):
    tile(ic, "#2E8A5C", "#0E3C24")
    ic.rect(1.2, 4, 13.6, 8.6, rx=0.8, fill="#8A5530")
    ic.rect(2.2, 4, 11.6, 8.6, fill="#2A2D33")
    ic.rect(3, 4.8, 3.6, 2, rx=0.3, fill="#4FE08A")
    for x in (8.4, 10.4, 12.4):
        ic.circle(x, 5.8, 0.7, fill="#C3C8CE")
    ic.rect(2.4, 8, 11.2, 4, fill="#F4F1EA")
    for x in (3.9, 5.6, 8.8, 10.5, 12.2):
        ic.rect(x - 0.4, 8, 0.8, 2.2, fill="#141518")


# --- MuseScore: a score, open on its music stand ----------------------------

def _clef(ic, x, y, s, col):
    """A treble clef, drawn: its curl round the second line from the bottom
    (y), s the staff's line spacing."""
    d = (f"M{x + 0.6 * s:.1f} {y + 2.6 * s:.1f}"
         f"C{x - 0.2 * s:.1f} {y + 3 * s:.1f} {x - 0.6 * s:.1f} {y + 2.2 * s:.1f} {x:.1f} {y + 1.8 * s:.1f}"
         f"C{x + 0.4 * s:.1f} {y + 1.6 * s:.1f} {x + 0.6 * s:.1f} {y + 2.2 * s:.1f} {x + 0.6 * s:.1f} {y + 2.6 * s:.1f}"
         f"L{x + 0.2 * s:.1f} {y - 3.4 * s:.1f}"
         f"C{x + 0.1 * s:.1f} {y - 4.4 * s:.1f} {x + 1.2 * s:.1f} {y - 4.4 * s:.1f} {x + 1 * s:.1f} {y - 3.4 * s:.1f}"
         f"C{x + 0.8 * s:.1f} {y - 2.2 * s:.1f} {x - 1.4 * s:.1f} {y - 1.2 * s:.1f} {x - 1.4 * s:.1f} {y + 0.4 * s:.1f}"
         f"C{x - 1.4 * s:.1f} {y + 1.6 * s:.1f} {x + 1.4 * s:.1f} {y + 1.6 * s:.1f} {x + 1.3 * s:.1f} {y + 0.2 * s:.1f}"
         f"C{x + 1.2 * s:.1f} {y - 0.8 * s:.1f} {x - 0.2 * s:.1f} {y - 0.9 * s:.1f} {x - 0.2 * s:.1f} {y + 0.2 * s:.1f}")
    ic.path(d, fill="none", stroke=col, stroke_width=s * 0.32, stroke_linecap="round", stroke_linejoin="round")


@icon("musescore", kind="app", names=["Musescore", "appimagekit-mscore-portable", "mscore", "mscore-portable",
                                      "musescore", "org.musescore.MuseScore"], title="MuseScore")
def musescore(ic):
    tile(ic, "#2F6EC4", "#123874")
    shadow(ic, 128, 214, 92, 11)
    # the stand: its desk, behind and below the pages
    ic.rect(122, 186, 12, 30, fill=steel(ic))
    ic.path("M30 50h196v136a6 6 0 0 1-6 6H36a6 6 0 0 1-6-6z", fill=ic.lin([(0, "#2A3240"), (1, "#10141C")]))
    for y in range(64, 186, 16):
        ic.rect(36, y, 184, 8, fill="#000", opacity=0.25)
    # the score, two pages open
    ink = "#1E2228"
    for side, rot in ((-1, -2), (1, 2)):
        x0 = 128 + (side - 1) * 46 + (0 if side < 0 else -46) * 0
        x0 = 38 if side < 0 else 128
        with ic.g(transform=f"rotate({rot} 128 190)"):
            ic.rect(x0, 30, 90, 160, rx=2, fill=paper(ic, "cream" if side < 0 else "white"))
            if side < 0:
                ic.text("Prelude in C", x0 + 45, 46, 8.5, font="sans-semibold", anchor="middle", fill=ink)
                ic.text("J. S. Bach", x0 + 84, 56, 5, font="sans", anchor="end", fill="#55534E")
            for st in range(5 if side < 0 else 6):
                sy = (64 if side < 0 else 44) + st * 24
                for ln in range(5):
                    ic.line(x0 + 6, sy + ln * 3.2, x0 + 84, sy + ln * 3.2, stroke=ink, stroke_width=0.6, opacity=0.8)
                ic.line(x0 + 84, sy, x0 + 84, sy + 12.8, stroke=ink, stroke_width=0.8)
                if side < 0:
                    _clef(ic, x0 + 12, sy + 9.6, 3.2, ink)
                start = x0 + (24 if side < 0 else 12)
                for j in range(6):
                    nx = start + j * 10
                    step = (st * 3 + j * 5) % 7
                    ny = sy + 12.8 - step * 1.6
                    ic.ellipse(nx, ny, 2.2, 1.6, fill=ink, transform=f"rotate(-20 {nx} {ny})")
                    ic.line(nx + 2, ny, nx + 2, ny - 9, stroke=ink, stroke_width=0.6)
                ic.line(start + 2, sy - 5 + 12.8 - ((st * 3) % 7) * 1.6, start + 52, sy - 5, stroke=ink,
                        stroke_width=1.6, opacity=0.0)
                ic.line(x0 + 54, sy, x0 + 54, sy + 12.8, stroke=ink, stroke_width=0.6)
    ic.line(128, 30, 128, 190, stroke="#000", stroke_opacity=0.12, stroke_width=2)
    # the stamp in the corner: a blue disc, three lines across a note
    sx, sy = 194, 176
    ic.circle(sx, sy, 15, fill="#123874", opacity=0.3, transform="translate(1 2)")
    ic.circle(sx, sy, 15, fill=ic.lin([(0, "#4A8EF0"), (1, "#1A56B8")], 0, 0, 1, 1))
    for k in range(3):
        ic.line(sx - 9, sy - 5 + k * 5, sx + 9, sy - 5 + k * 5 - 3, stroke="#fff", stroke_width=1.6,
                stroke_linecap="round")
    ic.circle(sx - 0.5, sy - 0.5, 14.3, fill="none", stroke="#fff", stroke_opacity=0.35)
    # the stand's ledge, holding the pages
    ic.rect(26, 186, 204, 12, rx=3, fill=ic.lin([(0, "#3A4456"), (1, "#141A24")]))
    ic.line(28, 186.8, 228, 186.8, stroke="#fff", stroke_opacity=0.3)


@small("musescore")
def musescore16(ic):
    tile(ic, "#2F6EC4", "#123874")
    ic.rect(2, 2, 12, 11, rx=0.4, fill="#FCF9F2")
    ic.line(8, 2, 8, 13, stroke="#B8B0A0", stroke_width=0.5)
    for y in (4, 5.5, 7, 8.5, 10):
        ic.line(3, y, 13, y, stroke="#5A5E66", stroke_width=0.45)
    for x, y in ((4.4, 8.5), (6.6, 7), (9.6, 5.5), (11.8, 7.8)):
        ic.ellipse(x, y, 1, 0.8, fill="#1E2228")
        ic.rect(x + 0.6, y - 3.4, 0.5, 3.4, fill="#1E2228")
    ic.rect(1.4, 12.6, 13.2, 1.6, rx=0.4, fill="#1A2230")


# --- REAPER: a reel-to-reel tape machine ------------------------------------

def _reel(ic, cx, cy, r, pack):
    ic.circle(cx + 2, cy + 3, r, fill="#000", opacity=0.35)
    ic.circle(cx, cy, pack, fill=ic.rad([(0, "#2A1A10"), (0.8, "#5A3A24"), (1, "#3A2414")]))
    for k in range(int(pack - 10), int(pack), 3):
        ic.circle(cx, cy, k, fill="none", stroke="#8A6040", stroke_opacity=0.25, stroke_width=0.6)
    # the flange, aluminium with three windows
    win = []
    for k in range(3):
        a = k * 120 + 20
        p1, p2 = polar(cx, cy, r * 0.32, a - 34), polar(cx, cy, r * 0.32, a + 34)
        q1, q2 = polar(cx, cy, r * 0.84, a + 46), polar(cx, cy, r * 0.84, a - 46)
        win.append(f"M{p1[0]:.1f} {p1[1]:.1f}A{r * 0.32:.1f} {r * 0.32:.1f} 0 0 1 {p2[0]:.1f} {p2[1]:.1f}"
                   f"L{q1[0]:.1f} {q1[1]:.1f}A{r * 0.84:.1f} {r * 0.84:.1f} 0 0 0 {q2[0]:.1f} {q2[1]:.1f}z")
    disc = (f"M{cx - r:.1f} {cy}a{r} {r} 0 1 0 {2 * r} 0a{r} {r} 0 1 0 {-2 * r} 0z" + "".join(win))
    ic.path(disc, fill=ic.lin([(0, "#F2F4F6"), (0.5, "#B4BAC2"), (1, "#6A7078")], 0, 0, 1, 1), fill_rule="evenodd")
    ic.path(disc, fill="none", stroke="#000", stroke_opacity=0.3, fill_rule="evenodd")
    ic.circle(cx - 0.6, cy - 0.6, r - 1, fill="none", stroke="#fff", stroke_opacity=0.5)
    ic.circle(cx, cy, r * 0.22, fill=steel(ic, False))
    ic.circle(cx, cy, r * 0.09, fill="#1A1B1E")


@icon("reaper", kind="app", names=["cockos-reaper", "fm.reaper.Reaper", "reaper"], title="REAPER")
def reaper(ic):
    tile(ic, "#4A5E56", "#18241F")
    shadow(ic, 128, 216, 98, 11)
    ic.rect(30, 26, 196, 186, rx=12, fill="#000", opacity=0.3, transform="translate(2 4)")
    ic.rect(30, 26, 196, 186, rx=12, fill=ic.lin([(0, "#3C4048"), (1, "#141518")], 0, 0, 1, 1))
    ic.rect(36, 32, 184, 174, rx=8, fill=ic.lin([(0, "#D4D8DD"), (0.5, "#A8AEB6"), (1, "#7A8088")], 0, 0, 1, 1))
    brushed = ic.define('<pattern id="{id}" width="4" height="3" patternUnits="userSpaceOnUse">'
                        '<rect width="4" height="1" fill="#fff" opacity=".18"/></pattern>', "p")
    ic.rect(36, 32, 184, 174, rx=8, fill=f"url(#{brushed})")
    ic.rect(36.5, 32.5, 183, 173, rx=7.5, fill="none", stroke="#fff", stroke_opacity=0.5)
    # the tape path: from the reels round the guides past the heads
    tape = "#3A2414"
    ic.path("M48 82L74 150H182L208 82", fill="none", stroke=tape, stroke_width=2.2)
    _reel(ic, 82, 80, 40, 34)
    _reel(ic, 174, 80, 40, 22)
    for x in (74, 182):
        ic.circle(x, 150, 6, fill=steel(ic, False))
        ic.circle(x, 150, 2, fill="#1A1B1E")
    # the head block and capstan
    ic.rect(98, 136, 60, 26, rx=4, fill=ic.lin([(0, "#3A3D44"), (1, "#141518")]))
    ic.line(100, 137, 156, 137, stroke="#fff", stroke_opacity=0.3)
    for x, c in ((108, "#9AA1A9"), (122, "#9AA1A9"), (136, "#C99645")):
        ic.rect(x, 140, 8, 9, rx=2, fill=c)
    ic.circle(150, 155, 4, fill="#E6E9ED")
    ic.text("REAPER", 128, 159, 5.5, font="mono-semibold", anchor="middle", spacing=1.2, fill="#E6E9ED",
            transform="translate(-8 0)")
    # the counter and the transport keys
    ic.rect(46, 172, 40, 16, rx=2, fill="#0A0B0D")
    ic.text("0:42", 66, 184, 10, font="mono-semibold", anchor="middle", fill="#5BE07A")
    keys = (("#E6E9ED", "rew"), ("#E6E9ED", "stop"), ("#4CC870", "play"), ("#E8402E", "rec"))
    for k, (c, kind) in enumerate(keys):
        x = 98 + k * 28
        ic.rect(x, 174 + 2, 22, 16, rx=3, fill="#000", opacity=0.4)
        ic.rect(x, 172, 22, 16, rx=3, fill=ic.lin([(0, "#4A4E56"), (1, "#202226")]))
        mx, my = x + 11, 180
        if kind == "rew":
            ic.path(f"M{mx} {my - 4}l-6 4l6 4zM{mx + 6} {my - 4}l-6 4l6 4z", fill=c)
        elif kind == "stop":
            ic.rect(mx - 4, my - 4, 8, 8, rx=1, fill=c)
        elif kind == "play":
            ic.path(f"M{mx - 3} {my - 5}l8 5l-8 5z", fill=c)
        else:
            ic.circle(mx, my, 4.5, fill=c)
    for x, y in ((42, 38), (214, 38), (42, 200), (214, 200)):
        _screw(ic, x, y, 2.6)


@small("reaper")
def reaper16(ic):
    tile(ic, "#4A5E56", "#18241F")
    ic.rect(1.6, 1.6, 12.8, 12.8, rx=1, fill="#B4BAC2")
    for x, p in ((5, 2.6), (11, 1.6)):
        ic.circle(x, 5.6, 3, fill="#E6E9ED")
        ic.circle(x, 5.6, p, fill="#5A3A24")
        ic.circle(x, 5.6, 0.7, fill="#3A3E44")
    ic.rect(5.6, 9.6, 4.8, 1.8, rx=0.3, fill="#2A2C30")
    ic.rect(3, 12, 2.2, 1.4, rx=0.3, fill="#4CC870")
    ic.rect(10.8, 12, 2.2, 1.4, rx=0.3, fill="#E8402E")


# --- TIDAL: a black hi-fi amplifier, its meters lit ------------------------

def _tidal_mark(ic, x, y, s, fill):
    """Four diamonds: three in a row, one beneath the middle."""
    for dx, dy in ((-1, 0), (0, 0), (1, 0), (0, 1)):
        cx, cy = x + dx * s, y + dy * s
        h = s * 0.48
        ic.path(f"M{cx:.1f} {cy - h:.1f}L{cx + h:.1f} {cy:.1f}L{cx:.1f} {cy + h:.1f}L{cx - h:.1f} {cy:.1f}z",
                fill=fill)


@icon("tidal", kind="app", names=["com.mastermindzh.tidal-hifi", "tidal", "tidal-hifi"], title="TIDAL")
def tidal(ic):
    tile(ic, "#4A4F58", "#15171B")
    shadow(ic, 128, 206, 110, 11)
    # the lid, seen from a little above, and the front
    ic.path("M36 58H220L232 74H24z", fill=ic.lin([(0, "#45484F"), (1, "#26282D")]))
    for x in range(60, 200, 10):
        ic.line(x, 61, x - 2, 70, stroke="#000", stroke_opacity=0.5, stroke_width=2)
    ic.line(36, 58.6, 220, 58.6, stroke="#fff", stroke_opacity=0.3)
    ic.rect(24, 74, 208, 122, rx=4, fill=ic.lin([(0, "#2A2B2F"), (1, "#0C0C0E")]))
    ic.line(25, 74.8, 231, 74.8, stroke="#fff", stroke_opacity=0.3)
    for x in (44, 212):
        ic.rect(x - 12, 196, 24, 8, rx=2, fill="#0A0A0B")
    # the meters, warm behind their glass
    for k, deg in enumerate((-14, 6)):
        x0 = 36 + k * 58
        ic.rect(x0 - 2, 86, 56, 46, rx=4, fill="#060607")
        ic.rect(x0, 88, 52, 42, rx=3, fill=ic.rad([(0, "#FFF0C8"), (1, "#E8B860")], cx=0.5, cy=0.9, r=0.9))
        mx, my = x0 + 26, 132
        ic.path(f"M{x0 + 8} 108A30 30 0 0 1 {x0 + 44} 108", fill="none", stroke="#2A2010", stroke_width=0.8)
        ic.path(f"M{x0 + 34} 102A30 30 0 0 1 {x0 + 44} 108", fill="none", stroke="#C8301C", stroke_width=2.4)
        for t in range(-40, 41, 10):
            a, b = polar(mx, my, 31, t), polar(mx, my, 35 if t % 20 == 0 else 33.5, t)
            ic.line(a[0], a[1], b[0], b[1], stroke="#2A2010", stroke_width=0.7)
        ic.text("VU", mx, 122, 6, font="mono-semibold", anchor="middle", fill="#2A2010")
        p = polar(mx, my, 38, deg)
        ic.line(mx, my, p[0], p[1], stroke="#1A1A1C", stroke_width=1.1)
        ic.rect(x0, 88, 52, 42, rx=3, fill=glare(ic, 1.3))
    # the volume knob, aluminium
    cx, cy = 190, 116
    ic.circle(cx + 3, cy + 5, 31, fill="#000", opacity=0.5)
    ic.circle(cx, cy, 31, fill=ic.lin([(0, "#E6E9ED"), (1, "#5A5E66")], 0, 0, 1, 1))
    ic.circle(cx, cy, 26, fill=ic.rad([(0, "#FFFFFF"), (0.5, "#C3C8CE"), (1, "#7A8088")], cx=0.38, cy=0.32, r=0.8))
    for r in range(4, 26, 3):
        ic.circle(cx, cy, r, fill="none", stroke="#000", stroke_opacity=0.06)
    p = polar(cx, cy, 20, -30)
    ic.circle(p[0], p[1], 2.2, fill="#1A1A1C")
    ic.text("VOLUME", cx, 160, 5, font="mono", anchor="middle", spacing=1, fill="#8A8F97")
    # the maker's mark and the small controls
    _tidal_mark(ic, 50, 152, 9, "#F1F1EF")
    ic.text("TIDAL", 70, 157, 11, font="sans-bold", spacing=2.4, fill="#F1F1EF")
    ic.text("HI-FI INTEGRATED", 70, 167, 4.8, font="mono", spacing=0.8, fill="#8A8F97")
    for k in range(3):
        _knob(ic, 52 + k * 22, 182, 6, -30 + k * 30, face=ic.rad([(0, "#E6E9ED"), (1, "#6A7078")], cx=0.35, cy=0.3,
                                                                    r=0.8), rim="#3A3D44", pointer="#1A1A1C")
    ic.circle(142, 182, 2.4, fill="#DCE8FF")
    ic.circle(142, 182, 4.5, fill="#DCE8FF", opacity=0.2)


@small("tidal")
def tidal16(ic):
    tile(ic, "#4A4F58", "#15171B")
    ic.rect(1.4, 4.4, 13.2, 7.8, rx=0.6, fill="#141518")
    ic.rect(2.4, 5.4, 3.4, 2.8, rx=0.3, fill="#F2D08A")
    ic.rect(6.2, 5.4, 3.4, 2.8, rx=0.3, fill="#F2D08A")
    ic.circle(12, 8.2, 2.2, fill="#C3C8CE")
    _tidal_mark(ic, 4, 10, 1.2, "#F1F1EF")
