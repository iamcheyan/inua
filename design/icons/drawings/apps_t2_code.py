"""The inua-objects theme, tier 2 code: Godot, Unity Hub, Arduino IDE,
Qt Creator, Geany, Kate, Text Editor, Meld, GitKraken, Bruno, Beekeeper
Studio, pgAdmin, MongoDB Compass, Podman Desktop
(docs/feat/object-icons.md, Part 2). Marks are redrawn, simplified."""

import math

from lib import (brass, glare, graphite, icon, paper, polar, shadow, small, steel, tile, wood)


def _f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def _bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def _taper(pts, w0, w1, n=14):
    """A limb along a chain of cubic Béziers (P0 C C P1 C C P2 …), w0 wide
    at its start and w1 at its end, its end rounded: a tentacle, a trunk."""
    line = []
    for s in range(0, len(pts) - 1, 3):
        for i in range(n + (1 if s + 4 >= len(pts) else 0)):
            line.append(_bez(pts[s], pts[s + 1], pts[s + 2], pts[s + 3], i / n))
    m = len(line)
    left, right = [], []
    for i, (x, y) in enumerate(line):
        a, b = line[max(i - 1, 0)], line[min(i + 1, m - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy) or 1
        w = (w0 + (w1 - w0) * i / (m - 1)) / 2
        left.append((x - dy / d * w, y + dx / d * w))
        right.append((x + dy / d * w, y - dx / d * w))
    ex, ey = line[-1]
    r = w1 / 2
    d = "M" + "L".join(f"{_f(x)} {_f(y)}" for x, y in left)
    d += f"A{_f(r)} {_f(r)} 0 0 0 {_f(right[-1][0])} {_f(right[-1][1])}"
    d += "L" + "L".join(f"{_f(x)} {_f(y)}" for x, y in reversed(right)) + "Z"
    return d


def _pts(pts):
    return "M" + "L".join(f"{_f(x)} {_f(y)}" for x, y in pts) + "Z"


def _ring_text(ic, s, cx, cy, r, start, step, size, **kw):
    """Letters set one by one round a ring, upright along the radius."""
    for i, ch in enumerate(s):
        if ch == " ":
            continue
        with ic.g(transform=f"rotate({_f(start + i * step)} {cx} {cy})"):
            ic.text(ch, cx, cy - r, size, anchor="middle", **kw)


# --- Godot: the robot head as a tin toy on a stand ---------------------------

@icon("godot", kind="app", names=["godot", "godot-mono", "org.godotengine.Godot", "org.godotengine.Godot3"],
      title="Godot")
def godot(ic):
    tile(ic, "#35546F", "#152536")
    shadow(ic, 128, 214, 84, 11)
    # the stand
    ic.ellipse(128, 206, 58, 10, fill="#14181D")
    ic.rect(70, 192, 116, 14, fill=graphite(ic))
    ic.ellipse(128, 192, 58, 10, fill=ic.lin([(0, "#5A6068"), (1, "#2A2E34")], 0, 0, 1, 1))
    ic.text("GODOT", 128, 204.5, 7, font="mono-semibold", anchor="middle", spacing=2.2, fill="#C3C8CE", opacity=0.7)
    ic.rect(104, 176, 48, 18, fill=steel(ic))
    blue = ic.lin([(0, "#8FCBF2"), (0.45, "#4F96C9"), (1, "#24557E")], 40, 40, 200, 200, units="userSpaceOnUse")
    dark = ic.lin([(0, "#3F7FAE"), (1, "#1C4466")], 0, 0, 0, 1)
    # the ears, side plates bolted on
    for x in (34, 196):
        ic.rect(x + 2, 116, 26, 42, rx=10, fill="#0F2638", opacity=0.5)
        ic.rect(x, 112, 26, 42, rx=10, fill=dark)
        ic.circle(x + 13, 133, 4.5, fill=steel(ic, False))
        ic.path(f"M{x + 10} 133h6", stroke="#4A5058", stroke_width=1.2)
    # the crown: three humps
    for cx, cy, r in ((82, 62, 19), (128, 52, 21), (174, 62, 19)):
        ic.circle(cx, cy, r, fill=blue)
    ic.rect(52, 56, 152, 128, rx=34, fill=blue)
    ic.path("M60 90 a32 32 0 0 1 20-30 M66 58 a19 19 0 0 1 22-14 M112 40 a21 21 0 0 1 22-8",
            fill="none", stroke="#fff", stroke_opacity=0.45, stroke_width=2.2, stroke_linecap="round")
    ic.path("M52 150 v0a34 34 0 0 0 34 34h84a34 34 0 0 0 34-34", fill="none", stroke="#0F2638",
            stroke_opacity=0.35, stroke_width=3)
    # the jaw, a darker plate, and the mouth with its round teeth
    ic.path("M60 148 H196 V152 a32 32 0 0 1 -32 32 H92 a32 32 0 0 1 -32-32z", fill=dark, opacity=0.85)
    ic.rect(74, 150, 108, 16, rx=8, fill="#EEF5FB")
    ic.rect(74, 150, 108, 4, rx=2, fill="#fff", opacity=0.7)
    for x in (92, 110, 128, 146, 164):
        ic.circle(x, 158, 4.6, fill="#3A78A8")
        ic.circle(x - 1, 157, 1.6, fill="#9ED0F2", opacity=0.6)
    # rivets round the face
    for x in (68, 188):
        for y in (78, 172):
            ic.circle(x, y, 2.6, fill="#CFE6F6")
            ic.circle(x + 0.6, y + 0.8, 2.6, fill="#0F2638", opacity=0.35)
            ic.circle(x, y, 2.2, fill="#B5D6EE")
    # the eyes
    for ex, px in ((96, 102), (160, 154)):
        ic.circle(ex + 1, 112, 25, fill="#0F2638", opacity=0.45)
        ic.circle(ex, 110, 25, fill=ic.rad([(0, "#FFFFFF"), (0.8, "#EAF2F8"), (1, "#B9CCDA")], cx=0.4, cy=0.35, r=0.7))
        ic.circle(px, 113, 11.5, fill="#3E4147")
        ic.circle(px - 3.5, 109, 3.6, fill="#fff")
    ic.path("M76 98 a25 25 0 0 1 14-12", fill="none", stroke="#fff", stroke_width=2, stroke_linecap="round")


@small("godot")
def godot16(ic):
    tile(ic, "#35546F", "#152536")
    ic.rect(1.6, 7, 2.4, 3.4, rx=0.8, fill="#2F6E9E")
    ic.rect(12, 7, 2.4, 3.4, rx=0.8, fill="#2F6E9E")
    for cx, cy, r in ((5, 4.4, 1.6), (8, 3.6, 1.8), (11, 4.4, 1.6)):
        ic.circle(cx, cy, r, fill="#5AA2D6")
    ic.rect(3, 4, 10, 9.5, rx=2.4, fill="#5AA2D6")
    ic.circle(6, 7.5, 1.9, fill="#fff")
    ic.circle(10, 7.5, 1.9, fill="#fff")
    ic.circle(6.4, 7.7, 0.9, fill="#3E4147")
    ic.circle(9.6, 7.7, 0.9, fill="#3E4147")
    ic.rect(4.5, 10.4, 7, 1.3, rx=0.6, fill="#EEF5FB")


# --- Unity Hub: a white ceramic cube on a turned display stand ---------------

@icon("unityhub", kind="app", names=["appimagekit-unityhub", "com.unity.UnityHub", "unity-hub", "unityhub"],
      title="Unity Hub")
def unityhub(ic):
    tile(ic, "#45494F", "#17191C")
    shadow(ic, 128, 216, 78, 10)
    # the stand: a base, a stem, a plate
    ic.ellipse(128, 208, 50, 11, fill="#0E0F11")
    ic.rect(78, 198, 100, 10, fill=graphite(ic))
    ic.ellipse(128, 198, 50, 11, fill=ic.lin([(0, "#55595F"), (1, "#26282C")], 0, 0, 1, 1))
    ic.text("UNITY", 128, 206.5, 6, font="mono-semibold", anchor="middle", spacing=2, fill="#AEB3B9", opacity=0.6)
    ic.rect(117, 176, 22, 24, fill=steel(ic))
    plate = ic.lin([(0, "#9DA2A9"), (0.5, "#6A6F76"), (1, "#3A3D42")], 0, 0, 1, 1)
    ic.path("M54 150 a74 34 0 0 0 148 0 v10 a74 34 0 0 1 -148 0z", fill="#141518")
    ic.ellipse(128, 150, 74, 34, fill=plate)
    ic.ellipse(128, 150, 74, 34, fill="none", stroke="#fff", stroke_opacity=0.18, stroke_width=1.5)
    ic.ellipse(128, 150, 62, 28, fill="none", stroke="#000", stroke_opacity=0.25, stroke_width=1.2)
    ic.ellipse(128, 162, 52, 13, fill="#000", opacity=0.3)
    # the cube, light from the top left
    a, b, h, T = 54, 31, 62, 38
    top = [(128, T), (128 + a, T + b), (128, T + 2 * b), (128 - a, T + b)]
    left = [(128 - a, T + b), (128, T + 2 * b), (128, T + 2 * b + h), (128 - a, T + b + h)]
    right = [(128 + a, T + b), (128 + a, T + b + h), (128, T + 2 * b + h), (128, T + 2 * b)]
    ic.path(_pts(top), fill=ic.lin([(0, "#FFFFFF"), (1, "#E4E6E9")], 0, 0, 1, 1))
    ic.path(_pts(left), fill=ic.lin([(0, "#E2E4E7"), (1, "#B9BDC2")], 0, 0, 1, 1))
    ic.path(_pts(right), fill=ic.lin([(0, "#8E939A"), (1, "#5C6168")], 0, 0, 1, 1))
    # the mark: the seams of a Y and the corners notched
    seam = dict(stroke="#1F2125", stroke_width=6.5, stroke_linecap="butt")
    ic.line(128, T + 2 * b, 128, T + 2 * b + h, **seam)
    ic.line(128, T + 2 * b, 128 - a, T + b, **seam)
    ic.line(128, T + 2 * b, 128 + a, T + b, **seam)
    ic.circle(128, T + 2 * b, 6, fill="#1F2125")
    hexa = [(128, T), (128 + a, T + b), (128 + a, T + b + h), (128, T + 2 * b + h), (128 - a, T + b + h), (128 - a, T + b)]
    ic.path(_pts(hexa), fill="none", stroke="#1F2125", stroke_width=3, stroke_linejoin="round")
    # light along the top edges
    ic.line(128 - a + 3, T + b - 1, 128 - 3, T + 2.5, stroke="#fff", stroke_width=1.5, opacity=0.9)
    ic.line(128 - a + 0.8, T + b + 3, 128 - a + 0.8, T + b + h - 3, stroke="#fff", stroke_width=1.2, opacity=0.6)


@small("unityhub")
def unityhub16(ic):
    tile(ic, "#45494F", "#17191C")
    ic.ellipse(8, 12.6, 5.6, 1.8, fill="#5A5E64")
    ic.poly([(8, 2), (12.5, 4.6), (8, 7.2), (3.5, 4.6)], fill="#FFFFFF")
    ic.poly([(3.5, 4.6), (8, 7.2), (8, 12.4), (3.5, 9.8)], fill="#C9CCD0")
    ic.poly([(12.5, 4.6), (12.5, 9.8), (8, 12.4), (8, 7.2)], fill="#7A7F86")
    ic.path("M8 7.2V12.4M8 7.2L3.5 4.6M8 7.2L12.5 4.6", stroke="#1F2125", stroke_width=0.8)


# --- Arduino IDE: a teal board, its infinity printed in white ----------------

def _infinity(cx, cy, w, h):
    """The infinity sign as a path to stroke: two loops crossing at cx."""
    q = w / 2
    return (f"M{_f(cx)} {_f(cy)}C{_f(cx + q * 0.35)} {_f(cy - h)} {_f(cx + q)} {_f(cy - h)} {_f(cx + q)} {_f(cy)}"
            f"C{_f(cx + q)} {_f(cy + h)} {_f(cx + q * 0.35)} {_f(cy + h)} {_f(cx)} {_f(cy)}"
            f"C{_f(cx - q * 0.35)} {_f(cy - h)} {_f(cx - q)} {_f(cy - h)} {_f(cx - q)} {_f(cy)}"
            f"C{_f(cx - q)} {_f(cy + h)} {_f(cx - q * 0.35)} {_f(cy + h)} {_f(cx)} {_f(cy)}Z")


@icon("arduino", kind="app", names=["arduino", "arduino-icon-small", "arduino-ide", "cc.arduino.IDE2",
                                     "cc.arduino.arduinoide"], title="Arduino IDE")
def arduino(ic):
    tile(ic, "#24676B", "#0C3236")
    shadow(ic, 130, 212, 100, 12)
    with ic.g(transform="rotate(-6 128 128)"):
        # the board, its thickness, its edge
        ic.rect(37, 68, 188, 130, rx=7, fill="#00393C")
        ic.rect(34, 64, 188, 130, rx=7, fill=ic.lin([(0, "#14B3B8"), (0.6, "#00979D"), (1, "#00777C")], 0, 0, 1, 1))
        ic.rect(34.75, 64.75, 186.5, 128.5, rx=6.25, fill="none", stroke="#7FE3E6", stroke_opacity=0.35,
                stroke_width=1.5)
        # traces
        for d in ("M70 120 H96 L104 128 H118", "M70 128 H92 L100 136 V150", "M180 92 V112 L170 122",
                  "M190 92 V114 L200 124 V168", "M104 100 L112 92 H150", "M62 140 H84 L92 148 V170"):
            ic.path(d, fill="none", stroke="#5ED3D6", stroke_opacity=0.35, stroke_width=1.6, stroke_linejoin="round")
        # mounting holes
        for x, y in ((46, 76), (210, 76), (210, 182), (100, 182)):
            ic.circle(x, y, 5.5, fill="#D9DEE3")
            ic.circle(x, y, 3.2, fill="#062A2C")
        # the headers
        for x0, x1, y in ((98, 206, 70), (118, 198, 180)):
            ic.rect(x0, y, x1 - x0, 11, rx=1.2, fill="#1A1C1F")
            ic.rect(x0, y, x1 - x0, 2, rx=1, fill="#fff", opacity=0.18)
            for x in range(x0 + 4, x1 - 2, 7):
                ic.rect(x, y + 3.5, 3.2, 3.2, fill="#0A0B0C")
                ic.rect(x + 0.4, y + 3.9, 1.2, 1.2, fill="#E8C46A")
        # the USB port and the power jack, over the left edge
        ic.rect(22, 86, 46, 32, rx=2, fill=steel(ic, False))
        ic.rect(22, 86, 46, 2, fill="#fff", opacity=0.5)
        ic.rect(24, 92, 8, 20, rx=1, fill="#1E2024")
        ic.rect(26, 96, 4, 12, fill="#D9DEE3")
        ic.rect(24, 146, 36, 30, rx=3, fill="#1E2024")
        ic.rect(24, 146, 36, 3, rx=1.5, fill="#fff", opacity=0.15)
        ic.circle(34, 161, 6, fill="#0A0B0C")
        ic.circle(34, 161, 2, fill="#AEB3B9")
        # the reset button, the lights
        ic.rect(72, 72, 16, 16, rx=2, fill=steel(ic, False))
        ic.circle(80, 80, 4.6, fill="#C8372D")
        ic.circle(79, 79, 1.6, fill="#fff", opacity=0.5)
        for y, c, t in ((98, "#F2C45C", "ON"), (108, "#7CF7A6", "L")):
            ic.rect(74, y, 8, 5, rx=1, fill=c)
            ic.text(t, 86, y + 5, 5, font="mono-semibold", fill="#fff", opacity=0.8)
        # the chip and its crystal
        ic.rect(84, 144, 18, 8, rx=4, fill=steel(ic))
        for x in range(122, 196, 7):
            ic.rect(x, 140, 3, 4, fill="#C3C8CE")
            ic.rect(x, 162, 3, 4, fill="#C3C8CE")
        ic.rect(116, 144, 84, 18, rx=1.5, fill="#1E2024")
        ic.rect(116, 144, 84, 2, fill="#fff", opacity=0.12)
        ic.circle(122, 153, 2, fill="#2E3136")
        ic.text("ATMEGA328P", 160, 156, 6.4, font="mono-semibold", anchor="middle", fill="#8C9096")
        # the mark, printed: infinity, minus and plus, and the name
        ic.path(_infinity(150, 110, 62, 15), fill="none", stroke="#FFFFFF", stroke_width=6.4, stroke_linejoin="round")
        ic.rect(126, 108.6, 9, 2.8, fill="#fff")
        ic.rect(165, 108.6, 9, 2.8, fill="#fff")
        ic.rect(168.1, 105.5, 2.8, 9, fill="#fff")
        ic.text("ARDUINO", 150, 136, 9.5, font="sans-bold", anchor="middle", spacing=1.2, fill="#FFFFFF")
        ic.text("UNO", 214, 132, 9, font="sans-bold", anchor="end", fill="#FFFFFF", opacity=0.9)


@small("arduino")
def arduino16(ic):
    tile(ic, "#24676B", "#0C3236")
    ic.rect(2, 3.5, 12.5, 9.5, rx=0.8, fill="#00979D")
    ic.rect(1.2, 5, 3, 2.6, fill="#B4BAC1")
    ic.rect(6, 4, 7.5, 1.1, fill="#1A1C1F")
    ic.rect(7, 11, 6, 1.1, fill="#1A1C1F")
    ic.path(_infinity(9.2, 8, 6, 2), fill="none", stroke="#fff", stroke_width=0.9)


# --- Qt Creator: a toolbox with tools in it, a green Qt badge on its front ---

def _qt_shape(x0, y0, x1, y1, c):
    return _pts([(x0 + c, y0), (x1, y0), (x1, y1 - c), (x1 - c, y1), (x0, y1), (x0, y0 + c)])


@icon("qtcreator", kind="app", names=["QtProject-qtcreator", "QtProject-qtcreator-qt5", "io.qt.QtCreator",
                                       "org.qt-project.qtcreator", "qt-creator", "qtcreator", "qtcreator_logo_32",
                                       "qtcreatorubuntu", "ubuntu-qtcreator"], title="Qt Creator")
def qtcreator(ic):
    tile(ic, "#3B5E48", "#15301F")
    shadow(ic, 128, 214, 100, 12)
    # inside, the back wall
    ic.path("M42 98 H214 L210 120 H46z", fill="#121417")
    # the tools, standing in it
    with ic.g(transform="rotate(-14 84 100)"):  # a screwdriver
        ic.rect(81, 34, 6, 50, fill=steel(ic))
        ic.path("M81 34 L84 26 L87 34z", fill="#9AA1A9")
        ic.rect(74, 78, 20, 48, rx=7, fill=ic.lin([(0, "#7BE58A"), (0.5, "#41CD52"), (1, "#22882F")], 0, 0, 1, 0))
        for x in (79, 84, 89):
            ic.line(x, 84, x, 120, stroke="#0E4A17", stroke_opacity=0.35, stroke_width=1.5)
    with ic.g(transform="rotate(10 168 100)"):  # a spanner
        ic.rect(161, 46, 14, 70, rx=3, fill=steel(ic))
        ic.path("M168 22 a20 20 0 1 1 -0.1 0z M163 24 v14 h10 v-14z", fill=steel(ic), fill_rule="evenodd")
        ic.path("M154 34 a16 16 0 0 1 8-10", fill="none", stroke="#fff", stroke_opacity=0.6, stroke_width=1.5)
    with ic.g(transform="rotate(4 128 100)"):  # a rule, folded
        ic.rect(118, 40, 16, 80, fill=ic.lin([(0, "#F6D46A"), (1, "#D8A62E")], 0, 0, 1, 0))
        for y in range(46, 116, 6):
            ic.line(118, y, 123 if y % 12 else 127, y, stroke="#3A2A10", stroke_width=1)
        ic.circle(126, 44, 2.6, fill=brass(ic))
    # the handle across the top
    for x in (50, 200):
        ic.rect(x, 52, 7, 52, rx=2, fill=steel(ic))
    ic.rect(48, 48, 160, 10, rx=5, fill=ic.lin([(0, "#E4E8EC"), (0.5, "#9AA1A9"), (1, "#4A5058")]))
    ic.rect(98, 46, 60, 14, rx=7, fill="#1E2024")
    ic.rect(100, 47, 56, 3, rx=1.5, fill="#fff", opacity=0.2)
    # the box: rim, body, ribs
    body = "M38 104 H218 L210 198 a6 6 0 0 1 -6 6 H52 a6 6 0 0 1 -6-6z"
    ic.path(body, fill=ic.lin([(0, "#4C525A"), (0.5, "#33373D"), (1, "#1C1F23")], 0, 0, 0.4, 1))
    ic.rect(34, 98, 188, 14, rx=4, fill=ic.lin([(0, "#E4E8EC"), (0.6, "#9AA1A9"), (1, "#5D636B")]))
    ic.line(36, 99.5, 220, 99.5, stroke="#fff", stroke_width=1.5, opacity=0.8)
    ic.line(48, 186, 208, 186, stroke="#000", stroke_opacity=0.35, stroke_width=2)
    ic.line(48, 188, 208, 188, stroke="#fff", stroke_opacity=0.08, stroke_width=1)
    ic.path("M40 112 L48 196", stroke="#fff", stroke_opacity=0.14, stroke_width=2)
    # the latches
    for x in (58, 186):
        ic.rect(x, 108, 14, 22, rx=2, fill=steel(ic))
        ic.rect(x + 3, 124, 8, 4, rx=1, fill="#4A5058")
    # the badge
    ic.path(_qt_shape(90, 126, 168, 182, 13), fill="#0B2A12", transform="translate(1.5 2.5)", opacity=0.6)
    ic.path(_qt_shape(90, 126, 168, 182, 13), fill=ic.lin([(0, "#7BE58A"), (0.5, "#41CD52"), (1, "#2A9A38")]))
    ic.path(_qt_shape(93, 129, 165, 179, 11), fill="none", stroke="#fff", stroke_opacity=0.35, stroke_width=1.2)
    ic.text("Qt", 129, 166, 34, font="sans-bold", anchor="middle", spacing=-1, fill="#fff")
    for x, y in ((96, 174), (162, 133)):
        ic.circle(x, y, 1.8, fill="#E4E8EC")


@small("qtcreator")
def qtcreator16(ic):
    tile(ic, "#3B5E48", "#15301F")
    ic.rect(4, 2.6, 1.4, 5, fill="#41CD52", transform="rotate(-14 4.7 5)")
    ic.rect(10.4, 2.4, 1.4, 5, fill="#B4BAC1", transform="rotate(10 11 5)")
    ic.rect(3.5, 2.6, 9, 1, rx=0.5, fill="#B4BAC1")
    ic.path("M2 6.4 H14 L13.4 13 H2.6z", fill="#33373D")
    ic.rect(1.8, 6, 12.4, 1.4, rx=0.4, fill="#B4BAC1")
    ic.path(_qt_shape(5.5, 8.2, 10.5, 12, 1.2), fill="#41CD52")


# --- Geany: a brass oil lamp, its lid green, a flame at the spout ------------

@icon("geany", kind="app", names=["geany", "org.geany.Geany"], title="Geany")
def geany(ic):
    tile(ic, "#34417A", "#141A3C")
    shadow(ic, 120, 212, 96, 11)
    with ic.g(transform="translate(-10 0)"):
        _geany_lamp(ic)


def _geany_lamp(ic):
    # the smoke, curling up from the flame
    ic.path("M222 92 C214 78 232 70 222 56 C214 44 226 36 220 26", fill="none", stroke="#C9C2F0",
            stroke_opacity=0.35, stroke_width=4, stroke_linecap="round")
    # the handle
    ic.path("M62 128 C26 120 22 176 66 168", fill="none", stroke="#5A3E14", stroke_width=11, stroke_linecap="round")
    ic.path("M62 128 C26 120 22 176 66 168", fill="none", stroke=brass(ic), stroke_width=8, stroke_linecap="round")
    ic.path("M54 126 C34 126 30 148 36 158", fill="none", stroke="#FFF1C4", stroke_opacity=0.6, stroke_width=2,
            stroke_linecap="round")
    # the foot
    ic.ellipse(126, 202, 36, 8, fill="#5A3E14")
    ic.path("M106 180 H146 L158 200 H94z", fill=brass(ic, 0, 0, 1, 0))
    ic.ellipse(126, 200, 34, 6.5, fill=brass(ic))
    # the body and the spout
    body = ("M54 150 C54 120 92 106 126 106 C162 106 190 118 200 136 L230 112 C234 108 241 112 237 117"
            " L206 158 C196 174 166 186 126 186 C88 186 54 174 54 150Z")
    ic.path(body, fill="#4A3210", transform="translate(2 3)", opacity=0.5)
    ic.path(body, fill=ic.lin([(0, "#FBE6AE"), (0.35, "#D9A64E"), (0.75, "#9C6C24"), (1, "#6E4A14")], 0, 0, 0.5, 1))
    ic.path("M66 136 C80 116 108 112 132 112", fill="none", stroke="#FFF6D8", stroke_width=3, stroke_linecap="round",
            opacity=0.8)
    ic.path("M204 136 L228 117", fill="none", stroke="#FFF6D8", stroke_width=1.6, opacity=0.7)
    # the engraved band and the name
    ic.path("M58 156 C80 168 170 170 200 152", fill="none", stroke="#6E4A14", stroke_width=1.6, opacity=0.7)
    ic.path("M58 160 C80 172 170 174 200 156", fill="none", stroke="#FFF1C4", stroke_width=1, opacity=0.35)
    ic.text("geany", 128, 150, 16, font="sans-semibold", anchor="middle", spacing=0.5, fill="#6E4A14", opacity=0.75)
    # the collar and the green lid
    ic.ellipse(126, 108, 30, 7, fill="#6E4A14")
    ic.rect(98, 98, 56, 10, fill=brass(ic, 0, 0, 1, 0))
    ic.ellipse(126, 98, 28, 6, fill="#F6DDA0")
    lid = ic.lin([(0, "#9BE38A"), (0.45, "#4CAF3E"), (1, "#1F6A1C")], 0, 0, 0.6, 1)
    ic.path("M100 98 C100 76 112 64 126 64 C140 64 152 76 152 98 C140 104 112 104 100 98Z", fill=lid)
    ic.path("M108 88 C110 76 116 70 124 68", fill="none", stroke="#fff", stroke_opacity=0.6, stroke_width=2.4,
            stroke_linecap="round")
    ic.circle(126, 58, 8, fill=lid)
    ic.circle(123.5, 55.5, 2.6, fill="#fff", opacity=0.6)
    ic.rect(122, 62, 8, 4, fill=brass(ic))
    # the flame at the spout
    ic.path("M234 112 C226 104 228 92 236 82 C238 92 246 100 240 110 C238 113 236 113 234 112Z", fill="#F59A3C")
    ic.path("M235 110 C231 104 233 98 236 93 C238 99 241 104 238 109Z", fill="#FFE68A")


@small("geany")
def geany16(ic):
    tile(ic, "#34417A", "#141A3C")
    ic.path("M3.2 8.4 C1.6 8.2 1.6 11 3.6 10.6", fill="none", stroke="#C99645", stroke_width=1)
    ic.path("M3 9.6 C3 7.8 5.6 7 8 7 C10 7 11.6 7.6 12.3 8.6 L14.2 7 L12.8 10.2 C12 11.6 10 12.4 8 12.4"
            " C5 12.4 3 11.4 3 9.6Z", fill="#D9A64E")
    ic.rect(6.2, 12.2, 3.6, 1.4, fill="#9C6C24")
    ic.path("M6.3 7 C6.3 5 7.1 4.2 8 4.2 C8.9 4.2 9.7 5 9.7 7Z", fill="#4CAF3E")
    ic.path("M14.2 6.6 C13.6 6 13.8 5 14.4 4.2 C14.8 5 15.2 5.8 14.6 6.6Z", fill="#F59A3C")


# --- Kate: a blue woodpecker at work on a log -------------------------------

@icon("kate", kind="app", names=["kate", "kate2", "org.kde.kate"], title="Kate")
def kate(ic):
    tile(ic, "#2A5592", "#0F2650")
    shadow(ic, 128, 214, 84, 11)
    with ic.g(transform="translate(12 0)"):
        # the log, standing
        ic.rect(48, 34, 54, 176, fill=ic.lin([(0, "#9C7A55"), (0.5, "#7A5634"), (1, "#4A3018")], 0, 0, 1, 0))
        for x, y0, y1 in ((56, 60, 120), (66, 90, 190), (78, 50, 100), (88, 120, 200), (60, 150, 204), (94, 44, 76)):
            ic.line(x, y0, x, y1, stroke="#2E1C0C", stroke_opacity=0.45, stroke_width=1.6, stroke_linecap="round")
            ic.line(x + 1.5, y0, x + 1.5, y1, stroke="#E0C49C", stroke_opacity=0.2, stroke_width=1)
        ic.ellipse(75, 210, 27, 6, fill="#3A2412")
        ic.ellipse(75, 34, 27, 8, fill=ic.lin([(0, "#F2DDB4"), (1, "#C9A46E")], 0, 0, 1, 1))
        for r in (18, 12, 6):
            ic.ellipse(76, 34.5, r, r * 0.3, fill="none", stroke="#9C7A55", stroke_opacity=0.6)
        # the holes it has made, and chips flying
        for y in (82, 118):
            ic.ellipse(101, y, 3.5, 5, fill="#1E1208")
        for x, y, r in ((106, 66, 20), (112, 60, -30), (104, 56, 50)):
            ic.rect(x, y, 5, 2.4, rx=1, fill="#E0C49C", transform=f"rotate({r} {x} {y})")
        # the bird: tail, body, wing, head, beak
        ic.path("M128 168 L140 174 L126 212 L116 210z", fill="#0B2C58")
        ic.ellipse(140, 136, 30, 52, fill=ic.lin([(0, "#5BB8F5"), (0.5, "#1D86D6"), (1, "#0D4A8E")], 0, 0, 1, 1),
                   transform="rotate(16 140 136)")
        ic.ellipse(126, 140, 14, 36, fill=ic.lin([(0, "#D8EEFC"), (1, "#8CC4EC")]), transform="rotate(16 126 140)")
        wing = "M150 104 C174 112 178 150 160 186 C152 172 146 142 150 104Z"
        ic.path(wing, fill=ic.lin([(0, "#1A6FB5"), (1, "#0B2C58")]))
        for x, y in ((160, 124), (164, 140), (162, 156), (156, 170), (154, 132), (156, 148)):
            ic.ellipse(x, y, 2.6, 1.8, fill="#E8F4FC", opacity=0.85)
        # facets on the head, as the mark has
        ic.circle(140, 80, 28, fill=ic.lin([(0, "#7CCBFA"), (1, "#1D86D6")], 0, 0, 1, 1))
        ic.path("M140 52 A28 28 0 0 1 168 80 L140 80z", fill="#0E5BA6", opacity=0.55)
        ic.path("M140 80 L168 80 A28 28 0 0 1 150 106z", fill="#0B2C58", opacity=0.45)
        ic.path("M112 80 A28 28 0 0 1 140 52 L132 80z", fill="#fff", opacity=0.18)
        # the crest
        ic.path("M136 52 C150 44 168 46 180 58 C168 58 162 62 160 72 C156 62 146 56 136 52Z", fill="#0B2C58")
        # the beak, into the log
        ic.path("M116 71 L88 80 L116 90z", fill=ic.lin([(0, "#F4F8FC"), (1, "#9AA9B8")]))
        ic.line(116, 80.6, 92, 80.4, stroke="#4A5866", stroke_width=1)
        # the eye
        ic.circle(130, 76, 7, fill="#fff")
        ic.circle(129, 76, 4.2, fill="#0A1626")
        ic.circle(127.6, 74.4, 1.4, fill="#fff")
        # the feet, gripping
        for y in (148, 166):
            ic.path(f"M120 {y} C114 {y - 2} 108 {y - 2} 104 {y - 6} M120 {y} C114 {y + 1} 108 {y + 2} 103 {y + 1}",
                    fill="none", stroke="#1E2630", stroke_width=2.6, stroke_linecap="round")


@small("kate")
def kate16(ic):
    tile(ic, "#2A5592", "#0F2650")
    ic.rect(2.5, 2, 3.4, 12.5, fill="#7A5634")
    ic.ellipse(9.6, 9.2, 2.6, 4, fill="#1D86D6", transform="rotate(16 9.6 9.2)")
    ic.path("M8.6 12 L7.6 14.4 L9.2 14.4z", fill="#0B2C58")
    ic.circle(9.2, 5.2, 2.4, fill="#3DA6EE")
    ic.path("M9 2.8 C10.4 2.2 11.8 2.6 12.4 3.6 L10.6 4.4z", fill="#0B2C58")
    ic.path("M7 4.6 L5.8 5.2 L7 5.8z", fill="#E4ECF4")
    ic.circle(8.5, 4.9, 0.6, fill="#0A1626")


# --- Text Editor: a sheet of notes and a yellow pencil ----------------------

def _pencil(ic, x, y, deg, length=150):
    """A hexagonal pencil lying with its point at (x, y), turned deg."""
    with ic.g(transform=f"translate({x} {y}) rotate({deg})"):
        ic.rect(6, -4, length, 16, rx=3, fill="#000", opacity=0.2)
        ic.path("M0 0 L24 -8 V8z", fill=ic.lin([(0, "#F3D6A6"), (1, "#C9965A")]))
        ic.path("M0 0 L8 -2.7 V2.7z", fill="#2A2C30")
        e = length - 30
        ic.rect(24, -8, e - 24, 5.4, fill="#FFD84D")
        ic.rect(24, -2.6, e - 24, 5.4, fill="#F2B518")
        ic.rect(24, 2.8, e - 24, 5.2, fill="#C98A0E")
        ic.path("M24 -8 L18 -6 V6 L24 8z", fill="#E8C688")
        for k in (0, 1, 2):
            ic.rect(24, -8 + k * 5.4, 4, 5.3, fill="#000", opacity=0.08)
        ic.text("HB", 40, 2, 5.5, font="mono-semibold", fill="#6A4A06", opacity=0.7)
        ic.rect(e, -8.6, 16, 17.2, fill=steel(ic, False))
        for k in (4, 8, 12):
            ic.line(e + k, -8.6, e + k, 8.6, stroke="#5D636B", stroke_width=1)
        ic.rect(e + 16, -8, 14, 16, rx=3, fill=ic.lin([(0, "#F7A5A0"), (1, "#C9665E")]))


@icon("gedit", kind="app", names=["1E64_notepad.0", "accessories-text-editor", "bottles_notepad", "deepin-editor",
                                   "edile", "gedit", "gedit-icon", "gedit-logo", "gnome-word", "io.liri.Text", "juffed",
                                   "kedit", "korg-todo", "kwrite", "leafpad", "medit", "notepad",
                                   "org.gnome.TextEditor", "org.gnome.gedit", "org.kde.kwrite", "package_editors",
                                   "preferences-composer", "text-editor", "wine-notepad", "wp", "xed", "xedit",
                                   "xfce-edit", "xfw"], title="Text Editor")
def gedit(ic):
    tile(ic, "#5C6D80", "#28323E")
    shadow(ic, 124, 214, 94, 12)
    with ic.g(transform="rotate(-5 124 124)"):
        sheet = "M50 34 H170 L198 62 V212 H50z"
        ic.path(sheet, fill="#000", opacity=0.3, transform="translate(3 4)")
        ic.path(sheet, fill=paper(ic, "white"))
        for y in range(78, 206, 12):
            ic.line(50, y + 2, 198, y + 2, stroke="#9CC3DE", stroke_opacity=0.55, stroke_width=1)
        ic.line(68, 34, 68, 212, stroke="#E58A8A", stroke_opacity=0.6, stroke_width=1.2)
        ic.text("notes.txt", 74, 64, 13, font="sans-semibold", fill="#2B3440")
        lines = ["Desk, Friday", "- ink for the pen", "- post the letters", "- fix the lamp",
                 "Read: chapter 4", "Call Mum at 6"]
        for i, s in enumerate(lines):
            ic.text(s, 74, 78 + i * 12, 8, font="mono", fill="#4E4C47")
        ic.rect(140, 141, 2, 10, fill="#3584E4")
        # the corner folded
        ic.path("M170 34 V62 H198z", fill=ic.lin([(0, "#F1EEE8"), (1, "#C9C4BA")], 0, 0, 1, 1))
        ic.path("M170 62 H198", stroke="#000", stroke_opacity=0.1)
        ic.line(51, 35, 169, 35, stroke="#fff", stroke_width=1.5)
    _pencil(ic, 134, 200, -50, 148)


@small("gedit")
def gedit16(ic):
    tile(ic, "#5C6D80", "#28323E")
    ic.path("M3 2 H10.5 L13 4.5 V14 H3z", fill="#FFFFFF")
    ic.path("M10.5 2 V4.5 H13z", fill="#C9C4BA")
    for y in (5, 7, 9):
        ic.rect(4.5, y, 5, 0.8, fill="#7D8590")
    ic.path("M7.6 13.6 L13.6 7.6 L14.8 8.8 L8.8 14.8 L7.2 15z", fill="#F2B518")
    ic.path("M7.6 13.6 L8.8 14.8 L7.2 15z", fill="#2A2C30")


# --- Meld: two pages side by side on a board, their differences banded ------

@icon("meld", kind="app", names=["meld", "org.gnome.Meld", "org.gnome.meld"], title="Meld")
def meld(ic):
    tile(ic, "#4E5A6A", "#1E2530")
    shadow(ic, 128, 216, 104, 12)
    # the board
    ic.rect(22, 42, 212, 170, rx=10, fill="#1A1E24", transform="translate(2 3)")
    ic.rect(22, 42, 212, 170, rx=10, fill=wood(ic, "#C8935C", "#7A4A22"))
    ic.rect(22.75, 42.75, 210.5, 168.5, rx=9.25, fill="none", stroke="#fff", stroke_opacity=0.2, stroke_width=1.5)
    left, right = (32, 120), (136, 224)
    for x0, x1 in (left, right):
        ic.rect(x0 + 2, 56, x1 - x0, 148, rx=2, fill="#000", opacity=0.25)
        ic.rect(x0, 54, x1 - x0, 148, rx=2, fill=paper(ic, "white"))
    # the bands: changed, added, removed; joined across the gap
    bands = [((70, 88), (78, 96), "#3584E4"), ((108, 132), (116, 148), "#4CB860"), ((158, 170), (184, 184.5), "#E0533F")]
    for (l0, l1), (r0, r1), c in bands:
        ic.rect(left[0], l0, left[1] - left[0], l1 - l0, fill=c, opacity=0.28)
        ic.rect(right[0], r0, right[1] - right[0], r1 - r0, fill=c, opacity=0.28)
        ic.path(f"M120 {l0} C128 {l0} 128 {r0} 136 {r0} V{r1} C128 {r1} 128 {l1} 120 {l1}z", fill=c, opacity=0.75)
        ic.rect(left[0], l0, 3, l1 - l0, fill=c)
        ic.rect(right[1] - 3, r0, 3, r1 - r0, fill=c)
    # the text on each, line by line
    lw = [(52, 0), (40, 8), (62, 8), (34, 0), (48, 8), (58, 8), (30, 8), (44, 0), (56, 8), (38, 8), (50, 0)]
    for side, (x0, x1) in enumerate((left, right)):
        for i, (w, ind) in enumerate(lw):
            y = 74 + i * 10.6
            if side == 1 and i == 9:
                continue
            ww = w + (10 if side == 1 and i in (1, 4, 5) else 0)
            ic.rect(x0 + 8 + ind, y, min(ww, x1 - x0 - 16 - ind), 3.4, rx=1.7, fill="#5A6470", opacity=0.75)
    # the file names
    ic.text("old.go", 40, 66, 7, font="mono-semibold", fill="#2B3440")
    ic.text("new.go", 144, 66, 7, font="mono-semibold", fill="#2B3440")
    # the clips
    for cx in (76, 180):
        ic.path(f"M{cx - 10} 36 a10 10 0 0 1 20 0", fill="none", stroke=steel(ic), stroke_width=3)
        ic.rect(cx - 18, 42, 36, 18, rx=3, fill="#141619")
        ic.rect(cx - 16, 43, 32, 3, rx=1.5, fill="#fff", opacity=0.22)
    # meld's three-colour stripe, painted on the board's foot
    for i, c in enumerate(("#3584E4", "#4CB860", "#E0533F")):
        ic.rect(98 + i * 21, 204, 19, 4, rx=2, fill=c)


@small("meld")
def meld16(ic):
    tile(ic, "#4E5A6A", "#1E2530")
    ic.rect(1.5, 3, 5.6, 10.5, fill="#FFFFFF")
    ic.rect(8.9, 3, 5.6, 10.5, fill="#FFFFFF")
    ic.rect(1.5, 4.6, 5.6, 1.8, fill="#3584E4", opacity=0.6)
    ic.path("M7.1 4.6 C8 4.6 8 5.6 8.9 5.6 V7.4 C8 7.4 8 6.4 7.1 6.4z", fill="#3584E4")
    ic.rect(8.9, 5.6, 5.6, 1.8, fill="#3584E4", opacity=0.6)
    ic.rect(1.5, 8.6, 5.6, 2.2, fill="#4CB860", opacity=0.6)
    ic.path("M7.1 8.6 C8 8.6 8 9.4 8.9 9.4 V11.6 C8 11.6 8 10.8 7.1 10.8z", fill="#4CB860")
    ic.rect(8.9, 9.4, 5.6, 2.2, fill="#4CB860", opacity=0.6)


# --- GitKraken: a teal ceramic kraken, its arms curling ---------------------

@icon("gitkraken", kind="app", names=["GitKraken", "app", "com.axosoft.GitKraken", "gitkraken"], title="GitKraken")
def gitkraken(ic):
    tile(ic, "#21414F", "#0A1A22")
    shadow(ic, 128, 214, 98, 12)
    teal = ic.lin([(0, "#5FE3D2"), (0.5, "#19A898"), (1, "#0A5E58")], 30, 40, 220, 220, units="userSpaceOnUse")
    under = "#0B4F49"
    arms = [
        [(96, 140), (80, 168), (40, 160), (40, 186), (40, 204), (66, 206), (66, 192)],
        [(110, 146), (102, 176), (76, 200), (92, 208), (102, 212), (110, 202), (104, 196)],
        [(124, 148), (124, 180), (128, 200), (130, 208), (132, 214), (142, 212), (138, 204)],
        [(140, 146), (150, 176), (168, 196), (176, 206), (184, 214), (190, 204), (182, 198)],
        [(158, 140), (178, 168), (218, 162), (218, 188), (218, 206), (192, 206), (192, 192)],
    ]
    for pts in arms:
        ic.path(_taper(pts, 26, 7), fill=under, transform="translate(1.5 3)")
        ic.path(_taper(pts, 26, 7), fill=teal)
    # suckers along the outer arms
    for x, y in ((52, 170), (46, 182), (50, 196), (204, 170), (210, 182), (206, 196), (96, 192), (162, 192)):
        ic.circle(x, y, 2.6, fill="#C9F5EE", opacity=0.8)
        ic.circle(x + 0.5, y + 0.6, 1.2, fill=under)
    # the mantle
    mantle = "M68 142 C58 92 82 38 128 38 C174 38 198 92 188 142 C168 158 88 158 68 142Z"
    ic.path(mantle, fill=under, transform="translate(2 3)")
    ic.path(mantle, fill=teal)
    ic.path("M80 104 C80 72 98 50 120 46", fill="none", stroke="#fff", stroke_opacity=0.55, stroke_width=3,
            stroke_linecap="round")
    for x, y, r in ((150, 62, 5), (164, 76, 3.5), (100, 70, 3), (170, 98, 4)):
        ic.circle(x, y, r, fill="#0E7A70", opacity=0.6)
    # the eyes
    for ex in (106, 150):
        ic.ellipse(ex + 1, 114, 16, 18, fill=under)
        ic.ellipse(ex, 112, 16, 18, fill=ic.rad([(0, "#FFFFFF"), (1, "#D6ECE8")], cx=0.4, cy=0.35, r=0.7))
        ic.circle(ex + 3, 116, 8.5, fill="#0B1E26")
        ic.circle(ex, 112, 3, fill="#fff")
    ic.path("M112 140 C120 146 136 146 144 140", fill="none", stroke=under, stroke_width=3, stroke_linecap="round")


@small("gitkraken")
def gitkraken16(ic):
    tile(ic, "#21414F", "#0A1A22")
    for d in ("M5 9.5 C4 11.5 2 11 2.4 13", "M7 10 C6.6 12 5.8 13 6.6 14", "M9 10 C9.4 12 10.2 13 9.4 14",
              "M11 9.5 C12 11.5 14 11 13.6 13"):
        ic.path(d, fill="none", stroke="#19A898", stroke_width=1.6, stroke_linecap="round")
    ic.path("M3.8 10 C3 6 5 2 8 2 C11 2 13 6 12.2 10 C10.6 11 5.4 11 3.8 10Z", fill="#2EC0AE")
    ic.circle(6.4, 7, 1.4, fill="#fff")
    ic.circle(9.6, 7, 1.4, fill="#fff")
    ic.circle(6.7, 7.3, 0.7, fill="#0B1E26")
    ic.circle(9.9, 7.3, 0.7, fill="#0B1E26")


# --- Bruno: the dog of its mark, a plush with a collar and a brass tag -------

@icon("bruno", kind="app", names=["bruno", "com.usebruno.Bruno"], title="Bruno")
def bruno(ic):
    tile(ic, "#34465C", "#141D2A")
    shadow(ic, 128, 216, 76, 10)
    fur = ic.lin([(0, "#FFD27A"), (0.5, "#F2A93B"), (1, "#B86E16")], 40, 40, 210, 210, units="userSpaceOnUse")
    ear = ic.lin([(0, "#8A5428"), (1, "#3E220C")], 0, 0, 1, 1)
    # the chest
    ic.path("M74 196 C70 168 92 150 128 150 C164 150 186 168 182 196 C178 212 156 216 128 216 C100 216 78 212 74 196Z", fill=fur)
    ic.path("M102 210 C100 190 112 176 128 176 C144 176 156 190 154 210 C146 214 110 214 102 210Z", fill="#FFF0D2", opacity=0.9)
    # the ears, hanging behind
    ic.path("M76 62 C46 60 36 100 44 140 C48 156 66 158 72 142 C78 120 86 92 92 72Z", fill=ear)
    ic.path("M180 62 C210 60 220 100 212 140 C208 156 190 158 184 142 C178 120 170 92 164 72Z", fill=ear)
    # the head
    ic.ellipse(128, 104, 62, 58, fill=fur)
    ic.path("M76 90 C80 64 100 50 124 48", fill="none", stroke="#FFF1C9", stroke_width=3, stroke_linecap="round",
            opacity=0.8)
    ic.path("M128 48 C120 60 120 72 128 84 C136 72 136 60 128 48Z", fill="#FFF0D2", opacity=0.6)
    # the collar and its tag
    ic.path("M78 160 C100 176 156 176 178 160 L182 172 C158 190 98 190 74 172Z", fill=ic.lin([(0, "#E0533F"), (1, "#8E2618")]))
    ic.path("M78 162 C100 178 156 178 178 162", fill="none", stroke="#FFB3A6", stroke_opacity=0.5, stroke_width=1.2)
    ic.circle(128, 184, 2.6, fill="#C3C8CE")
    ic.circle(128, 200, 15, fill="#5A3E14")
    ic.circle(127, 198.5, 15, fill=brass(ic))
    ic.circle(127, 198.5, 12, fill="none", stroke="#7E5A20", stroke_opacity=0.6)
    ic.text("bruno", 127, 202, 8, font="sans-bold", anchor="middle", fill="#5A3E14")
    # the muzzle, nose, mouth, tongue
    ic.ellipse(128, 132, 34, 25, fill=ic.lin([(0, "#FFF6E2"), (1, "#E6C89A")]))
    ic.path("M110 141 C118 150 138 150 146 141", fill="none", stroke="#3E220C", stroke_width=2.4, stroke_linecap="round")
    ic.line(128, 128, 128, 145, stroke="#3E220C", stroke_width=2.4, stroke_linecap="round")
    ic.path("M122 146 C122 158 134 158 134 146Z", fill="#E5707A")
    ic.path("M128 120 C116 120 112 112 116 108 C120 104 136 104 140 108 C144 112 140 120 128 120Z", fill="#1E1410")
    ic.ellipse(122, 109.5, 5, 2, fill="#fff", opacity=0.5)
    # the eyes and brows
    for x in (102, 154):
        ic.circle(x, 94, 8, fill="#1E1410")
        ic.circle(x - 2.5, 91, 2.8, fill="#fff")
        ic.path(f"M{x - 9} 80 C{x - 4} 76 {x + 4} 76 {x + 9} 80", fill="none", stroke="#8A5428", stroke_width=3,
                stroke_linecap="round")


@small("bruno")
def bruno16(ic):
    tile(ic, "#34465C", "#141D2A")
    ic.path("M4.4 3.6 C2.4 3.6 1.8 6.6 2.4 9 C2.8 10 4 10 4.4 9Z", fill="#6A3E1C")
    ic.path("M11.6 3.6 C13.6 3.6 14.2 6.6 13.6 9 C13.2 10 12 10 11.6 9Z", fill="#6A3E1C")
    ic.ellipse(8, 7.4, 4.4, 4.4, fill="#F2A93B")
    ic.ellipse(8, 9.6, 2.4, 1.8, fill="#FFF0D2")
    ic.ellipse(8, 8.7, 1.1, 0.7, fill="#1E1410")
    ic.circle(6.2, 6.6, 0.7, fill="#1E1410")
    ic.circle(9.8, 6.6, 0.7, fill="#1E1410")
    ic.rect(4.4, 11.6, 7.2, 1.2, rx=0.6, fill="#E0533F")
    ic.circle(8, 13.6, 1.2, fill="#D2A458")


# --- Beekeeper Studio: a straw skep on its stand, bees about ----------------

def _bee(ic, x, y, k=1.0, deg=0):
    with ic.g(transform=f"translate({x} {y}) rotate({deg}) scale({k})"):
        ic.ellipse(-2, -6, 6, 4, fill="#fff", opacity=0.75, transform="rotate(-20 -2 -6)")
        ic.ellipse(4, -6, 5, 3.4, fill="#fff", opacity=0.6, transform="rotate(20 4 -6)")
        ic.ellipse(0, 0, 9, 6, fill="#FAD83B")
        for dx in (-3, 2):
            ic.rect(dx, -5.6, 2.6, 11.2, fill="#1E1A14")
        ic.circle(8, -0.5, 3.6, fill="#1E1A14")
        ic.ellipse(-2, -2.6, 4, 1.4, fill="#fff", opacity=0.5)


@icon("beekeeper-studio", kind="app", names=["appimagekit-beekeeper-studio", "beekeeper-studio",
                                              "io.beekeeperstudio.Studio"], title="Beekeeper Studio")
def beekeeper(ic):
    tile(ic, "#3A3F4A", "#15181E")
    shadow(ic, 128, 214, 98, 12)
    # the stand
    ic.rect(30, 190, 196, 16, rx=3, fill=wood(ic, "#9C6A3C", "#4E2C12"))
    ic.line(32, 191, 224, 191, stroke="#E0B886", stroke_width=1.5, opacity=0.6)
    for x in (44, 202):
        ic.rect(x, 206, 10, 10, fill="#3A2210")
    # the skep: coils of straw, narrower toward the top
    rows = 9
    for i in range(rows):
        y = 172 - i * 16
        t = (190 - (y + 9)) / 150
        w = 86 * math.sqrt(max(1 - t * t, 0)) if i < rows - 1 else 26
        w = max(w, 24)
        straw = ic.lin([(0, "#FBE7A0"), (0.45, "#E8B94A"), (1, "#9C6A1C")])
        ic.rect(128 - w, y + 2, 2 * w, 20, rx=10, fill="#6E4A14", opacity=0.6)
        ic.rect(128 - w, y, 2 * w, 20, rx=10, fill=straw)
        # the binding: little stitches across each coil
        for k in range(-3, 4):
            sx = 128 + k * w / 4.2
            ic.line(sx - 2, y + 4, sx + 2, y + 16, stroke="#7E5414", stroke_width=1.6, opacity=0.5)
        ic.path(f"M{128 - w + 8} {y + 3} H{128 + w - 8}", stroke="#FFF6D0", stroke_width=1.4, opacity=0.6)
    ic.ellipse(128, 40, 16, 8, fill=ic.lin([(0, "#FBE7A0"), (1, "#C98A2A")]))
    # the light on its left
    ic.path("M60 176 C46 140 56 92 96 58", fill="none", stroke="#fff", stroke_opacity=0.25, stroke_width=5,
            stroke_linecap="round")
    # the doorway
    ic.path("M110 192 V182 a18 14 0 0 1 36 0 V192z", fill="#1E1208")
    ic.path("M112 182 a16 12 0 0 1 32 0", fill="none", stroke="#6E4A14", stroke_width=2)
    # a hexagonal plate on the stand
    hexa = [polar(128, 140, 15, a) for a in range(30, 390, 60)]
    ic.path(_pts([(x + 1, y + 2) for x, y in hexa]), fill="#4A3210", opacity=0.6)
    ic.path(_pts(hexa), fill=ic.lin([(0, "#2E3138"), (1, "#121418")]))
    ic.path(_pts([polar(128, 140, 11, a) for a in range(30, 390, 60)]), fill="none", stroke="#FAD83B",
            stroke_width=2.2)
    ic.circle(128, 140, 3.2, fill="#FAD83B")
    # the bees
    _bee(ic, 200, 70, 1.3, -14)
    _bee(ic, 56, 52, 1.0, 12)
    _bee(ic, 212, 140, 0.9, 8)


@small("beekeeper-studio")
def beekeeper16(ic):
    tile(ic, "#3A3F4A", "#15181E")
    ic.rect(2, 12.6, 12, 1.6, rx=0.4, fill="#7A4A22")
    ic.path("M3 12.6 C2.6 6 5 2.6 8 2.6 C11 2.6 13.4 6 13 12.6Z", fill="#E8B94A")
    for y in (5, 7.4, 9.8):
        ic.line(3, y, 13, y, stroke="#9C6A1C", stroke_width=0.6)
    ic.path("M6.8 12.6 V11.6 a1.2 1.2 0 0 1 2.4 0 V12.6z", fill="#1E1208")


# --- pgAdmin: the elephant, a glazed bust on a plinth -----------------------

@icon("pgadmin4", kind="app", names=["pgAdmin4", "pgadmin", "pgadmin3", "pgadmin4"], title="pgAdmin")
def pgadmin(ic):
    tile(ic, "#2C4B6C", "#10223A")
    shadow(ic, 128, 214, 86, 11)
    # the plinth
    ic.rect(60, 184, 136, 28, rx=3, fill=ic.lin([(0, "#3A3F46"), (1, "#16181C")]))
    ic.rect(54, 176, 148, 12, rx=3, fill=ic.lin([(0, "#6A7078"), (1, "#3A3F46")]))
    ic.line(56, 177, 200, 177, stroke="#fff", stroke_opacity=0.35, stroke_width=1.2)
    ic.rect(98, 192, 60, 14, rx=1.5, fill=brass(ic))
    ic.text("pgAdmin", 128, 202.5, 9, font="sans-semibold", anchor="middle", fill="#4A3210")
    glaze = ic.lin([(0, "#7FB2E2"), (0.5, "#336791"), (1, "#1A3D60")], 40, 30, 200, 200, units="userSpaceOnUse")
    trim = dict(fill="none", stroke="#F2F6FA", stroke_width=4)
    outline = dict(fill="none", stroke="#0C1E32", stroke_width=8)
    # the ears
    ears = ["M86 70 C52 52 26 80 34 118 C40 146 66 150 84 134 C92 120 94 92 86 70Z",
            "M170 70 C204 52 230 80 222 118 C216 146 190 150 172 134 C164 120 162 92 170 70Z"]
    for d in ears:
        ic.path(d, **outline)
        ic.path(d, fill=glaze)
        ic.path(d, **trim)
    ic.path("M80 80 C58 70 44 90 48 114 C52 132 66 136 78 126Z", fill="#0C1E32", opacity=0.3)
    ic.path("M176 80 C198 70 212 90 208 114 C204 132 190 136 178 126Z", fill="#0C1E32", opacity=0.35)
    # the trunk, curling to its right
    trunk = [(128, 118), (126, 146), (124, 168), (146, 176), (164, 182), (172, 164), (160, 160)]
    ic.path(_taper(trunk, 34, 13), **outline)
    ic.path(_taper(trunk, 34, 13), fill=glaze)
    ic.path(_taper(trunk, 34, 13), **trim)
    for y in (140, 150, 160):
        ic.path(f"M{116 + (y - 140) * 0.1} {y} q10 4 20 0", fill="none", stroke="#0C1E32", stroke_opacity=0.35,
                stroke_width=1.4)
    # the head
    head = "M128 42 C160 42 178 66 176 98 C174 124 156 136 128 136 C100 136 82 124 80 98 C78 66 96 42 128 42Z"
    ic.path(head, **outline)
    ic.path(head, fill=glaze)
    ic.path(head, **trim)
    ic.path(_taper(trunk[:4], 34, 26), fill=glaze)
    ic.path("M92 84 C94 64 106 52 122 50", fill="none", stroke="#fff", stroke_opacity=0.55, stroke_width=3,
            stroke_linecap="round")
    # the tusks
    ic.path("M108 128 C104 142 108 152 116 156 C112 146 112 138 114 130Z", fill="#FBF8F0", stroke="#0C1E32",
            stroke_width=1.5)
    ic.path("M148 128 C152 142 148 152 140 156 C144 146 144 138 142 130Z", fill="#FBF8F0", stroke="#0C1E32",
            stroke_width=1.5)
    # the eyes
    for x in (106, 150):
        ic.ellipse(x, 96, 6.5, 8, fill="#F2F6FA")
        ic.circle(x + 1, 97, 4, fill="#0C1E32")
        ic.circle(x - 0.5, 95, 1.4, fill="#fff")


@small("pgadmin4")
def pgadmin16(ic):
    tile(ic, "#2C4B6C", "#10223A")
    ic.ellipse(3.6, 7, 2.6, 3.4, fill="#336791", stroke="#F2F6FA", stroke_width=0.6)
    ic.ellipse(12.4, 7, 2.6, 3.4, fill="#336791", stroke="#F2F6FA", stroke_width=0.6)
    ic.path("M8 9 V12.4 C8 13.6 9.6 13.6 10.2 12.6", fill="none", stroke="#F2F6FA", stroke_width=2.6,
            stroke_linecap="round")
    ic.path("M8 9 V12.4 C8 13.6 9.6 13.6 10.2 12.6", fill="none", stroke="#336791", stroke_width=1.6,
            stroke_linecap="round")
    ic.circle(8, 6.6, 3.8, fill="#336791", stroke="#F2F6FA", stroke_width=0.6)
    ic.circle(6.6, 6.4, 0.6, fill="#0C1E32")
    ic.circle(9.4, 6.4, 0.6, fill="#0C1E32")


# --- MongoDB Compass: a brass pocket compass, its needle the green leaf ------

@icon("mongodb-compass", kind="app", names=["com.mongodb.Compass", "mongodb-compass", "mongodb-compass-community"],
      title="MongoDB Compass")
def compass(ic):
    tile(ic, "#14473D", "#03201C")
    cx, cy = 128, 132
    shadow(ic, 128, 220, 86, 10)
    # the bow
    ic.circle(cx, 30, 12, fill="none", stroke="#5A3E14", stroke_width=7, transform="translate(1 2)")
    ic.circle(cx, 30, 12, fill="none", stroke=brass(ic), stroke_width=6)
    ic.rect(cx - 9, 38, 18, 14, rx=3, fill=brass(ic, 0, 0, 1, 0))
    ic.rect(cx - 12, 46, 24, 6, rx=2, fill=brass(ic))
    # the case
    ic.circle(cx + 2, cy + 3, 88, fill="#2A1C06", opacity=0.6)
    ic.circle(cx, cy, 88, fill=brass(ic))
    ic.circle(cx, cy, 80, fill=brass(ic, 1, 1, 0, 0))
    ic.circle(cx, cy, 74, fill=ic.rad([(0, "#FFFDF7"), (1, "#E6DCC6")], cx=0.45, cy=0.4, r=0.65))
    ic.circle(cx, cy, 74, fill="none", stroke="#000", stroke_opacity=0.2, stroke_width=2)
    ink = "#2A2C30"
    for k in range(72):
        deg = k * 5
        major = k % 18 == 0
        mid = k % 9 == 0
        x1, y1 = polar(cx, cy, 71, deg)
        x2, y2 = polar(cx, cy, 71 - (9 if major else 6 if mid else 3.5), deg)
        ic.line(x1, y1, x2, y2, stroke=ink, stroke_width=1.8 if major else 1.1 if mid else 0.7)
    # the rose, faint, and the letters
    for deg in (45, 135, 225, 315):
        p1 = polar(cx, cy, 46, deg)
        q1, q2 = polar(cx, cy, 6, deg - 90), polar(cx, cy, 6, deg + 90)
        ic.poly([p1, q1, (cx, cy), q2], fill="#C9BFA9", opacity=0.6)
    for n, deg in (("N", 0), ("E", 90), ("S", 180), ("W", 270)):
        x, y = polar(cx, cy, 55, deg)
        ic.text(n, x, y + 5.5, 15, font="sans-semibold", anchor="middle", fill="#C8372D" if n == "N" else ink)
    ic.text("COMPASS", cx + 34, cy + 36, 5.5, font="mono-semibold", anchor="middle", spacing=1, fill="#8C887F",
            transform=f"rotate(-45 {cx + 34} {cy + 34})")
    # the needle: the leaf, pointing north
    leaf = (f"M{cx + 1} {cy - 46} C{cx + 20} {cy - 26} {cx + 18} {cy + 6} {cx + 3} {cy + 28}"
            f" L{cx} {cy + 44} L{cx - 3} {cy + 28} C{cx - 16} {cy + 8} {cx - 20} {cy - 22} {cx + 1} {cy - 46}Z")
    ic.path(leaf, fill="#000", opacity=0.22, transform="translate(3 4)")
    ic.path(leaf, fill=ic.lin([(0, "#6CF59E"), (0.45, "#00C25A"), (1, "#00684A")], 0, 0, 1, 1))
    ic.path(f"M{cx + 1} {cy - 44} C{cx - 16} {cy - 22} {cx - 14} {cy + 6} {cx - 2} {cy + 26} L{cx} {cy + 40}V{cy - 44}z",
            fill="#fff", opacity=0.16)
    ic.line(cx + 0.5, cy - 38, cx, cy + 40, stroke="#C9FADB", stroke_width=1.6, opacity=0.8)
    ic.circle(cx, cy, 7, fill=brass(ic))
    ic.circle(cx, cy, 2.2, fill="#3A2A10")
    # the glass
    ic.circle(cx, cy, 74, fill=glare(ic, 0.9))
    ic.path(f"M{cx - 64} {cy - 24}a68 68 0 0 1 80-46 76 76 0 0 0-80 46z", fill="#fff", opacity=0.5)


@small("mongodb-compass")
def compass16(ic):
    tile(ic, "#14473D", "#03201C")
    ic.circle(8, 1.8, 1, fill="none", stroke="#C99645", stroke_width=0.7)
    ic.circle(8, 8.6, 6.2, fill="#C99645")
    ic.circle(8, 8.6, 5.1, fill="#FBF7EC")
    ic.path("M8 3.8 C9.8 5.6 9.8 9 8.3 11.4 L8 13 L7.7 11.4 C6.2 9 6.2 5.6 8 3.8Z", fill="#00A84F")


# --- Podman Desktop: a seal balancing a purple container on its nose --------

@icon("podman-desktop", kind="app", names=["io.podman_desktop.PodmanDesktop", "podman-desktop"],
      title="Podman Desktop")
def podman(ic):
    tile(ic, "#5A3A88", "#22103E")
    shadow(ic, 120, 214, 92, 11)
    coat = ic.lin([(0, "#D2C6EA"), (0.45, "#8E7CB4"), (1, "#3E2E62")], 50, 60, 200, 210, units="userSpaceOnUse")
    # the floe it sits on
    ic.ellipse(124, 204, 94, 14, fill="#6E5C9C")
    ic.ellipse(124, 200, 94, 13, fill=ic.lin([(0, "#FFFFFF"), (1, "#C9C0E6")], 0, 0, 1, 1))
    ic.path("M44 198 C80 194 120 194 150 196", fill="none", stroke="#fff", stroke_width=1.5, opacity=0.8)
    # the tail flippers, then the body sitting up
    ic.path("M64 200 C44 206 30 198 32 186 C42 192 56 192 68 188z", fill="#3E2E62")
    body = "M58 202 C40 168 66 126 120 108 L170 112 C176 140 172 172 162 198 C130 208 90 208 58 202Z"
    ic.path(body, fill=coat)
    ic.path("M94 204 C90 176 108 142 138 128 C156 140 160 176 154 202 C134 207 112 207 94 204Z", fill="#E6DDF4", opacity=0.45)
    ic.path("M62 190 C56 160 76 130 110 116", fill="none", stroke="#fff", stroke_opacity=0.4, stroke_width=3,
            stroke_linecap="round")
    # the front flipper
    ic.path("M148 150 C164 158 182 176 188 194 C180 198 168 196 158 188 C150 180 144 168 148 150Z",
            fill=ic.lin([(0, "#8E7CB4"), (1, "#3E2E62")], 0, 0, 1, 1))
    ic.path("M152 156 C166 164 178 178 184 190", fill="none", stroke="#D2C6EA", stroke_opacity=0.5, stroke_width=1.5)
    # the head, nose up
    ic.ellipse(140, 104, 36, 32, fill=coat, transform="rotate(-24 140 104)")
    ic.ellipse(168, 86, 18, 14, fill=ic.lin([(0, "#E6DDF4"), (1, "#9E8CC4")]), transform="rotate(-30 168 86)")
    ic.ellipse(176, 76, 6, 4.6, fill="#1A1028", transform="rotate(-30 176 76)")
    ic.ellipse(174.4, 74.6, 2, 1.2, fill="#fff", opacity=0.6, transform="rotate(-30 174 75)")
    for x, y in ((160, 88), (164, 92), (168, 94)):
        ic.circle(x, y, 1.1, fill="#3E2E62")
    ic.path("M158 92 L134 98 M160 96 L138 106 M172 92 L196 96 M170 96 L192 104", stroke="#F4F0FA",
            stroke_opacity=0.7, stroke_width=1)
    for x, y in ((128, 100), (150, 90)):
        ic.circle(x, y, 6.5, fill="#140A22")
        ic.circle(x - 2, y - 2.4, 2.4, fill="#fff")
    # the container, balanced
    with ic.g(transform="rotate(-10 176 52)"):
        x, y, w, h = 140, 30, 74, 38
        ic.rect(x + 2, y + 3, w, h, rx=2, fill="#1A0A2A", opacity=0.5)
        ic.rect(x, y, w, h, rx=2, fill=ic.lin([(0, "#C77BE6"), (0.5, "#892CA0"), (1, "#521468")]))
        for i in range(1, int(w // 5)):
            ic.line(x + i * 5, y + 4, x + i * 5, y + h - 4, stroke="#000", stroke_opacity=0.2, stroke_width=1.2)
            ic.line(x + i * 5 + 1.3, y + 4, x + i * 5 + 1.3, y + h - 4, stroke="#fff", stroke_opacity=0.16)
        ic.rect(x + 0.6, y + 0.6, w - 1.2, h - 1.2, rx=2, fill="none", stroke="#3C0C50", stroke_width=1.6)
        ic.line(x + 2, y + 1.6, x + w - 2, y + 1.6, stroke="#fff", stroke_opacity=0.5)
        ic.rect(x + 14, y + 13, 46, 12, rx=1, fill="#3C0C50", opacity=0.55)
        ic.text("podman", x + 37, y + 22.5, 9, font="sans-bold", anchor="middle", fill="#F4E8FA")


@small("podman-desktop")
def podman16(ic):
    tile(ic, "#5A3A88", "#22103E")
    ic.path("M3 14.4 C2.2 11.6 4 8.6 7.4 7.6 L10.6 7.8 C11 10 10.8 12.4 10 14.4Z", fill="#9E8CC4")
    ic.ellipse(9.2, 7, 2.6, 2.2, fill="#B4A6D6", transform="rotate(-24 9.2 7)")
    ic.circle(11.4, 5.8, 0.7, fill="#1A1028")
    ic.circle(8.6, 6.6, 0.6, fill="#140A22")
    ic.rect(8.2, 1.4, 6, 3.2, rx=0.3, fill="#A54CC4", transform="rotate(-10 11.2 3)")
