"""Soft drawings of the video players and media centres (drawings/
apps_t2_video.py): the same objects with about half the detail, no text."""

from lib import bar, polar, soft, soft_shadow, tile, two


def _play(ic, cx, cy, s, fill):
    """A play triangle with rounded corners, s px tall, its middle at (cx, cy)."""
    w = s * 0.14
    pts = [(cx - s * 0.36, cy - s * 0.5 + w), (cx + s * 0.5 - w, cy), (cx - s * 0.36, cy + s * 0.5 - w)]
    ic.poly(pts, fill=fill, stroke=fill, stroke_width=w * 2, stroke_linejoin="round")


def _rounded(pts, r):
    n = len(pts)
    d = ""
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        a = _toward(p1, p0, r)
        b = _toward(p1, p2, r)
        d += ("M" if i == 0 else "L") + f"{a[0]:.1f} {a[1]:.1f}Q{p1[0]:.1f} {p1[1]:.1f} {b[0]:.1f} {b[1]:.1f}"
    return d + "Z"


def _toward(p, q, r):
    dx, dy = q[0] - p[0], q[1] - p[1]
    k = r / (dx * dx + dy * dy) ** 0.5
    return p[0] + dx * k, p[1] + dy * k


def _circle_d(cx, cy, r):
    return f"M{cx - r:.1f} {cy:.1f}a{r} {r} 0 1 0 {2 * r} 0a{r} {r} 0 1 0 {-2 * r} 0Z"


def _sector_d(cx, cy, r1, r2, a1, a2):
    p1, p2 = polar(cx, cy, r2, a1), polar(cx, cy, r2, a2)
    p3, p4 = polar(cx, cy, r1, a2), polar(cx, cy, r1, a1)
    return (f"M{p1[0]:.1f} {p1[1]:.1f}A{r2} {r2} 0 0 1 {p2[0]:.1f} {p2[1]:.1f}"
            f"L{p3[0]:.1f} {p3[1]:.1f}A{r1} {r1} 0 0 0 {p4[0]:.1f} {p4[1]:.1f}Z")


def _knob(ic, cx, cy, r, light="#5A5E66", dark="#2A2C31"):
    ic.circle(cx, cy, r, fill=two(ic, light, dark))
    ic.rect(cx - r * 0.12, cy - r * 0.85, r * 0.24, r * 0.6, rx=r * 0.12, fill="#F2F0EA",
            transform=f"rotate(35 {cx} {cy})")


# --- Celluloid: a strip of film, its frames the blue play mark --------------

def _film(ic, x, y, length, frames, frame, base, hole):
    h = 72
    ic.rect(x, y, length, h, rx=6, fill=base)
    n = int((length - 8) / 26)
    step = (length - 11) / n
    for k in range(n):
        hx = x + 6 + k * step + (step - 11) / 2
        ic.rect(hx, y + 3.5, 11, 9, rx=3, fill=hole)
        ic.rect(hx, y + h - 12.5, 11, 9, rx=3, fill=hole)
    fw = 58
    gap = (length - frames * fw) / (frames + 1)
    for k in range(frames):
        frame(ic, x + gap + k * (fw + gap), y + 16, fw, h - 32)


@soft("celluloid")
def celluloid(ic):
    tile(ic, "#3A6E9E", "#173556")
    soft_shadow(ic, 128, 212, 100, 12)

    def faint(ic, fx, fy, fw, fh):
        ic.rect(fx, fy, fw, fh, rx=4, fill="#6E8FA8", opacity=0.55)

    def blue(ic, fx, fy, fw, fh):
        ic.rect(fx, fy, fw, fh, rx=4, fill=two(ic, "#BFE3FA", "#7DBDE8"))
        cx, cy = fx + fw / 2, fy + fh / 2
        ic.circle(cx, cy, fh * 0.42, fill=two(ic, "#3E9BE6", "#1A5FB0"))
        _play(ic, cx + 1.5, cy, fh * 0.4, "#FFFFFF")

    with ic.g(transform="rotate(10 128 128)"):
        _film(ic, 36, 44, 184, 3, faint, "#2A2018", "#B8AC95")
    with ic.g(transform="rotate(-12 128 128)"):
        _film(ic, 22, 106, 212, 3, blue, two(ic, "#45301D", "#2A1C10"), "#E9DCC2")


# --- Videos (Totem): a steel film reel, a play on its hub -------------------

@soft("totem")
def totem(ic):
    tile(ic, "#4C5B6C", "#1F2832")
    cx, cy, R = 120, 118, 92
    soft_shadow(ic, 128, 214, 96, 11)
    ic.path("M196 150 C210 168 218 184 222 204 L204 210 C200 190 192 174 182 160z", fill="#2A1C10")
    ic.circle(cx + 4, cy + 5, R, fill="#2C3138")
    ic.circle(cx, cy, 76, fill="#2E2014")
    for r in (48, 62):
        ic.circle(cx, cy, r, fill="none", stroke="#D19A50", stroke_opacity=0.15, stroke_width=2)
    holes = "".join(_sector_d(cx, cy, 36, 76, a - 25, a + 25) for a in (36, 108, 180, 252, 324))
    ic.path(_circle_d(cx, cy, R) + holes, fill=two(ic, "#D2D7DD", "#8D949C"), fill_rule="evenodd")
    ic.circle(cx, cy, 26, fill=two(ic, "#AEB4BB", "#8D949C"))
    ic.circle(cx, cy, 19, fill=two(ic, "#4A90E8", "#1C5BB4"))
    _play(ic, cx + 2, cy, 17, "#FFFFFF")


# --- Haruna: a cine projector in rose enamel, two reels up ------------------

def _reel(ic, cx, cy, r):
    ic.circle(cx, cy, r * 0.7, fill="#2E2014")
    holes = "".join(_sector_d(cx, cy, r * 0.32, r * 0.8, a - 30, a + 30) for a in (0, 120, 240))
    ic.path(_circle_d(cx, cy, r) + holes, fill=two(ic, "#D2D7DD", "#8D949C"), fill_rule="evenodd")
    ic.circle(cx, cy, r * 0.18, fill="#5E6670")


@soft("haruna")
def haruna(ic):
    tile(ic, "#5E2F5A", "#2A1229")
    soft_shadow(ic, 120, 210, 96, 11)
    ic.path("M206 148 L256 112 L256 196 z", fill=ic.lin([(0, "#FFE8F2", 0.3), (1, "#FFE8F2", 0)], 0, 0, 1, 0))
    for x1, y1, x2, y2 in ((84, 70, 96, 128), (162, 62, 150, 128)):
        ic.line(x1, y1, x2, y2, stroke="#2A2C30", stroke_width=9, stroke_linecap="round")
    _reel(ic, 162, 62, 34)
    _reel(ic, 84, 70, 40)
    ic.path("M122 60 Q120 96 118 124", fill="none", stroke="#2A1C10", stroke_width=4)
    ic.rect(42, 122, 150, 74, rx=18, fill=two(ic, "#EE6A9C", "#A82A5C"))
    for k in range(3):
        bar(ic, 140, 148 + k * 12, 34, 6, fill="#6E1438", opacity=0.5)
    ic.circle(92, 159, 23, fill="#F9EEF3")
    ic.circle(92, 159, 17, fill=two(ic, "#E95A93", "#9C2459"))
    _play(ic, 94, 159, 16, "#FFFFFF")
    ic.rect(188, 136, 22, 26, rx=4, fill=two(ic, "#AEB4BB", "#8D949C"))
    ic.ellipse(210, 149, 7, 14, fill=two(ic, "#7FB6E6", "#2E4A6C"))
    ic.rect(56, 192, 22, 12, rx=4, fill="#2A2C30")
    ic.rect(158, 192, 22, 12, rx=4, fill="#2A2C30")


# --- SMPlayer: a little portable TV in blue plastic, its orb on screen ------

@soft("smplayer")
def smplayer(ic):
    tile(ic, "#B97A30", "#6A3E10")
    soft_shadow(ic, 128, 214, 92, 11)
    ic.path("M72 76 V58 a14 14 0 0 1 14-14 h84 a14 14 0 0 1 14 14 V76", fill="none", stroke="#1F5E9E",
            stroke_width=10, stroke_linecap="round")
    ic.rect(36, 70, 184, 136, rx=28, fill=two(ic, "#4A9FE6", "#1E62B0"))
    ic.rect(50, 84, 122, 104, rx=22, fill="#0F2C4C")
    ic.rect(56, 90, 110, 92, rx=18, fill=two(ic, "#24364E", "#0B121C"))
    ic.circle(111, 136, 32, fill=two(ic, "#5EC0F6", "#145AA8"))
    _play(ic, 114, 136, 28, "#FFFFFF")
    _knob(ic, 196, 104, 12)
    _knob(ic, 196, 136, 9)
    for k in range(3):
        bar(ic, 184, 158 + k * 11, 24, 6, fill="#0E3A6A", opacity=0.6)


# --- Kodi: a living-room media box, its blue mark lit, the remote by it -----

def _kodi_mark(ic, cx, cy, s, fill, **kw):
    k = s / 2
    parts = [
        [(-1, 0), (-0.6, -0.7), (-0.2, 0), (-0.6, 0.7)],
        [(0, -0.9), (0.4, -0.5), (0, -0.1), (-0.4, -0.5)],
        [(0.1, 0), (0.5, -0.4), (0.9, 0), (0.5, 0.4)],
        [(0, 0.1), (0.4, 0.5), (0, 0.9), (-0.4, 0.5)],
    ]
    for p in parts:
        ic.path(_rounded([(cx + x * k, cy + y * k) for x, y in p], k * 0.1), fill=fill, **kw)


@soft("kodi")
def kodi(ic):
    tile(ic, "#1F3B58", "#0A1828")
    soft_shadow(ic, 128, 196, 108, 12)
    ic.path(_rounded([(54, 74), (202, 74), (226, 116), (30, 116)], 6), fill=two(ic, "#DCE1E6", "#9EA6AF"))
    with ic.g(transform="translate(128 95) scale(1 0.42) translate(-128 -95)"):
        _kodi_mark(ic, 128, 95, 58, "#17B2E7", opacity=0.85)
    ic.rect(30, 112, 196, 66, rx=8, fill=two(ic, "#2A2D32", "#0E0F12"))
    _kodi_mark(ic, 66, 146, 40, two(ic, "#6FD8FF", "#0F8FC4"))
    ic.rect(100, 134, 84, 26, rx=5, fill="#05070A")
    bar(ic, 108, 143, 36, 8, fill="#38C6F4")
    bar(ic, 152, 143, 22, 8, fill="#38C6F4", opacity=0.5)
    ic.circle(206, 147, 4, fill="#38C6F4")
    ic.rect(44, 176, 22, 6, rx=3, fill="#050608")
    ic.rect(190, 176, 22, 6, rx=3, fill="#050608")
    with ic.g(transform="rotate(-8 128 204)"):
        ic.rect(70, 195, 120, 20, rx=10, fill=two(ic, "#3A3E44", "#16171A"))
        ic.circle(160, 205, 6.5, fill="#26292E")
        ic.circle(160, 205, 3.2, fill="#17B2E7")
        for x in (94, 110, 126):
            ic.circle(x, 205, 3, fill="#4A4F57")


# --- Jellyfin: a glass jellyfish lamp, the arch in its purple-blue ----------

@soft("jellyfin")
def jellyfin(ic):
    tile(ic, "#173F4F", "#07202A")
    soft_shadow(ic, 128, 214, 76, 10)
    ic.circle(128, 104, 104, fill=ic.rad([(0, "#9C6BE0", 0.35), (1, "#4A8FE0", 0)]))
    for k, x in enumerate((76, 100, 128, 156, 180)):
        sway = 7 if k % 2 else -7
        d = f"M{x} 152 C{x + sway} 168 {x - sway} 180 {128 + (x - 128) * 0.5:.1f} 198"
        ic.path(d, fill="none", stroke="#7AC8F2" if k % 2 else "#C08AEA", stroke_width=4, stroke_linecap="round")
    outer = [(128, 28), (222, 156), (34, 156)]
    ic.path(_rounded(outer, 28), fill=ic.lin([(0, "#B65DD6"), (1, "#14A8E4")], 0, 0, 1, 1))
    ic.path(_rounded([(128, 62), (188, 146), (68, 146)], 18), fill="#F3ECFF", opacity=0.9)
    ic.path(_rounded([(128, 80), (174, 142), (82, 142)], 14), fill=ic.lin([(0, "#D98CF2"), (1, "#3CC2F4")], 0, 0, 1, 1))
    ic.ellipse(128, 202, 44, 9, fill="#2A160A")
    ic.path("M84 196 a44 9 0 0 0 88 0 v6 a44 9 0 0 1-88 0z", fill="#5E3416")
    ic.ellipse(128, 196, 44, 9, fill=two(ic, "#B47A48", "#7A4A22"))
    ic.ellipse(128, 196, 28, 5, fill="#D8C6FA", opacity=0.8)


# --- Plex: a black streaming box, the gold chevron on its face --------------

@soft("plex")
def plex(ic):
    tile(ic, "#3E3A34", "#151311")
    soft_shadow(ic, 128, 206, 100, 12)
    T, Rt, F, L = (128, 40), (218, 80), (128, 120), (38, 80)
    h = 82
    Fb, Lb, Rb = (F[0], F[1] + h), (L[0], L[1] + h), (Rt[0], Rt[1] + h)
    ic.path(_rounded([L, F, Fb, Lb], 4), fill=two(ic, "#2C2D31", "#141517"))
    ic.path(_rounded([F, Rt, Rb, Fb], 4), fill=two(ic, "#18191C", "#08090A"))
    ic.path(_rounded([T, Rt, F, L], 5), fill=two(ic, "#4A4C52", "#24262A"))
    mt = (f"matrix({(Rt[0] - T[0]) / 100:.3f} {(Rt[1] - T[1]) / 100:.3f} {(L[0] - T[0]) / 100:.3f} "
          f"{(L[1] - T[1]) / 100:.3f} {T[0]} {T[1]})")
    with ic.g(transform=mt):
        ic.circle(50, 50, 30, fill="none", stroke="#16171A", stroke_width=4)
    m = f"matrix({(F[0] - L[0]) / 100:.3f} {(F[1] - L[1]) / 100:.3f} 0 {h / 100:.3f} {L[0]} {L[1]})"
    with ic.g(transform=m):
        chev = [(28, 14), (54, 14), (80, 50), (54, 86), (28, 86), (54, 50)]
        ic.path(_rounded(chev, 4), fill=two(ic, "#FFC93A", "#D99000"))
    m2 = f"matrix({(Rt[0] - F[0]) / 100:.3f} {(Rt[1] - F[1]) / 100:.3f} 0 {h / 100:.3f} {F[0]} {F[1]})"
    with ic.g(transform=m2):
        bar(ic, 24, 44, 52, 12, fill="#D8D6D0", opacity=0.6)
        ic.circle(86, 84, 3.5, fill="#EBAF00")


# --- Stremio: a cinema ticket, its purple play badge printed on it ----------

def _ticket_d(x0, y0, x1, y1, px, nr=9, r=8):
    return (f"M{x0 + r} {y0}H{px - nr}a{nr} {nr} 0 0 0 {2 * nr} 0H{x1 - r}q{r} 0 {r} {r}V{y1 - r}q0 {r}-{r} {r}"
            f"H{px + nr}a{nr} {nr} 0 0 0 {-2 * nr} 0H{x0 + r}q-{r} 0-{r}-{r}V{y0 + r}q0-{r} {r}-{r}z")


@soft("stremio")
def stremio(ic):
    tile(ic, "#2E2A5E", "#12102E")
    soft_shadow(ic, 128, 206, 104, 12)
    with ic.g(transform="rotate(9 128 128)"):
        ic.path(_ticket_d(34, 70, 222, 166, 172), fill=two(ic, "#9C86D8", "#6A52AE"))
    with ic.g(transform="rotate(-7 128 128)"):
        d = _ticket_d(28, 82, 228, 186, 176)
        ic.path(d, fill=two(ic, "#F6F1FF", "#DDD2F6"))
        band = ic.clip(f'<path d="{d}"/>')
        with ic.g(clip_path=band):
            ic.rect(28, 82, 200, 18, fill="#7B4CE8")
        bx, by = 70, 138
        ic.path(_rounded([(bx, by - 32), (bx + 32, by), (bx, by + 32), (bx - 32, by)], 10),
                fill=two(ic, "#9A70FA", "#5B2FC2"))
        _play(ic, bx + 2, by, 24, "#FFFFFF")
        bar(ic, 112, 120, 50, 10, fill="#3A1E86")
        bar(ic, 112, 138, 40, 6, fill="#8E7CC0")
        bar(ic, 112, 150, 46, 6, fill="#8E7CC0")
        ic.line(176, 104, 176, 176, stroke="#7B4CE8", stroke_opacity=0.5, stroke_width=3, stroke_dasharray="5 6",
                stroke_linecap="round")
        bar(ic, 196, 116, 8, 44, fill="#3A1E86", opacity=0.7)


# --- FreeTube: a walnut television, rabbit ears up, the red play on it ------

@soft("freetube")
def freetube(ic):
    tile(ic, "#3F6152", "#192C24")
    soft_shadow(ic, 128, 214, 96, 11)
    for x2, y2 in ((70, 24), (190, 30)):
        ic.line(128, 78, x2, y2, stroke="#AEB4BB", stroke_width=4.5, stroke_linecap="round")
        ic.circle(x2, y2, 5, fill="#AEB4BB")
    ic.path("M108 80 a20 15 0 0 1 40 0z", fill="#33363B")
    ic.path("M62 196 l-8 18 h8 l11-18z", fill="#3A2210")
    ic.path("M194 196 l8 18 h-8 l-11-18z", fill="#3A2210")
    ic.rect(34, 78, 188, 122, rx=20, fill=two(ic, "#B07440", "#6E401C"))
    ic.rect(46, 90, 124, 98, rx=18, fill="#E9DFC8")
    ic.rect(54, 97, 108, 84, rx=22, fill=two(ic, "#2A3540", "#0C1014"))
    ic.rect(80, 120, 56, 38, rx=12, fill=two(ic, "#F4525A", "#C02631"))
    _play(ic, 110, 139, 20, "#FFFFFF")
    _knob(ic, 195, 110, 11, "#E2B45E", "#B88433")
    _knob(ic, 195, 140, 8, "#E2B45E", "#B88433")
    for k in range(3):
        bar(ic, 184, 158 + k * 10, 22, 5, fill="#3A200C", opacity=0.55)
