"""The inua-objects theme, graphics: GIMP, Inkscape, Krita, Blender,
darktable, Aseprite, LibreSprite, ImageMagick (docs/feat/object-icons.md,
Part 2). Each is the app's job as an object in its brand's colours, its mark
redrawn as a painting, a print, a badge or the drawing itself."""

import math

from lib import (brass, glare, graphite, icon, paper, polar, shadow, small, steel, tile, wood)


def pixels(ic, rows, x, y, s, colours, **kw):
    """Pixel art: rows of characters, each a colour from colours (a space
    or a missing one is left empty); each pixel s px, top left at (x, y)."""
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            c = colours.get(ch)
            if c:
                ic.rect(x + i * s, y + j * s, s, s, fill=c, **kw)


def star(cx, cy, r, inner=0.38, n=4, turn=0):
    """A star's path: n points of radius r, the dips at r * inner."""
    pts = []
    for k in range(n * 2):
        pts.append(polar(cx, cy, r if k % 2 == 0 else r * inner, turn + k * 180 / n))
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"


def brush(ic, length, handle, ferrule_w=10, paint="#E2702C", tip=34):
    """A round paintbrush along the x axis, its bristles' point at 0 and
    the handle's end at length; drawn in place (wrap in a transform)."""
    h = ferrule_w / 2
    fe = tip + 26  # where the ferrule ends
    # the handle, tapering out then in to its end
    ic.path(f"M{fe} {-h + 0.5} C{fe + 40} {-h - 2.5} {length - 30} {-h + 1.5} {length - 4} -2.2 "
            f"a2.4 2.4 0 0 1 0 4.4 C{length - 30} {h - 1.5} {fe + 40} {h + 2.5} {fe} {h - 0.5}z",
            fill=handle)
    ic.path(f"M{fe + 2} {-h + 1.6} C{fe + 40} {-h - 1} {length - 30} {-h + 2.2} {length - 8} -1.2",
            fill="none", stroke="#fff", stroke_opacity=0.35, stroke_width=1.3, stroke_linecap="round")
    # the ferrule, crimped twice
    ic.path(f"M{tip + 2} {-h + 1}L{fe} {-h}V{h}L{tip + 2} {h - 1}z", fill=steel(ic, horizontal=False))
    for x in (fe - 8, fe - 5):
        ic.line(x, -h + 0.4, x, h - 0.4, stroke="#3A3F46", stroke_opacity=0.5, stroke_width=0.9)
    # the bristles, loaded with paint at the tip
    ic.path(f"M{tip + 2} {-h + 1}C{tip - 8} {-h - 1} 8 -3 0 0 C8 3 {tip - 8} {h + 1} {tip + 2} {h - 1}z",
            fill=ic.lin([(0, "#4A3420"), (1, "#2A1C10")], 1, 0, 0, 0))
    ic.path(f"M{tip * 0.55} {-h * 0.8}C{tip * 0.3} -3 6 -2 0 0 C6 2 {tip * 0.3} 3.4 {tip * 0.55} {h * 0.8}"
            f"Q{tip * 0.62} 0 {tip * 0.55} {-h * 0.8}z", fill=paint)
    ic.path(f"M{tip * 0.5} {-h * 0.6}Q{tip * 0.25} -2.6 3 -0.6", fill="none", stroke="#fff", stroke_opacity=0.45,
            stroke_width=1, stroke_linecap="round")


# --- GIMP: Wilber painted on a canvas, on an easel, a brush on its ledge ------

def _wilber(ic, x, y, k, body="#6F6552", dark="#3D362B", paint="#E2702C"):
    """GIMP's creature, redrawn: head, two ears, eyes on top, snout to the
    right, a brush in its mouth; on a 100 grid from (x, y), k px a unit."""
    with ic.g(transform=f"translate({x} {y}) scale({k})"):
        # the brush it holds, behind the head
        ic.path("M58 58 L96 30", stroke="#B07A3A", stroke_width=5, stroke_linecap="round")
        ic.path("M92 33 L99 25", stroke="#C9CED4", stroke_width=6)
        ic.path("M97 27 Q104 16 108 14 Q106 22 100 30z", fill=paint)
        # the ears, tall and pointed, leaning back
        ic.path("M22 44 C14 26 10 12 12 2 C22 10 32 24 36 38z", fill=body)
        ic.path("M34 40 C32 22 34 8 40 0 C46 12 48 26 46 40z", fill=body)
        ic.path("M20 36 C16 24 15 15 16 9 C21 15 26 24 29 34z", fill=dark, opacity=0.35)
        # the head and snout
        ic.path("M10 62 C8 44 22 34 40 36 C54 36 64 42 76 48 C86 52 92 58 90 66 C88 74 76 76 66 74 "
                "C58 86 40 92 26 86 C14 82 10 72 10 62z", fill=body)
        ic.path("M14 64 C14 50 24 42 38 40", fill="none", stroke="#fff", stroke_opacity=0.25, stroke_width=3,
                stroke_linecap="round")
        ic.ellipse(88, 60, 5, 4, fill=dark)
        ic.path("M66 72 C72 70 80 70 86 68", fill="none", stroke=dark, stroke_width=2, stroke_linecap="round")
        # the eyes, big, on top
        for ex, ey, r in ((44, 40, 11), (62, 44, 9)):
            ic.circle(ex, ey, r + 1.5, fill=dark)
            ic.circle(ex, ey, r, fill="#FBF7EC")
            ic.circle(ex + r * 0.3, ey + r * 0.15, r * 0.42, fill="#1E1A14")
            ic.circle(ex + r * 0.15, ey - r * 0.05, r * 0.14, fill="#fff")


@icon("gimp", kind="app", names=["gimp", "org.gimp.GIMP"], title="GIMP")
def gimp(ic):
    tile(ic, "#7D705B", "#3B3328")
    shadow(ic, 128, 218, 96, 11)
    legs = wood(ic, "#B07A48", "#5E3A1A")
    # the easel's back leg and its two front legs
    ic.path("M124 30 L134 30 L140 216 L132 216z", fill="#4E3218")
    ic.path("M96 150 L86 216 L95 216 L106 150z", fill=legs)
    ic.path("M150 150 L160 216 L169 216 L160 150z", fill=legs)
    ic.rect(122, 24, 12, 16, rx=2, fill=legs)
    # the canvas: its stretcher's edge, then the face
    ic.rect(44, 40, 168, 122, rx=3, fill="#000", opacity=0.3, transform="translate(3 4)")
    ic.rect(44, 40, 168, 122, rx=3, fill="#C9BEA6")
    ic.rect(44, 40, 165, 119, rx=2.5, fill=paper(ic, "cream"))
    weave = ic.define('<pattern id="{id}" width="3" height="3" patternUnits="userSpaceOnUse">'
                      '<rect width="3" height="1" fill="#8C7F68" opacity=".12"/>'
                      '<rect width="1" height="3" fill="#8C7F68" opacity=".08"/></pattern>', "p")
    ic.rect(44, 40, 165, 119, rx=2.5, fill=f"url(#{weave})")
    # the painting: a warm wash, Wilber
    ic.path("M54 150 C70 120 120 96 200 104 L200 150z", fill="#E8C68E", opacity=0.6)
    ic.circle(176, 70, 14, fill="#F2B45A", opacity=0.7)
    _wilber(ic, 58, 46, 1.12)
    ic.text("W.", 198, 152, 12, font="hand", anchor="end", fill="#6F6552")
    ic.line(45, 41.2, 208, 41.2, stroke="#fff", stroke_width=1.5, opacity=0.8)
    # the ledge it stands on, a brush lying there
    ic.rect(40, 160, 176, 14, rx=2, fill="#000", opacity=0.3, transform="translate(2 3)")
    ic.rect(40, 160, 176, 14, rx=2, fill=wood(ic, "#C48A55", "#7A4A22"))
    ic.line(41, 160.8, 215, 160.8, stroke="#fff", stroke_opacity=0.35, stroke_width=1.5)
    ic.text("GIMP", 200, 171, 8, font="mono-semibold", anchor="end", spacing=2, fill="#4E3218", opacity=0.75)
    with ic.g(transform="translate(54 156) rotate(-3)"):
        brush(ic, 118, wood(ic, "#E09A4A", "#8A4E18"), paint="#E2702C", tip=26)


@small("gimp")
def gimp16(ic):
    tile(ic, "#7D705B", "#3B3328")
    ic.rect(2, 2, 12, 9.5, rx=0.4, fill="#F4EEE0")
    ic.path("M9.4 8.2 L12.6 3.6", stroke="#E2702C", stroke_width=1.1, stroke_linecap="round")
    ic.path("M3.4 4 L4.6 7.6 L6.2 7 z M5.8 3.2 L6.4 6.8 L7.6 6.6z", fill="#5E5545")
    ic.path("M3.2 9 C3 7.2 4.6 6.4 6.6 6.6 C8.4 6.8 10.4 7.4 10.4 8.6 C10.2 9.8 8 10.4 6.2 10.4 "
            "C4.4 10.4 3.3 10 3.2 9z", fill="#5E5545")
    for x, y in ((6.4, 5.6), (9, 6.2)):
        ic.circle(x, y, 1.5, fill="#2E281F")
        ic.circle(x, y, 1.2, fill="#FFFFFF")
        ic.circle(x + 0.4, y + 0.2, 0.55, fill="#1E1A14")
    ic.rect(1.5, 11.5, 13, 1.6, rx=0.4, fill="#B07A48")
    ic.rect(4, 13, 1.2, 2, fill="#8A5A30")
    ic.rect(10.8, 13, 1.2, 2, fill="#8A5A30")


# --- Inkscape: a dip pen, its steel nib inking the mountain mark, as vectors --

@icon("inkscape", kind="app", names=["inkscape", "inkscape-logo", "org.inkscape.Inkscape"], title="Inkscape")
def inkscape(ic):
    tile(ic, "#4A5058", "#1B1E22")
    shadow(ic, 124, 214, 100, 12)
    # the sheet, a little turned
    with ic.g(transform="rotate(-4 124 128)"):
        ic.rect(34, 40, 176, 168, rx=3, fill="#000", opacity=0.3, transform="translate(3 4)")
        ic.rect(34, 40, 176, 168, rx=3, fill=paper(ic, "white"))
        ic.line(35, 41, 209, 41, stroke="#fff", stroke_width=1.5)
        grid = ic.define('<pattern id="{id}" width="12" height="12" patternUnits="userSpaceOnUse">'
                         '<path d="M12 0V12H0" fill="none" stroke="#7FA6CF" stroke-opacity=".22"/></pattern>', "p")
        ic.rect(40, 46, 164, 156, fill=f"url(#{grid})")
        # the mark: a black mountain, its snow running down in drips
        mtn = "M52 178 L104 92 Q116 74 128 92 L184 178 Q186 184 180 184 L56 184 Q50 184 52 178z"
        ic.path(mtn, fill="#16181B")
        ic.path("M92 112 L104 92 Q116 74 128 92 L140 112 Q136 122 130 116 Q126 132 120 118 Q114 140 108 120 "
                "Q102 128 98 116 Q94 122 92 112z", fill="#FFFFFF")
        ic.path("M108 120 Q110 134 112 146 Q114 152 116 146 Q117 134 118 120", fill="#fff")
        # selected: its box and its nodes, one with handles
        ic.rect(48, 78, 140, 110, fill="none", stroke="#1B1E22", stroke_opacity=0.55, stroke_dasharray="3 3")
        for x, y in ((48, 78), (188, 78), (48, 188), (188, 188), (118, 78), (118, 188), (48, 133), (188, 133)):
            ic.path("M-4 0L0-4L4 0L0 4z" if (x, y) in ((118, 78), (118, 188), (48, 133), (188, 133)) else
                    "M-3.5-3.5h7v7h-7z", transform=f"translate({x} {y})", fill="#1B1E22", opacity=0.7)
        ic.line(84, 112, 128, 70, stroke="#3B7FD4", stroke_width=1.2)
        for x, y in ((84, 112), (128, 70)):
            ic.circle(x, y, 3, fill="#fff", stroke="#3B7FD4", stroke_width=1.4)
        ic.rect(101.5, 87.5, 7, 7, fill="#3B7FD4", stroke="#fff")
        for x, y in ((52, 178), (184, 178)):
            ic.rect(x - 3, y - 3, 6, 6, fill="#fff", stroke="#16181B", stroke_width=1.2)
        ic.text("Inkscape", 44, 60, 10, font="sans-semibold", fill="#2B2E33", opacity=0.75)
        ic.text("mountain.svg", 44, 70, 6.5, font="mono", fill="#7A7E84")
    # the pen: its nib at the drawing, its holder up to the right
    with ic.g(transform="translate(150 160) rotate(38)"):
        ic.path("M-12 -136 a12 12 0 0 1 24 0 V-80 L11 -60 C10 -40 3 -14 0 0 C-3 -14 -10 -40 -11 -60 L-12 -80z",
                fill="#000", opacity=0.22, transform="translate(16 5)")
        holder = ic.lin([(0, "#3A3E45"), (0.35, "#1A1C20"), (1, "#060708")], 0, 0, 1, 0)
        ic.path("M-12 -136 a12 12 0 0 1 24 0 V-96 C12 -88 10 -84 9 -78 H-9 C-10 -84 -12 -88 -12 -96z", fill=holder)
        ic.line(-7, -136, -7, -98, stroke="#fff", stroke_opacity=0.3, stroke_width=2, stroke_linecap="round")
        ic.rect(-10, -100, 20, 8, rx=1, fill=brass(ic, 0, 0, 1, 0))
        nib = ic.lin([(0, "#E9ECEF"), (0.45, "#9AA1A9"), (1, "#4D535A")], 0, 0, 1, 0)
        ic.path("M0 0 C3 -14 10 -40 11 -60 L11 -80 L-11 -80 L-11 -60 C-10 -40 -3 -14 0 0z", fill=nib)
        ic.path("M-1 -4 C-4 -20 -8 -40 -9 -60", fill="none", stroke="#fff", stroke_opacity=0.6, stroke_width=1)
        ic.path("M0 0 C1.5 -6 2 -10 2 -12 L-2 -12 C-2 -10 -1.5 -6 0 0z", fill="#16181B")
        ic.line(0, -10, 0, -42, stroke="#2A2E33", stroke_width=1)
        ic.circle(0, -45, 3.4, fill="#2A2E33")
        ic.circle(-0.6, -45.6, 1.4, fill="#fff", opacity=0.3)
        ic.path("M-11 -72 h22", stroke="#2A2E33", stroke_opacity=0.5, stroke_width=1)


@small("inkscape")
def inkscape16(ic):
    tile(ic, "#4A5058", "#1B1E22")
    ic.rect(2, 2.5, 11, 11, rx=0.5, fill="#FFFFFF")
    ic.path("M3 12 L7 5.5 Q7.8 4.5 8.6 5.5 L12 12z", fill="#16181B")
    ic.path("M5.9 7.3 L7 5.5 Q7.8 4.5 8.6 5.5 L9.6 7.2 Q8.8 8 8.3 7.3 Q7.8 9.4 7.3 7.4 Q6.6 8 5.9 7.3z", fill="#fff")
    ic.path("M10.5 9.5 L14.2 3.6 L15.2 4.3 L11.5 10.2z", fill="#1A1C20")
    ic.path("M10.5 9.5 L9.8 11.8 L11.6 10.1z", fill="#C3C8CE")


# --- Krita: a painter's palette and a brush in Krita's pink and blue ----------

@icon("krita", kind="app", names=["calligrakrita", "calligrakrita2", "krita", "org.kde.krita"], title="Krita")
def krita(ic):
    tile(ic, "#3B5C9A", "#1A2B52")
    shadow(ic, 128, 210, 104, 12)
    pal = ("M30 118 C26 70 80 40 140 44 C196 48 232 86 226 132 C220 176 172 200 124 196 "
           "C104 194 100 178 86 176 C70 174 66 194 50 186 C34 178 32 150 30 118z")
    ic.path(pal, fill="#3A2210", transform="translate(2 5)")
    ic.path(pal, fill=wood(ic, "#E3B27A", "#A2672F"))
    grain = ic.clip(f'<path d="{pal}"/>')
    with ic.g(clip_path=grain, fill="none", stroke="#8A5424", stroke_opacity=0.18, stroke_width=1.2):
        for k in range(8):
            ic.path(f"M20 {70 + k * 18} C80 {56 + k * 18} 160 {84 + k * 18} 240 {66 + k * 18}")
    ic.path("M36 112 C36 76 82 50 138 50", fill="none", stroke="#FFE7C2", stroke_opacity=0.6, stroke_width=2,
            stroke_linecap="round")
    # the thumb hole
    ic.ellipse(70, 140, 13, 11, fill="#2A1A0C")
    ic.path("M58 142 a13 11 0 0 0 25 2", fill="none", stroke="#FFE7C2", stroke_opacity=0.5, stroke_width=1.5)
    # the daubs of paint, each a wet heap
    daubs = [(96, 76, 15, "#E8407A", "#9E1846"), (134, 66, 13, "#3BA3E8", "#185E9E"),
             (172, 76, 13, "#F6F2EA", "#B9B2A4"), (198, 104, 12, "#F5C04A", "#B07A14"),
             (200, 140, 12, "#8A4FD8", "#4E2290"), (176, 168, 11, "#3FC4B0", "#16786A")]
    for x, y, r, light, dark in daubs:
        ic.ellipse(x + 1.5, y + 3, r, r * 0.8, fill="#000", opacity=0.22)
        ic.path(f"M{x - r} {y + 2} C{x - r} {y - r * 0.9} {x - 2} {y - r * 0.6} {x + 2} {y - r * 0.9} "
                f"C{x + r * 0.7} {y - r * 0.8} {x + r} {y - 2} {x + r} {y + 2} C{x + r} {y + r * 0.8} "
                f"{x - r} {y + r * 0.8} {x - r} {y + 2}z",
                fill=ic.rad([(0, light), (1, dark)], cx=0.38, cy=0.3, r=0.8))
        ic.ellipse(x - r * 0.35, y - r * 0.3, r * 0.3, r * 0.18, fill="#fff", opacity=0.55,
                   transform=f"rotate(-25 {x - r * 0.35} {y - r * 0.3})")
    # pink and blue, being mixed: a stroke across the middle
    ic.path("M100 120 C118 104 146 104 160 116 C150 126 128 130 112 134 C104 134 98 128 100 120z", fill="#E8407A")
    ic.path("M128 128 C142 118 156 116 168 124 C160 134 146 138 132 138z", fill="#6C7BE0", opacity=0.9)
    ic.path("M106 120 C122 110 140 108 152 114", fill="none", stroke="#fff", stroke_opacity=0.4, stroke_width=1.5,
            stroke_linecap="round")
    # the brush, laid across: Krita pink handle
    with ic.g(transform="translate(104 128) rotate(32)"):
        ic.path("M6 0 L148 -3.5 L148 3.5z", fill="#000", opacity=0.2, transform="translate(5 3)")
        brush(ic, 150, ic.lin([(0, "#FF7AA8"), (0.5, "#E8407A"), (1, "#9E1846")], 0, 0, 0, 1),
              ferrule_w=11, paint="#E8407A", tip=30)
        ic.text("KRITA", 108, 2.4, 6.5, font="mono-semibold", anchor="middle", spacing=1.6, fill="#FFE0EA",
                opacity=0.85)


@small("krita")
def krita16(ic):
    tile(ic, "#3B5C9A", "#1A2B52")
    ic.path("M1.8 8 C1.6 4.6 5 2.6 8.8 2.8 C12.4 3 14.6 5.6 14.2 8.6 C13.8 11.4 10.8 12.8 7.8 12.6 "
            "C6.6 12.5 6.4 11.4 5.4 11.4 C4.4 11.3 4.2 12.6 3.2 12.1 C2.2 11.6 2 10 1.8 8z", fill="#D6A16A")
    ic.circle(4.4, 9, 1, fill="#5A3A1C")
    ic.circle(6, 5.2, 1.2, fill="#E8407A")
    ic.circle(9, 4.6, 1.1, fill="#3BA3E8")
    ic.circle(11.8, 6.4, 1, fill="#F5C04A")
    ic.path("M6.8 8.2 L14.6 13.6", stroke="#E8407A", stroke_width=1.4, stroke_linecap="round")
    ic.path("M6.8 8.2 L8.4 9.3", stroke="#3A2A1A", stroke_width=1.4, stroke_linecap="round")


# --- Blender: the default cube, selected, on a modelling turntable ------------

def _blender_mark(ic, cx, cy, r):
    """Blender's mark, redrawn small: a ring with a blue eye, its arm out to
    the lower left."""
    ic.path(f"M{cx - r * 0.6} {cy + r * 0.2} L{cx - r * 2} {cy + r * 1.1} L{cx - r * 2.05} {cy + r * 0.55} "
            f"L{cx - r * 1.3} {cy + r * 0.05} L{cx - r * 2.2} {cy + r * 0.05} L{cx - r * 2.2} {cy - r * 0.45} "
            f"L{cx - r * 0.7} {cy - r * 0.5}z", fill="#F07C1A")
    ic.circle(cx, cy, r, fill="#F07C1A")
    ic.circle(cx, cy, r * 0.66, fill="#FFFFFF")
    ic.circle(cx, cy, r * 0.38, fill="#2B6BC2")


@icon("blender", kind="app", names=["Blender", "blender", "org.blender.Blender"], title="Blender")
def blender(ic):
    tile(ic, "#3D6EA8", "#16335A")
    shadow(ic, 128, 214, 100, 12)
    cx, top = 128, 166
    # the turntable: its base, its side, its plate
    ic.path(f"M30 {top} v22 a98 22 0 0 0 196 0 v-22z", fill=ic.lin([(0, "#4A4E55"), (0.5, "#2A2D32"),
                                                                   (1, "#121316")], 0, 0, 1, 0))
    ic.path(f"M30 {top + 10} a98 22 0 0 0 196 0", fill="none", stroke="#000", stroke_opacity=0.4, stroke_width=1.5)
    ic.path(f"M30 {top + 11.5} a98 22 0 0 0 196 0", fill="none", stroke="#fff", stroke_opacity=0.12)
    ic.ellipse(cx, top, 98, 22, fill=ic.lin([(0, "#6B7078"), (1, "#3A3E44")], 0, 0, 1, 1))
    ic.ellipse(cx, top, 86, 18.5, fill=ic.lin([(0, "#55595F"), (1, "#2C2F34")], 0, 0, 1, 1))
    for k in range(36):
        a = math.radians(k * 10)
        x1, y1 = cx + 86 * math.cos(a), top + 18.5 * math.sin(a)
        x2, y2 = cx + (92 if k % 9 == 0 else 89) * math.cos(a), top + (20 if k % 9 == 0 else 19.4) * math.sin(a)
        ic.line(x1, y1, x2, y2, stroke="#D8DCE0", stroke_opacity=0.7, stroke_width=1 if k % 9 else 1.6)
    ic.path(f"M34 {top - 3} a98 22 0 0 1 120 -18", fill="none", stroke="#fff", stroke_opacity=0.3, stroke_width=1.5)
    # the floor grid on the plate, its red and green axes
    with ic.g(clip_path=ic.clip(f'<ellipse cx="{cx}" cy="{top}" rx="86" ry="18.5"/>')):
        for k in range(-4, 5):
            ic.line(cx + k * 20 - 40, top - 20, cx + k * 20 + 40, top + 20, stroke="#fff", stroke_opacity=0.08)
            ic.line(cx + k * 20 + 40, top - 20, cx + k * 20 - 40, top + 20, stroke="#fff", stroke_opacity=0.08)
        ic.line(cx - 80, top + 20, cx + 80, top - 20, stroke="#E0484A", stroke_opacity=0.7, stroke_width=1.4)
        ic.line(cx - 80, top - 20, cx + 80, top + 20, stroke="#7CC04A", stroke_opacity=0.7, stroke_width=1.4)
    # the badge on the front
    ic.rect(cx - 30, top + 22, 60, 15, rx=7.5, fill="#16181B")
    ic.rect(cx - 30, top + 22, 60, 15, rx=7.5, fill="none", stroke="#fff", stroke_opacity=0.2)
    _blender_mark(ic, cx - 15, top + 29.5, 5)
    ic.text("blender", cx + 7, top + 33, 8.5, font="sans-semibold", anchor="middle", fill="#F1F1EF")
    # the 3D cursor, red and white, on the plate
    ux, uy = 70, top - 2
    ic.ellipse(ux, uy, 9, 4, fill="none", stroke="#fff", stroke_width=1.8, stroke_dasharray="3.5 3.5")
    ic.ellipse(ux, uy, 9, 4, fill="none", stroke="#E0484A", stroke_width=1.8, stroke_dasharray="3.5 3.5",
               stroke_dashoffset=3.5)
    ic.line(ux - 13, uy, ux - 6, uy, stroke="#1B1C1F", stroke_width=1.2)
    ic.line(ux + 6, uy, ux + 13, uy, stroke="#1B1C1F", stroke_width=1.2)
    ic.line(ux, uy - 9, ux, uy - 5, stroke="#1B1C1F", stroke_width=1.2)
    # the cube: three faces of clay, its outline orange as Blender selects it
    s = 46
    p0 = (cx, top - 2)               # the bottom front corner
    l = (cx - s * 0.95, top - 2 - s * 0.48)
    r = (cx + s * 0.95, top - 2 - s * 0.48)
    up = s * 1.15
    b = (cx, top - 2 - s * 0.96)
    T = lambda p: (p[0], p[1] - up)  # noqa: E731
    ic.ellipse(cx + 8, top + 2, 70, 12, fill="#000", opacity=0.35)
    left = [l, p0, T(p0), T(l)]
    right = [p0, r, T(r), T(p0)]
    topf = [T(l), T(p0), T(r), T(b)]
    ic.poly(left, fill=ic.lin([(0, "#B4B8BE"), (1, "#8A8F96")], 0, 0, 1, 1))
    ic.poly(right, fill=ic.lin([(0, "#7C8188"), (1, "#5A5E65")], 0, 0, 1, 1))
    ic.poly(topf, fill=ic.lin([(0, "#E4E6E9"), (1, "#C4C8CD")], 0, 0, 1, 1))
    ic.poly([l, p0, r, T(r), T(b), T(l)], fill="none", stroke="#F59A2A", stroke_width=3.2, stroke_linejoin="round")
    for a, z in ((T(p0), p0), (T(l), T(p0)), (T(p0), T(r))):
        ic.line(a[0], a[1], z[0], z[1], stroke="#FFC37A", stroke_width=1.2, opacity=0.9)
    # its origin, a dot at the centre
    ic.circle(cx, top - 2 - s * 0.48 - up / 2, 3, fill="#F59A2A", stroke="#1B1C1F", stroke_width=0.8)


@small("blender")
def blender16(ic):
    tile(ic, "#3D6EA8", "#16335A")
    ic.ellipse(8, 11.6, 6.6, 2, fill="#2A2D32")
    ic.ellipse(8, 11, 6.6, 2, fill="#5A5E65")
    ic.poly([(3.6, 5.6), (8, 7.6), (8, 12.4), (3.6, 10.4)], fill="#A2A7AD")
    ic.poly([(8, 7.6), (12.4, 5.6), (12.4, 10.4), (8, 12.4)], fill="#6A6F76")
    ic.poly([(3.6, 5.6), (8, 3.6), (12.4, 5.6), (8, 7.6)], fill="#E0E2E5")
    ic.poly([(3.6, 5.6), (8, 3.6), (12.4, 5.6), (12.4, 10.4), (8, 12.4), (3.6, 10.4)], fill="none",
            stroke="#F59A2A", stroke_width=0.9, stroke_linejoin="round")


# --- darktable: a lens, its iris stopped down, on negatives under a safelight -

@icon("darktable", kind="app", names=["darktable", "org.darktable.Darktable"], title="darktable")
def darktable(ic):
    tile(ic, "#4A2226", "#14080A")
    shadow(ic, 128, 216, 96, 12)
    # a strip of negatives behind, across the desk
    with ic.g(transform="rotate(-14 128 128)"):
        ic.rect(8, 150, 240, 50, fill="#000", opacity=0.3, transform="translate(2 4)")
        ic.rect(8, 150, 240, 50, fill=ic.lin([(0, "#D8823A"), (1, "#9C4E1C")]))
        for x in range(10, 248, 9):
            ic.rect(x, 153, 5, 5, rx=1, fill="#2A1208")
            ic.rect(x, 192, 5, 5, rx=1, fill="#2A1208")
        for x in (14, 84, 154, 224):
            ic.rect(x, 162, 64, 27, fill="#3A2A30", opacity=0.55)
            ic.path(f"M{x} 189 L{x + 22} 172 L{x + 34} 180 L{x + 44} 170 L{x + 64} 186 V189z", fill="#E8D0C0",
                    opacity=0.5)
        ic.text("DT 400   23   24", 100, 160, 5, font="mono-semibold", spacing=0.8, fill="#2A1208", opacity=0.6)
    cx, cy = 128, 108
    # the lens: its barrel seen from the front
    ic.circle(cx + 3, cy + 5, 86, fill="#000", opacity=0.45)
    ic.circle(cx, cy, 86, fill=ic.lin([(0, "#5A5E65"), (0.5, "#24262A"), (1, "#0E0F11")], 0, 0, 1, 1))
    ic.circle(cx, cy, 84.5, fill="none", stroke="#1E2024", stroke_width=4, stroke_dasharray="1.4 1.6", opacity=0.9)
    ic.circle(cx, cy, 78, fill=ic.lin([(0, "#2E3136"), (1, "#0B0C0E")], 0, 0, 1, 1))
    ic.circle(cx, cy, 78, fill="none", stroke="#fff", stroke_opacity=0.18, stroke_width=1)
    # the ring's legend
    with ic.g():
        for s, deg, size in (("darktable", -38, 11), ("1:1.4", 30, 8.5), ("50mm", 64, 8.5)):
            _ring_text(ic, s, cx, cy, 67, deg, size)
        ic.path(f"M{cx} {cy - 76} l-3 -5 h6z", fill="#E0484A")
    ic.circle(cx, cy, 60, fill="#060607")
    # the iris: seven blades closing to a heptagon
    R, ro, n, turn = 56, 22, 7, 12
    iris = ic.clip(f'<circle cx="{cx}" cy="{cy}" r="{R}"/>')
    with ic.g(clip_path=iris):
        ic.circle(cx, cy, R, fill=ic.lin([(0, "#3E4248"), (1, "#141518")], 0, 0, 1, 1))
        corners = [polar(cx, cy, ro, turn + k * 360 / n) for k in range(n)]
        for k in range(n):
            ax, ay = corners[k]
            bx, by = corners[(k + 1) % n]
            dx, dy = bx - ax, by - ay
            m = math.hypot(dx, dy)
            ex, ey = ax + dx / m * 90, ay + dy / m * 90
            shade = 0.06 + 0.05 * ((k * 3) % n) / n
            ic.poly([(ax, ay), (ex, ey), polar(cx, cy, 120, turn + k * 360 / n + 70)],
                    fill="#fff", opacity=shade)
            ic.line(ax, ay, ex, ey, stroke="#000", stroke_opacity=0.6, stroke_width=1.6)
            ic.line(ax + 0.8, ay + 0.8, ex + 0.8, ey + 0.8, stroke="#fff", stroke_opacity=0.12, stroke_width=0.8)
    # through the opening, the rear glass in the safelight's red
    hept = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in [polar(cx, cy, ro, turn + k * 360 / n) for k in range(n)]) + "Z"
    ic.path(hept, fill=ic.rad([(0, "#E0484A"), (0.6, "#6A1214"), (1, "#1A0405")], cx=0.4, cy=0.4, r=0.7))
    # the front glass over it all
    ic.circle(cx, cy, 60, fill=glare(ic, 1.2))
    ic.path(f"M{cx - 50} {cy - 6}a52 52 0 0 1 40 -44 58 58 0 0 0 -40 44z", fill="#fff", opacity=0.45)
    ic.ellipse(cx + 30, cy + 34, 12, 5, fill="#FF6A5A", opacity=0.3, transform=f"rotate(-40 {cx + 30} {cy + 34})")


def _ring_text(ic, s, cx, cy, r, deg, size):
    with ic.g(transform=f"rotate({deg} {cx} {cy})"):
        ic.text(s, cx, cy - r + size * 0.35, size, font="sans-semibold", anchor="middle", fill="#E9E6DF")


@small("darktable")
def darktable16(ic):
    tile(ic, "#4A2226", "#14080A")
    ic.circle(8, 8, 6.6, fill="#2A2C30")
    ic.circle(8, 8, 5.2, fill="#4A4E55")
    for k in range(6):
        x1, y1 = polar(8, 8, 2, k * 60 + 10)
        x2, y2 = polar(8, 8, 5.2, k * 60 + 70)
        ic.line(x1, y1, x2, y2, stroke="#141518", stroke_width=0.7)
    ic.poly([polar(8, 8, 2.2, k * 60 + 10) for k in range(6)], fill="#D8383A")


# --- Aseprite: a sprite drawn square by square on a pixel board --------------

SPRITE = [
    "..............",
    "..K........K..",
    ".KHK......KHK.",
    ".KOPK....KPOK.",
    ".KOOOKKKKOOOK.",
    "KHHOOOOOOOOODK",
    "KHOOOOOOOOOODK",
    "KOOKWOOOOKWODK",
    "KOOKKOOOOKKODK",
    "KORROOKKOORRDK",
    "KOOOOOOOOOODDK",
    ".KOOOOOOOOODK.",
    "..KKDDDDDDKK..",
    "....KKKKKK....",
]


@icon("aseprite", kind="app", names=["aseprite"], title="Aseprite")
def aseprite(ic):
    tile(ic, "#3F8C95", "#163F48")
    shadow(ic, 128, 214, 98, 12)
    # the board: a dark frame, a light grid inside
    ic.rect(34, 30, 188, 180, rx=10, fill="#000", opacity=0.3, transform="translate(2 4)")
    ic.rect(34, 30, 188, 180, rx=10, fill=ic.lin([(0, "#3E4459"), (1, "#1F2232")]))
    ic.rect(34.75, 30.75, 186.5, 178.5, rx=9.25, fill="none", stroke="#fff", stroke_opacity=0.18, stroke_width=1.5)
    ic.text("ASEPRITE", 44, 44, 7, font="mono-semibold", spacing=1.6, fill="#C9D3E8", opacity=0.75)
    ic.text("14×14", 212, 44, 7, font="mono", anchor="end", fill="#C9D3E8", opacity=0.55)
    s, x0, y0 = 10, 58, 52
    # the transparent checks, then the sprite on them
    checks = ic.define('<pattern id="{id}" width="10" height="10" patternUnits="userSpaceOnUse" x="58" y="52">'
                       '<rect width="10" height="10" fill="#D9DCE3"/><rect width="5" height="5" fill="#C3C7D1"/>'
                       '<rect x="5" y="5" width="5" height="5" fill="#C3C7D1"/></pattern>', "p")
    ic.rect(x0, y0, 140, 140, fill=f"url(#{checks})")
    pixels(ic, SPRITE, x0, y0, s, {"K": "#1E2032", "O": "#F2A03A", "H": "#FFD08A", "D": "#C4661C",
                                    "W": "#FFFFFF", "P": "#F07A9A", "R": "#F07A6A"})
    grid = ic.define('<pattern id="{id}" width="10" height="10" patternUnits="userSpaceOnUse" x="58" y="52">'
                     '<path d="M10 0V10H0" fill="none" stroke="#1E2032" stroke-opacity=".18"/></pattern>', "p")
    ic.rect(x0, y0, 140, 140, fill=f"url(#{grid})")
    # the cursor: one pixel being set
    ic.rect(x0 + 12 * s, y0 + 1 * s, s, s, fill="#F2A03A")
    ic.rect(x0 + 12 * s - 1, y0 + 1 * s - 1, s + 2, s + 2, fill="none", stroke="#fff", stroke_width=1.5)
    # the palette along the bottom
    for i, c in enumerate(("#1E2032", "#FFFFFF", "#FFD08A", "#F2A03A", "#C4661C", "#F07A6A", "#5FBF6A")):
        ic.rect(58 + i * 20, 197, 16, 8, rx=1.5, fill=c)
    ic.rect(116.5, 196.5, 17, 9, rx=2, fill="none", stroke="#fff", stroke_width=1.2)


@small("aseprite")
def aseprite16(ic):
    tile(ic, "#3F8C95", "#163F48")
    ic.rect(2, 2, 12, 12, rx=1, fill="#2A2E40")
    ic.rect(3, 3, 10, 10, fill="#D9DCE3")
    pixels(ic, ["K......K", "KOK..KOK", "KOOKKOOK", "OOOOOOOO", "OKOOOOKO", "ORROORRO", "OOOOOOOO", ".OOOOOO."],
           4, 4, 1, {"K": "#1E2032", "O": "#F2A03A", "R": "#F07A6A"})


# --- LibreSprite: a pixel-art pencil, square by square, drawing a squiggle ---

def _pixel_pencil(tip, end, w=2.7):
    """The cells of a pencil drawn as pixel art on a grid, from its tip to
    its eraser (cell coordinates): {(i, j): part}, outline cells included."""
    (tx, ty), (ex, ey) = tip, end
    n = math.hypot(ex - tx, ey - ty)
    dx, dy = (ex - tx) / n, (ey - ty) / n
    nx, ny = dy, -dx  # toward the top left, where the light is
    if nx > 0 or ny > 0:
        nx, ny = -nx, -ny
    cells = {}
    for j in range(32):
        for i in range(32):
            cx, cy = i + 0.5 - tx, j + 0.5 - ty
            u = cx * dx + cy * dy
            v = cx * nx + cy * ny
            if u < -0.6 or u > n + 0.8:
                continue
            prof = w * min(1, max(u, 0) / 6)
            if abs(v) > prof + 0.9 or (u > n and abs(v) > prof):
                continue
            if abs(v) > prof or u > n:
                cells[(i, j)] = "line"
            elif u < 2.4:
                cells[(i, j)] = "lead"
            elif u < 6:
                cells[(i, j)] = "wood-lit" if v > 0.4 else "wood"
            elif u < n - 6:
                cells[(i, j)] = "lit" if v > 1.1 else "shade" if v < -0.9 else "body"
            elif u < n - 3.4:
                cells[(i, j)] = "band" if abs(u - (n - 4.7)) < 0.5 else "steel-lit" if v > 0.4 else "steel"
            else:
                cells[(i, j)] = "rubber-lit" if v > 0.4 else "rubber"
    return cells


PENCIL_COLOURS = {"line": "#24203A", "lead": "#3A3650", "wood": "#E2B47A", "wood-lit": "#F6D7A8",
                  "lit": "#FFE07A", "body": "#F5B82E", "shade": "#C9780E", "steel": "#9AA1A9",
                  "steel-lit": "#DDE1E5", "band": "#6B727B", "rubber": "#D94C74", "rubber-lit": "#FF8FAE"}


@icon("libresprite", kind="app", names=["libresprite"], title="LibreSprite")
def libresprite(ic):
    tile(ic, "#5E8C3E", "#25461A")
    shadow(ic, 132, 214, 92, 11)
    s = 8
    # the squiggle it has drawn, from its tip along the desk
    trail = [(7, 25), (6, 26), (6, 27), (7, 28), (8, 28), (9, 27), (10, 26), (11, 26), (12, 27), (13, 28),
             (14, 28), (15, 27), (16, 26), (17, 26), (18, 27)]
    for i, j in trail:
        ic.rect(i * s + 2, j * s + 3, s, s, fill="#000", opacity=0.28)
    for k, (i, j) in enumerate(trail):
        ic.rect(i * s, j * s, s, s, fill=("#B85AC8", "#9A46B8", "#7A3FA8", "#5A2E8A")[min(3, k // 4)])
        ic.rect(i * s, j * s, s, 2, fill="#fff", opacity=0.25)
    cells = _pixel_pencil((8.6, 23.4), (25.4, 6.6))
    # its shadow, cast down and right, then the pixels
    for (i, j) in cells:
        ic.rect(i * s + 6, j * s + 9, s, s, fill="#000", opacity=0.22)
    for (i, j), part in cells.items():
        ic.rect(i * s, j * s, s, s, fill=PENCIL_COLOURS[part])
    # a highlight pixel on the lead, a glint on the ferrule
    ic.rect(9 * s + 2, 22 * s + 2, 3, 3, fill="#fff", opacity=0.6)
    ic.text("LibreSprite", 136, 118, 11, font="mono-semibold", anchor="middle", fill="#7A4606",
            transform="rotate(-45 136 114)")


@small("libresprite")
def libresprite16(ic):
    tile(ic, "#5E8C3E", "#25461A")
    for x, y in ((3, 12), (2, 13), (3, 14), (4, 14), (5, 13)):
        ic.rect(x, y, 1, 1, fill="#B85AC8")
    col = {"L": "#24203A", "W": "#F6D7A8", "Y": "#F5B82E", "S": "#C9CED4", "P": "#E25A80"}
    pixels(ic, ["........PP.", ".......PPP.", "......SSP..", ".....YYSS..", "....YYYY...", "...YYYY....",
                "..WYYY.....", ".WWYY......", ".LW........"], 3, 2, 1, col)



# --- ImageMagick: the wizard's hat on a photograph it is changing -------------

def _scene(ic, sky, hill, far, water, sun):
    """A small landscape in the print's frame x 54..186, y 98..190."""
    ic.rect(54, 98, 132, 92, fill=ic.lin([(0, sky[0]), (1, sky[1])]))
    ic.circle(158, 120, 9, fill=sun)
    ic.path("M54 160 L84 132 L104 148 L126 124 L160 154 L186 140 V170 H54z", fill=far)
    ic.path("M54 170 Q90 150 128 164 T186 160 V190 H54z", fill=hill)
    ic.path("M54 180 Q100 172 186 182 V190 H54z", fill=water)


@icon("imagemagick", kind="app", names=["display-im6.q16", "display-im7.q16", "imagemagick"], title="ImageMagick")
def imagemagick(ic):
    tile(ic, "#6A3F9A", "#2C1556")
    shadow(ic, 128, 218, 98, 11)
    # the print, half turned already
    with ic.g(transform="rotate(5 120 144)"):
        ic.rect(44, 88, 152, 128, rx=3, fill="#000", opacity=0.3, transform="translate(3 4)")
        ic.rect(44, 88, 152, 128, rx=3, fill=paper(ic, "white"))
        ic.line(45, 89, 195, 89, stroke="#fff", stroke_width=1.5)
        _scene(ic, ("#7FB2D9", "#E2EEF2"), "#3E7A46", "#6F8296", "#4A7EA6", "#FFF2C0")
        right = ic.clip('<path d="M150 98 L186 98 L186 190 L104 190z"/>')
        with ic.g(clip_path=right):
            _scene(ic, ("#F28A3A", "#FCD6A0"), "#5A2A6E", "#B4487A", "#2A2C5A", "#FFF6D8")
        ic.path("M150 98 L104 190", stroke="#fff", stroke_width=1.6, opacity=0.9)
        ic.rect(54, 98, 132, 92, fill="none", stroke="#000", stroke_opacity=0.12)
        ic.text("-modulate 100,140,40", 56, 206, 8, font="mono-semibold", fill="#55534E")
    # sparkles where the magic went over it
    for x, y, r in ((146, 92, 7), (122, 128, 5), (100, 168, 6), (176, 132, 4)):
        ic.path(star(x, y, r, 0.28), fill="#FFE7A0")
    # the hat, leaning on the print's top
    hx, hy = 98, 104
    ic.ellipse(hx + 6, hy + 4, 58, 12, fill="#000", opacity=0.3)
    ic.path(f"M{hx - 62} {hy} C{hx - 42} {hy + 18} {hx + 46} {hy + 16} {hx + 64} {hy - 4} "
            f"C{hx + 42} {hy - 18} {hx - 42} {hy - 18} {hx - 62} {hy}z",
            fill=ic.lin([(0, "#5A2E9C"), (0.6, "#8A58D0"), (1, "#4A2488")], 0, 0, 0, 1))
    ic.path(f"M{hx - 56} {hy + 1} C{hx - 38} {hy + 15} {hx + 42} {hy + 13} {hx + 58} {hy - 3}", fill="none",
            stroke="#C9A8F2", stroke_opacity=0.6, stroke_width=1.5, stroke_linecap="round")
    cone = (f"M{hx - 36} {hy - 2} C{hx - 30} {hy - 40} {hx - 18} {hy - 70} {hx - 4} {hy - 82} "
            f"C{hx + 6} {hy - 90} {hx + 24} {hy - 84} {hx + 34} {hy - 74} "
            f"C{hx + 20} {hy - 74} {hx + 14} {hy - 66} {hx + 18} {hy - 50} "
            f"C{hx + 24} {hy - 30} {hx + 34} {hy - 14} {hx + 40} {hy - 2} "
            f"C{hx + 20} {hy + 6} {hx - 20} {hy + 6} {hx - 36} {hy - 2}z")
    ic.path(cone, fill=ic.lin([(0, "#9A64DE"), (0.5, "#6A38B0"), (1, "#2E1260")], 0, 0, 1, 0.3))
    ic.path(f"M{hx - 26} {hy - 10} C{hx - 20} {hy - 40} {hx - 12} {hy - 62} {hx - 2} {hy - 76}", fill="none",
            stroke="#fff", stroke_opacity=0.3, stroke_width=3, stroke_linecap="round")
    # the band, gold
    ic.path(f"M{hx - 35} {hy - 6} C{hx - 16} {hy + 2} {hx + 22} {hy + 2} {hx + 39} {hy - 6} l-2 -12 "
            f"C{hx + 20} {hy - 10} {hx - 14} {hy - 10} {hx - 32} {hy - 18}z", fill=brass(ic, 0, 0, 1, 0))
    # stars and a moon on the felt
    for x, y, r in ((hx - 12, hy - 34, 6), (hx + 16, hy - 32, 4.5), (hx - 2, hy - 58, 4), (hx - 22, hy - 22, 3)):
        ic.path(star(x, y, r, 0.42, 5), fill="#F5D46A")
    ic.path(f"M{hx + 8} {hy - 48} a7 7 0 1 0 6 10 a5.5 5.5 0 1 1 -6 -10z", fill="#F5D46A")


@small("imagemagick")
def imagemagick16(ic):
    tile(ic, "#6A3F9A", "#2C1556")
    ic.rect(4.5, 7.5, 10, 7, rx=0.4, fill="#FFFFFF")
    ic.rect(5.5, 8.5, 8, 5, fill="#7FB2D9")
    ic.path("M10.5 8.5 H13.5 V13.5 H8z", fill="#F28A3A")
    ic.path("M0.8 9.6 C2.6 10.8 9.4 10.8 11.2 9.2 C9.4 8.2 2.6 8.2 0.8 9.6z", fill="#8A58D0")
    ic.path("M2.6 9.2 C3.2 6 4.4 3 6.2 1.8 C7.4 1.4 8.6 2.2 9 3 C7.8 3.2 7.8 5 9.4 9.2 "
            "C7.2 9.9 4.6 9.9 2.6 9.2z", fill="#A06EE6")
    ic.path("M2.6 8.4 C4.6 9.2 7.6 9.2 9.4 8.4 L9.6 9.3 C7.6 10 4.6 10 2.5 9.3z", fill="#E8B84A")
    ic.circle(5.6, 5.6, 0.75, fill="#FFE07A")
