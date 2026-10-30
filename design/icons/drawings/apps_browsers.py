"""The theme's browsers: Firefox, Chrome, Chromium, Brave, Edge, Vivaldi,
Opera, Tor Browser (docs/feat/object-icons.md, Part 2). Each mark is
redrawn, simplified, as an object of its own: no two browsers share one."""

import math

from lib import (brass, glare, icon, paper, polar, shadow, small, steel, text_path, tile, wood)


def _d(pts, close=True):
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + ("Z" if close else "")


def _interp(keys, a):
    """Piecewise linear: keys (angle, value), angles falling."""
    for (a0, v0), (a1, v1) in zip(keys, keys[1:]):
        if a1 <= a <= a0:
            t = (a0 - a) / (a0 - a1) if a0 != a1 else 0
            return v0 + (v1 - v0) * t
    return keys[-1][1]


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


def _pinwheel(ic, cx, cy, R, r1, fills):
    """Three segments around a ring of radius r1, each bounded by a line
    tangent to it (the Chrome and Chromium construction, redrawn)."""
    ex = []
    for th in (0, 120, 240):
        tx, ty = polar(cx, cy, r1, th)
        dx, dy = math.sin(math.radians(th + 90)), -math.cos(math.radians(th + 90))
        # how far along the tangent the line meets the outer circle
        s = math.sqrt(R * R - r1 * r1)
        ex.append(((tx, ty), (tx + dx * s, ty + dy * s)))
    for i in range(3):
        (t0, e0), (t1, e1) = ex[i - 1], ex[i]
        ic.path(f"M{t0[0]:.1f} {t0[1]:.1f}L{e0[0]:.1f} {e0[1]:.1f}A{R} {R} 0 0 1 {e1[0]:.1f} {e1[1]:.1f}"
                f"L{t1[0]:.1f} {t1[1]:.1f}L{cx} {cy}Z", fill=fills[i])
    return ex


# --- Firefox: a desk globe, a fox curled round it ----------------------------

FOX_T = [(40, 22), (10, 15), (-40, 17), (-100, 27), (-160, 31), (-200, 24), (-224, 15), (-238, 3)]


def _fox_band(gx, gy, m, step=2.5):
    out, inn = [], []
    a = 40.0
    while a >= -238:
        t = _interp(FOX_T, a)
        mm = m + (a < -200) * (a + 200) * 0.25
        out.append(polar(gx, gy, mm + t / 2, a))
        inn.append(polar(gx, gy, mm - t / 2, a))
        a -= step
    return out, inn


@icon("firefox", kind="app", title="Firefox",
      names=["firefox", "firefox-beta", "firefox-bin", "firefox-esr", "firefox-icon", "firefox-mozilla-build",
             "org.mozilla.Firefox", "org.mozilla.firefox"])
def firefox(ic):
    tile(ic, "#3B3F86", "#17183D")
    gx, gy, rg = 122, 110, 60
    shadow(ic, 124, 214, 86, 11)
    # the foot, turned wood with a brass plate
    ic.rect(80, 196, 88, 12, rx=6, fill=ic.lin([(0, "#6A3E1E"), (1, "#3A200C")]))
    ic.ellipse(124, 197, 44, 8, fill=wood(ic, "#B97E4A", "#7A4A22"))
    ic.ellipse(124, 196.2, 41, 6.5, fill="none", stroke="#fff", stroke_opacity=0.18)
    ic.rect(119, 178, 10, 20, rx=2, fill=brass(ic, 0, 0, 1, 0))
    # the meridian ring, brass, behind the globe
    ic.circle(gx, gy, 68, fill="none", stroke="#3A2A10", stroke_width=6, stroke_opacity=0.5,
              transform="translate(1.5 2)")
    ic.circle(gx, gy, 68, fill="none", stroke=brass(ic), stroke_width=5)
    for a in (55, 70, 85, 100, 115):
        x1, y1 = polar(gx, gy, 66, a)
        x2, y2 = polar(gx, gy, 70.5, a)
        ic.line(x1, y1, x2, y2, stroke="#5A3E12", stroke_width=1)
    # the globe, violet glass
    ic.circle(gx, gy, rg, fill=ic.rad([(0, "#A795FF"), (0.45, "#6544E0"), (0.85, "#33208F"), (1, "#22156A")],
                                      cx=0.36, cy=0.3, r=0.75))
    clip = ic.clip(f'<circle cx="{gx}" cy="{gy}" r="{rg}"/>')
    with ic.g(clip_path=clip, fill="none", stroke="#D9D0FF", stroke_opacity=0.28, stroke_width=1.2):
        for ry in (14, 32, 48):
            ic.ellipse(gx, gy, rg, ry)
        for rx in (20, 42):
            ic.ellipse(gx, gy, rx, rg)
        ic.line(gx, gy - rg, gx, gy + rg)
    with ic.g(clip_path=clip, fill="#C7BBFF", opacity=0.22):
        ic.path("M84 76c10-8 26-6 30 2s-4 12-2 20-8 14-16 10-6-12-12-14-8-12 0-18z")
        ic.path("M132 72c8-4 22 0 26 8s-2 10-10 10-6 6-12 4-12-16-4-22z")
        ic.path("M140 112c10 0 18 8 16 18s-10 20-18 18-6-14-4-22-4-14 6-14z")
    ic.circle(gx, gy, rg, fill=glare(ic, 1.6))
    ic.ellipse(100, 78, 18, 9, fill="#fff", opacity=0.3, transform="rotate(-35 100 78)")
    # the fox's shadow on the glass
    out, inn = _fox_band(gx + 2, gy + 3, 68)
    ic.path(_d(out + inn[::-1]), fill="#120A40", opacity=0.35)
    # the fox, curled round it: head at the top right, tail round the bottom
    out, inn = _fox_band(gx, gy, 68)
    head = [(170, 80), (188, 86), (211, 78), (205, 66), (199, 57), (203, 34), (192, 45), (181, 22), (174, 44)]
    fur = ic.lin([(0, "#FFE65C"), (0.28, "#FFA733"), (0.62, "#FF5A2C"), (1, "#E0205E")], 204, 30, 40, 196,
                 units="userSpaceOnUse")
    ic.path(_d([inn[0]] + head + out + inn[::-1]), fill=fur, stroke=fur, stroke_width=2, stroke_linejoin="round")
    # its ear, cheek, eye and nose
    ic.path("M182 29l4 14-6 1z", fill="#9A2A16", opacity=0.55)
    ic.path("M201 40l-1 12-5-6z", fill="#9A2A16", opacity=0.45)
    ic.path("M186 70c8 0 16 4 25 8-8 5-17 8-27 6-6-1-9-6-6-10z", fill="#FFF3D6")
    ic.ellipse(194, 63, 3, 2, fill="#2A0E06", transform="rotate(25 194 63)")
    ic.circle(209.5, 77.5, 2.3, fill="#2A0E06")
    # the tail's pale tip
    tip_o, tip_i = _fox_band(gx, gy, 68, 1.5)
    k = next(i for i, p in enumerate(tip_o) if _angle(gx, gy, p) < -218)
    ic.path(_d(tip_o[k:] + tip_i[k:][::-1]), fill="#FFE6B0", opacity=0.9)
    # light along its back, shade along its belly
    lo = [p for p in out[4:60]]
    ic.path(_d(lo, close=False), fill="none", stroke="#FFF6C4", stroke_width=2, stroke_opacity=0.7,
            stroke_linecap="round")
    ic.path(_d(inn[50:100], close=False), fill="none", stroke="#7A0A2E", stroke_width=2, stroke_opacity=0.4)
    for a in (-60, -95, -130, -165):
        x1, y1 = polar(gx, gy, 72 + _interp(FOX_T, a) * 0.2, a)
        x2, y2 = polar(gx, gy, 66, a - 9)
        ic.line(x1, y1, x2, y2, stroke="#9A1A2A", stroke_opacity=0.35, stroke_width=1.4, stroke_linecap="round")
    # the plate on the foot
    ic.rect(104, 199, 40, 7, rx=1.5, fill=brass(ic))
    ic.text("FIREFOX", 124, 204.6, 5, font="mono-semibold", anchor="middle", spacing=0.8, fill="#4A3210")


def _angle(cx, cy, p):
    a = math.degrees(math.atan2(p[0] - cx, cy - p[1]))
    return a if a <= 45 else a - 360


@small("firefox")
def firefox16(ic):
    tile(ic, "#3B3F86", "#17183D")
    ic.circle(8.6, 7.4, 4.4, fill="#6544E0")
    ic.circle(7.4, 6.2, 1.8, fill="#A795FF", opacity=0.6)
    ic.path("M13.4 5.4A6 6 0 1 1 6.2 2.2 4.6 4.6 0 1 0 13.4 5.4Z", fill="#FF8A2C")
    ic.path("M2 9A6 6 0 0 0 9.6 13.8 6.2 6.2 0 0 1 2 9Z", fill="#E0205E")
    ic.path("M10.4 3.6l1.4-2.4.6 2.2 1.6-.6-.4 2.2 1 .8-2.4.4z", fill="#FFB43A")
    ic.rect(6, 14, 4, 1, rx=0.5, fill="#B97E4A")


# --- Google Chrome: a camera lens, its glass in the three enamels -------------

def _lens(ic, cx, cy, name, colours, centre):
    shadow(ic, cx, 214, 92, 11)
    # the barrel's side, seen from a little above
    ic.circle(cx, cy + 12, 92, fill=ic.lin([(0, "#3A3E44"), (1, "#16181B")]))
    ic.rect(cx - 92, cy, 184, 12, fill=ic.lin([(0, "#2A2D31"), (0.5, "#5A5F66"), (1, "#1E2023")], 0, 0, 1, 0))
    # the focus grip, knurled
    ic.circle(cx, cy, 92, fill=steel(ic, False))
    ic.circle(cx, cy, 89, fill="none", stroke="#2A2D31", stroke_width=6, stroke_dasharray="1.6 2.2",
              stroke_opacity=0.55)
    ic.circle(cx, cy, 91.2, fill="none", stroke="#fff", stroke_opacity=0.35, stroke_width=1.2)
    # the front ring, black, its legend in white
    ic.circle(cx, cy, 85, fill=ic.lin([(0, "#2E3136"), (1, "#0E0F11")], 0, 0, 1, 1))
    ic.circle(cx, cy, 84.2, fill="none", stroke="#fff", stroke_opacity=0.16, stroke_width=1.2)
    _arc_text(ic, name, cx, cy, 77, 0, 7.2, fill="#ECEDEE")
    _arc_text(ic, "1:1.4  f=50mm  Ø52", cx, cy, 77, 180, 6.2, font="mono", below=True, fill="#B9BCC0")
    ic.circle(cx + 52, cy - 52, 2.2, fill="#E8463A")
    # the glass: the three segments, the white ring, the blue eye
    ic.circle(cx, cy, 70, fill="#0B0C0E")
    _pinwheel(ic, cx, cy, 68, 29, colours)
    ic.circle(cx, cy, 68, fill="none", stroke="#000", stroke_opacity=0.3, stroke_width=2)
    ic.circle(cx + 1.5, cy + 2.5, 30, fill="#000", opacity=0.3)
    ic.circle(cx, cy, 30, fill=ic.lin([(0, "#FFFFFF"), (1, "#D9DCE0")], 0, 0, 1, 1))
    ic.circle(cx, cy, 23, fill=centre)
    ic.circle(cx, cy, 23, fill="none", stroke="#000", stroke_opacity=0.2, stroke_width=1.5)
    # coating reflections and glare, light from the top left
    ic.path(f"M{cx - 52} {cy - 30}a60 60 0 0 1 40-34", fill="none", stroke="#C9A8FF", stroke_width=3,
            stroke_opacity=0.5, stroke_linecap="round")
    ic.path(f"M{cx + 30} {cy + 50}a58 58 0 0 0 26-24", fill="none", stroke="#9CFFC8", stroke_width=2.2,
            stroke_opacity=0.4, stroke_linecap="round")
    ic.ellipse(cx - 8, cy - 9, 7, 4.5, fill="#fff", opacity=0.75, transform=f"rotate(-35 {cx - 8} {cy - 9})")
    ic.circle(cx, cy, 68, fill=glare(ic, 1.4))


CHROME = [("#EA4335", "#C5281C"), ("#FBC02D", "#E39A10"), ("#34A853", "#1E7E3A")]


@icon("google-chrome", kind="app", title="Google Chrome",
      names=["com.google.Chrome", "google-chrome", "google-chrome2", "googlechrome"])
def chrome(ic):
    tile(ic, "#5A6774", "#262E37")
    fills = [ic.lin([(0, a), (1, b)], 0, 0, 1, 1) for a, b in CHROME]
    _lens(ic, 128, 112, "GOOGLE CHROME", fills,
          ic.rad([(0, "#7FB0FF"), (0.6, "#2F74E8"), (1, "#1A4FB0")], cx=0.38, cy=0.35, r=0.7))


@small("google-chrome")
def chrome16(ic):
    tile(ic, "#5A6774", "#262E37")
    ic.circle(8, 8, 6.4, fill="#1A1C1F")
    _pinwheel(ic, 8, 8, 5.2, 2.3, [c[0] for c in CHROME])
    ic.circle(8, 8, 2.4, fill="#fff")
    ic.circle(8, 8, 1.7, fill="#2F74E8")


# --- Chromium: a glass paperweight, the mark in three blues inside -------------

CHROMIUM = [("#5E97F6", "#3F7BE0"), ("#A9C8FF", "#7FA8F0"), ("#2A5DC0", "#1A438E")]


@icon("chromium", kind="app", title="Chromium",
      names=["chromium", "chromium-browser", "chromium-browser-privacy", "chromium-freeworld",
             "com.github.Eloston.UngoogledChromium", "org.chromium.Chromium"])
def chromium(ic):
    tile(ic, "#2B4766", "#101E30")
    cx = 128
    shadow(ic, cx, 206, 100, 14)
    # light through the glass, falling on the desk
    ic.ellipse(cx + 10, 206, 60, 7, fill=ic.rad([(0, "#9CC4FF", 0.55), (1, "#9CC4FF", 0)]))
    dome = f"M{cx - 92} 186C{cx - 92} 92 {cx - 50} 34 {cx} 34S{cx + 92} 92 {cx + 92} 186" \
           f"A92 18 0 0 1 {cx - 92} 186Z"
    # the glass body, faintly blue, darker at its edges
    ic.path(dome, fill=ic.rad([(0, "#DCEBFF", 0.12), (0.7, "#8FB6F0", 0.22), (1, "#1C3A66", 0.65)],
                              cx=0.45, cy=0.5, r=0.6))
    # the base, seen through the glass
    ic.ellipse(cx, 186, 86, 15, fill="#0E1B2C", opacity=0.45)
    ic.ellipse(cx, 184, 78, 12, fill=ic.lin([(0, "#E8F2FF", 0.35), (1, "#9CC4FF", 0.15)]))
    ic.ellipse(cx, 184, 78, 12, fill="none", stroke="#E8F2FF", stroke_opacity=0.5)
    ic.text("chromium", cx, 188, 7, font="sans-semibold", anchor="middle", spacing=1.2, fill="#DCEBFF",
            opacity=0.55)
    # the mark inside, enlarged by the dome
    ic.circle(cx + 2, 124, 62, fill="#0A1A33", opacity=0.35)
    fills = [ic.lin([(0, a), (1, b)], 0, 0, 1, 1) for a, b in CHROMIUM]
    _pinwheel(ic, cx, 120, 60, 26, fills)
    ic.circle(cx, 120, 60, fill="none", stroke="#0A1A33", stroke_opacity=0.35, stroke_width=1.5)
    ic.circle(cx + 1, 122, 27, fill="#000", opacity=0.25)
    ic.circle(cx, 120, 27, fill=ic.lin([(0, "#FFFFFF"), (1, "#DCE6F5")], 0, 0, 1, 1))
    ic.circle(cx, 120, 20, fill=ic.rad([(0, "#5E97F6"), (1, "#1C4793")], cx=0.38, cy=0.35, r=0.7))
    ic.ellipse(cx - 7, 112, 5.5, 3.2, fill="#fff", opacity=0.7, transform=f"rotate(-35 {cx - 7} 112)")
    # the dome's surface: edge light, glare from the top left, a bright rim below
    ic.path(dome, fill="none", stroke="#E4F0FF", stroke_opacity=0.45, stroke_width=2)
    ic.path(f"M{cx - 80} 150C{cx - 82} 96 {cx - 50} 46 {cx - 4} 42C{cx - 46} 56 {cx - 68} 100 {cx - 70} 150Z",
            fill="#fff", opacity=0.42)
    ic.path(f"M{cx + 50} 58C{cx + 70} 74 {cx + 82} 100 {cx + 84} 130", fill="none", stroke="#fff",
            stroke_opacity=0.3, stroke_width=3, stroke_linecap="round")
    ic.path(f"M{cx - 88} 190A92 18 0 0 0 {cx + 88} 190", fill="none", stroke="#CFE3FF", stroke_opacity=0.7,
            stroke_width=2)
    ic.ellipse(cx - 38, 66, 9, 5, fill="#fff", opacity=0.8, transform=f"rotate(-40 {cx - 38} 66)")


@small("chromium")
def chromium16(ic):
    tile(ic, "#2B4766", "#101E30")
    ic.path("M2 12.5C2 6 4.6 2.4 8 2.4S14 6 14 12.5A6 1.4 0 0 1 2 12.5Z", fill="#9CC4FF", opacity=0.35)
    _pinwheel(ic, 8, 8.4, 4.6, 2, [c[0] for c in CHROMIUM])
    ic.circle(8, 8.4, 2.1, fill="#fff")
    ic.circle(8, 8.4, 1.5, fill="#2E63C4")
    ic.path("M3.6 10C3.6 6.4 5 4 7 3.4 5.2 4.8 4.6 7 4.6 10z", fill="#fff", opacity=0.6)


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
