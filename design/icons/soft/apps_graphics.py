"""Soft drawings, graphics: GIMP, Inkscape, Krita, Blender, darktable,
Aseprite, LibreSprite, ImageMagick. The same objects as
drawings/apps_graphics.py, about half the detail, no text."""

import math

from lib import bar, polar, soft, soft_shadow, tile, two


def _pixels(ic, rows, x, y, s, colours):
    """Pixel art, each run of one colour in a row drawn as one rect."""
    for j, row in enumerate(rows):
        i = 0
        while i < len(row):
            c = colours.get(row[i])
            n = 1
            while i + n < len(row) and row[i + n] == row[i]:
                n += 1
            if c:
                ic.rect(x + i * s, y + j * s, n * s, s, fill=c)
            i += n


def _star(cx, cy, r, inner=0.38, n=4, turn=0):
    pts = [polar(cx, cy, r if k % 2 == 0 else r * inner, turn + k * 180 / n) for k in range(n * 2)]
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"


def _brush(ic, length, handle, w=10, paint="#E2702C", tip=30):
    """A round brush along the x axis, its point at 0: handle, ferrule,
    bristles with paint on them."""
    h = w / 2
    fe = tip + 22
    ic.rect(fe - 2, -h, length - fe + 2, w, rx=h, fill=handle)
    ic.rect(tip, -h + 0.5, fe - tip, w - 1, rx=2, fill=two(ic, "#D4D8DD", "#8D949C"))
    ic.path(f"M{tip + 1} {-h + 1}C{tip - 10} {-h - 1} 8 -3 0 0C8 3 {tip - 10} {h + 1} {tip + 1} {h - 1}z", fill="#3A2818")
    ic.path(f"M{tip * 0.6} {-h * 0.85}C{tip * 0.3} -3 6 -2 0 0C6 2 {tip * 0.3} 3.4 {tip * 0.6} {h * 0.85}z", fill=paint)


@soft("gimp")
def gimp(ic):
    tile(ic, "#7D705B", "#3B3328")
    soft_shadow(ic, 128, 218, 96, 11)
    ic.path("M124 30h10l6 186h-10z", fill="#4E3218")
    ic.path("M96 150L86 216h11l10-66z", fill="#9A6838")
    ic.path("M150 150l10 66h11l-10-66z", fill="#9A6838")
    # the canvas, its painting
    ic.rect(44, 40, 168, 122, rx=6, fill=two(ic, "#FCF9F2", "#E8E0CF"))
    ic.path("M50 150C70 120 120 96 206 104V150z", fill="#E8C68E", opacity=0.6)
    ic.circle(176, 70, 14, fill="#F2B45A", opacity=0.75)
    with ic.g(transform="translate(58 46) scale(1.12)"):
        body, dark = "#6F6552", "#3D362B"
        ic.path("M58 58L96 30", stroke="#B07A3A", stroke_width=6, stroke_linecap="round")
        ic.path("M95 28Q104 16 109 13Q107 22 100 32z", fill="#E2702C", stroke="#E2702C", stroke_width=3,
                stroke_linejoin="round")
        ic.path("M22 44C14 26 10 12 12 2C22 10 32 24 36 38z", fill=body)
        ic.path("M34 40C32 22 34 8 40 0C46 12 48 26 46 40z", fill=body)
        ic.path("M10 62C8 44 22 34 40 36C54 36 64 42 76 48C86 52 92 58 90 66C88 74 76 76 66 74"
                "C58 86 40 92 26 86C14 82 10 72 10 62z", fill=body)
        ic.ellipse(88, 60, 5, 4, fill=dark)
        for ex, ey, r in ((44, 40, 11), (62, 44, 9)):
            ic.circle(ex, ey, r + 2, fill=dark)
            ic.circle(ex, ey, r, fill="#FBF7EC")
            ic.circle(ex + r * 0.3, ey + r * 0.15, r * 0.45, fill="#1E1A14")
    # the ledge and a brush on it
    ic.rect(40, 160, 176, 14, rx=5, fill=two(ic, "#C48A55", "#8A5A2E"))
    with ic.g(transform="translate(54 156) rotate(-3)"):
        _brush(ic, 118, "#C67A32", paint="#E2702C", tip=26)


@soft("inkscape")
def inkscape(ic):
    tile(ic, "#4A5058", "#1B1E22")
    soft_shadow(ic, 124, 214, 100, 12)
    with ic.g(transform="rotate(-4 124 128)"):
        ic.rect(34, 40, 176, 168, rx=8, fill=two(ic, "#FFFFFF", "#ECE8DF"))
        bar(ic, 46, 52, 54, 8, fill="#2B2E33", opacity=0.7)
        bar(ic, 46, 64, 36, 6, fill="#9A9EA4")
        # the mark: a black mountain, its snow running down
        ic.path("M52 178L104 92Q116 74 128 92L184 178Q186 184 180 184L56 184Q50 184 52 178z", fill="#16181B")
        ic.path("M92 112L104 92Q116 74 128 92L140 112Q136 122 130 116Q126 132 120 118Q114 140 108 120"
                "Q102 128 98 116Q94 122 92 112z", fill="#FFFFFF")
        ic.path("M108 120Q110 134 112 146Q114 152 116 146Q117 134 118 120", fill="#fff")
        # a node with its handle, the corners selected
        ic.line(84, 112, 128, 70, stroke="#3B7FD4", stroke_width=2.5)
        for x, y in ((84, 112), (128, 70)):
            ic.circle(x, y, 5, fill="#fff", stroke="#3B7FD4", stroke_width=2.5)
        ic.rect(100, 86, 10, 10, rx=2, fill="#3B7FD4", stroke="#fff", stroke_width=1.5)
        for x, y in ((52, 178), (184, 178)):
            ic.rect(x - 5, y - 5, 10, 10, rx=2, fill="#fff", stroke="#16181B", stroke_width=2)
    # the dip pen
    with ic.g(transform="translate(150 160) rotate(38)"):
        ic.path("M-12-136a12 12 0 0 1 24 0V-96C12-88 10-84 9-78H-9C-10-84-12-88-12-96z",
                fill=two(ic, "#3A3E45", "#141518"))
        ic.rect(-11, -100, 22, 10, rx=3, fill=two(ic, "#E2B45E", "#B88433"))
        ic.path("M0 0C3-14 10-40 11-60L11-80L-11-80L-11-60C-10-40-3-14 0 0z", fill=two(ic, "#E4E8EC", "#9AA1A9"))
        ic.line(0, -6, 0, -42, stroke="#2A2E33", stroke_width=2, stroke_linecap="round")
        ic.circle(0, -46, 4, fill="#2A2E33")


@soft("krita")
def krita(ic):
    tile(ic, "#3B5C9A", "#1A2B52")
    soft_shadow(ic, 128, 210, 104, 12)
    pal = ("M30 118C26 70 80 40 140 44C196 48 232 86 226 132C220 176 172 200 124 196"
           "C104 194 100 178 86 176C70 174 66 194 50 186C34 178 32 150 30 118z")
    ic.path(pal, fill="#8A5424", transform="translate(0 5)")
    ic.path(pal, fill=two(ic, "#E8BA84", "#BE8448"))
    ic.ellipse(70, 140, 13, 11, fill="#2A1A0C")
    for x, y, r, c in ((96, 76, 15, "#E8407A"), (134, 66, 13, "#3BA3E8"), (172, 76, 13, "#F6F2EA"),
                       (198, 104, 12, "#F5C04A"), (200, 140, 12, "#8A4FD8"), (176, 168, 11, "#3FC4B0")):
        ic.ellipse(x, y, r, r * 0.85, fill=c)
    # pink and blue, being mixed
    ic.path("M100 120C118 104 146 104 160 116C150 126 128 130 112 134C104 134 98 128 100 120z", fill="#E8407A")
    ic.path("M128 128C142 118 156 116 168 124C160 134 146 138 132 138z", fill="#6C7BE0")
    with ic.g(transform="translate(104 128) rotate(32)"):
        _brush(ic, 150, two(ic, "#FF7AA8", "#C42E64"), w=12, paint="#E8407A", tip=30)


def _blender_mark(ic, cx, cy, r):
    ic.path(f"M{cx - r * 0.6} {cy + r * 0.2}L{cx - r * 2} {cy + r * 1.1}L{cx - r * 2.05} {cy + r * 0.55}"
            f"L{cx - r * 1.3} {cy + r * 0.05}L{cx - r * 2.2} {cy + r * 0.05}L{cx - r * 2.2} {cy - r * 0.45}"
            f"L{cx - r * 0.7} {cy - r * 0.5}z", fill="#F07C1A")
    ic.circle(cx, cy, r, fill="#F07C1A")
    ic.circle(cx, cy, r * 0.66, fill="#FFFFFF")
    ic.circle(cx, cy, r * 0.38, fill="#2B6BC2")


@soft("blender")
def blender(ic):
    tile(ic, "#3D6EA8", "#16335A")
    soft_shadow(ic, 128, 214, 100, 12)
    cx, top = 128, 166
    # the turntable
    ic.path(f"M30 {top}v22a98 22 0 0 0 196 0v-22z", fill=two(ic, "#3A3E44", "#1A1B1E"))
    ic.ellipse(cx, top, 98, 22, fill=two(ic, "#6B7078", "#454950"))
    ic.ellipse(cx, top, 86, 18.5, fill="#3E4248")
    with ic.g(clip_path=ic.clip(f'<ellipse cx="{cx}" cy="{top}" rx="86" ry="18.5"/>')):
        ic.line(cx - 80, top + 20, cx + 80, top - 20, stroke="#E0484A", stroke_width=3)
        ic.line(cx - 80, top - 20, cx + 80, top + 20, stroke="#7CC04A", stroke_width=3)
    # the badge on its front
    ic.rect(cx - 30, top + 21, 60, 17, rx=8.5, fill="#16181B")
    _blender_mark(ic, cx - 14, top + 29.5, 5.5)
    bar(ic, cx - 2, top + 26.5, 24, 6, fill="#F1F1EF")
    # the default cube, selected
    s = 46
    p0 = (cx, top - 2)
    l, r = (cx - s * 0.95, top - 2 - s * 0.48), (cx + s * 0.95, top - 2 - s * 0.48)
    up = s * 1.15
    b = (cx, top - 2 - s * 0.96)

    def T(p):
        return (p[0], p[1] - up)
    ic.poly([l, p0, T(p0), T(l)], fill="#A9AEB4")
    ic.poly([p0, r, T(r), T(p0)], fill="#71767D")
    ic.poly([T(l), T(p0), T(r), T(b)], fill="#DCDFE2")
    ic.poly([l, p0, r, T(r), T(b), T(l)], fill="none", stroke="#F59A2A", stroke_width=5, stroke_linejoin="round")
    ic.circle(cx, top - 2 - s * 0.48 - up / 2, 4.5, fill="#F59A2A")


@soft("darktable")
def darktable(ic):
    tile(ic, "#4A2226", "#14080A")
    soft_shadow(ic, 128, 216, 96, 12)
    # a strip of negatives behind
    with ic.g(transform="rotate(-14 128 128)"):
        ic.rect(8, 150, 240, 50, rx=3, fill=two(ic, "#D8823A", "#A8561E"))
        for x in range(12, 244, 14):
            ic.rect(x, 153, 7, 6, rx=2, fill="#2A1208")
            ic.rect(x, 191, 7, 6, rx=2, fill="#2A1208")
        for x in (14, 84, 154, 224):
            ic.rect(x, 163, 62, 25, rx=3, fill="#3A2A30", opacity=0.55)
    cx, cy = 128, 108
    # the lens
    ic.circle(cx, cy, 86, fill=two(ic, "#4A4E55", "#16171A"))
    ic.circle(cx, cy, 78, fill="#1C1E21")
    with ic.g(fill="none", stroke="#E9E6DF", stroke_width=6, stroke_linecap="round"):
        for a1, a2 in ((-66, -12), (18, 40), (52, 74)):
            p, q = polar(cx, cy, 69, a1), polar(cx, cy, 69, a2)
            ic.path(f"M{p[0]:.1f} {p[1]:.1f}A69 69 0 0 1 {q[0]:.1f} {q[1]:.1f}", stroke_opacity=0.85 if a1 < 0 else 0.5)
    ic.path(f"M{cx} {cy - 74}l-5 -8h10z", fill="#E0484A")
    ic.circle(cx, cy, 60, fill="#060607")
    # the iris, stopped down
    R, ro, n, turn = 56, 22, 7, 12
    with ic.g(clip_path=ic.clip(f'<circle cx="{cx}" cy="{cy}" r="{R}"/>')):
        ic.circle(cx, cy, R, fill="#2C2F34")
        corners = [polar(cx, cy, ro, turn + k * 360 / n) for k in range(n)]
        for k in range(n):
            ax, ay = corners[k]
            bx, by = corners[(k + 1) % n]
            m = math.hypot(bx - ax, by - ay)
            ex, ey = ax + (bx - ax) / m * 90, ay + (by - ay) / m * 90
            ic.poly([(ax, ay), (ex, ey), polar(cx, cy, 120, turn + k * 360 / n + 70)],
                    fill="#fff", opacity=0.04 + 0.06 * (k % 2))
            ic.line(ax, ay, ex, ey, stroke="#0B0C0E", stroke_width=2.5)
    ic.poly([polar(cx, cy, ro, turn + k * 360 / n) for k in range(n)], fill=two(ic, "#E0484A", "#8A1A1C"))


SPRITE = [
    "..............",
    "..K........K..",
    ".KOK......KOK.",
    ".KOPK....KPOK.",
    ".KOOOKKKKOOOK.",
    "KOOOOOOOOOOODK",
    "KOOOOOOOOOOODK",
    "KOOKWOOOOKWODK",
    "KOOKKOOOOKKODK",
    "KORROOKKOORRDK",
    "KOOOOOOOOOODDK",
    ".KOOOOOOOOODK.",
    "..KKDDDDDDKK..",
    "....KKKKKK....",
]


@soft("aseprite")
def aseprite(ic):
    tile(ic, "#3F8C95", "#163F48")
    soft_shadow(ic, 128, 214, 98, 12)
    ic.rect(34, 28, 188, 182, rx=18, fill=two(ic, "#3E4459", "#22253A"))
    bar(ic, 46, 36, 48, 7, fill="#C9D3E8", opacity=0.6)
    s, x0, y0 = 10, 58, 50
    ic.rect(x0, y0, 140, 140, rx=4, fill="#D9DCE3")
    _pixels(ic, SPRITE, x0, y0, s, {"K": "#1E2032", "O": "#F2A03A", "D": "#C4661C",
                                    "W": "#FFFFFF", "P": "#F07A9A", "R": "#F07A6A"})
    ic.rect(x0 + 12 * s - 1.5, y0 + s - 1.5, s + 3, s + 3, rx=2, fill="#F2A03A", stroke="#fff", stroke_width=2.5)
    for i, c in enumerate(("#1E2032", "#FFFFFF", "#F2A03A", "#C4661C", "#F07A6A", "#5FBF6A")):
        ic.rect(60 + i * 23, 196, 18, 9, rx=3, fill=c)


def _pixel_pencil(tip, end, w=2.7):
    """The cells of a pixel-art pencil from its tip to its eraser: {(i, j): part}."""
    (tx, ty), (ex, ey) = tip, end
    n = math.hypot(ex - tx, ey - ty)
    dx, dy = (ex - tx) / n, (ey - ty) / n
    nx, ny = dy, -dx
    if nx > 0 or ny > 0:
        nx, ny = -nx, -ny
    cells = {}
    for j in range(32):
        for i in range(32):
            cx, cy = i + 0.5 - tx, j + 0.5 - ty
            u, v = cx * dx + cy * dy, cx * nx + cy * ny
            if u < -0.6 or u > n + 0.8:
                continue
            prof = w * min(1, max(u, 0) / 6)
            if abs(v) > prof + 0.9 or (u > n and abs(v) > prof):
                continue
            if abs(v) > prof or u > n:
                cells[(i, j)] = "L"
            elif u < 2.4:
                cells[(i, j)] = "G"
            elif u < 6:
                cells[(i, j)] = "W"
            elif u < n - 6:
                cells[(i, j)] = "S" if v < -0.9 else "Y"
            elif u < n - 3.4:
                cells[(i, j)] = "M"
            else:
                cells[(i, j)] = "R"
    return cells


@soft("libresprite")
def libresprite(ic):
    tile(ic, "#5E8C3E", "#25461A")
    with ic.g(transform="rotate(-45 150 168)"):
        soft_shadow(ic, 150, 168, 104, 16)
    s = 8
    trail = [(7, 25), (6, 26), (6, 27), (7, 28), (8, 28), (9, 27), (10, 26), (11, 26), (12, 27), (13, 28),
             (14, 28), (15, 27), (16, 26), (17, 26), (18, 27)]
    for i, j in trail:
        ic.rect(i * s, j * s, s, s, fill="#9A46B8")
    cells = _pixel_pencil((8.6, 23.4), (25.4, 6.6))
    rows = [["."] * 32 for _ in range(32)]
    for (i, j), part in cells.items():
        rows[j][i] = part
    _pixels(ic, ["".join(r) for r in rows], 0, 0, s,
            {"L": "#24203A", "G": "#3A3650", "W": "#EAC08A", "Y": "#F5B82E", "S": "#D48A1A",
             "M": "#AEB4BB", "R": "#E25A80"})


def _scene(ic, sky, hill, far, sun):
    ic.rect(54, 98, 132, 92, fill=two(ic, *sky))
    ic.circle(158, 120, 10, fill=sun)
    ic.path("M54 160L84 132L104 148L126 124L160 154L186 140V170H54z", fill=far)
    ic.path("M54 170Q90 150 128 164T186 160V190H54z", fill=hill)


@soft("imagemagick")
def imagemagick(ic):
    tile(ic, "#6A3F9A", "#2C1556")
    soft_shadow(ic, 128, 218, 98, 11)
    with ic.g(transform="rotate(5 120 144)"):
        ic.rect(44, 88, 152, 128, rx=7, fill=two(ic, "#FFFFFF", "#ECE8DF"))
        with ic.g(clip_path=ic.clip('<rect x="54" y="98" width="132" height="92" rx="3"/>')):
            _scene(ic, ("#7FB2D9", "#E2EEF2"), "#3E7A46", "#6F8296", "#FFF2C0")
            with ic.g(clip_path=ic.clip('<path d="M150 98L186 98L186 190L104 190z"/>')):
                _scene(ic, ("#F28A3A", "#FCD6A0"), "#5A2A6E", "#B4487A", "#FFF6D8")
            ic.path("M150 98L104 190", stroke="#fff", stroke_width=3)
        bar(ic, 56, 199, 80, 7, fill="#8C887F")
    for x, y, r in ((148, 90, 10), (100, 168, 8), (178, 132, 7)):
        ic.path(_star(x, y, r, 0.32), fill="#FFE7A0", stroke="#FFE7A0", stroke_width=1.5, stroke_linejoin="round")
    # the hat
    hx, hy = 98, 104
    ic.path(f"M{hx - 62} {hy}C{hx - 42} {hy + 18} {hx + 46} {hy + 16} {hx + 64} {hy - 4}"
            f"C{hx + 42} {hy - 18} {hx - 42} {hy - 18} {hx - 62} {hy}z", fill=two(ic, "#8A58D0", "#4A2488"))
    ic.path(f"M{hx - 36} {hy - 2}C{hx - 30} {hy - 40} {hx - 18} {hy - 70} {hx - 4} {hy - 82}"
            f"C{hx + 6} {hy - 90} {hx + 24} {hy - 84} {hx + 34} {hy - 74}"
            f"C{hx + 20} {hy - 74} {hx + 14} {hy - 66} {hx + 18} {hy - 50}"
            f"C{hx + 24} {hy - 30} {hx + 34} {hy - 14} {hx + 40} {hy - 2}"
            f"C{hx + 20} {hy + 6} {hx - 20} {hy + 6} {hx - 36} {hy - 2}z", fill=two(ic, "#9A64DE", "#5A2A9E"))
    ic.path(f"M{hx - 35} {hy - 6}C{hx - 16} {hy + 2} {hx + 22} {hy + 2} {hx + 39} {hy - 6}l-2 -12"
            f"C{hx + 20} {hy - 10} {hx - 14} {hy - 10} {hx - 32} {hy - 18}z", fill=two(ic, "#E2B45E", "#B88433"))
    for x, y, r in ((hx - 10, hy - 36, 7), (hx + 14, hy - 30, 5)):
        ic.path(_star(x, y, r, 0.45, 5), fill="#F5D46A", stroke="#F5D46A", stroke_width=1.5, stroke_linejoin="round")
    ic.path(f"M{hx + 4} {hy - 60}a8 8 0 1 0 7 11a6 6 0 1 1 -7 -11z", fill="#F5D46A")
