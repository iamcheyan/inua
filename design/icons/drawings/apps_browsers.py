"""The theme's browsers: Firefox, Chrome, Chromium, Brave, Edge, Vivaldi,
Opera, Tor Browser (docs/feat/object-icons.md, Part 2). Each mark is
redrawn, simplified, as an object of its own: no two browsers share one.
Firefox's, Chrome's and Chromium's are their own marks (brands/, each with
its licence), lit as objects."""

import math

from lib import (brand, brand_gradients, brand_shape, brass, glare, icon, paper, polar, shadow, small, steel, text_path, tile, wood)


def _d(pts, close=True):
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + ("Z" if close else "")


def _arc_text(ic, s, cx, cy, r, deg, size, font="mono-semibold", spacing=0.6, below=False, **kw):
    """A line set along a circle, centred at angle deg, each letter upright
    to the radius; below sets it on the bottom of the circle, readable."""
    ws = [text_path(c, 0, 0, size, font)[1] for c in s]
    total = sum(ws) + spacing * (len(s) - 1)
    a = deg - math.degrees(total / 2 / r) * (-1 if below else 1)
    for c, w in zip(s, ws):
        step = math.degrees((w + spacing) / r)
        mid = a + (-1 if below else 1) * math.degrees(w / 2 / r)
        if c != " ":
            if below:
                with ic.g(transform=f"rotate({mid - 180:.2f} {cx} {cy})"):
                    ic.text(c, cx, cy + r + size * 0.36, size, font=font, anchor="middle", **kw)
            else:
                with ic.g(transform=f"rotate({mid:.2f} {cx} {cy})"):
                    ic.text(c, cx, cy - r + size * 0.36, size, font=font, anchor="middle", **kw)
        a += (-1 if below else 1) * step


# --- Firefox: Firefox's own mark (brands/firefox-2019.svg, MPL 2.0, its
# notice there), on inua's tile, a shadow under it and the glass of a globe
# over its globe: faint lines and the light from the top left -------------

# Where the mark sits on the tile, 196 of its 256.
MARK = "translate(30 24) scale(0.383)"


@icon("firefox", kind="app", title="Firefox",
      names=["firefox", "firefox-beta", "firefox-bin", "firefox-esr", "firefox-icon", "firefox-mozilla-build",
             "org.mozilla.Firefox", "org.mozilla.firefox"])
def firefox(ic):
    tile(ic, "#3B3F86", "#17183D")
    shadow(ic, 128, 226, 88, 10)
    grads, shapes = brand("firefox-2019")
    ids = brand_gradients(ic, grads)
    paths = _fox_paths(shapes)
    d_of = {g: d for d, g in paths}
    with ic.g(transform=MARK):
        for d, g in paths:
            if g == "g":
                _firefox_glass(ic, d_of)  # over its globe (e, f), under the fox
            ic.path(d, fill=f"url(#{ids[g]})")
        _firefox_fur(ic, d_of)


def _fox_paths(shapes):
    """Firefox's paths: each one's d and the id of its gradient."""
    return [(geom["d"], fill[5:-1]) for _, geom, fill in shapes]


def _firefox_glass(ic, d_of):
    """The globe as glass, on the 512 grid: its lit rim and darker limb,
    faint lands and lines, the fox's shadow on it, a gleam."""
    clip = ic.clip(f'<path d="{d_of["e"]}"/>')
    with ic.g(clip_path=clip):
        ic.circle(254, 250, 116, fill=ic.rad([(0.55, "#000", 0), (1, "#14063F", 0.55)], cx=0.42, cy=0.38, r=0.62))
        with ic.g(fill="#D9C8FF", opacity=0.2):
            ic.path("M182 212c22-16 52-12 60 6s-8 26-4 42-16 30-34 22-14-26-26-30-18-26 4-40z")
            ic.path("M274 262c22 0 38 18 34 38s-22 42-38 38-12-30-8-46-12-30 12-30z")
            ic.path("M292 176c14-6 34 0 38 12s-6 16-18 16-24-18-20-28z")
        with ic.g(fill="none", stroke="#EDE4FF", stroke_opacity=0.2, stroke_width=2.5):
            for ry in (38, 76, 112):
                ic.ellipse(254, 250, 116, ry)
            for rx in (46, 92):
                ic.ellipse(254, 250, rx, 116)
            ic.line(254, 134, 254, 366)
        # the fox's shadow on the glass, down and to the right of it
        with ic.g(transform="translate(10 12)", fill="#12053A", opacity=0.4):
            for g in ("h", "j", "k"):
                ic.path(d_of[g])
        ic.path(d_of["e"], fill=glare(ic, 1.5))
        ic.path("M152 224a104 104 0 0 1 70-78", fill="none", stroke="#F3ECFF", stroke_opacity=0.55, stroke_width=7,
                stroke_linecap="round")
        ic.ellipse(196, 186, 22, 11, fill="#fff", opacity=0.35, transform="rotate(-40 196 186)")


def _firefox_fur(ic, d_of):
    """Over the fox, on the 512 grid: a rim of light along its top edges, a
    gleam up the tail's flame, and fine strokes of fur round its body."""
    clip = ic.clip(f'<path d="{d_of["a"]}"/>')
    with ic.g(clip_path=clip):
        rim = ic.lin([(0, "#FFFBE0", 0.7), (0.45, "#FFFBE0", 0), (1, "#FFFBE0", 0)], 0.15, 0.1, 0.75, 0.9)
        ic.path(d_of["a"], fill="none", stroke=rim, stroke_width=10)
    ic.path(d_of["i"], fill=ic.lin([(0, "#FFFDE8", 0.65), (1, "#FFFDE8", 0)], 0.6, 0, 0.4, 1))
    body = ic.clip(f'<path d="{d_of["h"]}"/>')
    with ic.g(clip_path=body, fill="none", stroke="#B0104F", stroke_opacity=0.18, stroke_width=2.5,
              stroke_linecap="round"):
        for a in range(-110, 115, 16):
            x1, y1 = polar(256, 262, 200, a + 180)
            x2, y2 = polar(256, 262, 184, a + 184)
            ic.line(x1, y1, x2, y2)


@small("firefox")
def firefox16(ic):
    tile(ic, "#3B3F86", "#17183D")
    with ic.g(transform="translate(1.6 1.4) scale(0.025)"):
        for d, g in _fox_paths(brand("firefox-2019")[1]):
            if g in MARK_FILLS:
                ic.path(d, fill=MARK_FILLS[g][0])


# The mark's colours without its gradients, for the soft drawing and the
# 16 px one: each path's two tones, light then dark; the shading over it
# (c, f, l) left out.
MARK_FILLS = {
    "a": ("#FF6A3D", "#E31587"), "b": ("#FFA02E", "#E8205E"), "d": ("#FFE24A", "#FF980E"),
    "e": ("#9A6BFF", "#5B2DD1"), "g": ("#FFE226", "#FF7139"), "h": ("#FFC23A", "#FF3647"),
    "i": ("#FF980E", "#FF3647"), "j": ("#FFB02E", "#FF3647"), "k": ("#FFE24A", "#FF980E"),
}


# --- Google Chrome and Chromium: each one's own mark (brands/chrome-2022.svg,
# public domain; brands/chromium.svg, BSD, its notice there) as a domed
# button on inua's tile: lit from the top left, its ring raised, its centre
# a glass jewel -------------------------------------------------------------

def _domed_mark(ic, name, scale, centre, ring, jewel, ring_tones, fill_of=None):
    """A round mark on a 196 px disc: its shapes (their own gradients, or
    fill_of's colours), then on its grid the dome's light and shade, the
    ring raised with its shadow and the centre a jewel. centre is the
    mark's centre, ring and jewel the ring's outer and inner radius."""
    grads, shapes = brand(name)
    ids = brand_gradients(ic, grads)
    cx, cy = centre
    with ic.g(transform=f"translate(30 22) scale({scale:.5f})"):
        u = 1 / scale  # a tile pixel, on the mark's grid
        R = 98 * u
        for tag, geom, fill in shapes:
            if fill.startswith("url("):
                fill = f"url(#{ids[fill[5:-1]]})"
            brand_shape(ic, tag, geom, fill=(fill_of or {}).get(fill, fill))
        # the dome: light from the top left, shade down the far edge
        ic.circle(cx, cy, R, fill=ic.rad([(0, "#fff", 0.28), (0.5, "#fff", 0.04), (1, "#fff", 0)],
                                         cx=0.3, cy=0.25, r=0.7))
        ic.circle(cx, cy, R, fill=ic.rad([(0.75, "#000", 0), (1, "#0A0F1E", 0.2)], cx=0.42, cy=0.38, r=0.62))
        ic.circle(cx, cy, R - 0.8 * u, fill="none", stroke="#fff", stroke_opacity=0.25, stroke_width=1.6 * u)
        # the ring, raised: its shadow on the colours, then white metal
        def round_(x, y, r):
            return f"M{x - r:.2f} {y:.2f}a{r:.2f} {r:.2f} 0 1 0 {2 * r:.2f} 0a{r:.2f} {r:.2f} 0 1 0 {-2 * r:.2f} 0z"
        ic.path(round_(cx + 1.5 * u, cy + 2.5 * u, ring + 0.6 * u) + round_(cx, cy, ring), fill="#0A0F1E",
                opacity=0.25, fill_rule="evenodd")
        light, dark = ring_tones
        ic.path(round_(cx, cy, ring) + round_(cx, cy, jewel), fill=ic.lin([(0, light), (1, dark)], 0.2, 0, 0.8, 1),
                fill_rule="evenodd")
        ic.circle(cx, cy, ring - 0.6 * u, fill="none", stroke="#fff", stroke_opacity=0.8, stroke_width=1.2 * u,
                  stroke_dasharray=f"{ring * 1.6:.2f} {ring * 9:.2f}", transform=f"rotate(-150 {cx} {cy})")
        # the centre, a glass jewel: deeper at its rim, a gleam at the top
        ic.circle(cx, cy, jewel, fill=ic.rad([(0.65, "#000", 0), (1, "#06102E", 0.22)], cx=0.45, cy=0.4, r=0.6))
        ic.circle(cx, cy, jewel, fill=ic.rad([(0, "#fff", 0.35), (0.6, "#fff", 0)], cx=0.35, cy=0.28, r=0.55))
        ic.ellipse(cx - jewel * 0.32, cy - jewel * 0.42, jewel * 0.34, jewel * 0.16, fill="#fff", opacity=0.55,
                   transform=f"rotate(-30 {cx - jewel * 0.32:.2f} {cy - jewel * 0.42:.2f})")


@icon("google-chrome", kind="app", title="Google Chrome",
      names=["com.google.Chrome", "google-chrome", "google-chrome2", "googlechrome"])
def chrome(ic):
    tile(ic, "#5A6774", "#262E37")
    shadow(ic, 128, 224, 86, 10)
    _domed_mark(ic, "chrome-2022", 196 / 48, (24, 24), 12, 9.5, ("#FFFFFF", "#C9D0D8"))


@small("google-chrome")
def chrome16(ic):
    tile(ic, "#5A6774", "#262E37")
    with ic.g(transform="translate(1.5 1.5) scale(0.2708)"):
        for tag, geom, fill in brand("chrome-2022")[1]:
            brand_shape(ic, tag, geom, fill=CHROME_FILLS.get(fill, fill))


# Chrome's colours without its gradients, for the soft and 16 px drawings:
# each shape's light and dark tones, by its fill in the mark.
CHROME_FILLS = {"url(#a)": "#EA4335", "url(#b)": "#FBBC04", "url(#c)": "#34A853"}
CHROME_TONES = {"url(#a)": ("#EF5B4C", "#D33426"), "url(#b)": ("#FFD24A", "#F4A900"),
                "url(#c)": ("#43B866", "#1E8E3E"), "#1a73e8": ("#4A90F0", "#1765CC")}


@icon("chromium", kind="app", title="Chromium",
      names=["chromium", "chromium-browser", "chromium-browser-privacy", "chromium-freeworld",
             "com.github.Eloston.UngoogledChromium", "org.chromium.Chromium"])
def chromium(ic):
    tile(ic, "#3D5A8A", "#1A2A4A")
    shadow(ic, 128, 224, 86, 10)
    _domed_mark(ic, "chromium", 196 / 512, (256, 256), 120.2, 99.2, ("#FFFFFF", "#C9D6EA"))


@small("chromium")
def chromium16(ic):
    tile(ic, "#3D5A8A", "#1A2A4A")
    with ic.g(transform="translate(1.5 1.5) scale(0.0254)"):
        for tag, geom, fill in brand("chromium")[1]:
            brand_shape(ic, tag, geom, fill=fill)


CHROMIUM_TONES = {"#91b0e8": ("#A9C2F0", "#7E9FDE"), "#396bd7": ("#4E7FE0", "#2B58BE"),
                  "#6199f6": ("#79AAF8", "#4C86EC"), "#4688f4": ("#5E98F6", "#2F6FDE")}


# --- Brave: a copper shield, a lion's face in relief --------------------------

def _brave_shape(cx, top, k=1.0):
    half = [(0, 0), (30, 0), (42, 10), (56, 22), (52, 38), (60, 60), (50, 100), (32, 140), (12, 160), (0, 168)]
    right = [(cx + x * k, top + y * k) for x, y in half]
    left = [(cx - x * k, top + y * k) for x, y in half[::-1]]
    return right + left[1:-1]


@icon("brave-browser", kind="app", title="Brave", names=["brave", "com.brave.Browser"])
def brave(ic):
    tile(ic, "#3E3050", "#1A1224")
    shadow(ic, 128, 214, 76, 10)
    shape = _brave_shape(128, 32)
    # the plaque's thickness, then its face
    ic.path(_d(_brave_shape(132, 38)), fill="#5E1F0C", stroke="#5E1F0C", stroke_width=6, stroke_linejoin="round")
    ic.path(_d(_brave_shape(130, 35)), fill="#8A3416", stroke="#8A3416", stroke_width=6, stroke_linejoin="round")
    face = ic.lin([(0, "#FF9257"), (0.45, "#F55A2A"), (1, "#C4321A")], 0, 0, 1, 1)
    ic.path(_d(shape), fill=face, stroke=face, stroke_width=6, stroke_linejoin="round")
    ic.path(_d(_brave_shape(128, 40, 0.9)), fill="none", stroke="#FFC4A0", stroke_opacity=0.5, stroke_width=1.5,
            stroke_linejoin="round")
    ic.path(_d(shape[:6], close=False), fill="none", stroke="#FFD9BE", stroke_opacity=0.75, stroke_width=2,
            stroke_linejoin="round", transform="translate(0 -2.5)")
    ic.path(_d(shape[-5:] + [shape[0]], close=False), fill="none", stroke="#FFD9BE", stroke_opacity=0.75,
            stroke_width=2, stroke_linejoin="round", transform="translate(0 -2.5)")
    # the lion's face, raised, pale copper
    mask = [(104, 62), (152, 62), (170, 90), (160, 122), (146, 146), (128, 160), (110, 146), (96, 122), (86, 90)]
    ic.path(_d(mask), fill="#7A2410", opacity=0.55, transform="translate(2.5 3.5)", stroke="#7A2410",
            stroke_width=4, stroke_linejoin="round")
    pale = ic.lin([(0, "#FFF6EE"), (0.6, "#FBD9C2"), (1, "#EDA987")], 0, 0, 1, 1)
    ic.path(_d(mask), fill=pale, stroke=pale, stroke_width=4, stroke_linejoin="round")
    ic.path(_d(mask[:3], close=False), fill="none", stroke="#fff", stroke_width=1.5, stroke_linejoin="round",
            transform="translate(0 -2)")
    # brow, eyes, nose and mouth, cut in
    cut = "#C4401E"
    ic.path("M100 82 L122 90 L118 100 L98 92 Z", fill=cut)
    ic.path("M156 82 L134 90 L138 100 L158 92 Z", fill=cut)
    ic.path("M114 118 H142 L128 134 Z", fill=cut, stroke=cut, stroke_width=3, stroke_linejoin="round")
    ic.path("M128 134 V144 M118 146 Q128 152 138 146", fill="none", stroke=cut, stroke_width=3,
            stroke_linecap="round")
    ic.path("M100 92 L118 100", stroke="#fff", stroke_opacity=0.6, stroke_width=1)
    ic.path("M138 100 L158 92", stroke="#fff", stroke_opacity=0.6, stroke_width=1)
    # the screws that hold it
    for x, y in ((104, 46), (152, 46)):
        ic.circle(x, y, 4, fill=steel(ic, False))
        ic.line(x - 2.6, y + 1.2, x + 2.6, y - 1.2, stroke="#3A3E44", stroke_width=1.2)
    # the name, struck below
    ic.text("BRAVE", 128, 186, 9, font="mono-semibold", anchor="middle", spacing=2, fill="#7A2410")
    ic.text("BRAVE", 128, 185.2, 9, font="mono-semibold", anchor="middle", spacing=2, fill="#FFC6A2", opacity=0.6)


@small("brave-browser")
def brave16(ic):
    tile(ic, "#3E3050", "#1A1224")
    ic.path(_d(_brave_shape(8, 2, 0.072)), fill="#F55A2A", stroke="#F55A2A", stroke_width=0.6,
            stroke_linejoin="round")
    ic.path("M6.4 4.4h3.2l1.2 2-.8 2.4L8 10.6 6 8.8l-.8-2.4z", fill="#FFF1E6")
    ic.path("M7.2 8.2h1.6L8 9z", fill="#C4401E")


# --- Microsoft Edge: a glass wave on a slate ------------------------------------

@icon("microsoft-edge", kind="app", title="Microsoft Edge", names=["com.microsoft.Edge", "microsoft-edge"])
def edge(ic):
    tile(ic, "#173A62", "#0A1730")
    cx, cy, R = 128, 112, 80
    shadow(ic, 128, 214, 90, 11)
    # the slate it stands on
    ic.rect(56, 192, 144, 16, rx=5, fill=ic.lin([(0, "#2C3138"), (1, "#14171B")]))
    ic.rect(56, 186, 144, 12, rx=5, fill=ic.lin([(0, "#59616B"), (1, "#3A4048")]))
    ic.line(62, 186.8, 194, 186.8, stroke="#fff", stroke_opacity=0.25)
    ic.text("Edge", 128, 205, 8, font="sans-semibold", anchor="middle", spacing=1, fill="#9AA4B0")
    # coloured light through the glass, on the slate
    ic.ellipse(112, 190, 50, 4, fill=ic.rad([(0, "#5FE0B0", 0.6), (1, "#5FE0B0", 0)]))
    # the wave: a disc with the curl bitten out at the lower right
    hx, hy, hr = 160, 146, 44
    body = (f"M{cx - R} {cy}A{R} {R} 0 1 1 {cx + R} {cy}A{R} {R} 0 1 1 {cx - R} {cy}Z"
            f"M{hx - hr} {hy}A{hr} {hr} 0 1 0 {hx + hr} {hy}A{hr} {hr} 0 1 0 {hx - hr} {hy}Z")
    ic.path(body, fill_rule="evenodd", fill="#06142A", opacity=0.45, transform="translate(3 4)")
    sea = ic.lin([(0, "#3FA9F5"), (0.38, "#1C7FD6"), (0.62, "#14A7A0"), (0.85, "#47CF7A"), (1, "#7BE07A")], 1, 0, 0.1, 1)
    ic.path(body, fill_rule="evenodd", fill=sea, opacity=0.94)
    # the inside of the curl, lighter, and the crest
    clip = ic.clip(f'<circle cx="{cx}" cy="{cy}" r="{R}"/>')
    with ic.g(clip_path=clip):
        ic.circle(hx, hy, hr + 9, fill="none", stroke=ic.lin([(0, "#9FF0D8"), (1, "#36C3E8")], 0, 0, 1, 1),
                  stroke_width=18, stroke_opacity=0.85)
        ic.circle(hx, hy, hr + 1, fill="none", stroke="#E8FFF6", stroke_width=2, stroke_opacity=0.7)
    ic.path(f"M{cx - 64} {cy - 46}A{R - 4} {R - 4} 0 0 1 {cx + 70} {cy - 30}", fill="none", stroke="#BFE6FF",
            stroke_width=10, stroke_opacity=0.25, stroke_linecap="round")
    # glass: glare from the top left, a hard edge light, the far side darker
    ic.path(body, fill_rule="evenodd", fill=glare(ic, 1.8))
    ic.path(f"M{cx - 76} {cy - 6}A{R - 2} {R - 2} 0 0 1 {cx - 10} {cy - R + 1}", fill="none", stroke="#fff",
            stroke_width=2.5, stroke_opacity=0.8, stroke_linecap="round")
    ic.path(f"M{cx + 79} {cy + 4}A{R} {R} 0 0 1 {cx + 76} {cy + 26}", fill="none", stroke="#0A2A50",
            stroke_width=3, stroke_opacity=0.5)
    ic.ellipse(cx - 40, cy - 46, 12, 6, fill="#fff", opacity=0.55, transform=f"rotate(-40 {cx - 40} {cy - 46})")


@small("microsoft-edge")
def edge16(ic):
    tile(ic, "#173A62", "#0A1730")
    ic.path("M2 7.6A6 6 0 1 1 14 7.6A6 6 0 1 1 2 7.6ZM7.2 10.4A3.4 3.4 0 1 0 14 10.4A3.4 3.4 0 1 0 7.2 10.4Z",
            fill_rule="evenodd", fill="#1C7FD6")
    ic.path("M2 7.6A6 6 0 0 0 8.4 13.6 4 4 0 0 1 6.4 10 4 4 0 0 1 10 6.6 6 6 0 0 0 2 7.6Z", fill="#3BC08A")
    ic.rect(3, 13.4, 10, 1.2, rx=0.6, fill="#59616B")


# --- Vivaldi: a manuscript of the Spring, sealed in red with a V --------------

def _seal_blob(cx, cy, r, n=14, jitter=(1.0, 0.92, 1.04, 0.95, 1.02, 0.9, 1.05)):
    pts = [polar(cx, cy, r * jitter[i % len(jitter)], i * 360 / n) for i in range(n)]
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(n):
        p0, p1 = pts[i], pts[(i + 1) % n]
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        q = polar(cx, cy, r * 1.06, (i + 0.5) * 360 / n)
        d += f"Q{q[0]:.1f} {q[1]:.1f} {p1[0]:.1f} {p1[1]:.1f}"
        del mx, my
    return d + "Z"


@icon("vivaldi", kind="app", title="Vivaldi", names=["com.vivaldi.Vivaldi", "vivaldi", "vivaldi-stable"])
def vivaldi(ic):
    tile(ic, "#4A3F52", "#1E1824")
    shadow(ic, 124, 214, 98, 11)
    # the manuscript: a sheet of music, a little turned
    with ic.g(transform="rotate(-5 120 120)"):
        ic.rect(34, 34, 168, 178, rx=3, fill="#000", opacity=0.25, transform="translate(3 4)")
        ic.rect(34, 34, 168, 178, rx=3, fill=paper(ic, "cream"))
        ic.text("La Primavera", 48, 58, 17, font="hand", fill="#3A2E28")
        ic.text("A. Vivaldi · RV 269", 190, 57, 6, font="mono", anchor="end", fill="#8C7F72")
        ink = "#4A3E36"
        notes = [(0, 3), (1, 2), (2, 2), (3, 1), (4, 3), (5, 0), (6, 2), (7, 4), (8, 3), (9, 1)]
        for s, top in enumerate((72, 104, 136)):
            for k in range(5):
                ic.line(46, top + k * 4.5, 192, top + k * 4.5, stroke=ink, stroke_opacity=0.45, stroke_width=0.8)
            ic.line(46, top, 46, top + 18, stroke=ink, stroke_width=1)
            ic.line(192, top, 192, top + 18, stroke=ink, stroke_width=1)
            for i, (x, n) in enumerate(notes):
                if s == 2 and x > 4:
                    break
                nx = 64 + x * 12.6
                ny = top + 18 - (n + (s * 3 + i) % 4) * 2.25
                ic.ellipse(nx, ny, 3, 2.1, fill=ink, transform=f"rotate(-20 {nx} {ny})")
                ic.line(nx + 2.7, ny - 0.5, nx + 2.7, ny - 13, stroke=ink, stroke_width=0.9)
            ic.path(f"M50 {top + 13}c4-12 7 0 2 6s-6-12 0-16", fill="none", stroke=ink, stroke_width=1.1)
    # the seal, Vivaldi red, a V in relief
    sx, sy = 150, 158
    ic.path(_seal_blob(sx + 3, sy + 4, 48), fill="#3A0A0A", opacity=0.4)
    ic.path(_seal_blob(sx, sy, 48), fill=ic.rad([(0, "#FF6A5E"), (0.55, "#E8312F"), (1, "#8F1517")],
                                                 cx=0.38, cy=0.32, r=0.75))
    ic.circle(sx, sy, 36, fill="#D92A2A")
    ic.circle(sx, sy, 36, fill="none", stroke="#6E0E10", stroke_opacity=0.55, stroke_width=2.5)
    ic.circle(sx - 0.8, sy - 0.8, 36, fill="none", stroke="#FFA49A", stroke_opacity=0.35, stroke_width=1)
    v = f"M{sx - 18} {sy - 14}L{sx - 4} {sy + 14} M{sx - 4} {sy + 14}L{sx + 16} {sy - 20}"
    ic.path(v, fill="none", stroke="#6E0E10", stroke_width=9, stroke_linecap="round", stroke_linejoin="round",
            opacity=0.6, transform="translate(1.5 2)")
    ic.path(v, fill="none", stroke=ic.lin([(0, "#FFF6F2"), (1, "#F6C9C2")]), stroke_width=9,
            stroke_linecap="round", stroke_linejoin="round")
    ic.circle(sx - 20, sy - 18, 5, fill="#FFF6F2")
    ic.ellipse(sx - 22, sy - 32, 9, 4, fill="#fff", opacity=0.3, transform=f"rotate(-25 {sx - 22} {sy - 32})")


@small("vivaldi")
def vivaldi16(ic):
    tile(ic, "#4A3F52", "#1E1824")
    ic.rect(2, 2.2, 10, 11.6, rx=0.6, fill="#F7F1E4", transform="rotate(-5 7 8)")
    for y in (4.6, 6.2):
        ic.line(3.4, y, 10.6, y - 0.5, stroke="#8C7F72", stroke_width=0.5)
    ic.circle(9.8, 10.2, 4.6, fill="#E8312F")
    ic.path("M7.8 8.6L9.4 11.6 11.6 7.8", fill="none", stroke="#fff", stroke_width=1.3, stroke_linecap="round",
            stroke_linejoin="round")


# --- Opera: a red enamel ring, standing --------------------------------------

@icon("opera", kind="app", title="Opera", names=["com.opera.Opera", "opera"])
def opera(ic):
    tile(ic, "#2E3040", "#101118")
    cx, cy = 128, 116
    shadow(ic, cx, 208, 82, 11)

    def ell(rx, ry, dx=0):
        x = cx + dx
        return f"M{x - rx} {cy}A{rx} {ry} 0 1 1 {x + rx} {cy}A{rx} {ry} 0 1 1 {x - rx} {cy}Z"

    # the inside of the ring, seen through its opening: darker on the shaded side
    ic.path(ell(40, 66) + ell(26, 56, 5), fill_rule="evenodd",
            fill=ic.lin([(0, "#5A0610"), (0.55, "#8E0A18"), (1, "#D21A2C")], 0, 0, 1, 0))
    # the face of the ring
    ic.path(ell(74, 90) + ell(40, 66), fill_rule="evenodd",
            fill=ic.rad([(0, "#FF6B6B"), (0.4, "#F2192E"), (0.85, "#B30A1C"), (1, "#7E0612")],
                        cx=0.36, cy=0.3, r=0.8))
    # gloss: a long highlight on the upper left, a rim light on the inner edge
    ic.path(f"M{cx - 60} {cy - 4}C{cx - 62} {cy - 52} {cx - 34} {cy - 82} {cx + 2} {cy - 84}"
            f"C{cx - 30} {cy - 72} {cx - 50} {cy - 46} {cx - 50} {cy + 2}Z", fill="#fff", opacity=0.42)
    ic.path(f"M{cx + 34} {cy - 40}A40 66 0 0 1 {cx + 36} {cy + 36}", fill="none", stroke="#FFB0B4",
            stroke_width=2, stroke_opacity=0.55, stroke_linecap="round")
    ic.path(ell(74, 90), fill="none", stroke="#5A0510", stroke_opacity=0.5, stroke_width=1.5)
    ic.path(f"M{cx + 50} {cy + 66}A74 90 0 0 1 {cx - 20} {cy + 88}", fill="none", stroke="#FF8A8E",
            stroke_opacity=0.35, stroke_width=1.5)
    ic.ellipse(cx - 46, cy - 50, 6, 3.5, fill="#fff", opacity=0.85, transform=f"rotate(-50 {cx - 46} {cy - 50})")
    # its maker's name, in gold along the foot
    _arc_text(ic, "OPERA", cx, cy + 10, 70, 180, 7, font="mono-semibold", spacing=1.6, below=True,
              fill="#F2C45C", opacity=0.9)


@small("opera")
def opera16(ic):
    tile(ic, "#2E3040", "#101118")
    ic.path("M3 8A5 6.2 0 1 1 13 8A5 6.2 0 1 1 3 8ZM5.6 8A2.4 4.4 0 1 0 10.4 8A2.4 4.4 0 1 0 5.6 8Z",
            fill_rule="evenodd", fill="#F2192E")
    ic.path("M5.6 8A2.4 4.4 0 1 0 10.4 8A2.4 4.4 0 1 0 5.6 8ZM6.8 8A1.6 3.8 0 1 0 10 8A1.6 3.8 0 1 0 6.8 8Z",
            fill_rule="evenodd", fill="#8E0A18")
    ic.path("M4.2 7C4.4 4.4 5.8 2.8 7.4 2.6 6 3.6 5.2 5 5.1 7z", fill="#fff", opacity=0.55)


# --- Tor Browser: a purple onion on a board, one half cut ---------------------

@icon("torbrowser", kind="app", title="Tor Browser",
      names=["browser-tor", "com.github.micahflee.torbrowser-launcher", "org.torproject.torbrowser-launcher",
             "tor", "tor-browser", "tor-browser-en", "tor-browser-ru", "torbrowser"])
def tor(ic):
    tile(ic, "#3E2C5A", "#1A1230")
    shadow(ic, 128, 216, 100, 11)
    # the board
    ic.rect(26, 178, 204, 30, rx=10, fill=ic.lin([(0, "#8A5A30"), (1, "#5A3416")]))
    ic.rect(26, 164, 204, 30, rx=10, fill=wood(ic, "#E2B47E", "#B07A44"))
    ic.ellipse(212, 179, 6, 4, fill="#7A4A22")
    for y, x0, x1 in ((172, 40, 120), (180, 70, 190), (186, 36, 96)):
        ic.line(x0, y, x1, y, stroke="#9A6634", stroke_opacity=0.35, stroke_width=1)
    ic.line(34, 165, 222, 165, stroke="#FFE7C4", stroke_opacity=0.5, stroke_width=1.5)
    # the whole onion, behind
    ox = 98
    bulb = (f"M{ox} 30C{ox + 4} 58 {ox + 62} 66 {ox + 60} 116C{ox + 58} 156 {ox + 28} 176 {ox} 176"
            f"C{ox - 28} 176 {ox - 58} 156 {ox - 60} 116C{ox - 62} 66 {ox - 4} 58 {ox} 30Z")
    ic.path(bulb, fill=ic.rad([(0, "#B47AD4"), (0.5, "#7D4698"), (1, "#42205A")], cx=0.36, cy=0.4, r=0.75))
    with ic.g(fill="none", stroke_linecap="round"):
        for dx, c, o in ((-40, "#E4C6F2", 0.35), (-22, "#E4C6F2", 0.45), (-4, "#E4C6F2", 0.3), (16, "#2E1240", 0.3),
                         (34, "#2E1240", 0.35)):
            ic.path(f"M{ox + dx * 0.15} 52Q{ox + dx * 1.45} 110 {ox + dx * 0.55} 172", stroke=c,
                    stroke_opacity=o, stroke_width=1.6)
    ic.path(f"M{ox - 3} 30C{ox - 6} 22 {ox - 4} 14 {ox + 2} 10C{ox + 1} 18 {ox + 6} 24 {ox + 4} 32Z",
            fill="#C8A878")
    ic.path(f"M{ox - 30} 82C{ox - 40} 100 {ox - 42} 120 {ox - 38} 136", fill="none", stroke="#fff",
            stroke_opacity=0.45, stroke_width=4, stroke_linecap="round")
    # the cut half, in front: its rings, nested and meeting low on the left
    hx, hy = 164, 140
    ic.circle(hx + 3, hy + 5, 46, fill="#200C30", opacity=0.4)
    rings = [(46, "#6A3486"), (42, "#F6EEF9"), (34, "#8C55AA"), (30, "#F1E6F6"), (22, "#9C66BA"), (18, "#EEE0F4"),
             (10, "#7D4698")]
    for r, c in rings:
        k = (46 - r) * 0.3
        ic.circle(hx + k, hy - k * 0.6, r, fill=c)
    ic.circle(hx, hy, 46, fill="none", stroke="#3A1650", stroke_opacity=0.5, stroke_width=1.5)
    ic.circle(hx, hy, 46, fill=glare(ic, 1.5))
    ic.ellipse(hx - 18, hy - 22, 10, 4, fill="#fff", opacity=0.6, transform=f"rotate(-40 {hx - 18} {hy - 22})")
    for a, b in ((150, 156), (200, 206)):
        ic.path(f"M{a} {hy + 38}l2 6", stroke="#fff", stroke_opacity=0.5)
        del b


@small("torbrowser")
def tor16(ic):
    tile(ic, "#3E2C5A", "#1A1230")
    ic.rect(1.6, 11.6, 12.8, 2.6, rx=1, fill="#D6A46E")
    ic.path("M6 2C6.4 4 10 4.8 10 8.2 10 10.6 8.2 12 6 12S2 10.6 2 8.2C2 4.8 5.6 4 6 2Z", fill="#7D4698")
    ic.circle(10.6, 9.4, 3.6, fill="#6A3486")
    ic.circle(10.8, 9.3, 2.8, fill="#F6EEF9")
    ic.circle(11, 9.2, 1.7, fill="#8C55AA")
    ic.circle(11.1, 9.1, 0.8, fill="#F6EEF9")
