"""Soft drawings of the pictures apps (drawings/apps_t2_pictures.py): the
same tin, loupe, frame, album, shoebox, camera, light box, panorama, iris,
scissors, camcorder and magnifier, about half the detail, no text."""

from lib import bar, polar, soft, soft_shadow, tile, two

STEEL = ("#AEB4BB", "#8D949C")
BRASS = ("#E2B45E", "#B88433")


def _land(ic, x, y, w, h, sky=("#6FA6D6", "#E6EEE6"), far="#7F95AC", near="#3D7A4C", sun="#FFF3C8",
          water=None, snow=True):
    """A soft landscape photograph filling x, y, w, h: sky, sun, a range,
    a green hill or a lake. Drawn on a 100 x 70 grid, stretched."""
    clip = ic.clip(f'<rect x="{x}" y="{y}" width="{w}" height="{h}"/>')
    with ic.g(clip_path=clip):
        with ic.g(transform=f"translate({x} {y}) scale({w / 100:.4f} {h / 70:.4f})"):
            ic.rect(0, 0, 100, 70, fill=two(ic, *sky))
            if sun:
                ic.circle(74, 17, 8, fill=sun)
            ic.path("M0 46 L22 28 L42 16 L62 30 L80 22 L100 34 V56 H0z", fill=far)
            if snow:
                ic.path("M34 22 L42 16 L50 22 L46 24 L42 21 L38 24z", fill="#F7FAFC")
            if water:
                ic.path("M0 46 Q30 40 60 46 T100 44 V56 H0z", fill=near)
                ic.rect(0, 52, 100, 18, fill=water)
            else:
                ic.path("M0 52 Q30 40 60 48 T100 46 V70 H0z", fill=near)


# --- Pinta: an open tin of paint, a brush resting in it ----------------------

@soft("pinta")
def pinta(ic):
    tile(ic, "#3F6394", "#182C4B")
    soft_shadow(ic, 120, 212, 90, 12)
    cx, top, bot, rx, ry = 116, 104, 196, 64, 18
    ic.path(f"M{cx - rx + 4} 118 Q{cx} 34 {cx + rx - 4} 118", fill="none", stroke="#C3C8CE", stroke_width=5,
            stroke_linecap="round")
    ic.path(f"M{cx - rx} {top} V{bot} A{rx} {ry} 0 0 0 {cx + rx} {bot} V{top}z", fill=two(ic, *STEEL))
    ic.path(f"M{cx - rx} 128 A{rx} {ry} 0 0 0 {cx + rx} 128 V178 A{rx} {ry} 0 0 1 {cx - rx} 178z", fill="#2F5C9E")
    ic.path(f"M{cx - rx} 136 A{rx} {ry} 0 0 0 {cx + rx} 136 V170 A{rx} {ry} 0 0 1 {cx - rx} 170z",
            fill=two(ic, "#FFF8EA", "#EDE3CE"))
    # the swatch fan
    with ic.g(transform="translate(84 186)"):
        for k, c in enumerate(("#E8432C", "#F29A2E", "#F4D03F", "#3D8FD9")):
            ic.path("M0 0 L-6 -34 a7 7 0 0 1 12 0z", fill=c, transform=f"rotate({-36 + k * 24})")
        ic.circle(0, 0, 4, fill="#2A2E35")
    bar(ic, 112, 160, 50, 8, fill="#1E3B66")
    # the rim and the paint
    ic.ellipse(cx, top, rx, ry, fill=two(ic, "#E6E9EC", "#9AA1A9"))
    ic.ellipse(cx, top + 2, rx - 7, ry - 5, fill="#E8432C")
    ic.path(f"M{cx + 40} {top + 11} q6 1 12 -1 v26 a6 6 0 0 1 -12 0z", fill="#E8432C")
    # the brush
    with ic.g(transform=f"translate({cx + 14} {top + 2}) rotate(38)"):
        ic.path("M-14 0 Q-15 -14 -12 -26 H12 Q15 -14 14 0 Q0 5 -14 0z", fill="#E8432C")
        ic.rect(-13, -48, 26, 24, rx=4, fill=two(ic, *STEEL))
        ic.path("M-9 -48 L-7 -124 a7 7 0 0 1 14 0 L9 -48z", fill=two(ic, "#E09A5C", "#A8642E"))


# --- Image Viewer (Loupe): a stand loupe on a print ---------------------------

@soft("loupe")
def loupe(ic):
    tile(ic, "#4B86C8", "#1D4170")
    soft_shadow(ic, 124, 212, 98, 12)
    land = dict(sky=("#5C9BE0", "#DCEBF5"), far="#8399B5", near="#4E9A4A", sun="#FFE58A")
    with ic.g(transform="rotate(-7 118 140)"):
        ic.rect(30, 68, 170, 132, rx=6, fill=two(ic, "#FFFFFF", "#ECE8DF"))
        _land(ic, 40, 78, 150, 106, **land)
    cx, ty, by = 140, 84, 170
    # the clear skirt, then the barrel, the ring and the glass
    skirt = f"M{cx - 44} 118 L{cx - 50} {by} A50 20 0 0 0 {cx + 50} {by} L{cx + 44} 118z"
    ic.path(skirt, fill="#E8F2FA", opacity=0.35)
    ic.ellipse(cx, by, 50, 20, fill="none", stroke="#1E2228", stroke_width=4)
    ic.path(f"M{cx - 44} {ty} V118 A44 18 0 0 0 {cx + 44} 118 V{ty}z", fill=two(ic, "#3A3E44", "#1E2024"))
    ic.ellipse(cx, ty, 44, 18, fill=two(ic, "#E6E9EC", "#8D949C"))
    lens = ic.clip(f'<ellipse cx="{cx}" cy="{ty}" rx="36" ry="13"/>')
    with ic.g(clip_path=lens):
        _land(ic, cx - 44, ty - 16, 88, 36, **land)


# --- Eye of GNOME: an eye-shaped frame, a round photo for its iris ---------

@soft("eog")
def eog(ic):
    tile(ic, "#4C6B78", "#1E323B")
    soft_shadow(ic, 128, 210, 90, 11)
    cx, cy = 128, 118
    ic.path(f"M16 {cy} Q{cx} 2 240 {cy} Q{cx} 234 16 {cy}z", fill=two(ic, "#9A6A42", "#5A321A"))
    ic.path(f"M30 {cy} Q{cx} 18 226 {cy} Q{cx} 218 30 {cy}z", fill=two(ic, *BRASS))
    ic.path(f"M38 {cy} Q{cx} 32 218 {cy} Q{cx} 204 38 {cy}z", fill=two(ic, "#FFFDF7", "#EDE5D4"))
    ic.circle(cx, cy, 48, fill=two(ic, "#5AA2E6", "#1E5AA8"))
    photo = ic.clip(f'<circle cx="{cx}" cy="{cy}" r="34"/>')
    with ic.g(clip_path=photo):
        _land(ic, cx - 48, cy - 34, 96, 68, sky=("#3F6E9E", "#F2D6A8"), far="#5E6E8A", near="#3D6A4C",
              water="#3E6A88", sun="#FFE2A0")


# --- Gwenview: a cloth-bound photo album, a print in corners on its cover ---

@soft("gwenview")
def gwenview(ic):
    tile(ic, "#5E6E80", "#25303C")
    soft_shadow(ic, 128, 214, 96, 12)
    with ic.g(transform="rotate(5 128 140)"):
        ic.rect(46, 60, 168, 146, rx=10, fill="#7A3A2E")
    with ic.g(transform="rotate(-3 128 130)"):
        ic.rect(52, 52, 162, 152, rx=8, fill=two(ic, "#FBF5E8", "#E6DCC6"))
        ic.rect(42, 44, 166, 156, rx=10, fill=two(ic, "#2E9AEA", "#1468B4"))
        ic.rect(42, 44, 24, 156, rx=10, fill="#0D4C86")
        ic.rect(56, 44, 10, 156, fill="#0D4C86")
        ic.rect(82, 62, 108, 82, rx=3, fill="#FFFFFF")
        _land(ic, 89, 69, 94, 68, sky=("#2C5FA0", "#F4B66A"), far="#6A5E86", near="#3F6A3E",
              water="#7A5A6A", sun="#FFE0A0")
        for (x, y, r) in ((82, 62, 0), (190, 62, 90), (190, 144, 180), (82, 144, 270)):
            ic.path("M-3 -3 H16 L-3 16z", fill="#1E2024", transform=f"translate({x} {y}) rotate({r})")
        bar(ic, 96, 162, 80, 8, fill="#F2D488")
        bar(ic, 116, 178, 40, 6, fill="#F2D488", opacity=0.7)


# --- Shotwell: a shoebox of prints ------------------------------------------

@soft("shotwell")
def shotwell(ic):
    tile(ic, "#3F7D70", "#173A33")
    soft_shadow(ic, 128, 216, 102, 12)
    ic.path("M44 112 L54 50 a8 8 0 0 1 8-7 H194 a8 8 0 0 1 8 7 L212 112z", fill=two(ic, "#F6A54A", "#D07020"))
    ic.path("M40 110 H216 L226 132 H30z", fill="#4A2A12")
    prints = [
        (60, 66, -6, ("#5C9BE0", "#E2EEF4"), "#4E9A4A", None),
        (112, 60, 3, ("#F28A3E", "#FFE0A0"), "#6A4A7A", "#5A3E5E"),
        (150, 72, 8, ("#9CC8E8", "#F2F4EE"), "#3D7A4C", None),
    ]
    for (x, y, r, sky, near, water) in prints:
        with ic.g(transform=f"rotate({r} {x + 30} 130)"):
            ic.rect(x, y, 62, 74, rx=4, fill="#FFFFFF")
            _land(ic, x + 5, y + 5, 52, 40, sky=sky, near=near, water=water, far="#7A8AA0", snow=False)
    with ic.g(transform="rotate(-2 100 120)"):
        ic.path("M38 96 H82 a6 6 0 0 1 6 6 V106 H190 V140 H38z", fill="#C9A06A")
    ic.path("M30 132 H226 L222 202 a8 8 0 0 1-8 7 H42 a8 8 0 0 1-8-7z", fill=two(ic, "#F4A048", "#C86A1E"))
    ic.rect(90, 150, 76, 38, rx=6, fill=two(ic, *BRASS))
    ic.rect(96, 156, 64, 26, rx=4, fill="#FBF5E8")
    bar(ic, 106, 166, 44, 7, fill="#2C4660")


# --- digiKam: a compact digital camera from the back -------------------------

@soft("digikam")
def digikam(ic):
    tile(ic, "#2B4C78", "#101F38")
    soft_shadow(ic, 128, 210, 104, 12)
    ic.rect(144, 52, 28, 18, rx=6, fill=two(ic, *STEEL))
    ic.rect(178, 48, 38, 22, rx=6, fill="#2A2C30")
    ic.rect(24, 64, 208, 136, rx=22, fill=two(ic, "#454B53", "#1E2125"))
    # the screen with its photo
    ic.rect(34, 84, 130, 106, rx=10, fill="#0A0B0D")
    with ic.g(clip_path=ic.clip('<rect x="42" y="92" width="114" height="90" rx="4"/>')):
        _land(ic, 42, 92, 114, 90, sky=("#3E86D6", "#D6E8F2"), far="#7889A8", near="#3D7A4C", water="#3E6E96")
    ic.path("M84 122 h-8 v8 M114 122 h8 v8 M84 152 h-8 v-8 M114 152 h8 v-8", fill="none", stroke="#7CF7A6",
            stroke_width=3, stroke_linecap="round", stroke_linejoin="round")
    # the controls: the mark, two buttons, the dial
    ic.circle(196, 92, 13, fill=two(ic, "#5AB0FF", "#1A62C0"))
    ic.circle(197, 93, 7, fill="none", stroke="#E6F4FF", stroke_width=2.6)
    for x in (178, 214):
        ic.circle(x, 122, 7, fill="#5A606A")
    ic.circle(196, 160, 24, fill=two(ic, "#5A606A", "#2A2D33"))
    ic.circle(196, 160, 11, fill=two(ic, *STEEL))


# --- RawTherapee: a negative strip on a light box, a petal sticker ---------

@soft("rawtherapee")
def rawtherapee(ic):
    tile(ic, "#4A3A34", "#1A1210")
    soft_shadow(ic, 128, 216, 104, 12)
    ic.rect(22, 62, 212, 144, rx=16, fill=two(ic, *STEEL))
    ic.rect(32, 72, 192, 120, rx=8, fill=two(ic, "#FFFFFF", "#DCE6EE"))
    with ic.g(transform="rotate(-10 128 128)"):
        ic.rect(6, 92, 244, 66, fill="#C8702E")
        for x in range(12, 248, 14):
            ic.rect(x, 96, 7, 7, rx=2, fill="#FFF4E6")
            ic.rect(x, 147, 7, 7, rx=2, fill="#FFF4E6")
        for k, sky in enumerate(("#2E4E6E", "#33405A", "#3A3F5E")):
            x = 14 + k * 80
            ic.rect(x, 107, 72, 36, rx=2, fill=sky)
            ic.path(f"M{x} 133 L{x + 24} 117 L{x + 40} 127 L{x + 56} 119 L{x + 72} 129 V143 H{x}z", fill="#C9B8A8")
    sx, sy = 196, 172
    ic.circle(sx, sy, 22, fill="#FFFFFF")
    for k, c in enumerate(("#E53A2F", "#F28C28", "#F6D33C", "#5CB848", "#2D8FD8", "#7A4FC4")):
        ic.path("M0 -2 C-7 -6 -7 -15 0 -18 C7 -15 7 -6 0 -2z", fill=c,
                transform=f"translate({sx} {sy}) rotate({k * 60 + 15})")


# --- Hugin: a long panorama print, bowed to stand ---------------------------

@soft("hugin")
def hugin(ic):
    tile(ic, "#C2843E", "#653A12")
    soft_shadow(ic, 128, 202, 112, 13)
    ic.path("M14 58 Q128 112 242 58 L242 178 Q128 218 14 178z", fill="#FFFFFF")
    clip = ic.clip('<path d="M22 68 Q128 120 234 68 L234 162 Q128 200 22 162z"/>')
    with ic.g(clip_path=clip):
        ic.rect(0, 50, 256, 160, fill=two(ic, "#3D78C2", "#E6EEF2"))
        ic.circle(186, 104, 10, fill="#FFF0C4")
        ic.path("M0 150 L40 124 L64 108 L96 128 L148 104 L190 124 L256 118 V170 H0z", fill="#6A7A98")
        ic.path("M54 116 L64 108 L74 116 L64 120z M138 112 L148 104 L158 112 L148 116z", fill="#F4F7FA")
        ic.path("M0 156 Q60 140 128 154 T256 152 V220 H0z", fill="#3D7A44")
        ic.path("M0 172 Q128 152 256 172 V220 H0z", fill="#5D88A6")
        for x in (92, 164):
            ic.line(x, 50, x, 210, stroke="#fff", stroke_opacity=0.6, stroke_width=2.5, stroke_dasharray="6 5")
    ic.path("M14 58 L22 68 L22 162 L14 178z", fill="#000", opacity=0.12)
    ic.path("M242 58 L234 68 L234 162 L242 178z", fill="#000", opacity=0.2)


# --- Flameshot: an iris diaphragm, its blades flame red ---------------------

@soft("flameshot")
def flameshot(ic):
    tile(ic, "#4A2A24", "#1A0C0A")
    soft_shadow(ic, 128, 216, 86, 11)
    cx, cy = 128, 120
    ic.circle(cx, cy, 96, fill=two(ic, "#C9CED4", "#7A8189"))
    ic.circle(cx, cy, 84, fill="#1E2024")
    ic.path(f"M{cx} {cy - 84}l-6 9h12z", fill="#FF6A3D")
    n, r0, R = 6, 26, 72
    pts = [polar(cx, cy, r0, k * 360 / n) for k in range(n)]

    def out(a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]
        t = 0
        while (b[0] + dx * t - cx) ** 2 + (b[1] + dy * t - cy) ** 2 < (R + 4) ** 2:
            t += 0.05
        return b[0] + dx * t, b[1] + dy * t
    blades = ic.clip(f'<circle cx="{cx}" cy="{cy}" r="{R}"/>')
    shades = ("#F26A3A", "#E2502A", "#F6844A", "#D8462A", "#EE6034", "#F7905A")
    with ic.g(clip_path=blades):
        for k in range(n):
            a, b, c = pts[k], pts[(k + 1) % n], pts[(k + 2) % n]
            e1, e2 = out(a, b), out(b, c)
            ic.path(f"M{b[0]:.1f} {b[1]:.1f}L{e1[0]:.1f} {e1[1]:.1f}A{R + 4} {R + 4} 0 0 1 {e2[0]:.1f} "
                    f"{e2[1]:.1f}L{c[0]:.1f} {c[1]:.1f}z", fill=shades[k])
    ic.path("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "z", fill="#14121E")


# --- ksnip: scissors cutting a printed screenshot along its selection ------

def _blade(ic, rot, flip):
    s = -1 if flip else 1
    with ic.g(transform=f"rotate({rot})"):
        ic.path(f"M6 {-8 * s} L-92 {-1 * s} L-92 {1.5 * s} L6 {7 * s}z", fill=two(ic, "#E6E9EC", "#A3AAB2"))
        ic.path(f"M0 {5 * s} L30 {-12 * s} L32 {-24 * s} L0 {-4 * s}z", fill="#0F6FB0")
        ic.path(f"M27 {-20 * s} a17 15 0 1 0 34 0 a17 15 0 1 0 -34 0z M35 {-20 * s} a9 7 0 1 1 18 0 "
                f"a9 7 0 1 1 -18 0z", fill="#1C8AE0", fill_rule="evenodd")


@soft("ksnip")
def ksnip(ic):
    tile(ic, "#4E5C70", "#1E2733")
    soft_shadow(ic, 124, 214, 98, 12)
    with ic.g(transform="rotate(-4 120 130)"):
        ic.rect(26, 50, 186, 150, rx=6, fill="#FFFFFF")
        ic.rect(36, 60, 166, 130, rx=6, fill="#E9EDF2")
        ic.path("M36 66 a6 6 0 0 1 6 -6 H196 a6 6 0 0 1 6 6 V76 H36z", fill="#3A4452")
        ic.rect(36, 76, 40, 114, fill="#D3DAE3")
        for k in range(3):
            bar(ic, 84, 86 + k * 12, 100 - k * 24, fill="#B7C1CD")
        _land(ic, 86, 124, 70, 50, sky=("#5C9BE0", "#E2EEF4"), near="#4E9A4A", snow=False)
        ic.rect(80, 118, 82, 62, fill="none", stroke="#E0483A", stroke_width=3, stroke_dasharray="8 5")
    with ic.g(transform="translate(146 174) rotate(-18) scale(1.15)"):
        _blade(ic, 16, True)
        _blade(ic, -16, False)
        ic.circle(0, 0, 6, fill=two(ic, *STEEL))


# --- Kooha: a camcorder in profile, its big red record button --------------

@soft("kooha")
def kooha(ic):
    tile(ic, "#5E7A44", "#253516")
    soft_shadow(ic, 128, 210, 102, 12)
    ic.rect(24, 92, 60, 66, rx=10, fill=two(ic, "#3A3E44", "#1E2024"))
    ic.ellipse(28, 125, 15, 34, fill="#1A1C20")
    ic.ellipse(28, 125, 11, 28, fill=two(ic, "#4A4A80", "#141A30"))
    ic.path("M146 64 V50 a10 10 0 0 1 10-10 H202 a10 10 0 0 1 10 10 V64 H200 V54 a3 3 0 0 0-3-3 H161 a3 3 0 0 0-3 3 "
            "V64z", fill="#2A2D33")
    ic.rect(110, 52, 24, 12, rx=5, fill="#FF5A44")
    body = "M74 78 a18 18 0 0 1 18-18 H198 a26 26 0 0 1 26 26 V172 a18 18 0 0 1-18 18 H92 a18 18 0 0 1-18-18z"
    ic.path(body, fill=two(ic, "#FFFFFF", "#D8D5CE"))
    ic.path("M74 166 H224 V172 a18 18 0 0 1-18 18 H92 a18 18 0 0 1-18-18z", fill="#3A3D42")
    # the flip screen showing the desktop
    ic.rect(90, 82, 94, 72, rx=10, fill="#2A2D33")
    ic.rect(97, 89, 80, 58, rx=4, fill=two(ic, "#3A6FB0", "#5B3E8A"))
    ic.rect(106, 100, 42, 32, rx=4, fill="#F2F4F6")
    bar(ic, 112, 112, 28, 5, fill="#9AA6B4")
    bar(ic, 112, 121, 18, 5, fill="#9AA6B4")
    ic.rect(152, 110, 18, 26, rx=3, fill="#F2F4F6", opacity=0.85)
    ic.circle(204, 124, 17, fill=two(ic, *STEEL))
    ic.circle(204, 124, 12, fill=two(ic, "#F04A36", "#B81A10"))


# --- Upscayl: a magnifier over pixel art, smooth inside the glass ----------

def _pixels(u, v):
    if (u - 0.74) ** 2 + ((v - 0.25) * 0.7) ** 2 < 0.012:
        return "#FFF3C8"
    ridge = 0.63 - 0.3 * max(0.0, 1 - abs(u - 0.4) / 0.3) - 0.18 * max(0.0, 1 - abs(u - 0.8) / 0.25)
    if v > ridge + 0.14 or v > 0.72:
        return "#4E9A4A"
    if v > ridge:
        return "#6A7C96"
    return ("#5C8FD8", "#7FA8E2", "#A8C6EC")[min(2, int(v * 5))]


@soft("upscayl")
def upscayl(ic):
    tile(ic, "#7A48C2", "#2E1458")
    soft_shadow(ic, 124, 214, 100, 12)
    cols, rows, cell, x0, y0 = 8, 6, 20, 34, 64
    with ic.g(transform="rotate(-6 114 124)"):
        ic.rect(x0 - 10, y0 - 10, cols * cell + 20, rows * cell + 20, rx=8, fill="#FFFFFF")
        for j in range(rows):
            for i in range(cols):
                ic.rect(x0 + i * cell, y0 + j * cell, cell + 0.4, cell + 0.4,
                        fill=_pixels((i + 0.5) / cols, (j + 0.5) / rows))
    lx, ly, lr = 150, 112, 44
    with ic.g(transform=f"rotate(42 {lx} {ly})"):
        ic.rect(lx - 6, ly + lr, 12, 16, fill="#8D949C")
        ic.rect(lx - 10, ly + lr + 12, 20, 62, rx=10, fill=two(ic, "#A878F0", "#5A2AA8"))
    ic.circle(lx, ly, lr + 8, fill=two(ic, "#E6E9EC", "#8D949C"))
    lens = ic.clip(f'<circle cx="{lx}" cy="{ly}" r="{lr}"/>')
    with ic.g(clip_path=lens):
        with ic.g(transform=f"rotate(-6 {lx} {ly})"):
            X, Y, W, H = lx - 129, ly - 81, 256, 192
            pt = lambda u, v: f"{X + u * W:.1f} {Y + v * H:.1f}"  # noqa: E731
            ic.rect(X, Y, W, H, fill=two(ic, "#5C8FD8", "#D2E2F2"))
            ic.circle(X + 0.74 * W, Y + 0.23 * H, 0.05 * W, fill="#FFF3C8")
            ic.path(f"M{pt(0, 0.66)} Q{pt(0.3, 0.5)} {pt(0.42, 0.33)} Q{pt(0.55, 0.5)} {pt(0.62, 0.55)}"
                    f" Q{pt(0.72, 0.44)} {pt(0.78, 0.45)} Q{pt(0.9, 0.55)} {pt(1, 0.62)} L{pt(1, 0.9)} L{pt(0, 0.9)}z",
                    fill="#6A7C96")
            ic.path(f"M{pt(0, 0.76)} Q{pt(0.5, 0.66)} {pt(1, 0.74)} L{pt(1, 1)} L{pt(0, 1)}z", fill="#4E9A4A")
    with ic.g(transform=f"translate({lx + 32} {ly - 42})"):
        ic.circle(0, 0, 14, fill=two(ic, "#B07CFF", "#6A2AC8"))
        ic.path("M0 -8 L7 0 H3 V7 H-3 V0 H-7z", fill="#fff")
