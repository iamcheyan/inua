"""The soft drawings of the desktop's own tools (drawings/apps_t2_desktop.py):
the same objects with about half the detail, no text."""

from lib import bar, polar, soft, soft_shadow, tile, two


def _pts(points):
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in points) + "Z"


def _iso(ox, oy, k=1.0):
    def p(x, y, z=0):
        return (ox + (x - y) * 0.866 * k, oy + (x + y) * 0.5 * k - z * k)
    p.k = k
    return p


def _faces(p, x, y, z, w, d, h):
    top = [p(x, y, z + h), p(x + w, y, z + h), p(x + w, y + d, z + h), p(x, y + d, z + h)]
    left = [p(x, y + d, z + h), p(x + w, y + d, z + h), p(x + w, y + d, z), p(x, y + d, z)]
    right = [p(x + w, y + d, z + h), p(x + w, y, z + h), p(x + w, y, z), p(x + w, y + d, z)]
    return top, left, right


def _on(p, face, x, y, z, w, d, h):
    k = p.k
    if face == "left":
        ox, oy = p(x, y + d, z + h)
        return f"matrix({0.866 * k:.4f} {0.5 * k:.4f} 0 {k:.4f} {ox:.2f} {oy:.2f})"
    if face == "right":
        ox, oy = p(x + w, y + d, z + h)
        return f"matrix({0.866 * k:.4f} {-0.5 * k:.4f} 0 {k:.4f} {ox:.2f} {oy:.2f})"
    ox, oy = p(x, y, z + h)
    return f"matrix({0.866 * k:.4f} {0.5 * k:.4f} {-0.866 * k:.4f} {0.5 * k:.4f} {ox:.2f} {oy:.2f})"


def _box(ic, p, x, y, z, w, d, h, top, left, right):
    t, l, r = _faces(p, x, y, z, w, d, h)
    ic.path(_pts(l), fill=left)
    ic.path(_pts(r), fill=right)
    ic.path(_pts(t), fill=top)
    return t, l, r


# --- Warehouse ---------------------------------------------------------------

def _crate(ic, p, x, y, z, w, d, h, top, left, right, seam):
    _box(ic, p, x, y, z, w, d, h, top, left, right)
    for face, span in (("left", w), ("right", d)):
        with ic.g(transform=_on(p, face, x, y, z, w, d, h)):
            ic.rect(0, h / 2 - 1.2, span, 2.4, fill=seam, opacity=0.5)
            ic.rect(0, 0, span, h, fill="none", stroke=seam, stroke_width=4, opacity=0.35)


@soft("warehouse")
def warehouse(ic):
    tile(ic, "#3E6690", "#1A3150")
    soft_shadow(ic, 128, 208, 100, 13)
    p = _iso(128, 112, 0.95)
    _box(ic, p, -4, -4, 0, 108, 108, 13, "#E2BE84", "#B88A52", "#86603A")
    with ic.g(transform=_on(p, "left", -4, -4, 0, 108, 108, 13)):
        for u in (14, 62):
            ic.rect(u, 4, 32, 9, rx=2, fill="#3A2614")
    with ic.g(transform=_on(p, "right", -4, -4, 0, 108, 108, 13)):
        for u in (14, 62):
            ic.rect(u, 4, 32, 9, rx=2, fill="#2A1C0E")
    for (x, y) in ((0, 0), (52, 0), (0, 52), (52, 52)):
        _crate(ic, p, x, y, 13, 48, 48, 40, "#E8C088", two(ic, "#D7A867", "#B98648"),
               two(ic, "#A87440", "#8A5C30"), "#5E3A16")
    _crate(ic, p, 22, 22, 53, 56, 56, 38, two(ic, "#86BDF0", "#62A2E2"), two(ic, "#4A90D9", "#3577C0"),
           two(ic, "#2D67A8", "#22558E"), "#123459")
    tx, ty = p(50, 50, 91)
    with ic.g(transform=f"translate({tx:.1f} {ty:.1f}) scale(1 0.58) rotate(30)"):
        hexa = [polar(0, 0, 17, a) for a in range(0, 360, 60)]
        ic.path(_pts(hexa), fill="none", stroke="#FFFFFF", stroke_width=5, stroke_linejoin="round")
        for a in (0, 120, 240):
            ic.line(0, 0, *polar(0, 0, 17, (a + 180) % 360), stroke="#FFFFFF", stroke_width=5,
                    stroke_linecap="round")
    with ic.g(transform=_on(p, "left", 22, 22, 53, 56, 56, 38)):
        bar(ic, 12, 16, 32, 7, fill="#FFFFFF", opacity=0.85)


# --- Extension Manager -------------------------------------------------------

def _jigsaw(x, y, s, edges):
    tab = [(0.36, 0), (0.42, 0, 0.44, 0.06, 0.41, 0.12), (0.36, 0.22, 0.42, 0.31, 0.5, 0.31),
           (0.58, 0.31, 0.64, 0.22, 0.59, 0.12), (0.56, 0.06, 0.58, 0, 0.64, 0), (1, 0)]
    corners = [(x, y), (x + s, y), (x + s, y + s), (x, y + s)]
    d = f"M{x:.1f} {y:.1f}"
    for i, sign in enumerate(edges):
        (ax, ay), (bx, by) = corners[i], corners[(i + 1) % 4]
        ux, uy = (bx - ax) / s, (by - ay) / s
        nx, ny = uy, -ux

        def pt(t, n):
            return f"{ax + (ux * t + nx * n * sign) * s:.1f} {ay + (uy * t + ny * n * sign) * s:.1f}"
        if sign == 0:
            d += f"L{bx:.1f} {by:.1f}"
            continue
        for seg in tab:
            if len(seg) == 2:
                d += "L" + pt(*seg)
            else:
                d += "C" + " ".join(pt(seg[j], seg[j + 1]) for j in (0, 2, 4))
    return d + "Z"


@soft("extension-manager")
def extension_manager(ic):
    tile(ic, "#3F7458", "#183A28")
    soft_shadow(ic, 128, 208, 98, 13)
    with ic.g(transform="rotate(-14 170 70)"):
        back = _jigsaw(142, 36, 76, (0, 0, 1, -1))
        ic.path(back, fill="#B9B2A2", transform="translate(0 6)")
        ic.path(back, fill=two(ic, "#FBF6EA", "#E8DFCB"))
        bar(ic, 158, 54, 42, 8, fill="#C9C1AE")
        bar(ic, 158, 70, 28, 8, fill="#C9C1AE")
    with ic.g(transform="rotate(-6 120 130)"):
        d = _jigsaw(46, 66, 120, (1, 1, -1, -1))
        ic.path(d, fill="#1A4F94", transform="translate(0 10)")
        ic.path(d, fill=two(ic, "#5A9CEC", "#2A6CC6"))
        ic.rect(66, 100, 80, 42, rx=21, fill="#F6F8FB")
        ic.rect(71, 105, 70, 32, rx=16, fill="#1F62B8")
        ic.circle(124, 121, 13, fill="#FFFFFF")
        bar(ic, 70, 158, 72, 10, fill="#FFFFFF", opacity=0.9)
        bar(ic, 84, 174, 44, 6, fill="#D6E6FB", opacity=0.8)


# --- Tweaks ------------------------------------------------------------------

def _knob(ic, cx, cy, r, deg):
    ic.circle(cx, cy, r, fill=two(ic, "#4A4F58", "#24272C"))
    ic.circle(cx, cy, r - 5, fill="#3584E4")
    ic.line(cx, cy, *polar(cx, cy, r - 8, deg), stroke="#FFFFFF", stroke_width=4, stroke_linecap="round")


@soft("gnome-tweaks")
def tweaks(ic):
    tile(ic, "#56677F", "#232D3D")
    soft_shadow(ic, 128, 212, 102, 12)
    ic.rect(28, 52, 200, 160, rx=18, fill="#2A2E35")
    ic.rect(28, 46, 200, 152, rx=18, fill=two(ic, "#EEF0F3", "#BCC2CA"))
    _knob(ic, 74, 92, 20, -60)
    _knob(ic, 128, 92, 20, 40)
    ic.rect(162, 76, 44, 26, rx=13, fill="#3584E4")
    ic.circle(193, 89, 10, fill="#FFFFFF")
    ic.circle(184, 116, 5, fill="#F6A33A")
    ic.rect(42, 130, 172, 3, rx=1.5, fill="#8A919B", opacity=0.6)
    for i, (x, t) in enumerate(((66, 0.25), (108, 0.62), (150, 0.4), (192, 0.75))):
        ic.rect(x - 3.5, 146, 7, 40, rx=3.5, fill="#2A2D33")
        y = 146 + 40 * t
        ic.rect(x - 13, y - 7, 26, 14, rx=5, fill="#3584E4" if i == 1 else "#F6F7F9")
        ic.rect(x - 9, y - 1.5, 18, 3, rx=1.5, fill="#FFFFFF" if i == 1 else "#5D636B")


# --- dconf Editor ------------------------------------------------------------

@soft("dconf-editor")
def dconf_editor(ic):
    tile(ic, "#4C4A8E", "#211F4A")
    soft_shadow(ic, 128, 214, 100, 12)

    def card(y, tx, col, tone):
        ic.rect(44, y, 168, 60, rx=6, fill=tone)
        ic.path(f"M{tx} {y + 2}v-10a5 5 0 0 1 5-5h40a5 5 0 0 1 5 5v10z", fill=col)
    card(84, 52, "#E8B04A", "#E2DACA")
    with ic.g(transform="rotate(-3 128 80)"):
        ic.rect(54, 24, 150, 100, rx=8, fill=two(ic, "#FFFFFF", "#F0ECE3"))
        ic.rect(54, 42, 150, 3, fill="#D9473E", opacity=0.75)
        bar(ic, 64, 30, 96, 6, fill="#B9B4AA")
        bar(ic, 64, 54, 70, 10, fill="#1E2A3E")
        bar(ic, 64, 76, 86, 10, fill="#2D4A9A")
        bar(ic, 64, 98, 104, 6, fill="#B9B4AA")
    card(110, 104, "#5DA0E6", "#EDE6D8")
    card(122, 158, "#E07A5F", "#E6DED0")
    ic.rect(34, 132, 188, 78, rx=10, fill=two(ic, "#C99360", "#8E5A2E"))
    ic.rect(96, 142, 64, 30, rx=5, fill=two(ic, "#E2B45E", "#B88433"))
    ic.rect(101, 147, 54, 20, rx=3, fill="#FBF4E2")
    bar(ic, 110, 153, 36, 8, fill="#2A2C30")
    ic.rect(104, 184, 48, 14, rx=7, fill=two(ic, "#E2B45E", "#B88433"))


# --- Font Manager ------------------------------------------------------------

def _bilerp(q, u, v):
    (ax, ay), (bx, by), (cx, cy), (dx, dy) = q
    tx, ty = ax + (bx - ax) * u, ay + (by - ay) * u
    sx, sy = dx + (cx - dx) * u, dy + (cy - dy) * u
    return tx + (sx - tx) * v, ty + (sy - ty) * v


@soft("font-manager")
def font_manager(ic):
    tile(ic, "#424A5E", "#1A1E28")
    soft_shadow(ic, 128, 212, 104, 12)
    q = [(56, 36), (200, 36), (226, 140), (30, 140)]
    ic.path("M60 28H196a8 8 0 0 1 8 6L234 146H22L52 34a8 8 0 0 1 8-6z", fill=two(ic, "#C48A55", "#93602F"))
    ic.path(_pts(q), fill="#3A2412")
    cols = [0, 0.25, 0.5, 0.75, 1]
    rows = [0, 0.33, 0.66, 1]
    for r in range(3):
        for c in range(4):
            u0, u1, v0, v1 = cols[c] + 0.02, cols[c + 1] - 0.02, rows[r] + 0.06, rows[r + 1] - 0.04
            cell = [_bilerp(q, u0, v0), _bilerp(q, u1, v0), _bilerp(q, u1, v1), _bilerp(q, u0, v1)]
            ic.path(_pts(cell), fill="#9AA0A8" if (r + c) % 2 else "#7E848D")
    for u in cols:
        ic.line(*_bilerp(q, u, 0), *_bilerp(q, u, 1), stroke="#C99360", stroke_width=4)
    for v in rows:
        ic.line(*_bilerp(q, 0, v), *_bilerp(q, 1, v), stroke="#D5A06A", stroke_width=4.5)
    ic.path("M22 146H234L231 162H25z", fill="#6E4420")
    ic.rect(108, 147, 40, 12, rx=3, fill=two(ic, "#E2B45E", "#B88433"))
    with ic.g(transform="rotate(-7 80 186)"):
        ic.rect(34, 156, 100, 58, rx=6, fill=two(ic, "#FBF6EA", "#ECE3CF"))
        ic.path("M44 202L58 166H66L80 202H71L68 193H56L53 202ZM58.5 186H65.5L62 175Z", fill="#1E1E20")
        ic.path("M88 202L97 178H103L112 202H106L104 196H96L94 202ZM97.5 191H102.5L100 184Z", fill="#C8372D")
    fx, fy, fw, fh, dx, dy = 160, 160, 40, 46, 16, 24
    ic.path(_pts([(fx, fy), (fx + fw, fy), (fx + fw + dx, fy - dy), (fx + dx, fy - dy)]), fill="#C9CED6")
    ic.path(_pts([(fx + fw, fy), (fx + fw + dx, fy - dy), (fx + fw + dx, fy + fh - dy), (fx + fw, fy + fh)]),
            fill="#5D636B")
    ic.rect(fx, fy, fw, fh, fill=two(ic, "#AEB4BB", "#8D949C"))
    ic.rect(fx, fy + 28, fw, 4, fill="#5D636B")
    ic.path(_pts([(fx + 10, fy - 4), (fx + 30, fy - 4), (fx + 38, fy - 18), (fx + 18, fy - 18)]), fill="#3E434A")


# --- Characters --------------------------------------------------------------

@soft("gnome-characters")
def characters(ic):
    tile(ic, "#3B8A7A", "#14453B")
    soft_shadow(ic, 128, 214, 102, 12)
    ic.rect(26, 34, 204, 180, rx=24, fill=two(ic, "#2F3338", "#16181B"))
    ic.rect(34, 42, 188, 164, rx=18, fill="#0F1113")
    white = ("#ECECEA", "#FFFFFF", "#2A2C30")
    blue = ("#2A72CC", "#4E96EC", "#FFFFFF")
    yellow = ("#E0B634", "#F6D35A", "#2A2C30")
    caps = [white, white, blue, white, white, yellow]
    for i, (side, face, ink) in enumerate(caps):
        x = 42 + (i % 3) * 59
        y = 50 + (i // 3) * 76
        ic.rect(x, y, 54, 54, rx=11, fill=side)
        ic.rect(x + 5, y + 3, 44, 42, rx=9, fill=face)
        cx, cy = x + 27, y + 24
        st = dict(fill="none", stroke=ink, stroke_width=5, stroke_linecap="round", stroke_linejoin="round")
        if i == 0:  # alpha
            ic.ellipse(cx - 3, cy, 8, 9, **st)
            ic.path(f"M{cx + 8} {cy - 10}Q{cx + 3} {cy + 11} {cx + 12} {cy + 10}", **st)
        elif i == 1:  # an arrow
            ic.path(f"M{cx - 11} {cy}H{cx + 10}M{cx + 2} {cy - 8}L{cx + 11} {cy}L{cx + 2} {cy + 8}", **st)
        elif i == 2:  # omega
            ic.path(f"M{cx - 12} {cy + 11}H{cx - 5}V{cy + 7}A11 11 0 1 1 {cx + 5} {cy + 7}V{cy + 11}H{cx + 12}", **st)
        elif i == 3:  # e acute
            ic.path(f"M{cx - 8} {cy + 2}H{cx + 8}A8 8 0 1 0 {cx + 5} {cy + 8}", **st)
            ic.path(f"M{cx - 1} {cy - 11}L{cx + 5} {cy - 16}", **st)
        elif i == 4:  # division
            ic.path(f"M{cx - 11} {cy}H{cx + 11}", **st)
            ic.circle(cx, cy - 9, 3.4, fill=ink)
            ic.circle(cx, cy + 9, 3.4, fill=ink)
        else:  # a face
            ic.circle(cx, cy, 13, fill="none", stroke=ink, stroke_width=4)
            ic.circle(cx - 4.5, cy - 3, 2.4, fill=ink)
            ic.circle(cx + 4.5, cy - 3, 2.4, fill=ink)
            ic.path(f"M{cx - 6} {cy + 3}a6.5 6.5 0 0 0 12 0", fill="none", stroke=ink, stroke_width=3.5,
                    stroke_linecap="round")


# --- Software ----------------------------------------------------------------

@soft("gnome-software")
def software(ic):
    tile(ic, "#C47A36", "#743A12")
    soft_shadow(ic, 128, 214, 94, 12)
    ic.path("M100 78 C98 30 162 30 160 78", fill="none", stroke="#A8581C", stroke_width=8, stroke_linecap="round")
    for x, y, rot, col in ((80, 50, -12, "#3584E4"), (114, 44, 6, "#E5534B"), (146, 52, 14, "#33B479")):
        with ic.g(transform=f"rotate({rot} {x + 18} {y + 18})"):
            ic.rect(x, y, 36, 36, rx=11, fill=col)
            ic.circle(x + 18, y + 18, 8, fill="#fff", opacity=0.85)
    ic.path("M58 80H198L208 204a8 8 0 0 1-8 8H56a8 8 0 0 1-8-8z", fill=two(ic, "#FFFFFF", "#ECE8DF"))
    ic.path("M178 80H198L208 204a8 8 0 0 1-8 8H186z", fill="#000", opacity=0.07)
    ic.rect(58, 80, 140, 10, fill="#E2DCD0")
    ic.path("M88 98 C86 46 150 46 148 98", fill="none", stroke="#E07A2C", stroke_width=8, stroke_linecap="round")
    ic.circle(118, 148, 32, fill="#3584E4")
    ic.path("M104 140H132L129 165H107z", fill="#FFFFFF")
    ic.path("M111 140v-3a7 7 0 0 1 14 0v3", fill="none", stroke="#FFFFFF", stroke_width=3.5)
    ic.path("M113 151l5 5 5-5M118 146v10", fill="none", stroke="#3584E4", stroke_width=3, stroke_linecap="round",
            stroke_linejoin="round")
    bar(ic, 88, 192, 60, 9, fill="#2A2C30")


# --- Discover ----------------------------------------------------------------

@soft("discover")
def discover(ic):
    tile(ic, "#2B3D5A", "#0F1828")
    soft_shadow(ic, 128, 212, 102, 13)
    p = _iso(128, 104, 0.92)
    W, D, H = 104, 104, 70
    _box(ic, p, 0, 0, 0, W, D, H, "#5BB8F5", two(ic, "#2FA0EC", "#1D7FC8"), two(ic, "#1878BE", "#0F5590"))
    lid = (-4, -4, H - 16, W + 8, D + 8, 18)
    _box(ic, p, *lid, two(ic, "#7CC4FA", "#4CB2EE"), "#46AEEE", "#1E7FC6")
    for face, box, col in (("left", lid, "#FFFFFF"), ("right", lid, "#D6DEE8"),
                           ("left", (0, 0, 0, W, D, H - 16), "#FFFFFF"),
                           ("right", (0, 0, 0, W, D, H - 16), "#D6DEE8")):
        with ic.g(transform=_on(p, face, *box)):
            span = box[3] if face == "left" else box[4]
            ic.rect(span / 2 - 9, 0, 18, box[5], fill=col)
    with ic.g(transform=_on(p, "top", *lid)):
        ic.rect((W + 8) / 2 - 9, 0, 18, D + 8, fill="#F4F8FC")
        ic.rect(0, (D + 8) / 2 - 9, W + 8, 18, fill="#FFFFFF")
    cx, cy = p(W / 2, D / 2, H + 2)
    for sx in (-1, 1):
        ic.path(f"M{cx} {cy}C{cx + sx * 12} {cy - 36} {cx + sx * 46} {cy - 24} {cx + sx * 30} {cy - 4}"
                f"C{cx + sx * 22} {cy + 2} {cx + sx * 8} {cy + 2} {cx} {cy}z", fill=two(ic, "#FFFFFF", "#D3DCE8"))
        ic.path(f"M{cx} {cy + 2}L{cx + sx * 14} {cy + 26}L{cx + sx * 22} {cy + 19}z", fill="#E8EEF5")
    ic.ellipse(cx, cy, 9, 7.5, fill="#C9D4E2")


# --- Synaptic ----------------------------------------------------------------

@soft("synaptic")
def synaptic(ic):
    tile(ic, "#A13A30", "#521610")
    soft_shadow(ic, 128, 210, 98, 12)
    p = _iso(128, 92, 0.98)
    W, D, H = 100, 76, 76
    _box(ic, p, 0, 0, 0, W, D, H, two(ic, "#F1F2F4", "#DDE0E4"), two(ic, "#D9DCE0", "#BEC3C9"),
         two(ic, "#9BA1A9", "#7D838B"))
    with ic.g(transform=_on(p, "top", 0, 0, 0, W, D, H)):
        ic.rect(0, D / 2 - 10, W, 20, fill="#D8382C")
    with ic.g(transform=_on(p, "right", 0, 0, 0, W, D, H)):
        ic.rect(D / 2 - 10, 0, 20, 24, fill="#A82418")
    with ic.g(transform=_on(p, "left", 0, 0, 0, W, D, H)):
        ic.path("M23 12h18v16h10L32 48 13 28h10z", fill="#D8382C", stroke="#D8382C", stroke_width=2,
                stroke_linejoin="round")
        ic.path("M14 52v5h36v-5", fill="none", stroke="#D8382C", stroke_width=4, stroke_linecap="round",
                stroke_linejoin="round")
        bar(ic, 60, 16, 32, 8, fill="#3A3E45")
        bar(ic, 60, 30, 24, 5, fill="#7D838B")
        bar(ic, 60, 40, 28, 5, fill="#7D838B")


# --- Boxes -------------------------------------------------------------------

def _open_box(ic, p, s, z, h, o, front):
    if not front:
        back_l = [p(o, o, z + h), p(o, o + s, z + h), p(o, o + s, z), p(o, o, z)]
        back_r = [p(o, o, z + h), p(o + s, o, z + h), p(o + s, o, z), p(o, o, z)]
        floor = [p(o, o, z), p(o + s, o, z), p(o + s, o + s, z), p(o, o + s, z)]
        ic.path(_pts(back_l), fill="#B8591A")
        ic.path(_pts(back_r), fill="#D2701E")
        ic.path(_pts(floor), fill="#9A4A0E")
        return
    _, left, right = _faces(p, o, o, z, s, s, h)
    ic.path(_pts(left), fill=two(ic, "#FFB25C", "#F2902F"))
    ic.path(_pts(right), fill=two(ic, "#D8711E", "#B85A12"))
    rim = [p(o, o + s, z + h), p(o, o, z + h), p(o + s, o, z + h), p(o + s, o + s, z + h)]
    ic.path("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in rim) + "Z", fill="none", stroke="#FFDDA8",
            stroke_width=4, stroke_linejoin="round")


@soft("gnome-boxes")
def boxes(ic):
    tile(ic, "#4E3E66", "#211833")
    soft_shadow(ic, 128, 212, 102, 12)
    p = _iso(128, 92, 0.9)
    sizes = [(120, 0, 62, 0), (88, 8, 50, 16), (56, 16, 30, 32)]
    for s_, z, h, o in sizes:
        _open_box(ic, p, s_, z, h, o, False)
    ic.path(_pts([p(40, 40, 16), p(80, 40, 16), p(80, 80, 16), p(40, 80, 16)]), fill=two(ic, "#7FB8F0", "#3A6EAE"))
    ic.path(_pts([p(40, 40, 16), p(80, 40, 16), p(80, 47, 16), p(40, 47, 16)]), fill="#F6F8FB", opacity=0.85)
    for s_, z, h, o in reversed(sizes):
        _open_box(ic, p, s_, z, h, o, True)


# --- Camera (Snapshot) -------------------------------------------------------

@soft("snapshot")
def snapshot(ic):
    tile(ic, "#8494A8", "#3E4A5C")
    soft_shadow(ic, 128, 216, 86, 12)
    cx, rx, ry = 128, 74, 28

    def band(y0, y1, r, fill):
        ic.path(f"M{cx - r} {y0}A{r} {ry * r / rx} 0 0 0 {cx + r} {y0}V{y1}A{r} {ry * r / rx} 0 0 1 {cx - r} {y1}z",
                fill=fill)
    band(186, 202, 64, "#1A1C20")
    band(176, 188, 70, "#AEB4BB")
    band(150, 178, rx, "#2A2D32")
    band(104, 150, rx, "#3E4248")
    for k in (-24, -12, 0, 12, 24):
        x = cx + k * 2.4
        f = (1 - (k * 2.4 / rx) ** 2) ** 0.5
        ic.line(x, 110 + ry * f, x, 144 + ry * f, stroke="#1A1C20", stroke_width=4, stroke_linecap="round",
                opacity=0.6)
    band(80, 104, rx, "#24272C")
    ic.path(f"M{cx - 5} {80 + ry + 6}l5 6 5-6z", fill="#4A90D9")
    ic.ellipse(cx, 80, rx, ry, fill="#5A5F67")
    ic.ellipse(cx, 80, rx - 6, ry - 3, fill="#0A0B0D")
    ic.ellipse(cx, 81, rx - 12, ry - 6, fill=two(ic, "#3A50A8", "#121A44"))
    ic.ellipse(cx, 82, 34, 12.5, fill="none", stroke="#7A5CD8", stroke_opacity=0.6, stroke_width=3)
    ic.ellipse(cx, 82, 20, 7.5, fill="#020203")


# --- Cheese ------------------------------------------------------------------

@soft("cheese")
def cheese(ic):
    tile(ic, "#6B3C8C", "#30174A")
    soft_shadow(ic, 124, 206, 106, 12)
    with ic.g(transform="rotate(-9 64 90)"):
        ic.rect(42, 30, 42, 104, rx=5, fill=two(ic, "#FFFFFF", "#ECE8DF"))
        for i in range(3):
            y = 35 + i * 31
            ic.rect(47, y, 32, 27, rx=3, fill="#6E44A0")
            ic.circle(63, y + 12, 6.5, fill="#F6D28A")
            ic.path(f"M53 {y + 27}a10 9 0 0 1 20 0z", fill="#F6D28A")
    fx, fy = 182, 58
    for a in range(-150, 41, 38):
        ic.line(*polar(fx, fy, 37, a), *polar(fx, fy, 50, a), stroke="#FFF4B0", stroke_width=6,
                stroke_linecap="round", opacity=0.9)
    ic.rect(178, 82, 9, 42, rx=3, fill=two(ic, "#AEB4BB", "#8D949C"))
    ic.circle(fx, fy, 29, fill=two(ic, "#E6E9EE", "#8D949C"))
    ic.circle(fx, fy, 23, fill="#F4F6F9")
    ic.circle(fx, fy, 10, fill="#FFE98A")
    L, F, R = (24, 128), (148, 156), (210, 108)
    h = 52
    Lb, Fb = (L[0], L[1] + h), (F[0], F[1] + h)
    cut = [L, F, Fb, Lb]
    ic.path(_pts(cut), fill=two(ic, "#FFE27A", "#F2BC3A"))
    ic.path(f"M{F[0]} {F[1]}Q186 138 {R[0]} {R[1]}V{R[1] + h}Q186 {138 + h} {Fb[0]} {Fb[1]}z",
            fill=two(ic, "#E8A21C", "#C07C10"))
    ic.path(f"M{L[0]} {L[1]}L{F[0]} {F[1]}Q186 138 {R[0]} {R[1]}z", fill="#FFEFA0")
    for u, v, r in ((0.3, 0.45, 9), (0.66, 0.66, 11), (0.6, 0.24, 6), (0.12, 0.74, 5)):
        x, y = _bilerp(cut, u, v)
        ic.ellipse(x, y, r * 0.95, r, fill="#D49A1C", transform=f"rotate(12 {x:.1f} {y:.1f})")
    for x, y, r in ((96, 130, 9), (150, 124, 6)):
        ic.ellipse(x, y, r * 1.3, r * 0.6, fill="#EDC048")
