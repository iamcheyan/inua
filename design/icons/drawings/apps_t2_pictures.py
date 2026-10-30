"""The inua-objects theme, pictures: Pinta, Image Viewer (Loupe), Eye of
GNOME, Gwenview, Shotwell, digiKam, RawTherapee, Hugin, Flameshot, ksnip,
Kooha, Upscayl (docs/feat/object-icons.md, Part 2). Each is its own object:
a tin, a loupe, a frame, an album, a shoebox, a camera's back, a negative on
a light box, a panorama, an iris, scissors, a camcorder and a magnifier."""

from lib import (brass, glare, graphite, icon, paper, polar, shadow, small, steel, tile, wood)


def _arc_text(ic, s, cx, cy, r, deg, size, **kw):
    """A word set on a ring, upright along the radius at angle deg."""
    with ic.g(transform=f"rotate({deg} {cx} {cy})"):
        ic.text(s, cx, cy - r, size, anchor="middle", **kw)


def _land(ic, x, y, w, h, sky=("#6FA6D6", "#E6EEE6"), far="#7F95AC", near="#3D7A4C", water=None,
          sun="#FFF3C8", snow=True):
    """A landscape photograph filling x, y, w, h: sky, sun, a far range, a
    green near hill, maybe a lake. Drawn on a 100 x 70 grid, stretched."""
    clip = ic.clip(f'<rect x="{x}" y="{y}" width="{w}" height="{h}"/>')
    with ic.g(clip_path=clip):
        with ic.g(transform=f"translate({x} {y}) scale({w / 100:.4f} {h / 70:.4f})"):
            ic.rect(0, 0, 100, 70, fill=ic.lin([(0, sky[0]), (1, sky[1])]))
            if sun:
                ic.circle(74, 16, 6.5, fill=sun)
                ic.circle(74, 16, 10, fill=sun, opacity=0.25)
            ic.path("M0 44 L16 30 L26 36 L42 18 L52 26 L60 20 L78 34 L90 28 L100 34 L100 50 L0 50z",
                    fill=ic.lin([(0, far), (1, "#3E4F63")], 0, 0, 1, 1))
            if snow:
                ic.path("M36 25 L42 18 L52 26 L60 20 L66 25 L60 24 L55 29 L50 26 L45 30 L42 25z", fill="#F7FAFC")
            if water:
                ic.path("M0 46 Q20 40 40 45 T80 44 T100 45 L100 52 L0 52z", fill=near)
                ic.rect(0, 51, 100, 19, fill=ic.lin([(0, water[0]), (1, water[1])]))
                for yy in (56, 61, 66):
                    ic.line(6, yy, 94, yy, stroke="#fff", stroke_opacity=0.2, stroke_dasharray="9 6")
            else:
                ic.path("M0 50 Q30 38 60 46 T100 44 L100 70 L0 70z",
                        fill=ic.lin([(0, near), (1, "#22472C")]))
                ic.path("M0 58 Q40 50 100 60 L100 70 L0 70z", fill="#1E3E26", opacity=0.6)


def _screw(ic, x, y, r=2.6):
    ic.circle(x, y, r, fill=steel(ic, horizontal=False))
    ic.line(x - r * 0.6, y + r * 0.35, x + r * 0.6, y - r * 0.35, stroke="#3C4148", stroke_width=0.8)


# --- Pinta: an open tin of paint, a brush resting in it ----------------------

@icon("pinta", kind="app", names=["colors", "com.github.PintaProject.Pinta", "gnome-paint", "kcoloredit", "kipi",
                                  "kipi-logo", "mypaint", "org.mypaint.MyPaint", "pinta"], title="Pinta")
def pinta(ic):
    tile(ic, "#3F6394", "#182C4B")
    shadow(ic, 120, 210, 90, 12)
    cx, top, bot, rx, ry = 116, 104, 196, 64, 18
    # the bail, lowered behind
    ic.path(f"M{cx - rx + 2} 118 Q{cx} 34 {cx + rx - 2} 118", fill="none", stroke="#2A2E35", stroke_width=3.2)
    ic.path(f"M{cx - rx + 2} 118 Q{cx} 34 {cx + rx - 2} 118", fill="none", stroke="#C3C8CE", stroke_width=1.6)
    # the tin
    ic.path(f"M{cx - rx} {top} V{bot} A{rx} {ry} 0 0 0 {cx + rx} {bot} V{top}z", fill=steel(ic))
    ic.path(f"M{cx - rx} {bot - 4} A{rx} {ry} 0 0 0 {cx + rx} {bot - 4}", fill="none", stroke="#000",
            stroke_opacity=0.25, stroke_width=1.5)
    # the label, wrapped round
    ic.path(f"M{cx - rx} 128 A{rx} {ry} 0 0 0 {cx + rx} 128 V178 A{rx} {ry} 0 0 1 {cx - rx} 178z",
            fill=ic.lin([(0, "#5A84C0"), (0.35, "#2F5C9E"), (1, "#173A6E")], 0, 0, 1, 0))
    ic.path(f"M{cx - rx} 134 A{rx} {ry} 0 0 0 {cx + rx} 134 V170 A{rx} {ry} 0 0 1 {cx - rx} 170z",
            fill=ic.lin([(0, "#FFF8EA"), (0.4, "#F2EAD8"), (1, "#B8AE98")], 0, 0, 1, 0))
    # the mark: a swatch fan of four colours, pressed on the label
    with ic.g(transform="translate(76 182)"):
        for k, c in enumerate(("#E8432C", "#F29A2E", "#F4D03F", "#3D8FD9")):
            ic.path("M0 0 L-4 -30 a5 5 0 0 1 8 0z", fill=c, transform=f"rotate({-36 + k * 24})")
        ic.circle(0, 0, 3, fill="#2A2E35")
    ic.text("PINTA", 96, 175, 15, font="sans-bold", spacing=1.2, fill="#1E3B66")
    ic.text("gloss · 0.5 L", 97, 184, 6.5, font="mono", fill="#5E5A52")
    ic.text("Vermilion", 97, 162, 7.5, font="sans-semibold", fill="#C8371F")
    # the rim and the paint
    ic.ellipse(cx, top, rx, ry, fill=ic.lin([(0, "#E6E9EC"), (1, "#7C838B")], 0, 0, 1, 1))
    ic.ellipse(cx, top + 1, rx - 6, ry - 4.5, fill="#4D535A")
    ic.ellipse(cx, top + 2, rx - 7, ry - 5.5,
               fill=ic.rad([(0, "#FF7A50"), (0.6, "#E8432C"), (1, "#A82612")], cx=0.4, cy=0.35, r=0.7))
    ic.ellipse(cx - 22, top - 2, 16, 3.5, fill="#fff", opacity=0.35)
    # drips over the rim and down the label
    ic.path(f"M{cx + 42} {top + 11} q4 1 8 -1 v26 a4 4 0 0 1 -8 0z", fill="#E2402A")
    ic.path(f"M{cx + 43.5} {top + 14} v20", stroke="#fff", stroke_opacity=0.4, stroke_width=1.2,
            stroke_linecap="round")
    ic.path(f"M{cx - 50} {top + 9} q3 1.5 6 1 v8 a3 3 0 0 1 -6 0z", fill="#E2402A")
    ic.line(cx - rx + 4, top + 4, cx - rx + 4, bot - 4, stroke="#fff", stroke_opacity=0.35, stroke_width=2)
    # the brush, its bristles in the paint, its handle up to the right
    with ic.g(transform=f"translate({cx + 14} {top + 2}) rotate(38)"):
        ic.path("M-13 0 Q-14 -14 -11 -26 H11 Q14 -14 13 0 Q0 4 -13 0z", fill="#3A2A20")
        ic.path("M-13 0 Q-14 -8 -12.5 -12 H12.5 Q14 -8 13 0 Q0 4 -13 0z", fill="#E2402A")
        for k in range(-9, 10, 3):
            ic.line(k, -24, k * 1.08, -12, stroke="#6B5444", stroke_width=0.8)
        ic.rect(-12, -46, 24, 21, rx=2, fill=steel(ic))
        for yy in (-41, -35, -30):
            ic.line(-12, yy, 12, yy, stroke="#000", stroke_opacity=0.25)
        ic.path("M-9 -46 L-6 -128 a6 6 0 0 1 12 0 L9 -46z", fill=wood(ic, "#E09A5C", "#8A4E22"))
        ic.path("M-6.5 -50 L-4 -124", stroke="#fff", stroke_opacity=0.35, stroke_width=1.6, stroke_linecap="round")
        ic.circle(0, -116, 2.4, fill="#2A1A10")


@small("pinta")
def pinta16(ic):
    tile(ic, "#3F6394", "#182C4B")
    ic.path("M3 7 V13 a5 1.6 0 0 0 10 0 V7z", fill="#B9BEC5")
    ic.path("M3 8.5 a5 1.6 0 0 0 10 0 V11.5 a5 1.6 0 0 1 -10 0z", fill="#2F5C9E")
    ic.ellipse(8, 7, 5, 1.7, fill="#E8432C")
    ic.path("M8.6 6.6 L13.4 1.8", stroke="#C98A4E", stroke_width=1.6, stroke_linecap="round")
    ic.path("M7.8 7.4 L9.4 5.8", stroke="#3A2A20", stroke_width=2.2)


# --- Image Viewer (Loupe): a photographer's stand loupe on a print ---------

@icon("loupe", kind="app", names=["loupe", "org.gnome.Loupe"], title="Image Viewer")
def loupe(ic):
    tile(ic, "#4B86C8", "#1D4170")
    shadow(ic, 124, 210, 98, 12)
    land = dict(sky=("#5C9BE0", "#DCEBF5"), far="#8399B5", near="#4E9A4A", sun="#FFE58A")
    # the print, lying on the desk
    with ic.g(transform="rotate(-7 118 140)"):
        ic.rect(30, 68, 170, 132, rx=3, fill="#000", opacity=0.3, transform="translate(3 4)")
        ic.rect(30, 68, 170, 132, rx=3, fill=paper(ic, "white"))
        ic.line(31, 69, 199, 69, stroke="#fff", stroke_width=1.5)
        _land(ic, 40, 78, 150, 106, **land)
        ic.rect(40, 78, 150, 106, fill="none", stroke="#000", stroke_opacity=0.12)
        ic.text("Loupe", 44, 195, 9, font="hand", fill="#6A665D")
    # the loupe: clear skirt, black barrel, chrome eye ring, glass on top
    cx, ty, by = 140, 84, 170
    ic.ellipse(cx + 4, by + 4, 54, 22, fill="#000", opacity=0.25)
    skirt = f"M{cx - 44} 118 L{cx - 50} {by} A50 20 0 0 0 {cx + 50} {by} L{cx + 44} 118z"
    ic.path(skirt, fill="#E8F2FA", opacity=0.22)
    ic.path(skirt, fill=ic.lin([(0, "#fff", 0.5), (0.25, "#fff", 0.05), (0.8, "#fff", 0), (1, "#fff", 0.35)],
                               0, 0, 1, 0))
    ic.ellipse(cx, by, 50, 20, fill="none", stroke="#1E2228", stroke_width=4)
    ic.ellipse(cx, by - 1, 50, 20, fill="none", stroke="#fff", stroke_opacity=0.3, stroke_width=1)
    ic.line(cx - 47, 122, cx - 50, by - 4, stroke="#fff", stroke_opacity=0.7, stroke_width=1.6)
    ic.path(f"M{cx - 44} {ty} V118 A44 18 0 0 0 {cx + 44} 118 V{ty}z", fill=graphite(ic))
    ic.path(f"M{cx - 44} 112 A44 18 0 0 0 {cx + 44} 112", fill="none", stroke="#fff", stroke_opacity=0.15)
    for k in range(-40, 44, 5):
        ic.line(cx + k, ty + 14 + 0.004 * k * k * 4, cx + k, ty + 30 + 0.004 * k * k * 4, stroke="#000",
                stroke_opacity=0.35, stroke_width=1.2)
    ic.text("8×", cx + 24, 117, 9, font="mono-semibold", fill="#C9CED4", opacity=0.8)
    ic.ellipse(cx, ty, 44, 18, fill=ic.lin([(0, "#F2F4F6"), (0.5, "#9AA1A9"), (1, "#4D535A")], 0, 0, 1, 1))
    ic.ellipse(cx, ty, 37, 14.5, fill="#0C0D0F")
    lens = ic.clip(f'<ellipse cx="{cx}" cy="{ty}" rx="35" ry="13.5"/>')
    with ic.g(clip_path=lens):
        _land(ic, cx - 96, ty - 40, 200, 140, **land)
    ic.ellipse(cx, ty, 35, 13.5, fill=ic.rad([(0, "#fff", 0), (0.8, "#fff", 0), (1, "#000", 0.35)]))
    ic.ellipse(cx, ty, 35, 13.5, fill=glare(ic, 1.3))
    ic.path(f"M{cx - 28} {ty - 3}a28 10 0 0 1 24 -8 34 12 0 0 0 -24 8z", fill="#fff", opacity=0.7)


@small("loupe")
def loupe16(ic):
    tile(ic, "#4B86C8", "#1D4170")
    ic.rect(1.8, 6, 10, 8, rx=0.4, fill="#FFFFFF", transform="rotate(-7 7 10)")
    ic.rect(2.6, 6.8, 8.4, 6.4, fill="#79AEE6", transform="rotate(-7 7 10)")
    ic.path("M2.6 13 L6 9.6 L8 11 L11 9.4 V13z", fill="#4E9A4A", transform="rotate(-7 7 10)")
    ic.path("M7.2 4.6 V9 a3.6 1.4 0 0 0 7.2 0 V4.6z", fill="#2A2C30")
    ic.ellipse(10.8, 4.6, 3.6, 1.6, fill="#C9CED4")
    ic.ellipse(10.8, 4.6, 2.7, 1, fill="#8DC0F0")


# --- Eye of GNOME: an eye-shaped frame, a round photo for its iris ---------

@icon("eog", kind="app", names=["eog", "org.gnome.eog"], title="Eye of GNOME")
def eog(ic):
    tile(ic, "#4C6B78", "#1E323B")
    shadow(ic, 128, 208, 90, 11)
    cx, cy = 128, 118
    outer = f"M18 {cy} Q{cx} 4 238 {cy} Q{cx} 232 18 {cy}z"
    inner = f"M36 {cy} Q{cx} 30 220 {cy} Q{cx} 206 36 {cy}z"
    # the frame: walnut, a brass bevel, a cream mat
    ic.path(outer, fill="#000", opacity=0.3, transform="translate(3 5)")
    ic.path(outer, fill=wood(ic, "#9A6A42", "#4A2814"))
    ic.path(f"M18 {cy} Q{cx} 4 238 {cy}", fill="none", stroke="#E8C08C", stroke_opacity=0.5, stroke_width=2)
    ic.path(f"M29 {cy} Q{cx} 18 227 {cy} Q{cx} 218 29 {cy}z", fill=brass(ic))
    ic.path(inner, fill=ic.rad([(0, "#FFFFFF"), (0.7, "#F3EEE3"), (1, "#C9C0AE")], cx=0.45, cy=0.4, r=0.6))
    ic.path(f"M36 {cy} Q{cx} 30 220 {cy}", fill="none", stroke="#000", stroke_opacity=0.25, stroke_width=2.5)
    # the iris: a blue ring round a round photograph
    ic.circle(cx + 1.5, cy + 2.5, 47, fill="#000", opacity=0.2)
    ic.circle(cx, cy, 47, fill=ic.lin([(0, "#7FC0F2"), (0.5, "#2F78C8"), (1, "#163E7A")], 0, 0, 1, 1))
    for k in range(36):
        x1, y1 = polar(cx, cy, 36, k * 10)
        x2, y2 = polar(cx, cy, 45, k * 10 + 4)
        ic.line(x1, y1, x2, y2, stroke="#0E2A55", stroke_opacity=0.35, stroke_width=1.2)
    ic.circle(cx, cy, 47, fill="none", stroke="#0E2A55", stroke_width=2.5)
    photo = ic.clip(f'<circle cx="{cx}" cy="{cy}" r="34"/>')
    with ic.g(clip_path=photo):
        _land(ic, cx - 48, cy - 34, 96, 68, sky=("#3F6E9E", "#F2D6A8"), far="#5E6E8A", near="#3D6A4C",
              water=("#5D88A6", "#1E3E54"), sun="#FFE2A0")
    ic.circle(cx, cy, 34, fill="none", stroke="#0B1E3C", stroke_width=2)
    ic.circle(cx, cy, 34, fill=glare(ic, 1.2))
    # the catchlight on the glass
    ic.ellipse(cx - 16, cy - 18, 10, 6, fill="#fff", opacity=0.75, transform=f"rotate(-30 {cx - 16} {cy - 18})")
    ic.circle(cx + 18, cy + 16, 3, fill="#fff", opacity=0.35)


@small("eog")
def eog16(ic):
    tile(ic, "#4C6B78", "#1E323B")
    ic.path("M1 8 Q8 0.4 15 8 Q8 15.6 1 8z", fill="#7A4E2C")
    ic.path("M2.6 8 Q8 2.6 13.4 8 Q8 13.4 2.6 8z", fill="#F6F2EA")
    ic.circle(8, 8, 3.6, fill="#2F78C8")
    ic.circle(8, 8, 2.4, fill="#F2D6A8")
    ic.path("M5.6 8.6 L7.4 7 L9 8.2 L10.4 7.4 V9.6 H5.6z", fill="#3D6A4C")


# --- Gwenview: a cloth-bound photo album, a print in corners on its cover ---

@icon("gwenview", kind="app", names=["gwenview", "org.kde.gwenview"], title="Gwenview")
def gwenview(ic):
    tile(ic, "#5E6E80", "#25303C")
    shadow(ic, 128, 212, 96, 12)
    # an older album underneath
    with ic.g(transform="rotate(5 128 140)"):
        ic.rect(46, 60, 168, 146, rx=6, fill="#7A3A2E")
        ic.rect(46, 196, 168, 10, rx=4, fill="#E6DDC9")
        ic.rect(46, 60, 168, 146, rx=6, fill="none", stroke="#000", stroke_opacity=0.25)
    with ic.g(transform="rotate(-3 128 130)"):
        # the page block, then the cover over it
        ic.rect(48, 48, 166, 156, rx=4, fill="#000", opacity=0.3, transform="translate(4 5)")
        ic.rect(52, 52, 162, 152, rx=3, fill=paper(ic, "cream"))
        for k in range(5):
            ic.line(212.5 - k * 1.6, 56, 212.5 - k * 1.6, 200, stroke="#B9AE96", stroke_opacity=0.5)
        cloth = ic.define('<pattern id="{id}" width="3" height="3" patternUnits="userSpaceOnUse">'
                          '<rect width="3" height="1" fill="#fff" opacity=".06"/>'
                          '<rect width="1" height="3" fill="#000" opacity=".1"/></pattern>', "p")
        ic.rect(42, 44, 166, 156, rx=6, fill=ic.lin([(0, "#3DA6F5"), (0.5, "#1D86D8"), (1, "#0F5A9E")], 0, 0, 1, 1))
        ic.rect(42, 44, 166, 156, rx=6, fill=f"url(#{cloth})")
        # the spine
        ic.rect(42, 44, 22, 156, rx=6, fill=ic.lin([(0, "#0D4C86"), (0.6, "#1A6EB8"), (1, "#0B4478")], 0, 0, 1, 0))
        ic.line(64, 45, 64, 199, stroke="#082E52", stroke_width=1.6)
        ic.line(65.5, 45, 65.5, 199, stroke="#7CC4FF", stroke_opacity=0.35)
        for y in (60, 70, 174, 184):
            ic.rect(44, y, 18, 3, rx=1, fill="#E9C46A", opacity=0.8)
        ic.line(48, 45, 204, 45, stroke="#B9E0FF", stroke_opacity=0.6, stroke_width=1.5)
        # the print in its corners
        ic.rect(82, 62, 108, 82, fill="#000", opacity=0.3, transform="translate(2 3)")
        ic.rect(82, 62, 108, 82, fill=paper(ic, "white"))
        _land(ic, 88, 68, 96, 70, sky=("#2C5FA0", "#F4B66A"), far="#6A5E86", near="#3F6A3E",
              water=("#C27B4A", "#3A3E6A"), sun="#FFE0A0")
        for (x, y, r) in ((82, 62, 0), (190, 62, 90), (190, 144, 180), (82, 144, 270)):
            ic.path("M-2 -2 H14 L-2 14z", fill="#1E2024", transform=f"translate({x} {y}) rotate({r})")
            ic.path("M-2 -2 H14", stroke="#fff", stroke_opacity=0.25, transform=f"translate({x} {y}) rotate({r})")
        # gold foil on the cloth
        ic.text("PHOTOGRAPHS", 136, 167, 10, font="sans-semibold", anchor="middle", spacing=2.2, fill="#F2D488")
        ic.line(104, 175, 168, 175, stroke="#F2D488", stroke_opacity=0.7)
        ic.text("2026", 136, 187, 8, font="mono-semibold", anchor="middle", spacing=1.5, fill="#F2D488", opacity=0.85)


@small("gwenview")
def gwenview16(ic):
    tile(ic, "#5E6E80", "#25303C")
    ic.rect(3, 2.5, 11, 11.5, rx=0.6, fill="#F2EBDC")
    ic.rect(2, 2, 11, 11.5, rx=0.8, fill="#1D86D8")
    ic.rect(2, 2, 2, 11.5, rx=0.6, fill="#0D4C86")
    ic.rect(5.5, 4, 6, 5, fill="#FFFFFF")
    ic.rect(6, 4.5, 5, 4, fill="#F4B66A")
    ic.path("M6 8.5 L8 6.5 L9.4 7.6 L11 6.6 V8.5z", fill="#3F6A3E")
    ic.rect(6, 10.5, 5, 0.8, fill="#F2D488")


# --- Shotwell: a shoebox of prints, years on the dividers -------------------

@icon("shotwell", kind="app", names=["multimedia-photo-manager", "org.gnome.Shotwell", "org.kde.pix", "pix",
                                     "shotwell"], title="Shotwell")
def shotwell(ic):
    tile(ic, "#3F7D70", "#173A33")
    shadow(ic, 128, 214, 102, 12)
    # the lid, leaning at the back
    ic.path("M44 112 L54 48 a6 6 0 0 1 6-5 H196 a6 6 0 0 1 6 5 L212 112z",
            fill=ic.lin([(0, "#F6A54A"), (1, "#C4661C")]))
    ic.line(58, 45, 198, 45, stroke="#FFD9A0", stroke_width=1.5)
    ic.text("SHOTWELL", 128, 70, 12, font="sans-bold", anchor="middle", spacing=3, fill="#7A3408", opacity=0.75)
    # the opening, dark inside
    ic.path("M40 110 H216 L226 132 H30z", fill="#4A2A12")
    ic.path("M40 110 H216 L218 116 H38z", fill="#000", opacity=0.3)
    # prints standing in the box, back to front
    prints = [
        (60, 66, -6, ("#5C9BE0", "#E2EEF4"), "#4E9A4A", None),
        (112, 60, 3, ("#F28A3E", "#FFE0A0"), "#6A4A7A", ("#E0904E", "#5A3E5E")),
        (150, 72, 8, ("#9CC8E8", "#F2F4EE"), "#3D7A4C", None),
    ]
    for (x, y, r, sky, near, water) in prints:
        with ic.g(transform=f"rotate({r} {x + 30} 130)"):
            ic.rect(x, y, 62, 74, rx=1.5, fill="#000", opacity=0.25, transform="translate(2 2)")
            ic.rect(x, y, 62, 74, rx=1.5, fill=paper(ic, "white"))
            _land(ic, x + 4, y + 4, 54, 40, sky=sky, near=near, water=water, far="#7A8AA0")
    # a divider card with its tab
    with ic.g(transform="rotate(-2 100 120)"):
        ic.path("M38 96 H84 a4 4 0 0 1 4 4 V106 H190 V140 H38z", fill=paper(ic, "kraft"))
        ic.text("2025", 63, 104, 12, font="hand", anchor="middle", fill="#5A3A10")
    # the front, the side
    ic.path("M30 132 H226 L222 204 a6 6 0 0 1-6 5 H40 a6 6 0 0 1-6-5z",
            fill=ic.lin([(0, "#F4A048"), (0.5, "#E5862E"), (1, "#B95E18")]))
    ic.line(31, 133, 225, 133, stroke="#FFD9A0", stroke_width=2)
    ic.path("M30 132 L34 204", stroke="#fff", stroke_opacity=0.25, stroke_width=2)
    ic.line(36, 200, 220, 200, stroke="#7A3408", stroke_opacity=0.3, stroke_width=2)
    # the label holder, brass, a card in it
    ic.rect(92, 150, 72, 36, rx=3, fill=brass(ic))
    ic.rect(96, 154, 64, 28, rx=1.5, fill=paper(ic, "cream"))
    ic.path("M92 153 a3 3 0 0 1 3-3 h66 a3 3 0 0 1 3 3 v4 h-72z", fill=brass(ic, 0, 1, 1, 0))
    ic.text("Summer", 128, 175, 15, font="hand", anchor="middle", fill="#2C4660")
    for x in (98, 158):
        ic.circle(x, 182, 1.6, fill="#5A3E12")
    ic.text("PRINTS · 4×6", 128, 197, 6.5, font="mono-semibold", anchor="middle", spacing=1, fill="#7A3408",
            opacity=0.7)


@small("shotwell")
def shotwell16(ic):
    tile(ic, "#3F7D70", "#173A33")
    ic.rect(3, 3, 5, 6, fill="#FFFFFF", transform="rotate(-6 5 6)")
    ic.rect(3.6, 3.6, 3.8, 3, fill="#5C9BE0", transform="rotate(-6 5 6)")
    ic.rect(8, 2.5, 5, 6, fill="#FFFFFF", transform="rotate(6 10 6)")
    ic.rect(8.6, 3.1, 3.8, 3, fill="#F28A3E", transform="rotate(6 10 6)")
    ic.path("M1.5 8 H14.5 L14 13.6 a.6 .6 0 0 1-.6.5 H2.6 a.6 .6 0 0 1-.6-.5z", fill="#E5862E")
    ic.rect(6, 10, 4, 2.2, rx=0.3, fill="#F6EFD9")


# --- digiKam: a compact digital camera from the back, its blue mark --------

def _digikam_mark(ic, x, y, r):
    """digiKam's mark, redrawn: a blue lens, a lighter iris set off-centre."""
    ic.circle(x, y, r, fill=ic.rad([(0, "#7AC6FF"), (0.6, "#1F7BD8"), (1, "#0B3E86")], cx=0.38, cy=0.35, r=0.75))
    ic.circle(x + r * 0.12, y + r * 0.1, r * 0.55, fill="none", stroke="#E6F4FF", stroke_width=r * 0.18)
    ic.circle(x + r * 0.12, y + r * 0.1, r * 0.22, fill="#0B2E66")
    ic.circle(x - r * 0.35, y - r * 0.4, r * 0.16, fill="#fff", opacity=0.8)


@icon("digikam", kind="app", names=["digikam", "org.kde.digikam"], title="digiKam")
def digikam(ic):
    tile(ic, "#2B4C78", "#101F38")
    shadow(ic, 128, 208, 104, 12)
    # on top: shutter release, mode dial
    ic.rect(144, 56, 26, 12, rx=5, fill=steel(ic))
    ic.ellipse(157, 56, 13, 3.5, fill="#D9DDE1")
    ic.rect(178, 50, 36, 18, rx=3, fill=graphite(ic))
    for x in range(180, 213, 3):
        ic.line(x, 52, x, 66, stroke="#fff", stroke_opacity=0.18)
    ic.rect(180, 50.6, 32, 1.2, fill="#fff", opacity=0.4)
    # the body
    ic.rect(24, 64, 208, 136, rx=18, fill="#000", opacity=0.4, transform="translate(2 4)")
    ic.rect(24, 64, 208, 136, rx=18, fill=ic.lin([(0, "#4C525B"), (0.12, "#33373D"), (1, "#16181B")]))
    ic.rect(24.75, 64.75, 206.5, 134.5, rx=17.25, fill="none", stroke="#fff", stroke_opacity=0.16,
            stroke_width=1.5)
    grip = ic.define('<pattern id="{id}" width="4" height="4" patternUnits="userSpaceOnUse">'
                     '<circle cx="2" cy="2" r=".9" fill="#000" opacity=".35"/></pattern>', "p")
    ic.rect(168, 150, 56, 42, rx=8, fill=f"url(#{grip})")
    ic.text("digiKam", 36, 80, 9, font="sans-semibold", fill="#C9CED4", opacity=0.85)
    # the screen, a photo on it with the camera's readings
    ic.rect(34, 86, 128, 102, rx=6, fill="#0A0B0D")
    ic.rect(40, 92, 116, 86, rx=2, fill="#000")
    _land(ic, 40, 92, 116, 86, sky=("#3E86D6", "#D6E8F2"), far="#7889A8", near="#3D7A4C",
          water=("#4A7EA6", "#1E3E5A"))
    ic.rect(40, 92, 116, 12, fill="#000", opacity=0.35)
    ic.text("1/250  f4.0  ISO 200", 44, 101, 6.5, font="mono-semibold", fill="#F2F4F6")
    ic.text("P", 150, 101, 7, font="mono-semibold", anchor="end", fill="#F2C45C")
    ic.path("M84 122 h-6 v6 M112 122 h6 v6 M84 150 h-6 v-6 M112 150 h6 v-6", fill="none", stroke="#7CF7A6",
            stroke_width=1.6)
    ic.rect(140, 168, 12, 6, rx=1, fill="none", stroke="#F2F4F6", stroke_width=1)
    ic.rect(141.5, 169.5, 7, 3, fill="#7CF7A6")
    ic.path("M40 94a2 2 0 0 1 2-2h50L60 178H42a2 2 0 0 1-2-2z", fill=glare(ic, 0.8))
    # the controls
    _digikam_mark(ic, 196, 90, 12)
    for (x, y, s) in ((176, 118, "MENU"), (214, 118, "DISP")):
        ic.circle(x, y, 6, fill=graphite(ic))
        ic.circle(x, y, 6, fill="none", stroke="#fff", stroke_opacity=0.15)
        ic.text(s, x, y + 13, 5, font="mono-semibold", anchor="middle", fill="#9AA1A9")
    ic.circle(195, 158, 22, fill=ic.lin([(0, "#5A606A"), (1, "#1A1C20")], 0, 0, 1, 1))
    ic.circle(195, 158, 21.3, fill="none", stroke="#fff", stroke_opacity=0.18)
    for deg in (0, 90, 180, 270):
        x, y = polar(195, 158, 16, deg)
        ic.path("M0 -2.4 L2.4 1.6 H-2.4z", fill="#C9CED4", transform=f"translate({x:.1f} {y:.1f}) rotate({deg})")
    ic.circle(195, 158, 9, fill=steel(ic, horizontal=False))
    ic.text("OK", 195, 161, 6.5, font="sans-semibold", anchor="middle", fill="#2A2C30")


@small("digikam")
def digikam16(ic):
    tile(ic, "#2B4C78", "#101F38")
    ic.rect(1.5, 3.5, 13, 9.5, rx=1.6, fill="#2E3238")
    ic.rect(2.6, 4.8, 7.4, 7, rx=0.4, fill="#6FA6E0")
    ic.path("M2.6 10 L5 7.6 L6.8 9 L10 7 V11.8 H2.6z", fill="#3D7A4C")
    ic.circle(12.3, 6.2, 1.5, fill="#2F8BE6")
    ic.circle(12.3, 10, 1.4, fill="#8A9099")


# --- RawTherapee: a negative strip on a light box, a petal sticker ---------

@icon("rawtherapee", kind="app", names=["com.rawtherapee.RawTherapee", "rawtherapee"], title="RawTherapee")
def rawtherapee(ic):
    tile(ic, "#4A3A34", "#1A1210")
    shadow(ic, 128, 214, 104, 12)
    # the light box
    ic.rect(22, 62, 212, 144, rx=12, fill="#000", opacity=0.4, transform="translate(2 4)")
    ic.rect(22, 62, 212, 144, rx=12, fill=ic.lin([(0, "#DADDE1"), (0.5, "#9AA1A9"), (1, "#5D636B")], 0, 0, 1, 1))
    ic.rect(22.75, 62.75, 210.5, 142.5, rx=11.25, fill="none", stroke="#fff", stroke_opacity=0.5, stroke_width=1.5)
    ic.rect(32, 72, 192, 118, rx=4, fill=ic.rad([(0, "#FFFFFF"), (0.7, "#F2F6FA"), (1, "#C9D6E2")], cx=0.45,
                                                cy=0.4, r=0.7))
    ic.text("LIGHT · 5000K", 40, 200, 6.5, font="mono-semibold", spacing=1, fill="#2A2C30", opacity=0.6)
    # the strip
    with ic.g(transform="rotate(-10 128 128)"):
        ic.rect(6, 92, 244, 66, fill="#000", opacity=0.18, transform="translate(2 3)")
        ic.rect(6, 92, 244, 66, fill="#C8702E", opacity=0.92)
        ic.rect(6, 92, 244, 66, fill=ic.lin([(0, "#fff", 0.15), (1, "#fff", 0)]))
        for x in range(10, 248, 9):
            ic.rect(x, 95, 5, 6, rx=1, fill="#FFF4E6")
            ic.rect(x, 149, 5, 6, rx=1, fill="#FFF4E6")
        frames = (("#2E4E6E", "#C9B8A8", "#E6E0D8"), ("#33405A", "#B8A08E", "#F0EAE0"),
                  ("#3A3F5E", "#A89688", "#E8E2DA"))
        for k, (sky, far, near) in enumerate(frames):
            x = 14 + k * 80
            # a negative: the land's colours turned
            _land(ic, x, 104, 72, 42, sky=(sky, "#6A5A60"), far=far, near=near, sun="#20202E", snow=False)
            ic.rect(x, 104, 72, 42, fill="#D07A34", opacity=0.35)
        for k, n in enumerate(("12", "12A", "13", "13A", "14")):
            ic.text(n, 30 + k * 46, 104.2, 4.5, font="mono-semibold", fill="#FFE2B8", opacity=0.8)
        ic.text("RT 400", 160, 152.5, 4.5, font="mono-semibold", fill="#FFE2B8", opacity=0.8)
    # the sticker: RawTherapee's petals, redrawn
    sx, sy = 196, 172
    ic.circle(sx + 1, sy + 2, 20, fill="#000", opacity=0.3)
    ic.circle(sx, sy, 20, fill=paper(ic, "white"))
    for k, c in enumerate(("#E53A2F", "#F28C28", "#F6D33C", "#5CB848", "#2D8FD8", "#7A4FC4")):
        ic.path("M0 -2 C-6 -6 -6 -14 0 -16 C6 -14 6 -6 0 -2z", fill=c, transform=f"translate({sx} {sy}) rotate({k * 60 + 15})")
    ic.circle(sx, sy, 3, fill="#2A2C30")
    ic.circle(sx, sy, 20, fill="none", stroke="#000", stroke_opacity=0.12)


@small("rawtherapee")
def rawtherapee16(ic):
    tile(ic, "#4A3A34", "#1A1210")
    ic.rect(1.5, 3, 13, 10, rx=1, fill="#E8ECF0")
    ic.rect(0.5, 5.5, 15, 5, fill="#C8702E", transform="rotate(-10 8 8)")
    ic.rect(2.5, 6.6, 4.6, 2.8, fill="#3A3F5E", transform="rotate(-10 8 8)")
    ic.rect(8.6, 6.6, 4.6, 2.8, fill="#3A3F5E", transform="rotate(-10 8 8)")
    ic.circle(12.4, 11.4, 2.2, fill="#F6D33C")
    ic.circle(12.4, 11.4, 1, fill="#E53A2F")


# --- Hugin: a long panorama print, bowed to stand, its seams marked ---------

def _raven(ic, x, y, k, **kw):
    """Hugin's raven, a small silhouette, its beak to the left."""
    ic.path("M0 6 L6 3.6 L9 1 L13 0 L16 2 L22 3 L17 5 L16 8 L20 14 L13 11.6 L7 12.6 L4 10 L7 7.6z",
            transform=f"translate({x} {y}) scale({k})", **kw)


@icon("hugin", kind="app", names=["Panini", "hugin", "kipi-panorama", "net.sourceforge.Hugin", "panini",
                                  "ptbatcher"], title="Hugin")
def hugin(ic):
    tile(ic, "#C2843E", "#653A12")
    shadow(ic, 128, 200, 112, 13)
    top, bot = "M14 58 Q128 112 242 58", "L242 178 Q128 218 14 178z"
    shape = top + bot
    ic.path(shape, fill="#000", opacity=0.3, transform="translate(2 4)")
    ic.path(shape, fill=paper(ic, "white"))
    clip = ic.clip(f'<path d="M20 66 Q128 118 236 66 L236 162 Q128 200 20 162z"/>')
    with ic.g(clip_path=clip):
        ic.rect(0, 50, 256, 160, fill=ic.lin([(0, "#3D78C2"), (0.55, "#B9D6EC"), (0.8, "#F6DCB0")]))
        ic.circle(186, 104, 8, fill="#FFF0C4")
        ic.circle(186, 104, 14, fill="#FFF0C4", opacity=0.3)
        ic.path("M0 150 L22 128 L40 138 L64 108 L84 126 L104 112 L128 132 L148 106 L170 124 L192 116 L214 132"
                " L236 120 L256 132 L256 170 L0 170z", fill=ic.lin([(0, "#7C8AA6"), (1, "#3E4A63")]))
        ic.path("M56 116 L64 108 L72 116 L67 115 L64 119 L60 115z M142 112 L148 106 L156 113 L151 112 L148 116z",
                fill="#F4F7FA")
        ic.path("M0 156 Q60 140 128 154 T256 152 L256 220 L0 220z", fill=ic.lin([(0, "#4A8A4E"), (1, "#22472C")]))
        ic.path("M0 172 Q128 152 256 172 L256 220 L0 220z", fill="#5D88A6")
        ic.path("M0 176 Q128 158 256 176", fill="none", stroke="#fff", stroke_opacity=0.35, stroke_dasharray="10 7")
        # where the frames were stitched: seams and paired control points
        for x in (92, 164):
            ic.line(x, 50, x, 210, stroke="#fff", stroke_opacity=0.55, stroke_width=1, stroke_dasharray="3 3")
        for (x, y, c) in ((86, 124, "#F2C45C"), (98, 126, "#F2C45C"), (158, 116, "#E0483A"), (170, 118, "#E0483A"),
                          (84, 154, "#7CF7A6"), (96, 156, "#7CF7A6"), (160, 150, "#7CF7A6"), (171, 151, "#7CF7A6")):
            ic.rect(x - 3, y - 3, 6, 6, fill="none", stroke=c, stroke_width=1.4)
    # the white border along the foot, with its caption and the raven
    ic.path("M20 66 Q128 118 236 66", fill="none", stroke="#000", stroke_opacity=0.15)
    ic.path("M14 58 Q128 112 242 58", fill="none", stroke="#fff", stroke_width=2)
    ic.text("Hugin · 360°", 34, 176.5, 7, font="mono-semibold", fill="#6A665D", transform="rotate(6 34 176)")
    with ic.g(transform="rotate(-8 212 170)"):
        _raven(ic, 198, 160, 1.3, fill="#1E2024")
    # the bow: the near ends darker on their outside
    ic.path("M14 58 L20 66 L20 162 L14 178z", fill="#000", opacity=0.12)
    ic.path("M242 58 L236 66 L236 162 L242 178z", fill="#000", opacity=0.2)


@small("hugin")
def hugin16(ic):
    tile(ic, "#C2843E", "#653A12")
    ic.path("M1 4 Q8 7.4 15 4 V11.6 Q8 14.6 1 11.6z", fill="#FFFFFF")
    ic.path("M1.6 4.8 Q8 8 14.4 4.8 V10.8 Q8 13.6 1.6 10.8z", fill="#7DB0DE")
    ic.path("M1.6 9.6 L4 8 L6 9 L8.4 7.4 L10.6 9 L12.6 8 L14.4 9.2 V10.8 Q8 13.6 1.6 10.8z", fill="#3E4A63")


# --- Flameshot: an iris diaphragm, its blades flame red ---------------------

@icon("flameshot", kind="app", names=["flameshot", "org.flameshot.Flameshot"], title="Flameshot")
def flameshot(ic):
    tile(ic, "#4A2A24", "#1A0C0A")
    cx, cy = 128, 120
    shadow(ic, 128, 214, 86, 11)
    # the mount: a knurled steel ring
    ic.circle(cx + 2, cy + 5, 96, fill="#000", opacity=0.35)
    ic.circle(cx, cy, 96, fill=ic.lin([(0, "#F2F4F6"), (0.45, "#A3AAB2"), (1, "#3E444B")], 0, 0, 1, 1))
    ic.circle(cx, cy, 93, fill="none", stroke="#1E2024", stroke_width=5, stroke_dasharray="1.4 2", opacity=0.5)
    ic.circle(cx, cy, 86, fill=ic.lin([(0, "#3A3D42"), (1, "#101113")], 0, 0, 1, 1))
    for n, deg in (("FLAMESHOT", -38), ("2.8", 50), ("4", 66), ("5.6", 82), ("8", 98), ("11", 114)):
        _arc_text(ic, n, cx, cy, 77, deg, 7.5 if len(n) > 4 else 6.5, font="mono-semibold",
                  spacing=1.4 if len(n) > 4 else 0, fill="#F1F1EF")
    ic.path(f"M{cx} {cy - 86}l-3 5h6z", fill="#FF6A3D")
    ic.circle(cx, cy, 70, fill="#070708")
    # the blades: each between two edges of the opening, carried out to the rim
    n, r0, R = 8, 24, 69
    pts = [polar(cx, cy, r0, 22.5 * 0 + k * 360 / n) for k in range(n)]

    def out(a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]
        t = 0
        while (b[0] + dx * t - cx) ** 2 + (b[1] + dy * t - cy) ** 2 < (R + 4) ** 2:
            t += 0.05
        return b[0] + dx * t, b[1] + dy * t
    blades = ic.clip(f'<circle cx="{cx}" cy="{cy}" r="{R}"/>')
    with ic.g(clip_path=blades):
        for k in range(n):
            a, b, c = pts[k], pts[(k + 1) % n], pts[(k + 2) % n]
            e1, e2 = out(a, b), out(b, c)
            d = (f"M{b[0]:.1f} {b[1]:.1f}L{e1[0]:.1f} {e1[1]:.1f}A{R + 4} {R + 4} 0 0 1 {e2[0]:.1f} {e2[1]:.1f}"
                 f"L{c[0]:.1f} {c[1]:.1f}z")
            g = ic.lin([(0, "#FFB060"), (0.4, "#F2552E"), (1, "#A81E10")], 0, 0, 1, 1)
            ic.path(d, fill=g)
            ic.path(d, fill="#000", opacity=0.05 + 0.04 * (k % 4))
            ic.line(b[0], b[1], e1[0], e1[1], stroke="#5A0E06", stroke_width=1.6)
            ic.line(b[0], b[1], (b[0] + e1[0]) / 2, (b[1] + e1[1]) / 2, stroke="#FFD2A0", stroke_opacity=0.5,
                    stroke_width=0.8, transform="translate(-0.8 0.8)")
    # the opening: glass beyond, a spark of light in it
    hole = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "z"
    ic.path(hole, fill=ic.rad([(0, "#3A2A50"), (0.6, "#14121E"), (1, "#050508")], cx=0.4, cy=0.4, r=0.7))
    ic.ellipse(cx - 7, cy - 8, 6, 3.5, fill="#fff", opacity=0.55, transform=f"rotate(-35 {cx - 7} {cy - 8})")
    ic.circle(cx, cy, 70, fill="none", stroke="#000", stroke_opacity=0.6, stroke_width=2)
    ic.circle(cx, cy, 70, fill=glare(ic, 0.9))
    ic.path(f"M{cx - 76} {cy - 30}a82 82 0 0 1 52 -50 90 90 0 0 0 -52 50z", fill="#fff", opacity=0.45)


@small("flameshot")
def flameshot16(ic):
    tile(ic, "#4A2A24", "#1A0C0A")
    ic.circle(8, 8, 6.6, fill="#B9BEC5")
    ic.circle(8, 8, 5.4, fill="#E8452A")
    for k in range(6):
        x, y = polar(8, 8, 5.4, k * 60 + 10)
        x2, y2 = polar(8, 8, 1.8, k * 60 + 70)
        ic.line(x2, y2, x, y, stroke="#7A1408", stroke_width=0.6)
    ic.circle(8, 8, 1.9, fill="#14121E")


# --- ksnip: scissors cutting a printed screenshot along its selection ------

def _blade(ic, rot, flip):
    s = -1 if flip else 1
    with ic.g(transform=f"rotate({rot})"):
        ic.path(f"M6 {-7 * s} L-92 {-0.5 * s} L-94 {0.8 * s} L6 {6 * s}z",
                fill=ic.lin([(0, "#F2F4F6"), (0.5, "#A9B0B8"), (1, "#5D636B")], 0, 0, 0, 1))
        ic.path(f"M6 {-7 * s} L-92 {-0.5 * s}", stroke="#fff", stroke_opacity=0.7, stroke_width=0.8)
        # the shank to the ring
        ic.path(f"M0 {5 * s} L30 {-12 * s} L32 {-24 * s} L0 {-4 * s}z", fill="#0F6FB0")
        ring = (f"M{44 - 17} {-20 * s} a17 15 0 1 0 34 0 a17 15 0 1 0 -34 0z"
                f"M{44 - 10} {-20 * s} a10 8 0 1 1 20 0 a10 8 0 1 1 -20 0z")
        ic.path(ring, fill="#000", opacity=0.3, fill_rule="evenodd", transform="translate(2 3)")
        ic.path(ring, fill=ic.lin([(0, "#6CC8FF"), (0.5, "#1C8AE0"), (1, "#0A4E92")], 0, 0, 1, 1),
                fill_rule="evenodd")


@icon("ksnip", kind="app", names=["appimagekit-ksnip", "ksnip", "org.ksnip.ksnip"], title="ksnip")
def ksnip(ic):
    tile(ic, "#4E5C70", "#1E2733")
    shadow(ic, 124, 212, 98, 12)
    with ic.g(transform="rotate(-4 120 130)"):
        ic.rect(26, 50, 186, 150, rx=3, fill="#000", opacity=0.3, transform="translate(3 4)")
        ic.rect(26, 50, 186, 150, rx=3, fill=paper(ic, "white"))
        # the screenshot printed on it: a window, its sidebar, its text, a picture
        ic.rect(36, 60, 166, 130, rx=4, fill="#E9EDF2", stroke="#AAB3BE")
        ic.rect(36, 60, 166, 14, rx=4, fill="#3A4452")
        for k, c in enumerate(("#E0483A", "#F2C45C", "#5CB848")):
            ic.circle(45 + k * 8, 67, 2.4, fill=c)
        ic.rect(36, 74, 40, 116, fill="#D3DAE3")
        for k in range(6):
            ic.rect(42, 82 + k * 12, 28 - (k % 3) * 5, 4, rx=2, fill="#9AA6B4")
        for k in range(4):
            ic.rect(84, 82 + k * 9, 108 - (k % 2) * 30, 4, rx=2, fill="#B7C1CD")
        _land(ic, 86, 124, 70, 50, sky=("#5C9BE0", "#E2EEF4"), near="#4E9A4A")
        for k in range(3):
            ic.rect(162, 126 + k * 9, 30, 4, rx=2, fill="#B7C1CD")
        # the selection, dashed, cut along its bottom so far
        ic.rect(80, 118, 82, 62, fill="none", stroke="#E0483A", stroke_width=1.6, stroke_dasharray="5 3")
        for (x, y) in ((80, 118), (162, 118), (80, 180), (162, 180)):
            ic.rect(x - 2.5, y - 2.5, 5, 5, fill="#fff", stroke="#E0483A", stroke_width=1.2)
        ic.path("M162 180 L130 180", stroke="#2A2C30", stroke_width=1.2)
        ic.path("M162 182 L131 181", stroke="#000", stroke_opacity=0.15, stroke_width=2)
    # the scissors at the cut, open
    with ic.g(transform="translate(146 174) rotate(-18) scale(1.15)"):
        with ic.g(transform="translate(1.5 4)", opacity=0.25):
            ic.path("M6 -5 L-92 0 L6 5z", fill="#000")
        _blade(ic, 16, True)
        _blade(ic, -16, False)
        ic.circle(0, 0, 5, fill=steel(ic, horizontal=False))
        ic.circle(0, 0, 2, fill="#3C4148")


@small("ksnip")
def ksnip16(ic):
    tile(ic, "#4E5C70", "#1E2733")
    ic.rect(1.5, 2, 11, 10, rx=0.4, fill="#FFFFFF")
    ic.rect(2.3, 2.8, 9.4, 1.6, fill="#3A4452")
    ic.rect(4.5, 6, 6, 4.4, fill="none", stroke="#E0483A", stroke_width=0.8, stroke_dasharray="1.4 0.8")
    ic.path("M10.6 11 L4.6 9.8 M10.6 11 L4.8 12.4", stroke="#C3C8CE", stroke_width=1)
    ic.circle(12.6, 10.8, 1.7, fill="none", stroke="#1C8AE0", stroke_width=1.1)
    ic.circle(12.2, 13.6, 1.6, fill="none", stroke="#1C8AE0", stroke_width=1.1)


# --- Kooha: a camcorder in profile, its big red record button --------------

@icon("kooha", kind="app", names=["io.github.seadve.Kooha", "kooha"], title="Kooha")
def kooha(ic):
    tile(ic, "#5E7A44", "#253516")
    shadow(ic, 128, 208, 102, 12)
    # the lens barrel, forward to the left, its glass turned to us
    ic.rect(24, 92, 56, 66, rx=6, fill=ic.lin([(0, "#4C525B"), (0.3, "#2A2D33"), (1, "#121316")]))
    for x in range(34, 72, 4):
        ic.line(x, 94, x, 156, stroke="#000", stroke_opacity=0.35, stroke_width=1.6)
    ic.ellipse(26, 125, 14, 34, fill="#1A1C20")
    ic.ellipse(26, 125, 11, 29, fill=ic.rad([(0, "#5A4A8A"), (0.5, "#1A2240"), (1, "#05070C")], cx=0.4, cy=0.35,
                                            r=0.7))
    ic.ellipse(23, 112, 3.5, 9, fill="#fff", opacity=0.5)
    ic.ellipse(26, 125, 11, 29, fill=glare(ic, 1.2))
    # the body: white enamel, a darker base
    body = "M74 74 a14 14 0 0 1 14-14 H200 a24 24 0 0 1 24 24 V176 a14 14 0 0 1-14 14 H88 a14 14 0 0 1-14-14z"
    ic.path(body, fill="#000", opacity=0.35, transform="translate(2 4)")
    ic.path(body, fill=ic.lin([(0, "#FFFFFF"), (0.6, "#E8E6E1"), (1, "#B9B5AD")], 0, 0, 0.4, 1))
    ic.path("M74 168 H224 V176 a14 14 0 0 1-14 14 H88 a14 14 0 0 1-14-14z", fill="#3A3D42")
    ic.line(88, 61, 200, 61, stroke="#fff", stroke_width=1.5)
    # the carry handle on top
    ic.path("M146 62 V50 a8 8 0 0 1 8-8 H204 a8 8 0 0 1 8 8 V62 H202 V54 a3 3 0 0 0-3-3 H159 a3 3 0 0 0-3 3 V62z",
            fill=ic.lin([(0, "#4A4F57"), (1, "#1A1C20")]))
    ic.line(156, 43, 204, 43, stroke="#fff", stroke_opacity=0.25, stroke_width=1.2)
    # the flip screen, open toward us: what it records, the desktop
    ic.rect(90, 82, 92, 70, rx=6, fill="#000", opacity=0.3, transform="translate(2 3)")
    ic.rect(90, 82, 92, 70, rx=6, fill=graphite(ic))
    ic.rect(96, 88, 80, 58, rx=2, fill=ic.lin([(0, "#3A6FB0"), (1, "#5B3E8A")], 0, 0, 1, 1))
    ic.rect(96, 88, 80, 6, fill="#141517", opacity=0.8)
    ic.rect(104, 100, 40, 30, rx=2, fill="#F2F4F6")
    ic.rect(104, 100, 40, 6, rx=2, fill="#C9CED4")
    for k in range(3):
        ic.rect(108, 110 + k * 6, 30 - k * 8, 2.4, rx=1.2, fill="#9AA6B4")
    ic.rect(150, 112, 20, 26, rx=2, fill="#F2F4F6", opacity=0.85)
    ic.circle(102, 91, 1.6, fill="#E0483A")
    ic.text("REC 00:42", 172, 92.6, 5, font="mono-semibold", anchor="end", fill="#F2F4F6")
    ic.path("M96 90a2 2 0 0 1 2-2h40L110 146H98a2 2 0 0 1-2-2z", fill=glare(ic, 0.8))
    ic.text("KOOHA", 212, 180.5, 8, font="mono-semibold", anchor="end", spacing=2, fill="#C9CED4", opacity=0.8)
    # the record button, big, on the back
    bx, by = 204, 124
    ic.circle(bx, by + 2, 15, fill="#000", opacity=0.3)
    ic.circle(bx, by, 15, fill=ic.lin([(0, "#E6E9EC"), (1, "#7C838B")], 0, 0, 1, 1))
    ic.circle(bx, by, 11, fill=ic.rad([(0, "#FF7A66"), (0.55, "#E0281A"), (1, "#8A1008")], cx=0.38, cy=0.32,
                                      r=0.75))
    ic.ellipse(bx - 4, by - 4, 4, 2.4, fill="#fff", opacity=0.6, transform=f"rotate(-35 {bx - 4} {by - 4})")
    # the tally light on top
    ic.rect(110, 54, 22, 8, rx=3, fill="#3A3D42")
    ic.rect(113, 55.5, 16, 5, rx=2, fill="#FF5A44")


@small("kooha")
def kooha16(ic):
    tile(ic, "#5E7A44", "#253516")
    ic.rect(1.2, 6, 4.4, 5, rx=0.6, fill="#2A2D33")
    ic.rect(4.6, 3.8, 10, 9.4, rx=1.6, fill="#F2F0EB")
    ic.rect(4.6, 11.4, 10, 1.8, rx=0.6, fill="#3A3D42")
    ic.rect(6, 5.2, 5, 4.6, rx=0.4, fill="#3A6FB0")
    ic.circle(12.8, 7.6, 1.5, fill="#E0281A")


# --- Upscayl: a magnifier over pixel art, smooth inside the glass ----------

def _pixels(u, v):
    """The colour at u, v (0..1) of the scene Upscayl's lens enlarges."""
    if (u - 0.74) ** 2 + ((v - 0.23) * 0.7) ** 2 < 0.008:
        return "#FFF3C8"
    ridge = 0.63 - 0.3 * max(0.0, 1 - abs(u - 0.42) / 0.26) - 0.18 * max(0.0, 1 - abs(u - 0.78) / 0.22)
    if v > 0.82:
        return "#2E5A36"
    if v > ridge + 0.12 or v > 0.7:
        return "#4E9A4A"
    if v > ridge:
        return "#F7FAFC" if v < ridge + 0.05 and ridge < 0.45 else "#6A7C96"
    return ("#5C8FD8", "#7FA8E2", "#A8C6EC", "#D2E2F2")[min(3, int(v * 6))]


@icon("upscayl", kind="app", names=["org.upscayl.Upscayl", "upscayl"], title="Upscayl")
def upscayl(ic):
    tile(ic, "#7A48C2", "#2E1458")
    shadow(ic, 124, 212, 100, 12)
    cols, rows, cell, x0, y0 = 16, 12, 10, 34, 64
    # a card of pixel art
    with ic.g(transform="rotate(-6 114 124)"):
        ic.rect(x0 - 8, y0 - 8, cols * cell + 16, rows * cell + 26, rx=4, fill="#000", opacity=0.3,
                transform="translate(3 4)")
        ic.rect(x0 - 8, y0 - 8, cols * cell + 16, rows * cell + 26, rx=4, fill=paper(ic, "white"))
        for j in range(rows):
            for i in range(cols):
                ic.rect(x0 + i * cell, y0 + j * cell, cell + 0.4, cell + 0.4, fill=_pixels((i + 0.5) / cols,
                                                                                          (j + 0.5) / rows))
        ic.text("32 × 24", x0, y0 + rows * cell + 13, 7, font="mono-semibold", fill="#6A665D")
    # the magnifier: violet enamel handle, steel rim, the scene smooth in its glass
    lx, ly, lr = 150, 112, 44
    with ic.g(transform=f"rotate(42 {lx} {ly})"):
        ic.rect(lx - 8, ly + lr + 4, 16, 64, rx=7, fill="#000", opacity=0.3, transform="translate(3 3)")
        ic.rect(lx - 5, ly + lr, 10, 14, fill=steel(ic))
        ic.rect(lx - 8, ly + lr + 12, 16, 60, rx=7, fill=ic.lin([(0, "#C9A2FF"), (0.4, "#8A4FE0"), (1, "#3E1A7A")],
                                                                  0, 0, 1, 0))
        ic.rect(lx - 5, ly + lr + 16, 3, 50, rx=1.5, fill="#fff", opacity=0.35)
        ic.text("4×", lx, ly + lr + 40, 9, font="sans-bold", anchor="middle", fill="#F2E8FF",
                transform=f"rotate(-90 {lx} {ly + lr + 37})")
    ic.circle(lx + 2, ly + 4, lr + 7, fill="#000", opacity=0.3)
    ic.circle(lx, ly, lr + 7, fill=ic.lin([(0, "#F2F4F6"), (0.5, "#A3AAB2"), (1, "#4D535A")], 0, 0, 1, 1))
    ic.circle(lx, ly, lr + 1.5, fill="#2A2C30")
    lens = ic.clip(f'<circle cx="{lx}" cy="{ly}" r="{lr}"/>')
    with ic.g(clip_path=lens):
        ic.rect(lx - lr, ly - lr, lr * 2, lr * 2, fill="#fff")
        # the same scene, enlarged and smooth
        sx = 12
        X, Y = lx - 0.55 * cols * cell * 1.6 + 12, ly - 0.42 * rows * cell * 1.6
        with ic.g(transform=f"rotate(-6 {lx} {ly})"):
            ic.rect(X, Y, cols * cell * 1.6, rows * cell * 1.6,
                    fill=ic.lin([(0, "#5C8FD8"), (0.6, "#D2E2F2")]))
            W, H = cols * cell * 1.6, rows * cell * 1.6
            pt = lambda u, v: f"{X + u * W:.1f} {Y + v * H:.1f}"
            ic.circle(X + 0.74 * W, Y + 0.23 * H, 0.05 * W, fill="#FFF3C8")
            ic.path(f"M{pt(0, 0.66)} Q{pt(0.3, 0.5)} {pt(0.42, 0.33)} Q{pt(0.55, 0.5)} {pt(0.62, 0.55)}"
                    f" Q{pt(0.72, 0.44)} {pt(0.78, 0.45)} Q{pt(0.9, 0.55)} {pt(1, 0.62)} L{pt(1, 0.9)} L{pt(0, 0.9)}z",
                    fill=ic.lin([(0, "#7A8CA6"), (1, "#45536A")], 0, 0, 1, 1))
            ic.path(f"M{pt(0.35, 0.42)} Q{pt(0.4, 0.35)} {pt(0.42, 0.33)} Q{pt(0.46, 0.38)} {pt(0.5, 0.43)}"
                    f" Q{pt(0.45, 0.41)} {pt(0.42, 0.45)} Q{pt(0.39, 0.41)} {pt(0.35, 0.42)}z", fill="#F7FAFC")
            ic.path(f"M{pt(0, 0.76)} Q{pt(0.5, 0.66)} {pt(1, 0.74)} L{pt(1, 1)} L{pt(0, 1)}z",
                    fill=ic.lin([(0, "#5DAA56"), (1, "#2E5A36")]))
        _ = sx
    ic.circle(lx, ly, lr, fill=ic.rad([(0, "#fff", 0), (0.85, "#fff", 0), (1, "#2E1458", 0.3)]))
    ic.circle(lx, ly, lr, fill=glare(ic, 1.3))
    ic.path(f"M{lx - 34} {ly - 8}a34 34 0 0 1 28 -26 40 40 0 0 0 -28 26z", fill="#fff", opacity=0.65)
    # Upscayl's mark, redrawn: an arrow rising out of a square, on the rim
    with ic.g(transform=f"translate({lx + 30} {ly - 42})"):
        ic.circle(0, 0, 11, fill=ic.lin([(0, "#B07CFF"), (1, "#5A22B0")], 0, 0, 1, 1))
        ic.circle(0, 0, 11, fill="none", stroke="#fff", stroke_opacity=0.5)
        ic.path("M0 -6 L5 0 H2 V5 H-2 V0 H-5z", fill="#fff")


@small("upscayl")
def upscayl16(ic):
    tile(ic, "#7A48C2", "#2E1458")
    for j, row in enumerate(("bbbbs", "bmbbb", "mmmgb", "ggggg")):
        for i, c in enumerate(row):
            ic.rect(1.5 + i * 2, 3 + j * 2, 2, 2, fill={"b": "#7FA8E2", "s": "#FFF3C8", "m": "#6A7C96",
                                                         "g": "#4E9A4A"}[c])
    ic.path("M12.4 12.4 L14.6 14.6", stroke="#B07CFF", stroke_width=2, stroke_linecap="round")
    ic.circle(9.6, 9.6, 3.6, fill="#D2E2F2")
    ic.path("M6.6 10.4 Q8.6 7 10 8.4 Q11.4 7.6 12.8 9.4 V12 H6.6z", fill="#45536A")
    ic.circle(9.6, 9.6, 3.6, fill="none", stroke="#C9CED4", stroke_width=1.1)
