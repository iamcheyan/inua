"""Soft drawings of the talk and mail apps (drawings/apps_t2_talk.py): the
same objects with about half the detail, no text."""

from lib import bar, polar, soft, soft_shadow, tile, two

BRASS = ("#E2B45E", "#B88433")
STEEL = ("#AEB4BB", "#8D949C")
GRAPHITE = ("#3F4349", "#2A2C31")


def _brass(ic):
    return two(ic, *BRASS)


def _steel(ic):
    return two(ic, *STEEL)


# --- WhatsApp: a green rotary telephone -------------------------------------

def _wa_handset(ic, cx, cy, r, fg):
    k = r / 10
    d = ("M-4.4 -5.6c-1.2 .2-2.2 1.6-1.8 3.4c.8 3.8 4.4 7.6 8.4 8.6c1.8 .4 3.2-.6 3.4-1.8"
         "l.2-1.2-3-1.6-1.6 1.4c-2-.8-3.6-2.4-4.4-4.4l1.4-1.6-1.6-3z")
    ic.path(d, fill=fg, transform=f"translate({cx:.2f} {cy:.2f}) scale({k:.3f})")


def _wa_bubble(ic, cx, cy, r, fg):
    t0x, t0y = polar(cx, cy, r, 222)
    t1x, t1y = polar(cx, cy, r, 198)
    ic.path(f"M{t0x:.1f} {t0y:.1f}A{r} {r} 0 1 1 {t1x:.1f} {t1y:.1f}L{cx - r * 1.12:.1f} {cy + r * 1.12:.1f}z",
            fill="none", stroke=fg, stroke_width=r * 0.2, stroke_linejoin="round")
    _wa_handset(ic, cx, cy, r * 0.66, fg)


@soft("whatsapp")
def whatsapp(ic):
    tile(ic, "#1D6F58", "#0A3A2E")
    soft_shadow(ic, 128, 214, 100, 12)
    green = two(ic, "#45D67F", "#169650")
    ic.path("M40 208a8 8 0 0 1-7-10l22-80a14 14 0 0 1 13-10h120a14 14 0 0 1 13 10l22 80a8 8 0 0 1-7 10z",
            fill="#0B5A2E")
    ic.path("M44 200a8 8 0 0 1-7-10l20-72a14 14 0 0 1 13-10h116a14 14 0 0 1 13 10l20 72a8 8 0 0 1-7 10z",
            fill=green)
    cx, cy = 128, 156
    ic.circle(cx, cy, 44, fill=two(ic, "#F6FBF7", "#D4E2D8"))
    for i in range(10):
        x, y = polar(cx, cy, 31, -150 + i * 27)
        ic.circle(x, y, 6.6, fill="#0E4E2B")
    ic.circle(cx, cy, 20, fill="#25C463")
    _wa_bubble(ic, cx + 0.6, cy - 0.4, 11.5, "#fff")
    hs = "M48 92c0-14 12-22 26-24 36-6 72-6 108 0 14 2 26 10 26 24 0 6-4 10-10 10-8 0-12-6-14-10" \
         "-34-6-78-6-112 0-2 4-6 10-14 10-6 0-10-4-10-10z"
    ic.path(hs, fill="#0B5A2E", transform="translate(0 6)")
    ic.path(hs, fill=green)
    for x in (92, 164):
        ic.rect(x - 8, 104, 16, 10, rx=4, fill="#0E6A36")


# --- Microsoft Teams: a conference speakerphone -----------------------------

def _teams_mark(ic, cx, cy, s):
    """Teams' mark, simply: a person behind a tile with a T."""
    k = s / 40
    ic.circle(cx + 6 * k, cy - 26 * k, 12 * k, fill="#7B83EB")
    ic.path(f"M{cx - 10 * k:.1f} {cy - 12 * k:.1f}h{40 * k:.1f}v{26 * k:.1f}a{18 * k:.1f} {18 * k:.1f} 0 0 1"
            f"-{36 * k:.1f} 0z", fill="#7B83EB")
    ic.rect(cx - 24 * k, cy - 20 * k, s, s, rx=7 * k, fill=two(ic, "#6A70DC", "#3F45B0"))
    ic.rect(cx - 15 * k, cy - 11 * k, 22 * k, 6 * k, rx=1.5 * k, fill="#fff")
    ic.rect(cx - 7 * k, cy - 11 * k, 6 * k, 24 * k, rx=1.5 * k, fill="#fff")


@soft("teams")
def teams(ic):
    tile(ic, "#5B5FC7", "#2A2C7A")
    soft_shadow(ic, 128, 196, 108, 16)
    cx, cy = 128, 128
    ic.path(f"M{cx - 104} {cy}v22a104 52 0 0 0 208 0v-22z", fill="#1C1E22")
    ic.ellipse(cx, cy, 104, 52, fill=two(ic, "#474B54", "#2A2C32"))
    ic.ellipse(cx, cy, 62, 31, fill="none", stroke="#B9BDFF", stroke_width=6)
    ic.ellipse(cx, cy, 48, 24, fill=two(ic, "#E9EAF2", "#C2C4D2"))
    with ic.g(transform=f"translate({cx} {cy}) scale(1 0.5) translate({-cx} {-cy})"):
        _teams_mark(ic, cx - 2, cy + 4, 40)
    for x, col in ((86, "#3A3D45"), (128, "#C4314B"), (170, "#3A3D45")):
        y = cy + 40 - abs(x - cx) * 0.12
        ic.ellipse(x, y, 12, 5, fill=col)


# --- Skype: a headset, Skype's mark on its ear cup --------------------------

def _skype_mark(ic, cx, cy, r):
    blue = two(ic, "#36C5FA", "#0A8FD6")
    ic.circle(cx - r * 0.42, cy - r * 0.42, r * 0.56, fill=blue)
    ic.circle(cx + r * 0.42, cy + r * 0.42, r * 0.56, fill=blue)
    ic.circle(cx, cy, r * 0.82, fill=blue)
    # the S as one bold stroke
    k = r / 20
    d = (f"M{cx + 8 * k:.1f} {cy - 8 * k:.1f}C{cx + 4 * k:.1f} {cy - 12 * k:.1f} {cx - 9 * k:.1f} {cy - 11 * k:.1f} "
         f"{cx - 8 * k:.1f} {cy - 4 * k:.1f}C{cx - 7 * k:.1f} {cy + 1 * k:.1f} {cx + 8 * k:.1f} {cy - 1 * k:.1f} "
         f"{cx + 8 * k:.1f} {cy + 5 * k:.1f}C{cx + 8 * k:.1f} {cy + 12 * k:.1f} {cx - 5 * k:.1f} {cy + 12 * k:.1f} "
         f"{cx - 9 * k:.1f} {cy + 7 * k:.1f}")
    ic.path(d, fill="none", stroke="#fff", stroke_width=4.6 * k, stroke_linecap="round")


@soft("skype")
def skype(ic):
    tile(ic, "#1E86C8", "#0B4775")
    soft_shadow(ic, 128, 214, 98, 12)
    ic.path("M54 140V116a74 74 0 0 1 148 0v24", fill="none", stroke=_steel(ic), stroke_width=8)
    ic.path("M62 104a68 68 0 0 1 132 0", fill="none", stroke="#2E3136", stroke_width=20, stroke_linecap="round")
    ic.path("M196 186c-8 18-36 24-62 20", fill="none", stroke="#2E3136", stroke_width=6, stroke_linecap="round")
    ic.ellipse(126, 204, 14, 11, fill="#1A1B1E")
    for x in (56, 200):
        ic.rect(x - 4, 110, 8, 16, rx=4, fill=_steel(ic))
        ic.rect(x - 30, 120, 60, 84, rx=30, fill=two(ic, *GRAPHITE))
        ic.rect(x - 22, 128, 44, 68, rx=22, fill=two(ic, "#2C2E33", "#1A1B1E"))
    _skype_mark(ic, 56, 162, 22)
    ic.circle(200, 162, 5, fill="#36C5FA")


# --- Evolution: a rotary card file -------------------------------------------

@soft("evolution")
def evolution(ic):
    tile(ic, "#6C7A84", "#323C44")
    soft_shadow(ic, 128, 214, 100, 12)
    ax, ay = 128, 168
    ic.path("M60 214l14-34h108l14 34z", fill=two(ic, "#3A3D42", "#1E1F23"))
    for a, tab in ((-24, 74), (18, 150), (-12, 96), (9, 120)):
        with ic.g(transform=f"rotate({a} {ax} {ay})"):
            ic.rect(tab, 54, 30, 12, rx=4, fill="#CF372D" if tab in (96, 120) else "#B9C2C7")
            ic.rect(62, 64, 132, 96, rx=7, fill=two(ic, "#EDE6D8", "#CFC6B4"))
    ic.rect(62, 64, 132, 96, rx=7, fill=two(ic, "#FCF9F2", "#ECE5D6"))
    ic.path("M140 66v-10a5 5 0 0 1 5-5h26a5 5 0 0 1 5 5v10z", fill="#DC4236")
    bar(ic, 74, 76, 70, 9, fill="#2C3338")
    bar(ic, 74, 94, 96, fill="#8E9AA4")
    bar(ic, 74, 108, 80, fill="#8E9AA4")
    bar(ic, 74, 128, 64, fill="#5B7AA6")
    for x, s in ((44, 1), (212, -1)):
        ic.rect(min(x, x + 16 * s), ay - 4, 16, 8, fill=_steel(ic))
        ic.ellipse(x, ay, 14, 40, fill=two(ic, "#D2D7DD", "#7E858E"))
        ic.ellipse(x, ay, 8, 30, fill="#9EA5AE")


# --- Geary: a letterbox on its post, the flag up --------------------------------

@soft("geary")
def geary(ic):
    tile(ic, "#7A4E6A", "#3C2032")
    soft_shadow(ic, 134, 216, 76, 10)
    ic.rect(122, 150, 26, 66, fill=two(ic, "#A8774A", "#6E4622"))
    ic.rect(100, 150, 70, 12, rx=4, fill="#6E4622")
    ic.path("M58 64h130a36 36 0 0 1 36 36v54H58z", fill=two(ic, "#FCD460", "#E0A020"))
    with ic.g(transform="rotate(-18 76 70)"):
        ic.rect(60, 40, 52, 34, rx=4, fill="#FFFFFF")
        ic.path("M62 42l24 13 24-13", fill="none", stroke="#C9BFA9", stroke_width=2.5, stroke_linecap="round",
                stroke_linejoin="round")
    ic.path("M34 156V102c0-22 11-40 24-40s24 18 24 40v54z", fill=two(ic, "#F8C84A", "#C88A14"))
    ic.rect(50, 104, 16, 8, rx=4, fill=_steel(ic))
    bar(ic, 118, 112, 68, 12, fill="#8A5A72", opacity=0.75)
    bar(ic, 134, 132, 36, 7, fill="#8A5A72", opacity=0.5)
    ic.rect(204, 46, 11, 74, rx=4, fill="#C83A2C")
    ic.rect(204, 34, 30, 22, rx=5, fill=two(ic, "#F25B4B", "#C42F22"))


# --- Fractal: a walkie-talkie, a Sierpinski triangle on it ------------------

def _sierpinski(ic, x, y, s, depth, **kw):
    if depth == 0:
        ic.poly([(x, y + s), (x + s / 2, y), (x + s, y + s)], **kw)
        return
    h = s / 2
    _sierpinski(ic, x + h / 2, y, h, depth - 1, **kw)
    _sierpinski(ic, x, y + h, h, depth - 1, **kw)
    _sierpinski(ic, x + h, y + h, h, depth - 1, **kw)


@soft("fractal")
def fractal(ic):
    tile(ic, "#3F6FB2", "#1A3866")
    soft_shadow(ic, 128, 218, 66, 10)
    ic.rect(88, 18, 14, 54, rx=7, fill="#16171A")
    ic.rect(150, 46, 18, 22, rx=5, fill=_steel(ic))
    ic.rect(124, 54, 16, 14, rx=4, fill="#E0483A")
    ic.rect(64, 104, 12, 40, rx=5, fill="#2A2C31")
    ic.rect(72, 66, 112, 152, rx=24, fill=two(ic, "#5089D2", "#2A5596"))
    ic.rect(84, 78, 88, 40, rx=8, fill="#12233C")
    ic.rect(89, 83, 78, 30, rx=5, fill=two(ic, "#BFE3D6", "#98CAB8"))
    bar(ic, 96, 90, 34, 8, fill="#1C3A33")
    bar(ic, 96, 102, 48, 5, fill="#1C3A33", opacity=0.6)
    for k in range(3):
        ic.rect(150 + k * 5, 98 - k * 4, 3.5, 6 + k * 4, rx=1, fill="#1C3A33")
    for y in range(128, 164, 9):
        bar(ic, 86, y, 84, 5, fill="#183256")
    ic.rect(94, 170, 68, 42, rx=8, fill=two(ic, "#F4F7FB", "#DCE4EE"))
    _sierpinski(ic, 110, 174, 36, 2, fill="#3B6CB5")
    ic.circle(166, 72, 3, fill="#7CF7A6")


# --- Dino: a tin wind-up dinosaur ---------------------------------------------

@soft("dino")
def dino(ic):
    tile(ic, "#2D5560", "#13282F")
    soft_shadow(ic, 124, 210, 92, 11)
    tin = two(ic, "#A8DC7C", "#5E9E36")
    leg = two(ic, "#90CC62", "#4A8A2A")
    dark = "#3E7A22"
    with ic.g(transform="translate(-6 10) scale(0.92) translate(11 -8)"):
        for x in (92, 164):
            ic.path(f"M{x - 4} 160c-2 14-4 30-4 42h18c2-12 4-28 4-40z", fill="#35661C")
        for i, (x, y) in enumerate(((96, 128), (116, 120), (138, 118), (160, 120))):
            ic.path(f"M{x - 11} {y + 6}L{x} {y - 13}L{x + 11} {y + 6}z", fill="#EBA83F", stroke="#EBA83F",
                    stroke_width=4, stroke_linejoin="round")
        d = ("M30 176c18 0 36-6 50-22 8-20 30-34 58-34 22 0 38 8 46-6 6-12 2-30 6-48 4-16 18-24 32-20 "
             "12 3 18 14 14 24-4 8-14 10-20 10-6 0-8 6-8 14 0 22-2 44-12 62-10 18-30 26-54 26h-60"
             "c-18 0-36 6-52 6-6 0-6-12 0-12z")
        ic.path(d, fill=tin)
        for x in (74, 146):
            ic.path(f"M{x - 6} 160c0-10 30-10 30 0 0 16-2 30-4 42h-22c-2-12-4-26-4-42z", fill=leg)
            ic.path(f"M{x - 10} 211a5 5 0 0 1 0-10h30a5 5 0 0 1 0 10z", fill="#2E5A18")
        ic.circle(208, 62, 6, fill="#fff")
        ic.circle(209.5, 62, 3.2, fill="#1A1B1E")
        ic.path("M216 76c-6 3-12 3-17 0", fill="none", stroke=dark, stroke_width=3, stroke_linecap="round")
        ic.path("M100 138h48a10 10 0 0 1 10 10v12a10 10 0 0 1-10 10h-30l-10 8 2-8h-10a10 10 0 0 1-10-10v-12"
                "a10 10 0 0 1 10-10z", fill="#F4F4F2")
        for x in (114, 124, 134):
            ic.circle(x, 154, 3.4, fill="#048C7F")
        ic.rect(54, 147, 24, 8, rx=3, fill=_brass(ic))
        ic.path("M50 132c-9 0-11 9-6 14l6 6 6-6c5-5 3-14-6-14zM50 172c-9 0-11-9-6-14l6-6 6 6c5 5 3 14-6 14z",
                fill=_brass(ic))
        ic.circle(50, 152, 5, fill="#B88433")


# --- Pidgin: a carrier pigeon on its perch -----------------------------------

@soft("pidgin")
def pidgin(ic):
    tile(ic, "#7A5A9E", "#3A2552")
    soft_shadow(ic, 128, 208, 92, 11)
    ic.rect(24, 184, 208, 16, rx=8, fill=two(ic, "#C48A55", "#8A5A2E"))
    ic.path("M74 134L22 168c-6 4-4 14 2 16l72-8z", fill="#5D3E80")
    ic.path("M34 160L22 168c-6 4-4 14 2 16l16-2z", fill="#2E1C42")
    ic.path("M64 148c6-40 40-60 80-60 18 0 30 4 40 12 14 12 16 34 8 52-10 20-32 30-60 30-30 0-56-10-68-34z",
            fill=two(ic, "#BCA0DE", "#7A58A2"))
    ic.path("M146 92c16 0 32 10 36 26-10 8-26 6-38-2-4-10-4-18 2-24z", fill="#7BC9B0", opacity=0.85)
    ic.path("M74 142c10-28 40-40 72-34 18 4 26 18 20 34-8 20-38 26-62 22-14-2-26-10-30-22z",
            fill=two(ic, "#A88ACE", "#6E4E96"))
    ic.path("M108 122c14-6 28-4 40 4-12-2-26-2-40 2z", fill="#3A2552", stroke="#3A2552", stroke_width=3,
            stroke_linejoin="round")
    ic.path("M100 136c18-6 36-4 52 4-16-2-34-2-52 2z", fill="#3A2552", stroke="#3A2552", stroke_width=3,
            stroke_linejoin="round")
    ic.circle(168, 78, 25, fill=two(ic, "#B898DC", "#7E5EA6"))
    ic.path("M187 72l24 9-24 7z", fill="#F38C25", stroke="#F38C25", stroke_width=3, stroke_linejoin="round")
    ic.circle(176, 74, 6, fill="#F38C25")
    ic.circle(176, 74, 3.4, fill="#1A1B1E")
    for x in (118, 146):
        ic.path(f"M{x} 176v10", stroke="#E07A2A", stroke_width=6, stroke_linecap="round")
    ic.rect(140, 169, 28, 13, rx=6.5, fill=_brass(ic))
    ic.rect(166, 170.5, 12, 10, rx=2, fill="#FCF9F2")


# --- HexChat: a telegraph key, a hexagonal knob ------------------------------

@soft("hexchat")
def hexchat(ic):
    tile(ic, "#3E4858", "#1A1F28")
    soft_shadow(ic, 128, 214, 106, 12)
    ic.path("M196 136c24-2 22-34 44-40", fill="none", stroke="#C8372D", stroke_width=5, stroke_linecap="round")
    ic.path("M204 140c22 0 30-22 36-24", fill="none", stroke="#1A1B1E", stroke_width=5, stroke_linecap="round")
    ic.path("M28 174l20-50h160l20 50z", fill=two(ic, "#A86E40", "#7A4A24"), stroke="#A06A3C", stroke_width=8,
            stroke_linejoin="round")
    ic.path("M22 174h212v24a10 10 0 0 1-10 10H32a10 10 0 0 1-10-10z", fill=two(ic, "#6E4320", "#45260E"))
    ic.rect(94, 180, 68, 18, rx=5, fill=_brass(ic))
    bar(ic, 106, 186, 44, 6, fill="#6A4A16")
    ic.rect(144, 128, 9, 28, rx=3, fill=_brass(ic))
    ic.rect(160, 128, 9, 28, rx=3, fill=_brass(ic))
    ic.rect(189, 120, 14, 30, rx=3, fill=_brass(ic))
    ic.rect(68, 144, 16, 16, rx=3, fill=_brass(ic))
    ic.path("M62 132L204 124v10L62 143z", fill="#B88433", stroke="#C99645", stroke_width=3, stroke_linejoin="round")
    ic.circle(156, 131, 5.5, fill=_steel(ic))
    ic.rect(68, 110, 10, 26, rx=3, fill=_brass(ic))
    pts = [polar(73, 92, 30, a) for a in range(30, 390, 60)]
    ic.poly(pts, fill=two(ic, "#FFCB4A", "#D99A12"), stroke="#E8AE2A", stroke_width=6, stroke_linejoin="round")
    # the # as four bold strokes
    for dx in (-5, 5):
        ic.line(73 + dx + 2, 80, 73 + dx - 2, 104, stroke="#5A3A06", stroke_width=4.4, stroke_linecap="round")
    for dy in (-5, 5):
        ic.line(62, 92 + dy, 84, 92 + dy, stroke="#5A3A06", stroke_width=4.4, stroke_linecap="round")


# --- Ferdium: a telephone switchboard, patch cords plugged in -----------------

@soft("ferdium")
def ferdium(ic):
    tile(ic, "#6A5CD6", "#2E2478")
    soft_shadow(ic, 128, 214, 102, 12)
    ic.rect(32, 36, 192, 174, rx=14, fill=two(ic, "#B07A48", "#7A4A24"))
    ic.rect(88, 43, 80, 17, rx=5, fill=_brass(ic))
    bar(ic, 102, 48, 52, 7, fill="#6A4A16")
    ic.rect(44, 66, 168, 90, rx=7, fill=two(ic, "#2B2440", "#181326"))
    cols = [64 + i * 32 for i in range(5)]
    lit = {(1, 0): "#8471F2", (3, 1): "#F2C45C", (0, 2): "#7CF7A6"}
    for r, y in enumerate((80, 110, 140)):
        for c, x in enumerate(cols):
            col = lit.get((c, r))
            if col:
                ic.circle(x, y - 8, 3.8, fill=col)
            ic.circle(x, y + 4, 7, fill=_brass(ic))
            ic.circle(x, y + 4, 3.4, fill="#0C0A12")
    ic.rect(32, 160, 192, 24, fill=two(ic, "#8E5E32", "#6A4222"))
    cords = (("#8471F2", 66, 96, 114), ("#E0483A", 104, 128, 84), ("#F2C45C", 150, 160, 144),
             ("#4F9BE8", 190, 192, 114))
    for col, sx, jx, jy in cords:
        ic.path(f"M{sx} 168C{sx} 196 {jx} 196 {jx} {jy + 10}", fill="none", stroke=col, stroke_width=5,
                stroke_linecap="round")
        ic.rect(jx - 4, jy + 2, 8, 10, rx=2, fill=_steel(ic))
        ic.rect(sx - 5, 163, 10, 13, rx=3, fill="#1A1B1E")


# --- Mattermost: a ship's bell on its bracket ------------------------------------

@soft("mattermost-desktop")
def mattermost(ic):
    tile(ic, "#2A4378", "#101E3C")
    cx = 128
    soft_shadow(ic, 128, 218, 80, 10)
    ic.rect(30, 22, 16, 58, rx=6, fill=_brass(ic))
    ic.path("M46 70C60 70 70 52 96 40", fill="none", stroke="#C99645", stroke_width=7, stroke_linecap="round")
    ic.rect(44, 29, 116, 11, rx=5.5, fill=_brass(ic))
    ic.circle(160, 34.5, 7, fill=_brass(ic))
    ic.circle(cx, 40, 9, fill="none", stroke="#B88433", stroke_width=5)
    ic.rect(cx - 11, 44, 22, 14, rx=4, fill="#A87A30")
    ic.line(cx, 180, cx, 200, stroke="#8A6425", stroke_width=5)
    ic.circle(cx, 204, 9, fill=_brass(ic))
    bell = ("M98 72C98 60 110 55 128 55S158 60 158 72L164 136C166 160 178 170 198 176C206 179 206 192 196 192"
            "H60C50 192 50 179 58 176C78 170 90 160 92 136Z")
    ic.path(bell, fill=two(ic, "#EAC06A", "#B0802E"))
    ic.path("M60 180Q128 188 196 180", fill="none", stroke="#8A6425", stroke_width=3.5, stroke_linecap="round")
    bar(ic, 100, 160, 56, 7, fill="#8A6425", opacity=0.7)
    ic.rect(101, 82, 54, 56, rx=10, fill="#C99645")
    ic.rect(104, 85, 48, 50, rx=8, fill=two(ic, "#2E5296", "#1A3068"))
    mx, my = cx, 110
    a, b = polar(mx, my, 15, 55), polar(mx, my, 15, 20)
    ic.path(f"M{a[0]:.1f} {a[1]:.1f}A15 15 0 1 1 {b[0]:.1f} {b[1]:.1f}", fill="none", stroke="#E3F6FD",
            stroke_width=6, stroke_linecap="round")
    p1, p2, p3 = polar(mx, my, 17, 37), polar(mx, my, 7, 230), polar(mx, my, 1, 180)
    ic.path(f"M{p1[0]:.1f} {p1[1]:.1f}L{p2[0]:.1f} {p2[1]:.1f}A4.5 4.5 0 0 1 {p3[0]:.1f} {p3[1]:.1f}Z",
            fill="#E3F6FD")


# --- Rocket.Chat: a tin rocket ------------------------------------------------------

@soft("rocketchat-desktop")
def rocketchat(ic):
    tile(ic, "#2C3352", "#121528")
    soft_shadow(ic, 128, 220, 62, 9)
    red = two(ic, "#F65A6E", "#C42840")
    ic.path("M106 190c0 22 22 38 22 38s22-16 22-38z", fill="#F28A3C")
    ic.path("M116 190c0 15 12 26 12 26s12-11 12-26z", fill="#F8D06A")
    ic.path("M92 140L52 186l4 12 40-14z", fill=red, stroke="#E04058", stroke_width=4, stroke_linejoin="round")
    ic.path("M164 140L204 186l-4 12-40-14z", fill=red, stroke="#E04058", stroke_width=4, stroke_linejoin="round")
    body = "M128 20C96 44 86 90 90 140c2 24 6 40 10 52h56c4-12 8-28 10-52 4-50-6-96-38-120z"
    ic.path(body, fill=two(ic, "#FFFFFF", "#DCD9E4"))
    clip = ic.clip(f'<path d="{body}"/>')
    with ic.g(clip_path=clip):
        ic.rect(60, 0, 140, 58, fill="#F0485E")
        ic.rect(60, 150, 140, 60, fill="#E03C52")
    ic.circle(128, 100, 23, fill=_steel(ic))
    ic.circle(128, 100, 16, fill=two(ic, "#4E5E8E", "#1E2640"))
    ic.path("M128 150c-8 0-10 4-10 10v44h20v-44c0-6-2-10-10-10z", fill="#B02036")
    ic.path("M119 176c0-5.5 3.5-9 9-9s9 3.5 9 9-3.5 9-9 9h-3l-5 4v-5c-1-2-1-4-1-8z", fill="#fff")


# --- Proton Mail: a safe with a letter slot ------------------------------------------

@soft("proton-mail")
def protonmail(ic):
    tile(ic, "#5B3FD6", "#261670")
    soft_shadow(ic, 128, 214, 98, 12)
    ic.rect(40, 54, 176, 156, rx=16, fill=two(ic, "#7E5EFF", "#4A2BC8"))
    ic.rect(80, 64, 96, 11, rx=5.5, fill="#1A1040")
    with ic.g(transform="rotate(-4 128 60)"):
        ic.rect(86, 26, 84, 44, rx=4, fill="#FFFFFF")
        ic.path("M89 30l39 20 39-20", fill="none", stroke="#C9C2E0", stroke_width=2.5, stroke_linecap="round",
                stroke_linejoin="round")
    ic.rect(80, 69, 96, 6, fill="#1A1040")
    ic.rect(56, 86, 146, 110, rx=10, fill=two(ic, "#6E4EFA", "#4E30D2"))
    for y in (98, 184):
        ic.rect(46, y - 9, 13, 20, rx=4, fill=_steel(ic))
    cx, cy = 106, 140
    ic.circle(cx, cy, 30, fill=_steel(ic))
    ic.circle(cx, cy, 23, fill=two(ic, "#3A3E44", "#202226"))
    for k in range(8):
        x1, y1 = polar(cx, cy, 21, k * 45)
        x2, y2 = polar(cx, cy, 16, k * 45)
        ic.line(x1, y1, x2, y2, stroke="#E9E4FF", stroke_width=2.2, stroke_linecap="round")
    ic.circle(cx, cy, 10, fill=_steel(ic))
    ic.rect(150, 112, 13, 56, rx=6.5, fill=_steel(ic))
    ic.circle(156.5, 140, 10, fill=two(ic, "#C2C8CF", "#8D949C"))
    ic.rect(140, 176, 50, 14, rx=5, fill="#E9E4FF")
    bar(ic, 148, 180, 34, 6, fill="#5B3FD6")


# --- Mailspring: a spring balance weighing a bundle of letters -----------------------

@soft("mailspring")
def mailspring(ic):
    tile(ic, "#1F7F8A", "#0B3F46")
    soft_shadow(ic, 128, 222, 64, 8)
    cx = 128
    ic.circle(cx, 24, 10, fill="none", stroke="#C99645", stroke_width=6)
    ic.rect(cx - 27, 32, 54, 120, rx=14, fill=_brass(ic))
    ic.rect(cx - 16, 44, 32, 98, rx=7, fill="#0E2A2E")
    for k in range(6):
        y = 52 + k * 10
        ic.path(f"M{cx - 11} {y}q11 7 22 0", fill="none", stroke="#46D8DA", stroke_width=3.2, stroke_linecap="round")
    ic.rect(cx - 15, 116, 30, 5, rx=2.5, fill="#E0483A")
    ic.path(f"M{cx} 152v12a8 8 0 1 1-8 8", fill="none", stroke="#9EA5AE", stroke_width=5, stroke_linecap="round")
    with ic.g(transform=f"rotate(-3 {cx} 190)"):
        ic.rect(cx - 56, 185, 124, 38, rx=6, fill="#E4DCCB")
        ic.rect(cx - 62, 176, 124, 38, rx=6, fill=two(ic, "#FFFFFF", "#F0EBE0"))
        ic.path(f"M{cx - 58} 181l58 17 58-17", fill="none", stroke="#D0C8B6", stroke_width=2.5,
                stroke_linecap="round", stroke_linejoin="round")
        ic.rect(cx - 2.5, 176, 5, 38, fill="#46D8DA")
        ic.rect(cx - 62, 192.5, 124, 5, fill="#46D8DA")
        ic.rect(cx + 34, 181, 22, 26, rx=3, fill="#35D5D7")
        ic.path(f"M{cx + 38} 188l7 9 7-9-7 3z", fill="#fff")


# --- Betterbird: a birdhouse, a letter through its door ------------------------------

@soft("betterbird")
def betterbird(ic):
    tile(ic, "#2F5F9E", "#122E58")
    soft_shadow(ic, 128, 218, 58, 8)
    ic.rect(119, 170, 18, 50, fill=two(ic, "#8E6238", "#5E3A1C"))
    ic.path("M56 104L128 50 200 104V180a8 8 0 0 1-8 8H64a8 8 0 0 1-8-8z", fill=two(ic, "#F7F2E7", "#DDD3BE"))
    ic.path("M36 112L128 38v18L46 120z", fill=two(ic, "#F6C34E", "#DA9420"), stroke="#E8AC34", stroke_width=4,
            stroke_linejoin="round")
    ic.path("M220 112L128 38v18l82 64z", fill=two(ic, "#EF4334", "#B82A1E"), stroke="#D8382A", stroke_width=4,
            stroke_linejoin="round")
    ic.circle(128, 124, 22, fill="#2A1C10")
    with ic.g(transform="rotate(-12 128 128)"):
        ic.rect(100, 120, 56, 30, rx=4, fill="#FFFFFF")
        ic.path("M103 123l25 13 25-13", fill="none", stroke="#C9BFA9", stroke_width=2.5, stroke_linecap="round",
                stroke_linejoin="round")
    ic.ellipse(128, 166, 8, 6, fill="#8E5E32")
    ic.path("M114 82c4-6 12-8 18-4l6-4-2 6c2 4 0 10-6 12-6 2-12 0-16-6l-6 0z", fill="#EF4334",
            stroke="#EF4334", stroke_width=2, stroke_linejoin="round")
    ic.path("M122 84c4 4 10 4 14 0", fill="none", stroke="#EEB43F", stroke_width=3, stroke_linecap="round")


# --- Tuta: a postman's satchel, letters in it -------------------------------------------

@soft("tuta")
def tuta(ic):
    tile(ic, "#9A2234", "#4E0A16")
    soft_shadow(ic, 128, 214, 100, 12)
    ic.path("M48 120C40 30 216 30 208 120", fill="none", stroke="#A81C34", stroke_width=15)
    for x in (48, 208):
        ic.rect(x - 10, 104, 20, 15, rx=4, fill=_steel(ic))
    for i, (x, a) in enumerate(((64, -8), (98, 3), (140, -5))):
        with ic.g(transform=f"rotate({a} {x + 30} 120)"):
            ic.rect(x, 84, 60, 40, rx=4, fill=("#F2ECDF", "#FFFFFF", "#EAF0F8")[i])
            if i == 1:
                ic.rect(x + 41, 89, 13, 15, rx=2, fill="#D93951")
                bar(ic, x + 8, 94, 26, 5, fill="#B5AD9E")
    ic.rect(34, 108, 188, 104, rx=20, fill=two(ic, "#B8283E", "#7E1022"))
    flap = ("M30 112a10 10 0 0 1 10-10h176a10 10 0 0 1 10 10v26c0 14-12 24-26 24h-40c-10 0-14 6-16 14h-28"
            "c-2-8-6-14-16-14h-40c-14 0-26-10-26-24z")
    ic.path(flap, fill=two(ic, "#E8506A", "#B8263E"))
    bar(ic, 92, 126, 72, 14, fill="#FFF1F3")
    ic.rect(119, 166, 18, 38, rx=4, fill="#C42E46")
    ic.rect(110, 164, 36, 22, rx=6, fill="none", stroke=_steel(ic), stroke_width=5)
    ic.rect(126, 162, 4, 26, rx=2, fill="#AEB4BB")

