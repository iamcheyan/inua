"""inua's apps, first batch: Calendar, Weather, Viewer, Video, Screenshot,
Settings, Launcher, Assistant (docs/feat/object-icons.md, Part 1)."""

from lib import (brass, glare, graphite, icon, mark, paper, polar, shadow, small, steel, tile, wood)


def _gear(cx, cy, ro, ri, n, phase=0.0):
    """A spur gear's outline: n teeth from root radius ri to tip ro; a
    tooth's middle at phase + 0.3 pitch, a gap's at phase + 0.8 pitch."""
    p = 360 / n
    pts = []
    for i in range(n):
        a = phase + i * p
        pts += [polar(cx, cy, ri, a), polar(cx, cy, ro, a + p * 0.12), polar(cx, cy, ro, a + p * 0.48),
                polar(cx, cy, ri, a + p * 0.6)]
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"


def _arc_text(ic, s, cx, cy, r, deg, size, **kw):
    """A word set on a dial, upright along the radius at angle deg."""
    with ic.g(transform=f"rotate({deg} {cx} {cy})"):
        ic.text(s, cx, cy - r, size, anchor="middle", **kw)


# --- Calendar: a tear-off desk calendar on rings, today's page --------------

@icon("Calendar")
def calendar(ic):
    tile(ic, "#9A4A3A", "#592318")
    shadow(ic, 128, 216, 94, 12)
    # the board behind, standing on the desk
    ic.rect(40, 40, 176, 176, rx=10, fill=ic.lin([(0, "#3A3430"), (1, "#1E1A18")]))
    ic.rect(40.75, 40.75, 174.5, 174.5, rx=9.25, fill="none", stroke="#fff", stroke_opacity=0.1, stroke_width=1.5)
    # the pages still to come, their edges
    for i, c in ((3, "#CFC6B4"), (2, "#DDD5C4"), (1, "#E9E2D3")):
        ic.rect(48, 56 + i * 3, 160, 146, rx=4, fill=c)
    # today's page
    ic.rect(48, 56, 160, 146, rx=4, fill=paper(ic, "cream"))
    ic.rect(48, 56, 160, 40, rx=4, fill=ic.lin([(0, "#E0483A"), (1, "#B42A1F")]))
    ic.rect(48, 88, 160, 8, fill="#B42A1F")
    ic.line(48, 96.5, 208, 96.5, stroke="#7A1810", stroke_opacity=0.35)
    ic.text("OCTOBER", 128, 87, 17, font="sans-bold", anchor="middle", spacing=2.6, fill="#FFF6EC")
    ic.text("30", 128, 176, 84, font="sans-bold", anchor="middle", spacing=-3, fill="#000", opacity=0.08,
            transform="translate(1.5 2)")
    ic.text("30", 128, 176, 84, font="sans-bold", anchor="middle", spacing=-3, fill="#24211E")
    ic.text("FRIDAY", 128, 192, 10, font="mono-semibold", anchor="middle", spacing=2.4, fill="#B42A1F")
    ic.text("2026", 198, 110, 7, font="mono", anchor="end", fill="#8C887F")
    ic.text("wk 44", 58, 110, 7, font="mono", fill="#8C887F")
    # yesterday's page, torn off: its stub under the rings
    stub = "M48 56h160v10" + "".join(f"l-{4 if k % 2 else 4} {3 if k % 2 else -3}" for k in range(40)) + "z"
    ic.path(stub, fill="#F4EEE2")
    ic.path(stub, fill="none", stroke="#000", stroke_opacity=0.08)
    # the rings through the holes
    for x in (70, 94, 162, 186):
        ic.ellipse(x, 61, 4.5, 3, fill="#1A1614")
        ic.path(f"M{x - 4} 61 V44 a4 4 0 0 1 8 0 V61", fill="none", stroke="#000", stroke_opacity=0.35,
                stroke_width=5, transform="translate(1 1.5)")
        ic.path(f"M{x - 4} 61 V44 a4 4 0 0 1 8 0 V61", fill="none", stroke=steel(ic), stroke_width=3.6,
                stroke_linecap="round")
        ic.path(f"M{x - 4.6} 58 V44 a4.6 4.6 0 0 1 4.6 -4.6", fill="none", stroke="#fff", stroke_opacity=0.55,
                stroke_width=1)
    # the hanger in the middle
    ic.circle(128, 47, 4, fill="#121010")
    ic.circle(128, 47, 4, fill="none", stroke="#fff", stroke_opacity=0.15)


@small("Calendar")
def calendar16(ic):
    tile(ic, "#9A4A3A", "#592318")
    ic.rect(2.5, 3, 11, 11, rx=1, fill="#2A2522")
    ic.rect(3, 4, 10, 9.5, rx=0.6, fill="#F7F2E7")
    ic.rect(3, 4, 10, 3, rx=0.6, fill="#D23B2E")
    ic.rect(5, 9, 6, 2.6, rx=0.4, fill="#2A2522")
    ic.rect(5, 2, 1, 3, rx=0.5, fill="#C3C8CE")
    ic.rect(10, 2, 1, 3, rx=0.5, fill="#C3C8CE")


# --- Weather: an aneroid barometer in a wooden case -------------------------

@icon("Weather")
def weather(ic):
    tile(ic, "#4F8FC4", "#22547E")
    cx, cy = 128, 122
    shadow(ic, 128, 218, 86, 11)
    ic.circle(cx, cy, 100, fill=wood(ic, "#B47A48", "#5E3518"))
    ic.circle(cx, cy, 99, fill="none", stroke="#fff", stroke_opacity=0.12, stroke_width=2)
    ic.circle(cx, cy, 89, fill=brass(ic))
    ic.circle(cx, cy, 82, fill=brass(ic, 1, 1, 0, 0))
    ic.circle(cx, cy, 77, fill=ic.rad([(0, "#FFFDF7"), (1, "#E6DCC6")], cx=0.45, cy=0.4, r=0.65))
    ic.circle(cx, cy, 77, fill="none", stroke="#000", stroke_opacity=0.18, stroke_width=2)
    ink = "#2A2C30"
    # the scale, 28 to 31 inches over 240 degrees
    for k in range(61):
        deg = -120 + k * 4
        major = k % 10 == 0
        mid = k % 5 == 0
        x1, y1 = polar(cx, cy, 74, deg)
        x2, y2 = polar(cx, cy, 74 - (11 if major else 7 if mid else 4.5), deg)
        ic.line(x1, y1, x2, y2, stroke=ink, stroke_width=2 if major else 1.2 if mid else 0.8)
    ic.path(f"M{polar(cx, cy, 60, -120)[0]:.1f} {polar(cx, cy, 60, -120)[1]:.1f}A60 60 0 1 1 "
            f"{polar(cx, cy, 60, 120)[0]:.1f} {polar(cx, cy, 60, 120)[1]:.1f}", fill="none", stroke=ink,
            stroke_width=0.8, opacity=0.6)
    for n, deg in (("28", -120), ("29", -40), ("30", 40), ("31", 120)):
        x, y = polar(cx, cy, 54, deg)
        ic.text(n, x, y + 3.5, 10, font="sans-medium", anchor="middle", fill=ink)
    for w, deg in (("RAIN", -66), ("CHANGE", 0), ("FAIR", 66)):
        _arc_text(ic, w, cx, cy, 33, deg, 9.5, font="sans-semibold", spacing=1, fill=ink)
    ic.text("INUA", cx, cy + 34, 7, font="mono-semibold", anchor="middle", spacing=2.2, fill="#6A665D")
    ic.text("ANEROID", cx, cy + 43, 5, font="mono", anchor="middle", spacing=1, fill="#8C887F")
    # the set hand, brass, left where the needle was this morning
    with ic.g(transform=f"rotate(12 {cx} {cy})"):
        ic.path(f"M{cx - 1.6} {cy}L{cx} {cy - 70}L{cx + 1.6} {cy}z", fill="#B98A3C")
        ic.circle(cx, cy - 22, 4, fill="none", stroke="#B98A3C", stroke_width=1.6)
    # the needle, blued steel, toward fair
    with ic.g(transform=f"translate(2 3) rotate(30 {cx} {cy})", opacity=0.2, fill="#000"):
        ic.path(f"M{cx - 2.6} {cy + 22}L{cx} {cy - 68}L{cx + 2.6} {cy + 22}z")
    with ic.g(transform=f"rotate(30 {cx} {cy})"):
        ic.path(f"M{cx - 2.6} {cy + 24}L{cx} {cy - 68}L{cx + 2.6} {cy + 24}z", fill="#1E2A3E")
        ic.circle(cx, cy + 20, 5, fill="none", stroke="#1E2A3E", stroke_width=2.4)
    ic.circle(cx, cy, 7, fill=brass(ic))
    ic.circle(cx, cy, 2.2, fill="#3A2A10")
    # the glass
    ic.circle(cx, cy, 77, fill=glare(ic, 0.8))
    ic.path("M62 96a72 72 0 0 1 88-46 80 80 0 0 0-88 46z", fill="#fff", opacity=0.5)


@small("Weather")
def weather16(ic):
    tile(ic, "#4F8FC4", "#22547E")
    ic.circle(8, 8, 6.6, fill="#6E4020")
    ic.circle(8, 8, 5.7, fill="#D9AA5A")
    ic.circle(8, 8, 4.7, fill="#2F7FD0")
    ic.circle(6.6, 6.6, 1.9, fill="#FFD04A")
    ic.path("M6.6 11.2a1.3 1.3 0 0 1 .3-2.6 1.9 1.9 0 0 1 3.5-.5 1.4 1.4 0 0 1 .7 3.1z", fill="#fff")


# --- Viewer: a photograph, its corner curled, a loupe on it ----------------

def _photo(ic):
    """A mountain over a lake, in the photograph's frame x 50..190, y 56..160."""
    ic.rect(50, 56, 140, 104, fill=ic.lin([(0, "#7FB2D9"), (0.55, "#CFE2EA"), (1, "#F2E6CF")]))
    ic.circle(160, 76, 7, fill="#FFF5D6", opacity=0.9)
    ic.path("M50 118 L72 100 L86 108 L100 92 L112 100 L50 120z", fill="#8FA6B8")
    ic.path("M50 120 L96 82 L118 64 L134 78 L148 70 L190 106 L190 122 L50 122z",
            fill=ic.lin([(0, "#6F8296"), (1, "#3E4F63")], 0, 0, 1, 1))
    ic.path("M106 74 L118 64 L134 78 L148 70 L160 80 L150 79 L140 84 L132 80 L122 88 L116 78 L108 84z",
            fill="#F7FAFC")
    ic.path("M50 122 Q72 112 92 118 T140 116 T190 118 L190 128 L50 128z", fill="#2E4A34")
    ic.rect(50, 127, 140, 33, fill=ic.lin([(0, "#5D88A6"), (1, "#24485E")]))
    water = ic.clip('<rect x="50" y="127" width="140" height="33"/>')
    with ic.g(clip_path=water):
        with ic.g(opacity=0.35, transform="translate(0 255) scale(1 -1)"):
            ic.path("M50 128 L96 92 L118 74 L134 88 L148 80 L190 116 L190 128z", fill="#3E4F63")
    for y in (136, 144, 152):
        ic.line(60, y, 180, y, stroke="#fff", stroke_opacity=0.18, stroke_dasharray="14 9", stroke_width=1)


@icon("Viewer")
def viewer(ic):
    tile(ic, "#2E7A78", "#11403F")
    shadow(ic, 120, 210, 98, 12)
    with ic.g(transform="rotate(-5 120 120)"):
        ic.rect(42, 48, 156, 152, rx=3, fill="#000", opacity=0.3, transform="translate(3 4)")
        # the print, its bottom right corner turned up
        ic.path("M40 46h160v124l-30 30H40z", fill=paper(ic, "white"))
        ic.line(41, 47, 199, 47, stroke="#fff", stroke_width=1.5)
        _photo(ic)
        ic.rect(50, 56, 140, 104, fill="none", stroke="#000", stroke_opacity=0.12)
        ic.text("Lake Mashu · Oct 2026", 52, 184, 11, font="hand", fill="#55534E")
        # the curl: its back, a little shadow under it
        ic.path("M200 170 L170 200 L178 204 Z", fill="#000", opacity=0.18)
        ic.path("M200 170 Q184 176 170 200 Q186 180 200 170 Z", fill="#000", opacity=0.05)
        ic.path("M200 170 L170 200 Q176 181 200 170 Z",
                fill=ic.lin([(0, "#D8D2C6"), (0.6, "#F5F2EC"), (1, "#BDB6A8")], 0, 0, 1, 1))
    # the loupe, standing on the photo
    lx, ly, lr = 116, 96, 34
    shadow(ic, lx + 6, ly + 10, lr + 10, lr + 8, 0.9)
    ic.circle(lx + 2, ly + 5, lr + 5, fill="#16181B")
    ic.circle(lx, ly, lr + 5, fill=graphite(ic))
    ic.circle(lx, ly, lr + 4.2, fill="none", stroke="#fff", stroke_opacity=0.18, stroke_width=1.4)
    ic.circle(lx, ly, lr + 1, fill="#0C0D0F")
    lens = ic.clip(f'<circle cx="{lx}" cy="{ly}" r="{lr}"/>')
    with ic.g(clip_path=lens):
        with ic.g(transform=f"translate({lx} {ly}) scale(1.9) translate(-120 -80) rotate(-5 120 120)"):
            _photo(ic)
    ic.circle(lx, ly, lr, fill=ic.rad([(0, "#fff", 0), (0.85, "#fff", 0), (1, "#000", 0.25)]))
    ic.circle(lx, ly, lr, fill=glare(ic, 1.2))
    ic.path(f"M{lx - 26} {ly - 5}a26 26 0 0 1 22-21 30 30 0 0 0-22 21z", fill="#fff", opacity=0.6)


@small("Viewer")
def viewer16(ic):
    tile(ic, "#2E7A78", "#11403F")
    ic.rect(2, 2.5, 12, 11, rx=0.5, fill="#FFFFFF")
    ic.rect(3, 3.5, 10, 7, fill="#9CC3DE")
    ic.path("M3 9 L7 5 L9.5 7.5 L11 6.5 L13 8.5 V10.5 H3z", fill="#4D6075")
    ic.circle(6.5, 9, 3.2, fill="#2A2C30")
    ic.circle(6.5, 9, 2.3, fill="#7FB2D9")
    ic.path("M5.3 8.2 a1.6 1.6 0 0 1 1.4-.9", fill="none", stroke="#fff", stroke_width=0.6, stroke_linecap="round")


# --- Video: a clapperboard, chalked for scene 3, take 2 ---------------------

def _stripes(ic, x, y, w, h, tilt=0, light="#F3F1EC", dark="#1B1C1F"):
    clip = ic.clip(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2"/>')
    with ic.g(clip_path=clip):
        ic.rect(x, y, w, h, fill=dark)
        for k in range(-1, int(w / 26) + 2):
            sx = x + k * 26
            ic.poly([(sx, y + h), (sx + 13, y + h), (sx + 13 + h * 0.7, y), (sx + h * 0.7, y)], fill=light)
        ic.rect(x, y, w, h * 0.45, fill="#fff", opacity=0.12)


@icon("Video")
def video(ic):
    tile(ic, "#B43344", "#651420")
    shadow(ic, 128, 216, 98, 12)
    chalk = dict(font="hand", fill="#F1EFE8")
    label = dict(font="sans-semibold", fill="#F1EFE8", opacity=0.6)
    # the slate
    ic.rect(34, 96, 188, 112, rx=8, fill=graphite(ic))
    ic.rect(34.75, 96.75, 186.5, 110.5, rx=7.25, fill="none", stroke="#fff", stroke_opacity=0.12, stroke_width=1.5)
    _stripes(ic, 34, 80, 188, 18)
    rule = dict(stroke="#F1EFE8", stroke_opacity=0.55, stroke_width=1.4)
    ic.line(42, 140, 214, 140, **rule)
    ic.line(42, 176, 214, 176, **rule)
    ic.line(100, 140, 100, 176, **rule)
    ic.line(158, 140, 158, 176, **rule)
    ic.text("PROD.", 44, 110, 6.5, spacing=0.8, **label)
    ic.text("INUA", 128, 134, 30, anchor="middle", spacing=2, **chalk)
    for x, w, v in ((44, "ROLL", "A12"), (102, "SCENE", "3"), (160, "TAKE", "2")):
        ic.text(w, x, 149, 6.5, spacing=0.8, **label)
        ic.text(v, x + 27, 172, 24, anchor="middle", **chalk)
    ic.text("DATE", 44, 186, 6.5, spacing=0.8, **label)
    ic.text("30.10.26", 44, 201, 15, **chalk)
    ic.text("DIR.", 140, 186, 6.5, spacing=0.8, **label)
    ic.text("Lyric", 140, 201, 15, **chalk)
    # chalk dust
    ic.path("M60 120 q30 -4 64 2", stroke="#fff", stroke_opacity=0.06, stroke_width=8, fill="none",
            stroke_linecap="round")
    # the clapstick, raised on its hinge
    with ic.g(transform="rotate(-16 38 80)"):
        ic.rect(36, 66, 188, 18, rx=2, fill="#000", opacity=0.3, transform="translate(2 4)")
        _stripes(ic, 34, 62, 188, 18)
        ic.line(36, 62.8, 220, 62.8, stroke="#fff", stroke_opacity=0.5)
    # the hinge
    ic.circle(40, 80, 7, fill=steel(ic, False))
    ic.circle(40, 80, 2.5, fill="#3A3E44")


@small("Video")
def video16(ic):
    tile(ic, "#B43344", "#651420")
    ic.rect(2.5, 7, 11, 7, rx=0.8, fill="#2A2C30")
    ic.path("M2.5 6.6 L13.5 6.6 L13.5 5 L2.5 5z", fill="#F1EFE8")
    ic.path("M4.5 5 L6.5 5 L5.5 6.6 L3.5 6.6z M9 5 L11 5 L10 6.6 L8 6.6z", fill="#2A2C30")
    ic.path("M2.5 4.7 L13 1.8 L13.4 3.3 L2.9 6.2z", fill="#F1EFE8")
    ic.path("M5 3.9 L7 3.3 L7.4 4.9 L5.4 5.4z M9.4 2.7 L11.3 2.2 L11.7 3.7 L9.8 4.2z", fill="#2A2C30")
    ic.rect(4, 9.5, 8, 0.8, fill="#F1EFE8", opacity=0.6)


# --- Screenshot: a rangefinder camera --------------------------------------

@icon("Screenshot")
def screenshot(ic):
    tile(ic, "#B8607A", "#6A2440")
    shadow(ic, 128, 210, 104, 12)
    # on the top plate: rewind knob, shutter dial, release
    ic.rect(50, 66, 30, 18, rx=3, fill=steel(ic))
    for x in range(52, 80, 3):
        ic.line(x, 68, x, 82, stroke="#000", stroke_opacity=0.2)
    ic.rect(150, 60, 44, 24, rx=3, fill=steel(ic))
    for x in range(152, 194, 3):
        ic.line(x, 62, x, 70, stroke="#000", stroke_opacity=0.22)
    ic.text("125 250 500", 172, 80, 6.5, font="mono-semibold", anchor="middle", fill="#2A2C30")
    ic.rect(152, 60.6, 40, 1.2, fill="#fff", opacity=0.6)
    ic.rect(200, 72, 14, 12, rx=2, fill=steel(ic))
    ic.ellipse(207, 72, 7, 2.5, fill="#E3E6EA")
    # the body: chrome top, leather below
    ic.rect(26, 82, 204, 108, rx=14, fill="#16181B", transform="translate(2 3)", opacity=0.6)
    ic.rect(26, 82, 204, 108, rx=14, fill=ic.lin([(0, "#2E2F33"), (1, "#141517")]))
    leather_px = ic.define('<pattern id="{id}" width="4" height="4" patternUnits="userSpaceOnUse">'
                           '<circle cx="1" cy="1" r=".8" fill="#fff" opacity=".07"/>'
                           '<circle cx="3" cy="3" r=".8" fill="#000" opacity=".25"/></pattern>', "p")
    ic.rect(26, 118, 204, 72, rx=0, fill=f"url(#{leather_px})")
    ic.path("M26 96a14 14 0 0 1 14-14h176a14 14 0 0 1 14 14v22H26z",
            fill=ic.lin([(0, "#F2F4F6"), (0.35, "#C9CED4"), (0.7, "#9AA1A9"), (1, "#6F767E")]))
    ic.line(40, 83, 216, 83, stroke="#fff", stroke_width=1.5)
    ic.line(26, 118.5, 230, 118.5, stroke="#000", stroke_opacity=0.35)
    # windows: viewfinder, rangefinder, frame light
    ic.rect(36, 90, 34, 20, rx=3, fill="#2A2C30")
    ic.rect(38, 92, 30, 16, rx=2, fill=ic.rad([(0, "#5A7D93"), (1, "#121B22")], cx=0.35, cy=0.35, r=0.8))
    ic.path("M38 94a2 2 0 0 1 2-2h12l-10 16h-2a2 2 0 0 1-2-2z", fill="#fff", opacity=0.25)
    ic.rect(80, 94, 22, 13, rx=2, fill="#F3F1EC", opacity=0.9)
    for x in range(82, 101, 3):
        ic.line(x, 95, x, 106, stroke="#9AA1A9", stroke_width=0.8)
    ic.rect(186, 90, 30, 20, rx=3, fill="#2A2C30")
    ic.rect(188, 92, 26, 16, rx=2, fill=ic.rad([(0, "#5A7D93"), (1, "#121B22")], cx=0.35, cy=0.35, r=0.8))
    ic.path("M188 94a2 2 0 0 1 2-2h10l-9 16h-1a2 2 0 0 1-2-2z", fill="#fff", opacity=0.25)
    ic.text("INUA", 216, 182, 8, font="mono-semibold", anchor="end", spacing=2, fill="#C9CED4", opacity=0.7)
    # the lens
    lx, ly = 128, 146
    ic.circle(lx + 2, ly + 4, 54, fill="#000", opacity=0.35)
    ic.circle(lx, ly, 54, fill=ic.lin([(0, "#E9ECEF"), (0.5, "#9AA1A9"), (1, "#4D535A")], 0, 0, 1, 1))
    ic.circle(lx, ly, 52.5, fill="none", stroke="#1E2024", stroke_width=3, stroke_dasharray="1.6 1.6", opacity=0.55)
    ic.circle(lx, ly, 49, fill=ic.lin([(0, "#3A3D42"), (1, "#121315")], 0, 0, 1, 1))
    for n, deg in (("∞", -60), ("10", -36), ("5", -12), ("3", 12), ("2", 36), ("1.5", 60)):
        _arc_text(ic, n, lx, ly, 43, deg, 7, font="mono-semibold", fill="#F1F1EF")
    ic.circle(lx, ly, 37, fill=ic.lin([(0, "#D9DDE1"), (1, "#6F767E")], 0, 0, 1, 1))
    for n, deg in (("2", -90), ("2.8", -60), ("4", -30), ("5.6", 0), ("8", 30), ("11", 60), ("16", 90)):
        _arc_text(ic, n, lx, ly, 32, deg, 6, font="mono-semibold", fill="#2A2C30")
    ic.path(f"M{lx} {ly - 39}l-2.5 -4h5z", fill="#E0483A")
    ic.circle(lx, ly, 25, fill="#0C0D0F")
    ic.circle(lx, ly, 22, fill=ic.rad([(0, "#3C3060"), (0.5, "#16203A"), (1, "#05070C")], cx=0.4, cy=0.4, r=0.7))
    ic.circle(lx, ly, 13, fill="none", stroke="#6FA8C8", stroke_opacity=0.25, stroke_width=1.5)
    ic.circle(lx, ly, 22, fill=glare(ic, 1.3))
    ic.ellipse(lx - 8, ly - 9, 7, 4, fill="#fff", opacity=0.55, transform=f"rotate(-35 {lx - 8} {ly - 9})")
    ic.circle(lx + 9, ly + 8, 2, fill="#B88AFF", opacity=0.45)


@small("Screenshot")
def screenshot16(ic):
    tile(ic, "#B8607A", "#6A2440")
    ic.rect(10, 3, 3, 1.6, rx=0.4, fill="#C3C8CE")
    ic.rect(1.5, 4.5, 13, 8, rx=1.2, fill="#1E2024")
    ic.rect(1.5, 4.5, 13, 2.6, rx=1.2, fill="#C9CED4")
    ic.rect(2.5, 5.1, 2.2, 1.4, rx=0.3, fill="#2A3A46")
    ic.circle(8, 9, 3.6, fill="#C3C8CE")
    ic.circle(8, 9, 2.4, fill="#0C0D0F")
    ic.circle(7.3, 8.3, 0.7, fill="#fff", opacity=0.7)


# --- Settings: two machined gears in mesh ----------------------------------

def _gear_body(ic, cx, cy, ro, ri, n, phase, face, side, bore, holes=0):
    d = _gear(cx, cy, ro, ri, n, phase)
    ic.path(d, fill=side, transform="translate(2.5 4)")
    ic.path(d, fill=face)
    ic.path(d, fill="none", stroke="#fff", stroke_opacity=0.35, stroke_width=1, transform="translate(-0.5 -0.5)")
    ic.path(d, fill="none", stroke="#000", stroke_opacity=0.25, stroke_width=1)
    # the web, turned a little lower than the rim
    web = ri - 8
    ic.circle(cx, cy, web, fill="#000", opacity=0.14)
    ic.circle(cx, cy, web, fill="none", stroke="#000", stroke_opacity=0.25, stroke_width=1.5)
    ic.circle(cx + 0.8, cy + 0.8, web, fill="none", stroke="#fff", stroke_opacity=0.25, stroke_width=1,
              stroke_dasharray=f"{web * 1.6:.0f} {web * 10:.0f}", transform=f"rotate(30 {cx} {cy})")
    for k in range(holes):
        hx, hy = polar(cx, cy, (web + bore) / 2 + 2, 45 + k * 360 / holes)
        hr = (web - bore) / 2 - 5
        ic.circle(hx, hy, hr, fill=ic.lin([(0, "#2A3038"), (1, "#4E5761")]))
        ic.path(f"M{hx - hr * 0.7:.1f} {hy + hr * 0.7:.1f}A{hr} {hr} 0 0 0 {hx + hr * 0.7:.1f} {hy + hr * 0.7:.1f}",
                fill="none", stroke="#fff", stroke_opacity=0.3, stroke_width=1)
        ic.circle(hx, hy, hr, fill="none", stroke="#000", stroke_opacity=0.35, stroke_width=1.2)
    # the hub and its bore with a keyway
    hub = bore + 9
    ic.circle(cx, cy, hub, fill=face)
    ic.circle(cx, cy, hub, fill="none", stroke="#000", stroke_opacity=0.3, stroke_width=1.2)
    ic.circle(cx - 0.6, cy - 0.6, hub - 1, fill="none", stroke="#fff", stroke_opacity=0.35, stroke_width=1)
    ic.circle(cx, cy, bore, fill=ic.lin([(0, "#0B0C0E"), (1, "#3A3D42")]))
    ic.rect(cx - 2.5, cy - bore - 4, 5, 6, fill="#0B0C0E")


@icon("Settings")
def settings(ic):
    tile(ic, "#66717D", "#333B44")
    shadow(ic, 124, 214, 96, 12)
    # big gear: brass, 14 teeth; small: steel, 9 teeth; same module
    ax, ay, bx, by = 102, 142, 170, 76
    # mesh: centre line at 45 deg from big to small
    dist = ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5
    import math
    ang = math.degrees(math.atan2(bx - ax, ay - by))
    pa = 360 / 14
    pb = 360 / 9
    ra = 56 * dist / 92
    rb = 36 * dist / 92
    _gear_body(ic, ax, ay, ra + 6, ra - 6, 14, ang - 0.3 * pa, brass(ic), "#4A3410", 10, holes=4)
    # the set screw in the big hub, hex socket
    sx, sy = ax, ay + 15
    ic.circle(sx, sy, 3.6, fill="#2A2C30")
    ic.poly([polar(sx, sy, 2, a) for a in range(0, 360, 60)], fill="#0B0C0E")
    _gear_body(ic, bx, by, rb + 6, rb - 6, 9, ang + 180 - 0.8 * pb,
               ic.lin([(0, "#E8EBEE"), (0.5, "#A9AFB6"), (1, "#5D636B")], 0, 0, 1, 1), "#2C3036", 7)
    ic.circle(bx, by + 11, 2.6, fill="#2A2C30")
    ic.poly([polar(bx, by + 11, 1.4, a) for a in range(0, 360, 60)], fill="#0B0C0E")


@small("Settings")
def settings16(ic):
    tile(ic, "#66717D", "#333B44")
    ic.path(_gear(10.6, 5.4, 4, 2.9, 8, 0), fill="#C3C8CE")
    ic.circle(10.6, 5.4, 1.1, fill="#333B44")
    ic.path(_gear(6.2, 9.8, 5.2, 3.9, 10, 9), fill="#D2A458")
    ic.circle(6.2, 9.8, 1.5, fill="#333B44")


# --- Launcher: a magnifying glass over a tray of app tiles -----------------

TILES = [
    ("#557797", "#2C4660", "folder"), ("#3D79A6", "#1F4467", "env"), ("#22282D", "#0B0E10", "term"),
    ("#9A4A3A", "#592318", "cal"), ("#7A4C8E", "#3D2150", "disc"), ("#C27236", "#7A3C14", "calc"),
    ("#2E4468", "#141F35", "clock"), ("#2E7A78", "#11403F", "photo"), ("#B43344", "#651420", "clap"),
]


def _tiles(ic):
    """Nine app tiles, 40 px each, in a 3 x 3 grid from (58, 46)."""
    for i, (top, bottom, glyph) in enumerate(TILES):
        x = 58 + (i % 3) * 50
        y = 46 + (i // 3) * 50
        ic.rect(x + 1, y + 3, 40, 40, rx=10, fill="#000", opacity=0.3)
        ic.rect(x, y, 40, 40, rx=10, fill=ic.lin([(0, top), (1, bottom)]))
        ic.rect(x + 0.5, y + 0.5, 39, 39, rx=9.5, fill="none", stroke="#fff", stroke_opacity=0.18)
        cx, cy = x + 20, y + 20
        if glyph == "folder":
            ic.path(f"M{cx - 11} {cy - 7}h8l2 2h12v14h-22z", fill="#C99C50")
            ic.rect(cx - 12, cy - 2, 24, 11, rx=1.5, fill="#F3D493")
        elif glyph == "env":
            ic.rect(cx - 12, cy - 8, 24, 16, rx=1.5, fill="#F6F1E6")
            ic.path(f"M{cx - 11} {cy - 7}L{cx} {cy + 1}L{cx + 11} {cy - 7}", fill="none", stroke="#C9BFA9", stroke_width=1.5)
            ic.circle(cx, cy + 1, 2.6, fill="#B53523")
        elif glyph == "term":
            ic.path(f"M{cx - 9} {cy - 6}l6 5-6 5", fill="none", stroke="#7CF7A6", stroke_width=2.4,
                    stroke_linecap="round", stroke_linejoin="round")
            ic.rect(cx, cy + 2, 8, 3, fill="#7CF7A6")
        elif glyph == "cal":
            ic.rect(cx - 11, cy - 11, 22, 22, rx=2, fill="#F7F2E7")
            ic.rect(cx - 11, cy - 11, 22, 7, rx=2, fill="#D23B2E")
            ic.text("30", cx, cy + 9, 12, font="sans-bold", anchor="middle", fill="#24211E")
        elif glyph == "disc":
            ic.circle(cx, cy, 13, fill="#141416")
            ic.circle(cx, cy, 9, fill="none", stroke="#fff", stroke_opacity=0.1)
            ic.circle(cx, cy, 4.5, fill="#E2B04A")
        elif glyph == "calc":
            ic.rect(cx - 9, cy - 13, 18, 26, rx=3, fill="#2A2C30")
            ic.rect(cx - 6, cy - 10, 12, 6, rx=1, fill="#B9C7A5")
            for kx in (-6, -1, 4):
                for ky in (-1, 4, 9):
                    ic.rect(cx + kx, cy + ky - 1, 3, 2.4, rx=0.6, fill="#F2A24A" if kx == 4 else "#8A8F97")
        elif glyph == "clock":
            ic.circle(cx, cy, 13, fill="#C99645")
            ic.circle(cx, cy, 10.5, fill="#FBF7EC")
            ic.path(f"M{cx} {cy}L{cx - 5} {cy - 3}M{cx} {cy}L{cx + 5} {cy - 6}", stroke="#23262B", stroke_width=1.8,
                    stroke_linecap="round")
        elif glyph == "photo":
            ic.rect(cx - 12, cy - 10, 24, 20, fill="#fff")
            ic.rect(cx - 10, cy - 8, 20, 13, fill="#9CC3DE")
            ic.path(f"M{cx - 10} {cy + 5}l7-9 4 4 3-2 6 7z", fill="#4D6075")
        elif glyph == "clap":
            ic.rect(cx - 12, cy - 3, 24, 14, rx=1.5, fill="#2A2C30")
            ic.rect(cx - 12, cy - 7, 24, 4, fill="#F1EFE8")
            ic.path(f"M{cx - 12} {cy - 8}l23-6 1 4-23 6z", fill="#F1EFE8")


@icon("Launcher")
def launcher(ic):
    tile(ic, "#4B4FA6", "#22245E")
    shadow(ic, 128, 216, 98, 12)
    # the tray the tiles lie on
    ic.rect(46, 34, 164, 164, rx=22, fill="#000", opacity=0.22, transform="translate(2 4)")
    ic.rect(46, 34, 164, 164, rx=22, fill=ic.lin([(0, "#E9E6F2"), (1, "#B9B4CC")]))
    ic.rect(46.75, 34.75, 162.5, 162.5, rx=21.25, fill="none", stroke="#fff", stroke_opacity=0.7, stroke_width=1.5)
    _tiles(ic)
    # the glass: its shadow on the tray, the handle, the rim, the lens
    lx, ly, lr = 116, 104, 42
    ic.circle(lx + 8, ly + 12, lr + 9, fill="#000", opacity=0.18)
    ic.path(f"M{lx + 40} {ly + 40} L{lx + 84} {ly + 84}", stroke="#000", stroke_opacity=0.25, stroke_width=20,
            stroke_linecap="round", transform="translate(6 8)")
    ic.path(f"M{lx + 50} {ly + 50} L{lx + 84} {ly + 84}", stroke="#3A1E10", stroke_width=20, stroke_linecap="round")
    ic.path(f"M{lx + 50} {ly + 50} L{lx + 84} {ly + 84}", stroke=wood(ic, "#9A5A30", "#3E200E"), stroke_width=17,
            stroke_linecap="round")
    ic.path(f"M{lx + 50} {ly + 46} L{lx + 82} {ly + 78}", stroke="#fff", stroke_opacity=0.22, stroke_width=3,
            stroke_linecap="round")
    ic.path(f"M{lx + 34} {ly + 34} L{lx + 52} {ly + 52}", stroke=brass(ic), stroke_width=15)
    ic.path(f"M{lx + 49} {ly + 49} L{lx + 53} {ly + 53}", stroke="#5E4012", stroke_width=15)
    lens = ic.clip(f'<circle cx="{lx}" cy="{ly}" r="{lr}"/>')
    with ic.g(clip_path=lens):
        ic.rect(lx - lr, ly - lr, lr * 2, lr * 2, fill="#E2DEEC")
        with ic.g(transform=f"translate({lx} {ly}) scale(1.4) translate({-lx} {-ly})"):
            _tiles(ic)
    ic.circle(lx, ly, lr, fill=ic.rad([(0, "#fff", 0), (0.82, "#fff", 0), (1, "#3B3570", 0.35)]))
    ic.circle(lx, ly, lr, fill=glare(ic, 1.3))
    ic.path(f"M{lx - 36} {ly - 4}a36 36 0 0 1 30-32 40 40 0 0 0-30 32z", fill="#fff", opacity=0.6)
    ic.circle(lx, ly, lr + 5, fill="none", stroke="#5E4012", stroke_width=11, transform="translate(1 2)")
    ic.circle(lx, ly, lr + 5, fill="none", stroke=brass(ic), stroke_width=10)
    ic.circle(lx, ly, lr + 9.5, fill="none", stroke="#FFF1C8", stroke_opacity=0.45, stroke_width=1,
              stroke_dasharray="80 400", transform=f"rotate(-150 {lx} {ly})")
    ic.circle(lx, ly, lr + 0.5, fill="none", stroke="#3A2A10", stroke_opacity=0.6, stroke_width=1)


@small("Launcher")
def launcher16(ic):
    tile(ic, "#4B4FA6", "#22245E")
    cols = ["#557797", "#D23B2E", "#7A4C8E", "#C27236", "#2E7A78", "#3D79A6"]
    for i, c in enumerate(cols):
        ic.rect(2.5 + (i % 3) * 3.8, 2.5 + (i // 3) * 3.8, 3, 3, rx=0.7, fill=c)
    ic.path("M10 10 L13.5 13.5", stroke="#7A4A22", stroke_width=2, stroke_linecap="round")
    ic.circle(7.5, 7.5, 3.6, fill="#C9D3F0", opacity=0.6)
    ic.circle(7.5, 7.5, 3.6, fill="none", stroke="#D2A458", stroke_width=1.3)


# --- Assistant: a brass service bell, inua's mark on its dome ---------------

@icon("Assistant")
def assistant(ic):
    tile(ic, "#7650A8", "#3A2266")
    shadow(ic, 128, 214, 104, 12)
    # the base: black lacquered wood, its edge toward us
    ic.path("M28 178 v16 a100 20 0 0 0 200 0 v-16z", fill=ic.lin([(0, "#2A2420"), (1, "#0E0B09")], 0, 0, 1, 0))
    ic.path("M28 186 a100 20 0 0 0 200 0", fill="none", stroke="#fff", stroke_opacity=0.08, stroke_width=1.5)
    ic.ellipse(128, 178, 100, 20, fill=ic.lin([(0, "#4A3E36"), (1, "#1A1512")], 0, 0, 1, 1))
    ic.path("M30 176 a100 20 0 0 1 160 -16", fill="none", stroke="#fff", stroke_opacity=0.25, stroke_width=1.5)
    # the plunger
    ic.rect(124, 52, 8, 26, fill=steel(ic))
    ic.ellipse(128, 52, 17, 6, fill="#4A4E55")
    ic.path("M111 52 a17 6 0 0 0 34 0 v-5 a17 6 0 0 0 -34 0z", fill=steel(ic))
    ic.ellipse(128, 47, 17, 6, fill=ic.lin([(0, "#F2F4F6"), (1, "#9AA1A9")], 0, 0, 1, 1))
    # the dome
    dome = "M46 176 C46 116 84 76 128 76 C172 76 210 116 210 176 Z"
    ic.ellipse(128, 176, 82, 13, fill="#000", opacity=0.35)
    ic.path(dome, fill=ic.rad([(0, "#FFF2C8"), (0.25, "#E8C27A"), (0.7, "#B3812F"), (1, "#6E4C16")],
                              cx=0.32, cy=0.25, r=0.85))
    ic.path("M48 172 C60 186 196 186 208 172", fill="none", stroke="#C79BEA", stroke_opacity=0.4, stroke_width=4)
    # the lip of the dome
    ic.path("M44 174 a84 12 0 0 0 168 0 v4 a84 12 0 0 1 -168 0z", fill=brass(ic, 0, 0, 1, 0))
    ic.path("M44 174 a84 12 0 0 0 168 0", fill="none", stroke="#FFF1C8", stroke_opacity=0.6, stroke_width=1)
    # the mark, engraved
    for dx, dy, col, op in ((0.8, 0.8, "#FFF2C8", 0.55), (-0.6, -0.6, "#3E2A08", 0.6), (0, 0, "#7A5418", 0.9)):
        mark(ic, 100 + dx, 108 + dy, 56, fill=col, opacity=op)
    ic.text("INUA · DESK", 128, 171, 6, font="mono-semibold", anchor="middle", spacing=1.8, fill="#6E4C16",
            opacity=0.8)
    # the light on the dome
    ic.path("M70 132 C76 104 96 88 116 84 C98 96 84 112 78 136 Z", fill="#fff", opacity=0.55)
    ic.ellipse(160, 96, 10, 4, fill="#fff", opacity=0.25, transform="rotate(30 160 96)")


@small("Assistant")
def assistant16(ic):
    tile(ic, "#7650A8", "#3A2266")
    ic.ellipse(8, 12.6, 6.6, 1.6, fill="#1E1814")
    ic.path("M2.8 12 C2.8 7.5 5 5.2 8 5.2 C11 5.2 13.2 7.5 13.2 12 Z", fill="#D2A458")
    ic.path("M4.3 9.5 C4.7 7.8 5.7 6.6 7 6.2", fill="none", stroke="#FFF2C8", stroke_width=0.8, stroke_linecap="round")
    ic.rect(7.4, 3, 1.2, 2.4, fill="#9AA1A9")
    ic.ellipse(8, 3, 2, 0.8, fill="#C3C8CE")
