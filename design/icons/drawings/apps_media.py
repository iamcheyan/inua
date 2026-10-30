"""The inua-objects theme, media: Spotify, VLC, mpv, Audacity, Kdenlive,
Shotcut, HandBrake, OBS Studio, Sunshine, Moonlight
(docs/feat/object-icons.md, Part 2)."""

import math

from lib import glare, graphite, icon, paper, polar, shadow, small, steel, tile, wood


def _f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def _crescent(cx, cy, r, ox, oy, r2):
    """The crescent left of a circle (cx, cy, r) when a circle (ox, oy, r2)
    is taken out of it: path data."""
    dx, dy = ox - cx, oy - cy
    d = math.hypot(dx, dy)
    a = (r * r - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(max(r * r - a * a, 0))
    mx, my = cx + a * dx / d, cy + a * dy / d
    p1 = (mx + h * dy / d, my - h * dx / d)
    p2 = (mx - h * dy / d, my + h * dx / d)
    return (f"M{_f(p1[0])} {_f(p1[1])}A{r} {r} 0 1 0 {_f(p2[0])} {_f(p2[1])}"
            f"A{r2} {r2} 0 0 1 {_f(p1[0])} {_f(p1[1])}Z")


def _ring(cx, cy, r):
    return f"M{_f(cx - r)} {_f(cy)}a{r} {r} 0 1 0 {_f(2 * r)} 0a{r} {r} 0 1 0 {_f(-2 * r)} 0z"


def _sector(cx, cy, r1, r2, a1, a2):
    """An annular sector, angles 0 up, clockwise."""
    p1, p2 = polar(cx, cy, r2, a1), polar(cx, cy, r2, a2)
    p3, p4 = polar(cx, cy, r1, a2), polar(cx, cy, r1, a1)
    return (f"M{_f(p1[0])} {_f(p1[1])}A{r2} {r2} 0 0 1 {_f(p2[0])} {_f(p2[1])}"
            f"L{_f(p3[0])} {_f(p3[1])}A{r1} {r1} 0 0 0 {_f(p4[0])} {_f(p4[1])}Z")


# --- Spotify: a bookshelf speaker with a green enamel badge -----------------

def _spotify_arcs(ic, cx, cy, s, colour, tilt=8):
    """The three arcs of Spotify's mark, redrawn, s the badge's radius."""
    with ic.g(transform=f"rotate({tilt} {cx} {cy})", fill="none", stroke=colour, stroke_linecap="round"):
        for w, y, bow, sw in ((0.62, -0.28, 0.24, 0.17), (0.52, 0.02, 0.2, 0.14), (0.42, 0.29, 0.15, 0.115)):
            ic.path(f"M{_f(cx - w * s)} {_f(cy + y * s + bow * s * 0.35)}"
                    f"Q{_f(cx)} {_f(cy + y * s - bow * s)} {_f(cx + w * s)} {_f(cy + y * s + bow * s * 0.35)}",
                    stroke_width=_f(sw * s))


@icon("spotify", kind="app", names=["com.spotify.Client", "spotify", "spotify-client"], title="Spotify")
def spotify(ic):
    tile(ic, "#2B3A31", "#0F1712")
    shadow(ic, 130, 216, 92, 11)
    # the cabinet: its right side, then its face
    ic.rect(56, 28, 156, 186, rx=16, fill="#08090A")
    ic.rect(48, 24, 156, 186, rx=16, fill=ic.lin([(0, "#3A3D41"), (0.12, "#26282B"), (1, "#141517")], 0, 0, 0.4, 1))
    ic.rect(48.75, 24.75, 154.5, 184.5, rx=15.25, fill="none", stroke="#fff", stroke_opacity=0.13, stroke_width=1.5)
    weave = ic.define('<pattern id="{id}" width="3" height="3" patternUnits="userSpaceOnUse">'
                      '<rect width="1.5" height="1.5" fill="#fff" opacity=".05"/>'
                      '<rect x="1.5" y="1.5" width="1.5" height="1.5" fill="#000" opacity=".25"/></pattern>', "p")
    ic.rect(58, 34, 136, 166, rx=9, fill="#1A1B1D")
    ic.rect(58, 34, 136, 166, rx=9, fill=f"url(#{weave})")
    ic.rect(58, 34, 136, 166, rx=9, fill="none", stroke="#000", stroke_opacity=0.5, stroke_width=1.5)
    # the badge: Spotify's green, in a steel bezel
    bx, by = 126, 76
    ic.circle(bx + 1.5, by + 3, 37, fill="#000", opacity=0.45)
    ic.circle(bx, by, 37, fill=ic.lin([(0, "#E6E9EC"), (0.5, "#9AA1A9"), (1, "#4D535A")], 0, 0, 1, 1))
    ic.circle(bx, by, 33, fill=ic.rad([(0, "#4BEA87"), (0.7, "#1DB954"), (1, "#128A3C")], cx=0.38, cy=0.32, r=0.8))
    _spotify_arcs(ic, bx, by + 1, 33, "#0E1A12")
    ic.path(f"M{bx - 29} {by - 7}a30 30 0 0 1 41 -23 34 34 0 0 0 -41 23z", fill="#fff", opacity=0.4)
    # the woofer
    wx, wy = 126, 158
    ic.circle(wx, wy + 2, 42, fill="#000", opacity=0.5)
    ic.circle(wx, wy, 41, fill=ic.lin([(0, "#5A5E64"), (1, "#1D1F22")], 0, 0, 1, 1))
    ic.circle(wx, wy, 36, fill=ic.rad([(0, "#2C2E31"), (0.75, "#121314"), (1, "#3A3D41")], cx=0.45, cy=0.42, r=0.6))
    ic.circle(wx, wy, 36, fill="none", stroke="#fff", stroke_opacity=0.12, stroke_width=1,
              stroke_dasharray="40 200", transform=f"rotate(200 {wx} {wy})")
    for r in (30, 24):
        ic.circle(wx, wy, r, fill="none", stroke="#fff", stroke_opacity=0.05)
    ic.circle(wx, wy, 14, fill=ic.rad([(0, "#55595F"), (1, "#16171A")], cx=0.35, cy=0.3, r=0.75))
    ic.ellipse(wx - 5, wy - 6, 5, 2.6, fill="#fff", opacity=0.3, transform=f"rotate(-35 {wx - 5} {wy - 6})")
    for a in (45, 135, 225, 315):
        sx, sy = polar(wx, wy, 38.5, a)
        ic.circle(sx, sy, 1.8, fill=steel(ic, False))
    ic.text("Spotify", 126, 208, 8, font="sans-semibold", anchor="middle", spacing=0.6, fill="#9AA1A9", opacity=0.75)
    # its rubber feet
    for x in (62, 180):
        ic.rect(x, 210, 14, 4, rx=2, fill="#050506")


@small("spotify")
def spotify16(ic):
    tile(ic, "#2B3A31", "#0F1712")
    ic.rect(4, 1.5, 8.5, 13, rx=1.2, fill="#1E2023")
    ic.circle(8.2, 5, 2.8, fill="#1ED760")
    ic.path("M6.6 4.4q1.7-.6 3.3.3M6.9 5.8q1.3-.4 2.5.2", stroke="#0E1A12", stroke_width=0.6, fill="none",
            stroke_linecap="round")
    ic.circle(8.2, 10.4, 2.6, fill="#5A5E64")
    ic.circle(8.2, 10.4, 1, fill="#16171A")


# --- VLC: a traffic cone on its base --------------------------------------

@icon("vlc", kind="app", names=["org.videolan.VLC", "vlc"], title="VLC")
def vlc(ic):
    tile(ic, "#4D5966", "#20272F")
    shadow(ic, 128, 214, 98, 12)
    top, bot, rt, rb = 34, 182, 12, 60

    def hw(y):
        return rt + (y - top) * (rb - rt) / (bot - top)

    def sag(y):
        return 3 + (y - top) * 0.06

    # the base: a square slab seen from a little above
    ic.path("M40 182h176l14 18v8a6 6 0 0 1-6 6H32a6 6 0 0 1-6-6v-8z", fill="#000", opacity=0.3, transform="translate(2 3)")
    ic.path("M40 182h176l14 18H26z", fill=ic.lin([(0, "#FF9A2E"), (1, "#E06A00")]))
    ic.path("M26 200h204v8a6 6 0 0 1-6 6H32a6 6 0 0 1-6-6z", fill=ic.lin([(0, "#C25300"), (1, "#8A3600")]))
    ic.line(27, 200.5, 229, 200.5, stroke="#FFC37A", stroke_opacity=0.7)
    ic.ellipse(128, 190, 66, 7, fill="#7A3000", opacity=0.45)
    # the cone
    body = (f"M{128 - rt} {top}L{_f(128 - rb)} {bot}Q128 {bot + sag(bot) * 2} {_f(128 + rb)} {bot}"
            f"L{128 + rt} {top}z")
    cone = ic.lin([(0, "#FFB869"), (0.3, "#FF8C1A"), (0.75, "#E46A00"), (1, "#A84600")], 0, 0, 1, 0)
    ic.path(body, fill=cone)
    clip = ic.clip(f'<path d="{body}"/>')
    white = ic.lin([(0, "#FFFFFF"), (0.4, "#F1F2F4"), (0.8, "#C9CDD2"), (1, "#9EA4AB")], 0, 0, 1, 0)
    with ic.g(clip_path=clip):
        for y1, y2 in ((74, 98), (124, 150)):
            ic.path(f"M60 {y1}Q128 {_f(y1 + sag(y1) * 2)} 196 {y1}V{y2}Q128 {_f(y2 + sag(y2) * 2)} 60 {y2}z",
                    fill=white)
            ic.path(f"M60 {y2}Q128 {_f(y2 + sag(y2) * 2)} 196 {y2}", fill="none", stroke="#7A3000",
                    stroke_opacity=0.35, stroke_width=1.5)
        # light down the left of the cone, shade down the right
        ic.path(f"M{_f(128 - rt * 0.4)} {top}L{_f(128 - rb * 0.55)} {bot + 6}L{_f(128 - rb * 0.38)} {bot + 6}"
                f"L{_f(128 - rt * 0.1)} {top}z", fill="#fff", opacity=0.3)
        ic.path(f"M{_f(128 + rt * 0.5)} {top}L{_f(128 + rb * 0.6)} {bot + 6}L{128 + rb} {bot + 6}L{128 + rt} {top}z",
                fill="#000", opacity=0.12)
    # the opening at the top
    ic.ellipse(128, top, rt, 3.5, fill="#7A3000")
    ic.ellipse(128, top + 0.8, rt - 2.5, 2.2, fill="#2A1200")
    ic.path(f"M{128 - rt} {top}a{rt} 3.5 0 0 0 {2 * rt} 0", fill="none", stroke="#FFD3A0", stroke_width=1.2)


@small("vlc")
def vlc16(ic):
    tile(ic, "#4D5966", "#20272F")
    ic.path("M2 12.5h12l1 1.5H1z", fill="#F08A1A")
    ic.path("M7.2 1.8h1.6L12 12.8H4z", fill="#FF8C1A")
    ic.path("M6.2 5.4h3.6l.8 2.4H5.4zM4.9 9.6h6.2l.7 2.2H4.2z", fill="#F4F4F4")


# --- mpv: a purple arcade button with a play mark --------------------------

@icon("mpv", kind="app", names=["io.mpv.Mpv", "mpv", "mpv-icon-8bit-64x64"], title="mpv")
def mpv(ic):
    tile(ic, "#4B3870", "#1E1434")
    shadow(ic, 128, 214, 96, 13)
    cx, cy = 128, 118
    # the panel it is set in: a square of black plastic, four screws
    ic.rect(30, 26, 196, 192, rx=22, fill="#000", opacity=0.35, transform="translate(2 4)")
    ic.rect(30, 26, 196, 188, rx=22, fill=ic.lin([(0, "#3A3542"), (1, "#16131B")], 0, 0, 0.5, 1))
    ic.rect(30.75, 26.75, 194.5, 186.5, rx=21.25, fill="none", stroke="#fff", stroke_opacity=0.12, stroke_width=1.5)
    for x, y in ((46, 42), (210, 42), (46, 198), (210, 198)):
        ic.circle(x, y, 5, fill=steel(ic, False))
        ic.line(x - 3, y - 1.5, x + 3, y + 1.5, stroke="#3A3E44", stroke_width=1.3)
    # the bezel, then the plunger's wall and its domed cap
    ic.circle(cx, cy + 6, 82, fill="#000", opacity=0.45)
    ic.circle(cx, cy, 82, fill=ic.lin([(0, "#6B4D9A"), (0.5, "#3F2A63"), (1, "#1F1233")], 0, 0, 1, 1))
    ic.circle(cx, cy, 81, fill="none", stroke="#fff", stroke_opacity=0.2, stroke_width=1.5,
              stroke_dasharray="120 400", transform=f"rotate(200 {cx} {cy})")
    ic.circle(cx, cy, 70, fill="#140B22")
    ic.circle(cx, cy + 8, 64, fill="#4A2386")
    ic.circle(cx, cy, 64, fill=ic.rad([(0, "#B98BF2"), (0.55, "#8452CC"), (1, "#552496")], cx=0.38, cy=0.32, r=0.75))
    # mpv's mark: a darker disc, a play triangle
    ic.circle(cx, cy, 44, fill=ic.rad([(0, "#5A2C98"), (1, "#3A1468")], cx=0.4, cy=0.35, r=0.7))
    ic.circle(cx, cy, 44, fill="none", stroke="#2A0E50", stroke_opacity=0.5, stroke_width=2)
    ic.circle(cx - 0.6, cy - 0.6, 44, fill="none", stroke="#D5B5FF", stroke_opacity=0.35, stroke_width=1,
              stroke_dasharray="90 300", transform=f"rotate(220 {cx} {cy})")
    tri = f"M{cx - 13} {cy - 24}L{cx + 24} {cy}L{cx - 13} {cy + 24}z"
    ic.path(tri, fill="#1E0A3A", opacity=0.5, transform="translate(1.2 1.6)")
    ic.path(tri, fill=ic.lin([(0, "#FFFFFF"), (1, "#DCC8F7")]), stroke="#F4ECFF", stroke_width=5,
            stroke_linejoin="round")
    # gloss on the dome
    ic.path(f"M{cx - 54} {cy - 14}a58 58 0 0 1 64 -46 66 66 0 0 0 -64 46z", fill="#fff", opacity=0.5)
    ic.ellipse(cx - 30, cy - 36, 10, 5, fill="#fff", opacity=0.35, transform=f"rotate(-38 {cx - 30} {cy - 36})")
    ic.text("mpv", 128, 207, 10, font="mono-semibold", anchor="middle", spacing=1, fill="#B9A6D6", opacity=0.7)


@small("mpv")
def mpv16(ic):
    tile(ic, "#4B3870", "#1E1434")
    ic.circle(8, 8, 6.2, fill="#2A1A44")
    ic.circle(8, 8, 5.2, fill="#9A68DC")
    ic.circle(8, 8, 3.6, fill="#4A1C84")
    ic.path("M7 6l3 2-3 2z", fill="#FFFFFF", stroke="#FFFFFF", stroke_width=0.6, stroke_linejoin="round")


# --- Audacity: headphones over a printed waveform --------------------------

@icon("audacity", kind="app", names=["audacity", "org.audacityteam.Audacity"], title="Audacity")
def audacity(ic):
    tile(ic, "#304C7E", "#15233F")
    shadow(ic, 128, 214, 104, 12)
    # the printout of a track
    with ic.g(transform="rotate(-3 128 150)"):
        ic.rect(36, 102, 184, 96, rx=4, fill="#000", opacity=0.25, transform="translate(2 3)")
        ic.rect(36, 102, 184, 96, rx=4, fill=paper(ic, "white"))
        for x in range(56, 216, 20):
            ic.line(x, 116, x, 192, stroke="#2F6FD6", stroke_opacity=0.12)
        ic.line(44, 116, 212, 116, stroke="#8C887F", stroke_opacity=0.5)
        for i, t in enumerate(("0:00", "0:05", "0:10", "0:15")):
            ic.text(t, 58 + i * 40, 112, 6, font="mono", fill="#8C887F")
        ic.line(44, 156, 212, 156, stroke="#E0483A", stroke_opacity=0.25)
        wave = ic.lin([(0, "#FF8A3D"), (0.5, "#F2542D"), (1, "#C9243A")], 0, 0, 0, 1)
        pts_t, pts_b = [], []
        for k in range(0, 85):
            x = 46 + k * 2
            env = 0.25 + 0.75 * abs(math.sin(k * 0.11)) * (0.6 + 0.4 * math.sin(k * 0.037 + 1))
            a = 34 * env * (0.55 + 0.45 * abs(math.sin(k * 1.7)))
            pts_t.append((x, 156 - a))
            pts_b.append((x, 156 + a * 0.92))
        d = "M" + "L".join(f"{_f(x)} {_f(y)}" for x, y in pts_t + pts_b[::-1]) + "Z"
        ic.path(d, fill=wave)
        ic.path(d, fill="none", stroke="#8A1A20", stroke_opacity=0.4, stroke_width=0.6)
        ic.text("take 3 · mono · 48 kHz", 46, 193, 6, font="mono", fill="#8C887F")
    # the headband
    band = "M56 150V112a72 70 0 0 1 144 0V150"
    ic.path(band, fill="none", stroke="#000", stroke_opacity=0.3, stroke_width=14, transform="translate(2 4)")
    ic.path(band, fill="none", stroke=ic.lin([(0, "#55595F"), (1, "#16171A")]), stroke_width=12)
    ic.path("M60 112a68 66 0 0 1 64 -66", fill="none", stroke="#fff", stroke_opacity=0.25, stroke_width=2,
            stroke_linecap="round")
    ic.path("M68 112a60 58 0 0 1 120 0", fill="none", stroke="#2A2C30", stroke_width=6)
    for x in (52, 196):
        ic.rect(x, 108, 8, 46, rx=3, fill=steel(ic))
    # the cups: Audacity's blue, pads facing in
    cup = ic.lin([(0, "#6BA4FF"), (0.5, "#2F6FD6"), (1, "#163E8A")], 0, 0, 1, 1)
    for x, pad in ((24, 66), (180, 172)):
        ic.rect(x + 2, 140, 52, 74, rx=22, fill="#000", opacity=0.3)
        ic.rect(pad - 6, 136, 24, 70, rx=11, fill="#1A1B1E")
        ic.rect(x, 134, 52, 74, rx=22, fill=cup)
        ic.rect(x + 0.75, 134.75, 50.5, 72.5, rx=21.25, fill="none", stroke="#fff", stroke_opacity=0.3,
                stroke_width=1.5)
        ic.rect(x + 9, 146, 34, 50, rx=15, fill="none", stroke="#0E2C66", stroke_opacity=0.4, stroke_width=2)
        ic.ellipse(x + 16, 150, 6, 10, fill="#fff", opacity=0.25, transform=f"rotate(18 {x + 16} 150)")
    ic.text("L", 50, 176, 12, font="sans-bold", anchor="middle", fill="#E8F0FF", opacity=0.8)
    ic.text("R", 206, 176, 12, font="sans-bold", anchor="middle", fill="#E8F0FF", opacity=0.8)


@small("audacity")
def audacity16(ic):
    tile(ic, "#304C7E", "#15233F")
    ic.path("M3.5 9V7a4.5 4.5 0 0 1 9 0v2", fill="none", stroke="#2A2C30", stroke_width=1.3)
    ic.path("M5.2 9.5h1l.6-2 .8 4 .8-5 .8 4.5.6-1.5h1", fill="none", stroke="#F2542D", stroke_width=0.9,
            stroke_linejoin="round", stroke_linecap="round")
    ic.rect(1.5, 8, 3, 5.5, rx=1.3, fill="#3A7CE8")
    ic.rect(11.5, 8, 3, 5.5, rx=1.3, fill="#3A7CE8")


# --- Kdenlive: an editing bench, a viewer, a strip of film through its gate ----

def _film(ic, x, y, w, h, frames=True, base="#2E1C10", frame="#B8742E"):
    """A strip of film lying flat, its sprocket holes along both edges."""
    ic.rect(x, y, w, h, fill=base)
    if frames:
        fw = h * 0.95
        k = x + 5
        while k + fw < x + w:
            ic.rect(k, y + h * 0.22, fw, h * 0.56, rx=1.5, fill=ic.lin([(0, "#E8B260"), (1, frame)]), opacity=0.85)
            k += fw + 5
    for k in range(int(x) + 3, int(x + w) - 3, 7):
        ic.rect(k, y + h * 0.06, 3.6, h * 0.1, rx=0.8, fill="#F1E6D2", opacity=0.85)
        ic.rect(k, y + h * 0.84, 3.6, h * 0.1, rx=0.8, fill="#F1E6D2", opacity=0.85)


@icon("kdenlive", kind="app", names=["kdenlive", "org.kde.kdenlive"], title="Kdenlive")
def kdenlive(ic):
    tile(ic, "#34404C", "#121820")
    shadow(ic, 128, 214, 108, 11)
    # the bench: a wooden board on the desk
    ic.rect(14, 176, 228, 30, rx=6, fill="#000", opacity=0.3, transform="translate(2 3)")
    ic.rect(14, 176, 228, 30, rx=6, fill=wood(ic, "#B07A48", "#6A3E1C"))
    ic.line(18, 177.5, 238, 177.5, stroke="#F0C894", stroke_width=1.5, opacity=0.6)
    for y, x1, x2 in ((186, 30, 120), (194, 140, 226), (199, 40, 90)):
        ic.line(x1, y, x2, y, stroke="#5A3416", stroke_opacity=0.35)
    # the viewer: a blue body, a lamp house on top, a lit screen with a frame of the film on it
    ic.rect(100, 22, 56, 20, rx=6, fill=ic.lin([(0, "#4F535A"), (1, "#1E2024")]))
    for x in range(108, 150, 6):
        ic.rect(x, 27, 3, 10, rx=1.5, fill="#0E1012")
    ic.line(103, 23, 153, 23, stroke="#fff", stroke_opacity=0.3)
    body = "M64 44a8 8 0 0 1 8-8h112a8 8 0 0 1 8 8v98H64z"
    ic.path(body, fill="#000", opacity=0.3, transform="translate(3 4)")
    ic.path(body, fill=ic.lin([(0, "#6CC6F5"), (0.4, "#2A8AD0"), (1, "#14508A")], 0, 0, 1, 1))
    ic.path("M65 140V44a7 7 0 0 1 7-7h112", fill="none", stroke="#fff", stroke_opacity=0.45, stroke_width=1.5)
    # the focus knob on its side
    ic.rect(190, 84, 12, 22, rx=3, fill=steel(ic))
    for y in range(87, 104, 3):
        ic.line(191, y, 201, y, stroke="#3A4048", stroke_opacity=0.5)
    # the hood over the screen
    ic.path("M70 46h116l-7 10H77z", fill="#0E3A66")
    ic.rect(76, 54, 104, 70, rx=3, fill="#0B1E33")
    scr = ic.clip('<rect x="80" y="58" width="96" height="62" rx="2"/>')
    with ic.g(clip_path=scr):
        ic.rect(80, 58, 96, 62, fill=ic.lin([(0, "#FFE7B0"), (0.6, "#F2A65A"), (1, "#B85A30")]))
        ic.circle(144, 82, 10, fill="#FFF6DA")
        ic.path("M80 104L100 86L114 96L132 78L176 112V120H80z", fill="#4A2A3A")
        ic.path("M80 112Q104 104 126 110T176 108V120H80z", fill="#2A1626")
        ic.rect(80, 58, 96, 62, fill=glare(ic, 1.2))
    ic.text("kdenlive", 128, 136, 10, font="sans-semibold", anchor="middle", spacing=0.5, fill="#F4FAFF")
    # the strip of film, across the bench and through the gate
    ic.rect(10, 150, 236, 26, fill="#000", opacity=0.25, transform="translate(0 3)")
    _film(ic, 10, 150, 236, 26)
    ic.rect(10, 150, 236, 1.2, fill="#fff", opacity=0.2)
    # a wax-pencil cross on the frame to cut
    ic.path("M196 157l14 12M210 157l-14 12", stroke="#F4F4F0", stroke_width=2, stroke_linecap="round", opacity=0.9)
    # the gate: a steel block the film runs under, the viewer's foot on it
    ic.rect(80, 140, 96, 10, rx=2, fill=steel(ic))
    ic.rect(88, 146, 80, 34, rx=3, fill="#000", opacity=0.3, transform="translate(2 3)")
    ic.rect(88, 146, 80, 34, rx=3, fill=ic.lin([(0, "#E4E8EC"), (0.5, "#A9B0B8"), (1, "#5D636B")]))
    ic.line(90, 147, 166, 147, stroke="#fff", stroke_width=1.2)
    ic.rect(96, 156, 64, 14, rx=2, fill="#1A1E23")
    ic.rect(98, 158, 60, 10, fill="#3A2412")
    ic.rect(110, 159, 16, 8, rx=1, fill="#FFE7B0", opacity=0.9)
    ic.rect(130, 159, 16, 8, rx=1, fill="#E8B260", opacity=0.6)
    for x in (94, 162):
        ic.circle(x, 174, 2, fill=steel(ic, False))
    # a wax pencil for marking cuts, on the bench
    with ic.g(transform="rotate(-8 52 194)"):
        ic.rect(22, 190, 64, 7, rx=1.5, fill="#000", opacity=0.3, transform="translate(1 2)")
        ic.rect(30, 190, 56, 7, rx=1.5, fill=ic.lin([(0, "#FFFFFF"), (1, "#BFC3C8")]))
        ic.path("M30 190l-8 3.5 8 3.5z", fill="#E8E8E4")
        ic.path("M22 193.5l3-1.3v2.6z", fill="#F4F4F0")
        for x in (44, 60, 76):
            ic.line(x, 190, x - 3, 197, stroke="#9AA1A9", stroke_width=0.8)


@small("kdenlive")
def kdenlive16(ic):
    tile(ic, "#34404C", "#121820")
    ic.rect(1, 12, 14, 2.4, rx=0.6, fill="#9A6A3C")
    ic.rect(4.5, 2.4, 7, 7.2, rx=0.8, fill="#2A8AD0")
    ic.rect(5.5, 3.4, 5, 3.8, rx=0.3, fill="#F2B060")
    ic.rect(0.8, 9.4, 14.4, 2.8, fill="#3A2412")
    for x in (1.6, 4.6, 7.6, 10.6, 13.6):
        ic.rect(x, 10.2, 1.8, 1.2, fill="#E8B260")


# --- Shotcut: a film reel, its strip cut ----------------------------------

@icon("shotcut", kind="app", names=["org.shotcut.Shotcut", "shotcut"], title="Shotcut")
def shotcut(ic):
    tile(ic, "#21557E", "#0D2742")
    shadow(ic, 130, 214, 100, 12)
    cx, cy = 106, 112
    # the strip running off the reel, its end cut on the slant
    sy = cy + 64
    strip = f"M{cx} {sy}H230l-10 26H{cx}z"
    ic.path(strip, fill="#000", opacity=0.3, transform="translate(2 4)")
    clip = ic.clip(f'<path d="{strip}"/>')
    with ic.g(clip_path=clip):
        _film(ic, cx, sy, 126, 26, frame="#3A9BC8")
        ic.rect(cx, sy, 126, 8, fill="#fff", opacity=0.1)
    ic.path(f"M230 {sy}l-10 26", stroke="#F1E6D2", stroke_opacity=0.6)
    # the film wound on the hub, seen through the flange
    ic.circle(cx + 2, cy + 5, 86, fill="#000", opacity=0.4)
    ic.circle(cx, cy, 72, fill=ic.rad([(0, "#4A3020"), (0.6, "#2A1A10"), (1, "#3E2A1C")], r=0.5))
    for r in range(34, 72, 4):
        ic.circle(cx, cy, r, fill="none", stroke="#E8B260", stroke_opacity=0.08)
    ic.circle(cx, cy, 71, fill="none", stroke="#E8B260", stroke_opacity=0.2)
    # the front flange: anodised blue, three windows
    face = ic.lin([(0, "#8FE0FA"), (0.45, "#34A8DA"), (1, "#145E8E")], 0, 0, 1, 1)
    holes = "".join(_sector(cx, cy, 32, 70, a + 12, a + 108) for a in (0, 120, 240))
    ic.path(_ring(cx, cy, 84) + holes, fill=face, fill_rule="evenodd")
    with ic.g(fill="none", stroke="#0A3A5C", stroke_opacity=0.45, stroke_width=1.5):
        ic.path(holes)
        ic.circle(cx, cy, 84)
    # light on the windows' lower edges, the flange's thickness
    ic.path(holes, fill="none", stroke="#C8F2FF", stroke_opacity=0.45, stroke_width=1, transform="translate(0.8 1)")
    ic.circle(cx - 0.7, cy - 0.7, 83, fill="none", stroke="#fff", stroke_opacity=0.5, stroke_width=1.2,
              stroke_dasharray="130 600", transform=f"rotate(190 {cx} {cy})")
    ic.circle(cx, cy, 78, fill="none", stroke="#0A3A5C", stroke_opacity=0.25, stroke_width=1)
    for a in (60, 180, 300):
        x, y = polar(cx, cy, 75, a)
        ic.circle(x, y, 2.4, fill=steel(ic, False))
    # the hub, its square drive hole
    ic.circle(cx, cy, 24, fill=ic.lin([(0, "#E4E8EC"), (1, "#6F767E")], 0, 0, 1, 1))
    ic.circle(cx, cy, 24, fill="none", stroke="#000", stroke_opacity=0.3)
    ic.rect(cx - 7, cy - 7, 14, 14, rx=2, fill="#0B1A26", transform=f"rotate(12 {cx} {cy})")
    ic.text("SHOTCUT", cx, cy + 20, 5.5, font="mono-semibold", anchor="middle", spacing=0.5, fill="#2A2C30")
    # scissors, open, laid over the reel's edge
    blade = ic.lin([(0, "#F7F8FA"), (0.5, "#C3C8CE"), (1, "#6F767E")], 0, 0, 1, 0)
    with ic.g(transform="translate(206 112) rotate(14)"):
        with ic.g(transform="translate(3 5)", opacity=0.35, fill="#000"):
            ic.path("M-4 0Q-6 -30 0 -66Q6 -30 4 0z", transform="rotate(-11)")
            ic.path("M-4 0Q-6 -30 0 -66Q6 -30 4 0z", transform="rotate(11)")
            for s in (-1, 1):
                ic.ellipse(s * 12, 26, 10, 14, fill="none", stroke="#000", stroke_width=7, transform=f"rotate({s * -14} {s * 12} 26)")
        for s in (1, -1):
            with ic.g(transform=f"rotate({s * 11})"):
                ic.path("M-4 2Q-6 -30 0 -66Q6 -30 4 2z", fill=blade)
                ic.path("M0 -64Q4 -30 3.4 0", fill="none", stroke="#fff", stroke_opacity=0.7, stroke_width=0.8)
        ic.circle(0, 0, 4, fill=steel(ic, False))
        ic.circle(0, 0, 1.4, fill="#3A3E44")
        for s in (-1, 1):
            ic.path(f"M{s * 2} 3 L{s * 8} 13", stroke="#17191D", stroke_width=6, stroke_linecap="round")
            ic.ellipse(s * 12, 26, 10, 14, fill="none", stroke="#17191D", stroke_width=7,
                       transform=f"rotate({s * -14} {s * 12} 26)")
            ic.ellipse(s * 12, 26, 10, 14, fill="none", stroke="#8A929B", stroke_opacity=0.7, stroke_width=1.2,
                       stroke_dasharray="16 80", transform=f"rotate({s * -14 + 180} {s * 12} 26)")


@small("shotcut")
def shotcut16(ic):
    tile(ic, "#21557E", "#0D2742")
    ic.path("M7.5 11.5H15l-.8 2.2H7.5z", fill="#3A2414")
    ic.circle(7.5, 7.5, 6, fill="#3BB0E0")
    ic.circle(7.5, 7.5, 4.4, fill="#2A1A10")
    for a in (0, 120, 240):
        ic.line(*polar(7.5, 7.5, 1, a), *polar(7.5, 7.5, 4.6, a), stroke="#3BB0E0", stroke_width=2)
    ic.circle(7.5, 7.5, 1.6, fill="#D4D8DD")


# --- HandBrake: a pineapple and a tall drink -------------------------------

@icon("handbrake", kind="app", names=["handbrake"], title="HandBrake")
def handbrake(ic):
    tile(ic, "#2A7A78", "#0E3A3C")
    shadow(ic, 128, 214, 100, 12)
    # the pineapple's crown, behind its body
    px, py = 96, 146
    back = ic.lin([(0, "#5FA83A"), (1, "#1E5A1E")], 0, 0, 1, 1)
    leaf = ic.lin([(0, "#A6E070"), (0.5, "#5DB03A"), (1, "#2E7A2A")], 0, 0, 1, 1)
    for ang, ln, w, f in ((-50, 44, 11, back), (50, 42, 11, back), (-30, 58, 12, back), (30, 56, 12, back),
                          (-40, 40, 10, leaf), (40, 38, 10, leaf), (-18, 66, 12, leaf), (18, 62, 12, leaf),
                          (-5, 80, 12, leaf), (7, 72, 11, back)):
        base = f"M{px - w} {py - 44}Q{px - w * 0.5} {py - 44 - ln * 0.55} {px + w * 0.15} {py - 44 - ln}"
        ic.path(base + f"Q{px + w * 0.6} {py - 44 - ln * 0.55} {px + w} {py - 44}z",
                fill=f, stroke="#1E5A1E", stroke_opacity=0.45, transform=f"rotate({ang} {px} {py - 44})")
        ic.path(f"M{px} {py - 46}L{px + w * 0.1} {py - 44 - ln * 0.9}", stroke="#D8F5B0", stroke_opacity=0.35,
                stroke_width=1, transform=f"rotate({ang} {px} {py - 44})")
    # its body: gold, the diamond rind
    ic.ellipse(px + 2, py + 4, 46, 58, fill="#000", opacity=0.3)
    ic.ellipse(px, py, 46, 58, fill=ic.rad([(0, "#FFD86A"), (0.55, "#E9A52A"), (1, "#9A5A10")],
                                          cx=0.38, cy=0.32, r=0.75))
    clip = ic.clip(f'<ellipse cx="{px}" cy="{py}" rx="46" ry="58"/>')
    with ic.g(clip_path=clip):
        with ic.g(stroke="#8A4E0C", stroke_opacity=0.55, stroke_width=1.6, fill="none"):
            for k in range(-6, 7):
                ic.line(px - 60 + k * 16, py - 70, px + 60 + k * 16, py + 70)
                ic.line(px + 60 + k * 16, py - 70, px - 60 + k * 16, py + 70)
        for i in range(-5, 6):
            for j in range(-6, 7):
                x = px + (i - j) * 8 * 1.07
                y = py + (i + j) * 8 * 1.07 * 0.82
                ic.circle(x, y, 1.6, fill="#6A3A06", opacity=0.5)
        ic.ellipse(px - 18, py - 24, 14, 22, fill="#fff", opacity=0.18, transform=f"rotate(20 {px - 18} {py - 24})")
        ic.ellipse(px + 30, py + 30, 30, 40, fill="#5A2E00", opacity=0.25)
    # the drink: a tall glass, red to orange, a straw and a slice
    gx, gt, gb = 166, 92, 208
    glass = f"M{gx - 30} {gt}h60l-6 {gb - gt - 6}a6 6 0 0 1-6 6h-36a6 6 0 0 1-6-6z"
    ic.path(glass, fill="#000", opacity=0.3, transform="translate(3 3)")
    drink = f"M{gx - 28} {gt + 18}h56l-5.2 {gb - gt - 24}a5 5 0 0 1-5 5h-35.6a5 5 0 0 1-5-5z"
    ic.path(drink, fill=ic.lin([(0, "#FFB23A"), (0.5, "#F2542D"), (1, "#B8182A")]))
    ic.ellipse(gx, gt + 18, 28, 4, fill="#FFC85A")
    for x, y in ((gx - 10, gt + 30), (gx + 8, gt + 36)):
        ic.rect(x - 7, y - 7, 14, 14, rx=3, fill="#fff", opacity=0.35, transform=f"rotate(15 {x} {y})")
    # the straw, striped
    ic.path(f"M{gx + 8} {gb - 20}L{gx + 26} {gt - 34}l12 -4", fill="none", stroke="#fff", stroke_width=5,
            stroke_linecap="round", stroke_linejoin="round")
    ic.path(f"M{gx + 8} {gb - 20}L{gx + 26} {gt - 34}l12 -4", fill="none", stroke="#E0283A", stroke_width=5,
            stroke_dasharray="5 5", stroke_linejoin="round")
    ic.path(glass, fill=ic.lin([(0, "#fff", 0.3), (0.3, "#fff", 0.08), (1, "#fff", 0.15)], 0, 0, 1, 0),
            stroke="#fff", stroke_opacity=0.6, stroke_width=1.5)
    ic.line(gx - 24, gt + 10, gx - 20, gb - 14, stroke="#fff", stroke_opacity=0.6, stroke_width=3,
            stroke_linecap="round")
    ic.ellipse(gx, gt, 30, 4, fill="none", stroke="#fff", stroke_opacity=0.7, stroke_width=1.5)
    # the slice of lime on the rim
    lx, ly = gx - 28, gt + 2
    ic.path(f"M{lx - 18} {ly}a18 18 0 0 0 36 0z", fill="#4E9A2A", transform=f"rotate(-20 {lx} {ly})")
    ic.path(f"M{lx - 15} {ly}a15 15 0 0 0 30 0z", fill="#D8F08A", transform=f"rotate(-20 {lx} {ly})")
    for a in (-60, -20, 20, 60):
        x, y = polar(lx, ly, 13, 180 + a - 20)
        ic.line(lx, ly, x, y, stroke="#9AC850", stroke_width=1, transform=None)


@small("handbrake")
def handbrake16(ic):
    tile(ic, "#2A7A78", "#0E3A3C")
    ic.path("M6 5L4 1.5 6.2 3.5 6.5 1 7.2 3.6 9 1.5 7.6 5z", fill="#5FB83A")
    ic.ellipse(6.4, 9.6, 3.6, 4.8, fill="#F0B030")
    ic.path("M4 8l4.5 4M4.5 11.5l4-4.5", stroke="#8A4E0C", stroke_width=0.6)
    ic.path("M10 6.5h4.5l-.6 7.5h-3.3z", fill="#F2542D")
    ic.path("M13 9L14.5 2.5", stroke="#fff", stroke_width=0.8, stroke_linecap="round")


# --- OBS Studio: a studio camera, its tally lit, the mark on its side -------

def _obs_mark(ic, cx, cy, r, ground="#302E31", ink="#F4F4F2"):
    """OBS's mark redrawn: a ring, three blobs turning in it."""
    ic.circle(cx, cy, r, fill=ground)
    ic.circle(cx, cy, r * 0.86, fill="none", stroke=ink, stroke_width=_f(r * 0.1))
    for k in range(3):
        a = 30 + k * 120
        bx, by = polar(cx, cy, r * 0.38, a)
        tx, ty = polar(cx, cy, r * 0.62, a + 70)
        ic.circle(bx, by, r * 0.27, fill=ink)
        ic.path(f"M{_f(polar(bx, by, r * 0.27, a + 90)[0])} {_f(polar(bx, by, r * 0.27, a + 90)[1])}"
                f"Q{_f(tx)} {_f(ty)} {_f(polar(cx, cy, r * 0.72, a + 105)[0])} {_f(polar(cx, cy, r * 0.72, a + 105)[1])}"
                f"Q{_f(polar(cx, cy, r * 0.5, a + 80)[0])} {_f(polar(cx, cy, r * 0.5, a + 80)[1])}"
                f" {_f(polar(bx, by, r * 0.27, a - 20)[0])} {_f(polar(bx, by, r * 0.27, a - 20)[1])}z", fill=ink)
        ic.circle(bx, by, r * 0.12, fill=ground)


@icon("com.obsproject.Studio", kind="app", names=["com.obsproject.Studio", "obs", "obs-studio"],
      title="OBS Studio")
def obs(ic):
    tile(ic, "#3E4553", "#171A21")
    shadow(ic, 140, 216, 88, 11)
    with ic.g(transform="translate(6 -2)"):
        # the tripod head and column
        for x2 in (104, 168):
            ic.line(136, 194, x2, 214, stroke="#16171A", stroke_width=6, stroke_linecap="round")
            ic.line(136, 192, x2, 212, stroke="#fff", stroke_opacity=0.15, stroke_width=1.2)
        ic.line(136, 194, 136, 216, stroke="#16171A", stroke_width=6, stroke_linecap="round")
        ic.rect(127, 176, 18, 22, fill=steel(ic))
        ic.path("M98 170h76l-8 14h-60z", fill=ic.lin([(0, "#4F535A"), (1, "#1E2024")]))
        ic.path("M160 178l52 -18", stroke="#1E2024", stroke_width=6, stroke_linecap="round")
        ic.path("M160 178l52 -18", stroke="#fff", stroke_opacity=0.15, stroke_width=1.5, transform="translate(0 -2)")
        # the viewfinder on top
        ic.rect(126, 44, 82, 36, rx=6, fill=ic.lin([(0, "#4A4E55"), (1, "#202226")]))
        ic.rect(126.75, 44.75, 80.5, 34.5, rx=5.25, fill="none", stroke="#fff", stroke_opacity=0.14, stroke_width=1.5)
        ic.rect(134, 50, 40, 24, rx=3, fill=ic.rad([(0, "#2F5F78"), (1, "#0B151C")], cx=0.35, cy=0.35, r=0.8))
        ic.path("M134 53a3 3 0 0 1 3-3h14l-12 24h-2a3 3 0 0 1-3-3z", fill="#fff", opacity=0.2)
        ic.rect(140, 78, 30, 8, fill="#202226")
        # the tally lamp, lit
        ic.rect(184, 50, 16, 10, rx=3, fill="#1A1B1E")
        ic.circle(192, 55, 9, fill="#FF3B30", opacity=0.18)
        ic.rect(186, 52, 12, 6, rx=2, fill=ic.lin([(0, "#FF8A80"), (1, "#D0201A")]))
        # the body
        ic.rect(64, 82, 156, 92, rx=12, fill="#000", opacity=0.35, transform="translate(2 4)")
        ic.rect(64, 82, 156, 92, rx=12, fill=ic.lin([(0, "#55595F"), (0.15, "#3A3D42"), (1, "#18191C")], 0, 0, 0.3, 1))
        ic.rect(64.75, 82.75, 154.5, 90.5, rx=11.25, fill="none", stroke="#fff", stroke_opacity=0.15, stroke_width=1.5)
        for y in range(140, 166, 5):
            ic.line(76, y, 116, y, stroke="#000", stroke_opacity=0.4, stroke_width=2)
        ic.text("STUDIO", 78, 104, 7, font="mono-semibold", spacing=1.6, fill="#C9CED4", opacity=0.6)
        ic.text("REC", 78, 126, 9, font="sans-bold", spacing=1, fill="#FF5A4F")
        ic.circle(104, 122.5, 3.2, fill="#FF3B30")
        # OBS's mark: an enamel disc on its side
        mx, my = 168, 128
        ic.circle(mx + 1, my + 2.5, 34, fill="#000", opacity=0.45)
        ic.circle(mx, my, 34, fill=ic.lin([(0, "#E4E8EC"), (0.5, "#9AA1A9"), (1, "#4D535A")], 0, 0, 1, 1))
        _obs_mark(ic, mx, my, 30)
        ic.path(f"M{mx - 26} {my - 8}a27 27 0 0 1 34 -21 31 31 0 0 0 -34 21z", fill="#fff", opacity=0.3)
        # the lens out in front, to the left
        ic.rect(30, 98, 38, 60, rx=4, fill=ic.lin([(0, "#3A3D42"), (1, "#121315")]))
        for x in (38, 48, 58):
            ic.rect(x, 98, 4, 60, fill="#000", opacity=0.35)
        ic.rect(30, 98, 38, 3, fill="#fff", opacity=0.15)
        ic.rect(20, 90, 16, 76, rx=5, fill=ic.lin([(0, "#2A2C30"), (1, "#0B0C0E")]))
        ic.ellipse(20, 128, 8, 36, fill=ic.rad([(0, "#3C3060"), (0.5, "#16203A"), (1, "#05070C")], cx=0.4, cy=0.35, r=0.7))
        ic.ellipse(18, 116, 3, 10, fill="#fff", opacity=0.4)


@small("com.obsproject.Studio")
def obs16(ic):
    tile(ic, "#3E4553", "#171A21")
    ic.rect(8, 2.5, 5, 2.5, rx=0.5, fill="#4A4E55")
    ic.rect(4, 5, 10.5, 7, rx=1, fill="#3A3D42")
    ic.rect(1.5, 6, 3, 5, rx=0.6, fill="#16171A")
    ic.circle(10.5, 8.5, 2.8, fill="#F4F4F2")
    ic.circle(10.5, 8.5, 2, fill="#302E31")
    for k in range(3):
        x, y = polar(10.5, 8.5, 0.9, 30 + k * 120)
        ic.circle(x, y, 0.65, fill="#F4F4F2")
    ic.rect(7.8, 12, 1.4, 2.5, fill="#9AA1A9")
    ic.circle(13, 3.7, 0.7, fill="#FF3B30")


# --- Sunshine: a sun-yellow streaming box ---------------------------------

def _sun(ic, cx, cy, r, rays=12, **kw):
    ic.circle(cx, cy, r * 0.52, **kw)
    for k in range(rays):
        a = k * 360 / rays
        p = [polar(cx, cy, r * 0.66, a - 9), polar(cx, cy, r, a), polar(cx, cy, r * 0.66, a + 9)]
        ic.poly(p, **kw)


@icon("sunshine", kind="app", names=["dev.lizardbyte.app.Sunshine", "sunshine"], title="Sunshine")
def sunshine(ic):
    tile(ic, "#2E5B9C", "#13284B")
    shadow(ic, 128, 212, 108, 13)
    with ic.g(transform="translate(-12.8 -14) scale(1.1)"):
        # the cable out of its back
        ic.path("M196 150C218 150 220 176 212 200", fill="none", stroke="#1A1B1E", stroke_width=7, stroke_linecap="round")
        ic.path("M196 150C218 150 220 176 212 200", fill="none", stroke="#fff", stroke_opacity=0.18, stroke_width=1.5,
                transform="translate(-1.5 -1)")
        # the box: top, then front, lit from the top left
        ic.path("M54 76h164l-18 26H36z", fill=ic.lin([(0, "#FFF0B0"), (1, "#FFD860")], 0, 0, 1, 1))
        ic.path("M36 102h164l18 -26v84a10 10 0 0 1-4 8l-14 14z", fill="#B86E08")
        ic.path("M36 102h164v80H46a10 10 0 0 1-10-10z", fill=ic.lin([(0, "#FFD23F"), (0.6, "#F5A815"), (1, "#D9860A")]))
        ic.line(37, 102.5, 199, 102.5, stroke="#FFF6CC", stroke_width=1.8)
        ic.line(199.5, 103, 217, 77, stroke="#FFE7A0", stroke_opacity=0.6, stroke_width=1.2)
        # the power button on top
        ic.ellipse(186, 89, 9, 4.5, fill="#B86E08", opacity=0.6)
        ic.ellipse(186, 88, 7.5, 3.6, fill=ic.lin([(0, "#FFF6CC"), (1, "#E8A020")]))
        ic.path("M183.5 87.2a3.4 1.6 0 1 0 5 0M186 85.6v1.8", fill="none", stroke="#9A5A06", stroke_width=0.8,
                stroke_linecap="round")
        # the sun pressed into its face
        sx, sy = 82, 142
        ic.circle(sx, sy, 32, fill="#C97A06", opacity=0.35)
        _sun(ic, sx + 0.8, sy + 0.8, 26, fill="#FFF3B8", opacity=0.6)
        _sun(ic, sx, sy, 26, fill=ic.rad([(0, "#E8890A"), (1, "#B85E00")]))
        ic.circle(sx, sy, 10, fill=ic.rad([(0, "#FFEB8A"), (1, "#F5B020")], cx=0.4, cy=0.35, r=0.7))
        ic.text("SUNSHINE", 124, 128, 12, font="sans-bold", spacing=1.2, fill="#6A3A00", opacity=0.85)
        ic.text("game stream host", 124, 141, 7.5, font="mono", fill="#7A4A08", opacity=0.75)
        # vents and the status light
        for x in range(126, 186, 6):
            ic.rect(x, 152, 3, 18, rx=1.5, fill="#7A4200", opacity=0.45)
            ic.rect(x + 0.6, 152, 1.2, 18, rx=0.6, fill="#FFF0B0", opacity=0.2, transform="translate(-0.8 0.8)")
        ic.circle(190, 160, 8, fill="#7CF7A6", opacity=0.2)
        ic.circle(190, 160, 3.2, fill="#5CE08A")
        ic.circle(189.2, 159.2, 1.2, fill="#fff", opacity=0.8)
        # its feet
        for x in (52, 180):
            ic.rect(x, 182, 14, 5, rx=2, fill="#3A2400")


@small("sunshine")
def sunshine16(ic):
    tile(ic, "#2E5B9C", "#13284B")
    ic.path("M3.5 4.5h10.5l-1.8 2.2H1.8z", fill="#FFE68A")
    ic.path("M12.2 6.7l1.8-2.2v6.8l-1.8 2z", fill="#B86E08")
    ic.rect(1.8, 6.7, 10.4, 6.6, rx=0.6, fill="#F5B020")
    _sun(ic, 5.2, 10, 2.8, rays=8, fill="#B85E00")
    ic.circle(10.6, 11.5, 0.7, fill="#7CF7A6")


# --- Moonlight: a gamepad, a crescent moon rising behind it ----------------

@icon("moonlight", kind="app", names=["appimagekit-moonlight", "com.moonlight_stream.Moonlight", "moonlight"],
      title="Moonlight")
def moonlight(ic):
    tile(ic, "#303566", "#10122A")
    for x, y, r in ((44, 52, 1.6), (74, 34, 1.1), (210, 46, 1.4), (226, 92, 1), (36, 98, 1)):
        ic.circle(x, y, r, fill="#fff", opacity=0.55)
    shadow(ic, 128, 214, 102, 12)
    # the moon
    moon = _crescent(150, 82, 56, 178, 64, 48)
    ic.circle(150, 82, 66, fill="#E8E4FF", opacity=0.06)
    ic.path(moon, fill=ic.lin([(0, "#FFFBEA"), (0.6, "#E2DCC6"), (1, "#A8A290")], 0, 0, 1, 1))
    ic.path(moon, fill="none", stroke="#fff", stroke_opacity=0.4)
    for x, y, r in ((106, 70, 5), (112, 100, 3.5), (126, 120, 4), (100, 88, 2.5)):
        ic.circle(x, y, r, fill="#9C967F", opacity=0.35)
        ic.circle(x - 0.6, y - 0.6, r, fill="none", stroke="#fff", stroke_opacity=0.25, stroke_width=0.8)
    # the pad
    pad = ("M74 116H182C210 116 224 138 230 166C236 196 220 212 204 208C190 204 182 186 170 180H86"
           "C74 186 66 204 52 208C36 212 20 196 26 166C32 138 46 116 74 116Z")
    ic.path(pad, fill="#000", opacity=0.35, transform="translate(2 4)")
    ic.path(pad, fill=ic.lin([(0, "#5A5F6A"), (0.25, "#3A3E47"), (1, "#16171C")], 0, 0, 0.3, 1))
    ic.path(pad, fill="none", stroke="#fff", stroke_opacity=0.16, stroke_width=1.5)
    ic.path("M76 118.5H180", stroke="#fff", stroke_opacity=0.3, stroke_width=1.5)
    # the cross
    dx, dy = 66, 146
    for t in (f"M{dx - 5} {dy - 17}h10v12h12v10h-12v12h-10v-12h-12v-10h12z",):
        ic.path(t, fill="#000", opacity=0.5, transform="translate(0.8 1.5)")
        ic.path(t, fill=ic.lin([(0, "#3A3D42"), (1, "#0F1012")]))
        ic.path(t, fill="none", stroke="#fff", stroke_opacity=0.15)
    # the four buttons
    bx, by = 190, 146
    for (ox, oy), c in (((0, -13), "#7AD7A0"), ((13, 0), "#F08080"), ((0, 13), "#8AB4F8"), ((-13, 0), "#F2D27A")):
        ic.circle(bx + ox, by + oy + 1.5, 6.5, fill="#000", opacity=0.5)
        ic.circle(bx + ox, by + oy, 6.5, fill=ic.lin([(0, "#3A3D42"), (1, "#16171A")]))
        ic.circle(bx + ox, by + oy, 2.6, fill=c, opacity=0.9)
    # the sticks
    for x in (104, 152):
        ic.circle(x, 172, 13, fill="#0B0C0E")
        ic.circle(x, 170, 10.5, fill=ic.rad([(0, "#5A5F6A"), (1, "#1E2024")], cx=0.38, cy=0.32, r=0.7))
        ic.circle(x, 170, 7, fill="none", stroke="#000", stroke_opacity=0.35)
    # the home button: a little crescent
    ic.circle(128, 140, 9, fill="#0F1012")
    ic.path(_crescent(128, 140, 6.5, 131.5, 137.5, 5.5), fill="#E8E2C8")


@small("moonlight")
def moonlight16(ic):
    tile(ic, "#303566", "#10122A")
    ic.path(_crescent(9.5, 5.5, 4.2, 11.6, 4.2, 3.6), fill="#F2EDD8")
    ic.path("M4.5 7.5h7c1.8 0 2.8 1.6 3.1 3.6.3 2-1 2.8-2 2.4-.9-.3-1.4-1.4-2.2-1.8H5.6c-.8.4-1.3 1.5-2.2 1.8-1 .4-2.3-.4-2-2.4.3-2 1.3-3.6 3.1-3.6z",
            fill="#4A4F5A")
    ic.path("M3.6 9.8h2.4M4.8 8.6v2.4", stroke="#16171C", stroke_width=0.8)
    ic.circle(11.2, 9.2, 0.6, fill="#F08080")
    ic.circle(12.3, 10.2, 0.6, fill="#8AB4F8")
