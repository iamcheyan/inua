"""The soft drawings of the tier 2 "files" batch (drawings/apps_t2_files.py):
the same objects with about half the detail, no text."""

from lib import bar, polar, soft, soft_shadow, tile, two

BRASS = ("#E2B45E", "#B88433")
STEEL = ("#AEB4BB", "#8D949C")


def rot(deg, cx, cy):
    return f"rotate({deg:g} {cx:g} {cy:g})"


def sector(cx, cy, r_out, r_in, a1, a2):
    large = 1 if (a2 - a1) % 360 > 180 else 0
    x1, y1 = polar(cx, cy, r_out, a1)
    x2, y2 = polar(cx, cy, r_out, a2)
    x3, y3 = polar(cx, cy, r_in, a2)
    x4, y4 = polar(cx, cy, r_in, a1)
    return (f"M{x1:.1f} {y1:.1f}A{r_out} {r_out} 0 {large} 1 {x2:.1f} {y2:.1f}"
            f"L{x3:.1f} {y3:.1f}A{r_in} {r_in} 0 {large} 0 {x4:.1f} {y4:.1f}Z")


def bolt(x, y, s=1.0):
    pts = [(6, 0), (16, 0), (11, 11), (18, 11), (4, 30), (8, 16), (1, 16)]
    return "M" + "L".join(f"{x + px * s:.1f} {y + py * s:.1f}" for px, py in pts) + "Z"


# --- Files (Nautilus) --------------------------------------------------------

def _label(ic, x, y, w, h):
    ic.rect(x - 2, y - 2, w + 4, h + 4, rx=4, fill=STEEL[1])
    ic.rect(x, y, w, h, rx=2.5, fill="#FBF4E2")
    bar(ic, x + 7, y + h / 2 - 3, w - 14, 6, fill="#24406A")


@soft("nautilus")
def nautilus(ic):
    tile(ic, "#4F86C6", "#1E3D68")
    soft_shadow(ic, 128, 212, 92, 12)
    ic.rect(58, 32, 140, 176, rx=12, fill=two(ic, "#F2F4F7", "#BFC6D0"))
    ic.rect(64, 202, 128, 8, rx=3, fill="#4C5560")
    ic.rect(66, 40, 124, 80, rx=6, fill="#1E2630")
    ic.poly([(70, 46), (186, 46), (198, 98), (58, 98)], fill="#3A4552")
    for y, col, slot in ((56, "#C69447", 0), (68, "#3584E4", 2), (80, "#E3BA6C", 1)):
        f = (y - 46) / 52
        l, r = 70 - 12 * f + 3, 186 + 12 * f - 3
        tx = l + 12 + slot * 36
        ic.rect(tx, y - 8, 30, 12, rx=4, fill=col)
        ic.rect(l, y, r - l, 18, rx=4, fill=col)
    ic.rect(56, 98, 144, 46, rx=8, fill=two(ic, "#5C9EEC", "#1F64BA"))
    _label(ic, 104, 105, 48, 16)
    ic.rect(98, 128, 60, 9, rx=4.5, fill=two(ic, *STEEL))
    ic.rect(66, 154, 124, 46, rx=6, fill=two(ic, "#E6EAF0", "#BCC4CE"))
    _label(ic, 106, 160, 44, 15)
    ic.rect(100, 182, 56, 9, rx=4.5, fill=two(ic, *STEEL))


# --- Dolphin -----------------------------------------------------------------

DOLPHIN = ("M76 2C70 0 64-2 58-4C54-14 42-19 26-18C16-17 10-18 6-19C0-28-8-36-14-40C-14-32-16-24-20-16"
           "C-36-11-52-6-62-3C-68-8-76-14-86-17C-81-10-77-4-72 0C-77 4-81 10-86 17C-76 13-68 8-62 5"
           "C-46 10-22 16 0 15C2 22-2 30-8 35C0 31 8 24 14 15C32 13 50 9 60 6C66 5 72 4 76 2Z")


@soft("dolphin")
def dolphin(ic):
    tile(ic, "#24496F", "#0D1D31")
    soft_shadow(ic, 128, 214, 96, 12)
    ic.path("M40 110a8 8 0 0 1 8-8h38a8 8 0 0 1 6 3l7 8h109a8 8 0 0 1 8 8v82a8 8 0 0 1-8 8H48a8 8 0 0 1-8-8z",
            fill=two(ic, "#1D86D0", "#0D4E8C"))
    ic.rect(56, 108, 134, 40, rx=5, fill="#FFFFFF", transform=rot(-3, 120, 120))
    ic.rect(66, 112, 132, 40, rx=5, fill="#ECF1F5", transform=rot(2, 130, 120))
    with ic.g(transform="translate(134 72) rotate(-30) scale(1.02)"):
        ic.path(DOLPHIN, fill=two(ic, "#6CC2F2", "#1E78BE"))
        ic.path("M-58 4C-40 9-20 14 0 13C20 13 44 8 58 5C66 4 72 3 74 2C66 7 50 12 30 15C10 18-20 18-40 12Z",
                fill="#E2F4FD")
        ic.circle(44, -6, 3.2, fill="#0B2A48")
    for x, y, r in ((64, 110, 4), (74, 100, 3), (112, 104, 3.5)):
        ic.circle(x, y, r, fill="#D8F2FF")
    ic.path("M34 130a8 8 0 0 1 8-8h172a8 8 0 0 1 8 8l-7 72a9 9 0 0 1-9 8H50a9 9 0 0 1-9-8z",
            fill=two(ic, "#6CC8F6", "#2290D6"))
    ic.path("M64 184c12-10 24-10 36 0s24 10 36 0 24-10 36 0 14 8 20 6", fill="none", stroke="#0F5C9C",
            stroke_width=5, stroke_linecap="round", opacity=0.4)
    bar(ic, 52, 148, 52, 9, fill="#0D4E8C", opacity=0.55)


# --- Thunar ------------------------------------------------------------------

@soft("thunar")
def thunar(ic):
    tile(ic, "#4C5478", "#1A1D33")
    soft_shadow(ic, 122, 212, 102, 12)
    ic.poly([(34, 96), (162, 96), (184, 76), (56, 76)], fill="#E2B67E")
    ic.poly([(162, 96), (184, 76), (184, 186), (162, 206)], fill=two(ic, "#A46E3A", "#6E4420"))
    ic.rect(34, 96, 128, 110, fill="#5E3816")
    for y in (96, 133, 170):
        ic.rect(34, y + 2, 128, 33, rx=2, fill=two(ic, "#D9A86C", "#BF8A4E"))
    for x in (34, 148):
        ic.rect(x, 96, 14, 110, fill="#B07A40")
    ic.path(bolt(80, 106, 1.8), fill="#1E6FD0", stroke="#1E6FD0", stroke_width=2, stroke_linejoin="round")
    bar(ic, 62, 174, 72, 10, fill="#1E6FD0", opacity=0.85)
    ic.rect(182, 96, 18, 76, rx=6, fill=two(ic, "#7A4026", "#4A2410"))
    ic.path("M166 166h54l6 8v26l-6 8h-54l-6-8v-26z", fill=two(ic, "#C9CFD6", "#7C8590"), stroke="#C9CFD6",
            stroke_width=2, stroke_linejoin="round")
    ic.path(bolt(184, 172, 1.0), fill="#2B8FE3")
    ic.rect(183, 158, 14, 10, rx=3, fill=two(ic, *STEEL))


# --- Nemo --------------------------------------------------------------------

FISH = "M-10 0C-6-7 5-7 9 0C5 7-6 7-10 0ZM8 0L14-6V6Z"


@soft("nemo")
def nemo(ic):
    tile(ic, "#2D7464", "#0E322A")
    cx, cy = 128, 118
    soft_shadow(ic, 128, 222, 80, 10)
    timber = ic.lin([(0, "#C88C52"), (1, "#7E4C22")], 40, 30, 220, 210, units="userSpaceOnUse")
    for k in range(8):
        with ic.g(transform=rot(k * 45 + 22.5, cx, cy)):
            ic.rect(cx - 4.5, cy - 74, 9, 56, fill=timber)
            t = cy - 72
            ic.path(f"M{cx - 4.5} {t}L{cx - 5} {t - 6}C{cx - 9} {t - 11} {cx - 8} {t - 19} {cx - 5} {t - 23}"
                    f"A5.5 5.5 0 0 1 {cx + 5} {t - 23}C{cx + 8} {t - 19} {cx + 9} {t - 11} {cx + 5} {t - 6}"
                    f"L{cx + 4.5} {t}Z", fill=timber)
    ic.circle(cx, cy, 66, fill="none", stroke=timber, stroke_width=16)
    ic.circle(cx, cy, 66, fill="none", stroke=two(ic, *BRASS), stroke_width=4.5)
    ic.circle(cx, cy, 28, fill=two(ic, *BRASS))
    ic.circle(cx, cy, 17, fill=two(ic, "#94CF5A", "#4E9A22"))
    with ic.g(transform=f"translate({cx - 1} {cy + 1}) scale(1.05)"):
        ic.path(FISH, fill="#F4FBEA")


# --- Flatseal ----------------------------------------------------------------

INK = "#2C6BD6"


@soft("flatseal")
def flatseal(ic):
    tile(ic, "#6E5C9A", "#2B2149")
    soft_shadow(ic, 124, 214, 100, 12)
    with ic.g(transform=rot(-5, 104, 140)):
        ic.rect(36, 52, 132, 160, rx=8, fill=two(ic, "#FBF6EA", "#ECE3CF"))
        bar(ic, 48, 64, 70, 9, fill="#2B2149")
        for i in range(3):
            y = 92 + i * 15
            ic.rect(48, y - 8, 10, 10, rx=2.5, fill="none", stroke="#6A665D", stroke_width=1.6)
            ic.path(f"M49.5 {y - 3.5}l2.5 3 5-6", fill="none", stroke=INK, stroke_width=2.4, stroke_linecap="round",
                    stroke_linejoin="round")
            bar(ic, 64, y - 6.5, (52, 64, 44)[i], 7, fill="#B9B4AA")
        sx, sy = 92, 168
        with ic.g(opacity=0.9):
            ic.circle(sx, sy, 30, fill="none", stroke=INK, stroke_width=4.5)
            ic.circle(sx, sy, 22, fill="none", stroke=INK, stroke_width=2)
            ic.circle(sx, sy, 15, fill=INK)
            ic.path(f"M{sx - 7} {sy}l5 5.5 10-11", fill="none", stroke="#FCF9F2", stroke_width=4.5,
                    stroke_linecap="round", stroke_linejoin="round")
    ic.rect(142, 170, 68, 22, rx=5, fill="#1D3C8A")
    ic.rect(140, 148, 72, 26, rx=6, fill=two(ic, "#D9A86C", "#A06C38"))
    ic.rect(148, 155, 56, 12, rx=3, fill="#FCF9F2")
    bar(ic, 158, 158, 36, 6, fill=INK)
    ic.path("M166 148c2-12 4-24 2-36h16c-2 12 0 24 2 36z", fill=two(ic, "#C48A55", "#8A5628"))
    ic.circle(176, 88, 26, fill=two(ic, "#5C98EE", "#2556B0"))
    ic.path("M166 90l7 7.5 12-13", fill="none", stroke="#fff", stroke_width=5, stroke_linecap="round",
            stroke_linejoin="round", opacity=0.9)


# --- Mission Center ----------------------------------------------------------

@soft("mission-center")
def mission_center(ic):
    tile(ic, "#3A4182", "#111435")
    soft_shadow(ic, 128, 214, 102, 11)
    ic.rect(36, 36, 184, 112, rx=14, fill=two(ic, "#4A5262", "#252A34"))
    for x, w in ((46, 56), (108, 54), (168, 42)):
        ic.rect(x, 48, w, 62, rx=6, fill="#0C1A2A")
    pts = [(52, 98), (60, 92), (68, 94), (76, 80), (84, 86), (92, 74), (98, 82)]
    ic.path("M" + "L".join(f"{x} {y}" for x, y in pts) + "L98 104L52 104Z", fill="#33B4FF", opacity=0.25)
    ic.path("M" + "L".join(f"{x} {y}" for x, y in pts), fill="none", stroke="#5CC8FF", stroke_width=3,
            stroke_linejoin="round", stroke_linecap="round")
    ic.ellipse(135, 79, 22, 9, fill="none", stroke="#9FE0FF", stroke_width=2, opacity=0.7,
               transform=rot(-20, 135, 79))
    ic.circle(135, 79, 11, fill=two(ic, "#5BB7FF", "#1A5EAA"))
    ic.circle(154, 71, 3.5, fill="#FFD447")
    for i, (lvl, col) in enumerate(((0.7, "#3DDC84"), (0.45, "#FFB547"), (0.85, "#3DDC84"))):
        bx = 174 + i * 11
        ic.rect(bx, 56 + 46 * (1 - lvl), 8, 46 * lvl, rx=2.5, fill=col)
    for i, col in enumerate(("#3DDC84", "#FFB547", "#3DDC84", "#FF5B4F", "#5CC8FF", "#3DDC84")):
        ic.rect(54 + i * 26, 122, 18, 8, rx=4, fill=col)
    ic.poly([(36, 148), (220, 148), (232, 166), (24, 166)], fill="#5C6578")
    ic.rect(24, 166, 208, 40, rx=8, fill=two(ic, "#3A4150", "#1E222A"))
    for i in range(4):
        x = 44 + i * 22
        up = i % 2 == 0
        ic.rect(x - 5, 176, 10, 20, rx=3, fill="#0C0F14")
        ic.circle(x, 178 if up else 194, 4.5, fill="#E6EAEE")
    ic.rect(140, 176, 30, 20, rx=4, fill="#0C0F14")
    bar(ic, 146, 183, 18, 6, fill="#3DDC84")
    ic.circle(196, 186, 15, fill=two(ic, "#F2483A", "#A8160C"))


# --- Resources ---------------------------------------------------------------

def _gauge(ic, cx, cy, r, value):
    ic.circle(cx, cy, r, fill=two(ic, "#D7DCE1", "#7C858F"))
    ic.circle(cx, cy, r - 6, fill="#111317")
    ic.path(sector(cx, cy, r - 10, r - 16, -120, 60), fill="#3DDC84")
    ic.path(sector(cx, cy, r - 10, r - 16, 84, 120), fill="#E5483A")
    for i in range(5):
        a = -120 + 60 * i
        ic.line(*polar(cx, cy, r - 18, a), *polar(cx, cy, r - 25, a), stroke="#F4F6F8", stroke_width=3,
                stroke_linecap="round")
    bar(ic, cx - 12, cy + 16, 24, 7, fill="#3DDC84", opacity=0.8)
    with ic.g(transform=rot(-120 + 240 * value, cx, cy)):
        ic.path(f"M{cx - 3.5} {cy + 8}L{cx - 1.2} {cy - r + 14}H{cx + 1.2}L{cx + 3.5} {cy + 8}Z", fill="#FF8A2A")
    ic.circle(cx, cy, 7, fill="#3A4048")


@soft("resources")
def resources(ic):
    tile(ic, "#2F7259", "#0E3022")
    soft_shadow(ic, 128, 208, 104, 12)
    hood = ("M22 130C22 82 50 54 92 54C108 54 118 60 128 60C138 60 148 54 164 54C206 54 234 82 234 130"
            "V176a18 18 0 0 1-18 18H40a18 18 0 0 1-18-18z")
    ic.path(hood, fill=two(ic, "#3E434A", "#16181B"))
    _gauge(ic, 78, 132, 47, 0.34)
    _gauge(ic, 178, 132, 47, 0.62)
    ic.circle(128, 92, 4.5, fill="#3DDC84")
    ic.circle(128, 108, 4.5, fill="#FFB547")


# --- System Monitor ----------------------------------------------------------

def ecg(x0, y0, w, beats, amp):
    shape = [(0, 0), (0.18, 0), (0.24, -0.15), (0.3, 0), (0.33, 0.12), (0.37, -1), (0.42, 0.35),
             (0.47, 0), (0.6, 0), (0.67, -0.25), (0.75, 0)]
    bw = w / beats
    pts = [(x0 + b * bw + t * bw, y0 + v * amp) for b in range(beats) for t, v in shape] + [(x0 + w, y0)]
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def heart(x, y, s):
    return (f"M{x} {y + 3 * s}C{x - 6 * s} {y - 1 * s} {x - 5 * s} {y - 6 * s} {x - 2.4 * s} {y - 6 * s}"
            f"C{x - 1 * s} {y - 6 * s} {x} {y - 5 * s} {x} {y - 4 * s}C{x} {y - 5 * s} {x + 1 * s} {y - 6 * s}"
            f" {x + 2.4 * s} {y - 6 * s}C{x + 5 * s} {y - 6 * s} {x + 6 * s} {y - 1 * s} {x} {y + 3 * s}Z")


@soft("gnome-system-monitor")
def gnome_system_monitor(ic):
    tile(ic, "#8E4044", "#3A1418")
    soft_shadow(ic, 128, 214, 100, 12)
    ic.path("M80 56V42a12 12 0 0 1 12-12h72a12 12 0 0 1 12 12V56", fill="none", stroke="#D9DCDA", stroke_width=12)
    ic.rect(28, 48, 200, 158, rx=20, fill=two(ic, "#F7F7F5", "#C4C9C7"))
    ic.rect(38, 58, 160, 118, rx=10, fill="#0A1216")
    ic.path(ecg(46, 92, 100, 2, 22), fill="none", stroke="#3DE07A", stroke_width=3, stroke_linejoin="round",
            stroke_linecap="round")
    ic.path("M46 130" + "c8-14 16-14 24 0 " * 4, fill="none", stroke="#3CC8F0", stroke_width=3,
            stroke_linecap="round")
    ic.path("M46 160" + "c8-10 16-10 24 0 " * 4, fill="none", stroke="#F2D24A", stroke_width=2.6,
            stroke_linecap="round")
    ic.path(heart(160, 78, 1.3), fill="#FF5A5A")
    bar(ic, 156, 90, 32, 14, fill="#3DE07A")
    bar(ic, 162, 122, 26, 11, fill="#3CC8F0")
    bar(ic, 162, 152, 26, 11, fill="#F2D24A")
    ic.circle(214, 76, 10, fill=two(ic, "#E9ECEB", "#9AA0A2"))
    for i, col in enumerate(("#D8463C", "#E4E8E7", "#E4E8E7")):
        ic.rect(205, 100 + i * 22, 18, 14, rx=4, fill=col)
    for i in range(5):
        ic.rect(46 + i * 12, 184, 6, 14, rx=3, fill="#8A908E", opacity=0.6)


# --- BleachBit ---------------------------------------------------------------

BOTTLE = ("M98 82H128V96C128 104 150 110 154 128V196Q154 208 142 208H82Q70 208 70 196V128"
          "C74 110 98 104 98 96Z")


@soft("bleachbit")
def bleachbit(ic):
    tile(ic, "#3792A8", "#0F3E4C")
    soft_shadow(ic, 118, 212, 64, 10)
    ic.path(BOTTLE, fill="#E4F2F7")
    inside = ic.clip(f'<path d="{BOTTLE}"/>')
    with ic.g(clip_path=inside):
        ic.rect(60, 120, 100, 100, fill=two(ic, "#8AD4F2", "#3C9CCC"))
    ic.rect(72, 140, 80, 52, rx=6, fill="#FFFFFF")
    ic.path("M72 146a6 6 0 0 1 6-6h68a6 6 0 0 1 6 6v8H72z", fill="#C8281E")
    bar(ic, 84, 164, 56, 10, fill="#1F4A8A")
    bar(ic, 92, 179, 40, 5, fill="#9AA0A8")
    ic.rect(94, 72, 38, 14, rx=4, fill=two(ic, "#E6E9EC", "#A6AEB6"))
    head = "M90 74V56C90 44 100 38 112 38H164a6 6 0 0 1 6 6V56a6 6 0 0 1-6 6H140C134 62 132 66 132 74Z"
    ic.path(head, fill=two(ic, "#F2584A", "#B01E14"))
    ic.rect(170, 44, 9, 12, rx=3, fill="#2A2C30")
    ic.path("M140 62C146 70 150 82 148 100C146 104 142 104 140 100C140 86 136 74 132 66Z", fill="#B8261A")
    for x, y, r in ((190, 44, 3), (200, 54, 2.6), (196, 36, 2.2), (212, 46, 2.4), (208, 62, 2), (222, 38, 1.8)):
        ic.circle(x, y, r, fill="#E8FAFF", opacity=0.9)
    x, y, s = 214, 22, 7
    ic.path(f"M{x} {y - s}L{x + s * 0.3} {y - s * 0.3}L{x + s} {y}L{x + s * 0.3} {y + s * 0.3}L{x} {y + s}"
            f"L{x - s * 0.3} {y + s * 0.3}L{x - s} {y}L{x - s * 0.3} {y - s * 0.3}Z", fill="#fff")


# --- Disk Usage Analyzer -----------------------------------------------------

GNOME_COLOURS = ["#3584E4", "#33D17A", "#F6D32D", "#FF7800", "#E01B24", "#9141AC"]


@soft("baobab")
def baobab(ic):
    tile(ic, "#7C4A70", "#331830")
    soft_shadow(ic, 128, 216, 92, 12)
    ic.rect(50, 34, 152, 180, rx=14, fill=two(ic, "#C99A66", "#946234"))
    ic.rect(60, 50, 132, 156, rx=6, fill="#FFFFFF")
    bar(ic, 70, 64, 60, 9, fill="#331830")
    cx, cy = 126, 140
    ic.circle(cx, cy, 14, fill="#5E5C64")
    rings = [
        (16, 34, [(0, 120, 0), (120, 200, 1), (200, 260, 2), (260, 310, 3), (310, 360, 4)]),
        (36, 52, [(0, 70, 0), (120, 175, 1), (200, 240, 2), (260, 295, 3)]),
    ]
    for depth, (ri, ro, segs) in enumerate(rings):
        for a1, a2, c in segs:
            ic.path(sector(cx, cy, ro, ri, a1 + 1.5, a2 - 1.5), fill=GNOME_COLOURS[c], opacity=1 - depth * 0.25)
    ic.rect(98, 26, 60, 26, rx=8, fill=two(ic, *STEEL))
    ic.rect(108, 18, 40, 14, rx=7, fill="none", stroke=STEEL[0], stroke_width=5)
    lx, ly = 176, 178
    ic.line(lx + 16, ly + 16, lx + 36, ly + 36, stroke="#2A2C30", stroke_width=13, stroke_linecap="round")
    ic.circle(lx, ly, 25, fill="#FFFFFF")
    view = ic.clip(f'<circle cx="{lx}" cy="{ly}" r="25"/>')
    with ic.g(clip_path=view):
        with ic.g(transform=f"translate({lx} {ly}) scale(1.6) translate({-lx} {-ly})"):
            for ri, ro, segs in rings:
                for a1, a2, c in segs:
                    ic.path(sector(cx, cy, ro, ri, a1 + 1.5, a2 - 1.5), fill=GNOME_COLOURS[c])
    ic.circle(lx, ly, 25, fill="none", stroke="#3A3D44", stroke_width=7)


# --- Backups (Deja Dup) ------------------------------------------------------

@soft("deja-dup")
def deja_dup(ic):
    tile(ic, "#4C7158", "#1A2E21")
    soft_shadow(ic, 124, 214, 98, 12)
    for x in (54, 176):
        ic.rect(x, 198, 24, 12, rx=3, fill="#1A1C20")
    ic.poly([(196, 40), (212, 30), (212, 190), (196, 204)], fill="#24282D")
    ic.poly([(44, 40), (196, 40), (212, 30), (60, 30)], fill="#6A717A")
    ic.rect(44, 40, 152, 164, rx=12, fill=two(ic, "#555C65", "#2C3036"))
    ic.rect(57, 53, 126, 138, rx=8, fill=two(ic, "#656C75", "#3A3F46"))
    for y in (68, 160):
        ic.rect(49, y, 12, 22, rx=4, fill=two(ic, *STEEL))
    cx, cy = 120, 108
    ic.path(sector(cx, cy, 47, 39, 210, 520), fill="#3DDC84")
    ic.poly([polar(cx, cy, 54, 210), polar(cx, cy, 32, 210), polar(cx, cy, 43, 188)], fill="#3DDC84")
    ic.circle(cx, cy, 34, fill=two(ic, *BRASS))
    ic.circle(cx, cy, 27, fill="#FFFBF0")
    for h in range(0, 12, 3):
        ic.line(*polar(cx, cy, 24, h * 30), *polar(cx, cy, 19, h * 30), stroke="#2A2C30", stroke_width=3,
                stroke_linecap="round")
    ic.line(cx, cy, *polar(cx, cy, 12, 285), stroke="#23262B", stroke_width=4, stroke_linecap="round")
    ic.line(cx, cy, *polar(cx, cy, 18, 0), stroke="#23262B", stroke_width=3, stroke_linecap="round")
    hx, hy = 150, 162
    for a in (20, 140, 260):
        x, y = polar(hx, hy, 17, a)
        ic.line(hx, hy, x, y, stroke=STEEL[0], stroke_width=5.5, stroke_linecap="round")
        ic.circle(x, y, 5, fill="#D2D7DC")
    ic.circle(hx, hy, 8, fill=two(ic, *BRASS))
    ic.rect(68, 164, 54, 18, rx=4, fill=two(ic, *BRASS))
    bar(ic, 76, 170, 38, 6, fill="#4A3410")


# --- Pika Backup -------------------------------------------------------------

def _drive(ic, x, y, w, h, used):
    ic.rect(x, y, w, h, rx=9, fill=two(ic, "#4A5058", "#24272C"))
    ic.rect(x + 8, y + 7, w - 16, h - 14, rx=5, fill="#16181B")
    bar(ic, x + 15, y + h / 2 - 3, 40, 6, fill="#AEB6BF")
    ic.rect(x + w - 58, y + h / 2 - 3.5, 32, 7, rx=3.5, fill="#2E3238")
    ic.rect(x + w - 58, y + h / 2 - 3.5, 32 * used, 7, rx=3.5, fill="#F5A447")
    ic.circle(x + w - 16, y + h / 2, 3.5, fill="#5CC8FF")


@soft("pika-backup")
def pika_backup(ic):
    tile(ic, "#4A84B8", "#1B3B60")
    soft_shadow(ic, 128, 214, 98, 12)
    _drive(ic, 36, 172, 184, 34, 0.8)
    _drive(ic, 44, 140, 172, 32, 0.55)
    _drive(ic, 40, 108, 178, 32, 0.3)
    with ic.g(transform="translate(124 106) scale(1.12) translate(-124 -106)"):
        fur = two(ic, "#DDA46A", "#B0703A")
        for x, y in ((104, 52), (138, 46)):
            ic.circle(x, y, 13, fill="#B0703A")
            ic.circle(x, y + 1, 7, fill="#E8A49A")
        ic.path("M76 104C70 74 92 52 124 52C156 52 178 74 172 104Z", fill=fur)
        ic.path("M92 104C92 86 104 76 120 76C136 76 148 86 148 104Z", fill="#F4DCB8")
        for x in (110, 140):
            ic.ellipse(x, 103, 9, 4, fill="#C88850")
        for x in (108, 132):
            ic.circle(x, 72, 5, fill="#1E120A")
        ic.ellipse(120, 82, 4, 3, fill="#4A2A18")
        ic.circle(99, 83, 4.5, fill="#F09A8A", opacity=0.5)
        ic.circle(141, 83, 4.5, fill="#F09A8A", opacity=0.5)


# --- Vorta -------------------------------------------------------------------

def _cartridge(ic, x, y, w, h, shell, edge):
    c = 20
    d = (f"M{x + 9} {y}H{x + w - c}L{x + w} {y + c}V{y + h - 9}a9 9 0 0 1-9 9H{x + 9}a9 9 0 0 1-9-9V{y + 9}"
         f"a9 9 0 0 1 9-9z")
    ic.path(d, fill=edge, transform="translate(4 12)")
    ic.path(d, fill=shell)


@soft("vorta")
def vorta(ic):
    tile(ic, "#2F4C80", "#101C38")
    soft_shadow(ic, 124, 216, 100, 11)
    with ic.g(transform="rotate(9 170 110)"):
        _cartridge(ic, 104, 34, 118, 124, two(ic, "#7C8DA6", "#52617A"), "#2A3446")
        ic.rect(122, 38, 74, 20, rx=4, fill="#FBF4E2")
        ic.path("M122 42a4 4 0 0 1 4-4h66a4 4 0 0 1 4 4v3h-74z", fill="#2F5DB8")
    with ic.g(transform="translate(0 -12)"):
        _cartridge(ic, 36, 70, 154, 136, two(ic, "#93A2B8", "#56667E"), "#262F3F")
        lx, ly = 58, 82
        ic.rect(lx, ly, 108, 56, rx=5, fill="#FFFFFF")
        ic.path(f"M{lx} {ly + 5}a5 5 0 0 1 5-5h98a5 5 0 0 1 5 5v13h-108z", fill="#2C5EC0")
        ic.path(f"M{lx + 8} {ly + 4}L{lx + 13} {ly + 13}L{lx + 18} {ly + 4}", fill="none", stroke="#F2F5F8",
                stroke_width=3, stroke_linecap="round", stroke_linejoin="round")
        bar(ic, lx + 24, ly + 6, 40, 6, fill="#F2F5F8")
        bar(ic, lx + 8, ly + 25, 62, 7, fill="#2A3446")
        bar(ic, lx + 8, ly + 38, 44, 7, fill="#8A93A0")
        wx, wy = 72, 166
        ic.rect(wx - 22, wy - 18, 44, 32, rx=8, fill="#1B222E")
        win = ic.clip(f'<rect x="{wx - 19}" y="{wy - 15}" width="38" height="26" rx="6"/>')
        with ic.g(clip_path=win):
            ic.rect(wx - 20, wy - 16, 40, 28, fill="#0E131B")
            ic.circle(wx + 6, wy + 10, 28, fill="#6E4A2C")
            ic.circle(wx + 6, wy + 10, 10, fill="#C9D0D8")
        ic.rect(150, 160, 30, 16, rx=5, fill="#1B222E")
        ic.rect(164, 162, 14, 12, rx=3, fill="#E0563A")
