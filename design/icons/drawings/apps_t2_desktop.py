"""The inua-objects theme, the desktop's own tools: Warehouse, Extension
Manager, Tweaks, dconf Editor, Font Manager, Characters, Software,
Discover, Synaptic, Boxes, Camera (Snapshot), Cheese (docs/feat/object-icons.md,
Part 2, tier 2). Each is the app's job as an object on the desk in its
brand's colours, its mark redrawn as a stamp, a print or a label."""

import math

from lib import (brass, glare, graphite, icon, paper, polar, shadow, small, steel, tile, wood)


def _pts(points):
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in points) + "Z"


def _iso(ox, oy, k=1.0):
    """An isometric projection from (ox, oy): x runs down to the right, y
    down to the left, z up; k px a unit."""
    def p(x, y, z=0):
        return (ox + (x - y) * 0.866 * k, oy + (x + y) * 0.5 * k - z * k)
    p.k = k
    return p


def _faces(p, x, y, z, w, d, h):
    """A box's three visible faces: the top, the left (facing down left)
    and the right (facing down right)."""
    top = [p(x, y, z + h), p(x + w, y, z + h), p(x + w, y + d, z + h), p(x, y + d, z + h)]
    left = [p(x, y + d, z + h), p(x + w, y + d, z + h), p(x + w, y + d, z), p(x, y + d, z)]
    right = [p(x + w, y + d, z + h), p(x + w, y, z + h), p(x + w, y, z), p(x + w, y + d, z)]
    return top, left, right


def _on(p, face, x, y, z, w, d, h):
    """A transform drawing on a box's face in its own units: on the left
    and right faces u runs along it left to right, v down from the top
    edge; on the top u runs along x, v along y."""
    k = p.k
    if face == "left":
        ox, oy = p(x, y + d, z + h)
        return f"matrix({0.866 * k:.4f} {0.5 * k:.4f} 0 {k:.4f} {ox:.2f} {oy:.2f})"
    if face == "right":
        ox, oy = p(x + w, y + d, z + h)
        return f"matrix({0.866 * k:.4f} {-0.5 * k:.4f} 0 {k:.4f} {ox:.2f} {oy:.2f})"
    ox, oy = p(x, y, z + h)
    return f"matrix({0.866 * k:.4f} {0.5 * k:.4f} {-0.866 * k:.4f} {0.5 * k:.4f} {ox:.2f} {oy:.2f})"


def _cube_mark(ic, cx, cy, r, **kw):
    """A packaging mark: an isometric cube in outline, its three edges
    meeting in the middle."""
    hexa = [polar(cx, cy, r, a) for a in range(0, 360, 60)]
    ic.path(_pts(hexa), fill="none", stroke_linejoin="round", **kw)
    for a in (0, 120, 240):
        x, y = polar(cx, cy, r, a + 60 if a else 180)
        ic.line(cx, cy, *polar(cx, cy, r, (a + 180) % 360), stroke_linecap="round", **kw)


# --- Warehouse: crates stacked on a pallet, the blue one on top -------------

def _crate_face(ic, W, H, base, light, dark, planks=3):
    """A crate's side in its own units: boards, a frame and a brace."""
    ic.rect(0, 0, W, H, fill=ic.lin([(0, light), (1, base)]))
    for i in range(1, planks):
        ic.line(0, H * i / planks, W, H * i / planks, stroke=dark, stroke_width=1.2, opacity=0.7)
    f = 5
    ic.path(f"M0 0H{W}V{H}H0z M{f} {f}V{H - f}H{W - f}V{f}z", fill=light, fill_rule="evenodd")
    ic.path(f"M0 0H{W}V{H}H0z M{f} {f}V{H - f}H{W - f}V{f}z", fill="none", stroke=dark, stroke_width=0.8,
            opacity=0.6)
    ic.path(f"M{f} {H - f - 4}L{W - f - 4} {f}L{W - f} {f}V{f + 4}L{f + 4} {H - f}H{f}z", fill=light,
            stroke=dark, stroke_width=0.6, stroke_opacity=0.5)
    for x, y in ((2.5, 2.5), (W - 2.5, 2.5), (2.5, H - 2.5), (W - 2.5, H - 2.5)):
        ic.circle(x, y, 0.9, fill=dark)


def _crate(ic, p, x, y, z, w, d, h, tones):
    (tl, tb), (ll, lb), (rl, rb), dark = tones
    top, left, right = _faces(p, x, y, z, w, d, h)
    with ic.g(transform=_on(p, "top", x, y, z, w, d, h)):
        ic.rect(0, 0, w, d, fill=ic.lin([(0, tl), (1, tb)], 0, 0, 1, 1))
        for i in range(1, 5):
            ic.line(0, d * i / 5, w, d * i / 5, stroke=dark, stroke_width=1, opacity=0.5)
        ic.rect(0, 0, w, d, fill="none", stroke=dark, stroke_width=0.8, opacity=0.5)
    with ic.g(transform=_on(p, "left", x, y, z, w, d, h)):
        _crate_face(ic, w, h, lb, ll, dark)
    with ic.g(transform=_on(p, "right", x, y, z, w, d, h)):
        _crate_face(ic, d, h, rb, rl, dark)
    ic.line(*top[3], *top[0], stroke="#fff", stroke_opacity=0.4, stroke_width=1.2)
    ic.line(*top[0], *top[1], stroke="#fff", stroke_opacity=0.3, stroke_width=1.2)


WOOD = (("#EBC48A", "#D7A867"), ("#D2A061", "#B07A3E"), ("#A87440", "#7E5226"), "#5E3A16")
BLUE = (("#7FB6EE", "#5C9BE0"), ("#4A90D9", "#2F70B8"), ("#2D67A8", "#1D4C85"), "#123459")


@icon("warehouse", kind="app", names=["io.github.flattool.Warehouse", "warehouse"], title="Warehouse")
def warehouse(ic):
    tile(ic, "#3E6690", "#1A3150")
    shadow(ic, 128, 206, 98, 12)
    p = _iso(128, 112, 0.95)
    # the pallet: a deck on three blocks a side
    top, left, right = _faces(p, -4, -4, 0, 108, 108, 13)
    ic.path(_pts(left), fill=ic.lin([(0, "#C9A06A"), (1, "#9C7442")]))
    ic.path(_pts(right), fill=ic.lin([(0, "#9C7442"), (1, "#6E4E28")]))
    with ic.g(transform=_on(p, "left", -4, -4, 0, 108, 108, 13)):
        for u in (14, 62):
            ic.rect(u, 4, 32, 9, fill="#2A1C0E")
        ic.line(0, 3.5, 108, 3.5, stroke="#5E3A16", stroke_width=1)
    with ic.g(transform=_on(p, "right", -4, -4, 0, 108, 108, 13)):
        for u in (14, 62):
            ic.rect(u, 4, 32, 9, fill="#1A1008")
        ic.line(0, 3.5, 108, 3.5, stroke="#3E260E", stroke_width=1)
    ic.path(_pts(top), fill="#E2BE84")
    # the bottom layer: four crates
    for (x, y) in ((0, 0), (52, 0), (0, 52), (52, 52)):
        _crate(ic, p, x, y, 13, 48, 48, 40, WOOD)
    # a stencil on the front crates
    with ic.g(transform=_on(p, "left", 0, 52, 13, 48, 48, 40)):
        ic.text("THIS SIDE UP", 24, 25, 5.6, font="sans-condensed", anchor="middle", fill="#3E260E", opacity=0.8)
        ic.path("M18 31 l3-4 3 4 M21 27v8 M27 31 l3-4 3 4 M30 27v8", fill="none", stroke="#3E260E",
                stroke_width=1.2, opacity=0.8)
    with ic.g(transform=_on(p, "right", 52, 52, 13, 48, 48, 40)):
        ic.rect(9, 11, 30, 18, fill="#F4EEDF")
        ic.rect(9, 11, 30, 4, fill="#2F70B8")
        for i, wd in enumerate((1.2, 0.6, 1.6, 0.6, 0.6, 1.2, 0.6, 1.6, 0.6, 1.2, 0.6, 0.6, 1.6)):
            ic.rect(12 + i * 1.9, 18, wd, 8, fill="#2A2C30")
    # the top: the blue crate, the mark on its lid
    _crate(ic, p, 22, 22, 53, 56, 56, 38, BLUE)
    with ic.g(transform=_on(p, "top", 22, 22, 53, 56, 56, 38)):
        ic.circle(28, 28, 15, fill="#123459", opacity=0.25)
    tx, ty = p(50, 50, 91)
    with ic.g(transform=f"translate({tx:.1f} {ty:.1f}) scale(1 0.58) rotate(30)"):
        _cube_mark(ic, 0, 0, 16, stroke="#FFFFFF", stroke_width=3.2, opacity=0.92)
    with ic.g(transform=_on(p, "left", 22, 22, 53, 56, 56, 38)):
        ic.text("WAREHOUSE", 28, 23, 7.4, font="sans-condensed", anchor="middle", spacing=0.4, fill="#FFFFFF",
                opacity=0.92)
    with ic.g(transform=_on(p, "right", 22, 22, 53, 56, 56, 38)):
        ic.text("No. 24", 28, 23, 7.4, font="mono-semibold", anchor="middle", fill="#FFFFFF", opacity=0.85)


@small("warehouse")
def warehouse16(ic):
    tile(ic, "#3E6690", "#1A3150")
    ic.rect(2, 12.2, 12, 1.6, fill="#9C7442")
    ic.rect(2.5, 8, 5.2, 4.2, fill="#C9945A", stroke="#6E4E28", stroke_width=0.4)
    ic.rect(8.3, 8, 5.2, 4.2, fill="#B07A3E", stroke="#6E4E28", stroke_width=0.4)
    ic.rect(4.6, 3, 6.8, 5, fill="#4A90D9", stroke="#1D4C85", stroke_width=0.4)
    ic.path("M8 3.9 l1.6.9v1.8L8 7.5 6.4 6.6V4.8z", fill="none", stroke="#fff", stroke_width=0.6)


# --- Extension Manager: a jigsaw piece, a switch printed on it ---------------

def _jigsaw(x, y, s, edges):
    """A jigsaw piece's outline: a square at (x, y), side s, its edges top,
    right, bottom, left each +1 (a knob), -1 (a hole) or 0 (flat)."""
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


@icon("extension-manager", kind="app",
      names=["com.mattjakeman.ExtensionManager", "cs-extensions", "extension-manager",
             "gnome-shell-extension-prefs", "preferences-plugin", "yast-addon"],
      title="Extension Manager")
def extension_manager(ic):
    tile(ic, "#3F7458", "#183A28")
    shadow(ic, 128, 206, 96, 12)
    # a second piece lying behind, cream, fitting the first's knob
    with ic.g(transform="rotate(-14 170 70)"):
        back = _jigsaw(142, 36, 76, (0, 0, 1, -1))
        ic.path(back, fill="#000", opacity=0.3, transform="translate(3 6)")
        ic.path(back, fill="#B9B2A2", transform="translate(0 5)")
        ic.path(back, fill=paper(ic, "cream"))
        ic.path(back, fill="none", stroke="#fff", stroke_opacity=0.6, stroke_width=1.2)
        ic.rect(160, 56, 40, 6, rx=3, fill="#C9C1AE")
        ic.rect(160, 68, 28, 6, rx=3, fill="#C9C1AE")
    # the piece: blue, thick, a little turned
    with ic.g(transform="rotate(-6 120 130)"):
        d = _jigsaw(46, 66, 120, (1, 1, -1, -1))
        ic.path(d, fill="#000", opacity=0.35, transform="translate(4 14)")
        ic.path(d, fill="#1A4F94", transform="translate(0 10)")
        ic.path(d, fill="#225EAA", transform="translate(0 5)")
        ic.path(d, fill=ic.lin([(0, "#6AA8F2"), (0.5, "#3584E4"), (1, "#2264BE")], 0, 0, 1, 1))
        ic.path(d, fill="none", stroke="#fff", stroke_opacity=0.35, stroke_width=1.6)
        # the print: a switch, on, and the name
        ic.rect(68, 104, 76, 38, rx=19, fill="#174A8A", opacity=0.5, transform="translate(0 1.5)")
        ic.rect(68, 102, 76, 38, rx=19, fill="#F6F8FB")
        ic.rect(72, 106, 68, 30, rx=15, fill=ic.lin([(0, "#2F78D6"), (1, "#1C5AAE")]))
        ic.circle(124, 121, 12, fill="#000", opacity=0.2, transform="translate(0 1.5)")
        ic.circle(124, 121, 12, fill=ic.lin([(0, "#FFFFFF"), (1, "#DCE3EC")]))
        ic.text("ON", 92, 125.5, 11, font="sans-bold", anchor="middle", fill="#FFFFFF")
        ic.text("Extensions", 106, 164, 15, font="sans-semibold", anchor="middle", fill="#FFFFFF", opacity=0.95)
        ic.text("enabled · 12", 106, 176, 7.5, font="mono", anchor="middle", fill="#D6E6FB", opacity=0.85)


@small("extension-manager")
def extension_manager16(ic):
    tile(ic, "#3F7458", "#183A28")
    ic.path(_jigsaw(3, 4.5, 8.4, (1, 1, -1, -1)), fill="#3584E4")
    ic.rect(4.6, 7.8, 5.2, 2.6, rx=1.3, fill="#FFFFFF")
    ic.circle(8.5, 9.1, 0.9, fill="#3584E4")


# --- Tweaks: a control panel of faders, knobs and a switch -------------------

def _knob(ic, cx, cy, r, deg, cap):
    ic.circle(cx + 1.5, cy + 3, r, fill="#000", opacity=0.3)
    ic.circle(cx, cy, r, fill=ic.lin([(0, "#5A606A"), (1, "#202328")], 0, 0, 1, 1))
    for a in range(0, 360, 20):
        x1, y1 = polar(cx, cy, r, a)
        x2, y2 = polar(cx, cy, r - 2.4, a)
        ic.line(x1, y1, x2, y2, stroke="#0E0F11", stroke_width=1)
    ic.circle(cx, cy, r - 4, fill=cap)
    ic.circle(cx, cy, r - 4, fill="none", stroke="#fff", stroke_opacity=0.35, stroke_width=1)
    x, y = polar(cx, cy, r - 7, deg)
    ic.line(cx, cy, x, y, stroke="#FFFFFF", stroke_width=2.4, stroke_linecap="round")
    for k in range(9):
        a = -135 + k * 33.75
        x1, y1 = polar(cx, cy, r + 4, a)
        x2, y2 = polar(cx, cy, r + 7.5, a)
        ic.line(x1, y1, x2, y2, stroke="#2A2C30", stroke_width=1.1, opacity=0.8)


@icon("gnome-tweaks", kind="app",
      names=["gnome-tweak-tool", "gnome-tweaks", "org.gnome.tweaks", "org.xfce.xfwm4-tweaks",
             "preferences-desktop-tweaks", "tweaks-app"],
      title="Tweaks")
def tweaks(ic):
    tile(ic, "#56677F", "#232D3D")
    shadow(ic, 128, 210, 100, 12)
    # the console: a sloped aluminium face over a dark front edge
    ic.rect(28, 50, 200, 160, rx=14, fill="#000", opacity=0.3, transform="translate(2 4)")
    ic.rect(28, 50, 200, 160, rx=14, fill="#2A2E35")
    ic.rect(28, 46, 200, 150, rx=14, fill=ic.lin([(0, "#F3F4F6"), (0.5, "#D5D9DF"), (1, "#B3B9C2")], 0, 0, 1, 1))
    ic.path("M42 46.8H214", stroke="#fff", stroke_width=1.6)
    for x, y in ((38, 56), (218, 56), (38, 186), (218, 186)):
        ic.circle(x, y, 3, fill=steel(ic, horizontal=False))
        ic.line(x - 2, y - 2, x + 2, y + 2, stroke="#5D636B", stroke_width=0.8)
    # the knobs
    _knob(ic, 74, 88, 17, -60, "#3584E4")
    _knob(ic, 128, 88, 17, 40, "#3584E4")
    ic.text("SCALE", 74, 124, 6.5, font="mono-semibold", anchor="middle", spacing=0.8, fill="#4A505A")
    ic.text("FONTS", 128, 124, 6.5, font="mono-semibold", anchor="middle", spacing=0.8, fill="#4A505A")
    # the switch, on, and its light
    ic.rect(166, 72, 38, 22, rx=11, fill="#000", opacity=0.25, transform="translate(0 2)")
    ic.rect(166, 72, 38, 22, rx=11, fill=ic.lin([(0, "#2C6FC9"), (1, "#3D8CF0")]))
    ic.circle(193, 83, 9, fill=ic.lin([(0, "#FFFFFF"), (1, "#D5DBE3")]))
    ic.circle(185, 104, 3.4, fill="#F6A33A")
    ic.circle(185, 104, 6.5, fill="#F6A33A", opacity=0.25)
    ic.text("THEME", 185, 124, 6.5, font="mono-semibold", anchor="middle", spacing=0.8, fill="#4A505A")
    ic.line(42, 134, 214, 134, stroke="#8A919B", stroke_width=1)
    ic.line(42, 135, 214, 135, stroke="#fff", stroke_width=1, opacity=0.7)
    # the faders, set at three heights
    for i, (x, t) in enumerate(((66, 0.25), (108, 0.62), (150, 0.4), (192, 0.75))):
        ic.rect(x - 2.5, 144, 5, 42, rx=2.5, fill="#23262B")
        for k in range(5):
            ic.line(x - 12, 146 + k * 9.5, x - 7, 146 + k * 9.5, stroke="#5D636B", stroke_width=1)
        y = 144 + 42 * t
        ic.rect(x - 11, y - 6 + 3, 22, 12, rx=2.5, fill="#000", opacity=0.3)
        cap = ("#F6F7F9", "#C9CED6") if i != 1 else ("#6AA8F2", "#2264BE")
        ic.rect(x - 11, y - 6, 22, 12, rx=2.5, fill=ic.lin([(0, cap[0]), (1, cap[1])]))
        ic.line(x - 9, y, x + 9, y, stroke="#2A2C30" if i != 1 else "#FFFFFF", stroke_width=1.4)


@small("gnome-tweaks")
def tweaks16(ic):
    tile(ic, "#56677F", "#232D3D")
    ic.rect(2, 3, 12, 10.5, rx=1.4, fill="#D5D9DF")
    ic.circle(5, 6, 1.8, fill="#3584E4")
    ic.rect(8.5, 5, 4, 2.2, rx=1.1, fill="#3584E4")
    ic.circle(11.4, 6.1, 0.8, fill="#fff")
    for x, y in ((4.5, 10), (8, 11.5), (11.5, 9.5)):
        ic.rect(x - 0.3, 9, 0.6, 3.5, fill="#2A2C30")
        ic.rect(x - 1.2, y - 0.5, 2.4, 1.1, fill="#2A2C30")


# --- dconf Editor: a drawer of index cards, one key pulled up ----------------

@icon("dconf-editor", kind="app", names=["ca.desrt.dconf-editor", "dconf-editor"], title="dconf Editor")
def dconf_editor(ic):
    tile(ic, "#4C4A8E", "#211F4A")
    shadow(ic, 128, 212, 98, 12)
    # the cards behind, then the one pulled up, then the cards in front
    def card(y, name, tx, col, tone):
        ic.rect(44, y, 168, 60, rx=3, fill=tone, stroke="#000", stroke_opacity=0.12)
        ic.line(45, y + 1, 211, y + 1, stroke="#fff", stroke_opacity=0.7)
        ic.path(f"M{tx} {y + 1}v-11a3 3 0 0 1 3-3h42a3 3 0 0 1 3 3v11z", fill=col)
        ic.text(name, tx + 24, y - 2.5, 7.5, font="mono-semibold", anchor="middle", fill="#FFFFFF")
    card(84, "apps", 52, "#E8B04A", "#E2DACA")
    with ic.g(transform="rotate(-3 128 80)"):
        ic.rect(54, 24, 150, 100, rx=3, fill="#000", opacity=0.25, transform="translate(2 4)")
        ic.rect(54, 24, 150, 100, rx=3, fill=paper(ic, "white"))
        ic.line(55, 25, 203, 25, stroke="#fff", stroke_width=1.5)
        ic.rect(54, 41, 150, 1.2, fill="#D9473E", opacity=0.8)
        for y in (57, 71, 85, 99):
            ic.rect(54, y, 150, 0.8, fill="#9DB8D6", opacity=0.7)
        ic.text("/org/gnome/desktop/interface/", 61, 37, 7.2, font="mono", fill="#55534E")
        ic.text("font-name", 61, 54, 12, font="mono-semibold", fill="#1E2A3E")
        ic.text("'Inter 11'", 61, 82, 15, font="hand", fill="#2D4A9A")
        ic.text("type s · default 'Cantarell'", 61, 95, 6.4, font="mono", fill="#8C887F")
        ic.circle(190, 74, 8, fill="none", stroke="#D9473E", stroke_width=1.6, opacity=0.8)
        ic.path("M186 74l3 3 5-6", fill="none", stroke="#D9473E", stroke_width=1.8, stroke_linecap="round",
                stroke_linejoin="round", opacity=0.85)
    card(110, "desktop", 104, "#5DA0E6", "#EDE6D8")
    card(122, "shell", 158, "#E07A5F", "#E6DED0")
    # the drawer front, oak, a brass label frame and pull
    ic.rect(34, 132, 188, 76, rx=6, fill="#000", opacity=0.3, transform="translate(2 4)")
    ic.rect(34, 132, 188, 76, rx=6, fill=wood(ic, "#C99360", "#80502A"))
    for y in (148, 166, 186):
        ic.path(f"M40 {y}c40-3 80 3 176-1", fill="none", stroke="#6A3E1C", stroke_opacity=0.25, stroke_width=1)
    ic.line(40, 133.2, 216, 133.2, stroke="#F0C894", stroke_width=1.6, opacity=0.8)
    ic.rect(98, 144, 60, 26, rx=3, fill=brass(ic))
    ic.rect(102, 148, 52, 18, rx=1.5, fill=paper(ic, "cream"))
    ic.text("dconf", 128, 162, 13, font="sans-semibold", anchor="middle", fill="#2A2C30")
    for x in (101, 155):
        ic.circle(x, 157, 1.4, fill="#5A3E10")
    ic.path("M108 184h40a6 6 0 0 1 0 12h-40a6 6 0 0 1 0-12z", fill="#000", opacity=0.35, transform="translate(1 3)")
    ic.path("M108 184h40a6 6 0 0 1 0 12h-40a6 6 0 0 1 0-12z", fill=brass(ic, 0, 0, 0, 1))
    ic.path("M108 187h40", stroke="#FFF2C8", stroke_width=1.2, opacity=0.8)


@small("dconf-editor")
def dconf_editor16(ic):
    tile(ic, "#4C4A8E", "#211F4A")
    ic.rect(3, 4.5, 10, 5, fill="#E2DACA")
    ic.rect(4, 2.3, 8.5, 6.5, rx=0.4, fill="#FFFFFF")
    ic.rect(5, 4, 5.5, 0.9, fill="#1E2A3E")
    ic.rect(5, 6, 4, 0.7, fill="#2D4A9A")
    ic.rect(2, 8.5, 12, 5.5, rx=0.8, fill="#A8723F")
    ic.rect(6, 9.6, 4, 2, rx=0.3, fill="#E8C677")


# --- Font Manager: a typecase of metal sorts, one sort out and a proof -------

def _bilerp(q, u, v):
    (ax, ay), (bx, by), (cx, cy), (dx, dy) = q  # top left, top right, bottom right, bottom left
    tx, ty = ax + (bx - ax) * u, ay + (by - ay) * u
    sx, sy = dx + (cx - dx) * u, dy + (cy - dy) * u
    return tx + (sx - tx) * v, ty + (sy - ty) * v


@icon("font-manager", kind="app", names=["font-manager", "org.gnome.FontManager"], title="Font Manager")
def font_manager(ic):
    tile(ic, "#424A5E", "#1A1E28")
    shadow(ic, 128, 210, 102, 12)
    # the case, lying back: its inside a trapezoid
    q = [(56, 36), (200, 36), (226, 140), (30, 140)]
    ic.path(_pts([(52, 30), (204, 30), (234, 146), (22, 146)]), fill=wood(ic, "#C48A55", "#7A4A22"))
    ic.path(_pts(q), fill="#3A2412")
    cols = [0, 0.12, 0.24, 0.36, 0.5, 0.62, 0.74, 0.87, 1]
    rows = [0, 0.26, 0.5, 0.75, 1]
    sort = ic.lin([(0, "#B9BEC6"), (1, "#6F757E")])
    for r in range(4):
        for c in range(8):
            u0, u1, v0, v1 = cols[c], cols[c + 1], rows[r], rows[r + 1]
            cell = [_bilerp(q, u0, v0), _bilerp(q, u1, v0), _bilerp(q, u1, v1), _bilerp(q, u0, v1)]
            ic.path(_pts(cell), fill="#2A190A")
            inner = [_bilerp(q, u0 + 0.015, v0 + 0.09), _bilerp(q, u1 - 0.015, v0 + 0.09),
                     _bilerp(q, u1 - 0.015, v1 - 0.03), _bilerp(q, u0 + 0.015, v1 - 0.03)]
            ic.path(_pts(inner), fill=sort, opacity=0.55 + 0.35 * ((r * 3 + c * 5) % 4) / 3)
            # the sorts' faces, a row of little nicks
            n = 3 + (r + c) % 3
            for k in range(n):
                a = _bilerp(q, u0 + (u1 - u0) * (k + 0.5) / n, v0 + 0.12)
                b = _bilerp(q, u0 + (u1 - u0) * (k + 0.5) / n, v1 - 0.06)
                ic.line(*a, *b, stroke="#3A3F46", stroke_width=0.8, opacity=0.6)
    for u in cols:
        ic.line(*_bilerp(q, u, 0), *_bilerp(q, u, 1), stroke="#B07A45", stroke_width=2.2)
    for v in rows:
        ic.line(*_bilerp(q, 0, v), *_bilerp(q, 1, v), stroke="#C99360", stroke_width=2.6)
    # the case's front edge, a brass label pull
    ic.path("M22 146H234L232 160H24z", fill=ic.lin([(0, "#9A6434"), (1, "#5E3518")]))
    ic.line(24, 146.6, 232, 146.6, stroke="#E8B884", stroke_width=1.2)
    ic.rect(110, 148, 36, 10, rx=1.5, fill=brass(ic))
    ic.text("FONTS", 128, 155.6, 6.5, font="mono-semibold", anchor="middle", spacing=1, fill="#4A3410")
    # a proof slip, its face set in two weights
    with ic.g(transform="rotate(-7 80 186)"):
        ic.rect(34, 158, 96, 54, rx=2, fill="#000", opacity=0.3, transform="translate(2 4)")
        ic.rect(34, 158, 96, 54, rx=2, fill=paper(ic, "cream"))
        ic.text("Aa", 42, 196, 34, font="sans-bold", fill="#1E1E20")
        ic.text("Aa", 88, 196, 22, font="sans", fill="#C8372D")
        ic.text("IBM Plex Sans · 34", 42, 206, 5.5, font="mono", fill="#8C887F")
    # one sort standing out: its face up, the letter reversed on it
    fx, fy, fw, fh, dx, dy = 160, 158, 40, 46, 16, 26
    ic.path(_pts([(fx, fy), (fx + fw, fy), (fx + fw + dx, fy - dy), (fx + dx, fy - dy)]),
            fill=ic.lin([(0, "#6A7078"), (1, "#3E434A")], 0, 0, 1, 1))
    ic.path(_pts([(fx + fw, fy), (fx + fw + dx, fy - dy), (fx + fw + dx, fy + fh - dy), (fx + fw, fy + fh)]),
            fill=ic.lin([(0, "#5D636B"), (1, "#383C42")]))
    ic.rect(fx, fy, fw, fh, fill=ic.lin([(0, "#B9BEC6"), (1, "#6F757E")], 0, 0, 1, 0))
    for y in (fy + 28, fy + 34):
        ic.rect(fx, y, fw, 2.4, fill="#454A51")
        ic.path(f"M{fx + fw} {y}l{dx} {-dy}v2.4l{-dx} {dy}z", fill="#2E3238")
    ic.line(fx, fy + 0.6, fx + fw, fy + 0.6, stroke="#fff", stroke_opacity=0.7, stroke_width=1.2)
    k = dx / dy
    with ic.g(transform=f"matrix(1 0 {-k:.3f} 1 {k * fy:.2f} 0)"):
        with ic.g(transform=f"translate({fx + fw / 2:.1f} {fy - 3:.1f}) scale(-1 0.62)"):
            ic.text("R", 0, 0, 40, font="sans-bold", anchor="middle", fill="#1E2024", transform="translate(1.5 3)")
            ic.text("R", 0, 0, 40, font="sans-bold", anchor="middle", fill="#E9ECF0")


@small("font-manager")
def font_manager16(ic):
    tile(ic, "#424A5E", "#1A1E28")
    ic.path("M3.5 2.5H12.5L14.5 11H1.5z", fill="#A06A38")
    ic.path("M4.3 3.3H11.7L13.3 10.2H2.7z", fill="#3A2412")
    for x in (6, 8, 10):
        ic.path(f"M{x} 3.3L{x + (x - 8) * 0.22} 10.2", stroke="#C99360", stroke_width=0.6)
    for y, x0, x1 in ((5.6, 3.8, 12.2), (7.9, 3.2, 12.8)):
        ic.line(x0, y, x1, y, stroke="#C99360", stroke_width=0.6)
    ic.rect(1.5, 11, 13, 1.4, fill="#6E4420")
    ic.rect(10, 9, 3.6, 5.5, fill="#9AA1A9")
    ic.path("M10 9 L11.2 7.8 H14.8 L13.6 9z", fill="#5D636B")


# --- Characters: a tray of keycaps, a glyph pressed into each ----------------

def _keycap(ic, x, y, s, glyph, base, light, side, ink, font="sans-semibold", size=None, dy=0):
    ic.rect(x + 2, y + 6, s, s, rx=9, fill="#000", opacity=0.35)
    ic.rect(x, y, s, s, rx=9, fill=ic.lin([(0, base), (1, side)]))
    ic.rect(x + 6, y + 3, s - 12, s - 14, rx=7, fill=ic.lin([(0, light), (1, base)], 0, 0, 1, 1))
    ic.path(f"M{x + 11} {y + 3.8}H{x + s - 11}", stroke="#fff", stroke_opacity=0.7, stroke_width=1.2)
    if glyph:
        ic.text(glyph, x + s / 2, y + s / 2 + (size or s * 0.42) * 0.3 + dy, size or s * 0.42, font=font,
                anchor="middle", fill=ink)


@icon("gnome-characters", kind="app", names=["gnome-characters", "org.gnome.Characters"], title="Characters")
def characters(ic):
    tile(ic, "#3B8A7A", "#14453B")
    shadow(ic, 128, 212, 100, 12)
    # the tray they sit in
    ic.rect(26, 34, 204, 180, rx=22, fill=ic.lin([(0, "#2F3338"), (1, "#16181B")]))
    ic.rect(26.75, 34.75, 202.5, 178.5, rx=21.25, fill="none", stroke="#fff", stroke_opacity=0.14, stroke_width=1.5)
    ic.rect(34, 42, 188, 164, rx=16, fill="#0F1113")
    white = ("#F2F2F0", "#FFFFFF", "#B9BCC2", "#2A2C30")
    blue = ("#3584E4", "#7AB4F5", "#1C4E94", "#FFFFFF")
    caps = [("α", white, "sans-semibold", None, 0), ("ß", white, "sans-semibold", None, 0),
            ("Ω", blue, "sans-semibold", None, 0), ("é", white, "sans-semibold", None, 0),
            ("§", white, "sans-semibold", None, 0), (None, ("#F6D35A", "#FFF0A8", "#C99420", "#2A2C30"), "", 0, 0)]
    for i, (g, (b, l, s, ink), f, sz, dy) in enumerate(caps):
        x = 42 + (i % 3) * 59
        y = 50 + (i // 3) * 76
        _keycap(ic, x, y, 54, g, b, l, s, ink, font=f, size=sz, dy=dy - 2)
    # the last cap's glyph, a face, drawn
    cx, cy = 42 + 2 * 59 + 27, 50 + 76 + 22
    ic.circle(cx, cy, 13, fill="none", stroke="#2A2C30", stroke_width=2.6)
    ic.circle(cx - 4.5, cy - 3, 1.9, fill="#2A2C30")
    ic.circle(cx + 4.5, cy - 3, 1.9, fill="#2A2C30")
    ic.path(f"M{cx - 6} {cy + 3}a6.5 6.5 0 0 0 12 0", fill="none", stroke="#2A2C30", stroke_width=2.2,
            stroke_linecap="round")
    ic.text("U+03A9", 128, 202, 7, font="mono", anchor="middle", spacing=0.8, fill="#7FD3C0", opacity=0.8)


@small("gnome-characters")
def characters16(ic):
    tile(ic, "#3B8A7A", "#14453B")
    ic.rect(1.5, 2, 13, 12, rx=2, fill="#1E2024")
    for i, c in enumerate(("#F2F2F0", "#3584E4", "#F2F2F0", "#F6D35A")):
        ic.rect(2.5 + (i % 2) * 5.8, 3 + (i // 2) * 5.5, 5, 4.6, rx=1, fill=c)
    ic.text("α", 5, 6.6, 4.2, font="sans-bold", anchor="middle", fill="#2A2C30")
    ic.text("Ω", 10.8, 6.6, 4.2, font="sans-bold", anchor="middle", fill="#FFFFFF")


# --- Software: a paper shopping bag, apps in it -----------------------------

@icon("gnome-software", kind="app",
      names=["apper", "appgrid", "aptdaemon-download", "aptdaemon-working", "deepin-app-store", "deepin-appstore",
             "deepin-software-center", "dk.yumex.Yumex", "drakstats", "gnome-app-install", "gnome-apt",
             "gnome-software", "kentoo", "litesoftware", "lubuntu-software-center", "mintinstall",
             "mintupdate-release-upgrade", "muondiscover", "org.gnome.Software", "package-manager-icon", "pirut",
             "porthole", "rpmdrake", "software", "software-center", "software-manager", "software-properties-mint",
             "software-store", "softwarecenter", "softwarecenter-debian", "softwarecenter-ubuntu", "swcentre",
             "system-software-install", "system-software-installer", "ubuntu-kylin-software-center",
             "ubuntusoftware", "yast-software", "yast-sw_single", "yast-sw_source", "yumex", "yumex-dnf",
             "zeroinstall"],
      title="Software")
def software(ic):
    tile(ic, "#C47A36", "#743A12")
    shadow(ic, 128, 214, 92, 12)
    # the back of the bag and its far handle
    ic.path("M100 78 C98 30 162 30 160 78", fill="none", stroke="#A8581C", stroke_width=6, stroke_linecap="round")
    ic.path("M60 76H196L188 70H68z", fill="#C9C2B4")
    # app tiles peeking out of the top
    for x, y, rot, a, b in ((80, 50, -12, "#3584E4", "#1C5AAE"), (114, 44, 6, "#E5534B", "#B02E26"),
                            (146, 52, 14, "#33B479", "#1E7C50")):
        with ic.g(transform=f"rotate({rot} {x + 18} {y + 18})"):
            ic.rect(x, y, 36, 36, rx=9, fill=ic.lin([(0, a), (1, b)]))
            ic.rect(x + 1, y + 1, 34, 34, rx=8, fill="none", stroke="#fff", stroke_opacity=0.35, stroke_width=1.5)
            ic.circle(x + 18, y + 18, 8, fill="#fff", opacity=0.85)
    # the bag's body, white paper, its gusset in shade on the right
    ic.path("M58 80H198L208 206a6 6 0 0 1-6 6H54a6 6 0 0 1-6-6z", fill=paper(ic, "white"))
    ic.path("M178 80H198L208 206a6 6 0 0 1-6 6H186z", fill="#000", opacity=0.08)
    ic.path("M178 80 L186 212", stroke="#000", stroke_opacity=0.1, stroke_width=1.2)
    ic.path("M178 80 L192 96 L198 80", fill="#000", opacity=0.07)
    ic.line(58, 80.8, 198, 80.8, stroke="#fff", stroke_width=1.6)
    ic.rect(58, 80, 140, 10, fill="#E2DCD0")
    # the near handle, rope through two eyelets
    for x in (88, 148):
        ic.circle(x, 98, 4, fill=steel(ic, horizontal=False))
        ic.circle(x, 98, 1.8, fill="#2A2C30")
    ic.path("M88 98 C86 46 150 46 148 98", fill="none", stroke="#000", stroke_opacity=0.25, stroke_width=7,
            transform="translate(1 3)")
    ic.path("M88 98 C86 46 150 46 148 98", fill="none", stroke="#E07A2C", stroke_width=6.4, stroke_linecap="round")
    ic.path("M89 90 C88 56 120 50 136 58", fill="none", stroke="#FFC48A", stroke_width=1.6, stroke_linecap="round",
            opacity=0.8)
    # the print: a bag mark in a blue roundel, and the name
    ic.circle(118, 150, 30, fill="#3584E4")
    ic.circle(118, 150, 30, fill="none", stroke="#1C5AAE", stroke_width=2)
    ic.path("M105 142H131L128 166H108z", fill="#FFFFFF")
    ic.path("M111 142v-3a7 7 0 0 1 14 0v3", fill="none", stroke="#FFFFFF", stroke_width=2.6)
    ic.path("M114 152l4 4 4-4M118 147v9", fill="none", stroke="#3584E4", stroke_width=2.2, stroke_linecap="round",
            stroke_linejoin="round")
    ic.text("Software", 118, 199, 14, font="sans-semibold", anchor="middle", fill="#2A2C30")


@small("gnome-software")
def software16(ic):
    tile(ic, "#C47A36", "#743A12")
    ic.path("M5.5 6 C5.3 2 10.7 2 10.5 6", fill="none", stroke="#E07A2C", stroke_width=1.1)
    ic.path("M3.5 5.5H12.5L13.3 13.5H2.7z", fill="#FFFFFF")
    ic.circle(8, 9.5, 2.6, fill="#3584E4")
    ic.rect(6.8, 8.6, 2.4, 2, fill="#FFFFFF")


# --- Discover: a blue gift box, tied with a white ribbon -------------------

@icon("discover", kind="app", names=["discover", "org.kde.discover", "plasmadiscover"], title="Discover")
def discover(ic):
    tile(ic, "#2B3D5A", "#0F1828")
    shadow(ic, 128, 210, 100, 13)
    p = _iso(128, 104, 0.92)
    W, D, H = 104, 104, 70
    blue_top = ic.lin([(0, "#7CC4FA"), (1, "#3DAEE9")], 0, 0, 1, 1)
    # the box
    top, left, right = _faces(p, 0, 0, 0, W, D, H)
    ic.path(_pts(left), fill=ic.lin([(0, "#2FA0EC"), (1, "#1D7FC8")]))
    ic.path(_pts(right), fill=ic.lin([(0, "#1878BE"), (1, "#0F5590")]))
    # the lid, a little wider, and its lip
    lt, ll, lr = _faces(p, -4, -4, H - 16, W + 8, D + 8, 18)
    ic.path(_pts(ll), fill=ic.lin([(0, "#55B8F5"), (1, "#2C95DF")]))
    ic.path(_pts(lr), fill=ic.lin([(0, "#2386CE"), (1, "#16679F")]))
    ic.path(_pts(lt), fill=blue_top)
    ic.line(*lt[3], *lt[0], stroke="#fff", stroke_opacity=0.5, stroke_width=1.4)
    ic.line(*ll[3], *ll[2], stroke="#000", stroke_opacity=0.25, stroke_width=2)
    # the ribbon, round the box on both axes
    rib, rib_dark = "#FFFFFF", "#D6DEE8"
    for face, (x, y, z, w, d, h), lt_ in (("left", (-4, -4, H - 16, W + 8, D + 8, 18), rib),
                                          ("right", (-4, -4, H - 16, W + 8, D + 8, 18), rib_dark),
                                          ("left", (0, 0, 0, W, D, H - 16), rib),
                                          ("right", (0, 0, 0, W, D, H - 16), rib_dark)):
        with ic.g(transform=_on(p, face, x, y, z, w, d, h)):
            span = w if face == "left" else d
            ic.rect(span / 2 - 8, 0, 16, h, fill=lt_)
            ic.rect(span / 2 - 8, 0, 1.4, h, fill="#000", opacity=0.08)
    with ic.g(transform=_on(p, "top", -4, -4, H - 16, W + 8, D + 8, 18)):
        ic.rect((W + 8) / 2 - 8, 0, 16, D + 8, fill="#F4F8FC")
        ic.rect(0, (D + 8) / 2 - 8, W + 8, 16, fill="#FFFFFF")
    # a tag, the mark's bag printed on it
    with ic.g(transform=_on(p, "left", 0, 0, 0, W, D, H - 16)):
        ic.rect(12, 10, 30, 24, rx=2, fill="#F7F9FB")
        ic.circle(16, 22, 1.6, fill="#1D7FC8")
        ic.path("M23 17h15l-1.6 12h-11.8z", fill="#1D99F3")
        ic.path("M26 17v-2a4.5 4.5 0 0 1 9 0v2", fill="none", stroke="#1D99F3", stroke_width=1.6)
        ic.text("for you", 66, 30, 9, font="hand", anchor="middle", fill="#FFFFFF", opacity=0.9)
    # the bow, two loops and the knot
    cx, cy = p((W) / 2, (D) / 2, H + 2)
    ic.ellipse(cx + 2, cy + 4, 34, 10, fill="#000", opacity=0.2)
    for sx in (-1, 1):
        ic.path(f"M{cx} {cy}C{cx + sx * 12} {cy - 34} {cx + sx * 44} {cy - 22} {cx + sx * 28} {cy - 4}"
                f"C{cx + sx * 22} {cy + 2} {cx + sx * 8} {cy + 2} {cx} {cy}z",
                fill=ic.lin([(0, "#FFFFFF"), (1, "#C9D4E2")], 0, 0, 1, 1), stroke="#B4C2D4", stroke_width=1)
        ic.path(f"M{cx} {cy}C{cx + sx * 8} {cy - 18} {cx + sx * 24} {cy - 18} {cx + sx * 22} {cy - 8}",
                fill="none", stroke="#9FB0C6", stroke_width=1.2)
        ic.path(f"M{cx} {cy + 2}L{cx + sx * 14} {cy + 24}L{cx + sx * 20} {cy + 18}z", fill="#E8EEF5",
                stroke="#B4C2D4", stroke_width=1)
    ic.ellipse(cx, cy, 8, 6.5, fill=ic.lin([(0, "#FFFFFF"), (1, "#D0DAE6")]), stroke="#B4C2D4", stroke_width=1)


@small("discover")
def discover16(ic):
    tile(ic, "#2B3D5A", "#0F1828")
    ic.rect(3, 7, 10, 7, fill="#1D99F3")
    ic.rect(2.5, 5, 11, 2.6, fill="#5BB8F5")
    ic.rect(7.2, 5, 1.6, 9, fill="#FFFFFF")
    ic.path("M8 5 C6 2 3.5 3 5 5z M8 5 C10 2 12.5 3 11 5z", fill="#FFFFFF")


# --- Synaptic: a grey carton, taped in red, a package arrow on it ----------

@icon("synaptic", kind="app", names=["synaptic"], title="Synaptic")
def synaptic(ic):
    tile(ic, "#A13A30", "#521610")
    shadow(ic, 128, 208, 96, 12)
    p = _iso(128, 92, 0.98)
    W, D, H = 100, 76, 76
    top, left, right = _faces(p, 0, 0, 0, W, D, H)
    ic.path(_pts(left), fill=ic.lin([(0, "#D9DCE0"), (1, "#B3B8BF")]))
    ic.path(_pts(right), fill=ic.lin([(0, "#9BA1A9"), (1, "#737981")]))
    ic.path(_pts(top), fill=ic.lin([(0, "#F1F2F4"), (1, "#D5D8DC")], 0, 0, 1, 1))
    # the flaps' seam and the red tape over it, down both ends
    with ic.g(transform=_on(p, "top", 0, 0, 0, W, D, H)):
        ic.rect(0, D / 2 - 0.6, W, 1.2, fill="#8A9099")
        ic.rect(0, D / 2 - 9, W, 18, fill="#D8382C")
        ic.rect(0, D / 2 - 9, W, 2, fill="#fff", opacity=0.3)
    with ic.g(transform=_on(p, "right", 0, 0, 0, W, D, H)):
        ic.rect(D / 2 - 9, 0, 18, 22, fill="#A82418")
        ic.path(f"M{D / 2 - 9} 22l3 2 3-2 3 2 3-2 3 2 3-2v-1h-18z", fill="#A82418")
    ic.line(*top[3], *top[0], stroke="#fff", stroke_width=1.4, opacity=0.8)
    ic.line(*left[0], *left[1], stroke="#fff", stroke_width=1, opacity=0.5)
    # the front: the mark's arrow down into a tray, printed in red
    with ic.g(transform=_on(p, "left", 0, 0, 0, W, D, H)):
        ic.rect(10, 9, 44, 50, rx=4, fill="none", stroke="#D8382C", stroke_width=2.4)
        ic.path("M24 14h16v16h9L32 47 15 30h9z", fill="#D8382C")
        ic.path("M16 50v4h32v-4", fill="none", stroke="#D8382C", stroke_width=2.6, stroke_linecap="round")
        ic.text("synaptic", 77, 22, 9.5, font="sans-bold", anchor="middle", fill="#3A3E45")
        ic.text("package", 77, 33, 6.5, font="mono", anchor="middle", fill="#5D636B")
        ic.text(".deb", 77, 42, 6.5, font="mono", anchor="middle", fill="#5D636B")
        for i in range(11):
            ic.rect(62 + i * 2.6, 50, 1.2 if i % 3 else 1.8, 14, fill="#2A2C30", opacity=0.8)
    with ic.g(transform=_on(p, "right", 0, 0, 0, W, D, H)):
        ic.rect(14, 30, 48, 30, rx=2, fill="#F7F7F5", opacity=0.92)
        ic.text("TO: /usr", 20, 42, 6.5, font="mono-semibold", fill="#2A2C30")
        ic.text("apt 2.9", 20, 52, 6, font="mono", fill="#5D636B")
    ic.line(*left[3], *left[2], stroke="#000", stroke_opacity=0.25, stroke_width=1.5)


@small("synaptic")
def synaptic16(ic):
    tile(ic, "#A13A30", "#521610")
    ic.path("M8 2.5 L14 5.5 V11.5 L8 14.5 L2 11.5 V5.5z", fill="#B3B8BF")
    ic.path("M8 2.5 L14 5.5 L8 8.5 L2 5.5z", fill="#EEF0F2")
    ic.path("M8 8.5 L14 5.5 V11.5 L8 14.5z", fill="#848A92")
    ic.path("M4.8 2.9 L10.8 5.9 L11.4 5.6 L5.4 2.6z", fill="#D8382C")
    ic.path("M4.2 7.6 V9.4 H3 L5 12.2 L7 9.4 H5.8 V7.6z", fill="#D8382C")


# --- Boxes: open boxes nested one in another ---------------------------------

def _open_box(ic, p, s, z, h, inset, front):
    """An open box of side s, its floor at z, height h; inset its offset
    from the origin. Draws the back (front=False) or the front walls."""
    o = inset
    if not front:
        # the inside: the two back walls' inner faces and the floor
        back_l = [p(o, o, z + h), p(o, o + s, z + h), p(o, o + s, z), p(o, o, z)]
        back_r = [p(o, o, z + h), p(o + s, o, z + h), p(o + s, o, z), p(o, o, z)]
        floor = [p(o, o, z), p(o + s, o, z), p(o + s, o + s, z), p(o, o + s, z)]
        ic.path(_pts(back_l), fill=ic.lin([(0, "#C9661A"), (1, "#A44E10")]))
        ic.path(_pts(back_r), fill=ic.lin([(0, "#E07C26"), (1, "#B85A12")]))
        ic.path(_pts(floor), fill="#9A4A0E")
        ic.line(*p(o, o, z + h), *p(o, o, z), stroke="#7A3A08", stroke_width=1, opacity=0.6)
        return
    _, left, right = _faces(p, o, o, z, s, s, h)
    ic.path(_pts(left), fill=ic.lin([(0, "#FFB25C"), (1, "#F08A2C")]))
    ic.path(_pts(right), fill=ic.lin([(0, "#D8711E"), (1, "#B0540E")]))
    # the rim, the walls' thickness lit from above
    rim = [p(o, o + s, z + h), p(o + s, o + s, z + h), p(o + s, o, z + h)]
    ic.path("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in rim), fill="none", stroke="#FFE2B8", stroke_width=2.6,
            stroke_linejoin="round", stroke_linecap="round")
    ic.path("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in (p(o, o + s, z + h), p(o, o, z + h), p(o + s, o, z + h))),
            fill="none", stroke="#FFD49A", stroke_width=2.6, stroke_linejoin="round", stroke_linecap="round")


@icon("gnome-boxes", kind="app", names=["gnome-boxes", "org.gnome.Boxes"], title="Boxes")
def boxes(ic):
    tile(ic, "#4E3E66", "#211833")
    shadow(ic, 128, 210, 100, 12)
    p = _iso(128, 92, 0.9)
    sizes = [(120, 0, 62, 0), (88, 8, 50, 16), (56, 16, 30, 32)]
    for s_, z, h, o in sizes:
        _open_box(ic, p, s_, z, h, o, False)
    # the innermost holds a screen: a little desktop glowing on its floor
    ic.path(_pts([p(38, 38, 16), p(82, 38, 16), p(82, 82, 16), p(38, 82, 16)]), fill="#1E2A3E")
    ic.path(_pts([p(42, 42, 16), p(78, 42, 16), p(78, 78, 16), p(42, 78, 16)]),
            fill=ic.lin([(0, "#7FB8F0"), (1, "#2D5E9A")], 0, 0, 1, 1))
    ic.path(_pts([p(42, 42, 16), p(78, 42, 16), p(78, 48, 16), p(42, 48, 16)]), fill="#F6F8FB", opacity=0.8)
    for s_, z, h, o in reversed(sizes):
        _open_box(ic, p, s_, z, h, o, True)
    with ic.g(transform=_on(p, "left", 0, 0, 0, 120, 120, 62)):
        ic.text("Boxes", 60, 38, 13, font="sans-bold", anchor="middle", fill="#8A3E06", opacity=0.75)
    with ic.g(transform=_on(p, "right", 0, 0, 0, 120, 120, 62)):
        ic.text("THIS WAY UP", 60, 36, 7, font="sans-condensed", anchor="middle", spacing=0.8, fill="#6A2E04",
                opacity=0.7)


@small("gnome-boxes")
def boxes16(ic):
    tile(ic, "#4E3E66", "#211833")
    ic.rect(2, 2, 12, 12, rx=1, fill="#F08A2C")
    ic.rect(3.5, 3.5, 9, 9, rx=0.6, fill="#9A4A0E")
    ic.rect(5, 5, 6, 6, rx=0.6, fill="#FFB25C")
    ic.rect(6.5, 6.5, 3, 3, fill="#9A4A0E")


# --- Camera (Snapshot): a lens standing on its cap, glass up ----------------

@icon("snapshot", kind="app", names=["org.gnome.Snapshot", "snapshot"], title="Camera")
def snapshot(ic):
    tile(ic, "#8494A8", "#3E4A5C")
    shadow(ic, 128, 214, 84, 12)
    cx, rx, ry = 128, 74, 28
    barrel = ic.lin([(0, "#0E0F11"), (0.25, "#3A3E45"), (0.42, "#55595F"), (0.6, "#2A2D32"), (1, "#0C0D0F")],
                    0, 0, 1, 0)
    ribbed = ic.lin([(0, "#151618"), (0.3, "#4A4E55"), (0.45, "#5E636A"), (0.65, "#2C2F34"), (1, "#101113")],
                    0, 0, 1, 0)

    def band(y0, y1, r, fill):
        ic.path(f"M{cx - r} {y0}A{r} {ry * r / rx} 0 0 0 {cx + r} {y0}V{y1}A{r} {ry * r / rx} 0 0 1 {cx - r} {y1}z",
                fill=fill)
    # the rear cap and the mount
    band(186, 202, 64, barrel)
    band(176, 188, 70, ic.lin([(0, "#7A8088"), (0.4, "#D0D4DA"), (1, "#5A6068")], 0, 0, 1, 0))
    # the body, the zoom ring (ribbed), the focus ring with its scale
    band(150, 178, rx, barrel)
    band(104, 150, rx, ribbed)
    for k in range(-34, 35):
        x = cx + rx * (k / 35)
        ic.line(x, 104 + ry * (1 - (k / 35) ** 2) ** 0.5, x, 150 + ry * (1 - (k / 35) ** 2) ** 0.5,
                stroke="#000", stroke_width=1.1, opacity=0.35)
    band(80, 104, rx, barrel)
    ic.path(f"M{cx - rx} 104A{rx} {ry} 0 0 0 {cx + rx} 104", fill="none", stroke="#fff", stroke_opacity=0.15,
            stroke_width=1.2)
    ic.path(f"M{cx - rx} 150A{rx} {ry} 0 0 0 {cx + rx} 150", fill="none", stroke="#fff", stroke_opacity=0.15,
            stroke_width=1.2)
    for t, deg in (("∞", -40), ("3", -16), ("1.5", 8), ("0.8", 30)):
        x = cx + rx * math.sin(math.radians(deg)) * 1.0
        y = 80 + 12 + ry * math.cos(math.radians(deg)) * 0.9
        if t == "∞":
            ic.path(f"M{x - 5} {y}c0-3 4-3 5 0s5 3 5 0-4-3-5 0-5 3-5 0z", fill="none", stroke="#E9ECF0",
                    stroke_width=1.2, transform=f"translate(0 -3)")
        else:
            ic.text(t, x, y, 8, font="mono-semibold", anchor="middle", fill="#E9ECF0")
    ic.text("24–70 mm  1:2.8", cx, 172 + ry * 0.9, 8, font="mono-semibold", anchor="middle", fill="#C9CED6")
    ic.path(f"M{cx - 4} {80 + ry + 6}l4 5 4-5z", fill="#4A90D9")
    # the front: a ring, then the glass, coated, the iris deep in it
    ic.ellipse(cx, 80, rx, ry, fill=ic.lin([(0, "#6A6F77"), (1, "#1A1C20")]))
    ic.ellipse(cx, 80, rx - 4, ry - 2, fill="#0A0B0D")
    ic.ellipse(cx, 81, rx - 10, ry - 5, fill=ic.rad([(0, "#2B3A6E"), (0.5, "#151B3A"), (1, "#050609")],
                                                   cx=0.45, cy=0.5, r=0.6))
    ic.ellipse(cx, 82, 34, 12.5, fill="none", stroke="#6A4CC8", stroke_opacity=0.5, stroke_width=2)
    ic.ellipse(cx, 82, 22, 8, fill="#020203")
    ic.ellipse(cx, 82, 22, 8, fill="none", stroke="#3FBF9A", stroke_opacity=0.45, stroke_width=1.5)
    ic.path(f"M{cx - 50} 78a52 18 0 0 1 40-13c-14 3-28 8-34 16z", fill="#fff", opacity=0.55)
    ic.ellipse(cx + 26, 88, 8, 3, fill="#C8A2FF", opacity=0.35)
    ic.ellipse(cx - 10, 74, 4, 1.6, fill="#fff", opacity=0.7)


@small("snapshot")
def snapshot16(ic):
    tile(ic, "#8494A8", "#3E4A5C")
    ic.path("M2.5 7 V12.2 A5.5 2 0 0 0 13.5 12.2 V7z", fill="#24272C")
    ic.rect(2.5, 9, 11, 2, fill="#4A4E55")
    ic.ellipse(8, 7, 5.5, 3, fill="#6A7078")
    ic.ellipse(8, 7, 4.4, 2.3, fill="#2B3A8E")
    ic.ellipse(8, 7.1, 2, 1, fill="#05060A")
    ic.ellipse(6.3, 6.1, 1.3, 0.5, fill="#fff", opacity=0.8)


# --- Cheese: a wedge of cheese, a photo-booth flash going off over it ------

@icon("cheese", kind="app", names=["camorama", "cheese", "kamerka", "org.gnome.Cheese"], title="Cheese")
def cheese(ic):
    tile(ic, "#6B3C8C", "#30174A")
    shadow(ic, 124, 204, 104, 12)
    # a strip of photo-booth prints, leaning at the back
    with ic.g(transform="rotate(-9 64 90)"):
        ic.rect(44, 30, 38, 104, rx=2, fill="#000", opacity=0.3, transform="translate(2 4)")
        ic.rect(44, 30, 38, 104, rx=2, fill=paper(ic, "white"))
        for i in range(3):
            y = 35 + i * 31
            ic.rect(48, y, 30, 27, fill=ic.lin([(0, "#9A6AC0"), (1, "#4A2A6A")]))
            ic.circle(63, y + 12, 6.5, fill="#F6D28A")
            ic.path(f"M52 {y + 27}a11 9 0 0 1 22 0z", fill="#F6D28A")
            mouth = ("M60 {0}q3 3 6 0", "M60 {0}h6", "M59 {0}q4 5 8 0")[i]
            ic.path(mouth.format(y + 14.5), fill="none", stroke="#5A3A10", stroke_width=1.2, stroke_linecap="round")
    # the flash: a reflector dish on its stalk, firing
    fx, fy = 182, 58
    for a in range(-160, 41, 25):
        x1, y1 = polar(fx, fy, 36, a)
        x2, y2 = polar(fx, fy, 50, a)
        ic.line(x1, y1, x2, y2, stroke="#FFF4B0", stroke_width=3.6, stroke_linecap="round", opacity=0.85)
    ic.circle(fx, fy, 40, fill=ic.rad([(0, "#FFFBE0", 0.55), (1, "#FFFBE0", 0)]))
    ic.path(f"M{fx - 3} {fy + 26}h7l3 40h-13z", fill=steel(ic))
    ic.circle(fx + 1, fy + 3, 28, fill="#000", opacity=0.3)
    ic.circle(fx, fy, 28, fill=ic.lin([(0, "#F1F3F6"), (0.5, "#A9B0B9"), (1, "#5D636B")], 0, 0, 1, 1))
    ic.circle(fx, fy, 23, fill=ic.rad([(0, "#FFFFFF"), (0.4, "#E6EAF0"), (1, "#8A9099")], cx=0.45, cy=0.45, r=0.6))
    for a in range(0, 360, 30):
        x, y = polar(fx, fy, 22, a)
        ic.line(fx, fy, x, y, stroke="#8A9099", stroke_width=0.8, opacity=0.5)
    ic.circle(fx, fy, 9, fill=ic.rad([(0, "#FFFFFF"), (0.6, "#FFF6C8"), (1, "#E8D27A")]))
    ic.circle(fx - 3, fy - 3, 2.6, fill="#fff")
    # the wedge: its point to the left, the cut face toward us, the rind at the right
    L, F, R = (24, 128), (148, 156), (210, 108)
    h = 52
    Lb, Fb, Rb = (L[0], L[1] + h), (F[0], F[1] + h), (R[0], R[1] + h)
    cut = [L, F, Fb, Lb]
    ic.path(_pts(cut), fill=ic.lin([(0, "#FFE27A"), (1, "#F0B830")]))
    ic.path(f"M{F[0]} {F[1]}Q{186} {138} {R[0]} {R[1]}V{Rb[1]}Q{186} {138 + h} {Fb[0]} {Fb[1]}z",
            fill=ic.lin([(0, "#E8A21C"), (1, "#B8740A")], 0, 0, 1, 1))
    ic.path(f"M{F[0]} {F[1] + 3}Q{186} {141} {R[0]} {R[1] + 3}", fill="none", stroke="#FFD460",
            stroke_width=2.4, opacity=0.6)
    ic.path(f"M{L[0]} {L[1]}L{F[0]} {F[1]}Q186 138 {R[0]} {R[1]}z",
            fill=ic.lin([(0, "#FFF4B8"), (1, "#FFDC66")], 0, 0, 1, 1))
    ic.line(*L, *F, stroke="#FFF8D0", stroke_width=1.8)
    ic.line(*F, *Fb, stroke="#FFF2A8", stroke_width=1.4, opacity=0.8)
    # the holes: cut through on the face, cupped on the top, nicked on the edges
    for u, v, r in ((0.28, 0.42, 8), (0.58, 0.28, 6), (0.72, 0.66, 10), (0.12, 0.72, 4.5), (0.44, 0.8, 5),
                    (0.9, 0.3, 4)):
        x, y = _bilerp(cut, u, v)
        ic.ellipse(x, y, r * 0.95, r, fill="#D8A020", transform=f"rotate(12 {x:.1f} {y:.1f})")
        ic.ellipse(x + 1.2, y + 1.4, r * 0.7, r * 0.72, fill="#A86E08", transform=f"rotate(12 {x:.1f} {y:.1f})")
    for x, y, r in ((96, 130, 9), (150, 124, 6), (176, 122, 4.5), (70, 132, 4)):
        ic.ellipse(x, y, r * 1.3, r * 0.6, fill="#E8B83A")
        ic.ellipse(x + 1, y + 0.8, r * 1.0, r * 0.42, fill="#C08612")
    ic.path("M112 140.4a8 8 0 0 0 16 3.2", fill="#E8B83A")
    ic.path("M112 140.4a8 8 0 0 0 16 3.2", fill="none", stroke="#B07408", stroke_width=1)


@small("cheese")
def cheese16(ic):
    tile(ic, "#6B3C8C", "#30174A")
    ic.circle(11.5, 4.5, 2.6, fill="#FFF6C8")
    ic.circle(11.5, 4.5, 3.6, fill="none", stroke="#FFF4B0", stroke_width=0.6, opacity=0.7)
    ic.path("M1.5 9.5 L11 7 L13.5 9.5 V13.5 H1.5z", fill="#F2BE3A")
    ic.path("M1.5 9.5 L11 7 L13.5 9.5z", fill="#FFE27A")
    ic.circle(5, 11.5, 1, fill="#B57A0C")
    ic.circle(9.5, 12, 0.8, fill="#B57A0C")
