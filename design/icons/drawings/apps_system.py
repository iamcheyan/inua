"""The inua-objects theme, "system" batch: Steam, Lutris, Heroic, Bottles,
Virtual Machine Manager, VirtualBox, Remote Viewer, GParted, Disks and
Timeshift (docs/feat/object-icons.md, Part 2). Each brand's mark is
redrawn, simplified, on an object of the app's job."""

import math

from lib import (brass, glare, graphite, icon, paper, polar, shadow, small, steel, text_path, tile, wood)


def rot(deg, cx, cy):
    return f"rotate({deg:g} {cx:g} {cy:g})"


def arc_text(ic, s, cx, cy, r, mid_deg, size, font="sans-semibold", spacing=0.0, inner=False, **kw):
    """A line of text along a circle, centred on mid_deg (0 up, clockwise);
    over the top it reads clockwise, with inner=True it reads along the
    bottom, upright, counter-clockwise."""
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


def screw(ic, x, y, r=3.2, deg=30):
    ic.circle(x, y, r, fill=steel(ic, False))
    ic.circle(x, y, r, fill="none", stroke="#000", stroke_opacity=0.3, stroke_width=0.6)
    ic.line(*polar(x, y, r * 0.7, deg), *polar(x, y, r * 0.7, deg + 180), stroke="#3A3F45", stroke_width=0.9)


def cursor(ic, x, y, s=1.0):
    """A mouse pointer, its tip at x, y."""
    ic.path("M0 0V17L4.2 13.2 7 19.5 9.6 18.4 6.9 12.3H12.4Z", fill="#fff", stroke="#111", stroke_width=1.1,
            stroke_linejoin="round", transform=f"translate({x:g} {y:g}) scale({s:g})")


# --- Steam: a locomotive's driving wheel, its crank and connecting rod -------

NAVY = "#1B2838"


@icon("steam", kind="app", names=["com.valvesoftware.Steam", "steam", "steam-icon", "steam-launcher", "steampowered"],
      title="Steam")
def steam(ic):
    tile(ic, "#35648A", "#111A27")
    cx, cy = 142, 112
    shadow(ic, 128, 214, 96, 12)
    # the wheel: a white-walled tyre, navy spokes, a counterweight
    ic.circle(cx + 3, cy + 5, 86, fill="#000", opacity=0.3)
    ic.circle(cx, cy, 86, fill=ic.lin([(0, "#FFFFFF"), (0.5, "#D9DEE4"), (1, "#8D97A3")], 0, 0, 1, 1))
    ic.circle(cx, cy, 85, fill="none", stroke="#fff", stroke_width=1.5, opacity=0.8)
    ic.circle(cx, cy, 76, fill="#0B1118")
    ic.circle(cx, cy, 73, fill=ic.lin([(0, "#2E4A66"), (1, "#14202E")], 0, 0, 1, 1))
    ic.path(sector(cx, cy, 72, 38, 135, 225), fill="#0A0F16")
    ic.path(sector(cx, cy, 70, 40, 137, 223), fill=ic.lin([(0, "#466A8E"), (1, "#1E3044")], 0, 0, 1, 1))
    ic.path(sector(cx, cy, 70, 67, 137, 223), fill="#fff", opacity=0.2)
    for a in (150, 172, 194, 216):
        x, y = polar(cx, cy, 56, a)
        ic.circle(x, y, 2.4, fill="#C7D0DA")
        ic.circle(x + 0.5, y + 0.5, 2.4, fill="none", stroke="#0A0F16", stroke_width=0.6, opacity=0.6)
    spoke = ic.lin([(0, "#4E7092"), (1, "#1E3044")], 0, 0, 1, 1)
    for k in range(14):
        a = k * 360 / 14 + 8
        if 130 < a % 360 < 230:
            continue
        x1, y1 = polar(cx, cy, 20, a - 6)
        x2, y2 = polar(cx, cy, 70, a - 2.6)
        x3, y3 = polar(cx, cy, 70, a + 2.6)
        x4, y4 = polar(cx, cy, 20, a + 6)
        ic.poly([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], fill=spoke)
        ic.line(x1, y1, x2, y2, stroke="#fff", stroke_opacity=0.18, stroke_width=0.8)
    ic.circle(cx, cy, 22, fill=ic.lin([(0, "#3D5F80"), (1, "#162434")], 0, 0, 1, 1))
    ic.circle(cx, cy, 22, fill="none", stroke="#fff", stroke_opacity=0.2)
    for k in range(6):
        x, y = polar(cx, cy, 15, k * 60)
        ic.circle(x, y, 1.8, fill="#C7D0DA")
    # the crank: Steam's large ring on the pin
    px, py = 164, 92
    kx, ky = 62, 178
    ang = math.degrees(math.atan2(ky - py, kx - px))
    length = math.hypot(kx - px, ky - py)
    ic.circle(px + 2, py + 3, 33, fill="#000", opacity=0.3)
    # the connecting rod, polished steel
    with ic.g(transform=f"translate({px} {py}) rotate({ang:.2f})"):
        ic.rect(0, -10, length, 20, rx=6, fill="#000", opacity=0.3, transform="translate(2 4)")
        ic.rect(0, -10, length, 20, rx=6, fill=ic.lin([(0, "#FFFFFF"), (0.45, "#E2E6EA"), (1, "#8C96A2")]))
        ic.rect(14, -3, length - 28, 6, rx=3, fill="#9AA4AF", opacity=0.6)
    mid_x, mid_y = (px + kx) / 2, (py + ky) / 2
    ic.text("STEAM", mid_x, mid_y + 2.2, 7, font="mono-semibold", anchor="middle", spacing=2.2, fill=NAVY,
            transform=rot(ang + 180, mid_x, mid_y))
    # the big boss, ring and pin
    ic.circle(px, py, 32, fill=ic.lin([(0, "#FFFFFF"), (1, "#AEB7C1")], 0, 0, 1, 1))
    ic.circle(px, py, 31, fill="none", stroke="#fff", stroke_width=1.5)
    ic.circle(px, py, 23, fill=ic.lin([(0, "#0D141D"), (1, "#24384D")], 0, 0, 1, 1))
    ic.circle(px, py, 16, fill=ic.lin([(0, "#FFFFFF"), (1, "#B9C2CC")], 0, 0, 1, 1))
    ic.circle(px, py, 6, fill=ic.lin([(0, "#6C7886"), (1, "#C9D0D8")], 0, 0, 1, 1))
    ic.path(f"M{px - 28} {py - 8}a29 29 0 0 1 20-20 33 33 0 0 0-20 20z", fill="#fff", opacity=0.9)
    # the small end, at the crosshead
    ic.circle(kx + 2, ky + 3, 17, fill="#000", opacity=0.3)
    ic.circle(kx, ky, 17, fill=ic.lin([(0, "#FFFFFF"), (1, "#A9B2BC")], 0, 0, 1, 1))
    ic.circle(kx, ky, 10, fill=ic.lin([(0, "#0D141D"), (1, "#24384D")], 0, 0, 1, 1))
    ic.circle(kx, ky, 4.5, fill="#C9D0D8")


@small("steam")
def steam16(ic):
    tile(ic, "#35648A", "#111A27")
    ic.circle(8.8, 7.2, 5.6, fill="#E3E7EC")
    ic.circle(8.8, 7.2, 4.7, fill="#1E3044")
    ic.path("M10 6 L4 11.4", stroke="#F2F4F6", stroke_width=1.6, stroke_linecap="round")
    ic.circle(10, 6, 2.2, fill="#F2F4F6")
    ic.circle(10, 6, 1, fill="#1E3044")
    ic.circle(4, 11.4, 1.5, fill="#F2F4F6")


# --- Lutris: a nickel arcade token, an otter curled in its blue enamel -------

def otter(ic, cx, cy, s, body, dark):
    """A curled otter, simplified from Lutris's mark: its body round in a
    ring to the tail, its head at the top right, s the ring's radius."""
    def band(t0, t1, f0, f1, n=40):
        """Points along the body from t0 to t1, between the fractions f0
        and f1 of its width (0 its outside, 1 its inside)."""
        out, back = [], []
        for i in range(n + 1):
            t = t0 + (t1 - t0) * i / n
            a = 50 + t * 300
            w = s * (0.86 * (1 - t) ** 0.75 + 0.1)
            r = s * (1.0 - 0.1 * t)
            out.append(polar(cx, cy, r + w / 2 - w * f0, a))
            back.append(polar(cx, cy, r + w / 2 - w * f1, a))
        pts = out + back[::-1]
        return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"
    ic.path(band(0, 1, 0, 1), fill=body)
    # the belly, lighter, along the inside of the curl
    ic.path(band(0.04, 0.78, 0.55, 0.92), fill="#FFE2A0", opacity=0.6)
    # the tail's tip, round
    tx, ty = polar(cx, cy, s * 0.9, 350)
    ic.circle(tx, ty, s * 0.06, fill=body)
    # the head, its snout to the right, an ear, an eye, the nose
    hx, hy = polar(cx, cy, s * 0.95, 40)
    hr = s * 0.5
    ic.ellipse(hx, hy, hr * 1.02, hr * 0.9, fill=body, transform=rot(24, hx, hy))
    sx, sy = hx + hr * 0.92, hy + hr * 0.25
    ic.ellipse(sx, sy, hr * 0.52, hr * 0.4, fill=body, transform=rot(18, sx, sy))
    ic.ellipse(sx + hr * 0.04, sy + hr * 0.12, hr * 0.38, hr * 0.24, fill="#FFE6B8", transform=rot(18, sx, sy))
    ic.ellipse(sx + hr * 0.42, sy - hr * 0.1, hr * 0.15, hr * 0.12, fill=dark)
    for k in (-1, 1):
        ic.line(sx + hr * 0.1, sy + hr * 0.1 * k, sx + hr * 0.75, sy + hr * 0.24 * k + hr * 0.1, stroke=dark,
                stroke_width=0.6, opacity=0.5)
    ex, ey = hx - hr * 0.5, hy - hr * 0.6
    ic.circle(ex, ey, hr * 0.26, fill=body)
    ic.circle(ex, ey, hr * 0.13, fill=dark, opacity=0.55)
    ic.circle(hx + hr * 0.2, hy - hr * 0.22, hr * 0.13, fill=dark)
    ic.circle(hx + hr * 0.24, hy - hr * 0.27, hr * 0.04, fill="#fff")
    # a front paw, tucked under the chin
    px, py = polar(cx, cy, s * 0.62, 100)
    ic.ellipse(px, py, hr * 0.32, hr * 0.22, fill=body, transform=rot(-30, px, py))
    ic.ellipse(px, py, hr * 0.32, hr * 0.22, fill="none", stroke=dark, stroke_width=0.6, opacity=0.35,
               transform=rot(-30, px, py))


@icon("lutris", kind="app", names=["lutris", "net.lutris.Lutris"], title="Lutris")
def lutris(ic):
    tile(ic, "#E08A35", "#8A3E10")
    cx, cy = 128, 118
    shadow(ic, 128, 214, 90, 12)
    # the token's edge, its thickness below
    ic.circle(cx, cy + 8, 90, fill="#3E454E")
    ic.circle(cx, cy + 4, 90, fill="#70787F")
    ic.circle(cx, cy + 6, 90, fill="none", stroke="#2A2F35", stroke_width=2, stroke_dasharray="1.2 2.8", opacity=0.8)
    ic.circle(cx, cy, 90, fill=ic.lin([(0, "#FBFCFD"), (0.45, "#BFC6CD"), (1, "#6F7882")], 0, 0, 1, 1))
    ic.circle(cx, cy, 89, fill="none", stroke="#fff", stroke_width=1.5, opacity=0.8)
    ic.circle(cx, cy, 80, fill=ic.lin([(0, "#7D868F"), (0.55, "#C9CFD5"), (1, "#F4F6F8")], 0, 0, 1, 1))
    ic.circle(cx, cy, 78, fill=ic.lin([(0, "#F1F3F5"), (1, "#9AA3AC")], 0, 0, 1, 1))
    arc_text(ic, "LUTRIS", cx, cy, 66, 0, 13, font="sans-bold", spacing=3, fill="#4A525B")
    arc_text(ic, "GOOD FOR ONE PLAY", cx, cy, 72, 180, 7.5, font="mono-semibold", spacing=1.2, inner=True,
             fill="#4A525B")
    for a in (-62, 62):
        x, y = polar(cx, cy, 68, a)
        ic.path(f"M{x:.1f} {y - 3.4:.1f}l1 2.4 2.6.2-2 1.7.6 2.5-2.2-1.4-2.2 1.4.6-2.5-2-1.7 2.6-.2z", fill="#4A525B")
    # the enamel: Lutris's blue, the otter in orange
    ic.circle(cx, cy, 52, fill="#5D666F")
    ic.circle(cx, cy, 50, fill=ic.rad([(0, "#3F7FCB"), (1, "#173F7A")], cx=0.4, cy=0.35, r=0.75))
    otter(ic, cx - 4, cy + 4, 28, ic.lin([(0, "#FFC04A"), (1, "#E5651C")], 0, 0, 1, 1), "#2A1A10")
    ic.circle(cx, cy, 50, fill=glare(ic, 1.1))
    ic.path(f"M{cx - 44} {cy - 14}a46 46 0 0 1 30-32 50 50 0 0 0-30 32z", fill="#fff", opacity=0.55)
    ic.path(f"M{cx - 84} {cy - 22}a86 86 0 0 1 56-60 90 90 0 0 0-56 60z", fill="#fff", opacity=0.75)


@small("lutris")
def lutris16(ic):
    tile(ic, "#E08A35", "#8A3E10")
    ic.circle(8, 8.4, 6.4, fill="#5B636B")
    ic.circle(8, 8, 6.4, fill="#D9DEE3")
    ic.circle(8, 8, 4.4, fill="#2A5FA6")
    ic.path(sector(8, 8, 3.2, 1.4, 60, 340), fill="#FFA43A")
    ic.circle(9.9, 6.2, 1.4, fill="#FFA43A")


# --- Heroic: a heater shield in blue enamel, a sword across it --------------

SHIELD = "M{l} {t}H{r}V{m}C{r} {c1} {c2} {c3} {x} {b}C{c4} {c3} {l} {c1} {l} {m}Z"


def shield_path(x, t, w, h):
    l, r = x - w / 2, x + w / 2
    m = t + h * 0.38
    return SHIELD.format(l=l, t=t, r=r, m=f"{m:.1f}", c1=f"{t + h * 0.72:.1f}", c2=f"{x + w * 0.24:.1f}",
                         c3=f"{t + h * 0.9:.1f}", c4=f"{x - w * 0.24:.1f}", x=x, b=t + h)


@icon("heroic", kind="app", names=["appimagekit-heroic", "com.heroicgameslauncher.hgl", "heroic"],
      title="Heroic Games Launcher")
def heroic(ic):
    tile(ic, "#3B3E86", "#141633")
    shadow(ic, 128, 216, 80, 11)
    x = 124
    # the shield: steel rim, blue enamel, a cyan chevron
    ic.path(shield_path(x + 4, 42, 160, 174), fill="#000", opacity=0.3)
    ic.path(shield_path(x, 38, 160, 174), fill=ic.lin([(0, "#F2F5F8"), (0.5, "#A7B0BA"), (1, "#56606B")], 0, 0, 1, 1))
    ic.path(shield_path(x, 47, 142, 155), fill="#1A2440")
    ic.path(shield_path(x, 49, 138, 151), fill=ic.lin([(0, "#2C6FD6"), (1, "#122C6A")], 0, 0, 1, 1))
    inner = ic.clip(f'<path d="{shield_path(x, 49, 138, 151)}"/>')
    with ic.g(clip_path=inner):
        ic.path(f"M{x - 80} 112 L{x} 150 L{x + 80} 112 V136 L{x} 174 L{x - 80} 136Z", fill="#1CC4E8")
        ic.path(f"M{x - 80} 112 L{x} 150 L{x + 80} 112 V115 L{x} 153 L{x - 80} 115Z", fill="#B9F2FF", opacity=0.6)
        ic.path(f"M{x - 80} 30 H{x - 10} L{x - 80} 160Z", fill="#fff", opacity=0.10)
    # rivets on the rim
    for rx_, ry_ in ((x - 72, 46), (x + 72, 46), (x - 72, 100), (x + 72, 100), (x - 52, 160), (x + 52, 160),
                     (x, 203)):
        ic.circle(rx_, ry_, 2.6, fill="#E6EAEE")
        ic.circle(rx_ + 0.6, ry_ + 0.6, 2.6, fill="none", stroke="#3A424B", stroke_width=0.8, opacity=0.6)
    ic.line(x - 78, 39.5, x + 78, 39.5, stroke="#fff", stroke_width=1.5)
    # the sword, point down, across the shield
    with ic.g(transform=rot(-38, 128, 124)):
        bx = 128
        ic.path(f"M{bx - 7} 96 L{bx - 7} 220 L{bx} 236 L{bx + 7} 220 L{bx + 7} 96Z", fill="#000", opacity=0.3,
                transform="translate(4 3)")
        ic.path(f"M{bx - 7} 96 L{bx - 7} 220 L{bx} 236 L{bx} 96Z", fill=ic.lin([(0, "#FFFFFF"), (1, "#C3CBD3")]))
        ic.path(f"M{bx} 96 L{bx} 236 L{bx + 7} 220 L{bx + 7} 96Z", fill=ic.lin([(0, "#9AA4AE"), (1, "#5D6670")]))
        ic.line(bx, 100, bx, 226, stroke="#4C555F", stroke_width=0.8)
        ic.rect(bx - 26, 88, 52, 9, rx=4.5, fill="#000", opacity=0.3, transform="translate(3 3)")
        ic.rect(bx - 26, 88, 52, 9, rx=4.5, fill=brass(ic))
        ic.circle(bx - 26, 92.5, 6, fill=brass(ic))
        ic.circle(bx + 26, 92.5, 6, fill=brass(ic))
        ic.rect(bx - 5, 52, 10, 36, rx=3, fill=ic.lin([(0, "#6A3A22"), (1, "#3A1C0E")], 0, 0, 1, 0))
        for y in range(56, 88, 5):
            ic.line(bx - 5, y, bx + 5, y + 3, stroke="#C99645", stroke_width=1, opacity=0.7)
        ic.circle(bx, 46, 8, fill=brass(ic))
        ic.circle(bx - 2, 44, 2.5, fill="#fff", opacity=0.6)
    # the ribbon across the bottom
    ic.path("M50 170 L68 164 L70 186 L52 190 L58 179Z", fill="#9E2A22")
    ic.path("M206 170 L188 164 L186 186 L204 190 L198 179Z", fill="#9E2A22")
    ic.path("M64 160 Q128 176 192 160 L192 182 Q128 198 64 182Z", fill=ic.lin([(0, "#F04A3C"), (1, "#B8261C")]))
    ic.path("M64 160 Q128 176 192 160", fill="none", stroke="#FFB4A8", stroke_width=1.4, opacity=0.8)
    ic.text("HEROIC", 128, 182.5, 14, font="sans-bold", anchor="middle", spacing=3, fill="#FFF3E6")


@small("heroic")
def heroic16(ic):
    tile(ic, "#3B3E86", "#141633")
    ic.path(shield_path(8, 2, 11, 12.5), fill="#C9D0D8")
    ic.path(shield_path(8, 3, 9, 10.5), fill="#2463C8")
    ic.path("M3.5 8 L8 10.2 L12.5 8 V9.6 L8 11.8 L3.5 9.6Z", fill="#38D4F2")
    ic.path("M4.5 4.5 L11.5 11.5", stroke="#F2F4F6", stroke_width=1.3, stroke_linecap="round")
    ic.path("M3.8 6.6 L6.6 3.8", stroke="#D9A54A", stroke_width=1.3, stroke_linecap="round")


# --- Bottles: a corked bottle, wine in it, a paper label --------------------

BOTTLE = ("M112 58 V96 C112 106 84 112 80 132 V198 Q80 208 90 208 H166 Q176 208 176 198 V132 "
          "C172 112 144 106 144 96 V58Z")


@icon("bottles", kind="app", names=["bottles"], title="Bottles")
def bottles(ic):
    tile(ic, "#3F7B86", "#153840")
    shadow(ic, 128, 210, 66, 10)
    ic.path(BOTTLE, fill="#000", opacity=0.25, transform="translate(4 3)")
    # the glass, green, the wine seen through it
    ic.path(BOTTLE, fill=ic.lin([(0, "#3E6E48"), (0.5, "#24502E"), (1, "#123019")], 0, 0, 1, 0))
    wine = ic.clip(f'<path d="{BOTTLE}"/>')
    with ic.g(clip_path=wine):
        ic.rect(70, 122, 120, 100, fill=ic.lin([(0, "#8E1C2A"), (1, "#3A0710")], 0, 0, 1, 0), opacity=0.85)
        ic.ellipse(128, 122, 50, 4, fill="#B8344A", opacity=0.6)
        ic.rect(84, 60, 10, 150, fill="#fff", opacity=0.10)
    ic.path(BOTTLE, fill="none", stroke="#9FD3A8", stroke_opacity=0.35, stroke_width=1.5)
    ic.path("M82 200 Q128 192 174 200 V198 Q174 208 166 208 H90 Q82 208 82 198Z", fill="#0A1A0E", opacity=0.6)
    ic.path("M86 203 Q128 196 170 203", fill="none", stroke="#C8F0CF", stroke_opacity=0.35, stroke_width=1)
    # the label
    ic.rect(84, 142, 88, 54, rx=2, fill=paper(ic, "cream"))
    ic.rect(84, 142, 88, 4, fill="#C0282E")
    ic.rect(84, 192, 88, 4, fill="#C0282E")
    ic.text("Bottles", 128, 170, 19, font="hand", anchor="middle", fill="#3A1A18")
    ic.text("WIN64 · 2026", 128, 184, 6, font="mono-semibold", anchor="middle", spacing=1, fill="#7A3A30")
    ic.line(96, 175, 160, 175, stroke="#C0282E", stroke_width=0.8, opacity=0.6)
    ic.rect(172, 142, 4, 54, fill="#000", opacity=0.25)
    # the capsule and the cork
    ic.rect(110, 54, 36, 22, rx=3, fill=ic.lin([(0, "#E04848"), (0.5, "#B3222A"), (1, "#6E0E14")], 0, 0, 1, 0))
    ic.rect(110, 72, 36, 4, rx=2, fill="#5A0A10", opacity=0.6)
    ic.rect(113, 30, 30, 28, rx=4, fill=ic.lin([(0, "#E9C48C"), (0.6, "#C69457"), (1, "#8C6232")], 0, 0, 1, 0))
    ic.ellipse(128, 31, 15, 4, fill="#F4DBAE")
    for x, y in ((120, 40), (134, 44), (126, 50), (138, 36), (118, 52)):
        ic.circle(x, y, 1, fill="#7A5228", opacity=0.6)
    # the shine down the glass
    ic.path("M90 134 C92 120 104 112 112 106 L114 110 C106 116 96 124 94 136 V196 H90Z", fill="#fff", opacity=0.35)
    ic.rect(116, 78, 4, 22, rx=2, fill="#fff", opacity=0.3)


@small("bottles")
def bottles16(ic):
    tile(ic, "#3F7B86", "#153840")
    ic.path("M7 2.5 V5.5 C7 6.2 5 6.8 5 8.2 V13.5 H11 V8.2 C11 6.8 9 6.2 9 5.5 V2.5Z", fill="#2C5A36")
    ic.rect(5, 8.6, 6, 4.9, fill="#7A1826")
    ic.rect(5.5, 9.4, 5, 3, fill="#F4ECDC")
    ic.rect(6.8, 1.5, 2.4, 2, rx=0.5, fill="#D9A866")
    ic.rect(6.8, 3.3, 2.4, 1.3, fill="#C0282E")


# --- Virtual Machine Manager: a little rack of servers, its guests on a screen --

def _rack_unit(ic, y, h, x0=46, x1=210):
    """One steel chassis in the rack, y to y + h, its ears screwed to the posts."""
    ic.rect(x0, y, x1 - x0, h, rx=3, fill=ic.lin([(0, "#E4E8EC"), (0.5, "#B3BAC2"), (1, "#7C858F")], 0, 0, 0.3, 1))
    ic.line(x0 + 2, y + 1, x1 - 2, y + 1, stroke="#fff", stroke_width=1.2, opacity=0.9)
    ic.line(x0 + 2, y + h - 0.8, x1 - 2, y + h - 0.8, stroke="#000", stroke_width=1.2, opacity=0.25)
    for ex in (x0 - 10, x1):
        ic.rect(ex, y + 1, 10, h - 2, rx=2, fill=ic.lin([(0, "#C9D0D8"), (1, "#6B747E")]))
        for sy in ((y + h / 2,) if h < 30 else (y + 8, y + h - 8)):
            ic.circle(ex + 5, sy, 2.4, fill=ic.rad([(0, "#F2F4F6"), (1, "#5D636B")], cx=0.35, cy=0.3, r=0.8))
            ic.line(ex + 3.6, sy, ex + 6.4, sy, stroke="#3A4048", stroke_width=0.7)


def _drives(ic, x, y, n, w=17, h=10):
    for k in range(n):
        dx = x + k * (w + 2)
        ic.rect(dx, y, w, h, rx=1.2, fill="#2B3138")
        ic.rect(dx + 1, y + 1, w - 2, h - 2, rx=0.8, fill=ic.lin([(0, "#59616B"), (1, "#3A4048")]))
        for vx in range(int(dx) + 3, int(dx + w) - 5, 3):
            ic.rect(vx, y + 2.5, 1.4, h - 5, fill="#20252B")
        ic.circle(dx + w - 3, y + h / 2, 1.1, fill="#7CF7A6" if k % 3 else "#5AB0FF")


@icon("virt-manager", kind="app", names=["virt-manager"], title="Virtual Machine Manager")
def virt_manager(ic):
    tile(ic, "#55708C", "#1F3045")
    shadow(ic, 128, 214, 96, 11)
    # the rack: two black posts, holes up them, on little feet
    for px in (30, 214):
        ic.rect(px + 2, 32, 12, 178, rx=2, fill="#000", opacity=0.3)
        ic.rect(px, 30, 12, 178, rx=2, fill=ic.lin([(0, "#3E444C"), (1, "#16191C")], 0, 0, 1, 0))
        ic.line(px + 1, 31, px + 1, 206, stroke="#fff", stroke_opacity=0.15)
        for hy in range(36, 204, 7):
            ic.rect(px + 4.5, hy, 3, 3, fill="#08090B")
        ic.rect(px - 3, 204, 18, 6, rx=2, fill="#2A2E33")
    # the top unit, 3U: the screen with three guests, the plate, the lights
    _rack_unit(ic, 40, 70)
    ic.rect(56, 47, 86, 56, rx=4, fill="#2B3138")
    ic.rect(59, 50, 80, 50, rx=2, fill=ic.lin([(0, "#3F86B8"), (1, "#173F66")], 0, 0, 1, 1))
    for (gx, gy, col) in ((63, 54, "#D7543C"), (101, 54, "#56B567"), (63, 77, "#E8A33A")):
        ic.rect(gx, gy, 34, 19, rx=1.5, fill="#EEF0F2")
        ic.rect(gx, gy, 34, 4.5, rx=1.5, fill=col)
        ic.rect(gx + 2, gy + 6.5, 30, 10.5, fill="#1E2A36")
        ic.rect(gx + 4, gy + 8.5, 12, 1.4, fill="#7CF7A6", opacity=0.8)
        ic.rect(gx + 4, gy + 11.5, 18, 1.4, fill="#7CF7A6", opacity=0.5)
    ic.rect(101, 77, 34, 19, rx=1.5, fill="none", stroke="#EEF0F2", stroke_opacity=0.55, stroke_dasharray="3 2")
    ic.path("M118 82v9M113.5 86.5h9", stroke="#EEF0F2", stroke_opacity=0.7, stroke_width=1.6)
    ic.path("M59 52a2 2 0 0 1 2-2h46L74 100H61a2 2 0 0 1-2-2z", fill=glare(ic))
    # the plate
    ic.rect(150, 48, 52, 28, rx=2, fill=ic.lin([(0, "#2B3138"), (1, "#16191C")]))
    ic.text("virt-manager", 176, 59, 7.6, font="sans-semibold", anchor="middle", fill="#EEF0F2")
    ic.text("QEMU·KVM", 176, 70, 7, font="mono-semibold", anchor="middle", spacing=0.4, fill="#F2B33D")
    for k, col in enumerate(("#7CF7A6", "#5AB0FF", "#F2B33D")):
        lx = 158 + k * 11
        ic.circle(lx, 88, 3.4, fill="#16191C")
        ic.circle(lx, 88, 2.4, fill=col)
        ic.circle(lx - 0.7, 87.3, 0.8, fill="#fff", opacity=0.8)
    ic.rect(150, 96, 52, 6, rx=1, fill="#2B3138")
    ic.rect(152, 97.5, 18, 3, rx=1, fill="#5D636B")
    # the middle unit, 2U: a row of drives
    _rack_unit(ic, 114, 42)
    _drives(ic, 54, 120, 8)
    _drives(ic, 54, 136, 8)
    # the bottom unit, 2U: vents and a power switch
    _rack_unit(ic, 160, 42)
    for vx in range(56, 168, 6):
        ic.rect(vx, 168, 3, 26, rx=1.5, fill="#2B3138")
        ic.rect(vx + 0.4, 168.4, 2.2, 1, fill="#000", opacity=0.4)
    ic.circle(188, 181, 8, fill="#2B3138")
    ic.circle(188, 181, 6, fill=ic.rad([(0, "#5E656E"), (1, "#20252B")], cx=0.35, cy=0.3, r=0.8))
    ic.path("M185 178.4a4 4 0 1 0 6 0M188 176.6v4", fill="none", stroke="#7CF7A6", stroke_width=1.3,
            stroke_linecap="round")


@small("virt-manager")
def virt_manager16(ic):
    tile(ic, "#55708C", "#1F3045")
    ic.rect(1.8, 2, 1.4, 12.4, fill="#16191C")
    ic.rect(12.8, 2, 1.4, 12.4, fill="#16191C")
    ic.rect(2.6, 2.6, 10.8, 5.4, rx=0.5, fill="#C4CAD1")
    ic.rect(3.6, 3.4, 5.4, 3.8, fill="#2F6E9E")
    ic.rect(4.2, 4, 2, 1.4, fill="#EEF0F2")
    ic.rect(6.6, 4, 2, 1.4, fill="#EEF0F2")
    ic.rect(4.2, 5.6, 2, 1.2, fill="#EEF0F2")
    ic.circle(10.8, 5.4, 0.8, fill="#7CF7A6")
    for y in (8.8, 11.6):
        ic.rect(2.6, y, 10.8, 2.2, rx=0.4, fill="#AEB5BD")
        ic.rect(3.6, y + 0.7, 7, 0.8, fill="#3A4048")


# --- VirtualBox: a blue box, a cube, its V pressed in ------------------------

@icon("virtualbox", kind="app", names=["VBox", "indicator-virtual-box", "virtualbox", "virtualbox-ose"],
      title="VirtualBox")
def virtualbox(ic):
    tile(ic, "#5B93D3", "#1D427A")
    shadow(ic, 128, 210, 90, 12)
    T, L, R, C, BL, BR, B = (128, 26), (44, 72), (212, 72), (128, 118), (44, 164), (212, 164), (128, 210)
    ic.poly([L, C, B, BL], fill="#000", opacity=0.25, transform="translate(4 3)")
    ic.poly([C, R, BR, B], fill="#000", opacity=0.25, transform="translate(4 3)")
    top = ic.lin([(0, "#6FB4F2"), (1, "#2F74C6")], 0, 0, 1, 1)
    left = ic.lin([(0, "#2A62AE"), (1, "#173A72")], 0, 0, 1, 1)
    right = ic.lin([(0, "#16305C"), (1, "#0B1A36")], 0, 0, 1, 1)
    ic.poly([T, R, C, L], fill=top)
    ic.poly([T, R, C, L], fill=ic.rad([(0, "#fff", 0.35), (1, "#fff", 0)], cx=0.35, cy=0.3, r=0.6))
    ic.poly([L, C, B, BL], fill=left)
    ic.poly([C, R, BR, B], fill=right)
    # the lid's seam and a band around the box
    ic.poly([(128, 36), (194, 72), (128, 108), (62, 72)], fill="none", stroke="#1F4F92", stroke_width=1.6,
            stroke_linejoin="round", opacity=0.7)
    ic.poly([(128, 37.5), (192, 72.5), (128, 107.5), (64, 72.5)], fill="none", stroke="#BFE2FF", stroke_width=0.8,
            opacity=0.5)
    # the V on the left face, as on the box (face grid 100 x 100)
    with ic.g(transform="matrix(.84 .46 0 .92 44 72)"):
        ic.path("M22 22 H38 L50 62 L62 22 H78 L58 80 H42Z", fill="#0E2550", opacity=0.6, transform="translate(1.5 1.5)")
        ic.path("M22 22 H38 L50 62 L62 22 H78 L58 80 H42Z", fill=ic.lin([(0, "#FFFFFF"), (1, "#C9DCF2")]))
    # the right face: a printed name and a small cube
    with ic.g(transform="matrix(.84 -.46 0 .92 128 118)"):
        ic.text("VirtualBox", 50, 30, 13, font="sans-bold", anchor="middle", fill="#9CC8F5")
        ic.text("x86 · ARM · 7.2", 50, 44, 7, font="mono", anchor="middle", fill="#6E9BD0")
        for k in range(6):
            ic.rect(24 + k * 9, 64, 6, 14, fill="#6E9BD0", opacity=0.5)
    # edges catching the light
    ic.line(*T, *L, stroke="#D4ECFF", stroke_width=2, stroke_linecap="round")
    ic.line(*T, *R, stroke="#A9D2FA", stroke_width=1.5, stroke_linecap="round", opacity=0.8)
    ic.line(*L, *C, stroke="#CFE7FF", stroke_width=1.5, opacity=0.8)
    ic.line(*C, *R, stroke="#7DB2EA", stroke_width=1.2, opacity=0.7)
    ic.line(*C, *B, stroke="#4C7FC0", stroke_width=1.5, opacity=0.8)
    ic.line(*L, *BL, stroke="#7DB2EA", stroke_width=1.5, opacity=0.6)


@small("virtualbox")
def virtualbox16(ic):
    tile(ic, "#5B93D3", "#1D427A")
    ic.poly([(8, 1.5), (14, 4.8), (8, 8), (2, 4.8)], fill="#6FB4F2")
    ic.poly([(2, 4.8), (8, 8), (8, 14.5), (2, 11.3)], fill="#2A62AE")
    ic.poly([(8, 8), (14, 4.8), (14, 11.3), (8, 14.5)], fill="#14305C")
    ic.path("M3.4 7 L5 11.6 L6.6 7.9", fill="none", stroke="#fff", stroke_width=1.1, stroke_linejoin="round")


# --- Remote Viewer: a monitor with a set of rabbit ears, another desk on it --

@icon("virt-viewer", kind="app",
      names=["krdc", "org.kde.krdc", "org.virt_manager.virt-viewer", "virt-viewer", "yast-remote"],
      title="Remote Viewer")
def virt_viewer(ic):
    tile(ic, "#3F8A5C", "#163A25")
    shadow(ic, 128, 214, 84, 11)
    # the antenna: two telescopic rods on a little base
    for a, ln in ((-32, 46), (28, 52)):
        with ic.g(transform=rot(a, 128, 64)):
            ic.rect(126.4, 64 - ln, 3.2, ln, rx=1.2, fill=steel(ic))
            ic.rect(125.6, 64 - ln * 0.55, 4.8, ln * 0.55, rx=1.6, fill=steel(ic))
            ic.rect(125, 64 - ln * 0.28, 6, ln * 0.28, rx=2, fill=steel(ic))
            ic.circle(128, 64 - ln, 4, fill=steel(ic, False))
    ic.path("M108 70 Q108 56 128 56 Q148 56 148 70Z", fill=graphite(ic))
    ic.path("M112 62 Q118 58 128 58", fill="none", stroke="#fff", stroke_opacity=0.3, stroke_width=1.2)
    # signal
    for r, o in ((8, 0.9), (13, 0.6), (18, 0.35)):
        x, y = polar(128, 64, 50, 28)
        x, y = x + 4, y + 12
        ic.path(f"M{x + r * 0.6:.1f} {y - r * 0.8:.1f}A{r} {r} 0 0 1 {x + r * 0.8:.1f} {y + r * 0.6:.1f}",
                fill="none", stroke="#C9F7D6", stroke_width=2.4, stroke_linecap="round", opacity=o)
    # the stand, the monitor
    ic.path("M114 182h28l6 22h-40z", fill=steel(ic))
    ic.rect(88, 200, 80, 9, rx=4.5, fill=steel(ic))
    ic.rect(28, 68, 200, 120, rx=12, fill="#000", opacity=0.3, transform="translate(3 4)")
    ic.rect(28, 68, 200, 120, rx=12, fill=ic.lin([(0, "#4A5058"), (0.1, "#30353B"), (1, "#16191C")]))
    ic.rect(28.75, 68.75, 198.5, 118.5, rx=11.25, fill="none", stroke="#fff", stroke_opacity=0.14, stroke_width=1.5)
    sx, sy, sw, sh = 38, 78, 180, 96
    ic.rect(sx, sy, sw, sh, rx=4, fill=ic.lin([(0, "#E9A24F"), (0.5, "#C35B5A"), (1, "#4C2E6A")], 0, 0, 1, 1))
    ic.path(f"M{sx} {sy + 70} Q100 {sy + 48} 150 {sy + 64} T{sx + sw} {sy + 56} V{sy + sh} H{sx}Z", fill="#2C1E46",
            opacity=0.7)
    # the remote desktop: its own top bar, a window, a pointer
    ic.rect(sx, sy, sw, 9, fill="#14161A", opacity=0.85)
    ic.text("lab-pc:0 · remote", sx + 6, sy + 6.6, 5.4, font="mono-semibold", fill="#E8EAED")
    ic.text("14:02", sx + sw - 6, sy + 6.6, 5.4, font="mono-semibold", anchor="end", fill="#E8EAED")
    ic.rect(62, 96, 92, 60, rx=3, fill="#000", opacity=0.3, transform="translate(2 3)")
    ic.rect(62, 96, 92, 60, rx=3, fill="#F2F3F5")
    ic.rect(62, 96, 92, 10, rx=3, fill="#D6DADF")
    ic.rect(62, 103, 92, 3, fill="#D6DADF")
    ic.text("Report.odt", 108, 103.4, 5.4, font="sans-semibold", anchor="middle", fill="#4A525B")
    for i, w in enumerate((70, 78, 64, 74, 40)):
        ic.rect(70, 112 + i * 8, w, 2.6, rx=1.3, fill="#A6ADB5")
    ic.rect(162, 92, 44, 30, rx=3, fill="#1E2328")
    ic.text("$ top", 166, 102, 5.4, font="mono-semibold", fill="#7CF7A6")
    ic.text("load 0.42", 166, 110, 5.4, font="mono", fill="#7CF7A6", opacity=0.7)
    cursor(ic, 140, 140, 1.0)
    ic.path(f"M{sx} {sy + 4}a4 4 0 0 1 4-4h92L{sx + 30} {sy + sh}H{sx + 4}a4 4 0 0 1-4-4z", fill=glare(ic, 0.9))
    ic.circle(128, 181, 2, fill="#7CF7A6", opacity=0.8)


@small("virt-viewer")
def virt_viewer16(ic):
    tile(ic, "#3F8A5C", "#163A25")
    ic.path("M8 5 L5 1.5 M8 5 L11.2 1.8", stroke="#C3C8CE", stroke_width=0.8, stroke_linecap="round")
    ic.rect(1.5, 5, 13, 8, rx=1, fill="#2A2F35")
    ic.rect(2.5, 6, 11, 6, rx=0.4, fill="#D27A55")
    ic.rect(4, 7.3, 5.5, 3.6, rx=0.3, fill="#F2F3F5")
    ic.path("M10 8.4 V12 L11 11 L11.8 12.3", fill="#fff", stroke="#111", stroke_width=0.4)
    ic.rect(6.5, 13, 3, 1.4, fill="#9AA1A9")


# --- GParted: a platter cut into partitions, one lifted out ------------------

PARTS = [  # from, to, light, dark, label
    (4, 150, "#B6E36A", "#5E9E2A", "ext4"),
    (150, 228, "#7FD3F0", "#2C8FB8", "ntfs"),
    (228, 268, "#F2867A", "#C0392B", "swap"),
    (268, 318, "#D7DBDF", "#9AA2AA", ""),
]


@icon("gparted", kind="app", names=["gparted"], title="GParted")
def gparted(ic):
    tile(ic, "#6E5E52", "#2E241D")
    cx, cy, R, r = 120, 128, 84, 18
    shadow(ic, 128, 214, 96, 12)
    # the platter, mirror steel
    ic.circle(cx + 3, cy + 5, R + 2, fill="#000", opacity=0.3)
    ic.circle(cx, cy, R + 2, fill=ic.lin([(0, "#EEF1F4"), (0.4, "#9DA5AE"), (0.6, "#D7DCE1"), (1, "#5F6770")],
                                       0, 0, 1, 1))
    ic.circle(cx, cy, R + 1.2, fill="none", stroke="#fff", stroke_width=1.2, opacity=0.8)
    ic.path(sector(cx, cy, R - 4, r + 2, 318, 364), fill="#3A3F45")
    # the partitions, enamel on the platter
    for a1, a2, light, dark, label in PARTS:
        ic.path(sector(cx, cy, R - 4, r + 2, a1 + 1.2, a2 - 1.2),
                fill=ic.lin([(0, light), (1, dark)], 0, 0, 1, 1))
        ic.path(sector(cx, cy, R - 4, R - 7, a1 + 1.2, a2 - 1.2), fill="#fff", opacity=0.25)
        if label:
            mid = (a1 + a2) / 2
            x, y = polar(cx, cy, 54, mid)
            ic.text(label, x, y + 3.5, 11, font="mono-semibold", anchor="middle", fill="#1E2328", opacity=0.75)
    # the hub
    ic.circle(cx, cy, r + 2, fill=steel(ic, False))
    ic.circle(cx, cy, r - 6, fill="#2A2F35")
    ic.circle(cx, cy, r - 9, fill="#14171A")
    for k in range(6):
        x, y = polar(cx, cy, r - 2, k * 60 + 30)
        ic.circle(x, y, 1.4, fill="#5F6770")
    # the reflection across the platter
    ic.path(f"M{cx - R + 10} {cy - 30}A{R} {R} 0 0 1 {cx - 20} {cy - R + 6}L{cx - 8} {cy - 16}Z", fill="#fff",
            opacity=0.22)
    # the slice lifted out: a new partition, being made
    ox, oy = 14, -8
    a1, a2 = 322, 360
    with ic.g(transform=f"translate({ox} {oy})"):
        ic.path(sector(cx, cy, R - 4, r + 2, a1, a2), fill="#000", opacity=0.35, transform="translate(4 6)")
        ic.path(sector(cx, cy, R + 2, r + 2, a1, a2), fill=ic.lin([(0, "#EEF1F4"), (1, "#7F8790")], 0, 0, 1, 1))
        ic.path(sector(cx, cy, R - 4, r + 6, a1 + 1.4, a2 - 1.4), fill=ic.lin([(0, "#FFD86A"), (1, "#E09A1C")],
                                                                               0, 0, 1, 1))
        ic.path(sector(cx, cy, R + 1, R - 1, a1, a2), fill="#fff", opacity=0.8)
        x, y = polar(cx, cy, 58, (a1 + a2) / 2)
        ic.text("new", x, y + 3, 9, font="mono-semibold", anchor="middle", fill="#5A3A08",
                transform=rot(-18, x, y))
    # the label tape
    ic.rect(150, 182, 72, 22, rx=2, fill="#000", opacity=0.25, transform="translate(2 2)")
    ic.rect(150, 182, 72, 22, rx=2, fill=paper(ic, "cream"), transform=rot(-4, 186, 193))
    ic.text("/dev/sda", 186, 197, 11, font="mono-semibold", anchor="middle", fill="#2A2F35",
            transform=rot(-4, 186, 193))


@small("gparted")
def gparted16(ic):
    tile(ic, "#6E5E52", "#2E241D")
    ic.circle(7.5, 8.5, 6, fill="#C3C8CE")
    ic.path(sector(7.5, 8.5, 5.4, 1.4, 4, 150), fill="#8CC83E")
    ic.path(sector(7.5, 8.5, 5.4, 1.4, 154, 228), fill="#3BA6D4")
    ic.path(sector(7.5, 8.5, 5.4, 1.4, 232, 300), fill="#E0574A")
    ic.path(sector(8.8, 7.4, 6, 1.4, 320, 360), fill="#F2B83A")


# --- Disks: an external drive standing on the desk, its light on ------------

@icon("gnome-disks", kind="app", names=["gnome-disks", "matepalimpsest", "org.gnome.DiskUtility", "palimpsest"],
      title="Disks")
def gnome_disks(ic):
    tile(ic, "#6B7682", "#262B32")
    shadow(ic, 132, 210, 94, 12)
    # the cable, out of the back, along the desk
    ic.path("M206 160 C236 168 238 196 214 204 C196 210 176 206 160 212", fill="none", stroke="#1A1C20",
            stroke_width=6, stroke_linecap="round")
    ic.path("M206 160 C236 168 238 196 214 204", fill="none", stroke="#fff", stroke_opacity=0.15, stroke_width=1.5)
    # the box: top, side, front
    ic.poly([(36, 92), (72, 56), (222, 56), (186, 92)], fill=ic.lin([(0, "#F1F3F5"), (1, "#B4BBC3")], 0, 0, 1, 1))
    ic.poly([(186, 92), (222, 56), (222, 168), (186, 204)], fill=ic.lin([(0, "#7D8691"), (1, "#40474F")]))
    ic.rect(36, 92, 150, 112, fill=ic.lin([(0, "#DDE1E5"), (0.6, "#B9C0C8"), (1, "#8D959F")], 0, 0, 1, 1))
    ic.line(36, 92.6, 186, 92.6, stroke="#fff", stroke_width=1.5)
    ic.line(36.6, 92, 36.6, 204, stroke="#fff", stroke_width=1, opacity=0.7)
    ic.line(72, 56.6, 222, 56.6, stroke="#fff", stroke_width=1.2, opacity=0.8)
    ic.line(186, 92, 222, 56, stroke="#fff", stroke_width=1, opacity=0.6)
    # brushed lines on the top
    for k in range(7):
        y = 62 + k * 4.5
        ic.line(72 - (y - 56) + 6, y, 216 - (y - 56), y, stroke="#fff", stroke_opacity=0.25, stroke_width=0.6)
    # the front: a recessed panel, vents, the label, the light
    ic.rect(46, 102, 130, 92, rx=4, fill=ic.lin([(0, "#2E333A"), (1, "#16191D")]))
    ic.rect(46.5, 102.5, 129, 91, rx=3.5, fill="none", stroke="#000", stroke_opacity=0.4)
    ic.line(48, 194.5, 174, 194.5, stroke="#fff", stroke_opacity=0.35, stroke_width=1)
    for k in range(9):
        ic.rect(56, 112 + k * 6, 46, 2.6, rx=1.3, fill="#0B0D10")
        ic.rect(56, 114.2 + k * 6, 46, 0.6, fill="#fff", opacity=0.1)
    ic.text("DISKS", 114, 128, 12, font="sans-bold", spacing=1.6, fill="#E7EAED")
    ic.text("4 TB", 114, 142, 9, font="mono-semibold", fill="#9AA3AC")
    ic.text("USB 3.2", 114, 152, 6.5, font="mono", fill="#7C858F")
    # the activity light, glowing
    ic.circle(160, 178, 13, fill=ic.rad([(0, "#7FD8FF", 0.7), (1, "#7FD8FF", 0)]))
    ic.circle(160, 178, 4.2, fill="#0B0D10")
    ic.circle(160, 178, 3.2, fill=ic.rad([(0, "#FFFFFF"), (0.5, "#9BE3FF"), (1, "#2A9BD8")]))
    ic.text("ACT", 148, 181, 6, font="mono-semibold", anchor="end", fill="#7C858F")
    # feet
    ic.rect(48, 204, 20, 4, rx=2, fill="#1A1C20")
    ic.rect(154, 204, 20, 4, rx=2, fill="#1A1C20")


@small("gnome-disks")
def gnome_disks16(ic):
    tile(ic, "#6B7682", "#262B32")
    ic.poly([(2, 5.5), (4.5, 3), (14, 3), (11.5, 5.5)], fill="#E3E6EA")
    ic.poly([(11.5, 5.5), (14, 3), (14, 11), (11.5, 13.5)], fill="#5F6770")
    ic.rect(2, 5.5, 9.5, 8, fill="#BFC5CC")
    ic.rect(3, 6.5, 7.5, 6, rx=0.5, fill="#22262B")
    ic.circle(9, 11, 1.1, fill="#7FD8FF")


# --- Timeshift: an hourglass on a turned wooden stand, a snapshot plate -----

@icon("timeshift", kind="app", names=["timeshift"], title="Timeshift")
def timeshift(ic):
    tile(ic, "#6A4A8E", "#2A1A40")
    shadow(ic, 128, 214, 84, 11)
    cx = 128
    plate = wood(ic, "#C48A55", "#6E3E1A")
    edge = ic.lin([(0, "#9A6234"), (1, "#4E2A10")])
    # the back posts
    post = ic.lin([(0, "#6E3E1A"), (0.35, "#D9A06A"), (1, "#5A3012")], 0, 0, 1, 0)
    # the glass: two bulbs and the sand
    bulbs = ("M86 50 C86 92 118 104 122 124 C118 144 86 156 86 196 H170 C170 156 138 144 134 124 "
             "C138 104 170 92 170 50Z")
    ic.path(bulbs, fill=ic.lin([(0, "#F2F8FF", 0.34), (0.6, "#C9DDF0", 0.16), (1, "#2A1A40", 0.3)], 0, 0, 1, 0))
    sand = ic.lin([(0, "#F6D58A"), (1, "#D49A3C")], 0, 0, 1, 1)
    glass = ic.clip(f'<path d="{bulbs}"/>')
    with ic.g(clip_path=glass):
        ic.path("M80 84 Q128 90 176 84 V130 H80Z", fill=sand)
        ic.path("M80 84 Q128 90 176 84", fill="none", stroke="#FFF0C4", stroke_width=1.2, opacity=0.8)
        ic.rect(127, 118, 2.4, 70, fill="#E8B860")
        ic.path("M80 196 L80 184 Q110 160 128 156 Q146 160 176 184 V196Z", fill=sand)
        ic.path("M100 172 Q118 160 128 157", fill="none", stroke="#FFF0C4", stroke_width=1, opacity=0.7)
    ic.path(bulbs, fill="none", stroke="#E9F2FA", stroke_opacity=0.55, stroke_width=1.6)
    ic.path("M94 58 C94 86 112 100 116 112", fill="none", stroke="#fff", stroke_width=3, stroke_linecap="round",
            opacity=0.55)
    ic.path("M94 190 C94 166 108 152 114 146", fill="none", stroke="#fff", stroke_width=2.4, stroke_linecap="round",
            opacity=0.35)
    # the front posts
    for x in (66, 190):
        ic.rect(x - 6, 44, 12, 152, rx=5, fill=post)
        for y in (60, 124, 180):
            ic.ellipse(x, y, 8.5, 4, fill=post)
            ic.ellipse(x - 2, y - 1, 4, 1.2, fill="#fff", opacity=0.35)
    # the top and the base, turned wood
    for y in (30, 194):
        ic.rect(46, y + 4, 164, 14, rx=6, fill=edge)
        ic.rect(46, y, 164, 14, rx=6, fill=plate)
        ic.line(52, y + 1, 204, y + 1, stroke="#F2C795", stroke_width=1.4, opacity=0.8)
    # the brass plate on the base: the app, a snapshot's date, a turn-back arrow
    ic.rect(88, 196, 80, 12, rx=2, fill=brass(ic))
    ic.rect(88.5, 196.5, 79, 11, rx=1.5, fill="none", stroke="#5A3E12", stroke_opacity=0.5)
    ic.text("TIMESHIFT", 128, 205, 7, font="mono-semibold", anchor="middle", spacing=1.4, fill="#4A3210")
    # a snapshot tag hung from the top
    ic.path("M196 44 Q204 56 202 70", fill="none", stroke="#E9DCC0", stroke_width=1.2)
    with ic.g(transform=rot(10, 206, 88)):
        ic.path("M190 72 h32 v34 h-32z M190 72 l6 -6 h20 l6 6z", fill=paper(ic, "cream"))
        ic.circle(206, 70, 2, fill="#6A4A8E")
        # the turn-back arrow, drawn
        ic.path("M212 90 A7 7 0 1 1 205 83", fill="none", stroke="#6A4A8E", stroke_width=2, stroke_linecap="round")
        ic.path("M204 79 L209 83 L204 87Z", fill="#6A4A8E")
        ic.text("30.10", 206, 102, 6.5, font="mono-semibold", anchor="middle", fill="#3A2A4E")


@small("timeshift")
def timeshift16(ic):
    tile(ic, "#6A4A8E", "#2A1A40")
    ic.rect(3, 2, 10, 1.6, rx=0.6, fill="#B47A48")
    ic.rect(3, 12.4, 10, 1.6, rx=0.6, fill="#B47A48")
    ic.path("M4.6 3.6 C4.6 6.4 7.4 7 7.6 8 C7.4 9 4.6 9.6 4.6 12.4 H11.4 C11.4 9.6 8.6 9 8.4 8 "
            "C8.6 7 11.4 6.4 11.4 3.6Z", fill="#E9F2FA", opacity=0.35)
    ic.path("M5.6 5 H10.4 C10 6.4 8.6 7 8 7.6 C7.4 7 6 6.4 5.6 5Z", fill="#F2C460")
    ic.path("M5 12.4 C5.6 10.6 7 10 8 9.8 C9 10 10.4 10.6 11 12.4Z", fill="#F2C460")
    ic.rect(3.6, 3.6, 1, 8.8, fill="#8A5530")
    ic.rect(11.4, 3.6, 1, 8.8, fill="#8A5530")
