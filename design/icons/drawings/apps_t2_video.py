"""The theme's video players and media centres: Celluloid, Videos (Totem),
Haruna, SMPlayer, Kodi, Jellyfin, Plex, Stremio, FreeTube
(docs/feat/object-icons.md, Part 2). Each a different object, apart from
inua's own Video (a clapperboard) and the helpers' VLC (a cone), mpv and
OBS."""

from lib import (brass, glare, graphite, icon, paper, polar, shadow, small, steel, tile, wood)


def _play(ic, cx, cy, s, fill, **kw):
    """A play triangle with rounded corners, s px tall, its middle at
    (cx, cy)."""
    w = s * 0.12
    pts = [(cx - s * 0.36, cy - s * 0.5 + w), (cx + s * 0.5 - w, cy), (cx - s * 0.36, cy + s * 0.5 - w)]
    ic.poly(pts, fill=fill, stroke=fill, stroke_width=w * 2, stroke_linejoin="round", **kw)


def _rounded(pts, r):
    """A polygon's outline with its corners rounded by r."""
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
    """A ring's sector between radii r1 < r2 and angles a1 < a2 (0 up)."""
    p1, p2 = polar(cx, cy, r2, a1), polar(cx, cy, r2, a2)
    p3, p4 = polar(cx, cy, r1, a2), polar(cx, cy, r1, a1)
    return (f"M{p1[0]:.1f} {p1[1]:.1f}A{r2} {r2} 0 0 1 {p2[0]:.1f} {p2[1]:.1f}"
            f"L{p3[0]:.1f} {p3[1]:.1f}A{r1} {r1} 0 0 0 {p4[0]:.1f} {p4[1]:.1f}Z")


def _knob(ic, cx, cy, r, tone="dark"):
    """A round control knob with its pointer."""
    ic.circle(cx + 1, cy + 1.6, r, fill="#000", opacity=0.3)
    if tone == "dark":
        ic.circle(cx, cy, r, fill=ic.lin([(0, "#5A5E66"), (1, "#1C1E22")], 0, 0, 1, 1))
    else:
        ic.circle(cx, cy, r, fill=brass(ic))
    ic.circle(cx, cy, r * 0.72, fill="none", stroke="#fff", stroke_opacity=0.18)
    ic.line(cx, cy - r * 0.2, cx + r * 0.45, cy - r * 0.75, stroke="#F2F0EA", stroke_width=max(1, r * 0.16),
            stroke_linecap="round")


# --- Celluloid: a strip of celluloid film, its frames the blue play mark ----

def _film(ic, x, y, length, frames, frame, dark=False):
    """A strip of film at (x, y), 72 px wide, frames drawn by frame(ic, fx, fy)."""
    h = 72
    base = ic.lin([(0, "#4A3420"), (0.5, "#2A1C10"), (1, "#3A2716")]) if not dark else \
        ic.lin([(0, "#2F241A"), (1, "#18110A")])
    ic.rect(x + 2, y + 5, length, h, rx=3, fill="#000", opacity=0.28)
    ic.rect(x, y, length, h, rx=3, fill=base)
    # the amber of the celluloid along the edges
    ic.rect(x, y, length, 13, fill="#C98A3A", opacity=0.22)
    ic.rect(x, y + h - 13, length, 13, fill="#C98A3A", opacity=0.22)
    ic.line(x + 2, y + 0.8, x + length - 2, y + 0.8, stroke="#F6D49A", stroke_opacity=0.5, stroke_width=1.2)
    hole = "#E9DCC2" if not dark else "#B8AC95"
    for k in range(int(length / 12)):
        hx = x + 4 + k * 12
        ic.rect(hx, y + 3.5, 6, 6, rx=1.4, fill=hole)
        ic.rect(hx, y + h - 9.5, 6, 6, rx=1.4, fill=hole)
    fw = 62
    gap = (length - frames * fw) / (frames + 1)
    for k in range(frames):
        fx = x + gap + k * (fw + gap)
        frame(ic, fx, y + 15, fw, h - 30)


def _celluloid_frame(ic, fx, fy, fw, fh):
    ic.rect(fx, fy, fw, fh, rx=2, fill=ic.lin([(0, "#BFE3FA"), (1, "#6FB5E6")]))
    cx, cy = fx + fw / 2, fy + fh / 2
    ic.circle(cx, cy, fh * 0.4, fill=ic.lin([(0, "#3E9BE6"), (1, "#1A5FB0")], 0, 0, 1, 1))
    ic.circle(cx, cy, fh * 0.4, fill="none", stroke="#0E3E78", stroke_opacity=0.5)
    _play(ic, cx + 1.2, cy, fh * 0.38, "#FFFFFF")
    ic.rect(fx, fy, fw, fh * 0.45, rx=2, fill="#fff", opacity=0.14)


@icon("celluloid", kind="app", title="Celluloid",
      names=["celluloid", "gnome-mpv", "io.github.celluloid_player.Celluloid", "mplayer"])
def celluloid(ic):
    tile(ic, "#3A6E9E", "#173556")
    shadow(ic, 128, 212, 102, 12)

    def faint(ic, fx, fy, fw, fh):
        ic.rect(fx, fy, fw, fh, rx=2, fill="#6E8FA8", opacity=0.55)

    with ic.g(transform="rotate(10 128 128)"):
        _film(ic, 36, 44, 184, 3, faint, dark=True)
    # a strip of splicing tape on the strip behind, its label
    with ic.g(transform="rotate(10 128 128)"):
        ic.rect(150, 38, 52, 22, rx=2, fill="#F7F2E4", opacity=0.94)
        ic.rect(150, 38, 52, 22, rx=2, fill="none", stroke="#000", stroke_opacity=0.08)
        ic.text("reel 2", 176, 54, 14, font="hand", anchor="middle", fill="#1F4E86")
    with ic.g(transform="rotate(-12 128 128)"):
        _film(ic, 22, 106, 212, 3, _celluloid_frame)
        ic.text("CELLULOID 35", 42, 174.5, 5.6, font="mono-semibold", spacing=1, fill="#F2B45A", opacity=0.9)
        ic.text("12", 118, 174.5, 5.6, font="mono-semibold", fill="#F2B45A", opacity=0.9)
        ic.text("13", 186, 174.5, 5.6, font="mono-semibold", fill="#F2B45A", opacity=0.9)


@small("celluloid")
def celluloid16(ic):
    tile(ic, "#3A6E9E", "#173556")
    with ic.g(transform="rotate(-12 8 8)"):
        ic.rect(0.5, 3.8, 15, 8.4, rx=0.5, fill="#2A1C10")
        for x in (2, 5, 8, 11, 14):
            ic.rect(x - 0.5, 4.4, 1, 1, fill="#E9DCC2")
            ic.rect(x - 0.5, 10.6, 1, 1, fill="#E9DCC2")
        ic.rect(2, 6, 12, 4, fill="#8CC6EE")
        ic.circle(8, 8, 1.8, fill="#2470C8")
        ic.path("M7.4 7 L9.1 8 L7.4 9z", fill="#fff")


# --- Videos (Totem): a steel film reel, wound, its leader taped --------------

@icon("totem", kind="app", title="Videos", names=["org.gnome.Totem", "totem"])
def totem(ic):
    tile(ic, "#4C5B6C", "#1F2832")
    cx, cy, R = 120, 118, 92
    shadow(ic, 128, 214, 96, 11)
    # the leader, run off the reel onto the desk
    ic.path("M196 150 C210 168 218 184 222 204 L206 208 C202 190 194 174 184 160z", fill="#2A1C10")
    ic.path("M196 150 C210 168 218 184 222 204", fill="none", stroke="#C98A3A", stroke_opacity=0.5, stroke_width=1.5)
    # the reel's back flange, a sliver to the lower right
    ic.circle(cx + 4, cy + 5, R, fill="#2C3138")
    # the film wound on it
    ic.circle(cx, cy, 74, fill=ic.rad([(0, "#3E2A18"), (0.7, "#24170C"), (1, "#3A2716")]))
    for r in range(34, 74, 4):
        ic.circle(cx, cy, r, fill="none", stroke="#D19A50", stroke_opacity=0.10)
    # the front flange, five windows through it
    holes = "".join(_sector_d(cx, cy, 34, 78, a - 26, a + 26) for a in (36, 108, 180, 252, 324))
    ic.path(_circle_d(cx, cy, R) + holes, fill=ic.lin([(0, "#E3E7EC"), (0.45, "#A8B0B9"), (1, "#5E6670")], 0, 0, 1, 1),
            fill_rule="evenodd")
    ic.path(holes, fill="none", stroke="#30363E", stroke_opacity=0.6, stroke_width=1.5)
    ic.circle(cx, cy, R - 1, fill="none", stroke="#fff", stroke_opacity=0.4, stroke_width=1.5)
    ic.circle(cx, cy, R - 6, fill="none", stroke="#000", stroke_opacity=0.15, stroke_width=1)
    # the hub, a play stamped in it
    ic.circle(cx, cy, 24, fill=steel(ic, False))
    ic.circle(cx, cy, 24, fill="none", stroke="#000", stroke_opacity=0.25)
    ic.circle(cx, cy, 17, fill=ic.lin([(0, "#4A90E8"), (1, "#1C5BB4")], 0, 0, 1, 1))
    _play(ic, cx + 1.5, cy, 15, "#FFFFFF")
    for a in (0, 120, 240):
        x, y = polar(cx, cy, 20.5, a)
        ic.circle(x, y, 1.6, fill="#3A4048")
    # a label on the flange
    with ic.g(transform=f"rotate(0 {cx} {cy})"):
        ic.rect(cx - 25, cy - 88, 50, 17, rx=2, fill=paper(ic, "cream"))
        ic.rect(cx - 25, cy - 88, 50, 17, rx=2, fill="none", stroke="#000", stroke_opacity=0.12)
        ic.text("VIDEOS", cx, cy - 75.5, 9, font="sans-bold", anchor="middle", spacing=1.2, fill="#1C3F73")
    # tape on the leader
    with ic.g(transform="rotate(66 208 184)"):
        ic.rect(192, 177, 32, 13, rx=1.5, fill="#F2E2A8", opacity=0.92)
        ic.text("END", 208, 187, 8, font="mono-semibold", anchor="middle", fill="#7A5A1A")
    ic.path(f"M{cx - 80} {cy - 30}a86 86 0 0 1 60-56 92 92 0 0 0-60 56z", fill="#fff", opacity=0.55)


@small("totem")
def totem16(ic):
    tile(ic, "#4C5B6C", "#1F2832")
    ic.circle(8, 8, 6.4, fill="#B4BBC4")
    for a in (36, 108, 180, 252, 324):
        x, y = polar(8, 8, 3.7, a)
        ic.circle(x, y, 1.5, fill="#2A1C10")
    ic.circle(8, 8, 1.9, fill="#2A6FD0")
    ic.path("M7.6 7.2 L9 8 L7.6 8.8z", fill="#fff")


# --- Haruna: a cine projector in rose enamel, two reels up, its beam on -------

def _reel(ic, cx, cy, r, film=0.7):
    ic.circle(cx + 1.5, cy + 2.5, r, fill="#000", opacity=0.3)
    ic.circle(cx, cy, r * film, fill="#24170C")
    holes = "".join(_sector_d(cx, cy, r * 0.3, r * 0.82, a - 30, a + 30) for a in (0, 120, 240))
    ic.path(_circle_d(cx, cy, r) + holes, fill=ic.lin([(0, "#E3E7EC"), (0.5, "#A8B0B9"), (1, "#5E6670")], 0, 0, 1, 1),
            fill_rule="evenodd")
    ic.circle(cx, cy, r - 0.8, fill="none", stroke="#fff", stroke_opacity=0.4, stroke_width=1.2)
    ic.circle(cx, cy, r * 0.2, fill=steel(ic, False))
    ic.circle(cx, cy, r * 0.07, fill="#30363E")


@icon("haruna", kind="app", title="Haruna", names=["haruna", "org.kde.haruna", "sc-apps-haruna"])
def haruna(ic):
    tile(ic, "#5E2F5A", "#2A1229")
    shadow(ic, 120, 210, 96, 11)
    # the beam
    ic.path("M206 148 L256 112 L256 196 z", fill=ic.lin([(0, "#FFE8F2", 0.35), (1, "#FFE8F2", 0)], 0, 0, 1, 0))
    # the arms that carry the reels
    for x1, y1, x2, y2 in ((84, 70, 96, 128), (162, 62, 150, 128)):
        ic.line(x1, y1, x2, y2, stroke="#2A2C30", stroke_width=7, stroke_linecap="round")
        ic.line(x1 - 1, y1, x2 - 1, y2, stroke="#fff", stroke_opacity=0.18, stroke_width=1.5)
    _reel(ic, 162, 62, 34)
    _reel(ic, 84, 70, 40)
    # the film between them and down into the gate
    ic.path("M84 30 Q124 18 162 28", fill="none", stroke="#2A1C10", stroke_width=3)
    ic.path("M122 60 Q120 96 118 124", fill="none", stroke="#2A1C10", stroke_width=3)
    ic.path("M124 61 L124 66", stroke="#C98A3A", stroke_opacity=0.5)
    # the body
    rose = ic.lin([(0, "#F67AA8"), (0.5, "#D9437C"), (1, "#8E1F4C")], 0, 0, 0.6, 1)
    ic.rect(44, 124, 146, 70, rx=14, fill=rose)
    ic.path("M58 124h118a14 14 0 0 1 14 14v2H44v-2a14 14 0 0 1 14-14z", fill="#fff", opacity=0.3)
    ic.line(58, 125, 176, 125, stroke="#fff", stroke_opacity=0.7, stroke_width=1.5)
    # vents
    for k in range(5):
        ic.rect(140, 146 + k * 7, 34, 3, rx=1.5, fill="#6E1438", opacity=0.55)
    # the badge, play in a ring
    ic.circle(92, 159, 21, fill="#F9EEF3")
    ic.circle(92, 159, 21, fill="none", stroke="#6E1438", stroke_opacity=0.4)
    ic.circle(92, 159, 16, fill=ic.lin([(0, "#E95A93"), (1, "#9C2459")], 0, 0, 1, 1))
    _play(ic, 93.5, 159, 15, "#FFFFFF")
    ic.text("HARUNA", 120, 187, 7, font="mono-semibold", spacing=1.6, fill="#FFE0EC", opacity=0.85)
    # the lens barrel and its glass
    ic.rect(188, 138, 22, 22, fill=steel(ic, False))
    ic.rect(190, 134, 8, 30, rx=2, fill=graphite(ic))
    ic.ellipse(210, 149, 6, 13, fill=ic.rad([(0, "#9FD6FF"), (0.6, "#3D5E86"), (1, "#14202E")], cx=0.4, cy=0.4))
    ic.ellipse(209, 145, 2, 4, fill="#fff", opacity=0.7)
    # the feet and a knob
    ic.rect(56, 192, 20, 10, rx=3, fill="#2A2C30")
    ic.rect(160, 192, 20, 10, rx=3, fill="#2A2C30")
    _knob(ic, 60, 140, 7)


@small("haruna")
def haruna16(ic):
    tile(ic, "#5E2F5A", "#2A1229")
    ic.circle(5.5, 4.6, 3, fill="#B4BBC4")
    ic.circle(10.8, 4.2, 2.5, fill="#B4BBC4")
    ic.circle(5.5, 4.6, 0.8, fill="#3A4048")
    ic.circle(10.8, 4.2, 0.7, fill="#3A4048")
    ic.rect(2.5, 8, 10, 5.5, rx=1.2, fill="#D9437C")
    ic.rect(12.5, 9.4, 2, 2.6, fill="#9AA1A9")
    ic.path("M5.6 9.3 L8 10.75 L5.6 12.2z", fill="#fff")


# --- SMPlayer: a little portable TV in blue plastic, its orb on screen -------

@icon("smplayer", kind="app", title="SMPlayer", names=["appimagekit-smplayer", "info.smplayer.SMPlayer", "smplayer"])
def smplayer(ic):
    tile(ic, "#B97A30", "#6A3E10")
    shadow(ic, 128, 214, 92, 11)
    # the carrying handle
    ic.path("M72 74 V58 a14 14 0 0 1 14-14 h84 a14 14 0 0 1 14 14 V74", fill="none", stroke="#14406E", stroke_width=10,
            stroke_linecap="round")
    ic.path("M72 74 V58 a14 14 0 0 1 14-14 h84 a14 14 0 0 1 14 14 V74", fill="none", stroke="#2F7BC8", stroke_width=7,
            stroke_linecap="round")
    ic.path("M74 66 V58 a12 12 0 0 1 12-12 h40", fill="none", stroke="#fff", stroke_opacity=0.4, stroke_width=1.5)
    # the case
    blue = ic.lin([(0, "#5DB2F2"), (0.5, "#2C7ED0"), (1, "#16529A")], 0, 0, 0.5, 1)
    ic.rect(36, 70, 184, 136, rx=26, fill="#0E3A6A", transform="translate(0 4)")
    ic.rect(36, 70, 184, 136, rx=26, fill=blue)
    ic.path("M62 70h132a26 26 0 0 1 26 26v2H36v-2a26 26 0 0 1 26-26z", fill="#fff", opacity=0.22)
    ic.path("M56 71.5h144", stroke="#fff", stroke_opacity=0.65, stroke_width=1.5, stroke_linecap="round")
    # the screen, a bulging tube
    ic.rect(50, 84, 122, 104, rx=20, fill="#0F2C4C")
    ic.rect(55, 89, 112, 94, rx=18, fill=ic.rad([(0, "#24364E"), (1, "#070C14")], cx=0.4, cy=0.4, r=0.8))
    # the orb and its play
    ic.circle(111, 136, 46, fill=ic.rad([(0, "#7FD3FF", 0.35), (1, "#7FD3FF", 0)]))
    ic.circle(111, 136, 30, fill=ic.rad([(0, "#8EDBFF"), (0.55, "#2B8CE0"), (1, "#0D3E86")], cx=0.38, cy=0.32, r=0.75))
    ic.circle(111, 136, 30, fill="none", stroke="#BFE9FF", stroke_opacity=0.35)
    _play(ic, 114, 136, 28, "#FFFFFF")
    ic.ellipse(100, 120, 12, 6, fill="#fff", opacity=0.4, transform="rotate(-30 100 120)")
    ic.path("M55 107a18 18 0 0 1 18-18h56L72 183h-0a18 18 0 0 1-17-18z", fill=glare(ic, 1.1))
    # the side panel: dials, a grille
    _knob(ic, 196, 102, 11)
    _knob(ic, 196, 132, 8)
    for k in range(6):
        ic.rect(184, 150 + k * 5.5, 24, 2.5, rx=1.25, fill="#0E3A6A", opacity=0.6)
    ic.text("SMPLAYER", 111, 199, 7, font="mono-semibold", anchor="middle", spacing=1.6, fill="#E4F3FF", opacity=0.85)
    ic.circle(196, 194, 2.4, fill="#FF9E3D")


@small("smplayer")
def smplayer16(ic):
    tile(ic, "#B97A30", "#6A3E10")
    ic.path("M4.5 4.5 V3.4 a1 1 0 0 1 1-1 h5 a1 1 0 0 1 1 1 V4.5", fill="none", stroke="#2F7BC8", stroke_width=1)
    ic.rect(1.5, 4.2, 13, 9.6, rx=2, fill="#2C7ED0")
    ic.rect(2.6, 5.3, 8.4, 7.4, rx=1.4, fill="#0A1422")
    ic.circle(6.8, 9, 2.6, fill="#3E9BE6")
    ic.path("M6.1 7.8 L8.1 9 L6.1 10.2z", fill="#fff")
    ic.circle(12.8, 7, 0.9, fill="#1C1E22")
    ic.circle(12.8, 9.6, 0.7, fill="#1C1E22")


# --- Kodi: a living-room media box, its blue mark lit, the remote by it -------

def _kodi_mark(ic, cx, cy, s, fill, **kw):
    """Kodi's mark, redrawn: four tiles set in a diamond, the left one tall."""
    k = s / 2
    parts = [
        [(-1, 0), (-0.6, -0.7), (-0.2, 0), (-0.6, 0.7)],
        [(0, -0.9), (0.4, -0.5), (0, -0.1), (-0.4, -0.5)],
        [(0.1, 0), (0.5, -0.4), (0.9, 0), (0.5, 0.4)],
        [(0, 0.1), (0.4, 0.5), (0, 0.9), (-0.4, 0.5)],
    ]
    for p in parts:
        ic.path(_rounded([(cx + x * k, cy + y * k) for x, y in p], k * 0.06), fill=fill, **kw)


@icon("kodi", kind="app", title="Kodi", names=["kodi", "tv.kodi.Kodi"])
def kodi(ic):
    tile(ic, "#1F3B58", "#0A1828")
    shadow(ic, 128, 196, 108, 12)
    # the top, brushed aluminium, seen a little from above
    ic.path("M54 74 H202 L226 116 H30 Z", fill=ic.lin([(0, "#E4E8EC"), (0.5, "#B5BCC4"), (1, "#8A929B")]))
    for k in range(1, 9):
        y = 74 + k * 4.6
        ic.line(54 - k * 2.66, y, 202 + k * 2.66, y, stroke="#fff", stroke_opacity=0.18, stroke_width=0.8)
    ic.line(55, 74.8, 201, 74.8, stroke="#fff", stroke_opacity=0.9, stroke_width=1.5)
    # the blue mark, inlaid in the lid, foreshortened
    with ic.g(transform="translate(128 95) scale(1 0.42) translate(-128 -95)"):
        _kodi_mark(ic, 128, 95, 58, "#17B2E7", opacity=0.9)
    # the front, glossy black
    ic.rect(30, 116, 196, 62, rx=4, fill=ic.lin([(0, "#34383E"), (0.15, "#1A1C20"), (1, "#0A0B0D")]))
    ic.line(31, 116.8, 225, 116.8, stroke="#fff", stroke_opacity=0.3, stroke_width=1.5)
    # the lit mark on the front
    ic.circle(66, 147, 26, fill=ic.rad([(0, "#17B2E7", 0.35), (1, "#17B2E7", 0)]))
    _kodi_mark(ic, 66, 147, 38, ic.lin([(0, "#6FD8FF"), (1, "#0F8FC4")], 0, 0, 1, 1))
    # the display
    ic.rect(100, 134, 84, 26, rx=3, fill="#05070A")
    ic.rect(100, 134, 84, 26, rx=3, fill="none", stroke="#fff", stroke_opacity=0.1)
    ic.text("KODI", 106, 151, 12, font="mono-semibold", spacing=1.4, fill="#38C6F4")
    ic.text("21:04", 178, 151, 8, font="mono", anchor="end", fill="#38C6F4", opacity=0.7)
    ic.circle(206, 147, 3, fill="#38C6F4")
    ic.circle(206, 147, 7, fill=ic.rad([(0, "#38C6F4", 0.5), (1, "#38C6F4", 0)]))
    ic.path("M30 120 h196 v16 L30 168z", fill="#fff", opacity=0.05)
    # the feet
    ic.rect(44, 177, 22, 5, rx=2, fill="#050608")
    ic.rect(190, 177, 22, 5, rx=2, fill="#050608")
    # the remote, lying in front
    with ic.g(transform="rotate(-8 128 204)"):
        ic.rect(70, 196, 120, 18, rx=9, fill="#000", opacity=0.35, transform="translate(1 3)")
        ic.rect(70, 196, 120, 18, rx=9, fill=ic.lin([(0, "#3A3E44"), (1, "#141518")]))
        ic.line(78, 196.8, 182, 196.8, stroke="#fff", stroke_opacity=0.25)
        ic.circle(160, 205, 6.5, fill="#26292E")
        ic.circle(160, 205, 2.8, fill="#17B2E7")
        for x in (92, 104, 116, 128):
            ic.circle(x, 205, 2.4, fill="#4A4F57")


@small("kodi")
def kodi16(ic):
    tile(ic, "#1F3B58", "#0A1828")
    ic.path("M3.5 5 H12.5 L14.5 7.5 H1.5z", fill="#B5BCC4")
    ic.rect(1.5, 7.5, 13, 5, rx=0.5, fill="#141518")
    _kodi_mark(ic, 5, 10, 6, "#17B2E7")
    ic.rect(9, 9.3, 4, 1.4, fill="#38C6F4", opacity=0.8)


# --- Jellyfin: a glass jellyfish lamp, the arch in its purple-blue -----------

@icon("jellyfin", kind="app", title="Jellyfin", names=[
    "com.github.iwalton3.jellyfin-media-player", "com.github.iwalton3.jellyfin-mpv-shim", "jellyfin",
    "jellyfin-desktop", "jellyfinmediaplayer", "org.jellyfin.JellyfinServer"])
def jellyfin(ic):
    tile(ic, "#173F4F", "#07202A")
    shadow(ic, 128, 214, 76, 10)
    # the glow on the wall
    ic.circle(128, 104, 104, fill=ic.rad([(0, "#9C6BE0", 0.42), (0.5, "#4A8FE0", 0.14), (1, "#4A8FE0", 0)]))
    # the strands, hanging from the bell to the base
    for k, x in enumerate((70, 88, 106, 120, 136, 150, 168, 186)):
        sway = 7 if k % 2 else -7
        d = f"M{x} 152 C{x + sway} 168 {x - sway} 180 {128 + (x - 128) * 0.5:.1f} 198"
        ic.path(d, fill="none", stroke="#7AC8F2" if k % 2 else "#C08AEA", stroke_width=2.2, stroke_opacity=0.85,
                stroke_linecap="round")
    # the bell: the outer arch
    outer = [(128, 28), (222, 154), (34, 154)]
    glow = ic.lin([(0, "#B65DD6"), (0.55, "#7A6BE0"), (1, "#14A8E4")], 0, 0, 1, 1)
    ic.path(_rounded(outer, 26), fill="#000", opacity=0.25, transform="translate(2 4)")
    ic.path(_rounded(outer, 26), fill=glow)
    # the frosted ring and the inner arch
    ring = [(128, 60), (190, 146), (66, 146)]
    ic.path(_rounded(ring, 16), fill="#F3ECFF", opacity=0.85)
    inner = [(128, 76), (178, 142), (78, 142)]
    ic.path(_rounded(inner, 13), fill=ic.lin([(0, "#D98CF2"), (0.5, "#8E7CF0"), (1, "#3CC2F4")], 0, 0, 1, 1))
    ic.path(_rounded(inner, 13), fill=ic.rad([(0, "#fff", 0.55), (1, "#fff", 0)], cx=0.5, cy=0.65, r=0.5))
    # glass light from the top left
    ic.path("M118 40 Q94 78 60 134 Q68 134 72 128 Q98 84 122 44z", fill="#fff", opacity=0.45)
    ic.path(_rounded(outer, 26), fill="none", stroke="#fff", stroke_opacity=0.25, stroke_width=1.5)
    # the scalloped rim
    for k in range(10):
        x = 50 + k * 17.3
        ic.circle(x, 153, 6, fill=ic.lin([(0, "#8A70E4"), (1, "#2C7CC8")]))
    # the base, a turned walnut puck
    ic.ellipse(128, 202, 44, 9, fill="#2A160A")
    ic.path("M84 196 a44 9 0 0 0 88 0 v6 a44 9 0 0 1-88 0z", fill=wood(ic, "#8A5630", "#4A2810"))
    ic.ellipse(128, 196, 44, 9, fill=wood(ic, "#B47A48", "#6A3C18"))
    ic.ellipse(128, 196, 30, 5.5, fill=ic.rad([(0, "#E6D6FF", 0.9), (1, "#8A70E4", 0.3)]))


@small("jellyfin")
def jellyfin16(ic):
    tile(ic, "#173F4F", "#07202A")
    ic.path(_rounded([(8, 1.8), (14, 10.6), (2, 10.6)], 1.8), fill="#8E6AE0")
    ic.path(_rounded([(8, 4.2), (11.6, 9.8), (4.4, 9.8)], 1.1), fill="#EDE4FF")
    ic.path(_rounded([(8, 5.4), (10.6, 9.4), (5.4, 9.4)], 0.8), fill="#3CB4F0")
    ic.path("M5 11 l-.6 2 M8 11 v2.2 M11 11 l.6 2", stroke="#7AC8F2", stroke_width=0.8, stroke_linecap="round")
    ic.rect(4.5, 13.2, 7, 1.6, rx=0.8, fill="#9A6236")


# --- Plex: a black streaming box, the gold chevron on its face --------------

@icon("plex", kind="app", title="Plex", names=[
    "plex", "plex-desktop", "plex-media-player", "plexhometheater", "plexmediamanager", "plexmediaplayer",
    "plexmediaserver", "tv.plex.PlexDesktop"])
def plex(ic):
    tile(ic, "#3E3A34", "#151311")
    shadow(ic, 128, 206, 100, 12)
    T, Rt, F, L = (128, 40), (218, 80), (128, 120), (38, 80)
    h = 82
    Fb, Lb, Rb = (F[0], F[1] + h), (L[0], L[1] + h), (Rt[0], Rt[1] + h)
    # the faces
    ic.poly([L, F, Fb, Lb], fill=ic.lin([(0, "#2E2F33"), (1, "#0E0F11")], 0, 0, 1, 1))
    ic.poly([F, Rt, Rb, Fb], fill=ic.lin([(0, "#18191C"), (1, "#060708")], 0, 0, 1, 1))
    ic.poly([T, Rt, F, L], fill=ic.lin([(0, "#4A4C52"), (0.6, "#24262A"), (1, "#141518")], 0, 0, 1, 1))
    # gloss on the top
    ic.poly([T, (158, 53), (68, 93), L], fill="#fff", opacity=0.08)
    mt = f"matrix({(Rt[0] - T[0]) / 100:.3f} {(Rt[1] - T[1]) / 100:.3f} {(L[0] - T[0]) / 100:.3f} {(L[1] - T[1]) / 100:.3f} {T[0]} {T[1]})"
    with ic.g(transform=mt):
        ic.circle(50, 50, 30, fill="none", stroke="#000", stroke_opacity=0.45, stroke_width=2.4)
        ic.circle(50, 50, 30, fill="none", stroke="#fff", stroke_opacity=0.12, stroke_width=1, transform="translate(-1 -1)")
        ic.circle(50, 50, 22, fill=ic.rad([(0, "#EBAF00", 0.18), (1, "#EBAF00", 0)]))
    ic.line(L[0], L[1], T[0], T[1], stroke="#fff", stroke_opacity=0.35, stroke_width=1.5)
    ic.line(L[0], L[1], F[0], F[1], stroke="#fff", stroke_opacity=0.25, stroke_width=1.5)
    ic.line(F[0], F[1], Fb[0], Fb[1], stroke="#fff", stroke_opacity=0.15, stroke_width=1.2)
    # the chevron, on the left face
    m = f"matrix({(F[0] - L[0]) / 100:.3f} {(F[1] - L[1]) / 100:.3f} 0 {h / 100:.3f} {L[0]} {L[1]})"
    with ic.g(transform=m):
        chev = [(30, 16), (54, 16), (78, 50), (54, 84), (30, 84), (54, 50)]
        ic.path(_rounded(chev, 2.5), fill="#000", opacity=0.4, transform="translate(1.5 2)")
        ic.path(_rounded(chev, 2.5), fill=ic.lin([(0, "#FFD15C"), (0.5, "#EBAF00"), (1, "#C27C00")], 0, 0, 1, 1))
        ic.path("M31 17.5 H53 L60 27", fill="none", stroke="#FFF2C4", stroke_width=1.2, opacity=0.7)
    # the name, on the right face
    m2 = f"matrix({(Rt[0] - F[0]) / 100:.3f} {(Rt[1] - F[1]) / 100:.3f} 0 {h / 100:.3f} {F[0]} {F[1]})"
    with ic.g(transform=m2):
        ic.text("plex", 50, 60, 30, font="sans-bold", anchor="middle", fill="#D8D6D0", opacity=0.75)
        ic.circle(86, 86, 2.6, fill="#EBAF00")
    # the feet's shadow line
    ic.poly([Lb, Fb, Rb, (Rb[0], Rb[1] + 3), (Fb[0], Fb[1] + 3), (Lb[0], Lb[1] + 3)], fill="#000", opacity=0.6)


@small("plex")
def plex16(ic):
    tile(ic, "#3E3A34", "#151311")
    ic.poly([(8, 2), (14, 4.6), (8, 7.2), (2, 4.6)], fill="#3A3C40")
    ic.poly([(2, 4.6), (8, 7.2), (8, 13.6), (2, 11)], fill="#1E1F22")
    ic.poly([(8, 7.2), (14, 4.6), (14, 11), (8, 13.6)], fill="#0C0D0F")
    ic.poly([(3.6, 6.4), (5, 7), (6.6, 9.6), (5, 11.6), (3.6, 11), (5.1, 9)], fill="#EBAF00")


# --- Stremio: a cinema ticket, its purple play badge printed on it ---------

def _ticket_d(x0, y0, x1, y1, px, nr=8, r=6):
    return (f"M{x0 + r} {y0}H{px - nr}a{nr} {nr} 0 0 0 {2 * nr} 0H{x1 - r}q{r} 0 {r} {r}V{y1 - r}q0 {r}-{r} {r}"
            f"H{px + nr}a{nr} {nr} 0 0 0 {-2 * nr} 0H{x0 + r}q-{r} 0-{r}-{r}V{y0 + r}q0-{r} {r}-{r}z")


@icon("stremio", kind="app", title="Stremio", names=["com.stremio.Stremio", "smartcode-stremio", "stremio"])
def stremio(ic):
    tile(ic, "#2E2A5E", "#12102E")
    shadow(ic, 128, 206, 104, 12)
    # yesterday's ticket, under it
    with ic.g(transform="rotate(9 128 128)"):
        ic.path(_ticket_d(34, 70, 222, 166, 172), fill=ic.lin([(0, "#9C86D8"), (1, "#5E46A0")]))
        ic.line(172, 80, 172, 156, stroke="#2E1F66", stroke_opacity=0.4, stroke_dasharray="3 3")
    with ic.g(transform="rotate(-7 128 128)"):
        d = _ticket_d(28, 82, 228, 186, 176)
        ic.path(d, fill="#000", opacity=0.3, transform="translate(2 4)")
        ic.path(d, fill=ic.lin([(0, "#F6F1FF"), (1, "#D8CCF4")], 0, 0, 1, 1))
        # the printed band
        band = ic.clip(f'<path d="{d}"/>')
        with ic.g(clip_path=band):
            ic.rect(28, 82, 200, 16, fill=ic.lin([(0, "#8A5CF0"), (1, "#5B2FC2")], 0, 0, 1, 0))
            ic.rect(28, 176, 200, 10, fill=ic.lin([(0, "#8A5CF0"), (1, "#5B2FC2")], 0, 0, 1, 0))
        ic.text("ADMIT ONE", 36, 94, 9, font="mono-semibold", spacing=1.6, fill="#F6F1FF")
        ic.text("CINEMA", 168, 94, 7, font="mono", anchor="end", spacing=1, fill="#E4D8FF")
        # the badge: a purple tile set on its corner, a play in it
        bx, by = 70, 136
        ic.path(_rounded([(bx, by - 32), (bx + 32, by), (bx, by + 32), (bx - 32, by)], 9), fill="#3C1E8A",
                transform="translate(1.5 2.5)", opacity=0.5)
        ic.path(_rounded([(bx, by - 32), (bx + 32, by), (bx, by + 32), (bx - 32, by)], 9),
                fill=ic.lin([(0, "#A57CFF"), (0.5, "#7B4CE8"), (1, "#4E24B4")], 0, 0, 1, 1))
        ic.path(f"M{bx - 24} {by - 2} L{bx - 2} {by - 24}", stroke="#fff", stroke_opacity=0.4, stroke_width=1.5,
                stroke_linecap="round")
        _play(ic, bx + 2, by, 22, "#FFFFFF")
        ic.text("Stremio", 110, 128, 15, font="sans-bold", fill="#3A1E86")
        ic.text("SCREEN 4", 110, 143, 7, font="mono-semibold", spacing=0.8, fill="#5E4C8E")
        ic.text("ROW F · 21:30", 110, 153, 7, font="mono-semibold", spacing=0.8, fill="#5E4C8E")
        # the perforation and the stub
        ic.line(176, 92, 176, 176, stroke="#5B2FC2", stroke_opacity=0.5, stroke_width=1.4, stroke_dasharray="2.5 3")
        with ic.g(transform="rotate(-90 203 136)"):
            ic.text("SEAT 12", 203, 132, 10, font="sans-bold", anchor="middle", fill="#3A1E86")
            ic.text("No 0428", 203, 145, 7, font="mono", anchor="middle", fill="#5E4C8E")
        ic.line(36, 99, 168, 99, stroke="#fff", stroke_opacity=0.5)


@small("stremio")
def stremio16(ic):
    tile(ic, "#2E2A5E", "#12102E")
    with ic.g(transform="rotate(-7 8 8)"):
        ic.path(_ticket_d(1, 3.5, 15, 12.5, 11.5, 1.2, 0.8), fill="#EEE7FF")
        ic.rect(1, 3.5, 14, 1.4, fill="#7B4CE8")
        ic.path(_rounded([(5.4, 5.2), (8.4, 8.2), (5.4, 11.2), (2.4, 8.2)], 0.8), fill="#7B4CE8")
        ic.path("M4.9 7.2 L6.6 8.2 L4.9 9.2z", fill="#fff")
        ic.rect(9, 7.5, 2, 0.8, fill="#7B4CE8", opacity=0.6)


# --- FreeTube: a walnut television, rabbit ears up, the red play on it -------

@icon("freetube", kind="app", title="FreeTube", names=["freetube", "freetube-bin", "io.freetubeapp.FreeTube"])
def freetube(ic):
    tile(ic, "#3F6152", "#192C24")
    shadow(ic, 128, 214, 96, 11)
    # the rabbit ears
    for x2, y2 in ((70, 24), (190, 30)):
        ic.line(128, 78, x2, y2, stroke="#5D636B", stroke_width=3.6, stroke_linecap="round")
        ic.line(128, 78, x2, y2, stroke="#D4D8DD", stroke_width=1.4, stroke_linecap="round")
        ic.circle(x2, y2, 3.6, fill=steel(ic, False))
    ic.path("M110 80 a18 14 0 0 1 36 0z", fill=graphite(ic))
    # the legs
    ic.path("M62 196 l-8 18 h7 l11-18z", fill="#3A2210")
    ic.path("M194 196 l8 18 h-7 l-11-18z", fill="#3A2210")
    # the cabinet
    ic.rect(34, 78, 188, 122, rx=16, fill=wood(ic, "#B97A44", "#5E3416"))
    for y in (92, 112, 136, 160, 182):
        ic.path(f"M40 {y} q60 -4 120 2 t58 -2", fill="none", stroke="#3A1E0A", stroke_opacity=0.18, stroke_width=1.2)
    ic.path("M50 78h156a16 16 0 0 1 16 16v1H34v-1a16 16 0 0 1 16-16z", fill="#fff", opacity=0.18)
    ic.line(50, 79.2, 206, 79.2, stroke="#FFE3C0", stroke_opacity=0.6, stroke_width=1.5)
    # the screen, set in a cream mask
    ic.rect(46, 90, 124, 98, rx=14, fill="#E9DFC8")
    ic.rect(46, 90, 124, 98, rx=14, fill="none", stroke="#000", stroke_opacity=0.2)
    ic.rect(54, 97, 108, 84, rx=20, fill=ic.rad([(0, "#2E3A44"), (1, "#080B0E")], cx=0.4, cy=0.4, r=0.8))
    # the red play
    ic.circle(108, 139, 40, fill=ic.rad([(0, "#FF5A5F", 0.3), (1, "#FF5A5F", 0)]))
    ic.rect(80, 120, 56, 38, rx=11, fill=ic.lin([(0, "#F4525A"), (1, "#B8202C")]))
    ic.rect(80, 120, 56, 38, rx=11, fill="none", stroke="#FFB0B4", stroke_opacity=0.35)
    _play(ic, 110, 139, 20, "#FFFFFF")
    scan = ic.define('<pattern id="{id}" width="4" height="3" patternUnits="userSpaceOnUse">'
                     '<rect width="4" height="1" fill="#000" opacity=".35"/></pattern>', "p")
    ic.rect(54, 97, 108, 84, rx=20, fill=f"url(#{scan})", opacity=0.45)
    ic.path("M54 117a20 20 0 0 1 20-20h48L74 181h0a20 20 0 0 1-20-20z", fill=glare(ic, 1.2))
    # the control panel
    ic.rect(178, 92, 34, 96, rx=6, fill="#2A1A0E", opacity=0.35)
    _knob(ic, 195, 110, 10, "brass")
    _knob(ic, 195, 138, 7, "brass")
    for k in range(5):
        ic.rect(184, 154 + k * 5, 22, 2.4, rx=1.2, fill="#1E1208", opacity=0.6)
    ic.text("FreeTube", 128, 197, 7.5, font="sans-semibold", anchor="middle", spacing=0.6, fill="#FFE3C0", opacity=0.8)


@small("freetube")
def freetube16(ic):
    tile(ic, "#3F6152", "#192C24")
    ic.path("M8 5.5 L4.5 1.5 M8 5.5 L11.8 1.8", stroke="#C3C8CE", stroke_width=0.8, stroke_linecap="round")
    ic.rect(1.5, 5, 13, 9, rx=1.6, fill="#9A6236")
    ic.rect(2.5, 6, 8.6, 7, rx=1.4, fill="#0E1216")
    ic.rect(4, 7.6, 5.6, 3.8, rx=1, fill="#E23A44")
    ic.path("M6.2 8.6 L7.8 9.5 L6.2 10.4z", fill="#fff")
    ic.circle(12.8, 7.6, 0.9, fill="#E2B04A")
    ic.circle(12.8, 10.2, 0.7, fill="#E2B04A")
