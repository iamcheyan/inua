"""Soft drawings, media: Spotify, mpv, Audacity, Kdenlive, Shotcut,
HandBrake, OBS Studio, Sunshine, Moonlight (VLC is in core.py). The same
objects as drawings/apps_media.py, about half the detail, no text."""

import math

from lib import bar, polar, soft, soft_shadow, tile, two


def _f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def _crescent(cx, cy, r, ox, oy, r2):
    """The crescent left of a circle (cx, cy, r) when a circle (ox, oy, r2)
    is taken out of it: path data."""
    dx, dy = ox - cx, oy - cy
    d = math.hypot(dx, dy)
    a = (r * r - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(max(r * r - a * a, 0))
    mx, my = cx + a * dx / d, cy + a * dy / d
    p1 = (mx + h * dy / d, my - h * dx / d)
    p2 = (mx - h * dy / d, my + h * dx / d)
    return (f"M{_f(p1[0])} {_f(p1[1])}A{r} {r} 0 1 0 {_f(p2[0])} {_f(p2[1])}"
            f"A{r2} {r2} 0 0 1 {_f(p1[0])} {_f(p1[1])}Z")


def _ring(cx, cy, r):
    return f"M{_f(cx - r)} {_f(cy)}a{r} {r} 0 1 0 {_f(2 * r)} 0a{r} {r} 0 1 0 {_f(-2 * r)} 0z"


def _sector(cx, cy, r1, r2, a1, a2):
    p1, p2 = polar(cx, cy, r2, a1), polar(cx, cy, r2, a2)
    p3, p4 = polar(cx, cy, r1, a2), polar(cx, cy, r1, a1)
    return (f"M{_f(p1[0])} {_f(p1[1])}A{r2} {r2} 0 0 1 {_f(p2[0])} {_f(p2[1])}"
            f"L{_f(p3[0])} {_f(p3[1])}A{r1} {r1} 0 0 0 {_f(p4[0])} {_f(p4[1])}Z")


def _film(ic, x, y, w, h, frame):
    """A strip of film: its base, a few frames, big sprocket holes."""
    ic.rect(x, y, w, h, fill="#2E1C10")
    k = x + 6
    while k + 24 < x + w:
        ic.rect(k, y + h * 0.24, 22, h * 0.52, rx=3, fill=frame)
        k += 30
    for k in range(int(x) + 4, int(x + w) - 6, 12):
        ic.rect(k, y + 2, 6, 3.5, rx=1.5, fill="#F1E6D2", opacity=0.8)
        ic.rect(k, y + h - 5.5, 6, 3.5, rx=1.5, fill="#F1E6D2", opacity=0.8)


@soft("spotify")
def spotify(ic):
    tile(ic, "#2B3A31", "#0F1712")
    soft_shadow(ic, 130, 216, 92, 11)
    ic.rect(48, 24, 156, 186, rx=20, fill=two(ic, "#3A3D41", "#1C1D20"))
    ic.rect(58, 34, 136, 166, rx=14, fill="#151618")
    # the badge
    bx, by = 126, 78
    ic.circle(bx, by, 38, fill=two(ic, "#AEB4BB", "#8D949C"))
    ic.circle(bx, by, 33, fill="#1DB954")
    with ic.g(transform=f"rotate(8 {bx} {by + 1})", fill="none", stroke="#0E1A12", stroke_linecap="round"):
        for w, y, bow, sw in ((0.62, -0.28, 0.24, 0.19), (0.52, 0.02, 0.2, 0.16), (0.42, 0.29, 0.15, 0.13)):
            s = 33
            ic.path(f"M{_f(bx - w * s)} {_f(by + 1 + y * s + bow * s * 0.35)}"
                    f"Q{bx} {_f(by + 1 + y * s - bow * s)} {_f(bx + w * s)} {_f(by + 1 + y * s + bow * s * 0.35)}",
                    stroke_width=_f(sw * s))
    # the woofer
    wx, wy = 126, 158
    ic.circle(wx, wy, 40, fill=two(ic, "#5A5E64", "#2A2C30"))
    ic.circle(wx, wy, 34, fill="#101113")
    ic.circle(wx, wy, 14, fill=two(ic, "#55595F", "#26282B"))
    for x in (62, 180):
        ic.rect(x, 208, 14, 6, rx=3, fill="#050506")


@soft("mpv")
def mpv(ic):
    tile(ic, "#4B3870", "#1E1434")
    soft_shadow(ic, 128, 216, 96, 13)
    cx, cy = 128, 118
    ic.rect(30, 26, 196, 188, rx=28, fill=two(ic, "#3A3542", "#1C1922"))
    ic.circle(cx, cy, 82, fill=two(ic, "#6B4D9A", "#2F1D4E"))
    ic.circle(cx, cy, 70, fill="#140B22")
    ic.circle(cx, cy, 64, fill=two(ic, "#A877E8", "#6A38B0"))
    ic.circle(cx, cy, 44, fill="#45197E")
    ic.path(f"M{cx - 13} {cy - 24}L{cx + 24} {cy}L{cx - 13} {cy + 24}z", fill="#FFFFFF", stroke="#FFFFFF",
            stroke_width=8, stroke_linejoin="round")


@soft("audacity")
def audacity(ic):
    tile(ic, "#304C7E", "#15233F")
    soft_shadow(ic, 128, 214, 104, 12)
    # the printout, its waveform
    with ic.g(transform="rotate(-3 128 150)"):
        ic.rect(36, 102, 184, 96, rx=8, fill=two(ic, "#FFFFFF", "#ECE8DF"))
        top, bot = [], []
        for k in range(31):
            x = 48 + k * 5.4
            env = 0.3 + 0.7 * abs(math.sin(k * 0.3)) * (0.6 + 0.4 * math.sin(k * 0.1 + 1))
            a = 32 * env * (0.65 + 0.35 * abs(math.sin(k * 1.7)))
            top.append((x, 152 - a))
            bot.append((x, 152 + a * 0.9))
        ic.path("M" + "L".join(f"{_f(x)} {_f(y)}" for x, y in top + bot[::-1]) + "Z",
                fill=two(ic, "#FF8A3D", "#D0303A"), stroke="#F2542D", stroke_width=3, stroke_linejoin="round")
    # the headband
    ic.path("M56 150V112a72 70 0 0 1 144 0V150", fill="none", stroke=two(ic, "#55595F", "#26282B"), stroke_width=14)
    for x in (51, 195):
        ic.rect(x, 106, 10, 46, rx=5, fill=two(ic, "#AEB4BB", "#8D949C"))
    # the cups
    for x, pad in ((24, 66), (180, 172)):
        ic.rect(pad - 6, 136, 24, 70, rx=12, fill="#1A1B1E")
        ic.rect(x, 134, 52, 74, rx=24, fill=two(ic, "#5A96F2", "#1F56B8"))
        ic.rect(x + 12, 150, 28, 42, rx=14, fill="#1F56B8", opacity=0.5)


@soft("kdenlive")
def kdenlive(ic):
    tile(ic, "#34404C", "#121820")
    soft_shadow(ic, 128, 214, 108, 11)
    ic.rect(14, 176, 228, 30, rx=10, fill=two(ic, "#B07A48", "#7A4A22"))
    # the viewer
    ic.rect(100, 22, 56, 22, rx=8, fill=two(ic, "#4F535A", "#2A2C31"))
    ic.path("M64 48a12 12 0 0 1 12-12h104a12 12 0 0 1 12 12v94H64z", fill=two(ic, "#4AA8E8", "#1D63A8"))
    ic.rect(76, 52, 104, 72, rx=8, fill="#0B1E33")
    scr = ic.clip('<rect x="82" y="58" width="92" height="60" rx="4"/>')
    with ic.g(clip_path=scr):
        ic.rect(82, 58, 92, 60, fill=two(ic, "#FFE7B0", "#F2A65A"))
        ic.circle(144, 80, 10, fill="#FFF6DA")
        ic.path("M82 106L102 88L116 98L134 80L174 112V118H82z", fill="#4A2A3A")
    bar(ic, 104, 129, 48, 7, fill="#F4FAFF")
    # the film through the gate
    _film(ic, 10, 150, 236, 26, "#D89A4A")
    ic.rect(88, 144, 80, 36, rx=8, fill=two(ic, "#AEB4BB", "#8D949C"))
    ic.rect(98, 155, 60, 14, rx=4, fill="#1A1E23")
    ic.rect(112, 158, 18, 8, rx=2, fill="#FFE7B0")


@soft("shotcut")
def shotcut(ic):
    tile(ic, "#21557E", "#0D2742")
    soft_shadow(ic, 130, 214, 100, 12)
    cx, cy = 106, 112
    sy = cy + 64
    strip = f"M{cx} {sy}H230l-10 26H{cx}z"
    with ic.g(clip_path=ic.clip(f'<path d="{strip}"/>')):
        _film(ic, cx, sy, 126, 26, "#3A9BC8")
    # the film wound on, seen through the flange's windows
    ic.circle(cx, cy, 72, fill="#3A2618")
    holes = "".join(_sector(cx, cy, 32, 68, a + 14, a + 106) for a in (0, 120, 240))
    ic.path(_ring(cx, cy, 84) + holes, fill=two(ic, "#6FD0F2", "#1D78B0"), fill_rule="evenodd")
    ic.circle(cx, cy, 24, fill=two(ic, "#D4D8DD", "#8D949C"))
    ic.rect(cx - 7, cy - 7, 14, 14, rx=3, fill="#0B1A26", transform=f"rotate(12 {cx} {cy})")
    # scissors, open
    with ic.g(transform="translate(206 112) rotate(14)"):
        for s in (1, -1):
            ic.path("M-5 2Q-7 -30 0 -66Q7 -30 5 2z", fill=two(ic, "#E4E8EC", "#9AA1A9"), transform=f"rotate({s * 11})")
        for s in (-1, 1):
            ic.path(f"M{s * 2} 3 L{s * 8} 13", stroke="#17191D", stroke_width=7, stroke_linecap="round")
            ic.ellipse(s * 12, 26, 10, 14, fill="none", stroke="#17191D", stroke_width=8,
                       transform=f"rotate({s * -14} {s * 12} 26)")
        ic.circle(0, 0, 4.5, fill="#6F767E")


@soft("handbrake")
def handbrake(ic):
    tile(ic, "#2A7A78", "#0E3A3C")
    soft_shadow(ic, 128, 214, 100, 12)
    px, py = 96, 146
    # the crown
    for ang, ln, w, c in ((-44, 46, 13, "#3E8A2E"), (44, 44, 13, "#3E8A2E"), (-22, 62, 14, "#5DB03A"),
                          (22, 58, 14, "#5DB03A"), (0, 78, 14, "#7CC64A")):
        ic.path(f"M{px - w} {py - 44}Q{px - w * 0.5} {py - 44 - ln * 0.55} {px} {py - 44 - ln}"
                f"Q{px + w * 0.5} {py - 44 - ln * 0.55} {px + w} {py - 44}z",
                fill=c, transform=f"rotate({ang} {px} {py - 44})")
    # the body and its diamond rind
    ic.ellipse(px, py, 46, 58, fill=two(ic, "#FFD064", "#D18A1E"))
    with ic.g(clip_path=ic.clip(f'<ellipse cx="{px}" cy="{py}" rx="46" ry="58"/>'),
              stroke="#9A5A10", stroke_opacity=0.5, stroke_width=3, fill="none"):
        for k in range(-3, 4):
            ic.line(px - 60 + k * 26, py - 70, px + 60 + k * 26, py + 70)
            ic.line(px + 60 + k * 26, py - 70, px - 60 + k * 26, py + 70)
    # the drink
    gx, gt, gb = 166, 92, 208
    ic.path(f"M{gx + 8} {gb - 20}L{gx + 26} {gt - 34}l12 -4", fill="none", stroke="#E0283A", stroke_width=7,
            stroke_linecap="round", stroke_linejoin="round")
    ic.path(f"M{gx - 28} {gt + 18}h56l-5.2 {gb - gt - 24}a6 6 0 0 1-6 6h-33.6a6 6 0 0 1-6-6z",
            fill=two(ic, "#FFB23A", "#D0283A"))
    ic.path(f"M{gx - 30} {gt}h60l-6 {gb - gt - 8}a8 8 0 0 1-8 8h-32a8 8 0 0 1-8-8z", fill="#fff", fill_opacity=0.18,
            stroke="#fff", stroke_opacity=0.7, stroke_width=3, stroke_linejoin="round")
    # the slice of lime on the rim
    lx, ly = gx - 28, gt + 2
    ic.path(f"M{lx - 19} {ly}a19 19 0 0 0 38 0z", fill="#4E9A2A", transform=f"rotate(-20 {lx} {ly})")
    ic.path(f"M{lx - 14} {ly}a14 14 0 0 0 28 0z", fill="#D8F08A", transform=f"rotate(-20 {lx} {ly})")


def _obs_mark(ic, cx, cy, r, ground="#302E31", ink="#F4F4F2"):
    ic.circle(cx, cy, r, fill=ground)
    ic.circle(cx, cy, r * 0.86, fill="none", stroke=ink, stroke_width=_f(r * 0.12))
    for k in range(3):
        a = 30 + k * 120
        bx, by = polar(cx, cy, r * 0.38, a)
        tx, ty = polar(cx, cy, r * 0.62, a + 70)
        p1, p2 = polar(bx, by, r * 0.27, a + 90), polar(cx, cy, r * 0.72, a + 105)
        p3, p4 = polar(cx, cy, r * 0.5, a + 80), polar(bx, by, r * 0.27, a - 20)
        ic.circle(bx, by, r * 0.27, fill=ink)
        ic.path(f"M{_f(p1[0])} {_f(p1[1])}Q{_f(tx)} {_f(ty)} {_f(p2[0])} {_f(p2[1])}"
                f"Q{_f(p3[0])} {_f(p3[1])} {_f(p4[0])} {_f(p4[1])}z", fill=ink)


@soft("com.obsproject.Studio")
def obs(ic):
    tile(ic, "#3E4553", "#171A21")
    soft_shadow(ic, 140, 216, 88, 11)
    with ic.g(transform="translate(6 -2)"):
        # the tripod
        for x2 in (104, 168):
            ic.line(136, 194, x2, 214, stroke="#16171A", stroke_width=8, stroke_linecap="round")
        ic.line(136, 194, 136, 216, stroke="#16171A", stroke_width=8, stroke_linecap="round")
        ic.rect(126, 174, 20, 24, rx=3, fill=two(ic, "#AEB4BB", "#8D949C"))
        ic.path("M98 170h76l-8 14h-60z", fill="#2A2C31")
        ic.path("M160 178l52 -18", stroke="#1E2024", stroke_width=8, stroke_linecap="round")
        # the viewfinder and its tally
        ic.rect(126, 42, 82, 40, rx=10, fill=two(ic, "#4A4E55", "#2A2C30"))
        ic.rect(134, 50, 40, 24, rx=5, fill="#2F5F78")
        ic.rect(140, 78, 30, 8, fill="#202226")
        ic.rect(184, 52, 14, 10, rx=4, fill="#FF4A3E")
        # the body
        ic.rect(64, 82, 156, 92, rx=16, fill=two(ic, "#4A4E54", "#24262A"))
        ic.circle(84, 108, 6, fill="#FF3B30")
        bar(ic, 96, 104, 26, 8, fill="#FF5A4F")
        bar(ic, 78, 126, 40, 7, fill="#C9CED4", opacity=0.45)
        bar(ic, 78, 140, 28, 7, fill="#C9CED4", opacity=0.45)
        # OBS's mark
        mx, my = 168, 128
        ic.circle(mx, my, 35, fill=two(ic, "#C9CED4", "#8D949C"))
        _obs_mark(ic, mx, my, 30)
        # the lens
        ic.rect(28, 98, 42, 60, rx=6, fill=two(ic, "#3A3D42", "#18191C"))
        ic.rect(18, 88, 18, 80, rx=8, fill="#0E0F11")
        ic.ellipse(22, 128, 8, 34, fill="#2C2850")


def _sun(ic, cx, cy, r, rays=12, **kw):
    ic.circle(cx, cy, r * 0.54, **kw)
    for k in range(rays):
        a = k * 360 / rays
        p = [polar(cx, cy, r * 0.62, a - 11), polar(cx, cy, r, a), polar(cx, cy, r * 0.62, a + 11)]
        ic.poly(p, stroke_linejoin="round", **kw)


@soft("sunshine")
def sunshine(ic):
    tile(ic, "#2E5B9C", "#13284B")
    soft_shadow(ic, 128, 212, 108, 13)
    with ic.g(transform="translate(-12.8 -14) scale(1.1)"):
        ic.path("M196 150C218 150 220 176 212 200", fill="none", stroke="#1A1B1E", stroke_width=8, stroke_linecap="round")
        # the box: top, side, front
        ic.path("M58 76h160l-18 26H36z", fill="#FFE68A", stroke="#FFE68A", stroke_width=4, stroke_linejoin="round")
        ic.path("M200 102l18 -26v84a10 10 0 0 1-4 8l-14 14z", fill="#C27A0E")
        ic.path("M36 102h164v80H50a14 14 0 0 1-14-14z", fill=two(ic, "#FFD23F", "#E8960E"))
        ic.ellipse(186, 88, 8, 4, fill="#E8A020")
        # the sun pressed into its face
        _sun(ic, 82, 142, 27, fill="#C9700A", stroke="#C9700A", stroke_width=2)
        ic.circle(82, 142, 10, fill="#FFE07A")
        bar(ic, 124, 118, 64, 10, fill="#8A4A00", opacity=0.85)
        bar(ic, 124, 134, 44, 6, fill="#8A4A00", opacity=0.55)
        for x in range(126, 176, 10):
            ic.rect(x, 150, 5, 20, rx=2.5, fill="#9A5600", opacity=0.45)
        ic.circle(190, 160, 4.5, fill="#5CE08A")
        for x in (52, 180):
            ic.rect(x, 182, 14, 6, rx=3, fill="#3A2400")


@soft("moonlight")
def moonlight(ic):
    tile(ic, "#303566", "#10122A")
    for x, y, r in ((44, 52, 2.4), (74, 34, 1.8), (214, 52, 2.2)):
        ic.circle(x, y, r, fill="#fff", opacity=0.6)
    soft_shadow(ic, 128, 214, 102, 12)
    ic.path(_crescent(150, 82, 56, 178, 64, 48), fill=two(ic, "#FFFBEA", "#D8D2BA"))
    # the pad
    ic.path("M74 116H182C210 116 224 138 230 166C236 196 220 212 204 208C190 204 182 186 170 180H86"
            "C74 186 66 204 52 208C36 212 20 196 26 166C32 138 46 116 74 116Z", fill=two(ic, "#555A64", "#202228"))
    dx, dy = 66, 146
    ic.path(f"M{dx - 6} {dy - 18}h12v12h12v12h-12v12h-12v-12h-12v-12h12z", fill="#16171A",
            stroke="#16171A", stroke_width=3, stroke_linejoin="round")
    bx, by = 190, 146
    for (ox, oy), c in (((0, -14), "#7AD7A0"), ((14, 0), "#F08080"), ((0, 14), "#8AB4F8"), ((-14, 0), "#F2D27A")):
        ic.circle(bx + ox, by + oy, 7, fill=c)
    for x in (104, 152):
        ic.circle(x, 172, 13, fill="#0B0C0E")
        ic.circle(x, 171, 9, fill="#3A3E46")
    ic.circle(128, 140, 9, fill="#0F1012")
    ic.path(_crescent(128, 140, 6.5, 131.5, 137.5, 5.5), fill="#E8E2C8")
