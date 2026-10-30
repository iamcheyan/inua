"""The code editors, soft: the same objects as drawings/apps_code.py with
about half the detail, no text and no glare. The JetBrains badges keep
their two letters, drawn as bold strokes."""

import re

from lib import bar, soft, soft_shadow, tile, two

STEEL = ("#AEB4BB", "#8D949C")


def _pts(pts, dx=0, dy=0, k=1.0):
    return [(dx + x * k, dy + y * k) for x, y in pts]


# --- the JetBrains IDEs: hardcover notebooks ---------------------------------

# Block letters on a unit cell (x across its width, y down), drawn as strokes.
LETTERS = {
    "I": (0.0, "M0 0L0 1"),
    "J": (0.75, "M1 0L1 0.62Q1 1 0.5 1Q0 1 0 0.72"),
    "P": (0.8, "M0 1L0 0L0.55 0Q1 0 1 0.28Q1 0.56 0.55 0.56L0 0.56"),
    "C": (0.85, "M1 0.16Q0.86 0 0.52 0Q0 0 0 0.5Q0 1 0.52 1Q0.86 1 1 0.84"),
    "G": (0.85, "M1 0.16Q0.86 0 0.52 0Q0 0 0 0.5Q0 1 0.52 1Q1 1 1 0.58L0.56 0.58"),
    "O": (0.85, "M0.5 0Q1 0 1 0.5Q1 1 0.5 1Q0 1 0 0.5Q0 0 0.5 0Z"),
    "W": (1.25, "M0 0L0.24 1L0.5 0.36L0.76 1L1 0"),
    "S": (0.8, "M1 0.13Q0.82 0 0.5 0Q0.02 0 0.02 0.27Q0.02 0.5 0.5 0.5Q1 0.5 1 0.75Q1 1 0.5 1Q0.16 1 0 0.86"),
    "D": (0.8, "M0 0L0 1L0.42 1Q1 1 1 0.5Q1 0 0.42 0Z"),
}


def _letters(ic, s, x, y, h, w, fill):
    """Two block letters, their top left at (x, y), h tall, stroke w."""
    for c in s:
        k, d = LETTERS[c]
        cw = h * 0.72 * k
        nums = iter(range(10_000))

        def place(m, cx=x, cw=cw):
            v = float(m.group())
            return f"{(cx + v * cw) if next(nums) % 2 == 0 else (y + v * h):.1f}"
        ic.path(re.sub(r"-?\d*\.?\d+", place, d), fill="none", stroke=fill, stroke_width=w,
                stroke_linecap="square" if c in "IJ" else "butt", stroke_linejoin="round")
        x += cw + w + 5


def _notebook(ic, abbr, stops, ground, code):
    tile(ic, *ground)
    soft_shadow(ic, 130, 214, 92, 12)
    with ic.g(transform="rotate(-4 128 128)"):
        with ic.g(transform="rotate(7 150 60)"):
            ic.rect(100, 8, 100, 70, rx=6, fill="#FFFDF7")
            ic.path("M100 14a6 6 0 0 1 6-6h88a6 6 0 0 1 6 6v4H100z", fill=stops[0][1])
            for i, (w, col) in enumerate(code):
                bar(ic, 108, 24 + i * 11, w, 6, fill=col)
        ic.rect(52, 42, 152, 172, rx=12, fill="#15161A")
        ic.rect(50, 38, 150, 170, rx=10, fill=two(ic, "#F7F1E4", "#E2DACA"))
        ic.rect(44, 34, 150, 170, rx=12, fill=ic.lin(stops, 0, 0, 1, 1))
        ic.path("M56 34h8v170h-8a12 12 0 0 1-12-12V46a12 12 0 0 1 12-12z", fill="#000", opacity=0.16)
        ic.rect(80, 122, 66, 66, rx=3, fill="#000")
        _letters(ic, abbr, 88, 131, 22, 6, "#fff")
        ic.rect(88, 170, 26, 6, rx=1, fill="#fff")
        ic.rect(170, 32, 10, 174, rx=4, fill="#1B1C20")
        ic.path("M150 206v20l5-5 5 5v-20z", fill=stops[-1][1])


JB_CODE = lambda a, b, c: [(64, a), (80, b), (48, c)]


@soft("intellij-idea")
def intellij(ic):
    _notebook(ic, "IJ", [(0, "#FC801D"), (0.45, "#FE2857"), (1, "#7B3BF0")], ("#4A3270", "#22143A"),
              JB_CODE("#0033B3", "#3A3A40", "#871094"))


@soft("pycharm")
def pycharm(ic):
    _notebook(ic, "PC", [(0, "#FCF84A"), (0.5, "#21D789"), (1, "#07A3D2")], ("#1F6050", "#0C2E26"),
              JB_CODE("#0033B3", "#3A3A40", "#067D17"))


@soft("goland")
def goland(ic):
    _notebook(ic, "GO", [(0, "#3BEA62"), (0.5, "#0D7BF7"), (1, "#8F4AF7")], ("#2B4C8C", "#121F45"),
              JB_CODE("#0033B3", "#3A3A40", "#067D17"))


@soft("webstorm")
def webstorm(ic):
    _notebook(ic, "WS", [(0, "#FCF84A"), (0.45, "#07C3F2"), (1, "#087CFA")], ("#1A5E86", "#0A2C46"),
              JB_CODE("#0033B3", "#3A3A40", "#1750EB"))


@soft("datagrip")
def datagrip(ic):
    _notebook(ic, "DG", [(0, "#22D88F"), (0.5, "#9775F8"), (1, "#FF45ED")], ("#3E3478", "#1A1540"),
              JB_CODE("#0033B3", "#0033B3", "#3A3A40"))


# --- VS Code and VSCodium: their folded marks as enamel pins on a page --------

def _page(ic, lines):
    with ic.g(transform="rotate(-6 120 124)"):
        ic.rect(38, 40, 150, 172, rx=8, fill=two(ic, "#FFFFFF", "#ECE8DF"))
        bar(ic, 50, 52, 56, 8, fill="#3A3F4A")
        for i, (x, w, col) in enumerate(lines):
            bar(ic, 52 + x, 74 + i * 14, w, 7, fill=col)


VS_BACK = [(66, 2), (78, 12), (14, 74), (4, 66)]
VS_FRONT = [(66, 98), (78, 88), (14, 26), (4, 34)]
VS_PANEL = [(70, 4), (98, 16), (98, 84), (70, 96), (74, 74), (74, 26)]


def _vs_pin(ic, x, y, k, tones, rim):
    back, front, (pl, pd) = tones
    for shape in (VS_BACK, VS_FRONT, VS_PANEL):
        ic.poly(_pts(shape, x + 2, y + 3.5, k), fill=rim, stroke=rim, stroke_width=4, stroke_linejoin="round")
    ic.poly(_pts(VS_BACK, x, y, k), fill=back, stroke=back, stroke_width=3, stroke_linejoin="round")
    ic.poly(_pts(VS_FRONT, x, y, k), fill=front, stroke=front, stroke_width=3, stroke_linejoin="round")
    ic.poly(_pts(VS_PANEL, x, y, k), fill=two(ic, pl, pd), stroke=pl, stroke_width=3, stroke_linejoin="round")


@soft("code")
def vscode(ic):
    tile(ic, "#2A6FB0", "#0F3A66")
    soft_shadow(ic, 132, 214, 96, 12)
    kw, ty, st, fn = "#AF00DB", "#267F99", "#A31515", "#795E26"
    _page(ic, [(0, 70, kw), (8, 76, st), (0, 64, kw), (8, 60, fn), (8, 50, ty), (16, 56, st), (0, 10, "#3A3F4A")])
    soft_shadow(ic, 168, 196, 64, 10)
    _vs_pin(ic, 98, 70, 1.16, ("#0B5DA8", "#1180D8", ("#3DB0FF", "#0B6CC0")), "#0B3B6A")


@soft("vscodium")
def vscodium(ic):
    tile(ic, "#2E8C9E", "#124652")
    soft_shadow(ic, 132, 214, 96, 12)
    kw, st = "#0451A5", "#A31515"
    _page(ic, [(0, 10, "#3A3F4A"), (8, 64, kw), (16, 70, kw), (24, 40, st), (8, 70, kw), (24, 50, st),
               (0, 10, "#3A3F4A")])
    soft_shadow(ic, 168, 196, 64, 10)
    _vs_pin(ic, 98, 70, 1.16, ("#2C7FB8", "#5FB4E8", ("#B4E7FF", "#4BA6DC")), "#1B4F70")


# --- Sublime Text: an orange S inlaid in a slate ------------------------------

S_BARS = [
    [(18, 40), (82, 14), (82, 36), (18, 62)],
    [(18, 40), (82, 66), (82, 88), (18, 62)],
    [(18, 66), (82, 40), (82, 62), (18, 88)],
]


@soft("sublime-text")
def sublime(ic):
    tile(ic, "#B4622A", "#5E2A0E")
    soft_shadow(ic, 128, 214, 96, 12)
    ic.rect(36, 44, 184, 172, rx=28, fill="#121316")
    ic.rect(36, 34, 184, 170, rx=28, fill=two(ic, "#464A52", "#25282D"))
    x, y, k = 70, 40, 1.16
    for idx, col in ((1, "#C9530C"), (0, "#FFA040"), (2, "#FF8A1F")):
        ic.poly(_pts(S_BARS[idx], x, y, k), fill=col, stroke=col, stroke_width=2, stroke_linejoin="round")
    bar(ic, 84, 166, 88, 9, fill="#8A8F98")


# --- Zed: a keycap with its mark ---------------------------------------------

def _zed_mark(ic, x, y, k, col, w):
    d = (f"M{x + 22 * k:.1f} {y + 12 * k:.1f}H{x + 88 * k:.1f}V{y + 70 * k:.1f}"
         f"M{x + 78 * k:.1f} {y + 88 * k:.1f}H{x + 12 * k:.1f}V{y + 30 * k:.1f}"
         f"M{x + 34 * k:.1f} {y + 32 * k:.1f}H{x + 66 * k:.1f}L{x + 34 * k:.1f} {y + 68 * k:.1f}H{x + 66 * k:.1f}")
    ic.path(d, fill="none", stroke=col, stroke_width=w, stroke_linejoin="miter", stroke_linecap="square")


@soft("zed")
def zed(ic):
    tile(ic, "#2F5FB8", "#14306A")
    soft_shadow(ic, 128, 214, 96, 13)
    ic.path("M42 72a24 24 0 0 1 24-24h124a24 24 0 0 1 24 24l10 114a22 22 0 0 1-22 24H54a22 22 0 0 1-22-24z",
            fill=two(ic, "#2E3036", "#111215"))
    ic.rect(56, 44, 144, 136, rx=24, fill=two(ic, "#3E4148", "#22242A"))
    ic.rect(64, 52, 128, 120, rx=18, fill="#26282E")
    _zed_mark(ic, 84, 66, 0.88, "#F4F6FA", 11)


# --- Cursor: its cube, in smoked glass and graphite ---------------------------

@soft("cursor")
def cursor(ic):
    tile(ic, "#34363C", "#0F1012")
    soft_shadow(ic, 128, 212, 84, 12)
    cx, top, r = 128, 30, 92
    hw = r * 0.866
    T, C, B = (cx, top), (cx, top + r), (cx, top + 2 * r)
    L1, R1 = (cx - hw, top + r / 2), (cx + hw, top + r / 2)
    L2, R2 = (cx - hw, top + r * 1.5), (cx + hw, top + r * 1.5)
    ic.poly([T, R1, C, L1], fill="#7A7E86", stroke="#7A7E86", stroke_width=6, stroke_linejoin="round")
    ic.poly([L1, C, B, L2], fill="#383B42", stroke="#383B42", stroke_width=6, stroke_linejoin="round")
    ic.poly([C, R1, R2, B], fill="#1C1E22", stroke="#1C1E22", stroke_width=6, stroke_linejoin="round")
    ic.poly([C, R1, T], fill="#F4F5F7", stroke="#F4F5F7", stroke_width=2, stroke_linejoin="round")
    ic.poly([C, R1, R2], fill=two(ic, "#E9EBEE", "#A4A8B0"), stroke="#C9CCD2", stroke_width=2,
            stroke_linejoin="round")


# --- Android Studio: a drafting compass on a blueprint -----------------------

@soft("android-studio")
def android_studio(ic):
    tile(ic, "#1C5A6E", "#082C3A")
    soft_shadow(ic, 128, 214, 100, 12)
    with ic.g(transform="rotate(-4 128 160)"):
        ic.rect(28, 112, 200, 100, rx=8, fill=two(ic, "#2C6BD8", "#1A4CA8"))
        ic.rect(44, 124, 46, 80, rx=9, fill="none", stroke="#E8F0FF", stroke_width=3)
        ic.rect(51, 136, 32, 54, rx=2, fill="none", stroke="#E8F0FF", stroke_width=2, opacity=0.6)
    ic.path("M139.6 124.3A72 72 0 0 1 186 186", fill="none", stroke="#fff", stroke_width=3,
            stroke_linecap="round")
    hx, hy = 150, 60
    leg = two(ic, *STEEL)
    ic.line(hx - 3, hy + 18, 116, 178, stroke=leg, stroke_width=10, stroke_linecap="round")
    ic.line(hx + 3, hy + 18, 184, 170, stroke=leg, stroke_width=10, stroke_linecap="round")
    ic.path("M111 175l10 4-7 17z", fill="#C3C8CE", stroke="#C3C8CE", stroke_width=2, stroke_linejoin="round")
    ic.path("M180 166l11 3-2 11-5 7-4-10z", fill="#2A2C30", stroke="#2A2C30", stroke_width=2,
            stroke_linejoin="round")
    ic.rect(hx - 10, hy + 11, 20, 16, rx=5, fill="#8D949C")
    green = "#3DDC84"
    ic.line(hx - 11, hy - 20, hx - 19, hy - 34, stroke=green, stroke_width=6, stroke_linecap="round")
    ic.line(hx + 11, hy - 20, hx + 19, hy - 34, stroke=green, stroke_width=6, stroke_linecap="round")
    ic.path(f"M{hx - 32} {hy + 13}a32 32 0 0 1 64 0z", fill=two(ic, "#5EE89C", "#28B068"))
    ic.circle(hx - 12, hy - 1, 4.5, fill="#073042")
    ic.circle(hx + 12, hy - 1, 4.5, fill="#073042")
