"""The browsers, soft: the same objects as drawings/apps_browsers.py with
about half the detail, no text and no glare."""

import math

from lib import bar, polar, soft, soft_shadow, tile, two

BRASS = ("#E2B45E", "#B88433")
STEEL = ("#AEB4BB", "#8D949C")


def _d(pts, close=True):
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + ("Z" if close else "")


def _interp(keys, a):
    for (a0, v0), (a1, v1) in zip(keys, keys[1:]):
        if a1 <= a <= a0:
            t = (a0 - a) / (a0 - a1) if a0 != a1 else 0
            return v0 + (v1 - v0) * t
    return keys[-1][1]


def _pinwheel(ic, cx, cy, R, r1, fills):
    """Chrome's three segments, each bounded by a line tangent to the ring."""
    ex = []
    s = math.sqrt(R * R - r1 * r1)
    for th in (0, 120, 240):
        tx, ty = polar(cx, cy, r1, th)
        dx, dy = math.sin(math.radians(th + 90)), -math.cos(math.radians(th + 90))
        ex.append(((tx, ty), (tx + dx * s, ty + dy * s)))
    for i in range(3):
        (t0, e0), (t1, e1) = ex[i - 1], ex[i]
        ic.path(f"M{t0[0]:.1f} {t0[1]:.1f}L{e0[0]:.1f} {e0[1]:.1f}A{R} {R} 0 0 1 {e1[0]:.1f} {e1[1]:.1f}"
                f"L{t1[0]:.1f} {t1[1]:.1f}L{cx} {cy}Z", fill=fills[i])


# --- Firefox: a desk globe, a fox curled round it ----------------------------

FOX_T = [(40, 26), (10, 19), (-40, 21), (-100, 30), (-160, 34), (-200, 27), (-224, 18), (-238, 4)]


def _fox_band(gx, gy, m, step=4):
    out, inn = [], []
    a = 40.0
    while a >= -238:
        t = _interp(FOX_T, a)
        mm = m + (a < -200) * (a + 200) * 0.25
        out.append(polar(gx, gy, mm + t / 2, a))
        inn.append(polar(gx, gy, mm - t / 2, a))
        a -= step
    return out, inn


@soft("firefox")
def firefox(ic):
    tile(ic, "#3B3F86", "#17183D")
    gx, gy, rg = 122, 110, 60
    soft_shadow(ic, 124, 214, 86, 11)
    ic.rect(78, 194, 92, 16, rx=8, fill=two(ic, "#B97E4A", "#7A4A22"))
    ic.rect(117, 176, 14, 22, rx=3, fill=two(ic, *BRASS))
    ic.circle(gx, gy, 69, fill="none", stroke=two(ic, *BRASS), stroke_width=7)
    ic.circle(gx, gy, rg, fill=two(ic, "#8F78F5", "#3A23A0"))
    clip = ic.clip(f'<circle cx="{gx}" cy="{gy}" r="{rg}"/>')
    with ic.g(clip_path=clip, fill="#C7BBFF", opacity=0.3):
        ic.path("M80 76c12-10 30-6 34 4s-4 14-2 22-10 16-18 10-8-14-14-16-10-14 0-20z")
        ic.path("M138 112c12 0 20 10 18 20s-12 22-20 20-6-16-4-24-6-16 6-16z")
    out, inn = _fox_band(gx, gy, 68)
    head = [(170, 80), (188, 88), (213, 78), (205, 64), (199, 55), (204, 30), (190, 44), (180, 18), (172, 44)]
    fur = ic.lin([(0, "#FFB63A"), (1, "#E8344E")], 204, 30, 40, 196, units="userSpaceOnUse")
    ic.path(_d([inn[0]] + head + out + inn[::-1]), fill=fur, stroke=fur, stroke_width=3, stroke_linejoin="round")
    ic.path("M186 70c8 0 16 4 26 8-8 6-18 8-28 6-6-1-9-6-6-10z", fill="#FFF3D6")
    ic.circle(195, 62, 3.6, fill="#2A0E06")


# --- Google Chrome: a camera lens, its glass in the three enamels -------------

def _lens(ic, cx, cy, colours, centre):
    soft_shadow(ic, cx, 214, 92, 11)
    ic.circle(cx, cy + 12, 92, fill="#1E2023")
    ic.circle(cx, cy, 92, fill=two(ic, *STEEL))
    ic.circle(cx, cy, 84, fill=two(ic, "#2E3136", "#0E0F11"))
    ic.circle(cx, cy, 70, fill="#0B0C0E")
    _pinwheel(ic, cx, cy, 68, 29, colours)
    ic.circle(cx, cy, 31, fill="#FFFFFF")
    ic.circle(cx, cy, 23, fill=centre)


CHROME = [("#EA4335", "#C5281C"), ("#FBC02D", "#E39A10"), ("#34A853", "#1E7E3A")]


@soft("google-chrome")
def chrome(ic):
    tile(ic, "#5A6774", "#262E37")
    _lens(ic, 128, 112, [two(ic, a, b) for a, b in CHROME], two(ic, "#5A97FA", "#1F5FD0"))


# --- Chromium: a glass paperweight, the mark in three blues inside -------------

CHROMIUM = [("#5E97F6", "#3F7BE0"), ("#A9C8FF", "#7FA8F0"), ("#2A5DC0", "#1A438E")]


@soft("chromium")
def chromium(ic):
    tile(ic, "#2B4766", "#101E30")
    cx = 128
    soft_shadow(ic, cx, 206, 100, 14)
    dome = f"M{cx - 92} 186C{cx - 92} 92 {cx - 50} 34 {cx} 34S{cx + 92} 92 {cx + 92} 186" \
           f"A92 18 0 0 1 {cx - 92} 186Z"
    ic.path(dome, fill="#8FB6F0", opacity=0.28)
    ic.ellipse(cx, 184, 80, 13, fill="#C8DEFF", opacity=0.35)
    _pinwheel(ic, cx, 118, 60, 26, [two(ic, a, b) for a, b in CHROMIUM])
    ic.circle(cx, 118, 28, fill="#FFFFFF")
    ic.circle(cx, 118, 20, fill=two(ic, "#5E97F6", "#2456B8"))
    ic.path(dome, fill="none", stroke="#E4F0FF", stroke_opacity=0.6, stroke_width=4)
    ic.path(f"M{cx - 76} 140C{cx - 76} 96 {cx - 50} 56 {cx - 14} 46", fill="none", stroke="#fff",
            stroke_opacity=0.45, stroke_width=8, stroke_linecap="round")


# --- Brave: a copper shield, a lion's face in relief --------------------------

def _brave_shape(cx, top, k=1.0):
    half = [(0, 0), (30, 0), (42, 10), (56, 22), (52, 38), (60, 60), (50, 100), (32, 140), (12, 160), (0, 168)]
    right = [(cx + x * k, top + y * k) for x, y in half]
    left = [(cx - x * k, top + y * k) for x, y in half[::-1]]
    return right + left[1:-1]


@soft("brave-browser")
def brave(ic):
    tile(ic, "#3E3050", "#1A1224")
    soft_shadow(ic, 128, 214, 76, 10)
    ic.path(_d(_brave_shape(131, 37)), fill="#7A2A12", stroke="#7A2A12", stroke_width=10, stroke_linejoin="round")
    face = two(ic, "#FF8250", "#D23A1C")
    ic.path(_d(_brave_shape(128, 32)), fill=face, stroke=face, stroke_width=10, stroke_linejoin="round")
    mask = [(104, 62), (152, 62), (170, 90), (160, 122), (146, 146), (128, 160), (110, 146), (96, 122), (86, 90)]
    ic.path(_d(mask), fill=two(ic, "#FFF6EE", "#F2C2A4"), stroke="#FBE2D0", stroke_width=6, stroke_linejoin="round")
    cut = "#C4401E"
    ic.path("M98 82 L122 90 L118 102 L96 93 Z", fill=cut, stroke=cut, stroke_width=2, stroke_linejoin="round")
    ic.path("M158 82 L134 90 L138 102 L160 93 Z", fill=cut, stroke=cut, stroke_width=2, stroke_linejoin="round")
    ic.path("M112 118 H144 L128 136 Z", fill=cut, stroke=cut, stroke_width=4, stroke_linejoin="round")
    ic.path("M128 136 V145 M117 147 Q128 154 139 147", fill="none", stroke=cut, stroke_width=5,
            stroke_linecap="round")


# --- Microsoft Edge: a glass wave on a slate ------------------------------------

@soft("microsoft-edge")
def edge(ic):
    tile(ic, "#173A62", "#0A1730")
    cx, cy, R = 128, 112, 80
    soft_shadow(ic, 128, 214, 90, 11)
    ic.rect(54, 192, 148, 18, rx=7, fill="#1E2227")
    ic.rect(54, 184, 148, 14, rx=7, fill=two(ic, "#5F6771", "#3A4048"))
    hx, hy, hr = 160, 146, 44
    body = (f"M{cx - R} {cy}A{R} {R} 0 1 1 {cx + R} {cy}A{R} {R} 0 1 1 {cx - R} {cy}Z"
            f"M{hx - hr} {hy}A{hr} {hr} 0 1 0 {hx + hr} {hy}A{hr} {hr} 0 1 0 {hx - hr} {hy}Z")
    ic.path(body, fill_rule="evenodd", fill=ic.lin([(0, "#2C93EC"), (1, "#3ECB86")], 1, 0, 0.1, 1))
    clip = ic.clip(f'<circle cx="{cx}" cy="{cy}" r="{R}"/>')
    with ic.g(clip_path=clip):
        ic.circle(hx, hy, hr + 9, fill="none", stroke="#9FF0D8", stroke_width=18, stroke_opacity=0.8)


# --- Vivaldi: a manuscript of the Spring, sealed in red with a V --------------

def _seal_blob(cx, cy, r, n=12, jitter=(1.0, 0.93, 1.04, 0.95, 1.02, 0.92)):
    pts = [polar(cx, cy, r * jitter[i % len(jitter)], i * 360 / n) for i in range(n)]
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(n):
        p1 = pts[(i + 1) % n]
        q = polar(cx, cy, r * 1.06, (i + 0.5) * 360 / n)
        d += f"Q{q[0]:.1f} {q[1]:.1f} {p1[0]:.1f} {p1[1]:.1f}"
    return d + "Z"


@soft("vivaldi")
def vivaldi(ic):
    tile(ic, "#4A3F52", "#1E1824")
    soft_shadow(ic, 124, 214, 98, 11)
    ink = "#4A3E36"
    with ic.g(transform="rotate(-5 120 120)"):
        ic.rect(34, 34, 168, 178, rx=8, fill=two(ic, "#FBF6EA", "#ECE3CF"))
        bar(ic, 48, 46, 80, 10, fill="#3A2E28")
        for s, top in enumerate((74, 110, 146)):
            for k in range(5):
                ic.line(48, top + k * 5, 190, top + k * 5, stroke=ink, stroke_opacity=0.4, stroke_width=1.6)
            for i in range(6 if s < 2 else 3):
                nx = 62 + i * 21
                ny = top + 16 - ((s * 2 + i * 3) % 5) * 3
                ic.ellipse(nx, ny, 4.6, 3.4, fill=ink, transform=f"rotate(-20 {nx} {ny})")
                ic.rect(nx + 2.6, ny - 18, 2.4, 18, rx=1.2, fill=ink)
    sx, sy = 150, 158
    ic.path(_seal_blob(sx, sy, 48), fill=two(ic, "#F2453C", "#A8191B"))
    ic.circle(sx, sy, 35, fill="#D92A2A")
    ic.path(f"M{sx - 18} {sy - 14}L{sx - 4} {sy + 14}L{sx + 16} {sy - 20}", fill="none", stroke="#FFF4F0",
            stroke_width=11, stroke_linecap="round", stroke_linejoin="round")
    ic.circle(sx - 20, sy - 18, 6, fill="#FFF4F0")


# --- Opera: a red enamel ring, standing --------------------------------------

@soft("opera")
def opera(ic):
    tile(ic, "#2E3040", "#101118")
    cx, cy = 128, 116
    soft_shadow(ic, cx, 208, 82, 11)

    def ell(rx, ry, dx=0):
        x = cx + dx
        return f"M{x - rx} {cy}A{rx} {ry} 0 1 1 {x + rx} {cy}A{rx} {ry} 0 1 1 {x - rx} {cy}Z"

    ic.path(ell(40, 66) + ell(26, 56, 5), fill_rule="evenodd",
            fill=ic.lin([(0, "#6A0814"), (1, "#C8182A")], 0, 0, 1, 0))
    ic.path(ell(74, 90) + ell(40, 66), fill_rule="evenodd", fill=two(ic, "#FF3A48", "#B00A1C"))
    ic.path(f"M{cx - 58} {cy - 4}C{cx - 58} {cy - 48} {cx - 34} {cy - 78} {cx - 6} {cy - 82}", fill="none",
            stroke="#fff", stroke_opacity=0.35, stroke_width=9, stroke_linecap="round")


# --- Tor Browser: a purple onion on a board, one half cut ---------------------

@soft("torbrowser")
def tor(ic):
    tile(ic, "#3E2C5A", "#1A1230")
    soft_shadow(ic, 128, 216, 100, 11)
    ic.rect(26, 178, 204, 30, rx=12, fill="#6A4220")
    ic.rect(26, 164, 204, 30, rx=12, fill=two(ic, "#E2B47E", "#B88250"))
    ox = 98
    bulb = (f"M{ox} 30C{ox + 4} 58 {ox + 62} 66 {ox + 60} 116C{ox + 58} 156 {ox + 28} 176 {ox} 176"
            f"C{ox - 28} 176 {ox - 58} 156 {ox - 60} 116C{ox - 62} 66 {ox - 4} 58 {ox} 30Z")
    ic.path(bulb, fill=two(ic, "#A56CC6", "#5A2C76"))
    with ic.g(fill="none", stroke_linecap="round", stroke_width=3):
        for dx, c, o in ((-30, "#E4C6F2", 0.4), (24, "#2E1240", 0.3)):
            ic.path(f"M{ox + dx * 0.15} 52Q{ox + dx * 1.45} 110 {ox + dx * 0.55} 172", stroke=c, stroke_opacity=o)
    ic.path(f"M{ox - 4} 32C{ox - 7} 22 {ox - 4} 13 {ox + 3} 8C{ox + 2} 18 {ox + 7} 24 {ox + 5} 34Z",
            fill="#C8A878")
    hx, hy = 164, 140
    for r, c in ((46, "#6A3486"), (40, "#F6EEF9"), (31, "#8C55AA"), (25, "#F1E6F6"), (15, "#8C55AA")):
        k = (46 - r) * 0.3
        ic.circle(hx + k, hy - k * 0.6, r, fill=c)
