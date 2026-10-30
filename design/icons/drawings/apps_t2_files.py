"""The inua-objects theme, tier 2 "files" batch: Files (Nautilus), Dolphin,
Thunar, Nemo, Flatseal, Mission Center, Resources, System Monitor,
BleachBit, Disk Usage Analyzer, Backups (Deja Dup), Pika Backup and Vorta
(docs/feat/object-icons.md, Part 2). Each brand's mark is redrawn,
simplified, on an object of the app's job."""

import math

from lib import (brass, glare, graphite, icon, paper, polar, shadow, small, steel, text_path, tile, wood)


def rot(deg, cx, cy):
    return f"rotate({deg:g} {cx:g} {cy:g})"


def arc_text(ic, s, cx, cy, r, mid_deg, size, font="sans-semibold", spacing=0.0, inner=False, **kw):
    """A line of text along a circle, centred on mid_deg (0 up, clockwise);
    with inner=True it reads along the bottom, upright."""
    widths = [text_path(c, 0, 0, size, font)[1] for c in s]
    total = sum(widths) + spacing * (len(s) - 1)
    sign = -1 if inner else 1
    deg = mid_deg - sign * math.degrees(total / r) / 2
    for c, w in zip(s, widths):
        mid = deg + sign * math.degrees(w / 2 / r)
        x, y = polar(cx, cy, r, mid)
        if c != " ":
            ic.text(c, x, y, size, font=font, anchor="middle", transform=rot(mid + (180 if inner else 0), x, y), **kw)
        deg += sign * math.degrees((w + spacing) / r)


def sector(cx, cy, r_out, r_in, a1, a2):
    """An annular sector from angle a1 to a2 (clockwise, 0 up)."""
    large = 1 if (a2 - a1) % 360 > 180 else 0
    x1, y1 = polar(cx, cy, r_out, a1)
    x2, y2 = polar(cx, cy, r_out, a2)
    x3, y3 = polar(cx, cy, r_in, a2)
    x4, y4 = polar(cx, cy, r_in, a1)
    return (f"M{x1:.1f} {y1:.1f}A{r_out} {r_out} 0 {large} 1 {x2:.1f} {y2:.1f}"
            f"L{x3:.1f} {y3:.1f}A{r_in} {r_in} 0 {large} 0 {x4:.1f} {y4:.1f}Z")


def screw(ic, x, y, r=3.0, deg=30):
    ic.circle(x, y, r, fill=steel(ic, False))
    ic.circle(x, y, r, fill="none", stroke="#000", stroke_opacity=0.3, stroke_width=0.6)
    ic.line(*polar(x, y, r * 0.7, deg), *polar(x, y, r * 0.7, deg + 180), stroke="#3A3F45", stroke_width=0.9)


def rivet(ic, x, y, r=2.6, light="#E6EAEE", dark="#2A3038"):
    ic.circle(x + 0.6, y + 0.8, r, fill=dark, opacity=0.6)
    ic.circle(x, y, r, fill=ic.rad([(0, light), (1, "#7C8590")], cx=0.35, cy=0.3, r=0.8))


def bolt(x, y, s=1.0):
    """A lightning bolt, its top at x, y, about 30 s tall."""
    pts = [(6, 0), (16, 0), (11, 11), (18, 11), (4, 30), (8, 16), (1, 16)]
    return "M" + "L".join(f"{x + px * s:.1f} {y + py * s:.1f}" for px, py in pts) + "Z"


# --- Files (Nautilus): a steel filing cabinet, its top drawer pulled out ----

def label_holder(ic, x, y, w, h, word, size=11):
    ic.rect(x - 1.5, y - 1.5, w + 3, h + 3, rx=2, fill=steel(ic, False))
    ic.rect(x, y, w, h, rx=1, fill=paper(ic, "cream"))
    ic.text(word, x + w / 2, y + h - 3, size, font="hand", anchor="middle", fill="#24406A")
    ic.rect(x, y, w, 2, fill="#000", opacity=0.12)


def pull(ic, x, y, w):
    ic.rect(x + 1, y + 2, w, 7, rx=3.5, fill="#000", opacity=0.3)
    ic.rect(x, y, w, 7, rx=3.5, fill=steel(ic, False))
    ic.rect(x + 3, y + 1, w - 6, 1.4, rx=0.7, fill="#fff", opacity=0.7)


@icon("nautilus", kind="app", names=["nautilus"], title="Files (Nautilus)")
def nautilus(ic):
    tile(ic, "#4F86C6", "#1E3D68")
    shadow(ic, 128, 210, 90, 12)
    # the cabinet
    ic.rect(58, 32, 140, 176, rx=8, fill=ic.lin([(0, "#F4F6F9"), (1, "#B6BDC8")], 0, 0, 1, 1))
    ic.rect(58.75, 32.75, 138.5, 174.5, rx=7.25, fill="none", stroke="#fff", stroke_width=1.5, opacity=0.8)
    ic.rect(190, 36, 8, 168, rx=3, fill="#000", opacity=0.08)
    ic.rect(64, 202, 128, 8, rx=2, fill="#4C5560")
    # the opening of the top drawer, dark, and the drawer pulled out of it
    ic.rect(66, 40, 124, 80, rx=4, fill="#1E2630")
    ic.poly([(70, 46), (186, 46), (198, 98), (58, 98)], fill="#3A4552")
    ic.poly([(70, 46), (76, 46), (66, 98), (58, 98)], fill="#C9D0D9")
    ic.poly([(180, 46), (186, 46), (198, 98), (190, 98)], fill="#8C96A3")
    # hanging folders, back to front, the blue of the brand among kraft ones
    rows = [(56, "#C69447", 0), (68, "#3584E4", 2), (80, "#E3BA6C", 1)]
    for i, (y, col, slot) in enumerate(rows):
        f = (y - 46) / 52
        l, r = 70 - 12 * f + 3, 186 + 12 * f - 3
        ic.rect(l, y, r - l, 18, rx=2, fill=col)
        ic.rect(l, y, r - l, 1.6, fill="#fff", opacity=0.35)
        tx = l + 12 + slot * 36
        ic.rect(tx, y - 7, 30, 9, rx=2, fill=col)
        ic.rect(tx + 3, y - 5.5, 24, 5, rx=1, fill="#FFFDF7", opacity=0.9)
        ic.rect(l, y + 14, r - l, 4, fill="#000", opacity=0.18)
    # the drawer's front, in the brand's blue enamel
    ic.rect(56, 98, 144, 46, rx=5, fill="#123A72", transform="translate(0 3)")
    ic.rect(56, 98, 144, 46, rx=5, fill=ic.lin([(0, "#82B6F2"), (0.5, "#3584E4"), (1, "#1A5FB4")]))
    ic.rect(58, 99, 140, 2, rx=1, fill="#fff", opacity=0.55)
    label_holder(ic, 106, 105, 44, 15, "Home")
    pull(ic, 100, 128, 56)
    ic.rect(60, 147, 136, 6, fill="#000", opacity=0.25)
    # the lower drawer, shut
    ic.rect(66, 154, 124, 46, rx=4, fill=ic.lin([(0, "#E9EDF2"), (1, "#B9C1CB")]))
    ic.rect(66, 154, 124, 46, rx=4, fill="none", stroke="#6E7884", stroke_opacity=0.5)
    ic.line(68, 155.5, 188, 155.5, stroke="#fff", stroke_width=1.2, opacity=0.8)
    label_holder(ic, 108, 160, 40, 14, "Photos", 10)
    pull(ic, 102, 182, 52)


@small("nautilus")
def nautilus16(ic):
    tile(ic, "#4F86C6", "#1E3D68")
    ic.rect(3.5, 2, 9, 12, rx=0.8, fill="#E3E7EC")
    ic.rect(4.2, 2.6, 7.6, 4.4, fill="#26303A")
    ic.rect(4.6, 3.6, 3, 2, fill="#E3BA6C")
    ic.rect(8.2, 3.2, 3, 2.4, fill="#62A0EA")
    ic.rect(3, 5.6, 10, 3.4, rx=0.5, fill="#3584E4")
    ic.rect(6.5, 7.4, 3, 0.8, rx=0.4, fill="#E8EEF5")
    ic.rect(6.5, 11.6, 3, 0.8, rx=0.4, fill="#7E8894")


# --- Dolphin: a blue folder, a dolphin leaping out of it --------------------

DOLPHIN = ("M76 2C70 0 64-2 58-4C54-14 42-19 26-18C16-17 10-18 6-19C0-28-8-36-14-40C-14-32-16-24-20-16"
           "C-36-11-52-6-62-3C-68-8-76-14-86-17C-81-10-77-4-72 0C-77 4-81 10-86 17C-76 13-68 8-62 5"
           "C-46 10-22 16 0 15C2 22-2 30-8 35C0 31 8 24 14 15C32 13 50 9 60 6C66 5 72 4 76 2Z")


def dolphin_body(ic, scale=1.0, belly=True):
    ic.path(DOLPHIN, fill=ic.lin([(0, "#7CCBF5"), (0.45, "#2E9BE6"), (1, "#145C9E")], 0, 0, 0.3, 1))
    if belly:
        ic.path("M-58 4C-40 9-20 14 0 13C20 13 44 8 58 5C66 4 72 3 74 2C66 7 50 12 30 15C10 18-20 18-40 12Z",
                fill="#E2F4FD", opacity=0.9)
    ic.path("M-60-4C-40-10-10-17 6-18C14-18 22-19 30-18", fill="none", stroke="#fff", stroke_width=1.6,
            stroke_linecap="round", opacity=0.55)
    ic.circle(44, -6, 2.4, fill="#0B2A48")
    ic.circle(44.6, -6.6, 0.8, fill="#fff")
    ic.path("M60 3C55 4 50 3 46 1", fill="none", stroke="#0B2A48", stroke_width=1.2, stroke_linecap="round",
            opacity=0.7)


@icon("dolphin", kind="app", names=["dolphin", "org.kde.dolphin", "system-file-manager-dolphin"], title="Dolphin")
def dolphin(ic):
    tile(ic, "#24496F", "#0D1D31")
    shadow(ic, 128, 212, 94, 12)
    # the folder's back
    ic.path("M40 108a6 6 0 0 1 6-6h40a6 6 0 0 1 5 2l8 9h111a6 6 0 0 1 6 6v84a6 6 0 0 1-6 6H46a6 6 0 0 1-6-6z",
            fill=ic.lin([(0, "#1D86D0"), (1, "#0D4E8C")]))
    ic.path("M46 103h38a5 5 0 0 1 4 2", fill="none", stroke="#9AD6FA", stroke_width=1.5, opacity=0.7)
    ic.rect(56, 108, 134, 40, rx=2, fill=paper(ic, "white"), transform=rot(-3, 120, 120))
    ic.rect(66, 112, 132, 40, rx=2, fill="#F2F5F8", transform=rot(2, 130, 120))
    # the water in the folder, and the dolphin leaping out of it
    ic.ellipse(92, 126, 34, 6, fill="#9ADBFA", opacity=0.6)
    with ic.g(transform="translate(4 6) translate(134 72) rotate(-30) scale(1.02)", opacity=0.25):
        ic.path(DOLPHIN, fill="#000")
    with ic.g(transform="translate(134 72) rotate(-30) scale(1.02)"):
        dolphin_body(ic)
    for x, y, r in ((64, 112, 3), (72, 104, 2.2), (58, 100, 1.6), (110, 108, 2.6), (118, 100, 1.8), (104, 96, 1.3),
                    (80, 96, 1.4)):
        ic.circle(x, y, r, fill="#D8F2FF")
        ic.circle(x - r * 0.3, y - r * 0.3, r * 0.35, fill="#fff")
    # the folder's front, Breeze blue
    ic.path("M34 128a6 6 0 0 1 6-6h176a6 6 0 0 1 6 6l-7 76a7 7 0 0 1-7 6H48a7 7 0 0 1-7-6z", fill="#0A3A66",
            opacity=0.4, transform="translate(0 2)")
    ic.path("M34 128a6 6 0 0 1 6-6h176a6 6 0 0 1 6 6l-7 76a7 7 0 0 1-7 6H48a7 7 0 0 1-7-6z",
            fill=ic.lin([(0, "#7DD0F8"), (0.5, "#3DAEE9"), (1, "#1C86CC")]))
    ic.line(40, 123.2, 216, 123.2, stroke="#E2F6FF", stroke_width=2, stroke_linecap="round", opacity=0.9)
    # the wave on the front, pressed in
    ic.path("M64 186c12-10 24-10 36 0s24 10 36 0 24-10 36 0 14 8 20 6", fill="none", stroke="#0F5C9C",
            stroke_width=3, stroke_linecap="round", opacity=0.45)
    ic.path("M64 184c12-10 24-10 36 0s24 10 36 0 24-10 36 0 14 8 20 6", fill="none", stroke="#C9EEFF",
            stroke_width=1.2, stroke_linecap="round", opacity=0.6)
    ic.text("Dolphin", 52, 160, 11, font="sans-semibold", fill="#0D4E8C", opacity=0.75)


@small("dolphin")
def dolphin16(ic):
    tile(ic, "#24496F", "#0D1D31")
    ic.path("M2 7a.6.6 0 0 1 .6-.6h3l1 1h6.8a.6.6 0 0 1 .6.6v5.4h-12z", fill="#1675BE")
    with ic.g(transform="translate(8.2 4.6) rotate(-30) scale(0.088)"):
        ic.path(DOLPHIN, fill="#5FC0F2")
    ic.path("M1.6 9a.6.6 0 0 1 .6-.6h11.6a.6.6 0 0 1 .6.6l-.5 4.4a.6.6 0 0 1-.6.5H2.7a.6.6 0 0 1-.6-.5z",
            fill="#3DAEE9")


# --- Thunar: a wooden crate stencilled with a bolt, Thor's hammer by it -----

@icon("thunar", kind="app", names=["thunar"], title="Thunar")
def thunar(ic):
    tile(ic, "#4C5478", "#1A1D33")
    shadow(ic, 122, 210, 100, 12)
    plank = wood(ic, "#D9A86C", "#9A6634")
    # the crate: its top and its right side
    ic.poly([(34, 96), (162, 96), (184, 76), (56, 76)], fill=ic.lin([(0, "#E9C08A"), (1, "#C08850")]))
    for k in (1, 2, 3):
        x = 34 + k * 32
        ic.line(x, 96, x + 22, 76, stroke="#7A4A22", stroke_width=1.6, opacity=0.6)
    ic.poly([(162, 96), (184, 76), (184, 186), (162, 206)], fill=ic.lin([(0, "#A46E3A"), (1, "#5E3816")]))
    ic.line(173, 88, 173, 196, stroke="#3E2410", stroke_width=1.5, opacity=0.6)
    # the front, three planks on two battens
    ic.rect(34, 96, 128, 110, fill="#3E2410")
    for y in (96, 133, 170):
        ic.rect(34, y + 1, 128, 35, fill=plank)
        ic.line(34, y + 2, 162, y + 2, stroke="#FFE2B8", stroke_width=1.2, opacity=0.5)
        for gx in (58, 104, 132):
            ic.path(f"M{gx} {y + 10}c6 2 12 2 18 0", fill="none", stroke="#7A4A22", stroke_width=0.8, opacity=0.45)
    for x in (34, 148):
        ic.rect(x, 96, 14, 110, fill=wood(ic, "#C89156", "#7E4E24"))
        ic.line(x + 0.6, 96, x + 0.6, 206, stroke="#FFE2B8", stroke_width=1.2, opacity=0.45)
        for y in (104, 151, 198):
            ic.circle(x + 7, y, 1.8, fill="#3A3F45")
    # the stencil: Xfce's blue, a bolt and the name
    ic.path(bolt(84, 106, 1.7), fill="#1E6FD0", opacity=0.9)
    ic.path(bolt(84, 106, 1.7), fill="none", stroke="#0E3E80", stroke_width=1, opacity=0.4)
    ic.text("THUNAR", 98, 182, 15, font="sans-condensed", anchor="middle", spacing=2, fill="#1E6FD0", opacity=0.85)
    ic.text("FRAGILE · FILES", 98, 194, 6, font="mono-semibold", anchor="middle", spacing=1, fill="#3E2410",
            opacity=0.55)
    # the hammer, standing on its head, its grip up
    ic.rect(182, 98, 17, 74, rx=4, fill="#000", opacity=0.3, transform="translate(4 2)")
    ic.rect(182, 98, 17, 74, rx=4, fill=ic.lin([(0, "#8A4A2A"), (0.5, "#5A2C16"), (1, "#3A1A0A")], 0, 0, 1, 0))
    for y in range(102, 168, 6):
        ic.path(f"M182 {y}l17 4", stroke="#2A1206", stroke_width=1.2, opacity=0.6)
        ic.path(f"M182 {y + 1}l17 4", stroke="#C8845A", stroke_width=0.6, opacity=0.5)
    ic.rect(181, 92, 18, 10, rx=3, fill=steel(ic))
    ic.path("M190 92c-10-8-4-18 4-14", fill="none", stroke="#5A2C16", stroke_width=2.4, stroke_linecap="round")
    ic.rect(160, 166, 66, 42, rx=4, fill="#000", opacity=0.3, transform="translate(3 2)")
    ic.path("M166 166h54l6 8v26l-6 8h-54l-6-8v-26z", fill=ic.lin([(0, "#F1F3F6"), (0.45, "#A8B0BA"), (1, "#4D555F")],
                                                                    0, 0, 1, 1))
    ic.path("M170 172h46v30h-46z", fill=ic.lin([(0, "#C9CFD6"), (1, "#7C8590")], 0, 0, 1, 1))
    ic.path(bolt(186, 175, 0.8), fill="#2B8FE3")
    ic.path("M166 167h54", stroke="#fff", stroke_width=1.5, opacity=0.8)
    ic.rect(184, 160, 12, 8, rx=1.5, fill=steel(ic))


@small("thunar")
def thunar16(ic):
    tile(ic, "#4C5478", "#1A1D33")
    ic.rect(2, 5, 9, 9, fill="#C08850")
    ic.rect(2, 5, 9, 1, fill="#E9C08A")
    ic.path(bolt(4.4, 6.2, 0.24), fill="#1E6FD0")
    ic.rect(11.6, 5, 1.6, 6, rx=0.6, fill="#6A341C")
    ic.rect(10, 10.4, 5, 3.6, rx=0.6, fill="#AEB6BF")


# --- Nemo: a ship's wheel, Mint's green on its hub, a fish on the enamel ----

FISH = "M-10 0C-6-7 5-7 9 0C5 7-6 7-10 0ZM8 0L14-6V6Z"


@icon("nemo", kind="app", names=["nemo"], title="Nemo")
def nemo(ic):
    tile(ic, "#2D7464", "#0E322A")
    cx, cy = 128, 118
    shadow(ic, 128, 222, 76, 9)
    timber = ic.lin([(0, "#D69A5E"), (0.5, "#9C6230"), (1, "#5E3414")], 40, 30, 220, 210, units="userSpaceOnUse")
    # shadows of the spokes and the rim
    with ic.g(transform="translate(4 5)", opacity=0.3):
        for k in range(8):
            with ic.g(transform=rot(k * 45 + 22.5, cx, cy)):
                ic.rect(cx - 4, cy - 100, 8, 82, rx=4, fill="#000")
        ic.circle(cx, cy, 66, fill="none", stroke="#000", stroke_width=14)
    # the spokes, turned handles past the rim
    for k in range(8):
        with ic.g(transform=rot(k * 45 + 22.5, cx, cy)):
            ic.rect(cx - 3.5, cy - 74, 7, 56, fill=timber)
            t = cy - 72
            ic.path(f"M{cx - 3.5} {t}L{cx - 4} {t - 6}C{cx - 8} {t - 11} {cx - 7} {t - 19} {cx - 4} {t - 23}"
                    f"A4.5 4.5 0 0 1 {cx + 4} {t - 23}C{cx + 7} {t - 19} {cx + 8} {t - 11} {cx + 4} {t - 6}"
                    f"L{cx + 3.5} {t}Z", fill=timber)
            ic.rect(cx - 5, t - 2, 10, 3, rx=1.2, fill="#C99645")
            ic.line(cx - 2, t - 20, cx - 5, t - 12, stroke="#FFE2B8", stroke_width=1.2, stroke_linecap="round",
                    opacity=0.5)
    # the rim, its brass band
    ic.circle(cx, cy, 66, fill="none", stroke=timber, stroke_width=14)
    ic.circle(cx, cy, 72.5, fill="none", stroke="#3A1E0A", stroke_width=1, opacity=0.5)
    ic.circle(cx, cy, 66, fill="none", stroke=brass(ic, 0, 0, 1, 1), stroke_width=3.4)
    ic.path(f"M{cx - 68} {cy - 14}A70 70 0 0 1 {cx - 14} {cy - 68}", fill="none", stroke="#FFE2B8",
            stroke_width=1.6, opacity=0.6)
    for k in range(8):
        x, y = polar(cx, cy, 66, k * 45 + 22.5)
        ic.circle(x, y, 2.2, fill="#F6DDA0")
        ic.circle(x + 0.4, y + 0.5, 2.2, fill="none", stroke="#5A3A10", stroke_width=0.6, opacity=0.6)
    # the hub: brass, and the green enamel with a fish
    ic.circle(cx + 2, cy + 3, 27, fill="#000", opacity=0.3)
    ic.circle(cx, cy, 27, fill=brass(ic))
    ic.circle(cx, cy, 26, fill="none", stroke="#FFF2C8", stroke_width=1, opacity=0.6)
    arc_text(ic, "NEMO", cx, cy, 21, 0, 5.5, font="mono-semibold", spacing=1.6, fill="#5A3A10")
    ic.circle(cx, cy, 16, fill="#2F5A12")
    ic.circle(cx, cy, 15, fill=ic.rad([(0, "#A6DB6A"), (1, "#4E9A22")], cx=0.4, cy=0.35, r=0.8))
    with ic.g(transform=f"translate({cx - 1} {cy + 1}) scale(0.9)"):
        ic.path(FISH, fill="#F4FBEA")
        ic.circle(5, -1.5, 1.1, fill="#2F5A12")
    ic.path(f"M{cx - 12} {cy - 6}a14 14 0 0 1 12-9 15 15 0 0 0-12 9z", fill="#fff", opacity=0.55)
    # a paper tag tied to a spoke
    tx, ty = polar(cx, cy, 76, 157.5)
    ic.path(f"M{tx:.1f} {ty:.1f}C{tx + 6:.1f} {ty + 8:.1f} {tx + 14:.1f} {ty + 10:.1f} {tx + 22:.1f} {ty + 14:.1f}",
            fill="none", stroke="#F2E6CC", stroke_width=1)
    with ic.g(transform=rot(-14, tx + 22, ty + 14)):
        x0, y0 = tx + 20, ty + 10
        ic.path(f"M{x0} {y0}l8-4h42v24h-42l-8-4z", fill="#000", opacity=0.25, transform="translate(2 2)")
        ic.path(f"M{x0} {y0}l8-4h42v24h-42l-8-4z", fill=paper(ic, "kraft"))
        ic.circle(x0 + 6, y0 + 8, 1.6, fill="#7A5228")
        ic.text("~/home", x0 + 30, y0 + 13, 11, font="hand", anchor="middle", fill="#3A2A10")


@small("nemo")
def nemo16(ic):
    tile(ic, "#2D7464", "#0E322A")
    for k in range(8):
        x1, y1 = polar(8, 8, 2, k * 45 + 22.5)
        x2, y2 = polar(8, 8, 7, k * 45 + 22.5)
        ic.line(x1, y1, x2, y2, stroke="#B67A42", stroke_width=1.1, stroke_linecap="round")
    ic.circle(8, 8, 4.6, fill="none", stroke="#A86C36", stroke_width=1.4)
    ic.circle(8, 8, 2.4, fill="#C99645")
    ic.circle(8, 8, 1.6, fill="#7CC046")


# --- Flatseal: a rubber stamp, its seal of permission on a sheet ------------

INK = "#2C6BD6"


@icon("flatseal", kind="app", names=["com.github.tchx84.Flatseal", "flatseal"], title="Flatseal")
def flatseal(ic):
    tile(ic, "#6E5C9A", "#2B2149")
    shadow(ic, 124, 212, 98, 12)
    # the sheet, its permissions listed
    with ic.g(transform=rot(-5, 104, 140)):
        ic.rect(36, 52, 132, 160, rx=3, fill="#000", opacity=0.25, transform="translate(3 3)")
        ic.rect(36, 52, 132, 160, rx=3, fill=paper(ic, "cream"))
        ic.text("Permissions", 48, 72, 11, font="sans-semibold", fill="#2B2149")
        ic.text("org.inua.Notes", 48, 83, 6.2, font="mono", fill="#8C887F")
        for i, w in enumerate(("Network", "Home folder", "Wayland")):
            y = 98 + i * 13
            ic.rect(48, y - 7, 8, 8, rx=1.5, fill="none", stroke="#6A665D", stroke_width=1)
            ic.path(f"M49.5 {y - 3}l2 2.4 4-5", fill="none", stroke=INK, stroke_width=1.6, stroke_linecap="round",
                    stroke_linejoin="round")
            ic.text(w, 61, y, 7.5, fill="#4E4C47")
        # the impression: a round seal, a tick in it
        sx, sy = 92, 166
        with ic.g(opacity=0.88):
            ic.circle(sx, sy, 31, fill="none", stroke=INK, stroke_width=3)
            ic.circle(sx, sy, 24, fill="none", stroke=INK, stroke_width=1.2)
            arc_text(ic, "FLATSEAL", sx, sy, 26, 0, 5.5, font="mono-semibold", spacing=1.2, fill=INK)
            arc_text(ic, "ALLOWED", sx, sy, 30.5, 180, 5.5, font="mono-semibold", spacing=1.2, inner=True,
                     fill=INK)
            ic.circle(sx, sy, 16, fill=INK)
            ic.path(f"M{sx - 8} {sy}l5.5 6 11-12", fill="none", stroke="#FCF9F2", stroke_width=4,
                    stroke_linecap="round", stroke_linejoin="round")
        for x, y in ((70, 150), (113, 186), (98, 136), (76, 186)):
            ic.circle(x, y, 1.6, fill="#FCF9F2", opacity=0.8)
    # the stamp, standing beside it
    ic.ellipse(176, 196, 36, 8, fill="#000", opacity=0.3)
    ic.rect(142, 170, 68, 22, rx=3, fill="#1A2D5A")
    ic.rect(142, 186, 68, 6, rx=2, fill="#1D3C8A")
    ic.rect(140, 148, 72, 26, rx=4, fill=wood(ic, "#D9A86C", "#8A5628"))
    ic.line(142, 149, 210, 149, stroke="#FFE2B8", stroke_width=1.4, opacity=0.6)
    ic.rect(146, 154, 60, 14, rx=2, fill="#FCF9F2")
    ic.text("Flatseal", 176, 165, 10, font="sans-semibold", anchor="middle", fill=INK)
    ic.path("M166 148c2-12 4-24 2-36h16c-2 12 0 24 2 36z", fill=wood(ic, "#C48A55", "#6E3E18"))
    ic.path("M170 146c1-12 3-24 1-34", fill="none", stroke="#FFE2B8", stroke_width=1.2, opacity=0.4)
    ic.circle(176, 88, 26, fill=ic.rad([(0, "#7FB2F5"), (0.55, "#3A78DC"), (1, "#173E8A")], cx=0.38, cy=0.32,
                                       r=0.75))
    ic.ellipse(166, 77, 9, 5, fill="#fff", opacity=0.5, transform=rot(-30, 166, 77))
    ic.path("M168 92l5.5 6 11-12", fill="none", stroke="#fff", stroke_width=3.5, stroke_linecap="round",
            stroke_linejoin="round", opacity=0.85)


@small("flatseal")
def flatseal16(ic):
    tile(ic, "#6E5C9A", "#2B2149")
    ic.rect(1.6, 4, 8.4, 10, rx=0.5, fill="#FCF9F2")
    ic.circle(6, 9.4, 2.6, fill="none", stroke=INK, stroke_width=0.9)
    ic.path("M4.8 9.4l1 1 1.8-2", fill="none", stroke=INK, stroke_width=0.8)
    ic.rect(10, 9.6, 5, 3, rx=0.4, fill="#B67A42")
    ic.rect(11.8, 6, 1.4, 4, fill="#8A5628")
    ic.circle(12.5, 4.6, 2.2, fill="#3A78DC")


# --- Mission Center: a mission-control console, its screens lit -----------

def screen(ic, x, y, w, h):
    ic.rect(x - 3, y - 3, w + 6, h + 6, rx=4, fill="#0C0F14")
    ic.rect(x, y, w, h, rx=2, fill=glass_dark(ic, "#0E2A44"))
    grid = ic.define('<pattern id="{id}" width="8" height="8" patternUnits="userSpaceOnUse">'
                     '<path d="M8 0V8H0" fill="none" stroke="#3AA8FF" stroke-opacity=".14" stroke-width=".6"/>'
                     '</pattern>', "p")
    ic.rect(x, y, w, h, rx=2, fill=f"url(#{grid})")


def glass_dark(ic, tint):
    return ic.rad([(0, tint), (1, "#04080D")], cx=0.35, cy=0.4, r=0.8)


@icon("mission-center", kind="app", names=["io.missioncenter.MissionCenter", "mission-center"],
      title="Mission Center")
def mission_center(ic):
    tile(ic, "#3A4182", "#111435")
    shadow(ic, 128, 212, 100, 11)
    # the back panel with three screens
    ic.rect(36, 36, 184, 112, rx=10, fill=ic.lin([(0, "#5A6274"), (0.1, "#3A4150"), (1, "#1C2028")]))
    ic.rect(36.75, 36.75, 182.5, 110.5, rx=9.25, fill="none", stroke="#fff", stroke_opacity=0.14, stroke_width=1.5)
    for x, y in ((42, 42), (214, 42), (42, 142), (214, 142)):
        screw(ic, x, y, 2.2)
    screen(ic, 48, 50, 52, 58)
    screen(ic, 108, 50, 52, 58)
    screen(ic, 168, 50, 40, 58)
    # left: CPU, a line over time
    ic.text("CPU", 52, 60, 6, font="mono-semibold", fill="#7CC8FF")
    ic.text("23%", 96, 60, 6, font="mono-semibold", anchor="end", fill="#7CC8FF")
    pts = [(50, 96), (56, 92), (61, 94), (66, 84), (71, 88), (76, 78), (81, 86), (86, 80), (91, 90), (98, 82)]
    ic.path("M" + "L".join(f"{x} {y}" for x, y in pts) + "L98 108L50 108Z", fill="#33B4FF", opacity=0.22)
    ic.path("M" + "L".join(f"{x} {y}" for x, y in pts), fill="none", stroke="#5CC8FF", stroke_width=1.6,
            stroke_linejoin="round")
    # middle: an orbit, the craft on it
    ic.circle(134, 80, 10, fill=ic.rad([(0, "#5BB7FF"), (1, "#1A4E9A")], cx=0.35, cy=0.35, r=0.8))
    ic.ellipse(134, 80, 22, 9, fill="none", stroke="#9FE0FF", stroke_width=1, stroke_dasharray="2 2",
               transform=rot(-20, 134, 80))
    ic.circle(153, 72, 2.2, fill="#FFD447")
    ic.text("T+04:12", 134, 104, 6.5, font="mono-semibold", anchor="middle", fill="#FFD447")
    # right: memory and disk, bars
    for i, (lvl, col) in enumerate(((0.7, "#3DDC84"), (0.45, "#FFB547"), (0.85, "#3DDC84"))):
        bx = 174 + i * 11
        ic.rect(bx, 58, 7, 44, rx=1, fill="#fff", opacity=0.08)
        ic.rect(bx, 58 + 44 * (1 - lvl), 7, 44 * lvl, rx=1, fill=col)
    for x in (48, 108, 168):
        ic.path(f"M{x} {56}a6 6 0 0 1 6-6h24L{x} 92z", fill=glare(ic, 0.8))
    # the strip of lamps under the screens
    for i, col in enumerate(("#3DDC84", "#3DDC84", "#FFB547", "#3DDC84", "#FF5B4F", "#5CC8FF", "#3DDC84",
                             "#5CC8FF")):
        x = 56 + i * 21
        ic.rect(x, 120, 14, 6, rx=2, fill=col)
        ic.rect(x + 1, 120.6, 12, 1.6, rx=0.8, fill="#fff", opacity=0.5)
    ic.text("MISSION CENTER", 128, 140, 6.5, font="mono-semibold", anchor="middle", spacing=1.6, fill="#A7B0C2")
    # the desk: its sloped top and front
    ic.poly([(36, 148), (220, 148), (232, 166), (24, 166)], fill=ic.lin([(0, "#6C7588"), (1, "#454C5C")]))
    ic.line(36, 148.8, 220, 148.8, stroke="#fff", stroke_width=1.4, opacity=0.4)
    ic.rect(24, 166, 208, 40, rx=5, fill=ic.lin([(0, "#3A4150"), (1, "#1A1D24")]))
    ic.line(26, 167, 230, 167, stroke="#fff", stroke_width=1, opacity=0.18)
    for i in range(6):
        x = 40 + i * 18
        ic.rect(x - 4, 176, 8, 18, rx=2, fill="#0C0F14")
        ic.rect(x - 1.6, 172 if i % 3 else 182, 3.2, 12, rx=1.6, fill=steel(ic))
        ic.circle(x, 172 if i % 3 else 194, 2.6, fill="#E6EAEE")
    ic.circle(194, 186, 14, fill="#5A0E0A")
    ic.circle(194, 184, 12, fill=ic.rad([(0, "#FF7A66"), (0.6, "#D8281C"), (1, "#8A120A")], cx=0.38, cy=0.3, r=0.8))
    ic.ellipse(190, 179, 4.5, 2.4, fill="#fff", opacity=0.55, transform=rot(-25, 190, 179))
    ic.rect(150, 174, 26, 24, rx=3, fill="#0C0F14")
    ic.text("GO", 163, 190, 9, font="mono-semibold", anchor="middle", fill="#3DDC84")


@small("mission-center")
def mission_center16(ic):
    tile(ic, "#3A4182", "#111435")
    ic.rect(2, 2.5, 12, 7.5, rx=0.8, fill="#3A4150")
    ic.rect(3, 3.5, 4.6, 5.4, fill="#0E2A44")
    ic.rect(8.4, 3.5, 4.6, 5.4, fill="#0E2A44")
    ic.path("M3.2 7.6l1.2-1 1 .6 1.2-2", fill="none", stroke="#5CC8FF", stroke_width=0.7)
    ic.rect(9.4, 5.6, 1, 3, fill="#3DDC84")
    ic.rect(11.2, 4.6, 1, 4, fill="#3DDC84")
    ic.rect(1.5, 10.5, 13, 3.5, rx=0.6, fill="#2A303C")
    ic.circle(12, 12.2, 1.2, fill="#E23A2C")


# --- Resources: a car's gauge cluster, CPU and memory --------------------

def gauge(ic, cx, cy, r, value, labels, unit, reading, col):
    ic.circle(cx + 2, cy + 3, r, fill="#000", opacity=0.35)
    ic.circle(cx, cy, r, fill=ic.lin([(0, "#F4F6F8"), (0.5, "#9AA3AC"), (1, "#4A525B")], 0, 0, 1, 1))
    ic.circle(cx, cy, r - 4, fill=ic.lin([(0, "#3E454D"), (1, "#C9D0D6")], 0, 0, 1, 1))
    ic.circle(cx, cy, r - 6, fill=ic.rad([(0, "#24282E"), (1, "#0A0C0F")], cx=0.45, cy=0.4, r=0.7))
    ic.path(sector(cx, cy, r - 9, r - 13, -120, 60), fill=col, opacity=0.85)
    ic.path(sector(cx, cy, r - 9, r - 13, 84, 120), fill="#E5483A", opacity=0.9)
    n = len(labels) - 1
    for i in range(n * 4 + 1):
        a = -120 + 240 * i / (n * 4)
        big = i % 4 == 0
        x1, y1 = polar(cx, cy, r - 8, a)
        x2, y2 = polar(cx, cy, r - (16 if big else 12), a)
        ic.line(x1, y1, x2, y2, stroke="#F4F6F8", stroke_width=1.6 if big else 0.8)
    for i, s in enumerate(labels):
        x, y = polar(cx, cy, r - 23, -120 + 240 * i / n)
        ic.text(s, x, y + 2.6, 7, font="sans-semibold", anchor="middle", fill="#E8ECEF")
    ic.text(unit, cx, cy - 12, 6, font="mono-semibold", anchor="middle", spacing=1, fill="#9AA3AC")
    ic.rect(cx - 14, cy + 15, 28, 10, rx=1.5, fill="#0F2A1C")
    ic.text(reading, cx, cy + 23, 7, font="mono-semibold", anchor="middle", fill="#5CF0A0")
    a = -120 + 240 * value
    with ic.g(transform=rot(a, cx, cy)):
        ic.path(f"M{cx - 2.4} {cy}L{cx - 0.8} {cy - r + 12}H{cx + 0.8}L{cx + 2.4} {cy}Z", fill="#000", opacity=0.4,
                transform="translate(1.5 1.5)")
        ic.path(f"M{cx - 2.4} {cy + 8}L{cx - 0.8} {cy - r + 12}H{cx + 0.8}L{cx + 2.4} {cy + 8}Z", fill="#FF8A2A")
    ic.circle(cx, cy, 6, fill=ic.lin([(0, "#6A727C"), (1, "#1E2228")], 0, 0, 1, 1))
    ic.circle(cx - 1.4, cy - 1.4, 1.6, fill="#fff", opacity=0.5)
    ic.path(f"M{cx - r + 7} {cy - 6}A{r - 6} {r - 6} 0 0 1 {cx - 6} {cy - r + 7}L{cx} {cy - r + 12}"
            f"A{r - 12} {r - 12} 0 0 0 {cx - r + 12} {cy}z", fill="#fff", opacity=0.12)


@icon("resources", kind="app", names=["net.nokyan.Resources", "resources"], title="Resources")
def resources(ic):
    tile(ic, "#2F7259", "#0E3022")
    shadow(ic, 128, 206, 102, 12)
    # the binnacle: a leather hood over the dials
    hood = "M22 130C22 82 50 54 92 54C108 54 118 60 128 60C138 60 148 54 164 54C206 54 234 82 234 130V176a18 18 0 0 1-18 18H40a18 18 0 0 1-18-18z"
    ic.path(hood, fill="#000", opacity=0.3, transform="translate(3 4)")
    ic.path(hood, fill=ic.lin([(0, "#3E434A"), (1, "#121417")]))
    ic.path("M30 128C30 88 56 62 92 62C108 62 118 68 128 68C138 68 148 62 164 62C200 62 226 88 226 128",
            fill="none", stroke="#8A9098", stroke_width=1, stroke_dasharray="3 2.4", opacity=0.6)
    ic.path("M24 120C28 80 56 56 92 56", fill="none", stroke="#fff", stroke_width=1.5, opacity=0.25)
    gauge(ic, 78, 132, 47, 0.34, ["0", "25", "50", "75", "100"], "CPU %", "34%", "#3DDC84")
    gauge(ic, 178, 132, 47, 0.62, ["0", "4", "8", "12", "16"], "MEM GiB", "9.8", "#3DDC84")
    # the warning lamps between them
    for y, col in ((92, "#3DDC84"), (106, "#FFB547")):
        ic.circle(128, y, 3, fill=col)
        ic.circle(127.2, y - 0.8, 1, fill="#fff", opacity=0.7)
    ic.text("RESOURCES", 128, 188, 6.5, font="mono-semibold", anchor="middle", spacing=1.8, fill="#8A9098")


@small("resources")
def resources16(ic):
    tile(ic, "#2F7259", "#0E3022")
    ic.rect(1, 3.5, 14, 9.5, rx=3, fill="#1E2125")
    for cx in (5, 11):
        ic.circle(cx, 8.4, 3.6, fill="#C9D0D6")
        ic.circle(cx, 8.4, 2.9, fill="#0E1013")
        ic.path(sector(cx, 8.4, 2.6, 1.9, -120, 40), fill="#3DDC84")
    ic.line(5, 8.4, 3.6, 6.9, stroke="#FF8A2A", stroke_width=0.7)
    ic.line(11, 8.4, 12.8, 7.6, stroke="#FF8A2A", stroke_width=0.7)


# --- System Monitor: a bedside patient monitor, a pulse on it -------------

def ecg(x0, y0, w, beats, amp):
    pts = []
    shape = [(0, 0), (0.14, 0), (0.18, -0.12), (0.22, 0), (0.3, 0), (0.33, 0.12), (0.37, -1), (0.41, 0.35),
             (0.45, 0), (0.58, 0), (0.66, -0.25), (0.74, 0)]
    bw = w / beats
    for b in range(beats):
        for t, v in shape:
            pts.append((x0 + b * bw + t * bw, y0 + v * amp))
    pts.append((x0 + w, y0))
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def wave(x0, y0, w, n, amp):
    pts = [(x0 + w * i / (n * 12), y0 - amp * max(0, math.sin(math.pi * 2 * i / 12)) ** 0.7
            + amp * 0.3 * math.sin(math.pi * 4 * i / 12)) for i in range(n * 12 + 1)]
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def heart(x, y, s):
    return (f"M{x} {y + 3 * s}C{x - 6 * s} {y - 1 * s} {x - 5 * s} {y - 6 * s} {x - 2.4 * s} {y - 6 * s}"
            f"C{x - 1 * s} {y - 6 * s} {x} {y - 5 * s} {x} {y - 4 * s}C{x} {y - 5 * s} {x + 1 * s} {y - 6 * s}"
            f" {x + 2.4 * s} {y - 6 * s}C{x + 5 * s} {y - 6 * s} {x + 6 * s} {y - 1 * s} {x} {y + 3 * s}Z")


@icon("gnome-system-monitor", kind="app",
      names=["deepin-system-monitor", "gkrellm", "gnethogs", "gnome-monitor", "gnome-system-monitor", "ksysguard",
             "org.gnome.SystemMonitor", "org.kde.plasma.awesomewidget", "org.kde.plasma.systemloadviewer",
             "org.kde.resourcesMonitor", "org.xfce.taskmanager", "package_utilities", "qps",
             "utilities-system-monitor"],
      title="System Monitor")
def gnome_system_monitor(ic):
    tile(ic, "#8E4044", "#3A1418")
    shadow(ic, 128, 212, 98, 12)
    # the handle, and the housing
    ic.path("M80 56V40a10 10 0 0 1 10-10h76a10 10 0 0 1 10 10V56", fill="none", stroke="#5A1A1E", stroke_width=12,
            opacity=0.5, transform="translate(2 3)")
    ic.path("M80 56V40a10 10 0 0 1 10-10h76a10 10 0 0 1 10 10V56", fill="none",
            stroke=ic.lin([(0, "#F4F5F3"), (1, "#A9AEAC")]), stroke_width=10)
    ic.rect(28, 48, 200, 158, rx=16, fill="#000", opacity=0.3, transform="translate(3 4)")
    ic.rect(28, 48, 200, 158, rx=16, fill=ic.lin([(0, "#FAFAF8"), (1, "#BEC3C1")], 0, 0, 1, 1))
    ic.rect(28.75, 48.75, 198.5, 156.5, rx=15.25, fill="none", stroke="#fff", stroke_width=1.5)
    # the screen
    ic.rect(38, 58, 160, 118, rx=8, fill="#23272C")
    ic.rect(42, 62, 152, 110, rx=5, fill=ic.rad([(0, "#0E1A20"), (1, "#03070A")], cx=0.35, cy=0.4, r=0.8))
    ic.line(150, 66, 150, 168, stroke="#fff", stroke_opacity=0.12)
    for y in (100, 136):
        ic.line(46, y, 190, y, stroke="#fff", stroke_opacity=0.08)
    ic.text("II", 48, 72, 6, font="mono-semibold", fill="#3DE07A")
    ic.path(ecg(46, 90, 102, 3, 20), fill="none", stroke="#3DE07A", stroke_width=1.8, stroke_linejoin="round")
    ic.text("PLETH", 48, 110, 6, font="mono-semibold", fill="#3CC8F0")
    ic.path(wave(46, 128, 102, 3, 12), fill="none", stroke="#3CC8F0", stroke_width=1.6, stroke_linejoin="round")
    ic.text("RESP", 48, 146, 6, font="mono-semibold", fill="#F2D24A")
    ic.path("M46 160" + "".join(f"c8-10 16-10 24 0 8 10 {8} 10 {9.5} 0" for _ in range(3)), fill="none",
            stroke="#F2D24A", stroke_width=1.4)
    # the readings
    ic.path(heart(160, 76, 1.1), fill="#FF5A5A")
    ic.text("HR", 188, 74, 6, font="mono-semibold", anchor="end", fill="#3DE07A")
    ic.text("72", 188, 96, 22, font="sans-semibold", anchor="end", fill="#3DE07A")
    ic.text("SpO2", 188, 110, 6, font="mono-semibold", anchor="end", fill="#3CC8F0")
    ic.text("98", 188, 130, 18, font="sans-semibold", anchor="end", fill="#3CC8F0")
    ic.text("RR", 188, 144, 6, font="mono-semibold", anchor="end", fill="#F2D24A")
    ic.text("16", 188, 164, 16, font="sans-semibold", anchor="end", fill="#F2D24A")
    ic.path("M42 67a5 5 0 0 1 5-5h86L70 172H47a5 5 0 0 1-5-5z", fill=glare(ic, 0.9))
    # the controls on the right, the speaker below
    ic.circle(214, 76, 9, fill="#7A8084", transform="translate(1 1.5)")
    ic.circle(214, 76, 9, fill=ic.lin([(0, "#E9ECEB"), (1, "#8A908E")], 0, 0, 1, 1))
    ic.line(214, 69, 214, 74, stroke="#3A3F45", stroke_width=1.6, stroke_linecap="round")
    for i, col in enumerate(("#D8463C", "#E8ECEB", "#E8ECEB", "#E8ECEB")):
        y = 98 + i * 18
        ic.rect(206, y + 1, 16, 12, rx=3, fill="#7A8084")
        ic.rect(206, y, 16, 11, rx=3, fill=col)
        ic.rect(208, y + 1, 12, 1.6, rx=0.8, fill="#fff", opacity=0.6)
    ic.circle(212, 186, 2.6, fill="#3DE07A")
    for i in range(8):
        ic.rect(44 + i * 8, 184, 4, 12, rx=2, fill="#8A908E", opacity=0.6)
    ic.text("SYSTEM MONITOR", 192, 194, 6, font="mono-semibold", anchor="end", spacing=1, fill="#6A706E")


@small("gnome-system-monitor")
def gnome_system_monitor16(ic):
    tile(ic, "#8E4044", "#3A1418")
    ic.rect(1.5, 3, 13, 10.5, rx=1.4, fill="#E8EAE8")
    ic.rect(2.5, 4, 9, 7.6, rx=0.6, fill="#081014")
    ic.path(ecg(2.8, 8.2, 8.4, 2, 3.2), fill="none", stroke="#3DE07A", stroke_width=0.8)
    ic.circle(13, 6, 0.9, fill="#D8463C")
    ic.circle(13, 9, 0.9, fill="#9AA0A2")


# --- BleachBit: a spray bottle, its trigger red, mist out of the nozzle ---

BOTTLE = ("M98 82H128V96C128 104 150 110 154 128V196Q154 208 142 208H82Q70 208 70 196V128"
          "C74 110 98 104 98 96Z")


@icon("bleachbit", kind="app",
      names=["bleachbit", "computerjanitor", "gcleaner", "org.bleachbit.BleachBit",
             "preferences-system-privacy-housekeeping", "shredder", "ubuntu-cleaner"],
      title="BleachBit")
def bleachbit(ic):
    tile(ic, "#3792A8", "#0F3E4C")
    shadow(ic, 118, 210, 62, 10)
    # the bottle: translucent plastic, the liquid in it
    ic.path(BOTTLE, fill="#000", opacity=0.25, transform="translate(4 3)")
    ic.path(BOTTLE, fill=ic.lin([(0, "#F4FBFE"), (0.55, "#D6ECF4"), (1, "#9CC6D8")], 0, 0, 1, 0))
    inside = ic.clip(f'<path d="{BOTTLE}"/>')
    with ic.g(clip_path=inside):
        ic.rect(60, 120, 100, 100, fill=ic.lin([(0, "#7FD0F0"), (1, "#2A8EC0")], 0, 0, 1, 0), opacity=0.7)
        ic.ellipse(112, 120, 44, 3.5, fill="#C8F0FF", opacity=0.8)
        ic.rect(76, 90, 8, 120, fill="#fff", opacity=0.45)
    ic.line(113, 90, 116, 204, stroke="#8FB8C8", stroke_width=2, opacity=0.6)
    ic.path(BOTTLE, fill="none", stroke="#fff", stroke_width=1.5, opacity=0.6)
    # the label, the brand's red and blue
    ic.rect(72, 140, 80, 52, rx=3, fill=paper(ic, "white"))
    ic.rect(72, 140, 80, 13, rx=3, fill="#C8281E")
    ic.rect(72, 148, 80, 5, fill="#C8281E")
    ic.text("CLEANER", 112, 150, 7, font="mono-semibold", anchor="middle", spacing=1.6, fill="#FFF3EC")
    ic.text("BleachBit", 112, 172, 14, font="sans-bold", anchor="middle", fill="#1F4A8A")
    ic.text("cache · logs · tmp", 112, 184, 6, font="mono", anchor="middle", fill="#6A6F78")
    for x, y, r in ((96, 132, 2.4), (130, 127, 1.6), (106, 124, 1.3)):
        ic.circle(x, y, r, fill="none", stroke="#3792A8", stroke_width=0.8)
    ic.rect(148, 140, 4, 52, fill="#000", opacity=0.12)
    # the collar, the sprayer head and its trigger
    ic.rect(94, 72, 38, 14, rx=2, fill=ic.lin([(0, "#F2F4F6"), (1, "#9AA3AC")], 0, 0, 1, 0))
    for x in range(98, 130, 4):
        ic.line(x, 73, x, 85, stroke="#6A727C", stroke_width=0.8, opacity=0.6)
    head = "M90 74V56C90 44 100 38 112 38H164a6 6 0 0 1 6 6V56a6 6 0 0 1-6 6H140C134 62 132 66 132 74Z"
    ic.path(head, fill="#000", opacity=0.3, transform="translate(3 3)")
    ic.path(head, fill=ic.lin([(0, "#FF6A58"), (0.5, "#D8281C"), (1, "#8A120A")], 0, 0, 0.6, 1))
    ic.path("M94 60C94 48 102 42 112 42H160", fill="none", stroke="#FFC0B4", stroke_width=1.6, opacity=0.7)
    ic.rect(170, 44, 8, 12, rx=2, fill="#2A2C30")
    trig = "M140 62C146 70 150 82 148 100C146 104 142 104 140 100C140 86 136 74 132 66Z"
    ic.path(trig, fill=ic.lin([(0, "#E8402E"), (1, "#8A120A")], 0, 0, 1, 0))
    ic.path("M141 66C145 74 146 84 145 96", fill="none", stroke="#FFB0A4", stroke_width=1.2, opacity=0.6)
    # the mist
    for i in range(26):
        a = -24 + (i * 37 % 48)
        d = 12 + (i * 53 % 50)
        x, y = 182 + d * math.cos(math.radians(a)), 50 + d * math.sin(math.radians(a))
        ic.circle(x, y, 1.0 + (i % 3) * 0.6, fill="#E8FAFF", opacity=0.9 - d / 90)
    for x, y, s in ((206, 28, 5), (222, 76, 4)):
        ic.path(f"M{x} {y - s}L{x + s * 0.3} {y - s * 0.3}L{x + s} {y}L{x + s * 0.3} {y + s * 0.3}L{x} {y + s}"
                f"L{x - s * 0.3} {y + s * 0.3}L{x - s} {y}L{x - s * 0.3} {y - s * 0.3}Z", fill="#fff", opacity=0.9)


@small("bleachbit")
def bleachbit16(ic):
    tile(ic, "#3792A8", "#0F3E4C")
    ic.path("M6 5.5h2v1c0 .6 2 1 2 2.4v4.6a.8.8 0 0 1-.8.8H4.8a.8.8 0 0 1-.8-.8V8.9c0-1.4 2-1.8 2-2.4z",
            fill="#E4F3F8")
    ic.rect(4, 9.4, 6, 3, fill="#1F4A8A")
    ic.path("M5.5 5.6V4a1.6 1.6 0 0 1 1.6-1.6h4.4v2H9l-.4 1.2z", fill="#D8281C")
    for x, y in ((13, 2.6), (14.2, 4), (12.8, 4.8)):
        ic.circle(x, y, 0.6, fill="#E8FAFF")


# --- Disk Usage Analyzer: a ring chart on a clipboard, a loupe over it ----

GNOME_COLOURS = ["#3584E4", "#33D17A", "#F6D32D", "#FF7800", "#E01B24", "#9141AC"]


@icon("baobab", kind="app", names=["baobab", "org.gnome.baobab"], title="Disk Usage Analyzer")
def baobab(ic):
    tile(ic, "#7C4A70", "#331830")
    shadow(ic, 128, 214, 90, 12)
    # the clipboard and its sheet
    ic.rect(50, 34, 152, 180, rx=10, fill="#000", opacity=0.3, transform="translate(3 3)")
    ic.rect(50, 34, 152, 180, rx=10, fill=wood(ic, "#C99A66", "#7A4E26"))
    ic.rect(50.75, 34.75, 150.5, 178.5, rx=9.25, fill="none", stroke="#FFE2B8", stroke_width=1.5, opacity=0.4)
    ic.rect(60, 48, 132, 158, rx=2, fill=paper(ic, "white"))
    ic.text("Disk Usage", 70, 72, 11, font="sans-semibold", fill="#331830")
    ic.text("/home · 212 GB", 70, 83, 6.2, font="mono", fill="#8C887F")
    # the sunburst: folders, then the folders in them
    cx, cy = 126, 142
    ic.circle(cx, cy, 13, fill="#5E5C64")
    ic.text("212", cx, cy + 2.5, 7, font="mono-semibold", anchor="middle", fill="#fff")
    rings = [
        (15, 31, [(0, 120, 0), (120, 200, 1), (200, 260, 2), (260, 310, 3), (310, 340, 4), (340, 360, 5)]),
        (32, 46, [(0, 70, 0), (70, 110, 0), (120, 170, 1), (170, 195, 1), (200, 240, 2), (260, 300, 3),
                  (310, 330, 4)]),
        (47, 56, [(0, 40, 0), (70, 95, 0), (120, 150, 1), (200, 225, 2), (260, 285, 3)]),
    ]
    for depth, (ri, ro, segs) in enumerate(rings):
        for a1, a2, c in segs:
            ic.path(sector(cx, cy, ro, ri, a1 + 0.8, a2 - 0.8), fill=GNOME_COLOURS[c], opacity=1 - depth * 0.2)
    ic.circle(cx, cy, 56, fill=ic.lin([(0, "#fff", 0.25), (0.5, "#fff", 0), (1, "#000", 0.08)], 0, 0, 1, 1))
    # the clip
    ic.rect(98, 26, 60, 26, rx=6, fill="#000", opacity=0.3, transform="translate(2 3)")
    ic.rect(98, 26, 60, 26, rx=6, fill=steel(ic, False))
    ic.rect(108, 20, 40, 12, rx=6, fill="none", stroke="#AEB6BF", stroke_width=4)
    ic.rect(100, 27.5, 56, 1.6, rx=0.8, fill="#fff", opacity=0.7)
    for x in (110, 146):
        screw(ic, x, 42, 2.4)
    # the loupe over the chart's edge
    lx, ly = 174, 176
    ic.line(lx + 16, ly + 16, lx + 38, ly + 38, stroke="#000", stroke_width=12, stroke_linecap="round",
            opacity=0.3, transform="translate(2 3)")
    ic.line(lx + 16, ly + 16, lx + 38, ly + 38, stroke="#2A2C30", stroke_width=11, stroke_linecap="round")
    ic.line(lx + 18, ly + 18, lx + 36, ly + 36, stroke="#5A5E66", stroke_width=3, stroke_linecap="round")
    ic.circle(lx, ly, 26, fill="#fff", opacity=0.25)
    view = ic.clip(f'<circle cx="{lx}" cy="{ly}" r="24"/>')
    with ic.g(clip_path=view):
        with ic.g(transform=f"translate({lx} {ly}) scale(1.6) translate({-lx} {-ly})"):
            for ri, ro, segs in rings:
                for a1, a2, c in segs:
                    ic.path(sector(cx, cy, ro, ri, a1 + 0.8, a2 - 0.8), fill=GNOME_COLOURS[c])
    ic.circle(lx, ly, 24, fill=glare(ic, 1.4))
    ic.circle(lx, ly, 25, fill="none", stroke=ic.lin([(0, "#6A6E76"), (1, "#1E2024")], 0, 0, 1, 1), stroke_width=5)
    ic.path(f"M{lx - 20} {ly - 6}a21 21 0 0 1 14-14", fill="none", stroke="#fff", stroke_width=2,
            stroke_linecap="round", opacity=0.7)


@small("baobab")
def baobab16(ic):
    tile(ic, "#7C4A70", "#331830")
    ic.rect(3, 2, 10, 12.5, rx=1, fill="#A87A4A")
    ic.rect(3.8, 3.2, 8.4, 10.6, fill="#FFFFFF")
    ic.path(sector(8, 8.6, 3.8, 1.4, 0, 120), fill="#3584E4")
    ic.path(sector(8, 8.6, 3.8, 1.4, 120, 220), fill="#33D17A")
    ic.path(sector(8, 8.6, 3.8, 1.4, 220, 300), fill="#F6D32D")
    ic.path(sector(8, 8.6, 3.8, 1.4, 300, 360), fill="#FF7800")
    ic.rect(6, 1.4, 4, 1.8, rx=0.6, fill="#AEB6BF")


# --- Backups (Deja Dup): a safe, a clock for its dial, an arrow turning back

@icon("deja-dup", kind="app", names=["deja-dup", "org.gnome.DejaDup"], title="Backups")
def deja_dup(ic):
    tile(ic, "#4C7158", "#1A2E21")
    shadow(ic, 124, 212, 96, 12)
    # the safe: its body, its right side, its feet
    for x in (54, 178):
        ic.rect(x, 200, 22, 10, rx=2, fill="#1A1C20")
    ic.poly([(196, 40), (212, 30), (212, 190), (196, 204)], fill=ic.lin([(0, "#3E434A"), (1, "#16181B")]))
    ic.poly([(44, 40), (196, 40), (212, 30), (60, 30)], fill=ic.lin([(0, "#7A818A"), (1, "#4A5058")]))
    ic.rect(44, 40, 152, 164, rx=8, fill=ic.lin([(0, "#5C636C"), (0.5, "#3A3F46"), (1, "#22262B")], 0, 0, 1, 1))
    ic.rect(44.75, 40.75, 150.5, 162.5, rx=7.25, fill="none", stroke="#fff", stroke_width=1.5, opacity=0.2)
    # the door, its hinges at the left
    ic.rect(56, 52, 128, 140, rx=6, fill="#15171A")
    ic.rect(58, 54, 124, 136, rx=5, fill=ic.lin([(0, "#6E757E"), (0.5, "#454B53"), (1, "#2A2E34")], 0, 0, 1, 1))
    ic.rect(59, 55, 122, 1.5, rx=0.7, fill="#fff", opacity=0.35)
    for y in (68, 160):
        ic.rect(50, y, 10, 22, rx=3, fill=steel(ic))
    for x, y in ((66, 62), (174, 62), (66, 182), (174, 182)):
        rivet(ic, x, y, 2.4)
    # the dial: a clock, in brass, and the arrow turning back round it
    cx, cy = 120, 108
    ic.path(sector(cx, cy, 46, 40, 210, 520), fill="#3DDC84", opacity=0.95)
    tip = [polar(cx, cy, 51, 210), polar(cx, cy, 35, 210), polar(cx, cy, 43, 190)]
    ic.poly(tip, fill="#3DDC84")
    ic.circle(cx + 2, cy + 3, 34, fill="#000", opacity=0.35)
    ic.circle(cx, cy, 34, fill=brass(ic))
    ic.circle(cx, cy, 27, fill=ic.rad([(0, "#FFFDF7"), (1, "#E2D8C2")], cx=0.45, cy=0.4, r=0.65))
    for h in range(12):
        x1, y1 = polar(cx, cy, 25, h * 30)
        x2, y2 = polar(cx, cy, 21 if h % 3 == 0 else 23, h * 30)
        ic.line(x1, y1, x2, y2, stroke="#2A2C30", stroke_width=1.8 if h % 3 == 0 else 0.8)
    ic.text("12", cx, cy - 11, 6.5, font="sans-semibold", anchor="middle", fill="#2A2C30")
    ic.line(cx, cy, *polar(cx, cy, 13, 285), stroke="#23262B", stroke_width=2.6, stroke_linecap="round")
    ic.line(cx, cy, *polar(cx, cy, 19, 0), stroke="#23262B", stroke_width=1.8, stroke_linecap="round")
    ic.circle(cx, cy, 2.6, fill=brass(ic))
    ic.path(f"M{cx - 30} {cy - 8}a31 31 0 0 1 22-24 34 34 0 0 0-22 24z", fill="#fff", opacity=0.6)
    # the handle: three spokes
    hx, hy = 150, 162
    for a in (20, 140, 260):
        x, y = polar(hx, hy, 16, a)
        ic.line(hx, hy, x, y, stroke="#1A1C20", stroke_width=5, stroke_linecap="round", transform="translate(1 2)")
        ic.line(hx, hy, x, y, stroke=steel(ic, False), stroke_width=4, stroke_linecap="round")
        ic.circle(x, y, 4, fill=ic.rad([(0, "#F4F6F8"), (1, "#8A929C")], cx=0.35, cy=0.3, r=0.8))
    ic.circle(hx, hy, 7, fill=brass(ic))
    # the maker's plate
    ic.rect(70, 164, 50, 16, rx=2, fill=brass(ic, 0, 0, 0, 1))
    ic.text("DÉJÀ DUP", 95, 175, 7, font="mono-semibold", anchor="middle", spacing=0.6, fill="#4A3410")


@small("deja-dup")
def deja_dup16(ic):
    tile(ic, "#4C7158", "#1A2E21")
    ic.rect(2.5, 2.5, 11, 11.5, rx=1, fill="#454B53")
    ic.rect(3.5, 3.5, 9, 9.5, rx=0.6, fill="#5C636C")
    ic.path(sector(7.4, 7.4, 4, 3.1, 210, 500), fill="#3DDC84")
    ic.circle(7.4, 7.4, 2.6, fill="#E9DDC0")
    ic.path("M7.4 7.4V5.6M7.4 7.4l-1 .6", stroke="#23262B", stroke_width=0.6)
    ic.circle(11, 11.2, 1, fill="#AEB6BF")


# --- Pika Backup: a pika sitting on a stack of backup drives --------------

def drive(ic, x, y, w, h, n, used):
    ic.rect(x + 2, y + 3, w, h, rx=6, fill="#000", opacity=0.3)
    ic.rect(x, y, w, h, rx=6, fill=ic.lin([(0, "#4A5058"), (1, "#1E2125")]))
    ic.rect(x + 0.75, y + 0.75, w - 1.5, h - 1.5, rx=5.25, fill="none", stroke="#fff", stroke_width=1.2,
            opacity=0.18)
    ic.rect(x + 8, y + 7, w - 16, h - 14, rx=3, fill="#16181B")
    ic.text(f"BACKUP {n}", x + 14, y + h / 2 + 2.5, 7, font="mono-semibold", spacing=1, fill="#AEB6BF")
    ic.rect(x + w - 54, y + h / 2 - 2.5, 30, 5, rx=2.5, fill="#2E3238")
    ic.rect(x + w - 54, y + h / 2 - 2.5, 30 * used, 5, rx=2.5, fill="#F5A447")
    ic.circle(x + w - 15, y + h / 2, 2.6, fill="#5CC8FF")
    ic.circle(x + w - 15, y + h / 2, 4.5, fill="#5CC8FF", opacity=0.25)


@icon("pika-backup", kind="app", names=["org.gnome.World.PikaBackup", "pika-backup"], title="Pika Backup")
def pika_backup(ic):
    tile(ic, "#4A84B8", "#1B3B60")
    shadow(ic, 128, 212, 96, 12)
    drive(ic, 36, 172, 184, 34, 1, 0.8)
    drive(ic, 44, 140, 172, 32, 2, 0.55)
    drive(ic, 40, 108, 178, 32, 3, 0.3)
    # the pika: a round tan body, round ears, sitting on top
    with ic.g(transform="translate(124 106) scale(1.12) translate(-124 -106)"):
        fur = ic.rad([(0, "#E8B47A"), (0.6, "#C28048"), (1, "#8A5224")], cx=0.4, cy=0.3, r=0.8)
        ic.ellipse(128, 106, 46, 6, fill="#000", opacity=0.35)
        for x, y in ((104, 52), (138, 46)):
            ic.circle(x, y, 13, fill="#8A5224")
            ic.circle(x - 1, y - 1, 12, fill=fur)
            ic.circle(x, y + 1, 7, fill="#E8A49A")
        ic.path("M76 104C70 74 92 52 124 52C156 52 178 74 172 104Z", fill=fur)
        ic.path("M92 104C92 86 104 76 120 76C136 76 148 86 148 104Z", fill="#F4DCB8", opacity=0.85)
        for x in (110, 140):
            ic.ellipse(x, 104, 9, 4, fill="#C28048")
            ic.ellipse(x, 103, 8, 3, fill="#E8B47A")
        ic.circle(132, 72, 4.6, fill="#1E120A")
        ic.circle(133.4, 70.6, 1.5, fill="#fff")
        ic.circle(108, 74, 4.6, fill="#1E120A")
        ic.circle(109.4, 72.6, 1.5, fill="#fff")
        ic.ellipse(120, 82, 3.6, 2.6, fill="#4A2A18")
        ic.path("M120 84.5v3M116 88q4 3 8 0", fill="none", stroke="#4A2A18", stroke_width=1.2, stroke_linecap="round")
        for k in (-1, 1):
            ic.path(f"M{120 + k * 6} 84l{k * 16} -3M{120 + k * 6} 86l{k * 16} 2", fill="none", stroke="#5A3A20",
                    stroke_width=0.7, opacity=0.6)
        ic.circle(100, 82, 4, fill="#F09A8A", opacity=0.45)
        ic.circle(140, 82, 4, fill="#F09A8A", opacity=0.45)
        ic.path("M84 92C82 72 98 58 116 56", fill="none", stroke="#FFE2B8", stroke_width=2, stroke_linecap="round",
                opacity=0.5)


@small("pika-backup")
def pika_backup16(ic):
    tile(ic, "#4A84B8", "#1B3B60")
    for y in (8.4, 11.2):
        ic.rect(2, y, 12, 2.6, rx=0.6, fill="#2E3238")
        ic.circle(12.4, y + 1.3, 0.5, fill="#5CC8FF")
    ic.circle(5.8, 3.4, 1.3, fill="#A86A34")
    ic.circle(9.8, 3, 1.3, fill="#A86A34")
    ic.path("M4.2 8.4C3.6 5.4 5.4 3.4 8 3.4S12.4 5.4 11.8 8.4Z", fill="#D69A5E")
    ic.circle(9.2, 5.6, 0.55, fill="#1E120A")
    ic.circle(6.6, 5.6, 0.55, fill="#1E120A")


# --- Vorta: backup tape cartridges, the archive's label on the front ----------

def _cartridge(ic, x, y, w, h, shell, edge):
    """An LTO-style cartridge's shell, seen from the front, its door corner
    cut at the top right and its depth showing below and to the right."""
    c = 18
    d = (f"M{x + 6} {y}H{x + w - c}L{x + w} {y + c}V{y + h - 6}a6 6 0 0 1-6 6H{x + 6}a6 6 0 0 1-6-6V{y + 6}"
         f"a6 6 0 0 1 6-6z")
    ic.path(d, fill="#000", opacity=0.35, transform="translate(6 16)")
    ic.path(d, fill=edge, transform="translate(4 12)")
    for k in range(int(x) + 12, int(x + w) - 6, 6):
        ic.line(k, y + h + 3, k, y + h + 10, stroke="#fff", stroke_opacity=0.12, stroke_width=1.6)
    ic.path(d, fill=shell)
    ic.path(f"M{x + 1} {y + h - 8}V{y + 6}a5 5 0 0 1 5-5H{x + w - c}", fill="none", stroke="#fff",
            stroke_opacity=0.35, stroke_width=1.5)
    # the leader-pin door across the cut corner
    ic.path(f"M{x + w - c - 8} {y}L{x + w} {y + c + 8}", stroke="#000", stroke_opacity=0.35, stroke_width=1.5)
    ic.path(f"M{x + w - c - 7} {y + 1.5}L{x + w - 1.5} {y + c + 7}", stroke="#fff", stroke_opacity=0.2)
    # the grip, ribbed, along the left
    for k in range(6):
        ic.rect(x + 5, y + 22 + k * 6, 6, 2.4, rx=1, fill="#000", opacity=0.3)
        ic.rect(x + 5, y + 21 + k * 6, 6, 1.2, rx=0.6, fill="#fff", opacity=0.2)


@icon("vorta", kind="app", names=["com.borgbase.Vorta", "vorta", "vorta32"], title="Vorta")
def vorta(ic):
    tile(ic, "#2F4C80", "#101C38")
    shadow(ic, 124, 214, 98, 11)
    # the one behind, an older backup, standing a little askew
    with ic.g(transform="rotate(9 170 110)"):
        _cartridge(ic, 104, 34, 118, 124, ic.lin([(0, "#7C8DA6"), (1, "#45546C")], 0, 0, 1, 1), "#2A3446")
        ic.rect(122, 38, 74, 19, rx=2, fill=paper(ic, "cream"))
        ic.rect(122, 38, 74, 5, rx=2, fill="#2F5DB8")
        ic.text("2026-10-23", 127, 53, 8, font="mono-semibold", fill="#3A4250")
    with ic.g(transform="translate(0 -12)"):
        # the front one
        x, y, w, h = 36, 70, 154, 136
        _cartridge(ic, x, y, w, h, ic.lin([(0, "#97A6BC"), (0.5, "#6F809A"), (1, "#45546C")], 0, 0, 1, 1), "#262F3F")
        # the label, its band in Vorta's blue
        lx, ly = 58, 82
        ic.rect(lx + 1, ly + 2, 108, 56, rx=2, fill="#000", opacity=0.25)
        ic.rect(lx, ly, 108, 56, rx=2, fill=paper(ic, "white"))
        ic.rect(lx, ly, 108, 16, rx=2, fill=ic.lin([(0, "#3E72D6"), (1, "#1F4A9E")]))
        ic.rect(lx, ly + 12, 108, 4, fill="#1F4A9E")
        ic.path(f"M{lx + 7} {ly + 4}L{lx + 11.5} {ly + 12}L{lx + 16} {ly + 4}", fill="none", stroke="#F2F5F8",
                stroke_width=2.2, stroke_linecap="round", stroke_linejoin="round")
        ic.text("VORTA", lx + 22, ly + 12.5, 11, font="sans-bold", spacing=1.6, fill="#F2F5F8")
        ic.text("borg archive", lx + 7, ly + 28, 8, font="mono-semibold", fill="#2A3446")
        ic.text("2026-10-30", lx + 7, ly + 38, 8, font="mono-semibold", fill="#2A3446")
        # its barcode
        bx = lx + 7
        for k, bw in enumerate((1.2, 0.6, 0.6, 1.8, 0.6, 1.2, 0.6, 0.6, 1.8, 1.2, 0.6, 1.2, 0.6, 1.8, 0.6, 0.6, 1.2,
                                0.6, 1.8, 0.6, 1.2, 0.6, 0.6, 1.2, 1.8, 0.6, 0.6, 1.2)):
            if k % 2 == 0:
                ic.rect(bx, ly + 42, bw, 9, fill="#2A3446")
            bx += bw + 0.9
        ic.text("V00030L9", lx + 101, ly + 50, 6, font="mono", anchor="end", fill="#5A6370")
        # the window on the reel: tape wound on its hub
        wx, wy = 72, 166
        ic.rect(wx - 22, wy - 18, 44, 32, rx=6, fill="#1B222E")
        win = ic.clip(f'<rect x="{wx - 20}" y="{wy - 16}" width="40" height="28" rx="5"/>')
        with ic.g(clip_path=win):
            ic.rect(wx - 20, wy - 16, 40, 28, fill="#0E131B")
            ic.circle(wx + 6, wy + 10, 30, fill=ic.rad([(0, "#3A2618"), (0.55, "#6E4A2C"), (1, "#2A1A10")],
                                                       cx=0.4, cy=0.35, r=0.7))
            for r in (14, 20, 26):
                ic.circle(wx + 6, wy + 10, r, fill="none", stroke="#C08A5A", stroke_opacity=0.35, stroke_width=0.8)
            ic.circle(wx + 6, wy + 10, 10, fill="#C9D0D8")
            ic.circle(wx + 6, wy + 10, 4, fill="#3A4250")
            ic.rect(wx - 20, wy - 16, 40, 28, fill=glare(ic, 1.4))
        ic.path(f"M{wx - 16} {wy - 13}h18l-14 20", fill="#fff", opacity=0.12)
        # the write-protect tab, slid to locked
        tx, ty = 150, 160
        ic.rect(tx, ty, 30, 16, rx=3, fill="#1B222E")
        ic.rect(tx + 14, ty + 2, 14, 12, rx=2, fill=ic.lin([(0, "#F27B5A"), (1, "#B83A22")]))
        ic.rect(tx + 15, ty + 3, 12, 1.2, rx=0.6, fill="#fff", opacity=0.5)
        ic.path(f"M{tx + 18} {ty + 9.5}h6v3h-6zM{tx + 19} {ty + 9.5}v-1.5a2 2 0 0 1 4 0v1.5", fill="none",
                stroke="#FFF4EE", stroke_width=1)
        ic.text("SAFE", tx + 15, ty + 26, 6, font="mono-semibold", anchor="middle", spacing=1, fill="#20283A")
        # the screws
        for sx, sy in ((106, 196), (172, 196)):
            ic.circle(sx + 0.5, sy + 0.8, 2.6, fill="#1B222E", opacity=0.6)
            ic.circle(sx, sy, 2.6, fill=steel(ic, False))
            ic.line(sx - 1.6, sy, sx + 1.6, sy, stroke="#3A4250", stroke_width=0.8)


@small("vorta")
def vorta16(ic):
    tile(ic, "#2F4C80", "#101C38")
    ic.rect(6.6, 1.4, 8, 8.4, rx=0.7, fill="#4F5E78")
    ic.rect(1.6, 4.2, 11, 10.4, rx=0.8, fill="#262F3F")
    ic.rect(1.6, 4.2, 11, 8, rx=0.8, fill="#8090A8")
    ic.rect(3, 5.4, 8.2, 3.6, rx=0.3, fill="#F7F7F4")
    ic.rect(3, 5.4, 8.2, 1.4, fill="#2F5DB8")
    ic.circle(4.6, 10.6, 1.1, fill="#6E4A2C")
    ic.rect(8.8, 10, 2.4, 1.3, rx=0.3, fill="#E0563A")
