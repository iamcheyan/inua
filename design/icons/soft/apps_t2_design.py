"""The soft drawings of design and drafting: Scribus, Pencil2D, Synfig
Studio, FreeCAD, KiCad, LibreCAD, Sweet Home 3D. The same objects as
drawings/apps_t2_design.py, about half the detail, no text."""

from lib import bar, polar, soft, soft_shadow, tile, two

BRASS = ("#E2B45E", "#B88433")
STEEL = ("#AEB4BB", "#8D949C")


def _pts(points):
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in points) + "Z"


def _iso(ox, oy, k=1.0):
    def p(x, y, z=0):
        return (ox + (x - y) * 0.866 * k, oy + (x + y) * 0.5 * k - z * k)
    return p


def _pencil(ic, length, body=("#F6D06A", "#D9A02A"), band="#3F7FC0", eraser="#E88A8A"):
    """A pencil along the x axis, its point at 0: wood, lead, body,
    ferrule, eraser."""
    h = 9
    f0 = length - 22
    ic.path(f"M30 {-h} L0 0 L30 {h}z", fill="#EBCB98")
    ic.path("M0 0L10 -3V3z", fill="#2A2C30")
    ic.rect(30, -h, f0 - 30, 2 * h, fill=two(ic, *body))
    ic.rect(f0 - 5, -h, 5, 2 * h, fill=band)
    ic.rect(f0, -h - 0.5, 12, 2 * h + 1, fill=two(ic, *STEEL))
    ic.path(f"M{f0 + 12} {-h}h6a4 4 0 0 1 4 4v{2 * h - 8}a4 4 0 0 1-4 4h-6z", fill=eraser)


@soft("scribus")
def scribus(ic):
    tile(ic, "#4C6178", "#1E2A38")
    soft_shadow(ic, 124, 214, 98, 12)
    with ic.g(transform="rotate(-5 120 124)"):
        ic.rect(46, 34, 150, 182, rx=6, fill="#D9D3C6", transform="rotate(-4 120 124)")
        ic.rect(44, 30, 150, 182, rx=6, fill=two(ic, "#FFFFFF", "#ECE8DF"))
        ic.rect(56, 42, 126, 26, rx=4, fill="#2D4A7A")
        bar(ic, 64, 51, 56, 9, fill="#FFFFFF")
        ic.rect(56, 76, 68, 50, rx=4, fill=two(ic, "#F2B76A", "#D9663A"))
        ic.circle(108, 90, 7, fill="#FFE7B0")
        ic.path("M56 122 L76 100 L90 112 L104 96 L124 120 V122 a4 4 0 0 1 -4 4 H60 a4 4 0 0 1 -4-4z", fill="#3A4E6A")
        bar(ic, 132, 78, 50, 9, fill="#1E2A38")
        bar(ic, 132, 93, 44, 9, fill="#1E2A38")
        bar(ic, 132, 108, 34, 9, fill="#C8372D")
        ic.rect(56, 136, 14, 16, rx=3, fill="#2D4A7A")
        for i, y in enumerate(range(138, 204, 11)):
            x0 = 76 if y < 152 else 56
            bar(ic, x0, y, 114 - x0 if i != 5 else 30, 5, fill="#A49E91")
            bar(ic, 124, y, 58 if i not in (2, 5) else 34, 5, fill="#A49E91")
    with ic.g(transform="translate(120 190) rotate(-38) scale(0.8)"):
        barrel = two(ic, "#4A6CA4", "#1E3458")
        ic.path("M26 -7 H40 V7 H26 Q22 0 26 -7z", fill="#15181C")
        ic.path("M0 0 C6 -2 14 -8 28 -8 V8 C14 8 6 2 0 0z", fill=two(ic, *BRASS))
        ic.path("M40 -10 H120 V10 H40 Q34 6 34 0 Q34 -6 40 -10z", fill=barrel)
        ic.path("M126 -11 H182 a11 11 0 0 1 0 22 H126z", fill=barrel)
        ic.rect(118, -11.5, 9, 23, rx=2, fill=two(ic, *BRASS))
        ic.path("M134 -14 H180 a4 4 0 0 1 0 8 H140z", fill="#E2B45E")


@soft("pencil2d")
def pencil2d(ic):
    tile(ic, "#3E74AE", "#1A3762")
    soft_shadow(ic, 126, 212, 100, 12)
    for i, (dx, rot) in enumerate(((10, 6), (5, 3))):
        ic.rect(38 + dx, 52 + dx * 0.4, 162, 150, rx=6, fill="#E2DCCF" if i else "#D6CFC0",
                transform=f"rotate({rot} 40 200)")
    ic.rect(38, 52, 162, 150, rx=6, fill=two(ic, "#FBF6EA", "#EDE5D3"))
    ic.rect(28, 58, 20, 138, rx=6, fill=two(ic, "#3A3D42", "#1E2024"))
    bar(ic, 62, 66, 52, 8, fill="#1A3762", opacity=0.8)
    ic.line(60, 182, 192, 182, stroke="#5A5650", stroke_width=3, stroke_linecap="round")
    for cx, cy, col, op in ((74, 92, "#D9483B", 0.3), (92, 120, "#D9483B", 0.55),
                            (146, 144, "#2F6FCF", 0.5), (160, 120, "#2F6FCF", 0.3)):
        ic.circle(cx, cy, 12, fill="none", stroke=col, stroke_opacity=op, stroke_width=3)
    ic.ellipse(119, 170, 17, 11, fill="#F7D98A")
    ic.ellipse(119, 170, 17, 11, fill="none", stroke="#26282C", stroke_width=3.5)
    with ic.g(transform="translate(132 160) rotate(-40) scale(1.2)"):
        _pencil(ic, 112)


def _swirl(ic, cx, cy, r, fill="#fff", **kw):
    ic.path(f"M{cx - r:.1f} {cy:.1f}A{r} {r} 0 1 1 {cx + r * 0.2:.1f} {cy + r * 0.98:.1f}"
            f"C{cx - r * 0.5:.1f} {cy + r * 0.7:.1f} {cx - r * 0.55:.1f} {cy + r * 0.05:.1f} {cx:.1f} {cy - r * 0.15:.1f}"
            f"C{cx - r * 0.75:.1f} {cy - r * 0.2:.1f} {cx - r * 0.95:.1f} {cy + r * 0.3:.1f} {cx - r * 0.55:.1f} {cy + r * 0.85:.1f}"
            f"A{r} {r} 0 0 1 {cx - r:.1f} {cy:.1f}z", fill=fill, **kw)


@soft("synfig")
def synfig(ic):
    tile(ic, "#43384F", "#1A1422")
    soft_shadow(ic, 128, 216, 98, 12)
    cx, cy = 128, 120
    ic.rect(34, 30, 188, 184, rx=26, fill=two(ic, "#3E4249", "#24272C"))
    for k in range(11):
        a = -150 + k * 30
        x1, y1 = polar(cx, cy, 78, a)
        x2, y2 = polar(cx, cy, 68, a)
        ic.line(x1, y1, x2, y2, stroke="#C9CED4", stroke_opacity=0.7, stroke_width=3, stroke_linecap="round")
    for a, on in ((-150, False), (-100, True), (-36, True), (20, False), (88, True), (130, False)):
        x, y = polar(cx, cy, 88, a)
        ic.rect(x - 6, y - 6, 12, 12, rx=2.5, fill="#F08A24" if on else "#6A6473",
                transform=f"rotate(45 {x:.1f} {y:.1f})")
    ic.circle(cx, cy, 48, fill=two(ic, *STEEL))
    ic.circle(cx, cy, 37, fill=two(ic, "#FF9A3A", "#D85A12"))
    _swirl(ic, cx, cy, 23, fill="#FFF3DE")
    ic.circle(cx, cy - 1, 8, fill="#F8A040")
    x1, y1 = polar(cx, cy, 38, -36)
    x2, y2 = polar(cx, cy, 48, -36)
    ic.line(x1, y1, x2, y2, stroke="#1A1422", stroke_width=6, stroke_linecap="round")


@soft("freecad")
def freecad(ic):
    tile(ic, "#56687C", "#232D3A")
    soft_shadow(ic, 128, 214, 100, 12)
    with ic.g(transform="rotate(-3 128 128)"):
        ic.rect(28, 50, 200, 154, rx=6, fill=two(ic, "#FBF6EA", "#EDE5D3"))
        ic.rect(36, 58, 184, 138, rx=3, fill="none", stroke="#3D5A80", stroke_width=2.5)
        ic.rect(160, 174, 60, 22, rx=2, fill="none", stroke="#3D5A80", stroke_width=2.5)
        bar(ic, 166, 181, 34, 6, fill="#3D5A80")
        ic.rect(46, 150, 58, 32, fill="none", stroke="#2A3A52", stroke_width=2.5)
    p = _iso(124, 90, 1.0)
    W, D, H, S = 72, 56, 40, 20
    top = "#D3D8DD"
    left = "#A5ADB6"
    right = "#69727C"
    d2 = D * 0.5
    ic.path(_pts([p(0, D, 0), p(W, D, 0), p(W, D, S), p(0, D, S)]), fill=left)
    ic.path(_pts([p(W, 0, 0), p(W, D, 0), p(W, D, S), p(W, 0, S)]), fill=right)
    ic.path(_pts([p(0, d2, S), p(W, d2, S), p(W, D, S), p(0, D, S)]), fill=top)
    ic.path(_pts([p(0, d2, S), p(W, d2, S), p(W, d2, H + S), p(0, d2, H + S)]), fill=left)
    ic.path(_pts([p(W, 0, S), p(W, d2, S), p(W, d2, H + S), p(W, 0, H + S)]), fill=right)
    ic.path(_pts([p(0, 0, H + S), p(W, 0, H + S), p(W, d2, H + S), p(0, d2, H + S)]), fill=top)
    for (x, y, z, r) in ((W / 2, d2 / 2, H + S, 11), (W * 0.5, D * 0.76, S, 7)):
        hx, hy = p(x, y, z)
        ic.ellipse(hx, hy, r * 1.22, r * 0.71, fill="#3A4048")
    fx, fy = p(0, d2, H + S)
    with ic.g(transform=f"matrix(0.866 0.5 0 1 {fx:.1f} {fy:.1f})"):
        ic.rect(12, 5, 38, 30, rx=4, fill=two(ic, "#E8473A", "#B8241A"))
        ic.path("M21 9h20v6h-13v4h11v6h-11v8h-7z", fill="#fff")


@soft("kicad")
def kicad(ic):
    tile(ic, "#3448A0", "#141C48")
    soft_shadow(ic, 128, 214, 102, 12)
    ic.rect(26, 46, 204, 160, rx=12, fill="#123A1E")
    ic.rect(26, 42, 204, 158, rx=12, fill=two(ic, "#2E8A45", "#1A6232"))
    trace = dict(fill="none", stroke="#5FBF6E", stroke_width=5, stroke_linecap="round", stroke_linejoin="round",
                 opacity=0.7)
    for d in ("M98 100 H74 L62 112 V156", "M158 96 H184 L196 84 V64", "M120 138 V158 L134 172 H176"):
        ic.path(d, **trace)
    for x, y in ((62, 156), (196, 64), (176, 172)):
        ic.circle(x, y, 5.5, fill="#E3B65A")
    for x, y in ((42, 58), (214, 58), (42, 184), (214, 184)):
        ic.circle(x, y, 8, fill=two(ic, *BRASS))
        ic.circle(x, y, 4, fill="#0D1A10")
    for i in range(4):
        y = 80 + i * 15
        ic.rect(90, y, 10, 6, rx=1.5, fill="#C3C8CE")
        ic.rect(156, y, 10, 6, rx=1.5, fill="#C3C8CE")
    ic.rect(98, 70, 60, 68, rx=6, fill=two(ic, "#3A3D42", "#1E2024"))
    bar(ic, 108, 100, 40, 9, fill="#E9ECEF")
    ic.rect(48, 118, 26, 12, rx=6, fill=two(ic, "#E8D2A6", "#C4A672"))
    ic.rect(56, 118, 4, 12, fill="#C8372D")
    ic.circle(190, 136, 18, fill=two(ic, "#3E6FC0", "#1E4488"))
    ic.circle(190, 136, 10, fill="#D0D5DA")
    ic.circle(146, 174, 8.5, fill="#D8423A")
    ic.rect(54, 62, 36, 18, rx=9, fill=two(ic, *STEEL))


@soft("librecad")
def librecad(ic):
    tile(ic, "#3E6A5C", "#16342C")
    soft_shadow(ic, 128, 214, 102, 12)
    ic.rect(36, 40, 184, 168, rx=6, fill=two(ic, "#FFFFFF", "#ECE8DF"))
    for x, y, r in ((30, 36, -30), (210, 36, 30), (30, 200, 30), (210, 200, -30)):
        ic.rect(x, y, 24, 12, rx=2, fill="#EADFB8", transform=f"rotate({r} {x + 12} {y + 6})")
    ln = dict(fill="none", stroke="#2E3440", stroke_width=3.5, stroke_linejoin="round")
    ic.path("M58 72 H150 L170 92 V128 H58z", **ln)
    ic.circle(98, 100, 16, **ln)
    ic.line(70, 100, 126, 100, stroke="#C8372D", stroke_width=2, stroke_linecap="round")
    ic.line(98, 72, 98, 128, stroke="#C8372D", stroke_width=2, stroke_linecap="round")
    ic.line(58, 58, 170, 58, stroke="#3B7FD4", stroke_width=2.5, stroke_linecap="round")
    bar(ic, 58, 180, 52, 8, fill="#16342C", opacity=0.7)
    tri = "M134 146 L210 146 L210 46z"
    hole = "M154 139 L202 139 L202 76z"
    ic.path(tri + hole, fill="#4FA0E0", fill_opacity=0.6, fill_rule="evenodd", stroke="#2D74B4",
            stroke_width=2.5, stroke_linejoin="round")
    ic.rect(40, 146, 192, 18, fill="#EEF2F5")
    ic.rect(40, 146, 192, 4, fill="#C8372D")
    for k in range(0, 10):
        x = 50 + k * 19
        ic.line(x, 164, x, 157, stroke="#2E3440", stroke_width=2, stroke_linecap="round")
    ic.rect(20, 126, 26, 52, rx=5, fill=two(ic, "#D9A066", "#9C6634"))


@soft("sweethome3d")
def sweethome3d(ic):
    tile(ic, "#2F7C78", "#113C3C")
    soft_shadow(ic, 128, 214, 102, 12)
    with ic.g(transform="rotate(-4 128 140)"):
        ic.rect(26, 92, 204, 116, rx=6, fill=two(ic, "#FFFFFF", "#ECE8DF"))
        walls = dict(fill="none", stroke="#2E3440", stroke_width=6, stroke_linejoin="round", stroke_linecap="round")
        ic.path("M40 104 H216 V196 H40z", **walls)
        ic.path("M120 104 V146 M120 170 V196 M120 150 H156 M180 150 H216", **walls)
        ic.rect(140, 112, 30, 18, rx=4, fill="#E2DED4")
        bar(ic, 54, 182, 36, 7, fill="#2E3440", opacity=0.6)
    p = _iso(116, 104, 1.0)
    W, D, H, R = 84, 52, 34, 34
    ov = 6
    ic.path(_pts([p(0, D, 0), p(W, D, 0), p(W, D, H), p(0, D, H)]), fill=two(ic, "#FFFDF7", "#E8E0CF"))
    ic.path(_pts([p(W, 0, 0), p(W, D, 0), p(W, D, H), p(W, D / 2, H + R), p(W, 0, H)]), fill="#C9C0AC")

    def face_l(x0, z0, w, h, fill):
        ic.path(_pts([p(x0, D, z0), p(x0 + w, D, z0), p(x0 + w, D, z0 + h), p(x0, D, z0 + h)]), fill=fill)
    for x0 in (8, 56):
        face_l(x0, 12, 17, 14, "#6FA8D2")
    face_l(34, 0, 14, 24, "#9A5A32")
    ic.path(_pts([p(-ov, D / 2, H + R), p(W + ov, D / 2, H + R), p(W + ov, -ov, H - 4), p(-ov, -ov, H - 4)]),
            fill="#8E3214")
    ic.path(_pts([p(-ov, D / 2, H + R), p(W + ov, D / 2, H + R), p(W + ov, D + ov, H - 4), p(-ov, D + ov, H - 4)]),
            fill=two(ic, "#EE7448", "#C24A22"))
    ic.path(_pts([p(W + ov, D / 2, H + R), p(W + ov, D + ov, H - 4), p(W + ov, D + ov, H - 8),
                  p(W + ov, D / 2, H + R - 4)]), fill="#7A2A10")
    cx0, cy0 = 18, D / 2 + 6
    ztop, zb = H + R + 4, H + R - 8
    ic.path(_pts([p(cx0, cy0 + 8, zb), p(cx0 + 8, cy0 + 8, zb), p(cx0 + 8, cy0 + 8, ztop), p(cx0, cy0 + 8, ztop)]),
            fill="#E4DCCB")
    ic.path(_pts([p(cx0 + 8, cy0, zb), p(cx0 + 8, cy0 + 8, zb), p(cx0 + 8, cy0 + 8, ztop), p(cx0 + 8, cy0, ztop)]),
            fill="#B9AF9A")
    ic.path(_pts([p(cx0, cy0, ztop), p(cx0 + 8, cy0, ztop), p(cx0 + 8, cy0 + 8, ztop), p(cx0, cy0 + 8, ztop)]),
            fill="#5A5650")
