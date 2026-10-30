"""Soft drawings of the remote desktop, VPN and secrets apps
(drawings/apps_t2_remote.py): the same tablet, remote, monitors, toolbox,
gamepad, plug, tunnel, vault door, key card, fob, crate and drive, about
half the detail, no text."""

from lib import bar, polar, soft, soft_shadow, tile, two

STEEL = ("#AEB4BB", "#8D949C")
BRASS = ("#E2B45E", "#B88433")


def _cursor(ic, x, y, k=1.0):
    """A pointer arrow, its tip at (x, y)."""
    d = (f"M{x} {y}l0 {17 * k}l{4.2 * k} {-4 * k}l{3 * k} {6.6 * k}l{2.8 * k} {-1.3 * k}"
         f"l{-3 * k} {-6.4 * k}l{6 * k} 0z")
    ic.path(d, fill="#fff", stroke="#1A1C20", stroke_width=1.6 * k, stroke_linejoin="round")


def _padlock(ic, cx, top, w, body_fill, shackle="#C3C8CE"):
    """A padlock, its shackle's top at top, w wide; returns the body's top, height."""
    h = w * 0.82
    by = top + w * 0.55
    ic.path(f"M{cx - w * 0.3} {by + 2}V{top + w * 0.3}a{w * 0.3} {w * 0.3} 0 0 1 {w * 0.6} 0V{by + 2}",
            fill="none", stroke=shackle, stroke_width=w * 0.18)
    ic.rect(cx - w / 2, by, w, h, rx=w * 0.18, fill=body_fill)
    return by, h


# --- Remmina: a tablet on its folio stand, a remote desktop on it ------------

@soft("remmina")
def remmina(ic):
    tile(ic, "#3E7AA8", "#173A5C")
    soft_shadow(ic, 128, 212, 104, 12)
    ic.path("M70 204 L96 150 H160 L186 204 Z", fill="#1E3A58")
    with ic.g(transform="rotate(-3 128 128)"):
        ic.rect(26, 48, 204, 150, rx=22, fill=two(ic, "#3A3F46", "#1A1D21"))
        sx, sy, sw, sh = 38, 62, 180, 124
        clip = ic.clip(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="8"/>')
        with ic.g(clip_path=clip):
            ic.rect(sx, sy, sw, sh, fill=two(ic, "#7FC2E8", "#2E6AA8"))
            ic.rect(sx, sy, sw, 16, fill="#16222F")
            ic.circle(sx + 10, sy + 8, 4, fill="#5BD06A")
            bar(ic, sx + 20, sy + 5, 70, 6, fill="#DCE7F2")
            ic.rect(sx + 118, sy + 54, 56, 60, rx=6, fill="#2A3340")
            for k in range(3):
                bar(ic, sx + 126, sy + 70 + k * 12, 34 - k * 8, 5, fill="#8FD7A0")
            ic.rect(sx + 20, sy + 28, 112, 78, rx=6, fill="#FBFAF7")
            ic.path(f"M{sx + 20} {sy + 34} a6 6 0 0 1 6 -6 H{sx + 126} a6 6 0 0 1 6 6 V{sy + 42} H{sx + 20}z",
                    fill="#E3E7EC")
            for r in range(3):
                for c in range(3):
                    ic.rect(sx + 28 + c * 33, sy + 50 + r * 16, 30, 12, rx=2, fill="#D4E6F6" if r == 0 else "#EEF1F4")
            ic.rect(sx + 94, sy + 66, 30, 12, rx=2, fill="none", stroke="#2F7FD0", stroke_width=2.5)
            ic.rect(sx, sy + sh - 12, sw, 12, fill="#0F1A26")
            _cursor(ic, sx + 88, sy + 76, 1.2)


# --- AnyDesk: a white remote control, its red diamond badge -----------------

def _diamond(cx, cy, r):
    return f"M{cx} {cy - r}L{cx + r} {cy}L{cx} {cy + r}L{cx - r} {cy}Z"


@soft("anydesk")
def anydesk(ic):
    tile(ic, "#C2453B", "#6A1A14")
    soft_shadow(ic, 128, 216, 70, 11)
    with ic.g(transform="rotate(-18 128 124)"):
        x, y, w, h = 88, 22, 80, 206
        ic.rect(x, y, w, h, rx=34, fill=two(ic, "#FFFFFF", "#D6D6D2"))
        ic.circle(x + 58, y + 26, 8, fill="#EF443B")
        cx, cy = x + 40, y + 68
        ic.circle(cx, cy, 27, fill=two(ic, "#4C4F55", "#24262A"))
        ic.circle(cx, cy, 12, fill=two(ic, "#F4F4F2", "#C7C7C3"))
        for r in range(3):
            for c in range(3):
                kx, ky = x + 18 + c * 22, y + 106 + r * 19
                ic.rect(kx - 8, ky - 6, 16, 12, rx=6, fill="#4A4D53")
        bx, by = x + 40, y + 176
        ic.circle(bx, by, 19, fill="#FFFFFF", stroke="#C9CDD2", stroke_width=3)
        ic.path(_diamond(bx, by, 12), fill="#EF443B", stroke="#EF443B", stroke_width=3, stroke_linejoin="round")
        ic.path(_diamond(bx, by, 7), fill="#FFFFFF")
        ic.path(_diamond(bx, by, 3.4), fill="#EF443B")


# --- TeamViewer: two monitors, the blue double-arrow badge between them ------

def _monitor(ic, x, y, w, h, light):
    ic.path(f"M{x + w / 2 - 10} {y + h - 2}h20l5 22h-30z", fill="#8D949C")
    ic.rect(x + w / 2 - 26, y + h + 16, 52, 10, rx=5, fill=two(ic, *STEEL))
    ic.rect(x, y, w, h, rx=12, fill=two(ic, "#3A3F46", "#1A1D21"))
    sx, sy, sw, sh = x + 7, y + 7, w - 14, h - 16
    ic.rect(sx, sy, sw, sh, rx=5, fill=two(ic, "#BFE0FA", "#5FA6E0") if light else two(ic, "#2E5A86", "#14304E"))
    ic.rect(sx + sw * 0.12, sy + sh * 0.18, sw * 0.56, sh * 0.5, rx=4, fill="#FFFFFF")
    bar(ic, sx + sw * 0.18, sy + sh * 0.38, sw * 0.36, 5, fill="#9AA6B2")


@soft("teamviewer")
def teamviewer(ic):
    tile(ic, "#2F6FB4", "#0E3466")
    soft_shadow(ic, 128, 214, 108, 12)
    _monitor(ic, 18, 48, 120, 90, False)
    _monitor(ic, 106, 70, 132, 100, True)
    cx, cy, r = 112, 150, 40
    ic.circle(cx, cy, r + 5, fill=two(ic, "#E6E9EC", "#9AA1A9"))
    ic.circle(cx, cy, r, fill=two(ic, "#3A9CFF", "#0A5CC0"))
    ic.circle(cx, cy, r - 5, fill="none", stroke="#fff", stroke_width=4)
    ic.path(f"M{cx - 26} {cy}l13 -12v7c6 -3.5 20 -3.5 26 0v-7l13 12l-13 12v-7c-6 3.5 -20 3.5 -26 0v7z", fill="#fff")


# --- RustDesk: a rust-orange toolbox, a screen set in its side --------------

@soft("rustdesk")
def rustdesk(ic):
    tile(ic, "#2D4C7C", "#11223F")
    soft_shadow(ic, 128, 214, 104, 12)
    orange = two(ic, "#F08A4B", "#C0521E")
    ic.path("M86 72 V52 a12 12 0 0 1 12 -12 h60 a12 12 0 0 1 12 12 V72", fill="none", stroke="#A3AAB2",
            stroke_width=10)
    ic.rect(102, 32, 52, 16, rx=8, fill="#2A2C30")
    ic.rect(28, 70, 200, 34, rx=10, fill=orange)
    ic.path("M34 104 H222 L216 204 a8 8 0 0 1 -8 8 H48 a8 8 0 0 1 -8 -8 Z", fill=orange)
    ic.rect(34, 102, 188, 5, fill="#8E3512", opacity=0.5)
    for x in (52, 186):
        ic.rect(x, 86, 18, 28, rx=5, fill=two(ic, *STEEL))
    ic.rect(70, 120, 116, 72, rx=12, fill="#14161A")
    sx, sy, sw, sh = 78, 128, 100, 56
    ic.rect(sx, sy, sw, sh, rx=5, fill=two(ic, "#2A6BE8", "#123A9A"))
    ic.rect(sx + 10, sy + 10, 60, 36, rx=4, fill="#F4F6FA")
    bar(ic, sx + 16, sy + 17, 40, 5, fill="#9AA6B4")
    ic.rect(sx + 16, sy + 30, 34, 9, rx=4.5, fill="#2A6BE8")
    _cursor(ic, sx + 48, sy + 34, 0.9)
    ic.rect(100, 196, 56, 10, rx=5, fill=two(ic, *BRASS))


# --- Parsec: a gamepad on a star chart, the mark on its middle --------------

@soft("parsec")
def parsec(ic):
    tile(ic, "#3A3A6E", "#14142E")
    soft_shadow(ic, 128, 214, 104, 12)
    with ic.g(transform="rotate(-7 128 110)"):
        ic.rect(36, 30, 186, 150, rx=8, fill=two(ic, "#22305E", "#121A3C"))
        for r in (34, 60):
            ic.circle(140, 98, r, fill="none", stroke="#9FB0E0", stroke_opacity=0.25, stroke_width=2)
        stars = [(64, 54, 3), (86, 64, 2.4), (108, 50, 3.4), (124, 70, 2.6), (160, 52, 4), (188, 64, 2.6),
                 (200, 84, 3)]
        ic.path("M64 54 L86 64 L108 50 L124 70 L160 52 L188 64 L200 84", fill="none", stroke="#E9D7A0",
                stroke_opacity=0.55, stroke_width=2)
        for x, y, r in stars:
            ic.circle(x, y, r, fill="#F6E7B6")
    pad = ("M66 112 C66 100 76 94 88 94 H168 C180 94 190 100 190 112 L208 176 C213 196 196 210 180 200"
           " L160 184 H96 L76 200 C60 210 43 196 48 176 Z")
    ic.path(pad, fill=two(ic, "#F4F5F7", "#B8BCC3"))
    dx, dy = 90, 128
    ic.path(f"M{dx - 6} {dy - 17}h12v11h11v12h-11v11h-12v-11h-11v-12h11z", fill="#3A3D43")
    bx, by = 166, 128
    for (ox, oy), c in (((0, -12), "#F2C45C"), ((12, 0), "#E5574A"), ((0, 12), "#5BBF6A"), ((-12, 0), "#4C8FE0")):
        ic.circle(bx + ox, by + oy, 6.5, fill=c)
    for sx in (108, 148):
        ic.circle(sx, 160, 13, fill=two(ic, "#5A5E65", "#2A2D32"))
    ic.rect(110, 104, 36, 28, rx=9, fill="#1B1C22")
    for dx_, dy_ in ((-2, -6), (2, 0), (-2, 6)):
        ic.rect(128 + dx_ - 8, 118 + dy_ - 2, 16, 4, rx=2, fill="#F3F4F6")


# --- WireGuard: a network plug, its boot red with the serpent badge ----------

def _serpent(ic, cx, cy, r, fill):
    """A serpent curled almost to a ring, its head turned in."""
    a = polar(cx, cy, r * 0.62, 200)
    b = polar(cx, cy, r * 0.62, 128)
    ic.path(f"M{a[0]:.1f} {a[1]:.1f}A{r * 0.62} {r * 0.62} 0 1 1 {b[0]:.1f} {b[1]:.1f}", fill="none", stroke=fill,
            stroke_width=r * 0.36, stroke_linecap="round")
    hx, hy = polar(cx, cy, r * 0.6, 156)
    ic.ellipse(hx - r * 0.12, hy - r * 0.08, r * 0.38, r * 0.27, fill=fill,
               transform=f"rotate(-30 {hx - r * 0.12:.1f} {hy - r * 0.08:.1f})")


@soft("wireguard")
def wireguard(ic):
    tile(ic, "#8E2A26", "#3E0C0A")
    soft_shadow(ic, 140, 216, 92, 11)
    cable = "M128 150 C128 196 150 206 186 204 C224 202 230 160 206 138 C190 124 170 120 150 112"
    ic.path(cable, fill="none", stroke="#2A2C30", stroke_width=16, stroke_linecap="round")
    hx, hy, hw, hh = 92, 34, 72, 66
    ic.rect(hx, hy, hw, hh, rx=10, fill=two(ic, "#F4F7F9", "#C3CCD3"))
    for k in range(8):
        ic.rect(hx + 10 + k * 7.4, hy + 6, 4.4, 18, rx=2, fill="#D9A84E")
    top = hy + hh - 4
    boot = (f"M{hx - 4} {top + 6}a6 6 0 0 1 6 -6h{hw - 4}a6 6 0 0 1 6 6V{top + 48}L136 {top + 76}h-16"
            f"L{hx - 4} {top + 48}z")
    ic.path(boot, fill=two(ic, "#D8463E", "#8E1812"))
    cx, cy = 128, top + 26
    ic.circle(cx, cy, 22, fill=two(ic, *STEEL))
    ic.circle(cx, cy, 19, fill="#A01E18")
    _serpent(ic, cx, cy, 15, "#FFFFFF")


# --- Mullvad VPN: the mole by its tunnel, under a hill ----------------------

@soft("mullvad-vpn")
def mullvad(ic):
    tile(ic, "#2E5A86", "#122A46")
    soft_shadow(ic, 128, 216, 108, 11)
    ic.path("M16 212 C30 132 72 70 128 68 C184 70 226 132 240 212 Z", fill=two(ic, "#6E9A50", "#2E5026"))
    cx, cy, ro, ri = 128, 150, 58, 42
    ic.path(f"M{cx - ro} 212 V{cy} a{ro} {ro} 0 0 1 {2 * ro} 0 V212 Z", fill=two(ic, "#C4BFB2", "#8A857A"))
    ic.path(f"M{cx - ri} 212 V{cy} a{ri} {ri} 0 0 1 {2 * ri} 0 V212 Z", fill="#0C1116")
    for k in (2, 5, 8):
        x1, y1 = polar(cx, cy, ri, -90 + k * 18)
        x2, y2 = polar(cx, cy, ro, -90 + k * 18)
        ic.line(x1, y1, x2, y2, stroke="#7A766C", stroke_width=2.5)
    ic.rect(cx - 30, cy - ro - 10, 60, 16, rx=5, fill=two(ic, *BRASS))
    ic.path("M92 212 C90 176 104 156 128 156 C152 156 166 176 164 212 Z", fill=two(ic, "#F2C460", "#B87E28"))
    for side in (-1, 1):
        ic.circle(128 + side * 15, 178, 3.4, fill="#1A1208")
    ic.ellipse(128, 190, 9, 7, fill="#E98A92")
    ic.path("M30 212 C70 200 100 202 128 204 C160 206 196 200 226 212 Z", fill="#6B4A2A")
    for px, rot in ((100, 20), (156, -20)):
        with ic.g(transform=f"rotate({rot} {px} 204)"):
            ic.ellipse(px, 204, 15, 9, fill="#E07E88")


# --- 1Password: a round vault door, its keyhole badge in the middle ----------

@soft("1password")
def onepassword(ic):
    tile(ic, "#2A6FD0", "#0C2F6A")
    soft_shadow(ic, 128, 218, 92, 12)
    cx, cy = 128, 120
    ic.circle(cx, cy, 102, fill="#1A1D21")
    ic.rect(212, 92, 22, 56, rx=8, fill=two(ic, *STEEL))
    ic.circle(cx, cy, 94, fill=two(ic, "#D9DDE1", "#8D949C"))
    ic.circle(cx, cy, 80, fill=two(ic, "#C3C8CE", "#9AA1A9"))
    for k in range(8):
        x, y = polar(cx, cy, 87, k * 45 + 22.5)
        ic.circle(x, y, 4, fill="#6F767E")
    for a in (45, 135, 225, 315):
        ex, ey = polar(cx, cy, 68, a)
        ic.line(cx, cy, ex, ey, stroke="#7A8189", stroke_width=10, stroke_linecap="round")
        ic.circle(ex, ey, 9, fill=two(ic, "#E6E9EC", "#8D949C"))
    r = 42
    ic.circle(cx, cy, r + 5, fill=two(ic, "#E6E9EC", "#9AA1A9"))
    ic.circle(cx, cy, r, fill=two(ic, "#2F8CFF", "#0850B8"))
    ic.circle(cx, cy, r - 8, fill="none", stroke="#fff", stroke_width=5.5)
    ic.path(f"M{cx - 6} {cy - 21}h12v17l-4 4 4 4v17h-12v-15l4 -4 -4 -4z", fill="#fff", stroke="#fff",
            stroke_width=1, stroke_linejoin="round")


# --- Proton Pass: a violet key card on a badge reel -------------------------

@soft("proton-pass")
def proton_pass(ic):
    tile(ic, "#4A3690", "#1A1040")
    soft_shadow(ic, 132, 212, 100, 12)
    rx_, ry_ = 62, 44
    ic.rect(rx_ - 8, ry_ - 30, 16, 26, rx=5, fill=two(ic, *STEEL))
    ic.circle(rx_, ry_, 21, fill="#2A2C30")
    ic.circle(rx_, ry_, 14, fill=two(ic, "#A27BFF", "#5A3AD0"))
    ic.path(f"M{rx_ + 8} {ry_ + 18} C{rx_ + 14} {ry_ + 28} 76 76 82 80", fill="none", stroke="#1A1C20",
            stroke_width=3.5, stroke_linecap="round")
    with ic.g(transform="translate(-8 6) rotate(14 140 136)"):
        x, y, w, h = 52, 78, 176, 112
        ic.rect(x, y, w, h, rx=16, fill=two(ic, "#B48CFF", "#5A36D8"))
        ic.rect(x + 14, y + 9, 28, 8, rx=4, fill="#2A1460")
        ic.rect(x + 16, y + 34, 34, 28, rx=7, fill=two(ic, *BRASS))
        mx, my = x + 128, y + 48
        ic.path(f"M{mx - 18} {my + 28}V{my - 18}a6 6 0 0 1 6 -6h14a20 20 0 0 1 0 40h-8v10a4 4 0 0 1 -4 4h-4"
                f"a4 4 0 0 1 -4 -4z", fill="#FFFFFF")
        ic.circle(mx + 1, my + 2, 6.5, fill="#6D4AFF")
        ic.path(f"M{mx - 2} {my + 6}h6l1.5 10h-9z", fill="#6D4AFF")
        bar(ic, x + 16, y + 76, 76, 9, fill="#FFFFFF")
        bar(ic, x + 16, y + 92, 48, 6, fill="#F1EAFF", opacity=0.7)
    ic.circle(84, 83, 5.5, fill="none", stroke="#C3C8CE", stroke_width=3)


# --- Authenticator: a key fob counting a six-digit code down ----------------

@soft("authenticator")
def authenticator(ic):
    tile(ic, "#2E7C78", "#103A38")
    soft_shadow(ic, 124, 198, 104, 12)
    with ic.g(transform="rotate(-10 128 128)"):
        ic.circle(214, 110, 22, fill="none", stroke="#C3C8CE", stroke_width=6)
        body = ("M28 96 a32 32 0 0 1 32 -32 H180 a34 34 0 0 1 34 34 v24 a34 34 0 0 1 -34 34 H60 "
                "a32 32 0 0 1 -32 -32z")
        ic.path(body, fill=two(ic, "#E2E6EA", "#A3AAB2"))
        ic.path("M180 64 a34 34 0 0 1 34 34 v24 a34 34 0 0 1 -34 34 H170 V64z", fill=two(ic, "#58A9E8", "#1E64A8"))
        ic.circle(196, 110, 8, fill="#0E2E50")
        ic.rect(42, 80, 120, 50, rx=12, fill="#1A1C20")
        ic.rect(49, 87, 106, 36, rx=5, fill=two(ic, "#D2E2D8", "#AFC6B8"))
        # the code as three pairs of blocks, the countdown as bars
        for k in range(3):
            ic.rect(76 + k * 26, 95, 20, 20, rx=4, fill="#1E2A22")
        for k in range(3):
            ic.rect(56, 94 + k * 8, 10, 5, rx=2, fill="#1E2A22", opacity=0.85 if k else 0.15)
        bar(ic, 48, 140, 60, 7, fill="#4A5058")
        ic.circle(152, 143, 4.5, fill="#4FD07A")


# --- Cryptomator: a green crate, padlocked, on its way to the cloud ----------

@soft("cryptomator")
def cryptomator(ic):
    tile(ic, "#2F5E44", "#10281C")
    soft_shadow(ic, 128, 216, 102, 12)
    ic.path("M150 70 a22 22 0 0 1 40 -14 a18 18 0 0 1 30 14 a16 16 0 0 1 0 32 H160 a16 16 0 0 1 -10 -32z",
            fill=two(ic, "#FFFFFF", "#D2E0D8"))
    x, y, w, h = 36, 92, 184, 116
    ic.rect(x, y, w, h, rx=10, fill=two(ic, "#6CBC5E", "#2E7A30"))
    for k in range(1, 4):
        ic.rect(x + 8, y + k * h / 4 - 1.5, w - 16, 3, fill="#1A4A1C", opacity=0.45)
    for bx in (x, x + w - 18):
        ic.rect(bx, y, 18, h, rx=8, fill=two(ic, "#5DB052", "#26662C"))
    ic.rect(x, y, w, 16, rx=8, fill=two(ic, "#8AD27A", "#4A9A44"))
    bar(ic, x + 34, y + h - 22, 60, 8, fill="#F2F6EE", opacity=0.7)
    ic.rect(114, y + 8, 28, 40, rx=5, fill=two(ic, *STEEL))
    by, bh = _padlock(ic, 128, y + 20, 52, two(ic, "#8DE07A", "#2E8030"))
    ic.circle(128, by + 16, 6, fill="#123A14")
    ic.path(f"M125 {by + 18}l-2.5 13h11l-2.5 -13z", fill="#123A14")


# --- VeraCrypt: a hard drive, locked, its key lying across it ---------------

@soft("veracrypt")
def veracrypt(ic):
    tile(ic, "#36507A", "#141F38")
    soft_shadow(ic, 128, 216, 96, 12)
    with ic.g(transform="rotate(-6 128 120)"):
        x, y, w, h = 52, 26, 150, 190
        ic.rect(x, y, w, h, rx=14, fill=two(ic, "#DDE1E5", "#9AA1A9"))
        ic.circle(x + 75, y + 62, 46, fill="none", stroke="#7A828C", stroke_opacity=0.6, stroke_width=3)
        ic.circle(x + 75, y + 62, 12, fill=two(ic, "#8D949C", "#C9CED4"))
        lx, ly, lw, lh = x + 14, y + 118, w - 28, 58
        ic.rect(lx, ly, lw, lh, rx=6, fill="#FFFFFF")
        ic.path(f"M{lx} {ly + 6} a6 6 0 0 1 6 -6 H{lx + lw - 6} a6 6 0 0 1 6 6 V{ly + 16} H{lx}z", fill="#2A6AD0")
        bar(ic, lx + 8, ly + 26, 58, 7, fill="#3A4048")
        bar(ic, lx + 8, ly + 40, 44, 6, fill="#9AA1A9")
        for k in range(5):
            ic.rect(lx + 84 + k * 6, ly + 26, 3, 22, rx=1, fill="#2A2C30")
    by, bh = _padlock(ic, 58, 66, 42, two(ic, "#E8C878", "#A8782E"))
    ic.circle(58, by + 13, 4.5, fill="#3A2A10")
    ic.path(f"M55.5 {by + 15}l-2 10h9l-2 -10z", fill="#3A2A10")
    with ic.g(transform="rotate(32 160 120)"):
        kx, ky = 150, 112
        ic.path(f"M{kx + 20} {ky - 6}H{kx + 96}v12h-6v6h-7v-6h-6v8h-7v-8H{kx + 20}z", fill=two(ic, *STEEL))
        ic.circle(kx, ky, 25, fill=two(ic, "#E6E9EC", "#9AA1A9"))
        ic.circle(kx, ky, 20, fill=two(ic, "#3A8AE8", "#1A4E9E"))
        ic.circle(kx - 11, ky, 4.5, fill="#0E1E3A")
        ic.path(f"M{kx - 3} {ky - 9}l6 18l6 -18", fill="none", stroke="#fff", stroke_width=4.5,
                stroke_linecap="round", stroke_linejoin="round", transform=f"rotate(-32 {kx + 3} {ky})")
