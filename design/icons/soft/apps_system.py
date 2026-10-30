"""The soft drawings of the "system" batch: Steam, Lutris, Heroic,
Bottles, Virtual Machine Manager, VirtualBox, Remote Viewer, GParted,
Disks and Timeshift. The objects of drawings/apps_system.py with about
half the detail, no text."""

import math

from lib import bar, polar, soft, soft_shadow, tile, two

STEEL = ("#AEB4BB", "#8D949C")
BRASS = ("#E2B45E", "#B88433")


def rot(deg, cx, cy):
    return f"rotate({deg:g} {cx:g} {cy:g})"


def sector(cx, cy, r_out, r_in, a1, a2):
    """An annular sector from angle a1 to a2 (clockwise, 0 up)."""
    large = 1 if (a2 - a1) % 360 > 180 else 0
    x1, y1 = polar(cx, cy, r_out, a1)
    x2, y2 = polar(cx, cy, r_out, a2)
    x3, y3 = polar(cx, cy, r_in, a2)
    x4, y4 = polar(cx, cy, r_in, a1)
    return (f"M{x1:.1f} {y1:.1f}A{r_out} {r_out} 0 {large} 1 {x2:.1f} {y2:.1f}"
            f"L{x3:.1f} {y3:.1f}A{r_in} {r_in} 0 {large} 0 {x4:.1f} {y4:.1f}Z")


@soft("steam")
def steam(ic):
    tile(ic, "#35648A", "#111A27")
    soft_shadow(ic, 128, 214, 96, 12)
    cx, cy = 142, 112
    ic.circle(cx, cy, 86, fill=two(ic, "#FFFFFF", "#B9C2CC"))
    ic.circle(cx, cy, 74, fill="#0B1118")
    ic.circle(cx, cy, 70, fill=two(ic, "#2E4A66", "#14202E"))
    ic.path(sector(cx, cy, 70, 38, 137, 223), fill="#466A8E")
    for k in range(10):
        a = k * 360 / 10 + 18
        if 128 < a % 360 < 232:
            continue
        x1, y1 = polar(cx, cy, 20, a - 7)
        x2, y2 = polar(cx, cy, 68, a - 3.5)
        x3, y3 = polar(cx, cy, 68, a + 3.5)
        x4, y4 = polar(cx, cy, 20, a + 7)
        ic.poly([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], fill="#3E6084")
    ic.circle(cx, cy, 22, fill="#2E4A66")
    px, py, kx, ky = 164, 92, 62, 178
    ang = math.degrees(math.atan2(ky - py, kx - px))
    length = math.hypot(kx - px, ky - py)
    with ic.g(transform=f"translate({px} {py}) rotate({ang:.2f})"):
        ic.rect(0, -11, length, 22, rx=11, fill=two(ic, "#F2F4F6", "#B9C2CC"))
    ic.circle(px, py, 32, fill=two(ic, "#FFFFFF", "#B9C2CC"))
    ic.circle(px, py, 22, fill="#14202E")
    ic.circle(px, py, 15, fill=two(ic, "#FFFFFF", "#C9D0D8"))
    ic.circle(kx, ky, 17, fill=two(ic, "#FFFFFF", "#B9C2CC"))
    ic.circle(kx, ky, 9, fill="#14202E")


def _otter(ic, cx, cy, s, body, dark):
    """Lutris's curled otter, simplified: the body round to the tail, the
    head at the top right, its snout, an eye."""
    def band(t0, t1, f0, f1, n=32):
        out, back = [], []
        for i in range(n + 1):
            t = t0 + (t1 - t0) * i / n
            a = 50 + t * 300
            w = s * (0.86 * (1 - t) ** 0.75 + 0.12)
            r = s * (1.0 - 0.1 * t)
            out.append(polar(cx, cy, r + w / 2 - w * f0, a))
            back.append(polar(cx, cy, r + w / 2 - w * f1, a))
        return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in out + back[::-1]) + "Z"
    ic.path(band(0, 1, 0, 1), fill=body, stroke=body, stroke_width=2, stroke_linejoin="round")
    hx, hy = polar(cx, cy, s * 0.95, 40)
    hr = s * 0.5
    ic.ellipse(hx, hy, hr * 1.02, hr * 0.9, fill=body, transform=rot(24, hx, hy))
    sx, sy = hx + hr * 0.92, hy + hr * 0.25
    ic.ellipse(sx, sy, hr * 0.52, hr * 0.4, fill="#FFE6B8", transform=rot(18, sx, sy))
    ic.ellipse(sx + hr * 0.42, sy - hr * 0.1, hr * 0.16, hr * 0.13, fill=dark)
    ic.circle(hx - hr * 0.5, hy - hr * 0.6, hr * 0.28, fill=body)
    ic.circle(hx + hr * 0.2, hy - hr * 0.22, hr * 0.15, fill=dark)


@soft("lutris")
def lutris(ic):
    tile(ic, "#E08A35", "#8A3E10")
    soft_shadow(ic, 128, 214, 90, 12)
    cx, cy = 128, 118
    ic.circle(cx, cy + 6, 90, fill="#5D666F")
    ic.circle(cx, cy, 90, fill=two(ic, "#F4F6F8", "#A3ACB5"))
    ic.circle(cx, cy, 76, fill=two(ic, "#E4E8EC", "#AEB6BE"))
    ic.circle(cx, cy, 54, fill="#5D666F")
    ic.circle(cx, cy, 50, fill=two(ic, "#3A7AC6", "#1A4280"))
    _otter(ic, cx - 4, cy + 4, 28, "#F59A32", "#2A1A10")


SHIELD = "M{l} {t}H{r}V{m}C{r} {c1} {c2} {c3} {x} {b}C{c4} {c3} {l} {c1} {l} {m}Z"


def shield_path(x, t, w, h, rad=0):
    l, r = x - w / 2, x + w / 2
    m = t + h * 0.38
    return SHIELD.format(l=l, t=t, r=r, m=f"{m:.1f}", c1=f"{t + h * 0.72:.1f}", c2=f"{x + w * 0.24:.1f}",
                         c3=f"{t + h * 0.9:.1f}", c4=f"{x - w * 0.24:.1f}", x=x, b=t + h)


@soft("heroic")
def heroic(ic):
    tile(ic, "#3B3E86", "#141633")
    soft_shadow(ic, 128, 216, 80, 11)
    x = 124
    ic.path(shield_path(x, 38, 160, 174), fill=two(ic, "#E4E8EC", "#8D949C"), stroke="#C9CFD5", stroke_width=6,
            stroke_linejoin="round")
    ic.path(shield_path(x, 49, 138, 151), fill=two(ic, "#2C6FD6", "#16347A"))
    inner = ic.clip(f'<path d="{shield_path(x, 49, 138, 151)}"/>')
    with ic.g(clip_path=inner):
        ic.path(f"M{x - 80} 112 L{x} 150 L{x + 80} 112 V138 L{x} 176 L{x - 80} 138Z", fill="#1CC4E8")
    with ic.g(transform=rot(-38, 128, 124)):
        bx = 128
        ic.path(f"M{bx - 8} 96 L{bx - 8} 218 L{bx} 236 L{bx + 8} 218 L{bx + 8} 96Z", fill=two(ic, "#F2F4F6", "#B9C2CC"),
                stroke_linejoin="round")
        ic.path(f"M{bx} 96 L{bx} 236 L{bx + 8} 218 L{bx + 8} 96Z", fill="#8D949C", opacity=0.6)
        ic.rect(bx - 28, 86, 56, 12, rx=6, fill=two(ic, *BRASS))
        ic.rect(bx - 6, 52, 12, 36, rx=4, fill="#5A2E18")
        ic.circle(bx, 46, 9, fill=two(ic, *BRASS))
    ic.path("M48 172 L68 164 L70 188 L50 192 L58 181Z", fill="#9E2A22", stroke="#9E2A22", stroke_width=3,
            stroke_linejoin="round")
    ic.path("M208 172 L188 164 L186 188 L206 192 L198 181Z", fill="#9E2A22", stroke="#9E2A22", stroke_width=3,
            stroke_linejoin="round")
    ic.path("M64 160 Q128 176 192 160 L192 184 Q128 200 64 184Z", fill=two(ic, "#F04A3C", "#C02A1E"),
            stroke="#E0402F", stroke_width=3, stroke_linejoin="round")


BOTTLE = ("M112 58 V96 C112 106 84 112 80 132 V196 Q80 208 92 208 H164 Q176 208 176 196 V132 "
          "C172 112 144 106 144 96 V58Z")


@soft("bottles")
def bottles(ic):
    tile(ic, "#3F7B86", "#153840")
    soft_shadow(ic, 128, 210, 66, 10)
    ic.path(BOTTLE, fill=two(ic, "#4E8A5A", "#2A5634"))
    with ic.g(clip_path=ic.clip(f'<path d="{BOTTLE}"/>')):
        ic.rect(70, 122, 120, 100, fill=two(ic, "#7E1C2A", "#4A0A14"))
    ic.rect(84, 142, 88, 54, rx=4, fill=two(ic, "#FFFDF7", "#F1EADB"))
    ic.rect(84, 142, 88, 6, rx=2, fill="#C0282E")
    ic.rect(84, 190, 88, 6, rx=2, fill="#C0282E")
    bar(ic, 100, 158, 56, 8, fill="#3A2A20")
    bar(ic, 108, 174, 40, 6, fill="#A49E91")
    ic.rect(108, 54, 40, 24, rx=5, fill=two(ic, "#E04848", "#9A1A22"))
    ic.rect(113, 28, 30, 30, rx=6, fill=two(ic, "#E9C48C", "#B8844A"))


@soft("virt-manager")
def virt_manager(ic):
    tile(ic, "#55708C", "#1F3045")
    soft_shadow(ic, 128, 214, 96, 11)
    for px in (30, 214):
        ic.rect(px, 30, 12, 178, rx=4, fill="#24282D")
    unit = two(ic, "#E4E8EC", "#A3ABB4")
    for y, h in ((40, 70), (114, 42), (160, 42)):
        ic.rect(38, y, 180, h, rx=6, fill=unit)
    ic.rect(54, 46, 90, 58, rx=6, fill="#2B3138")
    ic.rect(58, 50, 82, 50, rx=4, fill=two(ic, "#3F86B8", "#1E4A72"))
    for gx, gy, col in ((62, 54, "#D7543C"), (100, 54, "#56B567"), (62, 77, "#E8A33A")):
        ic.rect(gx, gy, 34, 19, rx=3, fill="#EEF0F2")
        ic.rect(gx, gy, 34, 6, rx=3, fill=col)
    ic.path("M117 81v12M111 87h12", stroke="#EEF0F2", stroke_width=3, stroke_linecap="round")
    ic.rect(152, 50, 52, 26, rx=4, fill="#24282D")
    for k, col in enumerate(("#7CF7A6", "#5AB0FF", "#F2B33D")):
        ic.circle(162 + k * 16, 90, 4.5, fill=col)
    for k in range(5):
        ic.rect(52 + k * 30, 122, 26, 26, rx=4, fill="#3A4048")
        ic.circle(52 + k * 30 + 20, 135, 2.5, fill="#7CF7A6" if k % 2 else "#5AB0FF")
    for vx in range(56, 164, 12):
        ic.rect(vx, 168, 6, 26, rx=3, fill="#3A4048")
    ic.circle(190, 181, 10, fill="#2B3138")
    ic.path("M186 177.5a5.5 5.5 0 1 0 8 0M190 174.5v6", fill="none", stroke="#7CF7A6", stroke_width=2.4,
            stroke_linecap="round")


@soft("virtualbox")
def virtualbox(ic):
    tile(ic, "#5B93D3", "#1D427A")
    soft_shadow(ic, 128, 210, 90, 12)
    T, L, R, C, BL, BR, B = (128, 26), (44, 72), (212, 72), (128, 118), (44, 164), (212, 164), (128, 210)
    j = dict(stroke_linejoin="round", stroke_width=6)
    ic.poly([T, R, C, L], fill=two(ic, "#7ABCF4", "#3E82D0"), stroke="#5EA0E4", **j)
    ic.poly([L, C, B, BL], fill=two(ic, "#2A62AE", "#1A4280"), stroke="#2252A0", **j)
    ic.poly([C, R, BR, B], fill=two(ic, "#18345E", "#0E2242"), stroke="#132C52", **j)
    with ic.g(transform="matrix(.84 .46 0 .92 44 72)"):
        ic.path("M22 22 H38 L50 62 L62 22 H78 L58 80 H42Z", fill="#F2F7FD", stroke="#F2F7FD", stroke_width=3,
                stroke_linejoin="round")
    with ic.g(transform="matrix(.84 -.46 0 .92 128 118)"):
        bar(ic, 18, 22, 64, 10, fill="#9CC8F5")
        bar(ic, 28, 40, 44, 6, fill="#6E9BD0")


def _cursor(ic, x, y, s=1.0):
    ic.path("M0 0V17L4.2 13.2 7 19.5 9.6 18.4 6.9 12.3H12.4Z", fill="#fff", stroke="#111", stroke_width=1.4,
            stroke_linejoin="round", transform=f"translate({x:g} {y:g}) scale({s:g})")


@soft("virt-viewer")
def virt_viewer(ic):
    tile(ic, "#3F8A5C", "#163A25")
    soft_shadow(ic, 128, 214, 84, 11)
    for a, ln in ((-32, 46), (28, 52)):
        with ic.g(transform=rot(a, 128, 64)):
            ic.rect(125.5, 64 - ln, 5, ln, rx=2.5, fill="#AEB4BB")
            ic.circle(128, 64 - ln, 5, fill="#C3C8CE")
    ic.path("M106 70 Q106 54 128 54 Q150 54 150 70Z", fill="#2E3338")
    x, y = polar(128, 64, 50, 28)
    x, y = x + 4, y + 12
    for r, o in ((9, 0.9), (16, 0.55)):
        ic.path(f"M{x + r * 0.6:.1f} {y - r * 0.8:.1f}A{r} {r} 0 0 1 {x + r * 0.8:.1f} {y + r * 0.6:.1f}",
                fill="none", stroke="#C9F7D6", stroke_width=4, stroke_linecap="round", opacity=o)
    ic.path("M114 182h28l6 22h-40z", fill="#8D949C")
    ic.rect(86, 199, 84, 11, rx=5.5, fill=two(ic, *STEEL))
    ic.rect(28, 68, 200, 120, rx=16, fill=two(ic, "#3A4048", "#1A1D21"))
    sx, sy, sw, sh = 38, 78, 180, 96
    ic.rect(sx, sy, sw, sh, rx=6, fill=two(ic, "#E9A24F", "#7A3E6E"))
    with ic.g(clip_path=ic.clip(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="6"/>')):
        ic.path(f"M{sx} {sy + 70} Q100 {sy + 48} 150 {sy + 64} T{sx + sw} {sy + 56} V{sy + sh} H{sx}Z",
                fill="#2C1E46", opacity=0.7)
        ic.rect(sx, sy, sw, 10, fill="#14161A", opacity=0.85)
    ic.rect(62, 96, 92, 60, rx=5, fill="#F2F3F5")
    ic.path("M62 108V101a5 5 0 0 1 5-5h82a5 5 0 0 1 5 5v7z", fill="#D6DADF")
    for i, w in enumerate((64, 72, 50)):
        bar(ic, 70, 116 + i * 11, w, 6, fill="#A6ADB5")
    ic.rect(162, 92, 44, 30, rx=4, fill="#1E2328")
    _cursor(ic, 140, 138, 1.3)


PARTS = [(4, 150, "#A6D85A", "#6EA834"), (150, 228, "#7FD3F0", "#3696C0"),
         (228, 268, "#F2867A", "#C8463A"), (268, 318, "#D7DBDF", "#A7AEB5")]


@soft("gparted")
def gparted(ic):
    tile(ic, "#6E5E52", "#2E241D")
    soft_shadow(ic, 128, 214, 96, 12)
    cx, cy, R, r = 120, 128, 84, 18
    ic.circle(cx, cy, R + 2, fill=two(ic, "#E4E8EC", "#8D949C"))
    ic.path(sector(cx, cy, R - 5, r + 3, 318, 364), fill="#3A3F45")
    for a1, a2, light, dark in PARTS:
        ic.path(sector(cx, cy, R - 5, r + 3, a1 + 1.8, a2 - 1.8), fill=two(ic, light, dark))
    ic.circle(cx, cy, r + 1, fill=two(ic, *STEEL))
    ic.circle(cx, cy, r - 8, fill="#14171A")
    with ic.g(transform="translate(14 -8)"):
        ic.path(sector(cx, cy, R + 2, r + 2, 322, 360), fill=two(ic, "#E4E8EC", "#8D949C"), stroke="#C9CFD5",
                stroke_width=2, stroke_linejoin="round")
        ic.path(sector(cx, cy, R - 5, r + 6, 324, 358), fill=two(ic, "#FFD86A", "#E8A22A"))
    with ic.g(transform=rot(-4, 186, 193)):
        ic.rect(150, 182, 72, 22, rx=4, fill=two(ic, "#FFFDF7", "#F1EADB"))
        bar(ic, 160, 189.5, 50, 7, fill="#6E5E52")


@soft("gnome-disks")
def gnome_disks(ic):
    tile(ic, "#6B7682", "#262B32")
    soft_shadow(ic, 132, 210, 94, 12)
    ic.path("M206 160 C236 168 238 196 214 204 C196 210 176 206 160 212", fill="none", stroke="#1A1C20",
            stroke_width=8, stroke_linecap="round")
    j = dict(stroke_linejoin="round", stroke_width=6)
    ic.poly([(36, 92), (72, 56), (222, 56), (186, 92)], fill="#E4E8EC", stroke="#E4E8EC", **j)
    ic.poly([(186, 92), (222, 56), (222, 168), (186, 204)], fill=two(ic, "#7D8691", "#4A515A"), stroke="#636B75", **j)
    ic.rect(33, 89, 156, 118, rx=6, fill=two(ic, "#D5DAE0", "#99A1AB"))
    ic.rect(46, 102, 130, 92, rx=8, fill=two(ic, "#2E333A", "#16191D"))
    for k in range(5):
        bar(ic, 58, 116 + k * 12, 48, 6, fill="#0B0D10")
    ic.circle(160, 178, 12, fill="#7FD8FF", opacity=0.3)
    ic.circle(160, 178, 5, fill="#9BE3FF")
    ic.rect(48, 205, 22, 5, rx=2.5, fill="#1A1C20")
    ic.rect(152, 205, 22, 5, rx=2.5, fill="#1A1C20")


@soft("timeshift")
def timeshift(ic):
    tile(ic, "#6A4A8E", "#2A1A40")
    soft_shadow(ic, 128, 214, 84, 11)
    bulbs = ("M86 50 C86 92 118 104 122 124 C118 144 86 156 86 196 H170 C170 156 138 144 134 124 "
             "C138 104 170 92 170 50Z")
    ic.path(bulbs, fill="#D9E6F4", opacity=0.3)
    sand = two(ic, "#F6D58A", "#D9A04A")
    with ic.g(clip_path=ic.clip(f'<path d="{bulbs}"/>')):
        ic.path("M80 84 Q128 90 176 84 V130 H80Z", fill=sand)
        ic.rect(126, 118, 4, 70, rx=2, fill="#E8B860")
        ic.path("M80 196 L80 184 Q110 160 128 156 Q146 160 176 184 V196Z", fill=sand)
    ic.path(bulbs, fill="none", stroke="#E9F2FA", stroke_opacity=0.6, stroke_width=2.5)
    for x in (66, 190):
        ic.rect(x - 7, 44, 14, 152, rx=7, fill=two(ic, "#B47A48", "#7A4A22"))
    wood = two(ic, "#C48A55", "#8A5428")
    for y in (28, 192):
        ic.rect(46, y, 164, 18, rx=9, fill=wood)
    ic.rect(92, 195, 72, 12, rx=4, fill=two(ic, *BRASS))
    ic.path("M196 44 Q204 56 202 70", fill="none", stroke="#E9DCC0", stroke_width=2)
    with ic.g(transform=rot(10, 206, 88)):
        ic.path("M190 76 l8-8 h16 l8 8 v28 a4 4 0 0 1-4 4 h-24 a4 4 0 0 1-4-4z", fill=two(ic, "#FFFDF7", "#F1EADB"))
        ic.circle(206, 74, 2.5, fill="#6A4A8E")
        ic.path("M213 92 A8 8 0 1 1 205 84", fill="none", stroke="#6A4A8E", stroke_width=3.2, stroke_linecap="round")
        ic.path("M203 79 L209 84 L203 89Z", fill="#6A4A8E", stroke="#6A4A8E", stroke_width=1.5,
                stroke_linejoin="round")
