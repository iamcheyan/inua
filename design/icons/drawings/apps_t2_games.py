"""The inua-objects theme, games and emulators (t2-games): Prism Launcher,
Minecraft, RetroArch, Dolphin, PCSX2, PPSSPP, Ryujinx, itch, 0 A.D.,
SuperTuxKart, Battle for Wesnoth (docs/feat/object-icons.md, Part 2). Each
is its own object in the brand's colours with its mark redrawn, simplified;
inua's own games and Steam (a wheel), Lutris (a token), Heroic (a heater
shield) and Moonlight (a gamepad) are not repeated."""

import math
import random

from lib import (brass, glare, graphite, icon, paper, polar, shadow, small, steel, tile, wood)


# --- shared parts ----------------------------------------------------------

def _f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def _pixels(ic, cells, transform, **kw):
    """Unit squares, one path per colour: cells is {(i, j): colour}."""
    by = {}
    for (i, j), c in cells.items():
        by.setdefault(c, []).append(f"M{i} {j}h1v1h-1z")
    for c, ds in by.items():
        ic.path("".join(ds), fill=c, transform=transform, **kw)


GRASS = ["#7CC24A", "#6DB33F", "#5E9E34", "#8AD055", "#5A9530"]
DIRT = ["#8B5A2B", "#7A4E24", "#9C6A38", "#6A4220", "#A57444"]
SIDE_GRASS = ["#6DB33F", "#5E9E34", "#7CC24A"]


def grass_block(ic, x, y, w, h, n, seed=3):
    """An isometric grass block of n by n voxels a face: (x, y) its top
    face's left corner, w its half-width, h its sides' height."""
    rnd = random.Random(seed)
    top = f"matrix({_f(w / n)} {_f(-w / 2 / n)} {_f(w / n)} {_f(w / 2 / n)} {_f(x)} {_f(y)})"
    left = f"matrix({_f(w / n)} {_f(w / 2 / n)} 0 {_f(h / n)} {_f(x)} {_f(y)})"
    right = f"matrix({_f(w / n)} {_f(-w / 2 / n)} 0 {_f(h / n)} {_f(x + w)} {_f(y + w / 2)})"
    fx, fy = x + w, y + w / 2  # the front corner
    face_top = [(x, y), (x + w, y - w / 2), (x + 2 * w, y), (fx, fy)]
    face_left = [(x, y), (fx, fy), (fx, fy + h), (x, y + h)]
    face_right = [(fx, fy), (x + 2 * w, y), (x + 2 * w, y + h), (fx, fy + h)]
    ic.poly(face_top, fill="#6DB33F")
    ic.poly(face_left, fill="#7A4E24")
    ic.poly(face_right, fill="#7A4E24")
    _pixels(ic, {(i, j): rnd.choice(GRASS) for i in range(n) for j in range(n)}, top)
    for tf in (left, right):
        cells = {}
        depth = [1 + (rnd.random() < 0.55) + (rnd.random() < 0.18) for _ in range(n)]
        for i in range(n):
            for j in range(n):
                cells[(i, j)] = rnd.choice(SIDE_GRASS) if j < depth[i] else rnd.choice(DIRT)
        _pixels(ic, cells, tf)
    # light from the top left: the right face in shade, the left a little
    ic.poly(face_left, fill="#000", opacity=0.12)
    ic.poly(face_right, fill="#000", opacity=0.34)
    ic.poly(face_top, fill=ic.lin([(0, "#fff", 0.16), (1, "#fff", 0)], 0, 0, 1, 1))
    ic.path(f"M{_f(x)} {_f(y + h)}V{_f(y)}L{_f(x + w)} {_f(y - w / 2)}L{_f(x + 2 * w)} {_f(y)}V{_f(y + h)}"
            f"L{_f(fx)} {_f(fy + h)}Z", fill="none", stroke="#1E2A10", stroke_opacity=0.45, stroke_width=1.2,
            stroke_linejoin="round")
    ic.path(f"M{_f(x + 1)} {_f(y)}L{_f(x + w)} {_f(y - w / 2 + 0.6)}L{_f(x + 2 * w - 1)} {_f(y)}", fill="none",
            stroke="#fff", stroke_opacity=0.5, stroke_width=1.2)
    ic.line(fx, fy + 0.8, fx, fy + h - 1, stroke="#fff", stroke_opacity=0.18, stroke_width=1)


def tube(pts, widths, side=0):
    """A band along a centre line of points, its width at each; side 0 the
    whole band, 1 only its outer half (left of travel), -1 its inner."""
    a, b = [], []
    for k, ((x, y), w) in enumerate(zip(pts, widths)):
        x0, y0 = pts[max(0, k - 1)]
        x1, y1 = pts[min(len(pts) - 1, k + 1)]
        dx, dy = x1 - x0, y1 - y0
        d = math.hypot(dx, dy) or 1
        nx, ny = dy / d, -dx / d
        lo, hi = (-w / 2, w / 2) if side == 0 else ((0, w / 2) if side > 0 else (-w / 2, 0))
        a.append((x + nx * hi, y + ny * hi))
        b.append((x + nx * lo, y + ny * lo))
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in a + b[::-1]) + "Z"


def disc(ic, cx, cy, r, under="#C9CED6", hub="#EEF1F4"):
    """An optical disc face on: its rainbow sheen, clear hub and hole."""
    ic.circle(cx + 2, cy + 4, r, fill="#000", opacity=0.3)
    ic.circle(cx, cy, r, fill=ic.rad([(0, "#F4F6F8"), (0.6, under), (1, "#8A929C")], cx=0.4, cy=0.35, r=0.75))
    for a, c in ((20, "#FF8AD8"), (60, "#7FE3FF"), (110, "#FFE58A"), (200, "#FF8AD8"), (240, "#7FE3FF"),
                 (290, "#FFE58A")):
        x1, y1 = polar(cx, cy, r - 2, a - 12)
        x2, y2 = polar(cx, cy, r - 2, a + 12)
        ic.path(f"M{cx} {cy}L{x1:.1f} {y1:.1f}A{r - 2} {r - 2} 0 0 1 {x2:.1f} {y2:.1f}Z", fill=c, opacity=0.28)
    ic.circle(cx, cy, r, fill="none", stroke="#fff", stroke_opacity=0.7, stroke_width=1.2)
    ic.circle(cx, cy, r * 0.3, fill=hub, opacity=0.9)
    ic.circle(cx, cy, r * 0.3, fill="none", stroke="#000", stroke_opacity=0.12)
    ic.circle(cx, cy, r * 0.12, fill="#000", opacity=0.55)
    ic.circle(cx, cy, r * 0.12, fill="none", stroke="#fff", stroke_opacity=0.5, stroke_width=0.8)


def bevel(ic, d, fill, edge="#000", lift=(2, 4), hi=0.18, **kw):
    """A part with its shadow under it, its face and a light rim."""
    ic.path(d, fill=edge, opacity=0.35, transform=f"translate({lift[0]} {lift[1]})")
    ic.path(d, fill=fill, **kw)
    ic.path(d, fill="none", stroke="#fff", stroke_opacity=hi, stroke_width=1.4)


def dpad(ic, cx, cy, arm, wide, fill="#25232C"):
    a, w = arm, wide / 2
    d = (f"M{cx - w} {cy - a}h{2 * w}v{a - w}h{a - w}v{2 * w}h{w - a}v{a - w}h{-2 * w}v{w - a}h{w - a}"
         f"v{-2 * w}h{a - w}z")
    ic.path(d, fill="#000", opacity=0.45, transform="translate(1 2)")
    ic.path(d, fill=fill)
    ic.path(d, fill="none", stroke="#fff", stroke_opacity=0.16)
    ic.circle(cx, cy, w * 0.5, fill="#000", opacity=0.3)


def button(ic, x, y, r, light, dark):
    ic.circle(x + 0.8, y + 1.8, r, fill="#000", opacity=0.45)
    ic.circle(x, y, r, fill=ic.rad([(0, light), (1, dark)], cx=0.38, cy=0.32, r=0.75))
    ic.circle(x - r * 0.25, y - r * 0.3, r * 0.35, fill="#fff", opacity=0.3)


INVADER = ["..X.....X..",
           "...X...X...",
           "..XXXXXXX..",
           ".XX.XXX.XX.",
           "XXXXXXXXXXX",
           "X.XXXXXXX.X",
           "X.X.....X.X",
           "...XX.XX..."]


def invader(ic, x, y, s, **kw):
    d = "".join(f"M{i} {j}h1v1h-1z" for j, row in enumerate(INVADER) for i, c in enumerate(row) if c == "X")
    ic.path(d, transform=f"translate({_f(x)} {_f(y)}) scale({_f(s)})", **kw)


# --- Prism Launcher: a glass prism splitting light onto a grass block --------

PRISM = ["#99CD61", "#6CC0B0", "#4D9DE0", "#9E7BD8", "#E8686A", "#F4A35E"]


@icon("prismlauncher", kind="app", names=["org.prismlauncher.PrismLauncher", "prismlauncher"],
      title="Prism Launcher")
def prismlauncher(ic):
    tile(ic, "#24345A", "#0D1428")
    shadow(ic, 150, 212, 76, 11)
    grass_block(ic, 96, 150, 58, 40, 8, seed=5)
    ax, ay, lx, ly, rx_, ry = 94, 30, 46, 116, 142, 116
    # the rainbow, out of the prism's right face onto the block's top
    ox, oy = (ax + rx_) / 2 + 2, (ay + ry) / 2
    for k, c in enumerate(["#E8686A", "#F4A35E", "#F6D86A", "#99CD61", "#4D9DE0", "#9E7BD8"]):
        ex, ey = 132 + k * 12, 146 - k * 3.2
        ic.poly([(ox + k * 1.4, oy + k * 2.4), (ox + k * 1.4 + 1, oy + k * 2.4 + 3), (ex + 14, ey + 3), (ex, ey)],
                fill=c, opacity=0.75)
    ic.ellipse(168, 144, 40, 13, fill=ic.rad([(0, "#fff", 0.45), (1, "#fff", 0)]), transform="rotate(-10 168 144)")
    # the white beam, from the top left into the left face
    lmx, lmy = (ax + lx) / 2, (ay + ly) / 2
    ic.poly([(0, 30), (0, 40), (lmx + 1, lmy + 4), (lmx - 1, lmy - 4)],
            fill=ic.lin([(0, "#fff", 0), (1, "#fff", 0.95)], 0, 0, 1, 1))
    # the prism: its depth behind, then the faceted glass face
    ic.poly([(ax, ay), (ax + 10, ay - 7), (rx_ + 10, ry - 7), (rx_, ry)], fill="#9FC3EA", opacity=0.5)
    ic.poly([(ax, ay), (ax + 10, ay - 7), (rx_ + 10, ry - 7), (rx_, ry)], fill="none", stroke="#fff",
            stroke_opacity=0.55, stroke_linejoin="round")
    gx, gy = (ax + lx + rx_) / 3, (ay + ly + ry) / 3
    pts = [(ax, ay), ((ax + rx_) / 2, (ay + ry) / 2), (rx_, ry), ((lx + rx_) / 2, ly), (lx, ly),
           ((ax + lx) / 2, (ay + ly) / 2)]
    ic.poly([(ax + 3, ay + 5), (rx_ + 3, ry + 5), (lx + 3, ly + 5)], fill="#000", opacity=0.3)
    for k, c in enumerate(PRISM):
        p1, p2 = pts[k], pts[(k + 1) % 6]
        ic.poly([(gx, gy), p1, p2], fill=c, opacity=0.88)
    for q in pts:
        ic.line(gx, gy, q[0], q[1], stroke="#fff", stroke_opacity=0.4, stroke_width=0.8)
    ic.poly([(ax, ay), (rx_, ry), (lx, ly)], fill=glare(ic, 1.6))
    ic.poly([(ax, ay), (rx_, ry), (lx, ly)], fill="none", stroke="#fff", stroke_opacity=0.85, stroke_width=1.8,
            stroke_linejoin="round")
    ic.path(f"M{ax - 4} {ay + 14}L{lx + 8} {ly - 12}", stroke="#fff", stroke_opacity=0.7, stroke_width=2,
            stroke_linecap="round")


@small("prismlauncher")
def prismlauncher16(ic):
    tile(ic, "#24345A", "#0D1428")
    ic.poly([(7, 10.5), (10.5, 8.8), (14, 10.5), (10.5, 12.2)], fill="#7CC24A")
    ic.poly([(7, 10.5), (10.5, 12.2), (10.5, 15), (7, 13.3)], fill="#7A4E24")
    ic.poly([(10.5, 12.2), (14, 10.5), (14, 13.3), (10.5, 15)], fill="#5A3A1A")
    ic.poly([(8, 7), (10, 7), (12.5, 10), (11.5, 10.6)], fill="#F6D86A", opacity=0.8)
    ic.poly([(5, 1.5), (8.8, 8.2), (1.2, 8.2)], fill="#4D9DE0")
    ic.poly([(5, 1.5), (8.8, 8.2), (5, 6)], fill="#99CD61")
    ic.poly([(1.2, 8.2), (5, 6), (8.8, 8.2)], fill="#E8686A")


# --- Minecraft: a grass block, voxel by voxel ------------------------------

@icon("minecraft", kind="app", names=["ch.tlaun.TL", "com.mojang.Minecraft", "com.thebrokenrail.MCPIReborn",
                                      "legacylauncher", "minecraft", "minecraft-launcher", "minecraft-pi",
                                      "ru.turikhay.tlauncher"], title="Minecraft")
def minecraft(ic):
    tile(ic, "#82BCEB", "#3874AA")
    for x, y, w in ((30, 46, 34), (178, 28, 28), (200, 60, 18)):
        ic.rect(x, y, w, 8, fill="#fff", opacity=0.55)
        ic.rect(x + 6, y - 6, w - 14, 6, fill="#fff", opacity=0.55)
    shadow(ic, 128, 214, 92, 12)
    grass_block(ic, 44, 82, 84, 92, 16, seed=11)


@small("minecraft")
def minecraft16(ic):
    tile(ic, "#82BCEB", "#3874AA")
    ic.poly([(2, 5), (8, 2), (14, 5), (8, 8)], fill="#7CC24A")
    ic.poly([(2, 5), (8, 8), (8, 14.5), (2, 11.5)], fill="#8B5A2B")
    ic.poly([(8, 8), (14, 5), (14, 11.5), (8, 14.5)], fill="#5E3C1C")
    ic.poly([(2, 5), (8, 8), (8, 9.6), (2, 6.6)], fill="#5E9E34")
    ic.poly([(8, 8), (14, 5), (14, 6.6), (8, 9.6)], fill="#4A7E28")
    ic.rect(4, 4.6, 1, 0.8, fill="#5E9E34")
    ic.rect(9, 3.6, 1, 0.8, fill="#9AD866")


# --- RetroArch: a retro handheld, the space invader on its screen -----------

@icon("retroarch", kind="app", names=["appimagekit-retroarch", "org.libretro.RetroArch", "retroarch"],
      title="RetroArch")
def retroarch(ic):
    tile(ic, "#5E4590", "#271746")
    shadow(ic, 128, 216, 78, 11)
    body = "M74 22H182a12 12 0 0 1 12 12V174a40 40 0 0 1-40 40H74a12 12 0 0 1-12-12V34a12 12 0 0 1 12-12Z"
    ic.path(body, fill="#6E6A62", transform="translate(3 4)")
    ic.path(body, fill=ic.lin([(0, "#EEEBE4"), (0.6, "#D3CFC6"), (1, "#ABA69B")], 0, 0, 1, 1))
    ic.path(body, fill="none", stroke="#fff", stroke_opacity=0.7, stroke_width=1.5)
    ic.line(76, 30, 180, 30, stroke="#000", stroke_opacity=0.1)
    ic.text("OFF·ON", 80, 29, 5, font="mono-semibold", spacing=0.6, fill="#8A857B")
    # the screen in its bezel
    bez = "M80 38H176a6 6 0 0 1 6 6V112a18 18 0 0 1-18 18H80a6 6 0 0 1-6-6V44a6 6 0 0 1 6-6Z"
    ic.path(bez, fill=ic.lin([(0, "#4A4658"), (1, "#2C2937")]))
    ic.path(bez, fill="none", stroke="#000", stroke_opacity=0.3, stroke_width=1.2)
    ic.rect(95, 47, 74, 66, rx=3, fill=ic.rad([(0, "#22305A"), (1, "#0B1022")], cx=0.45, cy=0.45, r=0.7))
    ic.circle(132, 80, 30, fill=ic.rad([(0, "#5E7CFF", 0.45), (1, "#5E7CFF", 0)]))
    invader(ic, 105, 62, 5, fill="#EEF0FF")
    ic.rect(95, 47, 74, 66, rx=3, fill=glare(ic, 1.3))
    ic.circle(85, 70, 2.6, fill="#E8463C")
    ic.circle(85, 70, 4.5, fill="#E8463C", opacity=0.25)
    ic.text("BATTERY", 85, 80, 3.6, font="mono-semibold", anchor="middle", fill="#8E8AA0")
    ic.text("RetroArch", 76, 146, 13, font="sans-bold", fill="#3B3360")
    ic.text("LIBRETRO", 146, 146, 6, font="mono-semibold", spacing=1, fill="#7A7468")
    # the controls
    dpad(ic, 96, 178, 17, 11)
    button(ic, 170, 166, 9.5, "#C24A86", "#7E1E50")
    button(ic, 148, 178, 9.5, "#C24A86", "#7E1E50")
    ic.text("B", 148, 196, 6, font="sans-bold", anchor="middle", fill="#5A4F78")
    ic.text("A", 170, 184, 6, font="sans-bold", anchor="middle", fill="#5A4F78")
    for x in (108, 130):
        ic.rect(x, 198, 16, 5, rx=2.5, fill="#55525E", transform=f"rotate(-24 {x + 8} 200)")
    for k in range(4):
        x0, y0 = 160 + k * 6.5, 206
        ic.line(x0, y0 - k * 2.5, x0 + 6, y0 - 12 - k * 2.5, stroke="#7A7468", stroke_width=2.2,
                stroke_linecap="round", opacity=0.75)


@small("retroarch")
def retroarch16(ic):
    tile(ic, "#5E4590", "#271746")
    ic.path("M4.5 1.5h7a1 1 0 0 1 1 1V12a2.5 2.5 0 0 1-2.5 2.5H4.5a1 1 0 0 1-1-1V2.5a1 1 0 0 1 1-1z",
            fill="#E2DED6")
    ic.rect(4.5, 2.5, 7, 5.5, rx=0.6, fill="#1C2448")
    ic.path("M6 4h1v1h-1zM9 4h1v1h-1zM5.5 5h5v1.6h-5zM5.5 6.6h1v.8h-1zM9.5 6.6h1v.8h-1z", fill="#EEF0FF")
    ic.path("M5 10.6h3M6.5 9.1v3", stroke="#2A2833", stroke_width=1)
    ic.circle(10.6, 10.4, 0.9, fill="#B0306A")
    ic.circle(9.2, 11.6, 0.9, fill="#B0306A")


# --- Dolphin: a blue dolphin leaping over a game disc -----------------------

DOLPHIN = ("M58 150C58 98 86 56 132 48C166 42 194 58 204 86C208 98 214 106 224 114C216 120 204 116 196 110"
           "C190 106 184 102 178 98C160 82 134 78 112 88C92 98 78 122 72 152Z")


def _dolphin(ic):
    """A dolphin leaping right, over the disc: tail at the lower left,
    the rostrum pointing down at the right."""
    blue = ic.lin([(0, "#8AD8FF"), (0.45, "#2E8FE6"), (1, "#14509C")], 0, 0, 0.6, 1)
    fin = "#1E66B8"
    flukes = "M62 146C56 156 44 162 34 164C44 172 58 170 66 162C72 170 82 176 92 178C88 166 80 156 72 146Z"
    dorsal = "M108 58C114 38 130 26 146 24C138 34 136 44 140 52Z"
    flipper = "M168 92C168 104 162 114 152 122C164 118 174 108 180 98Z"
    for d in (flukes, dorsal, DOLPHIN):
        ic.path(d, fill="#061A3A", opacity=0.4, transform="translate(3 4)")
    ic.path(flukes, fill=fin)
    ic.path(dorsal, fill=fin)
    ic.path(DOLPHIN, fill=blue)
    body = ic.clip(f'<path d="{DOLPHIN}"/>')
    with ic.g(clip_path=body):
        ic.path("M200 114C184 100 142 74 108 92C88 102 78 126 74 154", fill="none", stroke="#D8F1FF",
                stroke_width=16, stroke_linecap="round", opacity=0.75)
        ic.path("M70 130C80 80 110 54 140 52C168 50 190 64 200 88", fill="none", stroke="#fff", stroke_width=6,
                stroke_linecap="round", opacity=0.35)
    ic.path(DOLPHIN, fill="none", stroke="#0C3A74", stroke_opacity=0.35, stroke_width=1.2)
    ic.path(flipper, fill=fin)
    ic.circle(188, 86, 3.2, fill="#0B1D38")
    ic.circle(187.2, 85.2, 1.1, fill="#fff")
    ic.path("M196 102Q206 108 218 114", fill="none", stroke="#0C3A74", stroke_width=1.4, stroke_linecap="round",
            opacity=0.6)


@icon("dolphin-emu", kind="app", names=["dolphin-emu", "org.DolphinEmu.dolphin-emu"], title="Dolphin Emulator")
def dolphin(ic):
    tile(ic, "#1F4478", "#0A1A36")
    shadow(ic, 128, 214, 80, 11)
    disc(ic, 132, 148, 60, under="#B7C0CC")
    ic.text("GAME DISC", 132, 184, 6.5, font="mono-semibold", anchor="middle", spacing=1.6, fill="#5A6472")
    ic.text("8 cm · 1.4 GB", 132, 193, 5, font="mono", anchor="middle", fill="#7A8492")
    _dolphin(ic)


@small("dolphin-emu")
def dolphin16(ic):
    tile(ic, "#1F4478", "#0A1A36")
    ic.circle(8.3, 9.6, 4.6, fill="#D5DBE2")
    ic.circle(8.3, 9.6, 1.2, fill="#1F4478")
    ic.path("M2.8 10.2C2.8 6 5 3 8.4 2.6c2.4-.3 4.2 1 5 3 .4.8.9 1.4 1.6 1.8-1 .4-2-.1-2.6-.6-1.6-1.6-3.4-2-5-1.2"
            "C5.8 6.2 4.6 8 4.2 10.4z", fill="#3A9BEF")
    ic.path("M6.6 3.3l1-2 .8 1.8z", fill="#2E7FD0")
    ic.path("M3.2 10L1.4 11.2 3.6 11.4 3.8 13 4.6 10.6z", fill="#2E7FD0")


# --- PCSX2: a deep blue console, a blue-bottomed disc on its lid -------------

@icon("pcsx2", kind="app", names=["PCSX2", "appimagekit-PCSX2", "net.pcsx2.PCSX2", "pcsx2"], title="PCSX2")
def pcsx2(ic):
    tile(ic, "#5B636E", "#25292F")
    shadow(ic, 124, 204, 104, 12)
    dx, dy = 34, -40
    x0, x1, y0, y1 = 22, 196, 136, 190
    top = [(x0, y0), (x1, y0), (x1 + dx, y0 + dy), (x0 + dx, y0 + dy)]
    side = [(x1, y0), (x1 + dx, y0 + dy), (x1 + dx, y1 + dy), (x1, y1)]
    ic.poly(top, fill=ic.lin([(0, "#3A56C8"), (1, "#1A2C86")], 0, 0, 1, 1))
    ic.poly(side, fill=ic.lin([(0, "#14216A"), (1, "#0A1240")]))
    ic.rect(x0, y0, x1 - x0, y1 - y0, fill=ic.lin([(0, "#2440A8"), (1, "#101E60")]))
    # ridges along the lid
    for k in range(1, 9):
        t = k / 9
        ic.line(x0 + dx * t + 4, y0 + dy * t, x1 + dx * t - 4, y0 + dy * t, stroke="#0A1240", stroke_opacity=0.5,
                stroke_width=1.6)
        ic.line(x0 + dx * t + 4, y0 + dy * t + 1.4, x1 + dx * t - 4, y0 + dy * t + 1.4, stroke="#fff",
                stroke_opacity=0.12, stroke_width=0.8)
    ic.line(x0, y0 + 0.6, x1, y0 + 0.6, stroke="#fff", stroke_opacity=0.45, stroke_width=1.4)
    ic.line(x1, y0, x1 + dx, y0 + dy, stroke="#fff", stroke_opacity=0.2)
    # the front: tray seam, a light strip, the name, the buttons
    ic.rect(x0 + 8, y0 + 12, 120, 9, rx=2, fill="#0A1240")
    ic.rect(x0 + 8, y0 + 12, 120, 2, rx=1, fill="#000", opacity=0.4)
    ic.rect(x0 + 8, y0 + 20, 120, 1, fill="#fff", opacity=0.15)
    ic.text("PCSX2", x0 + 10, y0 + 40, 14, font="sans-bold", spacing=1.5, fill="#E6ECFF")
    ic.rect(x0 + 72, y0 + 30, 54, 3, rx=1.5, fill="#5FA8FF", opacity=0.9)
    ic.rect(x0 + 72, y0 + 28, 54, 7, rx=3.5, fill="#5FA8FF", opacity=0.2)
    for k, c in ((0, "#5FFF9E"), (1, "#5FA8FF")):
        bx = x0 + 146 + k * 16
        ic.circle(bx, y0 + 20, 5.5, fill="#0A1240")
        ic.circle(bx, y0 + 19.4, 4.4, fill=ic.rad([(0, "#3A56C8"), (1, "#14216A")], cx=0.38, cy=0.32))
        ic.circle(bx, y0 + 30, 1.4, fill=c)
    for k in range(2):
        ic.rect(x0 + 140 + k * 18, y0 + 38, 14, 6, rx=1.2, fill="#060B2C")
    # the disc on the lid, its blue underside up
    cx, cy, r = 118, 112, 54
    m = f"matrix(1 0 {dx / 40 * 0.5:.3f} {dy / 40 * 0.5:.3f} {cx} {cy})"
    with ic.g(transform=m):
        ic.circle(2, 5, r, fill="#000", opacity=0.3)
        ic.circle(0, 0, r, fill=ic.rad([(0, "#7FB4FF"), (0.6, "#2C5CD8"), (1, "#122E86")], cx=0.4, cy=0.4, r=0.7))
        for a, c in ((30, "#C9A8FF"), (210, "#8AE8FF")):
            x1_, y1_ = polar(0, 0, r - 2, a - 14)
            x2_, y2_ = polar(0, 0, r - 2, a + 14)
            ic.path(f"M0 0L{x1_:.1f} {y1_:.1f}A{r - 2} {r - 2} 0 0 1 {x2_:.1f} {y2_:.1f}Z", fill=c, opacity=0.35)
        ic.circle(0, 0, r, fill="none", stroke="#fff", stroke_opacity=0.6, stroke_width=1.6)
        ic.circle(0, 0, 17, fill="#D8E2F2", opacity=0.85)
        ic.circle(0, 0, 6, fill="#0A1240")
    ic.ellipse(102, 98, 22, 5, fill="#fff", opacity=0.35, transform="rotate(-18 102 98)")


@small("pcsx2")
def pcsx216(ic):
    tile(ic, "#5B636E", "#25292F")
    ic.poly([(1.5, 9), (12, 9), (14.5, 6), (4, 6)], fill="#3A56C8")
    ic.poly([(12, 9), (14.5, 6), (14.5, 9.5), (12, 12.5)], fill="#0F1A58")
    ic.rect(1.5, 9, 10.5, 3.5, fill="#1E34A0")
    ic.rect(2.5, 10.2, 5, 0.8, fill="#5FA8FF")
    ic.ellipse(8, 5.6, 4.6, 2.6, fill="#2C5CD8")
    ic.ellipse(8, 5.6, 1.4, 0.8, fill="#D8E2F2")


# --- PPSSPP: a wide black handheld, the blue mark on its screen ---------------

@icon("ppsspp", kind="app", names=["org.ppsspp.PPSSPP", "ppsspp"], title="PPSSPP")
def ppsspp(ic):
    tile(ic, "#E39A3B", "#8E500E")
    shadow(ic, 128, 186, 112, 12)
    body = "M64 76H192a48 48 0 0 1 0 96H64a48 48 0 0 1 0-96Z"
    ic.rect(88, 70, 26, 10, rx=4, fill="#1A1B1F")
    ic.rect(142, 70, 26, 10, rx=4, fill="#1A1B1F")
    ic.path(body, fill="#000", opacity=0.45, transform="translate(2 5)")
    ic.path(body, fill=ic.lin([(0, "#4A4D55"), (0.3, "#24262B"), (1, "#0C0D10")], 0, 0, 0.3, 1))
    ic.path(body, fill="none", stroke="#fff", stroke_opacity=0.22, stroke_width=1.5)
    ic.path("M64 77.5H192", stroke="#fff", stroke_opacity=0.35, stroke_width=1.2)
    # the screen: the mark, a blue rounded square, "PPSSPP"
    ic.rect(66, 86, 124, 74, rx=4, fill="#050608")
    ic.rect(70, 90, 116, 66, rx=2, fill=ic.rad([(0, "#2A6FB8"), (1, "#0A2546")], cx=0.45, cy=0.4, r=0.75))
    # the mark: a little white handheld on a blue disc
    ic.circle(128, 114, 21, fill="#000", opacity=0.3, transform="translate(1 2)")
    ic.circle(128, 114, 21, fill=ic.lin([(0, "#9AD8FF"), (0.5, "#3A9BEF"), (1, "#1460C0")], 0, 0, 1, 1))
    ic.circle(128, 114, 21, fill="none", stroke="#fff", stroke_opacity=0.6)
    ic.rect(110, 106, 36, 16, rx=8, fill="#FFFFFF")
    ic.rect(119, 109, 18, 10, rx=1.5, fill="#1460C0")
    ic.circle(114.5, 114, 1.8, fill="#3A9BEF")
    ic.circle(141.5, 114, 1.8, fill="#3A9BEF")
    ic.text("PPSSPP", 128, 150, 13, font="sans-bold", anchor="middle", spacing=1.6, fill="#E9F4FF")
    ic.path("M70 92a2 2 0 0 1 2-2h70L104 156H72a2 2 0 0 1-2-2z", fill=glare(ic, 0.9))
    # the controls
    dpad(ic, 40, 116, 13, 9, fill="#2E3036")
    ic.circle(42, 152, 7.5, fill="#060708")
    ic.circle(42, 151, 6, fill=ic.rad([(0, "#6A6E78"), (1, "#2A2C32")], cx=0.38, cy=0.32))
    bx, by = 216, 120
    for ox, oy in ((0, -12), (12, 0), (0, 12), (-12, 0)):
        button(ic, bx + ox, by + oy, 5.5, "#4A4D55", "#16171A")
    ic.circle(bx, by - 12, 2.2, fill="none", stroke="#7AD7A0", stroke_width=1)
    ic.circle(bx + 12, by, 2.2, fill="none", stroke="#F08080", stroke_width=1)
    ic.circle(bx, by + 12, 2.2, fill="none", stroke="#8AB4F8", stroke_width=1)
    ic.circle(bx - 12, by, 2.2, fill="none", stroke="#E8A8E0", stroke_width=1)
    for k in range(3):
        ic.rect(100 + k * 22, 164, 14, 3.5, rx=1.75, fill="#3A3C42")
    ic.text("SELECT", 214, 160, 4.6, font="mono-semibold", anchor="middle", fill="#6A6E78")


@small("ppsspp")
def ppsspp16(ic):
    tile(ic, "#E39A3B", "#8E500E")
    ic.rect(0.8, 4.5, 14.4, 7.5, rx=3.75, fill="#1A1B1F")
    ic.rect(4.3, 5.3, 7.4, 5.9, rx=0.4, fill="#0A2546")
    ic.circle(8, 8.2, 2.5, fill="#3A9BEF")
    ic.rect(6.2, 7.5, 3.6, 1.4, rx=0.7, fill="#fff")
    ic.path("M1.6 8.2h2M2.6 7.2v2", stroke="#6A6E78", stroke_width=0.6)
    ic.circle(13.4, 8.2, 0.8, fill="#6A6E78")


# --- Ryujinx: a hybrid console in its dock, a dragon on the screen -----------

def _dragon(ic, x, y, s):
    """A dragon's head in profile, facing left, simplified: two horns
    swept back, a spiked mane, an open jaw; its box about 70 by 58 times s."""
    t = f"translate({x} {y}) scale({s})"
    head = ("M0 24L6 19L20 17L34 10L42 9L66 0L50 15L70 13L54 22L58 28L66 36L56 38L62 48L52 48L54 58L42 52"
            "L38 44L30 40L10 40L6 36L24 32L2 28Z")
    red = ("M42 9L66 0L50 15L70 13L54 22L48 18ZM56 26L66 36L56 38L62 48L52 48L54 58L46 54L50 42L52 32Z")
    ic.path(head, fill="#000", opacity=0.45, transform=f"translate({x + 2} {y + 3}) scale({s})")
    ic.path(head, fill=ic.lin([(0, "#8AEEFF"), (1, "#1A9CC8")], 0, 0, 1, 1), transform=t)
    ic.path(red, fill=ic.lin([(0, "#FF8A80"), (1, "#D8352E")], 0, 0, 1, 1), transform=t)
    ic.path("M6 28L9 31L12 28L15 31L18 29M10 36L13 33L16 35L19 32", fill="none", stroke="#fff",
            stroke_width=1.1 / s, stroke_linejoin="round", transform=t)
    ic.path("M1 24L6 19L20 17L34 10L42 9", fill="none", stroke="#fff", stroke_opacity=0.7,
            stroke_width=1.3 / s, transform=t)
    ic.path("M30 17L40 14L38 20Z", fill="#FF5F55", transform=t)
    ic.circle(x + 7 * s, y + 21 * s, 1.1 * s, fill="#0E3A4A")
    ic.path("M24 26C30 28 38 30 44 36", fill="none", stroke="#0E5A78", stroke_opacity=0.6, stroke_width=1.2 / s,
            transform=t)


@icon("ryujinx", kind="app", names=["org.ryujinx.Ryujinx", "ryujinx"], title="Ryujinx")
def ryujinx(ic):
    tile(ic, "#3E3342", "#151018")
    shadow(ic, 128, 210, 100, 12)
    # the controllers either side, cyan and red
    for x, w, light, dark, rr in ((24, 36, "#5ED6F0", "#1A88A8", "M"), (196, 36, "#FF7A70", "#C2302A", "M")):
        left = x < 100
        d = (f"M{x + w} 48V176H{x + 18}a18 18 0 0 1-18-18V66a18 18 0 0 1 18-18Z" if left else
             f"M{x} 48H{x + w - 18}a18 18 0 0 1 18 18V158a18 18 0 0 1-18 18H{x}Z")
        bevel(ic, d, ic.lin([(0, light), (1, dark)], 0, 0, 1, 1), hi=0.35)
    # left: stick and arrows; right: buttons and stick
    for cx, cy in ((42, 84), (214, 128)):
        ic.circle(cx, cy + 1.5, 9, fill="#000", opacity=0.4)
        ic.circle(cx, cy, 9, fill="#2A2C32")
        ic.circle(cx, cy - 0.6, 6.5, fill=ic.rad([(0, "#5A5E66"), (1, "#202226")], cx=0.38, cy=0.32))
    for ox, oy in ((0, -9), (9, 0), (0, 9), (-9, 0)):
        ic.circle(42 + ox, 128 + oy, 3.6, fill="#22242A")
        ic.circle(214 + ox, 84 + oy, 3.6, fill="#22242A")
    ic.rect(48, 56, 8, 2.4, fill="#22242A")
    ic.path("M200 57.2h8M204 53.2v8", stroke="#22242A", stroke_width=2.4)
    # the tablet, its screen, the dragon
    ic.rect(60, 46, 136, 132, rx=6, fill=ic.lin([(0, "#3A3C44"), (1, "#141519")]))
    ic.rect(60, 46, 136, 132, rx=6, fill="none", stroke="#fff", stroke_opacity=0.18)
    ic.rect(68, 54, 120, 112, rx=3, fill=ic.rad([(0, "#20283C"), (1, "#07090F")], cx=0.45, cy=0.4, r=0.75))
    ic.circle(128, 90, 38, fill=ic.rad([(0, "#3BC6E0", 0.3), (1, "#3BC6E0", 0)]))
    _dragon(ic, 90, 58, 1.1)
    ic.text("RYUJINX", 128, 136, 9, font="sans-bold", anchor="middle", spacing=2, fill="#DDEFF5")
    ic.path("M68 57a3 3 0 0 1 3-3h66L96 166H71a3 3 0 0 1-3-3z", fill=glare(ic, 0.8))
    # the dock in front, its own small mark
    dock = "M50 150H206a6 6 0 0 1 6 6V202a6 6 0 0 1-6 6H50a6 6 0 0 1-6-6V156a6 6 0 0 1 6-6Z"
    bevel(ic, dock, ic.lin([(0, "#4A4C55"), (0.15, "#2E3036"), (1, "#141519")]), hi=0.22)
    ic.path("M50 151.5H206", stroke="#fff", stroke_opacity=0.3, stroke_width=1.2)
    ic.circle(128, 180, 11, fill="none", stroke="#5A5D66", stroke_width=2)
    ic.path("M122 180a6 6 0 0 1 6-6v12a6 6 0 0 1-6-6z", fill="#3BC6E0")
    ic.path("M134 180a6 6 0 0 1-6 6v-12a6 6 0 0 1 6 6z", fill="#FF5F55")
    ic.circle(196, 196, 1.6, fill="#5FFF9E")


@small("ryujinx")
def ryujinx16(ic):
    tile(ic, "#3E3342", "#151018")
    ic.path("M4 3v10H2.8a1.6 1.6 0 0 1-1.6-1.6V4.6A1.6 1.6 0 0 1 2.8 3z", fill="#3BC6E0")
    ic.path("M12 3v10h1.2a1.6 1.6 0 0 0 1.6-1.6V4.6A1.6 1.6 0 0 0 13.2 3z", fill="#FF5F55")
    ic.rect(4, 3, 8, 10, fill="#22242A")
    ic.rect(4.6, 3.6, 6.8, 6, fill="#0D1220")
    ic.path("M5.4 7.6L7.4 5.6 9 4.6 10.6 5.2 9.6 6.4 10 8 8.6 8.8 8 7.6z", fill="#5ED6F0")
    ic.rect(3, 10, 10, 4.5, rx=0.6, fill="#3A3C44")


# --- itch: a red game cartridge, the shop-front mark on its label --------------

@icon("itch", kind="app", names=["io.itch.itch", "itch"], title="itch")
def itch(ic):
    tile(ic, "#2A5556", "#0E2526")
    shadow(ic, 128, 214, 82, 11)
    cart = "M56 30H178L200 52V198a10 10 0 0 1-10 10H66a10 10 0 0 1-10-10Z"
    bevel(ic, cart, ic.lin([(0, "#FF7A72"), (0.5, "#F2504F"), (1, "#B42A30")], 0, 0, 1, 1), lift=(3, 5),
          hi=0.4)
    # the grip ridges along the top
    for k in range(6):
        y = 38 + k * 5
        ic.line(66, y, 172 - (0 if y < 40 else 0), y, stroke="#9A1E26", stroke_width=1.6, opacity=0.6)
        ic.line(66, y + 1.4, 172, y + 1.4, stroke="#fff", stroke_opacity=0.25, stroke_width=0.8)
    # the label, set in, the mark in white
    ic.rect(70, 72, 116, 116, rx=6, fill="#8E1A22", opacity=0.6, transform="translate(-1 -1)")
    ic.rect(70, 72, 116, 116, rx=6, fill=ic.lin([(0, "#F65C5C"), (1, "#D63A40")]))
    ic.rect(70.5, 72.5, 115, 115, rx=5.5, fill="none", stroke="#fff", stroke_opacity=0.35)
    mx, my, mw = 98, 84, 60
    # awning: a band, five scallops below it
    ic.rect(mx, my, mw, 12, rx=3, fill="#FFFFFF")
    for k in range(5):
        ic.path(f"M{mx + k * 12} {my + 10}h12v2a6 6 0 0 1-12 0z", fill="#FFFFFF")
    # the shop below: a body with a door arch, two round eyes
    ic.path(f"M{mx + 3} {my + 22}h{mw - 6}v24a4 4 0 0 1-4 4h-14a8 8 0 0 0-16 0h-14a4 4 0 0 1-4-4z", fill="#FFFFFF")
    for ex in (mx + 21, mx + 39):
        ic.circle(ex, my + 33, 4.2, fill="#D63A40")
    ic.text("itch.io", 128, 166, 20, font="sans-bold", anchor="middle", fill="#FFFFFF")
    ic.text("GAMES · TOOLS · JAMS", 128, 178, 5.5, font="mono-semibold", anchor="middle", spacing=0.8,
            fill="#FFE0E0", opacity=0.85)
    # the arrow pressed in below the label
    ic.path("M120 194l8 6 8-6z", fill="#9A1E26", opacity=0.7)
    ic.path("M60 34a4 4 0 0 1 4-4h40L60 120z", fill=glare(ic, 1.0))


@small("itch")
def itch16(ic):
    tile(ic, "#2A5556", "#0E2526")
    ic.path("M3 1.5h8.2L13 3.3V13.5a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z", fill="#F2504F")
    ic.rect(4.6, 4.8, 6.8, 1.6, rx=0.4, fill="#fff")
    ic.path("M5 6.4h6v3.4H9.1a1.1 1.1 0 0 0-2.2 0H5z", fill="#fff")
    ic.circle(6.9, 7.6, 0.6, fill="#F2504F")
    ic.circle(9.1, 7.6, 0.6, fill="#F2504F")


# --- 0 A.D.: a bronze Corinthian helmet, its red crest ---------------------------

def bronze(ic):
    return ic.lin([(0, "#F8D79A"), (0.35, "#D49A50"), (0.7, "#9C6224"), (1, "#5A3410")], 0, 0, 1, 1)


@icon("0ad", kind="app", names=["0ad", "com.play0ad.zeroad"], title="0 A.D.")
def zeroad(ic):
    tile(ic, "#3A6C8A", "#14303F")
    shadow(ic, 132, 214, 86, 11)
    # the crest behind: horsehair on a stand, along the top
    crest = "M56 86C64 40 112 22 160 30C196 36 222 62 224 100L206 102C202 74 184 58 158 54C120 48 86 62 76 92Z"
    ic.path(crest, fill="#000", opacity=0.3, transform="translate(3 4)")
    ic.path(crest, fill=ic.lin([(0, "#E2483A"), (0.6, "#A82418"), (1, "#5E120C")], 0, 0, 1, 1))
    for k in range(14):
        t = k / 13
        a = 196 - t * 150
        x1, y1 = 140 + 82 * math.cos(math.radians(a)), 100 - 68 * math.sin(math.radians(a))
        x2, y2 = 140 + 62 * math.cos(math.radians(a)), 100 - 46 * math.sin(math.radians(a))
        ic.line(x1, y1, x2, y2, stroke="#5E120C", stroke_opacity=0.45, stroke_width=1.2)
    ic.path("M60 84C68 46 110 30 156 36", fill="none", stroke="#FF9A84", stroke_opacity=0.6, stroke_width=2,
            stroke_linecap="round")
    ic.rect(130, 62, 12, 26, rx=2, fill=bronze(ic))
    # the helmet, facing left
    helm = ("M64 112C66 84 96 70 132 70C172 70 196 96 196 132C196 156 200 176 210 196C192 200 162 196 146 186"
            "C140 170 130 164 118 166C112 180 106 196 82 204C76 190 72 170 70 150C64 146 60 130 64 112Z")
    ic.path(helm, fill="#2A1606", opacity=0.45, transform="translate(3 5)")
    ic.path(helm, fill=bronze(ic))
    ic.path(helm, fill="none", stroke="#FFE7B8", stroke_opacity=0.5, stroke_width=1.6)
    # the eye slot and the gap down to the mouth
    ic.path("M63 122C76 116 96 116 110 122C104 130 88 134 66 132Z", fill="#1A0E04")
    ic.path("M67 132L82 132L78 168L74 168Z", fill="#1A0E04")
    # the brow ridge, a meander band, the cheek's raised edge
    ic.path("M66 112C92 104 160 104 194 120", fill="none", stroke="#5A3410", stroke_opacity=0.6, stroke_width=2.4)
    ic.path("M66 110C92 102 160 102 194 118", fill="none", stroke="#FFE7B8", stroke_opacity=0.7, stroke_width=1.2)
    ic.path("M90 100C110 96 150 96 170 102", fill="none", stroke="#5A3410", stroke_opacity=0.5, stroke_width=4,
            stroke_dasharray="3 2")
    ic.text("0 A.D.", 156, 152, 13, font="sans-bold", anchor="middle", spacing=1, fill="#5A3410", opacity=0.55,
            transform="rotate(8 156 152)")
    ic.text("0 A.D.", 155.4, 151.2, 13, font="sans-bold", anchor="middle", spacing=1, fill="#FFE7B8",
            opacity=0.35, transform="rotate(8 156 152)")
    ic.path("M84 140C94 160 98 180 86 198", fill="none", stroke="#FFE7B8", stroke_opacity=0.45, stroke_width=1.5)
    ic.path("M150 182C164 190 186 194 204 192", fill="none", stroke="#5A3410", stroke_opacity=0.5, stroke_width=1.5)
    for x, y in ((122, 84), (150, 84), (176, 96)):
        ic.circle(x, y, 2.2, fill="#5A3410", opacity=0.6)
        ic.circle(x - 0.5, y - 0.5, 1.2, fill="#FFE7B8", opacity=0.8)
    ic.path("M76 104C82 86 104 76 128 75C106 80 88 90 80 108Z", fill="#fff", opacity=0.5)


@small("0ad")
def zeroad16(ic):
    tile(ic, "#3A6C8A", "#14303F")
    ic.path("M3 6C3.5 3 7 1.5 10 2c2.5.5 4 2.3 4 5h-1.4C12.4 5 11 3.6 9.6 3.4 7 3 5 4 4.4 6z", fill="#D23A2C")
    ic.path("M3.6 7.4C4 5.4 6 4.6 8.4 4.6c2.6 0 4.2 1.8 4.2 4.2 0 1.6.3 3 1 4.4-2 .4-3.6 0-4.6-.8-.6-1-1.4-1.3-2.2-1-.4 1-1 2-2.6 2.6-.6-1.4-.8-3-.8-4.4-.4-.4-.6-1.4-.2-2.2z",
            fill="#C98A40")
    ic.path("M3.6 8.2c1.6-.4 3-.4 4 0-.6.6-2 .8-3.8.6z", fill="#2A1606")


# --- SuperTuxKart: Tux at the wheel of a red go-kart ---------------------------

def _wheel(ic, x, y, r):
    ic.circle(x, y, r, fill="#141416")
    ic.circle(x, y, r, fill="none", stroke="#fff", stroke_opacity=0.12, stroke_width=2,
              stroke_dasharray="3 4")
    ic.circle(x, y, r * 0.5, fill=steel(ic, False))
    ic.circle(x, y, r * 0.2, fill="#3A3F45")
    ic.path(f"M{x - r * 0.4} {y - r * 0.2}a{r * 0.45} {r * 0.45} 0 0 1 {r * 0.3} {-r * 0.25}", fill="none",
            stroke="#fff", stroke_opacity=0.7, stroke_width=1.2)


@icon("supertuxkart", kind="app", names=["net.supertuxkart.SuperTuxKart", "supertuxkart"], title="SuperTuxKart")
def supertuxkart(ic):
    tile(ic, "#5E9C3F", "#244E16")
    shadow(ic, 128, 210, 104, 12)
    # the rear wing
    ic.rect(42, 104, 8, 40, fill="#2A2C30")
    ic.rect(22, 98, 46, 12, rx=3, fill=ic.lin([(0, "#3A3D44"), (1, "#16171A")]))
    ic.rect(22, 98, 46, 2, rx=1, fill="#fff", opacity=0.25)
    # Tux: body, belly, a flipper to the wheel, the head
    ic.ellipse(120, 126, 32, 34, fill=ic.lin([(0, "#3A3D44"), (1, "#0E0F12")], 0, 0, 1, 1))
    ic.ellipse(132, 132, 18, 24, fill=ic.lin([(0, "#FFFFFF"), (1, "#DCD8D0")], 0, 0, 1, 1))
    ic.circle(122, 76, 29, fill=ic.rad([(0, "#4A4E56"), (1, "#0E0F12")], cx=0.35, cy=0.3, r=0.75))
    ic.path("M112 80C112 66 120 60 130 60C142 60 150 70 150 82C150 96 140 102 130 102C120 102 112 94 112 80Z",
            fill=ic.lin([(0, "#FFFFFF"), (1, "#E2DED6")], 0, 0, 1, 1))
    for ex in (124, 140):
        ic.ellipse(ex, 74, 5.4, 7.4, fill="#FFFFFF", stroke="#2A2C30", stroke_width=0.8)
        ic.ellipse(ex + 1.6, 76, 2.8, 3.6, fill="#111")
        ic.circle(ex + 2.4, 74.6, 0.9, fill="#fff")
    ic.path("M122 88C130 84 148 84 156 90C150 96 136 98 124 94Z", fill=ic.lin([(0, "#FFC23A"), (1, "#E07A10")]))
    ic.path("M124 92C134 94 146 94 154 91", fill="none", stroke="#9A4A08", stroke_width=1.2)
    ic.path("M146 116C156 112 166 114 172 120L168 126C160 122 152 122 146 124Z", fill="#14151A")
    # the steering wheel, edge on
    ic.line(176, 124, 186, 152, stroke="#2A2C30", stroke_width=4, stroke_linecap="round")
    ic.ellipse(174, 122, 4, 13, fill="none", stroke="#1A1B1F", stroke_width=4, transform="rotate(20 174 122)")
    # the kart's body, red, its number roundel
    body = "M30 184V150Q30 138 42 138H96L106 150H150Q174 150 200 158L226 166Q234 170 230 180L214 186H30Z"
    ic.path(body, fill="#000", opacity=0.35, transform="translate(2 4)")
    ic.path(body, fill=ic.lin([(0, "#FF7A4A"), (0.5, "#E8441C"), (1, "#9E2408")], 0, 0, 0.4, 1))
    ic.path("M42 139.5H95L104 151.5H150Q172 151.5 198 159.5", fill="none", stroke="#FFC0A0", stroke_opacity=0.8,
            stroke_width=1.6)
    ic.path("M36 172H222", stroke="#7A1A04", stroke_opacity=0.5, stroke_width=1.4)
    ic.circle(124, 168, 13, fill="#FFFFFF")
    ic.circle(124, 168, 13, fill="none", stroke="#7A1A04", stroke_opacity=0.4)
    ic.text("1", 124, 175, 18, font="sans-bold", anchor="middle", fill="#1E1F24")
    ic.text("STK", 150, 168, 10, font="sans-bold", spacing=1, fill="#FFE6D8", transform="rotate(6 150 168)")
    ic.rect(18, 160, 14, 6, rx=2, fill=steel(ic, False))
    # the wheels
    _wheel(ic, 72, 186, 24)
    _wheel(ic, 194, 188, 21)


@small("supertuxkart")
def supertuxkart16(ic):
    tile(ic, "#5E9C3F", "#244E16")
    ic.circle(7.5, 5, 3, fill="#16171A")
    ic.ellipse(8.4, 5.4, 1.8, 2, fill="#fff")
    ic.path("M8 6.4h3l-1.4 1z", fill="#F2A21A")
    ic.path("M1.8 12V9.4h5l.8 1h3.8l2.8 1.2V12z", fill="#E8441C")
    ic.circle(4.5, 12.4, 2, fill="#141416")
    ic.circle(12, 12.6, 1.7, fill="#141416")
    ic.circle(4.5, 12.4, 0.8, fill="#A9B0B8")
    ic.circle(12, 12.6, 0.7, fill="#A9B0B8")


# --- Battle for Wesnoth: a round shield, a sword behind, a crown on it -----------

@icon("wesnoth", kind="app", names=["org.wesnoth.Wesnoth", "wesnoth", "wesnoth-1.10-icon", "wesnoth-1.12-icon",
                                    "wesnoth-1.14-icon", "wesnoth-icon"], title="Battle for Wesnoth")
def wesnoth(ic):
    tile(ic, "#5C4428", "#1F160B")
    shadow(ic, 128, 218, 80, 11)
    # the sword, upright behind the shield
    ic.path("M121 58H135L134 206L128 222L122 206Z", fill="#000", opacity=0.3, transform="translate(3 4)")
    ic.path("M121 58H135L134 206L128 222L122 206Z", fill=steel(ic))
    ic.line(128, 62, 128, 206, stroke="#5D636B", stroke_width=1.4)
    ic.rect(123, 24, 10, 30, rx=3, fill=ic.lin([(0, "#6A3A1E"), (1, "#3A1C0C")], 0, 0, 1, 0))
    for k in range(5):
        ic.line(123, 28 + k * 5.5, 133, 31 + k * 5.5, stroke="#2A1206", stroke_width=1.2, opacity=0.7)
    ic.circle(128, 20, 7.5, fill=brass(ic))
    ic.path("M88 52C100 56 112 56 128 54C144 56 156 56 168 52C170 58 166 62 160 62H96C90 62 86 58 88 52Z",
            fill=brass(ic))
    ic.path("M90 53C104 57 116 57 128 55.4C140 57 152 57 166 53", fill="none", stroke="#FFF2C8", stroke_opacity=0.8,
            stroke_width=1)
    # the shield: an iron rim with rivets, oak planks, a crimson field
    cx, cy = 128, 134
    ic.circle(cx + 3, cy + 5, 74, fill="#000", opacity=0.35)
    ic.circle(cx, cy, 74, fill=ic.lin([(0, "#D4D8DD"), (0.5, "#8A9098"), (1, "#3E444C")], 0, 0, 1, 1))
    ic.circle(cx, cy, 73, fill="none", stroke="#fff", stroke_opacity=0.5, stroke_width=1.4)
    ic.circle(cx, cy, 64, fill=wood(ic, "#B07A44", "#5E3518"))
    planks = ic.clip(f'<circle cx="{cx}" cy="{cy}" r="64"/>')
    with ic.g(clip_path=planks):
        for x in range(cx - 64, cx + 64, 18):
            ic.line(x, cy - 64, x, cy + 64, stroke="#3A1C0C", stroke_width=1.4, opacity=0.6)
            ic.line(x + 1.4, cy - 64, x + 1.4, cy + 64, stroke="#E2B07A", stroke_width=0.8, opacity=0.35)
    ic.circle(cx, cy, 46, fill="#3A0C0C", opacity=0.5, transform="translate(1 1.5)")
    ic.circle(cx, cy, 46, fill=ic.rad([(0, "#B83A2A"), (1, "#6A1610")], cx=0.4, cy=0.35, r=0.75))
    ic.circle(cx, cy, 46, fill="none", stroke="#E8C06A", stroke_width=2)
    for k in range(16):
        x, y = polar(cx, cy, 69, k * 22.5 + 11.25)
        ic.circle(x, y, 2.6, fill=steel(ic, False))
        ic.circle(x - 0.6, y - 0.6, 1, fill="#fff", opacity=0.8)
    # the crown, gold, painted on the field
    crown = "M100 150L95 114L113 130L128 102L143 130L161 114L156 150Z"
    ic.path(crown, fill="#2A0806", opacity=0.5, transform="translate(1.5 2.5)")
    ic.path(crown, fill=brass(ic))
    ic.rect(98, 146, 60, 11, rx=2, fill=brass(ic, 1, 1, 0, 0))
    for x, y in ((95, 111), (128, 99), (161, 111)):
        ic.circle(x, y, 4, fill=brass(ic))
    for x, c in ((114, "#2E6FD0"), (128, "#2EA05A"), (142, "#2E6FD0")):
        ic.circle(x, 151.5, 3, fill=c)
        ic.circle(x - 0.8, 150.7, 1, fill="#fff", opacity=0.7)
    ic.path("M97 117L113 132L128 106", fill="none", stroke="#FFF2C8", stroke_opacity=0.7, stroke_width=1.2)
    # a ribbon across the foot of the shield
    rib = "M40 186L64 182L64 208L48 204L54 196Z"
    ic.path(rib, fill="#B9A882")
    ic.path("M216 186L192 182L192 208L208 204L202 196Z", fill="#B9A882")
    ic.path("M60 180C100 188 156 188 196 180V204C156 212 100 212 60 204Z", fill="#000", opacity=0.3,
            transform="translate(2 3)")
    ic.path("M60 180C100 188 156 188 196 180V204C156 212 100 212 60 204Z", fill=paper(ic, "washi"))
    ic.path("M60 180C100 188 156 188 196 180", fill="none", stroke="#fff", stroke_width=1.2)
    ic.text("WESNOTH", 128, 202, 14, font="sans-bold", anchor="middle", spacing=3, fill="#4A2A14")


@small("wesnoth")
def wesnoth16(ic):
    tile(ic, "#5C4428", "#1F160B")
    ic.rect(7.4, 0.8, 1.2, 14.4, fill="#C3C8CE")
    ic.rect(5, 2.6, 6, 1, rx=0.5, fill="#D9A84A")
    ic.circle(8, 8.6, 5.4, fill="#8A9098")
    ic.circle(8, 8.6, 4.4, fill="#A82E22")
    ic.path("M5.4 10.6L5 6.8 6.6 8.2 8 5.8 9.4 8.2 11 6.8 10.6 10.6z", fill="#F2C45C")
