"""The talk apps, soft: the same objects as drawings/apps_talk.py with about
half the detail, no text and no glare (Telegram is in core.py)."""

from lib import bar, polar, soft, soft_shadow, tile, two

STEEL = ("#AEB4BB", "#8D949C")


# --- Thunderbird: a blue bird curled round a letter -------------------------

@soft("thunderbird")
def thunderbird(ic):
    tile(ic, "#34507E", "#16243F")
    soft_shadow(ic, 128, 214, 92, 12)
    with ic.g(transform="rotate(-4 140 140)"):
        ic.rect(76, 98, 132, 92, rx=12, fill=two(ic, "#F7F1E4", "#EAE1CE"))
        ic.path("M80 186 L130 146 a14 14 0 0 1 18 0 L204 186", fill="#EDE4D1")
        ic.path("M76 110a12 12 0 0 1 12-12h108a12 12 0 0 1 12 12 L148 152 a13 13 0 0 1-16 0z",
                fill=two(ic, "#FFFDF8", "#F3ECDD"))
    ic.path("M156 30 C146 14 126 8 104 12 C124 16 138 26 146 38 Z", fill="#3F8EF2")
    bird = ("M206 180 C184 204 150 216 116 212 C64 206 30 160 40 110 C48 64 94 36 140 36"
            " C150 26 166 22 182 26 C198 30 208 42 212 56 C206 66 196 74 180 78"
            " C150 80 98 84 80 104 C68 124 72 164 108 182 C138 196 176 196 206 180 Z")
    ic.path(bird, fill=two(ic, "#4C9FF6", "#3438B4"))
    ic.path("M58 94 C70 68 96 54 126 50 C100 62 82 80 74 106 Z", fill="#A8DBFF", opacity=0.65)
    ic.path("M211 51 L228 60 L206 67 Z", fill="#F2B84A", stroke="#F2B84A", stroke_width=2,
            stroke_linejoin="round")
    ic.circle(188, 48, 5.5, fill="#10183A")


# --- Signal: a blue walkie-talkie, its grille ringed in broken dashes --------

@soft("signal-desktop")
def signal(ic):
    tile(ic, "#3E4C68", "#18202F")
    soft_shadow(ic, 128, 216, 64, 10)
    ic.rect(84, 14, 16, 52, rx=8, fill="#2A2D33")
    ic.rect(146, 30, 22, 30, rx=6, fill="#3A3E45")
    ic.rect(56, 92, 16, 46, rx=6, fill="#1E2025")
    ic.rect(64, 56, 128, 156, rx=26, fill=two(ic, "#5A8CF6", "#2556C8"))
    ic.circle(128, 110, 40, fill="#163C94")
    ic.circle(128, 110, 30, fill="#15171B")
    for dx, dy in ((0, 0), (-12, 0), (12, 0), (-6, -11), (6, -11), (-6, 11), (6, 11)):
        ic.circle(128 + dx, 110 + dy, 3.5, fill="#3A3E46")
    ic.circle(128, 110, 36, fill="none", stroke="#F4F7FF", stroke_width=6, stroke_dasharray="16.5 6.1",
              stroke_dashoffset=3, transform="rotate(-80 128 110)")
    ic.path("M98 134 L90 149 L107 143", fill="none", stroke="#F4F7FF", stroke_width=6, stroke_linejoin="round",
            stroke_linecap="round")
    ic.rect(88, 158, 80, 26, rx=6, fill="#0F1F45")
    ic.rect(92, 162, 72, 18, rx=4, fill=two(ic, "#BFD9D2", "#9DBBB3"))
    bar(ic, 98, 167, 34, 8, fill="#20302C")
    for x in (98, 128, 158):
        ic.rect(x - 11, 191, 22, 10, rx=5, fill="#1A44A8")
    ic.circle(176, 72, 4, fill="#7CF7A6")


# --- Discord: a blurple game pad, the mark's face as its badge --------------

def _face(ic, cx, cy, k, fill, eyes):
    t = f"translate({cx} {cy}) scale({k})"
    ic.path("M-11 -6 Q-6 -9.4 -3 -9.4 L-2 -7.3 Q0 -7.7 2 -7.3 L3 -9.4 Q6 -9.4 11 -6 Q14.2 0 13.2 7.4"
            " Q10 10.2 6.2 11 L4.6 8.6 Q0 9.6 -4.6 8.6 L-6.2 11 Q-10 10.2 -13.2 7.4 Q-14.2 0 -11 -6Z",
            fill=fill, transform=t)
    ic.ellipse(-4.6, 1.4, 2.4, 2.8, fill=eyes, transform=t)
    ic.ellipse(4.6, 1.4, 2.4, 2.8, fill=eyes, transform=t)


@soft("discord")
def discord(ic):
    tile(ic, "#3B3E48", "#1A1B20")
    soft_shadow(ic, 128, 208, 100, 11)
    ic.path("M58 76 c4-6 12-9 24-9h12v7H76z M198 76 c-4-6-12-9-24-9h-12v7h18z", fill="#3B44B0")
    pad = ("M76 74h104c26 0 36 14 42 40l10 50c4 20-8 32-22 28c-10-3-15-11-21-22l-9-16H76l-9 16"
           "c-6 11-11 19-21 22c-14 4-26-8-22-28l10-50c6-26 16-40 42-40z")
    ic.path(pad, fill=two(ic, "#7480F8", "#4049C0"))
    with ic.g(transform="translate(70 116)"):
        ic.circle(0, 0, 21, fill="#454FC6")
        ic.path("M-5 -15h10v10h10v10h-10v10h-10v-10h-10v-10h10z", fill="#262A3C", stroke="#262A3C",
                stroke_width=2, stroke_linejoin="round")
    with ic.g(transform="translate(186 116)"):
        ic.circle(0, 0, 23, fill="#454FC6")
        for dx, dy in ((0, -12), (12, 0), (0, 12), (-12, 0)):
            ic.circle(dx, dy, 7, fill="#F2F3FD")
    for x in (100, 156):
        ic.circle(x, 150, 17, fill="#2E3591")
        ic.circle(x, 150, 12, fill="#262A3C")
    ic.circle(128, 108, 20, fill="#FFFFFF")
    _face(ic, 128, 108.5, 1.05, "#5865F2", "#FFFFFF")


# --- Slack: a corkboard, four notes pinned in the mark's pinwheel -------------

@soft("slack")
def slack(ic):
    tile(ic, "#5B2D5E", "#2A0F2C")
    soft_shadow(ic, 128, 214, 98, 11)
    ic.rect(26, 34, 204, 178, rx=14, fill=two(ic, "#C48E56", "#7E4E24"))
    ic.rect(38, 46, 180, 154, rx=5, fill=two(ic, "#D3A672", "#B08050"))
    x0, y0, L, S, g = 55, 52, 88, 56, 3
    notes = [
        ((x0, y0, L, S), "#36C5F0", "#0D4F6C", -2, (x0 + 14, y0 + 13)),
        ((x0 + L, y0, S, L), "#2EB67D", "#0B4A2E", 2, (x0 + L + S / 2, y0 + 13)),
        ((x0 + S, y0 + L, L, S), "#ECB22E", "#5E3F00", -1.5, (x0 + S + L - 14, y0 + L + 13)),
        ((x0, y0 + S, S, L), "#E01E5A", "#FFFFFF", 2.5, (x0 + S / 2, y0 + S + 13)),
    ]
    for (x, y, w, h), col, ink, rot, _ in notes:
        x, y, w, h = x + g, y + g, w - 2 * g, h - 2 * g
        with ic.g(transform=f"rotate({rot} {x + w / 2} {y + h / 2})"):
            ic.rect(x, y, w, h, rx=4, fill=col)
            if w > h:
                bar(ic, x + 14, y + h / 2 + 2, w - 32, 7, fill=ink, opacity=0.55)
            else:
                ic.rect(x + w / 2 - 3.5, y + 26, 7, h - 46, rx=3.5, fill=ink, opacity=0.55)
    for *_, (px, py) in notes:
        ic.circle(px, py, 6, fill="#EDEDEB")


# --- Element: a glazed periodic-table tile, "El", number 1 -------------------

@soft("element-desktop")
def element(ic):
    tile(ic, "#2B4A43", "#0F201C")
    soft_shadow(ic, 128, 214, 98, 11)
    with ic.g(transform="rotate(10 186 82)"):
        ic.rect(127, 33, 108, 108, rx=18, fill="#9C927E")
        ic.rect(124, 28, 108, 108, rx=18, fill=two(ic, "#FFFDF6", "#DCD3C0"))
        bar(ic, 138, 42, 12, 8, fill="#3A6B5E")
        bar(ic, 186, 68, 30, 14, fill="#3A6B5E", opacity=0.85)
    x, y, s = 40, 58, 148
    ic.rect(x + 3, y + 6, s, s, rx=18, fill="#05553E")
    ic.rect(x, y, s, s, rx=18, fill=two(ic, "#3ADDA8", "#0A9A6F"))
    ink = "#F4FFFA"
    bar(ic, x + 16, y + 16, 8, 16, fill=ink)
    bar(ic, x + s - 50, y + 18, 34, 8, fill=ink, opacity=0.8)
    # "El", as bold blocks
    ex, ey = x + 38, y + 44
    ic.rect(ex, ey, 14, 56, rx=3, fill=ink)
    ic.rect(ex, ey, 40, 13, rx=3, fill=ink)
    ic.rect(ex, ey + 22, 34, 12, rx=3, fill=ink)
    ic.rect(ex, ey + 43, 40, 13, rx=3, fill=ink)
    ic.rect(ex + 50, ey - 4, 14, 60, rx=3, fill=ink)
    bar(ic, x + 34, y + 114, 80, 9, fill=ink)
    bar(ic, x + 50, y + 128, 48, 6, fill=ink, opacity=0.7)


# --- Zoom: a webcam on its clip, the mark printed on it --------------------

@soft("zoom")
def zoom(ic):
    tile(ic, "#2F6FE4", "#103684")
    soft_shadow(ic, 128, 210, 66, 10)
    ic.path("M120 132h16l4 40h-24z", fill="#9AA1A9")
    ic.rect(76, 176, 104, 30, rx=12, fill=two(ic, "#3A3D44", "#1E2024"))
    ic.circle(128, 176, 11, fill="#2E3036")
    ic.rect(30, 52, 196, 90, rx=45, fill=two(ic, "#FFFFFF", "#C4CCD8"))
    cx, cy = 128, 97
    ic.circle(cx, cy, 40, fill=two(ic, "#B9C2CE", "#7C8796"))
    ic.circle(cx, cy, 34, fill="#24262B")
    ic.circle(cx, cy, 27, fill="#0B5CFF")
    ic.circle(cx, cy, 22, fill=two(ic, "#1B3E8C", "#060C1E"))
    ic.circle(cx - 8, cy - 8, 5, fill="#fff", opacity=0.5)
    with ic.g(transform="translate(50 80)"):
        ic.rect(0, 0, 34, 34, rx=10, fill="#1F6BFF")
        ic.rect(6, 11, 15, 12, rx=3, fill="#fff")
        ic.path("M22 15.5 L28.5 11.5 V22.5 L22 18.5 Z", fill="#fff", stroke="#fff", stroke_width=1.5,
                stroke_linejoin="round")
    ic.circle(190, 88, 5, fill="#4DF08A")


# --- Mixin Messenger: a blue leather wallet, the mark stamped in foil ---------

def _mixin_mark(ic, cx, cy, k, fill):
    t = f"translate({cx} {cy}) scale({k})"
    ic.path("M-30 -24 L-19 -17 V17 L-30 24 Z M30 -24 L19 -17 V17 L30 24 Z", fill=fill, transform=t,
            stroke=fill, stroke_width=3, stroke_linejoin="round")
    hexd = "M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in (polar(0, 0, 11.5, a) for a in range(0, 360, 60))) + "Z"
    ic.path(hexd, fill=fill, transform=t, stroke=fill, stroke_width=3, stroke_linejoin="round")


@soft("mixin")
def mixin(ic):
    tile(ic, "#3A4766", "#161D30")
    soft_shadow(ic, 128, 210, 100, 12)
    with ic.g(transform="rotate(-7 120 80)"):
        ic.rect(60, 40, 112, 70, rx=10, fill=two(ic, "#2AB0FA", "#2B5EE8"))
        ic.rect(74, 54, 20, 15, rx=4, fill=two(ic, "#F6DDA0", "#C8984A"))
    with ic.g(transform="rotate(5 160 70)"):
        ic.rect(136, 36, 68, 58, rx=5, fill=two(ic, "#FFFFFF", "#ECE8DF"))
        bar(ic, 146, 48, 36, fill="#2B5EE8")
        bar(ic, 146, 62, 46)
    ic.rect(28, 76, 200, 128, rx=20, fill=two(ic, "#3C8EF2", "#1D4CB4"))
    ic.rect(28, 76, 200, 12, rx=6, fill="#000", opacity=0.15)
    ic.path("M186 74h28v74a14 14 0 0 1-28 0z", fill=two(ic, "#3484EC", "#1A44A8"))
    ic.circle(200, 146, 8, fill=two(ic, *STEEL))
    _mixin_mark(ic, 124, 142, 1.25, "#EEF3FB")
