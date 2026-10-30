"""The browsers, soft: the same objects as drawings/apps_browsers.py with
about half the detail, no text and no glare."""

import math

from lib import bar, brand, brand_shape, polar, soft, soft_shadow, tile, two

BRASS = ("#E2B45E", "#B88433")
STEEL = ("#AEB4BB", "#8D949C")


def _d(pts, close=True):
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + ("Z" if close else "")


# --- Firefox: Firefox's own mark (brands/firefox-2019.svg, MPL 2.0), each
# shape in two tones of its colours, the shading over it left out -----------

FOX_TONES = {
    "a": ("#FF6A3D", "#E31587"), "b": ("#FFA02E", "#E8205E"), "d": ("#FFE24A", "#FF980E"),
    "e": ("#9A6BFF", "#5B2DD1"), "g": ("#FFE226", "#FF7139"), "h": ("#FFC23A", "#FF3647"),
    "i": ("#FF980E", "#FF3647"), "j": ("#FFB02E", "#FF3647"), "k": ("#FFE24A", "#FF980E"),
}


@soft("firefox")
def firefox(ic):
    tile(ic, "#3B3F86", "#17183D")
    soft_shadow(ic, 128, 226, 88, 10)
    with ic.g(transform="translate(30 24) scale(0.383)"):
        for tag, geom, fill in brand("firefox-2019")[1]:
            if fill[5:-1] in FOX_TONES:
                light, dark = FOX_TONES[fill[5:-1]]
                brand_shape(ic, tag, geom, fill=ic.lin([(0, light), (1, dark)], 0.87, 0.15, 0.09, 0.93))


# --- Google Chrome and Chromium: each one's own mark (brands/), each shape in
# two tones of its colours, a soft gleam over it --------------------------

CHROME_TONES = {"url(#a)": ("#EF5B4C", "#D33426"), "url(#b)": ("#FFD24A", "#F4A900"),
                "url(#c)": ("#43B866", "#1E8E3E"), "#1a73e8": ("#4A90F0", "#1765CC")}
CHROMIUM_TONES = {"#91b0e8": ("#A9C2F0", "#7E9FDE"), "#396bd7": ("#4E7FE0", "#2B58BE"),
                  "#6199f6": ("#79AAF8", "#4C86EC"), "#4688f4": ("#5E98F6", "#2F6FDE")}


def _toned_mark(ic, name, scale, tones):
    with ic.g(transform=f"translate(30 22) scale({scale:.5f})"):
        for tag, geom, fill in brand(name)[1]:
            if fill in tones:
                light, dark = tones[fill]
                fill = ic.lin([(0, light), (1, dark)], 0.2, 0, 0.8, 1)
            brand_shape(ic, tag, geom, fill=fill)


@soft("google-chrome")
def chrome(ic):
    tile(ic, "#5A6774", "#262E37")
    soft_shadow(ic, 128, 224, 86, 10)
    _toned_mark(ic, "chrome-2022", 196 / 48, CHROME_TONES)


@soft("chromium")
def chromium(ic):
    tile(ic, "#3D5A8A", "#1A2A4A")
    soft_shadow(ic, 128, 224, 86, 10)
    _toned_mark(ic, "chromium", 196 / 512, CHROMIUM_TONES)


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
