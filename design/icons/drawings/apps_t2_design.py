"""The inua-objects theme, design and drafting: Scribus, Pencil2D, Synfig
Studio, FreeCAD, KiCad, LibreCAD, Sweet Home 3D (docs/feat/object-icons.md,
Part 2, tier 2). Each is the app's job as an object on the desk in its
brand's colours, its mark redrawn as a stamp, an enamel cap or a badge."""

from lib import (brass, glare, graphite, icon, paper, polar, shadow, small, steel, tile, wood)


def _pts(points):
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in points) + "Z"


def _iso(ox, oy, k=1.0):
    """An isometric projection from (ox, oy): x runs down to the right, y
    down to the left, z up; k px a unit."""
    def p(x, y, z=0):
        return (ox + (x - y) * 0.866 * k, oy + (x + y) * 0.5 * k - z * k)
    return p


def _pencil(ic, length, body="#F2C14E", body_dark="#C98A1E", band="#3F7FC0", eraser="#E88A8A", top="#FFE39A"):
    """A hexagonal pencil along the x axis, its point at 0, its end at
    length; drawn in place (wrap in a transform)."""
    h = 8
    cone = 30
    ic.path(f"M{cone} {-h}L{length - 22} {-h}V{h}L{cone} {h}z", fill="#000", opacity=0.25,
            transform="translate(5 7)")
    # the body, three facets
    ic.rect(cone, -h, length - 22 - cone, h * 2 / 3, fill=ic.lin([(0, top), (1, body)]))
    ic.rect(cone, -h / 3, length - 22 - cone, h * 2 / 3, fill=body)
    ic.rect(cone, h / 3, length - 22 - cone, h * 2 / 3, fill=body_dark)
    ic.line(cone, -h + 1, length - 22, -h + 1, stroke="#fff", stroke_opacity=0.55, stroke_width=1.2)
    # the sharpened wood and the lead
    ic.path(f"M{cone} {-h}Q{cone - 6} {-h + 2} 0 0Q{cone - 6} {h - 2} {cone} {h}"
            f"Q{cone - 3} {h / 3} {cone} {h / 3}Q{cone - 3} {-h / 3} {cone} {-h / 3}Q{cone - 3} {-h + 2} {cone} {-h}z",
            fill=ic.lin([(0, "#F3D7A8"), (1, "#C99A62")]))
    ic.path("M0 0L9 -2.8Q10 0 9 2.8z", fill="#2A2C30")
    # the ferrule and the eraser
    f0 = length - 22
    ic.rect(f0, -h - 0.5, 12, h * 2 + 1, fill=steel(ic, horizontal=False))
    for x in (f0 + 3, f0 + 6, f0 + 9):
        ic.line(x, -h, x, h, stroke="#4D535A", stroke_opacity=0.5, stroke_width=0.8)
    ic.rect(f0 - 5, -h, 5, h * 2, fill=band)
    ic.path(f"M{f0 + 12} {-h + 0.5}h7a3 3 0 0 1 3 3v{h * 2 - 7}a3 3 0 0 1-3 3h-7z",
            fill=ic.lin([(0, "#F6B3B0"), (1, eraser)]))


# --- Scribus: a typeset magazine page under a fountain pen -------------------

@icon("scribus", kind="app", names=["net.scribus.Scribus", "scribus", "scribus-ng", "scribus-trunk"],
      title="Scribus")
def scribus(ic):
    tile(ic, "#4C6178", "#1E2A38")
    shadow(ic, 124, 214, 98, 12)
    with ic.g(transform="rotate(-5 120 124)"):
        # a page underneath, then the spread's right page
        ic.rect(46, 34, 150, 182, rx=2, fill="#D9D3C6", transform="rotate(-4 120 124)")
        ic.rect(44, 30, 150, 182, rx=2, fill="#000", opacity=0.28, transform="translate(3 4)")
        ic.rect(44, 30, 150, 182, rx=2, fill=paper(ic, "white"))
        ic.line(45, 31, 193, 31, stroke="#fff", stroke_width=1.5)
        # the masthead
        ic.rect(56, 42, 126, 26, fill="#2D4A7A")
        ic.text("FOLIO", 62, 63, 22, font="sans-bold", spacing=1.5, fill="#FFFFFF")
        ic.text("No. 14", 176, 52, 6, font="mono-semibold", anchor="end", fill="#C9D6EA")
        ic.text("AUTUMN", 176, 62, 6, font="mono", anchor="end", spacing=0.6, fill="#C9D6EA")
        # the picture
        ic.rect(56, 74, 70, 52, fill=ic.lin([(0, "#F2B76A"), (1, "#D9663A")]))
        ic.circle(108, 88, 7, fill="#FFE7B0")
        ic.path("M56 126 L76 100 L90 112 L104 96 L126 126z", fill="#3A4E6A")
        ic.path("M56 126 L76 100 L84 108 L70 126z", fill="#4F6A8C")
        # the headline and the columns, the first with a drop cap
        ic.text("Setting", 132, 84, 13, font="sans-bold", fill="#1E2A38")
        ic.text("type by", 132, 97, 13, font="sans-bold", fill="#1E2A38")
        ic.text("hand", 132, 110, 13, font="sans-bold", fill="#C8372D")
        for y in (117, 122):
            ic.rect(132, y, 50, 2, fill="#9A968D")
        ic.text("T", 56, 148, 22, font="sans-bold", fill="#2D4A7A")
        for i, y in enumerate(range(134, 202, 6)):
            x0 = 72 if y < 152 else 56
            w = 60 - x0 + 56 if i != 10 else 30
            ic.rect(x0, y, w, 2.2, fill="#8C887F")
        for i, y in enumerate(range(134, 202, 6)):
            ic.rect(122, y, 60 if i not in (5, 11) else 34, 2.2, fill="#8C887F")
        # the frame guides, as on screen
        ic.rect(52, 38, 134, 166, fill="none", stroke="#3BA5D8", stroke_opacity=0.55, stroke_width=0.9,
                stroke_dasharray="3 2")
        ic.line(119, 128, 119, 204, stroke="#3BA5D8", stroke_opacity=0.55, stroke_width=0.9,
                stroke_dasharray="3 2")
        ic.text("14", 186, 208, 6, font="mono", anchor="end", fill="#8C887F")
    # the fountain pen, its nib down at the lower left
    with ic.g(transform="translate(120 190) rotate(-38) scale(0.8)"):
        ic.path("M28 -9 H186 a9 9 0 0 1 0 18 H28z", fill="#000", opacity=0.3, transform="translate(4 10)")
        barrel = ic.lin([(0, "#5B7BB0"), (0.35, "#2D4A7A"), (1, "#101C30")], 0, 0, 0, 1)
        ic.path("M40 -9 H120 V9 H40 Q34 6 34 0 Q34 -6 40 -9z", fill=barrel)
        ic.path("M124 -10 H184 a10 10 0 0 1 0 20 H124z", fill=barrel)
        ic.line(126, -6.5, 186, -6.5, stroke="#fff", stroke_opacity=0.35, stroke_width=2, stroke_linecap="round")
        ic.line(42, -6, 118, -6, stroke="#fff", stroke_opacity=0.3, stroke_width=1.6, stroke_linecap="round")
        ic.rect(118, -10.5, 8, 21, rx=1, fill=brass(ic, 0, 0, 0, 1))
        # the clip
        ic.path("M134 -12 H182 a3 3 0 0 1 0 6 H140z", fill=brass(ic, 0, 0, 0, 1))
        ic.circle(180, -9, 2.4, fill="#F6DDA0")
        # the section and the nib, the mark's split nib engraved
        ic.path("M24 -6 H40 V6 H24 Q20 0 24 -6z", fill="#15181C")
        nib = ic.lin([(0, "#F4E2B0"), (0.5, "#C99645"), (1, "#7E5A20")], 0, 0, 0, 1)
        ic.path("M0 0 C6 -2 14 -7 26 -7 V7 C14 7 6 2 0 0z", fill=nib)
        ic.line(1, 0, 15, 0, stroke="#4A3410", stroke_width=0.9)
        ic.circle(16, 0, 1.6, fill="#4A3410")
        ic.path("M6 -1.5 C10 -3 15 -5 22 -5.4", fill="none", stroke="#fff", stroke_opacity=0.6, stroke_width=0.8)
        ic.text("Scribus", 154, 4, 7, font="sans-semibold", anchor="middle", spacing=0.6, fill="#C9D6EA",
                opacity=0.85)


@small("scribus")
def scribus16(ic):
    tile(ic, "#4C6178", "#1E2A38")
    ic.rect(3, 2, 9.5, 12, rx=0.4, fill="#FFFFFF")
    ic.rect(4, 3, 7.5, 2, fill="#2D4A7A")
    ic.rect(4, 6, 4, 3, fill="#E08A4A")
    for y in (10, 11.5):
        ic.rect(4, y, 7.5, 0.6, fill="#8C887F")
    ic.path("M7.5 13.2 L14 6.7 L15 7.7 L8.5 14.2z", fill="#2D4A7A")
    ic.path("M7.5 13.2 L6.4 14.6 L8.5 14.2z", fill="#C99645")


# --- Pencil2D: a pencil over a flip-book, a ball bouncing in onion skins -----

@icon("pencil2d", kind="app", names=["org.pencil2d.Pencil2D", "pencil2d"], title="Pencil2D")
def pencil2d(ic):
    tile(ic, "#3E74AE", "#1A3762")
    shadow(ic, 126, 212, 100, 12)
    # the pages, fanned at the far corner as if thumbed
    for i, (dx, rot) in enumerate(((10, 7), (7, 4.5), (4, 2.2), (2, 1))):
        ic.rect(38 + dx, 52 + dx * 0.4, 162, 150, rx=3, fill="#E2DCCF" if i % 2 else "#EEE9DE",
                stroke="#000", stroke_opacity=0.08, transform=f"rotate({rot} 40 200)")
    ic.rect(38, 52, 162, 150, rx=3, fill="#000", opacity=0.25, transform="translate(3 4)")
    ic.rect(38, 52, 162, 150, rx=3, fill=paper(ic, "cream"))
    ic.line(39, 53, 199, 53, stroke="#fff", stroke_width=1.5)
    # the binding: a black clip along the left
    ic.rect(30, 60, 18, 134, rx=4, fill=graphite(ic))
    ic.line(33, 64, 33, 190, stroke="#fff", stroke_opacity=0.18, stroke_width=1.5)
    for y in (78, 128, 176):
        ic.rect(44, y - 5, 10, 10, rx=2, fill=steel(ic, horizontal=False))
    # the frame: a ball's arc, earlier frames in red, later in blue
    ic.path("M66 92 Q86 76 104 168 Q126 100 148 168 Q166 128 186 150", fill="none", stroke="#8C887F",
            stroke_opacity=0.5, stroke_width=1, stroke_dasharray="2 3")
    ic.line(60, 180, 192, 180, stroke="#5A5650", stroke_width=1.6, stroke_linecap="round")
    for cx, cy, col, op in ((72, 88, "#D9483B", 0.25), (88, 108, "#D9483B", 0.4), (98, 140, "#D9483B", 0.6),
                            (140, 148, "#2F6FCF", 0.45), (154, 126, "#2F6FCF", 0.25)):
        ic.circle(cx, cy, 11, fill="none", stroke=col, stroke_opacity=op, stroke_width=1.6)
    # the current frame, squashed on the ground
    ic.ellipse(119, 170, 16, 10, fill="#F2C14E", opacity=0.35)
    ic.ellipse(119, 170, 16, 10, fill="none", stroke="#26282C", stroke_width=2.2)
    ic.path("M108 166 Q112 162 118 162", fill="none", stroke="#26282C", stroke_width=1.4, stroke_linecap="round")
    ic.text("12", 190, 196, 10, font="hand", anchor="end", fill="#5A5650")
    ic.text("Pencil2D", 60, 70, 9, font="sans-semibold", fill="#1A3762", opacity=0.8)
    ic.text("bounce · 24 fps", 60, 80, 6, font="mono", fill="#8C887F")
    # the pencil, its point on the ball
    with ic.g(transform="translate(130 160) rotate(-40) scale(1.2)"):
        _pencil(ic, 112)


@small("pencil2d")
def pencil2d16(ic):
    tile(ic, "#3E74AE", "#1A3762")
    ic.rect(3.5, 3.5, 10.5, 9.5, rx=0.4, fill="#D9D3C6")
    ic.rect(2.5, 3, 10.5, 9.5, rx=0.4, fill="#F6F1E6")
    ic.rect(2, 3.5, 1.4, 8.5, fill="#2A2C30")
    ic.circle(6, 7, 1.6, fill="none", stroke="#D9483B", stroke_width=0.8, opacity=0.7)
    ic.ellipse(8.2, 10.2, 1.8, 1.2, fill="#26282C")
    ic.path("M9 9.6 L14.2 4 L15.4 5.2 L10.2 10.6z", fill="#F2C14E")
    ic.path("M9 9.6 L8.4 11.2 L10.2 10.6z", fill="#2A2C30")


# --- Synfig Studio: a keyframe dial, Synfig's orange swirl on its cap ---------

def _swirl(ic, cx, cy, r, fill="#fff", **kw):
    """Synfig's mark, redrawn: a disc trailing a comet's swirl."""
    ic.path(f"M{cx - r:.1f} {cy:.1f}A{r} {r} 0 1 1 {cx + r * 0.2:.1f} {cy + r * 0.98:.1f}"
            f"C{cx - r * 0.5:.1f} {cy + r * 0.7:.1f} {cx - r * 0.55:.1f} {cy + r * 0.05:.1f} {cx:.1f} {cy - r * 0.15:.1f}"
            f"C{cx - r * 0.75:.1f} {cy - r * 0.2:.1f} {cx - r * 0.95:.1f} {cy + r * 0.3:.1f} {cx - r * 0.55:.1f} {cy + r * 0.85:.1f}"
            f"A{r} {r} 0 0 1 {cx - r:.1f} {cy:.1f}z", fill=fill, **kw)


@icon("synfig", kind="app", names=["appimagekit-synfigstudio", "org.synfig.SynfigStudio", "synfig", "synfig_icon",
                                   "synfigstudio"], title="Synfig Studio")
def synfig(ic):
    tile(ic, "#43384F", "#1A1422")
    shadow(ic, 128, 216, 98, 12)
    cx, cy = 128, 120
    # the plate it is set in
    ic.rect(34, 30, 188, 184, rx=22, fill="#0E0B12", opacity=0.6, transform="translate(2 4)")
    ic.rect(34, 30, 188, 184, rx=22, fill=graphite(ic))
    ic.rect(34.75, 30.75, 186.5, 182.5, rx=21.25, fill="none", stroke="#fff", stroke_opacity=0.14,
            stroke_width=1.5)
    for x, y in ((46, 42), (210, 42), (46, 202), (210, 202)):
        ic.circle(x, y, 4, fill=steel(ic, horizontal=False))
        ic.line(x - 2.5, y + 1, x + 2.5, y - 1, stroke="#3A3F46", stroke_width=1)
    # the scale: frames round the dial, keyframes as diamonds
    ic.circle(cx, cy, 82, fill="none", stroke="#000", stroke_opacity=0.35, stroke_width=1.5)
    for k in range(48):
        a = -150 + k * 300 / 47
        x1, y1 = polar(cx, cy, 80, a)
        x2, y2 = polar(cx, cy, 74 if k % 4 else 70, a)
        ic.line(x1, y1, x2, y2, stroke="#C9CED4", stroke_opacity=0.75, stroke_width=1.1 if k % 4 else 1.6)
    for n, a in (("0", -150), ("12", -75), ("24", 0), ("36", 75), ("48", 150)):
        x, y = polar(cx, cy, 62, a)
        ic.text(n, x, y + 3, 8, font="mono-semibold", anchor="middle", fill="#C9CED4", opacity=0.8)
    for a, on in ((-150, False), (-100, True), (-36, True), (20, False), (88, True), (130, False)):
        x, y = polar(cx, cy, 88, a)
        ic.path(f"M{x:.1f} {y - 6:.1f}l6 6-6 6-6-6z", fill="#F08A24" if on else "#5A5463",
                stroke="#1A1422", stroke_width=1)
        if on:
            ic.path(f"M{x - 2:.1f} {y - 2.5:.1f}l2-2 2 2", fill="none", stroke="#fff", stroke_opacity=0.6,
                    stroke_width=0.8)
    ic.text("KEYFRAME", cx, 196, 7, font="mono-semibold", anchor="middle", spacing=2, fill="#C9CED4", opacity=0.6)
    # the knob: a knurled steel ring, then the orange enamel cap
    ic.circle(cx + 3, cy + 6, 46, fill="#000", opacity=0.45)
    ic.circle(cx, cy, 46, fill=ic.lin([(0, "#E6E9EC"), (0.5, "#8E959D"), (1, "#3E444B")], 0, 0, 1, 1))
    ic.circle(cx, cy, 44, fill="none", stroke="#2A2E33", stroke_opacity=0.5, stroke_width=3,
              stroke_dasharray="1.2 2.2")
    ic.circle(cx, cy, 36, fill="#5A2508")
    ic.circle(cx, cy, 35, fill=ic.rad([(0, "#FFC15A"), (0.55, "#F07A1C"), (1, "#B8410C")], cx=0.38, cy=0.32,
                                      r=0.75))
    _swirl(ic, cx + 0.8, cy + 1, 22, fill="#7A2A06", opacity=0.45)
    _swirl(ic, cx, cy, 22, fill="#FFF3DE")
    ic.circle(cx, cy - 1, 8, fill=ic.rad([(0, "#FFD27A"), (1, "#F07A1C")]))
    # its pointer, at the keyframe it stands on
    x1, y1 = polar(cx, cy, 37, -36)
    x2, y2 = polar(cx, cy, 47, -36)
    ic.line(x1, y1, x2, y2, stroke="#1A1422", stroke_width=5, stroke_linecap="round")
    ic.line(x1, y1, x2, y2, stroke="#FFF3DE", stroke_width=2.6, stroke_linecap="round")
    ic.path(f"M{cx - 30} {cy - 12}A34 34 0 0 1 {cx + 8} {cy - 34}", fill="none", stroke="#fff",
            stroke_opacity=0.45, stroke_width=3, stroke_linecap="round")


@small("synfig")
def synfig16(ic):
    tile(ic, "#43384F", "#1A1422")
    ic.circle(8, 8, 6.4, fill="#2A2C30")
    for a in (-100, -36, 88):
        x, y = polar(8, 8, 6.4, a)
        ic.path(f"M{x:.2f} {y - 1.2:.2f}l1.2 1.2-1.2 1.2-1.2-1.2z", fill="#F08A24")
    ic.circle(8, 8, 4.4, fill="#F07A1C")
    _swirl(ic, 8, 8, 2.6, fill="#FFF3DE")


# --- FreeCAD: a machined block on its drawing, the red F anodised on it ------

@icon("freecad", kind="app", names=["freecad", "freecad-daily", "org.freecad.FreeCAD", "org.freecadweb.FreeCAD"],
      title="FreeCAD")
def freecad(ic):
    tile(ic, "#56687C", "#232D3A")
    shadow(ic, 128, 214, 100, 12)
    # the drawing sheet, with its border and title block
    with ic.g(transform="rotate(-3 128 128)"):
        ic.rect(28, 50, 200, 154, rx=2, fill="#000", opacity=0.28, transform="translate(3 4)")
        ic.rect(28, 50, 200, 154, rx=2, fill=paper(ic, "cream"))
        ic.rect(34, 56, 188, 142, fill="none", stroke="#3D5A80", stroke_width=1.2)
        ic.rect(158, 176, 64, 22, fill="none", stroke="#3D5A80", stroke_width=1)
        ic.line(158, 186, 222, 186, stroke="#3D5A80", stroke_width=0.8)
        ic.text("FreeCAD", 162, 184, 7, font="sans-semibold", fill="#2A3A52")
        ic.text("BRACKET-02  1:1", 162, 194, 5, font="mono", fill="#5A6878")
        # the part's front view, in the drawing's lines, and a dimension
        ic.rect(44, 150, 60, 34, fill="none", stroke="#2A3A52", stroke_width=1.3)
        ic.line(62, 150, 62, 184, stroke="#2A3A52", stroke_width=0.8, stroke_dasharray="4 2 1 2")
        ic.line(86, 150, 86, 184, stroke="#2A3A52", stroke_width=0.8, stroke_dasharray="4 2 1 2")
        ic.line(44, 190, 104, 190, stroke="#3D5A80", stroke_width=0.8)
        ic.path("M44 190l4-1.6v3.2zM104 190l-4-1.6v3.2z", fill="#3D5A80")
        ic.text("60", 74, 188, 6.5, font="mono", anchor="middle", fill="#2A3A52")
    # the block, in isometric: a step, a bore through the top
    p = _iso(124, 90, 1.0)
    W, D, H, S = 72, 56, 40, 20  # width (x), depth (y), height, the step's height
    top = steel(ic, horizontal=False)
    alu_l = ic.lin([(0, "#B9C0C8"), (1, "#7C858F")], 0, 0, 1, 1)
    alu_r = ic.lin([(0, "#7F8892"), (1, "#4B535C")], 0, 0, 1, 1)
    # the lower slab: x 0..W, y 0..D, z 0..S; the upper block x 0..W, y 0..D*0.55
    d2 = D * 0.5
    ic.path(_pts([p(0, D, 0), p(W, D, 0), p(W, D, S), p(0, D, S)]), fill=alu_l)
    ic.path(_pts([p(W, 0, 0), p(W, D, 0), p(W, D, S), p(W, 0, S)]), fill=alu_r)
    ic.path(_pts([p(0, d2, S), p(W, d2, S), p(W, D, S), p(0, D, S)]), fill=top)
    ic.path(_pts([p(0, d2, S), p(W, d2, S), p(W, d2, H + S), p(0, d2, H + S)]), fill=alu_l)
    ic.path(_pts([p(W, 0, S), p(W, d2, S), p(W, d2, H + S), p(W, 0, H + S)]), fill=alu_r)
    ic.path(_pts([p(0, 0, H + S), p(W, 0, H + S), p(W, d2, H + S), p(0, d2, H + S)]), fill=top)
    # the edges, light where the light catches them
    for a, b in (((0, d2, H + S), (W, d2, H + S)), ((W, 0, H + S), (W, d2, H + S)), ((0, D, S), (W, D, S)),
                 ((0, d2, S), (W, d2, S))):
        ic.line(*p(*a), *p(*b), stroke="#fff", stroke_opacity=0.55, stroke_width=1.1)
    for a, b in (((W, d2, S), (W, d2, H + S)), ((W, D, 0), (W, D, S))):
        ic.line(*p(*a), *p(*b), stroke="#2A3038", stroke_opacity=0.5, stroke_width=1)
    # the bore through the top, and a counterbored hole in the step
    for (x, y, z, r) in ((W / 2, d2 / 2, H + S, 11), (W * 0.5, D * 0.76, S, 7)):
        cx, cy = p(x, y, z)
        ic.ellipse(cx, cy, r * 1.22, r * 0.71, fill=ic.lin([(0, "#1B1F24"), (1, "#5A626C")]))
        ic.ellipse(cx, cy, r * 1.22, r * 0.71, fill="none", stroke="#2A3038", stroke_width=1)
        ic.path(f"M{cx - r * 1.1:.1f} {cy + r * 0.3:.1f}A{r * 1.22:.1f} {r * 0.71:.1f} 0 0 0 "
                f"{cx + r * 1.1:.1f} {cy + r * 0.3:.1f}", fill="none", stroke="#fff", stroke_opacity=0.5,
                stroke_width=1)
    # the red F, anodised on the tall face, skewed with it
    fx, fy = p(0, d2, H + S)
    with ic.g(transform=f"matrix(0.866 0.5 0 1 {fx:.1f} {fy:.1f})"):
        ic.rect(12, 6, 38, 30, rx=3, fill="#7A1410")
        ic.rect(12, 5, 38, 30, rx=3, fill=ic.lin([(0, "#E8473A"), (1, "#A81E16")]))
        ic.path("M21 9h20v6h-13v4h11v6h-11v8h-7z", fill="#fff")
        ic.line(14, 6.2, 48, 6.2, stroke="#fff", stroke_opacity=0.5, stroke_width=1)


@small("freecad")
def freecad16(ic):
    tile(ic, "#56687C", "#232D3A")
    ic.rect(1.5, 10, 13, 4.5, rx=0.4, fill="#F4EEE0")
    ic.path("M8 2 L13.5 5 L13.5 10.5 L8 13.5 L2.5 10.5 L2.5 5z", fill="#8E959D")
    ic.path("M8 2 L13.5 5 L8 8 L2.5 5z", fill="#D4D8DD")
    ic.path("M8 8 L13.5 5 L13.5 10.5 L8 13.5z", fill="#5D636B")
    ic.path("M1.3 1.6h3.2v1.2h-2v0.9h1.6v1.1h-1.6v2.1h-1.2z", fill="#E8473A", transform="matrix(1 0.545 0 1 2.5 5)")


# --- KiCad: a green circuit board, KiCad's name on its chip ------------------

@icon("kicad", kind="app", names=["kicad", "org.kicad.KiCad"], title="KiCad")
def kicad(ic):
    tile(ic, "#3448A0", "#141C48")
    shadow(ic, 128, 214, 102, 12)
    # the board: its edge, its solder mask, the copper under it
    ic.rect(26, 44, 204, 160, rx=8, fill="#0B2A14", transform="translate(2 5)")
    ic.rect(26, 44, 204, 160, rx=8, fill="#1F5A2C")
    ic.rect(26, 42, 204, 158, rx=8, fill=ic.lin([(0, "#2E8A45"), (1, "#14532A")], 0, 0, 1, 1))
    ic.line(34, 43, 222, 43, stroke="#fff", stroke_opacity=0.3, stroke_width=1.5)
    trace = dict(fill="none", stroke="#5FBF6E", stroke_width=3, stroke_linecap="round", stroke_linejoin="round",
                 opacity=0.75)
    for d in ("M98 96 H70 L58 108 V150", "M98 108 H80 L74 114 V176 H112", "M158 96 H184 L196 84 V64",
              "M158 112 H200 V160", "M120 138 V160 L134 174 H176", "M140 138 V150 L150 160 H196",
              "M120 70 V56 H160", "M134 70 V60"):
        ic.path(d, **trace)
    for x, y in ((58, 150), (112, 176), (196, 64), (160, 56), (134, 60), (176, 174)):
        ic.circle(x, y, 4, fill="#E3B65A")
        ic.circle(x, y, 1.6, fill="#0B2A14")
    # mounting holes, gold rings
    for x, y in ((40, 56), (216, 56), (40, 186), (216, 186)):
        ic.circle(x, y, 7, fill=brass(ic))
        ic.circle(x, y, 4, fill="#0D1A10")
    # the chip, KiCad's name on it
    ic.rect(98, 70, 60, 68, rx=2, fill="#000", opacity=0.4, transform="translate(2 3)")
    for i in range(7):
        y = 78 + i * 8.5
        ic.rect(92, y, 8, 3.4, fill=steel(ic))
        ic.rect(156, y, 8, 3.4, fill=steel(ic))
    ic.rect(98, 70, 60, 68, rx=2, fill=graphite(ic))
    ic.line(99, 71, 157, 71, stroke="#fff", stroke_opacity=0.2, stroke_width=1.2)
    ic.circle(105, 77, 2.4, fill="#16181B", stroke="#5A5F66", stroke_width=0.6)
    ic.text("KiCad", 128, 108, 13, font="sans-bold", anchor="middle", fill="#E9ECEF")
    ic.text("U1 · 2026", 128, 122, 6, font="mono", anchor="middle", fill="#9AA1A9")
    # resistors, an electrolytic capacitor, an LED
    for x, y in ((50, 120), (50, 136)):
        ic.rect(x - 4, y - 1.5, 30, 3, fill="#C3C8CE")
        ic.rect(x, y - 5, 22, 10, rx=5, fill=ic.lin([(0, "#E8D2A6"), (1, "#B89A62")]))
        for k, c in enumerate(("#7A4A22", "#2A2C30", "#C8372D", "#C99645")):
            ic.rect(x + 4 + k * 4, y - 5, 2.2, 10, fill=c)
    ic.circle(190, 136, 17, fill="#000", opacity=0.35, transform="translate(2 3)")
    ic.circle(190, 136, 17, fill=ic.lin([(0, "#3E6FC0"), (1, "#1A3A78")], 0, 0, 1, 1))
    ic.path("M190 119 A17 17 0 0 1 207 136 H200 A10 10 0 0 0 190 126z", fill="#C9D6EA", opacity=0.75)
    ic.circle(190, 136, 10, fill=ic.lin([(0, "#E3E7EB"), (1, "#8E959D")]))
    ic.path("M184 132l12 8M184 140l12-8", stroke="#5D636B", stroke_width=1)
    ic.circle(146, 172, 8, fill="#C8372D")
    ic.circle(146, 172, 8, fill="none", stroke="#7A1410", stroke_width=1)
    ic.circle(143.5, 169.5, 2.6, fill="#fff", opacity=0.6)
    # a crystal, a pin header
    ic.rect(56, 64, 34, 16, rx=8, fill="#000", opacity=0.35, transform="translate(1.5 2.5)")
    ic.rect(56, 64, 34, 16, rx=8, fill=steel(ic, horizontal=False))
    ic.rect(57.5, 65.2, 31, 4, rx=2, fill="#fff", opacity=0.45)
    ic.text("16.000", 73, 76, 5.5, font="mono-semibold", anchor="middle", fill="#3A3F46")
    ic.rect(58, 184, 44, 12, rx=1, fill="#000", opacity=0.35, transform="translate(1.5 2.5)")
    ic.rect(58, 184, 44, 12, rx=1, fill=graphite(ic))
    for k in range(4):
        x = 64 + k * 11
        ic.rect(x - 2.2, 187.8, 4.4, 4.4, fill=brass(ic))
        ic.rect(x - 1, 188.2, 1.2, 1.2, fill="#fff", opacity=0.6)
    # silkscreen
    ic.text("Y1", 56, 60, 6, font="mono-semibold", fill="#F2F5F0", opacity=0.85)
    ic.text("J1", 106, 194, 6, font="mono-semibold", fill="#F2F5F0", opacity=0.85)
    ic.text("R1", 50, 112, 6, font="mono-semibold", fill="#F2F5F0", opacity=0.85)
    ic.text("C3", 182, 162, 6, font="mono-semibold", fill="#F2F5F0", opacity=0.85)
    ic.text("D1", 158, 175, 6, font="mono-semibold", fill="#F2F5F0", opacity=0.85)
    ic.text("REV B", 214, 196, 6, font="mono-semibold", anchor="end", fill="#F2F5F0", opacity=0.7)


@small("kicad")
def kicad16(ic):
    tile(ic, "#3448A0", "#141C48")
    ic.rect(1.5, 3, 13, 10.5, rx=0.8, fill="#2E8A45")
    ic.path("M3 6 H5.5 M10.5 6 H13 M3 10.5 H5.5", stroke="#7FD48C", stroke_width=0.8)
    ic.rect(5.5, 4.8, 5, 6, rx=0.3, fill="#1E2024")
    ic.circle(12, 10.8, 1.4, fill="#3E6FC0")


# --- LibreCAD: a T-square and a drafting triangle over a drawing -------------

@icon("librecad", kind="app", names=["librecad", "org.librecad.librecad"], title="LibreCAD")
def librecad(ic):
    tile(ic, "#3E6A5C", "#16342C")
    shadow(ic, 128, 214, 102, 12)
    # the sheet, taped down
    ic.rect(36, 40, 184, 168, rx=2, fill="#000", opacity=0.28, transform="translate(3 4)")
    ic.rect(36, 40, 184, 168, rx=2, fill=paper(ic, "white"))
    for x, y, r in ((30, 36, -30), (210, 36, 30), (30, 200, 30), (210, 200, -30)):
        ic.rect(x, y, 22, 10, fill="#EADFB8", opacity=0.85, transform=f"rotate({r} {x + 11} {y + 5})")
    # the drawing: a plate, a hole, its centre lines and dimensions, in pencil
    ln = dict(fill="none", stroke="#2E3440", stroke_width=1.6, stroke_linejoin="round")
    ic.path("M58 70 H150 L170 90 V128 H58z", **ln)
    ic.circle(98, 99, 16, **ln)
    ic.line(74, 99, 122, 99, stroke="#C8372D", stroke_width=0.8, stroke_dasharray="6 2 1 2")
    ic.line(98, 75, 98, 123, stroke="#C8372D", stroke_width=0.8, stroke_dasharray="6 2 1 2")
    ic.line(58, 58, 170, 58, stroke="#3B7FD4", stroke_width=0.8)
    ic.path("M58 58l5-2v4zM170 58l-5-2v4z", fill="#3B7FD4")
    ic.text("112", 114, 55, 7, font="mono", anchor="middle", fill="#3B7FD4")
    ic.text("Ø32", 116, 120, 7, font="mono", fill="#2E3440")
    ic.text("LibreCAD", 58, 190, 9, font="sans-semibold", fill="#16342C", opacity=0.75)
    ic.text("plate.dxf · 1:2", 58, 200, 6, font="mono", fill="#8C887F")
    # the triangle, 30-60, clear blue acrylic with its cut-out
    tri = "M134 146 L210 146 L210 46z"
    hole = "M154 139 L202 139 L202 76z"
    ic.path(tri, fill="#000", opacity=0.2, transform="translate(3 4)")
    ic.path(tri + hole, fill="#4FA0E0", fill_opacity=0.55, fill_rule="evenodd")
    ic.path(tri, fill="none", stroke="#2D74B4", stroke_width=1.5, stroke_linejoin="round")
    ic.path(hole, fill="none", stroke="#BDE0FA", stroke_width=1.2, stroke_linejoin="round")
    ic.path("M136 144 L208 50", stroke="#fff", stroke_opacity=0.55, stroke_width=1.4)
    for k in range(1, 10):
        y = 146 - k * 10
        ic.line(210, y, 205 if k % 2 else 198, y, stroke="#1A4A78", stroke_width=0.8)
    # the T-square: its head at the left edge, the blade across the sheet
    ic.rect(24, 142, 208, 20, fill="#000", opacity=0.25, transform="translate(3 5)")
    blade = ic.lin([(0, "#F4F7F9", 0.92), (1, "#C9D6DE", 0.9)])
    ic.rect(40, 146, 192, 16, fill=blade)
    ic.rect(40, 146, 192, 3, fill="#C8372D")
    for k in range(0, 47):
        x = 44 + k * 4
        ic.line(x, 162, x, 158 if k % 5 else 154, stroke="#2E3440", stroke_width=0.7)
    ic.line(40, 162, 232, 162, stroke="#5A6878", stroke_width=1)
    ic.rect(22, 128, 22, 48, rx=3, fill=wood(ic, "#D9A066", "#7A4A22"))
    ic.line(24, 130, 24, 174, stroke="#fff", stroke_opacity=0.35, stroke_width=1.5)
    for y in (136, 168):
        ic.circle(33, y, 2.4, fill=brass(ic))
    # a drafting pencil, laid down
    with ic.g(transform="translate(150 196) rotate(-12) scale(0.8)"):
        _pencil(ic, 96, body="#3E6A5C", body_dark="#1F3E35", band="#C99645", top="#7FB0A0")


@small("librecad")
def librecad16(ic):
    tile(ic, "#3E6A5C", "#16342C")
    ic.rect(2.5, 2.5, 11, 11, rx=0.3, fill="#FFFFFF")
    ic.path("M4 4.5 H9 L11 6.5 V8.5 H4z", fill="none", stroke="#2E3440", stroke_width=0.7)
    ic.path("M8 13 L13.5 13 L13.5 6.5z", fill="#4FA0E0", opacity=0.85)
    ic.rect(1.5, 10, 13, 1.8, fill="#E9EEF2")
    ic.rect(1.5, 10, 13, 0.6, fill="#C8372D")
    ic.rect(1, 9, 2, 4, rx=0.3, fill="#B07A48")


# --- Sweet Home 3D: a little house model on its floor plan --------------------

@icon("sweethome3d", kind="app", names=["com.sweethome3d.Sweethome3d", "sweethome3d"], title="Sweet Home 3D")
def sweethome3d(ic):
    tile(ic, "#2F7C78", "#113C3C")
    shadow(ic, 128, 214, 102, 12)
    # the plan: walls, doors swinging, rooms named
    with ic.g(transform="rotate(-4 128 140)"):
        ic.rect(26, 92, 204, 116, rx=2, fill="#000", opacity=0.28, transform="translate(3 4)")
        ic.rect(26, 92, 204, 116, rx=2, fill=paper(ic, "white"))
        grid = ic.define('<pattern id="{id}" width="10" height="10" patternUnits="userSpaceOnUse">'
                         '<path d="M10 0V10H0" fill="none" stroke="#7FA6CF" stroke-opacity=".25"/></pattern>', "p")
        ic.rect(30, 96, 196, 108, fill=f"url(#{grid})")
        walls = dict(fill="none", stroke="#2E3440", stroke_width=4, stroke_linejoin="miter")
        ic.path("M40 104 H216 V196 H40z", **walls)
        ic.path("M120 104 V150 M120 166 V196 M120 150 H160 M176 150 H216", **walls)
        thin = dict(fill="none", stroke="#2E3440", stroke_width=1)
        ic.path("M120 166 A16 16 0 0 1 136 150", **thin)
        ic.path("M160 150 A16 16 0 0 0 176 166", **thin)
        ic.text("Living", 54, 186, 8, font="sans-semibold", fill="#2E3440")
        ic.text("24 m²", 54, 195, 6, font="mono", fill="#5A6878")
        ic.text("Kitchen", 168, 186, 7, font="sans-semibold", anchor="middle", fill="#2E3440")
        ic.rect(140, 112, 30, 18, rx=2, fill="#E7E3DA", stroke="#5A6878")
        ic.text("Sweet Home 3D · house.sh3d", 128, 205, 5.5, font="mono-semibold", anchor="middle", fill="#2F7C78")
    # the model, set on the plan
    p = _iso(116, 104, 1.0)
    W, D, H, R = 84, 52, 34, 34  # length, depth, wall height, ridge above the walls
    ov = 6
    ic.path(_pts([p(0, D, 0), p(W, D, 0), p(W, 0, 0), p(W + 8, 0, -2), p(W + 8, D + 8, -2), p(-4, D + 8, -2)]),
            fill="#000", opacity=0.25)
    wall_l = ic.lin([(0, "#FFFDF7"), (1, "#E4DCCB")])
    wall_r = ic.lin([(0, "#D8D0BF"), (1, "#B9AF9A")])
    ic.path(_pts([p(0, D, 0), p(W, D, 0), p(W, D, H), p(0, D, H)]), fill=wall_l)
    ic.path(_pts([p(W, 0, 0), p(W, D, 0), p(W, D, H), p(W, D / 2, H + R), p(W, 0, H)]), fill=wall_r)
    # windows and the door on the long wall, a round window in the gable
    def face_l(x0, z0, w, h, fill):
        ic.path(_pts([p(x0, D, z0), p(x0 + w, D, z0), p(x0 + w, D, z0 + h), p(x0, D, z0 + h)]), fill=fill)
    glass = ic.lin([(0, "#BFE3F5"), (1, "#4F8FBF")])
    for x0 in (8, 56):
        face_l(x0 - 1.5, 11.5, 19, 15, "#F4EFE4")
        face_l(x0, 13, 16, 12, glass)
        face_l(x0 + 7.4, 13, 1.2, 12, "#F4EFE4")
    face_l(34, 0, 14, 24, "#8A4E2A")
    face_l(36, 2, 10, 20, "#A8653A")
    import math
    for r, col in ((7.5, "#F4EFE4"), (5.6, glass)):
        ic.path(_pts([p(W, D / 2 + r * math.cos(t / 12 * math.pi), H + 13 + r * math.sin(t / 12 * math.pi))
                      for t in range(24)]), fill=col)
    # the roof: the far slope's eave over the gable, the slope we see, the ridge
    ic.path(_pts([p(-ov, D / 2, H + R), p(W + ov, D / 2, H + R), p(W + ov, -ov, H - 4), p(-ov, -ov, H - 4)]),
            fill="#8E3214")
    ic.path(_pts([p(W + ov, D / 2, H + R), p(W + ov, -ov, H - 4), p(W + ov, -ov, H - 7),
                  p(W + ov, D / 2, H + R - 3)]), fill="#6A220C")
    roof = ic.lin([(0, "#F07A4A"), (1, "#B8401C")], 0, 0, 1, 1)
    ic.path(_pts([p(-ov, D / 2, H + R), p(W + ov, D / 2, H + R), p(W + ov, D + ov, H - 4), p(-ov, D + ov, H - 4)]),
            fill=roof)
    tiles = ic.clip(f'<path d="{_pts([p(-ov, D / 2, H + R), p(W + ov, D / 2, H + R), p(W + ov, D + ov, H - 4), p(-ov, D + ov, H - 4)])}"/>')
    with ic.g(clip_path=tiles, fill="none", stroke="#7A2A10", stroke_opacity=0.35, stroke_width=1):
        for k in range(1, 6):
            t = k / 6
            y = D / 2 + t * (D / 2 + ov)
            z = H + R - t * (R + 4)
            ic.line(*p(-ov, y, z), *p(W + ov, y, z))
    ic.path(_pts([p(W + ov, D / 2, H + R), p(W + ov, D + ov, H - 4), p(W + ov, D + ov, H - 7),
                  p(W + ov, D / 2, H + R - 3)]), fill="#7A2A10")
    ic.line(*p(-ov, D / 2, H + R), *p(W + ov, D / 2, H + R), stroke="#FFC0A0", stroke_width=1.6,
            stroke_linecap="round")
    # the chimney
    cx0, cy0 = 18, D / 2 + 6
    ztop = H + R + 4
    zb = H + R - 8
    ic.path(_pts([p(cx0, cy0 + 8, zb), p(cx0 + 8, cy0 + 8, zb), p(cx0 + 8, cy0 + 8, ztop), p(cx0, cy0 + 8, ztop)]),
            fill="#E4DCCB")
    ic.path(_pts([p(cx0 + 8, cy0, zb), p(cx0 + 8, cy0 + 8, zb), p(cx0 + 8, cy0 + 8, ztop), p(cx0 + 8, cy0, ztop)]),
            fill="#B9AF9A")
    ic.path(_pts([p(cx0, cy0, ztop), p(cx0 + 8, cy0, ztop), p(cx0 + 8, cy0 + 8, ztop), p(cx0, cy0 + 8, ztop)]),
            fill="#5A5650")


@small("sweethome3d")
def sweethome3d16(ic):
    tile(ic, "#2F7C78", "#113C3C")
    ic.rect(1.5, 8, 13, 6, rx=0.3, fill="#FFFFFF")
    ic.path("M2.5 9 H13.5 V13 H2.5z M8 9 V13", fill="none", stroke="#2E3440", stroke_width=0.6)
    ic.rect(4, 7, 8, 5, fill="#F4EFE4")
    ic.path("M2.8 7.5 L8 2.5 L13.2 7.5z", fill="#E8602C")
    ic.rect(7, 9, 2, 3, fill="#A8653A")
