"""The soft drawings of the music and audio apps (t2-music): the same
objects as drawings/apps_t2_music.py, about half the detail, no text."""

import math

from lib import bar, polar, soft, soft_shadow, tile, two

STEEL = ("#AEB4BB", "#8D949C")
BRASS = ("#E2B45E", "#B88433")


def _knob(ic, cx, cy, r, deg=0, face="#3A3D44", rim="#16171A", pointer="#F1F1EF"):
    """A knob from above: a dark skirt, a face, a pointer at deg (0 up)."""
    ic.circle(cx, cy, r, fill=rim)
    ic.circle(cx, cy, r * 0.78, fill=face)
    a, b = polar(cx, cy, r * 0.2, deg), polar(cx, cy, r * 0.66, deg)
    ic.line(a[0], a[1], b[0], b[1], stroke=pointer, stroke_width=max(1.6, r * 0.18), stroke_linecap="round")


def _note(ic, x, y, s, **kw):
    """An eighth note, its head's centre at (x, y), s its head's width."""
    h = s * 0.5
    ic.ellipse(x, y, h, h * 0.75, transform=f"rotate(-22 {x} {y})", **kw)
    sx = x + h * 0.82
    ic.rect(sx - s * 0.12, y - s * 2.1, s * 0.24, s * 2.1, **kw)
    ic.path(f"M{sx - s * 0.12:.1f} {y - s * 2.1:.1f}c{s * 0.2:.1f} {s * 0.5:.1f} {s * 0.9:.1f} {s * 0.6:.1f} "
            f"{s * 0.7:.1f} {s * 1.3:.1f}c{s * 0.05:.1f} {-s * 0.55:.1f} {-s * 0.4:.1f} {-s * 0.7:.1f} "
            f"{-s * 0.7:.1f} {-s * 0.75:.1f}z", **kw)


# --- Rhythmbox: a bookshelf speaker ------------------------------------------

@soft("rhythmbox")
def rhythmbox(ic):
    tile(ic, "#D67A2E", "#7A3410")
    soft_shadow(ic, 128, 216, 78, 11)
    ic.rect(60, 24, 136, 192, rx=16, fill=two(ic, "#6E4428", "#3A2212"))
    ic.rect(70, 34, 116, 172, rx=10, fill=two(ic, "#2E2F33", "#18191C"))
    for cx, cy, r, cone in ((128, 72, 18, "#E8A855"), (128, 142, 46, "#F08A24")):
        ic.circle(cx, cy, r + 3, fill="#0E0E10")
        ic.circle(cx, cy, r * 0.9, fill="#3A3B40")
        ic.circle(cx, cy, r * 0.76, fill=two(ic, cone, "#B8540E"))
        ic.circle(cx, cy, r * 0.3, fill=two(ic, "#FFD890", "#E89030"))
    bar(ic, 104, 196, 48, 6, fill="#F0A050")


# --- Lollypop: a swirled lollipop, a tag on its ribbon ----------------------

def _spiral(cx, cy, r0, r1, turns, phase):
    pts = []
    n = int(turns * 40)
    for k in range(n + 1):
        t = k / n
        x, y = polar(cx, cy, r0 + (r1 - r0) * t, phase + t * turns * 360)
        pts.append(f"{x:.1f} {y:.1f}")
    return "M" + "L".join(pts)


@soft("lollypop")
def lollypop(ic):
    tile(ic, "#3FA0B6", "#17566A")
    soft_shadow(ic, 136, 216, 62, 9)
    cx, cy, r = 118, 96, 68
    ic.line(132, 150, 166, 214, stroke="#F4EEE2", stroke_width=11, stroke_linecap="round")
    ic.circle(cx, cy, r, fill=two(ic, "#F2649E", "#C42A6A"))
    clip = ic.clip(f'<circle cx="{cx}" cy="{cy}" r="{r}"/>')
    with ic.g(clip_path=clip):
        ic.path(_spiral(cx, cy, 2, r + 14, 2.4, 0), fill="none", stroke="#FFF6FA", stroke_width=14,
                stroke_linecap="round")
        ic.path(_spiral(cx, cy, 2, r + 14, 2.4, 180), fill="none", stroke="#FFC23D", stroke_width=10,
                stroke_linecap="round")
    bx, by = 140, 166
    ic.path(f"M{bx} {by}l-12 24l7 -3l4 6z", fill="#6A30B0")
    ic.path(f"M{bx} {by}l14 21l-7 0l-1 7z", fill="#7A3FC8")
    ic.path(f"M{bx} {by}c-10 -14 -28 -14 -26 -1c1 9 16 8 26 1z", fill="#8A4ADA")
    ic.path(f"M{bx} {by}c10 -14 28 -14 26 -1c-1 9 -16 8 -26 1z", fill="#9A5AE8")
    ic.circle(bx, by, 6, fill="#6A30B0")
    with ic.g(transform=f"rotate(14 {bx + 20} {by + 10})"):
        ic.path(f"M{bx + 22} {by + 4}h40a4 4 0 0 1 4 4v14a4 4 0 0 1-4 4h-40l-7 -11z",
                fill=two(ic, "#FCF9F2", "#E8E0CF"))
        bar(ic, bx + 26, by + 12, 32, 6, fill="#8A2A5A")


# --- Amberol: a little jukebox ------------------------------------------------

@soft("amberol")
def amberol(ic):
    tile(ic, "#6A2E40", "#2C0E1A")
    soft_shadow(ic, 128, 216, 82, 11)
    cy = 100
    ic.path(f"M56 212V{cy}A72 72 0 0 1 200 {cy}V212z", fill=two(ic, "#7A4426", "#3A1C0C"))
    arch = f"M66 210V{cy}A62 62 0 0 1 190 {cy}V210"
    ic.path(arch, fill="none", stroke="#9DA3AA", stroke_width=17)
    ic.path(arch, fill="none", stroke=two(ic, "#FFD27A", "#F08A24"), stroke_width=11)
    ic.path(f"M76 {cy + 8}V{cy}A52 52 0 0 1 180 {cy}V{cy + 8}z", fill="#2A1208")
    ic.ellipse(128, 101, 42, 11, fill="#141416")
    ic.ellipse(128, 101, 13, 3.6, fill="#FFB43A")
    ic.rect(76, 110, 104, 38, rx=5, fill="#1A0C06")
    for k in range(3):
        ic.rect(80, 114 + k * 11, 96, 8, rx=3, fill="#F4EEDF")
        bar(ic, 84, 116 + k * 11, 8, 4, fill="#C0561A")
    ic.rect(76, 156, 104, 44, rx=6, fill=two(ic, "#FFC060", "#D0681A"))
    for x in range(86, 176, 14):
        ic.rect(x, 156, 5, 44, fill="#C9CED4")
    ic.rect(102, 150, 52, 10, rx=3, fill=two(ic, *BRASS))


# --- Elisa: a music box, lid open --------------------------------------------

@soft("elisa")
def elisa(ic):
    tile(ic, "#3E3A86", "#17143E")
    soft_shadow(ic, 128, 214, 96, 12)
    ic.path("M54 114L63 36a8 8 0 0 1 8-7h114a8 8 0 0 1 8 7l9 78z", fill=two(ic, "#A86A3C", "#6A3A18"))
    ic.path("M64 110L72 42h112l8 68z", fill=two(ic, "#3E8ED8", "#1F4E9A"))
    ic.circle(128, 74, 23, fill=two(ic, *BRASS))
    ic.circle(128, 74, 18, fill=two(ic, "#5FC0F0", "#5A50D8"))
    _note(ic, 124, 82, 9, fill="#fff")
    ic.path("M46 114h164l8 34H38z", fill=two(ic, "#D8A06A", "#A86E3A"))
    ic.path("M58 118h140l5 26H53z", fill="#2A1A0E")
    ic.rect(72, 121, 84, 11, rx=5.5, fill=two(ic, *STEEL))
    ic.path("M72 133h84l2 8H70z", fill="#D9A84A")
    ic.rect(166, 122, 22, 18, rx=4, fill="#D9A84A")
    ic.rect(38, 148, 180, 58, rx=6, fill=two(ic, "#C48A55", "#8A5228"))
    ic.rect(100, 166, 56, 22, rx=4, fill=two(ic, *BRASS))
    bar(ic, 110, 174, 36, 6, fill="#6A4416")
    ic.rect(218, 172, 6, 6, fill="#C8953E")
    ic.path("M224 175c0-10 10-12 10-4v8c0 8-10 6-10-4z", fill="#D9A84A")


# --- Strawberry ---------------------------------------------------------------

@soft("strawberry")
def strawberry(ic):
    tile(ic, "#3A4C72", "#162240")
    soft_shadow(ic, 128, 214, 64, 10)
    berry = "M128 212C90 200 52 150 56 108C59 80 88 68 128 76C168 68 197 80 200 108C204 150 166 200 128 212z"
    ic.path(berry, fill=two(ic, "#F2483E", "#B0141E"))
    for row in range(5):
        y = 104 + row * 21
        t = (y - 108) / 104
        hw = 70 * (1 - max(0, t) ** 1.6) - 16
        off = 0 if row % 2 else 12
        x = 128 - hw + off
        while x <= 128 + hw:
            ic.ellipse(x, y, 2.6, 3.8, fill="#FFE07A", transform=f"rotate({(x - 128) * 0.35:.0f} {x:.1f} {y:.1f})")
            x += 24
    leaf = two(ic, "#7ACB4A", "#3A8A2A")
    for deg, ln in ((-112, 40), (-68, 36), (-26, 30), (26, 30), (68, 36), (112, 40)):
        tx, ty = polar(128, 80, ln, deg)
        mx, my = polar(128, 80, ln * 0.55, deg)
        lx, ly = polar(mx, my, ln * 0.26, deg - 90)
        rx, ry = polar(mx, my, ln * 0.26, deg + 90)
        ic.path(f"M128 80Q{lx:.1f} {ly:.1f} {tx:.1f} {ty:.1f}Q{rx:.1f} {ry:.1f} 128 80z", fill=leaf)
    ic.path("M128 82c0-14 2-28 12-40", fill="none", stroke="#3E7A26", stroke_width=8, stroke_linecap="round")


# --- Shortwave: a portable shortwave radio ------------------------------------

@soft("shortwave")
def shortwave(ic):
    tile(ic, "#2F6C9A", "#12345A")
    soft_shadow(ic, 128, 216, 98, 11)
    ic.path("M196 92L217 22", fill="none", stroke="#B4BAC2", stroke_width=5, stroke_linecap="round")
    ic.circle(217, 20, 5, fill="#C9CED4")
    ic.path("M64 92V70a10 10 0 0 1 10-10h68a10 10 0 0 1 10 10v22", fill="none", stroke="#2A1A12", stroke_width=10)
    ic.rect(32, 88, 192, 120, rx=20, fill=two(ic, "#F7F1E2", "#D6CAAE"))
    ic.circle(84, 150, 40, fill="#E0D6BE")
    ic.circle(84, 150, 34, fill=two(ic, "#4A4F56", "#2A2D32"))
    for k in range(4):
        y = 132 + k * 12
        hw = math.sqrt(max(0, 26 ** 2 - (y - 150) ** 2))
        bar(ic, 84 - hw, y - 2.5, 2 * hw, 5, fill="#1A1C20")
    bar(ic, 62, 101, 44, 6, fill="#2F6C9A")
    ic.rect(130, 104, 82, 54, rx=7, fill="#1C2A38")
    ic.rect(134, 108, 74, 46, rx=4, fill=two(ic, "#FFF4D6", "#F2D9A0"))
    for k in range(2):
        bar(ic, 140, 118 + k * 16, 8, 5, fill="#C0392B")
        bar(ic, 152, 119 + k * 16, 50, 3, fill="#22303E")
    ic.rect(174, 108, 3.5, 46, rx=1.75, fill="#D0281C")
    _knob(ic, 150, 184, 13, -40, face="#C9CED4", rim="#3A4048", pointer="#2F6C9A")
    _knob(ic, 192, 184, 13, 70, face="#C9CED4", rim="#3A4048", pointer="#2F6C9A")


# --- Podcasts: a studio microphone on its stand ------------------------------

@soft("podcasts")
def podcasts(ic):
    tile(ic, "#4E2C82", "#1C0C3A")
    soft_shadow(ic, 128, 214, 66, 10)
    ic.ellipse(128, 205, 50, 11, fill="#18191C")
    ic.ellipse(128, 202, 50, 11, fill=two(ic, "#5A5E66", "#2E3036"))
    ic.rect(121, 150, 14, 52, fill=two(ic, *STEEL))
    ic.path("M84 98v34a44 44 0 0 0 88 0v-34", fill="none", stroke="#A0A6AE", stroke_width=8)
    ic.rect(96, 24, 64, 144, rx=32, fill=two(ic, "#A06EE4", "#5E2EA8"))
    ic.path("M96 92V56a32 32 0 0 1 64 0v36z", fill=two(ic, "#BCC2C9", "#7E858D"))
    for y in (46, 60, 74):
        ic.line(102, y, 154, y, stroke="#5E646C", stroke_width=2.4, opacity=0.6)
    ic.rect(94, 89, 68, 11, rx=3, fill="#C9CED4")
    ic.circle(128, 128, 14, fill="#EEE4FC")
    ic.circle(128, 128, 3.2, fill="#6E44A8")
    for a0 in (-50, 130):
        p1, p2 = polar(128, 128, 8, a0), polar(128, 128, 8, a0 + 100)
        ic.path(f"M{p1[0]:.1f} {p1[1]:.1f}A8 8 0 0 1 {p2[0]:.1f} {p2[1]:.1f}", fill="none", stroke="#6E44A8",
                stroke_width=2.6, stroke_linecap="round")
    for x in (84, 172):
        ic.circle(x, 100, 8, fill="#2A2C30")


# --- Cozy: an audiobook with headphones over it -------------------------------

@soft("cozy")
def cozy(ic):
    tile(ic, "#2E5C58", "#10302C")
    soft_shadow(ic, 128, 214, 90, 11)
    ic.rect(80, 54, 116, 154, rx=6, fill="#F2EBDA")
    ic.rect(68, 48, 118, 160, rx=7, fill=two(ic, "#E8864A", "#B04A1C"))
    ic.rect(68, 48, 16, 160, rx=7, fill="#8A3412", opacity=0.6)
    ic.rect(95, 93, 78, 96, rx=5, fill="none", stroke="#FFD9A8", stroke_width=2.4)
    bar(ic, 108, 128, 52, 12, fill="#FFE2B8")
    bar(ic, 114, 150, 40, 5, fill="#FFD9A8")
    band = "M50 132C46 66 92 58 128 58C164 58 210 66 206 132"
    ic.path(band, fill="none", stroke="#2A2C30", stroke_width=13)
    ic.path("M92 64C108 59 148 59 164 64", fill="none", stroke="#C9A27A", stroke_width=7, stroke_linecap="round")
    for x in (50, 206):
        ic.rect(x - 7, 118, 14, 18, rx=4, fill=two(ic, *STEEL))
        ic.rect(x - 17, 130, 34, 54, rx=16, fill=two(ic, "#4A4C52", "#1E1F23"))
        ic.circle(x, 157, 8, fill="#E8864A")


# --- EasyEffects: a rack of effects ------------------------------------------

@soft("easyeffects")
def easyeffects(ic):
    tile(ic, "#24406A", "#0C1A30")
    soft_shadow(ic, 128, 216, 96, 10)
    for x in (30, 212):
        ic.rect(x, 26, 14, 186, rx=4, fill=two(ic, *STEEL))
    for y, h in ((34, 70), (108, 42), (154, 54)):
        ic.rect(26, y, 204, h - 2, rx=6, fill=two(ic, "#3C4048", "#22252A"))
    cyan = "#4FD0F0"
    bar(ic, 44, 40, 40, 6, fill="#E6E9ED")
    curve = (4, 7, 9, 6, 2, -2, 0, 5, 8, 6)
    for k, g in enumerate(curve):
        x = 54 + k * 16.6
        ic.rect(x - 1.5, 54, 3, 38, rx=1.5, fill="#0E0F12")
        y = 73 - g * 1.8
        ic.rect(x - 5.5, y - 3.5, 11, 7, rx=2.5, fill="#D4D8DD")
    pts = " ".join(f"{54 + k * 16.6:.1f} {73 - g * 1.8:.1f}" for k, g in enumerate(curve))
    ic.path("M" + pts, fill="none", stroke=cyan, stroke_width=2.4, stroke_linejoin="round", opacity=0.8)
    for k, lit in enumerate((70, 58)):
        y = 118 + k * 10
        ic.rect(44, y, 96, 6, rx=3, fill="#16181C")
        ic.rect(44, y, lit, 6, rx=3, fill="#5BE07A")
        ic.rect(44 + lit - 12, y, 12, 6, rx=0, fill="#F2C14A")
    for k, d in enumerate((-60, 20, 90)):
        _knob(ic, 162 + k * 22, 128, 8.5, d, pointer=cyan)
    ic.rect(44, 162, 92, 38, rx=5, fill="#06131A")
    wave = "M48 181" + "".join(
        f"L{48 + i * 3:.0f} {181 - 12 * math.sin(i * 0.63) * math.exp(-((i - 14) / 10.7) ** 2):.1f}" for i in range(29))
    ic.path(wave, fill="none", stroke=cyan, stroke_width=2.4, stroke_linejoin="round")
    for k, d in enumerate((-110, -20)):
        _knob(ic, 166 + k * 34, 180, 13, d, pointer=cyan)


# --- Volume Control: a big volume knob on a panel ----------------------------

@soft("pavucontrol")
def pavucontrol(ic):
    tile(ic, "#56606E", "#222831")
    soft_shadow(ic, 128, 216, 96, 11)
    cx, cy = 128, 120
    ic.rect(32, 30, 192, 182, rx=20, fill=two(ic, "#F4EFE4", "#D6CDBA"))
    n = 14
    for k in range(n):
        d0 = -135 + k * 270 / n
        f = k / (n - 1)
        col = "#3FAE5A" if f < 0.6 else "#E8B43A" if f < 0.85 else "#D8442E"
        ro = 72 + 14 * f
        p1, p2 = polar(cx, cy, 66, d0), polar(cx, cy, ro, d0)
        p3, p4 = polar(cx, cy, ro, d0 + 13), polar(cx, cy, 66, d0 + 13)
        ic.poly([p1, p2, p3, p4], fill=col, opacity=1 if k <= 9 else 0.3, stroke=col,
                stroke_opacity=1 if k <= 9 else 0.3, stroke_width=1.5, stroke_linejoin="round")
    bar(ic, 104, 196, 48, 7, fill="#5A5E66")
    ic.circle(cx, cy, 58, fill="#16171A")
    ic.circle(cx, cy, 46, fill=two(ic, "#E6E9ED", "#9AA1A9"))
    with ic.g(transform=f"rotate({-135 + 10 * 270 / n} {cx} {cy})"):
        ic.rect(cx - 4, cy - 56, 8, 22, rx=4, fill="#F1F1EF")


# --- Helvum: a patch bay, cables between its jacks ---------------------------

@soft("helvum")
def helvum(ic):
    tile(ic, "#2F5E78", "#10283A")
    soft_shadow(ic, 128, 220, 98, 10)
    with ic.g(transform="translate(0 12)"):
        ic.rect(22, 50, 212, 104, rx=10, fill=two(ic, "#3C4048", "#1E2024"))
        bar(ic, 38, 58, 34, 6, fill="#E6E9ED")
        xs = [48 + k * 26.6 for k in range(7)]
        for y in (94, 132):
            for x in xs:
                ic.circle(x, y, 8, fill=two(ic, "#C9CED4", "#8D949C"))
                ic.circle(x, y, 4, fill="#0A0B0D")
        cables = (("#4A8BE8", xs[0], xs[3], 214), ("#B07AF0", xs[2], xs[6], 222), ("#3CC8A8", xs[5], xs[1], 230))
        for col, x1, x2, sag in cables:
            ic.path(f"M{x1:.1f} 112C{x1:.1f} {sag} {x2:.1f} {sag} {x2:.1f} 150", fill="none", stroke=col,
                    stroke_width=7)
        for col, x1, x2, _ in cables:
            for x, y in ((x1, 94), (x2, 132)):
                ic.rect(x - 4, y - 2, 8, 6, fill="#B4BAC2")
                ic.rect(x - 6, y + 2, 12, 17, rx=4, fill=col)


# --- Ardour: a mixing desk, its meters lit ----------------------------------

@soft("ardour")
def ardour(ic):
    tile(ic, "#8E3028", "#3C0E0A")
    soft_shadow(ic, 128, 216, 104, 11)
    red = "#E8402E"
    ic.rect(44, 30, 168, 44, rx=8, fill=two(ic, "#3A3D44", "#1E1F23"))
    ic.rect(50, 36, 156, 32, rx=4, fill="#0A0B0D")
    for k, lv in enumerate((0.65, 0.85, 0.5, 0.78, 0.4)):
        for j, l in enumerate((lv, max(0.15, lv - 0.15))):
            x = 57 + k * 25 + j * 8
            h = 24 * l
            ic.rect(x, 40, 5, 24, rx=2, fill="#24262B")
            ic.rect(x, 64 - h, 5, h, rx=2, fill="#5BE07A")
            if l > 0.7:
                ic.rect(x, 64 - h, 5, 5, rx=2, fill="#F2C14A")
    ic.rect(184, 39, 18, 26, rx=3, fill=red)
    ic.path("M187.5 61L193 43L198.5 61M189.5 55H196.5", fill="none", stroke="#fff", stroke_width=3,
            stroke_linejoin="round")
    ic.path("M40 76H216L232 202H24z", fill=two(ic, "#4A4E56", "#2A2C31"), stroke="#3E4148", stroke_width=4,
            stroke_linejoin="round")
    ic.path("M24 202H232v6a6 6 0 0 1-6 6H30a6 6 0 0 1-6-6z", fill="#16171A")
    for k in range(6):
        t = k / 5
        x = 54 + k * 29.6
        master = k == 5
        _knob(ic, x, 92, 7.5, -40 + k * 22, pointer=red if master else "#E6E9ED")
        _knob(ic, x + (t - 0.5) * 2, 112, 7.5, 50 - k * 18, pointer="#F2C14A")
        sx = x + (t - 0.5) * 6
        ic.rect(sx - 2, 132, 4, 60, rx=2, fill="#0E0F11")
        fy = (170, 150, 160, 144, 176, 152)[k]
        ic.rect(sx - 8, fy - 6, 16, 13, rx=3, fill=two(ic, "#FF8A6E", "#C8321E") if master else
                two(ic, "#F1F1EF", "#B4BAC2"))


# --- LMMS: a synthesiser, its knobs and keys ---------------------------------

@soft("lmms")
def lmms(ic):
    tile(ic, "#2E8A5C", "#0E3C24")
    soft_shadow(ic, 128, 206, 108, 11)
    green = "#4FE08A"
    ic.rect(20, 66, 216, 134, rx=14, fill=two(ic, "#B47A48", "#7A4824"))
    ic.rect(34, 66, 188, 134, fill=two(ic, "#3A3D44", "#1E2024"))
    ic.rect(42, 76, 58, 38, rx=5, fill="#06140C")
    ic.path("M48 106" + "".join("l8 -18l0 18" for _ in range(6)), fill="none", stroke=green, stroke_width=2.4,
            stroke_linejoin="round", transform="translate(0 -2)")
    for r in range(2):
        for k in range(4):
            _knob(ic, 116 + k * 26, 86 + r * 24, 9, (-110, -30, 40, 100, -80, 10, 70, -50)[r * 4 + k],
                  pointer=green)
    kx, ky, kw, kh = 36, 136, 184, 58
    ic.rect(kx - 2, ky - 2, kw + 4, kh + 4, rx=3, fill="#0A0B0D")
    n = 10
    w = kw / n
    for i in range(n):
        ic.rect(kx + i * w + 0.8, ky, w - 1.6, kh, rx=3, fill=two(ic, "#FFFFFF", "#DDD6C8"))
    for i in range(n - 1):
        if i % 7 in (2, 6):
            continue
        ic.rect(kx + (i + 1) * w - w * 0.3, ky, w * 0.6, kh * 0.6, rx=2.5, fill="#1E2024")


# --- MuseScore: a score, open on its music stand -----------------------------

@soft("musescore")
def musescore(ic):
    tile(ic, "#2F6EC4", "#123874")
    soft_shadow(ic, 128, 214, 92, 11)
    ic.rect(121, 186, 14, 30, fill=two(ic, *STEEL))
    ic.path("M30 50h196v136a8 8 0 0 1-8 8H38a8 8 0 0 1-8-8z", fill=two(ic, "#2A3240", "#141A24"))
    ink = "#2A2E36"
    for side, rot in ((-1, -2), (1, 2)):
        x0 = 38 if side < 0 else 128
        with ic.g(transform=f"rotate({rot} 128 190)"):
            ic.rect(x0, 30, 90, 160, rx=3, fill=two(ic, "#FFFDF7", "#ECE6D8") if side < 0 else
                    two(ic, "#FFFFFF", "#ECE8DF"))
            if side < 0:
                bar(ic, x0 + 20, 40, 50, 7, fill=ink)
            for st in range(4 if side < 0 else 5):
                sy = (62 if side < 0 else 44) + st * 30
                for ln in range(5):
                    ic.rect(x0 + 8, sy + ln * 3.6 - 0.6, 74, 1.2, fill=ink, opacity=0.6)
                for j in range(4):
                    nx = x0 + 22 + j * 16
                    ny = sy + 14.4 - ((st * 3 + j * 5) % 6) * 1.8
                    ic.ellipse(nx, ny, 3.2, 2.4, fill=ink, transform=f"rotate(-20 {nx} {ny})")
                    ic.rect(nx + 2, ny - 12, 1.4, 12, fill=ink)
    sx, sy = 194, 176
    ic.circle(sx, sy, 16, fill=two(ic, "#4A8EF0", "#1A56B8"))
    for k in range(3):
        ic.line(sx - 9, sy - 5 + k * 5, sx + 9, sy - 5 + k * 5 - 3, stroke="#fff", stroke_width=2.4,
                stroke_linecap="round")
    ic.rect(26, 186, 204, 12, rx=5, fill=two(ic, "#3A4456", "#1A2230"))


# --- REAPER: a reel-to-reel tape machine -------------------------------------

def _reel(ic, cx, cy, r, pack):
    ic.circle(cx, cy, pack, fill="#4A2E1A")
    win = []
    for k in range(3):
        a = k * 120 + 20
        p1, p2 = polar(cx, cy, r * 0.32, a - 34), polar(cx, cy, r * 0.32, a + 34)
        q1, q2 = polar(cx, cy, r * 0.84, a + 46), polar(cx, cy, r * 0.84, a - 46)
        win.append(f"M{p1[0]:.1f} {p1[1]:.1f}A{r * 0.32:.1f} {r * 0.32:.1f} 0 0 1 {p2[0]:.1f} {p2[1]:.1f}"
                   f"L{q1[0]:.1f} {q1[1]:.1f}A{r * 0.84:.1f} {r * 0.84:.1f} 0 0 0 {q2[0]:.1f} {q2[1]:.1f}z")
    disc = f"M{cx - r:.1f} {cy}a{r} {r} 0 1 0 {2 * r} 0a{r} {r} 0 1 0 {-2 * r} 0z" + "".join(win)
    ic.path(disc, fill=two(ic, "#E6E9ED", "#9AA1A9"), fill_rule="evenodd", stroke="#6A7078", stroke_width=1.5,
            stroke_linejoin="round")
    ic.circle(cx, cy, r * 0.22, fill="#C9CED4")
    ic.circle(cx, cy, r * 0.09, fill="#1A1B1E")


@soft("reaper")
def reaper(ic):
    tile(ic, "#4A5E56", "#18241F")
    soft_shadow(ic, 128, 216, 98, 11)
    ic.rect(30, 26, 196, 186, rx=16, fill=two(ic, "#3C4048", "#1A1B1E"))
    ic.rect(36, 32, 184, 174, rx=12, fill=two(ic, "#C9CED4", "#8D949C"))
    ic.path("M48 82L74 150H182L208 82", fill="none", stroke="#3A2414", stroke_width=3)
    _reel(ic, 82, 80, 40, 34)
    _reel(ic, 174, 80, 40, 22)
    for x in (74, 182):
        ic.circle(x, 150, 7, fill="#D4D8DD")
        ic.circle(x, 150, 2.5, fill="#1A1B1E")
    ic.rect(98, 136, 60, 26, rx=6, fill=two(ic, "#3A3D44", "#1E1F23"))
    for x, c in ((108, "#9AA1A9"), (122, "#9AA1A9"), (136, "#C99645")):
        ic.rect(x, 141, 9, 10, rx=3, fill=c)
    ic.rect(46, 172, 40, 16, rx=4, fill="#0A0B0D")
    bar(ic, 52, 177, 28, 6, fill="#5BE07A")
    keys = (("#E6E9ED", "rew"), ("#E6E9ED", "stop"), ("#4CC870", "play"), ("#E8402E", "rec"))
    for k, (c, kind) in enumerate(keys):
        x = 98 + k * 28
        ic.rect(x, 172, 22, 16, rx=4, fill=two(ic, "#4A4E56", "#26282C"))
        mx, my = x + 11, 180
        if kind == "rew":
            ic.path(f"M{mx} {my - 4}l-6 4l6 4zM{mx + 6} {my - 4}l-6 4l6 4z", fill=c)
        elif kind == "stop":
            ic.rect(mx - 4, my - 4, 8, 8, rx=1.5, fill=c)
        elif kind == "play":
            ic.path(f"M{mx - 3} {my - 5}l8 5l-8 5z", fill=c)
        else:
            ic.circle(mx, my, 4.5, fill=c)


# --- TIDAL: a black hi-fi amplifier ------------------------------------------

def _tidal_mark(ic, x, y, s, fill):
    """Four diamonds: three in a row, one beneath the middle."""
    for dx, dy in ((-1, 0), (0, 0), (1, 0), (0, 1)):
        cx, cy = x + dx * s, y + dy * s
        h = s * 0.48
        ic.path(f"M{cx:.1f} {cy - h:.1f}L{cx + h:.1f} {cy:.1f}L{cx:.1f} {cy + h:.1f}L{cx - h:.1f} {cy:.1f}z",
                fill=fill)


@soft("tidal")
def tidal(ic):
    tile(ic, "#4A4F58", "#15171B")
    soft_shadow(ic, 128, 206, 110, 11)
    ic.path("M36 58H220L232 74H24z", fill="#3A3D43", stroke="#3A3D43", stroke_width=3, stroke_linejoin="round")
    ic.rect(24, 74, 208, 122, rx=7, fill=two(ic, "#2A2B2F", "#141416"))
    for x in (44, 212):
        ic.rect(x - 12, 194, 24, 10, rx=3, fill="#0A0A0B")
    for k, deg in enumerate((-14, 6)):
        x0 = 36 + k * 58
        ic.rect(x0 - 2, 86, 56, 46, rx=6, fill="#060607")
        ic.rect(x0, 88, 52, 42, rx=4, fill=two(ic, "#FFF0C8", "#EEC878"))
        mx, my = x0 + 26, 132
        ic.path(f"M{x0 + 8} 110A30 30 0 0 1 {x0 + 44} 110", fill="none", stroke="#2A2010", stroke_width=1.6)
        ic.path(f"M{x0 + 34} 104A30 30 0 0 1 {x0 + 44} 110", fill="none", stroke="#C8301C", stroke_width=3.4)
        p = polar(mx, my, 36, deg)
        ic.line(mx, my, p[0], p[1], stroke="#1A1A1C", stroke_width=2)
    cx, cy = 190, 116
    ic.circle(cx, cy, 31, fill=two(ic, "#D4D8DD", "#6A7078"))
    ic.circle(cx, cy, 26, fill=two(ic, "#F4F6F8", "#A8AEB6"))
    p = polar(cx, cy, 19, -30)
    ic.circle(p[0], p[1], 3, fill="#1A1A1C")
    _tidal_mark(ic, 50, 152, 10, "#F1F1EF")
    bar(ic, 70, 148, 52, 9, fill="#F1F1EF")
    for k in range(3):
        _knob(ic, 52 + k * 22, 182, 7, -30 + k * 30, face="#C9CED4", rim="#3A3D44", pointer="#1A1A1C")
    ic.circle(142, 182, 3, fill="#DCE8FF")
