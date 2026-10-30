"""The soft drawings of tier 2 code: Godot, Unity Hub, Arduino IDE, Qt
Creator, Geany, Kate, Text Editor, Meld, GitKraken, Bruno, Beekeeper
Studio, pgAdmin, MongoDB Compass, Podman Desktop. The same objects as
drawings/apps_t2_code.py, about half the detail, no text."""

import math

from lib import bar, polar, soft, soft_shadow, tile, two

BRASS = ("#E2B45E", "#B88433")
STEEL = ("#AEB4BB", "#8D949C")


def _f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def _pts(pts):
    return "M" + "L".join(f"{_f(x)} {_f(y)}" for x, y in pts) + "Z"


def _bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def _taper(pts, w0, w1, n=12):
    """A limb along a chain of cubic Béziers, w0 wide at its start and w1
    at its rounded end."""
    line = []
    for s in range(0, len(pts) - 1, 3):
        for i in range(n + (1 if s + 4 >= len(pts) else 0)):
            line.append(_bez(pts[s], pts[s + 1], pts[s + 2], pts[s + 3], i / n))
    m = len(line)
    left, right = [], []
    for i, (x, y) in enumerate(line):
        a, b = line[max(i - 1, 0)], line[min(i + 1, m - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy) or 1
        w = (w0 + (w1 - w0) * i / (m - 1)) / 2
        left.append((x - dy / d * w, y + dx / d * w))
        right.append((x + dy / d * w, y - dx / d * w))
    r = w1 / 2
    d = "M" + "L".join(f"{_f(x)} {_f(y)}" for x, y in left)
    d += f"A{_f(r)} {_f(r)} 0 0 0 {_f(right[-1][0])} {_f(right[-1][1])}"
    d += "L" + "L".join(f"{_f(x)} {_f(y)}" for x, y in reversed(right)) + "Z"
    return d


def _infinity(cx, cy, w, h):
    q = w / 2
    return (f"M{_f(cx)} {_f(cy)}C{_f(cx + q * 0.35)} {_f(cy - h)} {_f(cx + q)} {_f(cy - h)} {_f(cx + q)} {_f(cy)}"
            f"C{_f(cx + q)} {_f(cy + h)} {_f(cx + q * 0.35)} {_f(cy + h)} {_f(cx)} {_f(cy)}"
            f"C{_f(cx - q * 0.35)} {_f(cy - h)} {_f(cx - q)} {_f(cy - h)} {_f(cx - q)} {_f(cy)}"
            f"C{_f(cx - q)} {_f(cy + h)} {_f(cx - q * 0.35)} {_f(cy + h)} {_f(cx)} {_f(cy)}Z")


@soft("godot")
def godot(ic):
    tile(ic, "#35546F", "#152536")
    soft_shadow(ic, 128, 214, 84, 11)
    ic.ellipse(128, 204, 58, 11, fill="#1E2328")
    ic.rect(70, 190, 116, 14, fill="#2E3339")
    ic.ellipse(128, 190, 58, 11, fill="#4A5058")
    ic.rect(106, 174, 44, 18, fill=two(ic, *STEEL))
    blue = two(ic, "#7DBCE8", "#3E7FB2")
    for x in (32, 198):
        ic.rect(x, 110, 26, 46, rx=12, fill="#2B6290")
    for cx, cy, r in ((82, 62, 20), (128, 52, 22), (174, 62, 20)):
        ic.circle(cx, cy, r, fill=blue)
    ic.rect(52, 56, 152, 128, rx=36, fill=blue)
    ic.path("M56 146 H200 V150 a34 34 0 0 1 -34 34 H90 a34 34 0 0 1 -34-34z", fill="#2B6290")
    ic.rect(72, 148, 112, 20, rx=10, fill="#EEF5FB")
    for x in (92, 110, 128, 146, 164):
        ic.circle(x, 158, 5.5, fill="#3A78A8")
    for ex, px in ((96, 102), (160, 154)):
        ic.circle(ex, 110, 26, fill=two(ic, "#FFFFFF", "#DCE8F2"))
        ic.circle(px, 113, 12.5, fill="#3E4147")


@soft("unityhub")
def unityhub(ic):
    tile(ic, "#45494F", "#17191C")
    soft_shadow(ic, 128, 216, 78, 10)
    ic.ellipse(128, 206, 50, 12, fill="#1A1C1F")
    ic.rect(78, 196, 100, 10, fill="#2C2F33")
    ic.ellipse(128, 196, 50, 12, fill="#4A4E54")
    ic.rect(116, 174, 24, 24, fill=two(ic, *STEEL))
    ic.path("M54 150 a74 34 0 0 0 148 0 v10 a74 34 0 0 1 -148 0z", fill="#232528")
    ic.ellipse(128, 150, 74, 34, fill=two(ic, "#8E939A", "#5A5F66"))
    a, b, h, T = 54, 31, 62, 38
    top = [(128, T), (128 + a, T + b), (128, T + 2 * b), (128 - a, T + b)]
    left = [(128 - a, T + b), (128, T + 2 * b), (128, T + 2 * b + h), (128 - a, T + b + h)]
    right = [(128 + a, T + b), (128 + a, T + b + h), (128, T + 2 * b + h), (128, T + 2 * b)]
    ic.path(_pts(top), fill="#FFFFFF")
    ic.path(_pts(left), fill="#D2D5D9")
    ic.path(_pts(right), fill="#7E838A")
    seam = dict(stroke="#1F2125", stroke_width=8, stroke_linecap="round")
    ic.line(128, T + 2 * b, 128, T + 2 * b + h, **seam)
    ic.line(128, T + 2 * b, 128 - a, T + b, **seam)
    ic.line(128, T + 2 * b, 128 + a, T + b, **seam)
    hexa = [(128, T), (128 + a, T + b), (128 + a, T + b + h), (128, T + 2 * b + h), (128 - a, T + b + h), (128 - a, T + b)]
    ic.path(_pts(hexa), fill="none", stroke="#1F2125", stroke_width=5, stroke_linejoin="round")


@soft("arduino")
def arduino(ic):
    tile(ic, "#24676B", "#0C3236")
    soft_shadow(ic, 130, 212, 100, 12)
    with ic.g(transform="rotate(-6 128 128)"):
        ic.rect(36, 68, 188, 130, rx=10, fill="#00494C")
        ic.rect(34, 64, 188, 130, rx=10, fill=two(ic, "#14B3B8", "#00858A"))
        for x, y in ((48, 78), (208, 78), (208, 180)):
            ic.circle(x, y, 6, fill="#D9DEE3")
            ic.circle(x, y, 3, fill="#062A2C")
        for x0, x1, y in ((100, 196, 70), (118, 196, 178)):
            ic.rect(x0, y, x1 - x0, 12, rx=3, fill="#1A1C1F")
        ic.rect(20, 86, 48, 32, rx=4, fill=two(ic, *STEEL))
        ic.rect(22, 146, 38, 30, rx=5, fill="#1E2024")
        ic.circle(80, 82, 6, fill="#C8372D")
        ic.rect(116, 144, 84, 20, rx=4, fill="#1E2024")
        ic.path(_infinity(150, 108, 64, 16), fill="none", stroke="#FFFFFF", stroke_width=8, stroke_linejoin="round")
        ic.rect(125, 106, 11, 4, rx=1.5, fill="#fff")
        ic.rect(164, 106, 11, 4, rx=1.5, fill="#fff")
        ic.rect(167.5, 102.5, 4, 11, rx=1.5, fill="#fff")
        bar(ic, 124, 128, 52, 7, fill="#FFFFFF")


def _qt_shape(x0, y0, x1, y1, c):
    return _pts([(x0 + c, y0), (x1, y0), (x1, y1 - c), (x1 - c, y1), (x0, y1), (x0, y0 + c)])


@soft("qtcreator")
def qtcreator(ic):
    tile(ic, "#3B5E48", "#15301F")
    soft_shadow(ic, 128, 214, 100, 12)
    ic.path("M42 98 H214 L210 120 H46z", fill="#121417")
    with ic.g(transform="rotate(-14 84 100)"):
        ic.rect(80, 30, 8, 54, rx=3, fill=two(ic, *STEEL))
        ic.rect(73, 76, 22, 50, rx=9, fill=two(ic, "#6EDC7E", "#2FA03E"))
    with ic.g(transform="rotate(10 168 100)"):
        ic.rect(160, 46, 16, 70, rx=5, fill=two(ic, *STEEL))
        ic.path("M168 20 a21 21 0 1 1 -0.1 0z M162 22 v16 h12 v-16z", fill=two(ic, *STEEL), fill_rule="evenodd")
    with ic.g(transform="rotate(4 128 100)"):
        ic.rect(117, 38, 18, 82, rx=3, fill=two(ic, "#F6D46A", "#D8A62E"))
    for x in (50, 199):
        ic.rect(x, 52, 8, 52, rx=3, fill="#9AA1A9")
    ic.rect(46, 46, 164, 12, rx=6, fill=two(ic, "#D4D9DE", "#8D949C"))
    ic.rect(98, 44, 60, 16, rx=8, fill="#1E2024")
    ic.path("M38 104 H218 L210 196 a8 8 0 0 1 -8 8 H54 a8 8 0 0 1 -8-8z", fill=two(ic, "#474D55", "#24282D"))
    ic.rect(32, 96, 192, 16, rx=6, fill=two(ic, "#D4D9DE", "#8D949C"))
    for x in (58, 184):
        ic.rect(x, 108, 14, 22, rx=3, fill="#AEB4BB")
    ic.path(_qt_shape(88, 126, 168, 184, 14), fill=two(ic, "#6EDC7E", "#34A844"))
    ic.circle(117, 153, 13, fill="none", stroke="#fff", stroke_width=7)
    ic.line(123, 160, 132, 170, stroke="#fff", stroke_width=7, stroke_linecap="round")
    ic.rect(140, 136, 7.5, 36, rx=3.5, fill="#fff")
    ic.rect(134, 146, 20, 6.5, rx=3, fill="#fff")


@soft("geany")
def geany(ic):
    tile(ic, "#34417A", "#141A3C")
    soft_shadow(ic, 120, 212, 96, 11)
    with ic.g(transform="translate(-10 0)"):
        ic.path("M62 128 C26 120 22 176 66 168", fill="none", stroke="#C9963F", stroke_width=12,
                stroke_linecap="round")
        ic.ellipse(126, 202, 36, 8, fill="#8C6224")
        ic.path("M106 178 H146 L158 200 H94z", fill=two(ic, *BRASS))
        ic.path("M54 150 C54 120 92 106 126 106 C162 106 190 118 200 136 L230 112 C235 107 243 112 238 118"
                " L206 158 C196 174 166 186 126 186 C88 186 54 174 54 150Z", fill=two(ic, *BRASS))
        ic.path("M58 156 C80 170 170 172 200 152", fill="none", stroke="#9C6C24", stroke_width=4,
                stroke_linecap="round", opacity=0.7)
        ic.ellipse(126, 106, 30, 8, fill="#9C6C24")
        lid = two(ic, "#7FD46E", "#2E8A2A")
        ic.path("M100 100 C100 76 112 64 126 64 C140 64 152 76 152 100 C140 106 112 106 100 100Z", fill=lid)
        ic.circle(126, 58, 9, fill=lid)
        ic.path("M234 112 C224 104 227 90 236 78 C239 90 248 99 241 110 C239 114 236 114 234 112Z", fill="#F59A3C")
        ic.path("M235 110 C231 104 233 98 236 92 C238 98 241 104 238 109Z", fill="#FFE68A")


@soft("kate")
def kate(ic):
    tile(ic, "#2A5592", "#0F2650")
    soft_shadow(ic, 128, 214, 84, 11)
    with ic.g(transform="translate(12 0)"):
        ic.rect(48, 34, 54, 176, fill=two(ic, "#8E6A45", "#5E3E20"))
        ic.ellipse(75, 210, 27, 6, fill="#3A2412")
        ic.ellipse(75, 34, 27, 9, fill=two(ic, "#F2DDB4", "#C9A46E"))
        ic.ellipse(76, 34.5, 12, 3.6, fill="none", stroke="#9C7A55", stroke_width=2)
        ic.ellipse(100, 112, 4, 6, fill="#1E1208")
        ic.path("M128 166 L142 172 L126 212 L114 210z", fill="#0B2C58")
        ic.ellipse(140, 136, 30, 52, fill=two(ic, "#3FA2EA", "#0D5AA6"), transform="rotate(16 140 136)")
        ic.ellipse(126, 140, 14, 36, fill="#BFE0F6", transform="rotate(16 126 140)")
        ic.path("M150 104 C174 112 178 150 160 186 C152 172 146 142 150 104Z", fill="#0E3E78")
        ic.circle(140, 80, 28, fill=two(ic, "#6CC2F8", "#1D7FD0"))
        ic.path("M134 52 C150 42 170 46 182 58 C168 58 162 62 160 74 C156 62 146 56 134 52Z", fill="#0B2C58")
        ic.path("M116 70 L86 80 L116 91z", fill=two(ic, "#F4F8FC", "#B4C0CC"))
        ic.circle(130, 76, 8, fill="#fff")
        ic.circle(129, 76, 5, fill="#0A1626")


@soft("gedit")
def gedit(ic):
    tile(ic, "#5C6D80", "#28323E")
    soft_shadow(ic, 124, 214, 94, 12)
    with ic.g(transform="rotate(-5 124 124)"):
        ic.path("M58 34 H170 L198 62 V204 a8 8 0 0 1 -8 8 H58 a8 8 0 0 1 -8-8 V42 a8 8 0 0 1 8-8z",
                fill=two(ic, "#FFFFFF", "#ECE8DF"))
        ic.line(70, 34, 70, 212, stroke="#E58A8A", stroke_opacity=0.6, stroke_width=2)
        bar(ic, 80, 56, 64, 9, fill="#2B3440")
        for i, w in enumerate((70, 92, 84, 60, 88, 72)):
            bar(ic, 80, 80 + i * 18, w, 7, fill="#8C96A3")
        ic.path("M170 34 V62 H198z", fill="#D8D3C8")
    with ic.g(transform="translate(134 200) rotate(-50)"):
        ic.path("M0 0 L24 -9 V9z", fill="#E8C68E")
        ic.path("M0 0 L9 -3.4 V3.4z", fill="#2A2C30")
        ic.rect(24, -9, 94, 18, fill=two(ic, "#FFD84D", "#E0A010"))
        ic.rect(118, -9.5, 16, 19, fill=two(ic, *STEEL))
        ic.rect(134, -9, 14, 18, rx=4, fill="#E07F78")


@soft("meld")
def meld(ic):
    tile(ic, "#4E5A6A", "#1E2530")
    soft_shadow(ic, 128, 216, 104, 12)
    ic.rect(22, 42, 212, 170, rx=12, fill=two(ic, "#C8935C", "#8E5A2C"))
    left, right = (32, 120), (136, 224)
    for x0, x1 in (left, right):
        ic.rect(x0, 54, x1 - x0, 148, rx=4, fill="#FBF9F4")
    bands = [((72, 90), (80, 98), "#3584E4"), ((110, 132), (118, 148), "#4CB860"), ((160, 172), (184, 186), "#E0533F")]
    for (l0, l1), (r0, r1), c in bands:
        ic.rect(left[0], l0, left[1] - left[0], l1 - l0, fill=c, opacity=0.3)
        ic.rect(right[0], r0, right[1] - right[0], r1 - r0, fill=c, opacity=0.3)
        ic.path(f"M120 {l0} C128 {l0} 128 {r0} 136 {r0} V{r1} C128 {r1} 128 {l1} 120 {l1}z", fill=c)
    for side, (x0, x1) in enumerate((left, right)):
        for i, w in enumerate((52, 40, 60, 34, 50, 56, 30, 44)):
            if side == 1 and i == 6:
                continue
            bar(ic, x0 + 9, 76 + i * 15, min(w + (8 if side else 0), x1 - x0 - 18), 5, fill="#5A6470")
    for cx in (76, 180):
        ic.rect(cx - 18, 38, 36, 20, rx=5, fill="#1E2024")


@soft("gitkraken")
def gitkraken(ic):
    tile(ic, "#21414F", "#0A1A22")
    soft_shadow(ic, 128, 214, 98, 12)
    teal = two(ic, "#3FD0C0", "#0E7A70")
    arms = [
        [(96, 140), (80, 168), (40, 160), (40, 186), (40, 204), (66, 206), (66, 192)],
        [(110, 146), (102, 176), (76, 200), (92, 208), (102, 212), (110, 202), (104, 196)],
        [(124, 148), (124, 180), (128, 200), (130, 208), (132, 214), (142, 212), (138, 204)],
        [(140, 146), (150, 176), (168, 196), (176, 206), (184, 214), (190, 204), (182, 198)],
        [(158, 140), (178, 168), (218, 162), (218, 188), (218, 206), (192, 206), (192, 192)],
    ]
    for pts in arms:
        ic.path(_taper(pts, 28, 9), fill=teal)
    ic.path("M68 142 C58 92 82 38 128 38 C174 38 198 92 188 142 C168 158 88 158 68 142Z", fill=teal)
    for ex in (106, 150):
        ic.ellipse(ex, 112, 17, 19, fill="#FFFFFF")
        ic.circle(ex + 3, 116, 9.5, fill="#0B1E26")
    ic.path("M112 140 C120 146 136 146 144 140", fill="none", stroke="#0B4F49", stroke_width=4.5,
            stroke_linecap="round")


@soft("bruno")
def bruno(ic):
    tile(ic, "#34465C", "#141D2A")
    soft_shadow(ic, 128, 216, 76, 10)
    fur = two(ic, "#FFC864", "#E0952C")
    ear = two(ic, "#8A5428", "#5A3416")
    ic.path("M74 196 C70 168 92 150 128 150 C164 150 186 168 182 196 C178 212 156 216 128 216 C100 216 78 212 74 196Z", fill=fur)
    ic.path("M76 62 C46 60 36 100 44 140 C48 156 66 158 72 142 C78 120 86 92 92 72Z", fill=ear)
    ic.path("M180 62 C210 60 220 100 212 140 C208 156 190 158 184 142 C178 120 170 92 164 72Z", fill=ear)
    ic.ellipse(128, 104, 62, 58, fill=fur)
    ic.path("M76 160 C100 176 156 176 180 160 L184 174 C158 192 98 192 72 174Z", fill="#C8402E")
    ic.circle(128, 198, 15, fill=two(ic, *BRASS))
    ic.ellipse(128, 132, 34, 25, fill="#FFF2DA")
    ic.path("M110 141 C118 150 138 150 146 141", fill="none", stroke="#3E220C", stroke_width=3.5, stroke_linecap="round")
    ic.path("M122 146 C122 158 134 158 134 146Z", fill="#E5707A")
    ic.path("M128 121 C115 121 111 112 115 107 C120 103 136 103 141 107 C145 112 141 121 128 121Z", fill="#1E1410")
    for x in (102, 154):
        ic.circle(x, 94, 9, fill="#1E1410")


@soft("beekeeper-studio")
def beekeeper(ic):
    tile(ic, "#3A3F4A", "#15181E")
    soft_shadow(ic, 128, 214, 98, 12)
    ic.rect(30, 190, 196, 18, rx=5, fill=two(ic, "#9C6A3C", "#5E3818"))
    for x in (44, 202):
        ic.rect(x, 206, 10, 10, rx=2, fill="#3A2210")
    straw = two(ic, "#F6D27A", "#C98A2A")
    rows = 6
    for i in range(rows):
        y = 168 - i * 23
        t = (190 - (y + 12)) / 150
        w = max(86 * math.sqrt(max(1 - t * t, 0)), 28) if i < rows - 1 else 30
        ic.rect(128 - w, y + 3, 2 * w, 26, rx=13, fill="#8C5E1A")
        ic.rect(128 - w, y, 2 * w, 26, rx=13, fill=straw)
    ic.ellipse(128, 50, 18, 9, fill="#E8B94A")
    ic.path("M108 192 V182 a20 16 0 0 1 40 0 V192z", fill="#1E1208")
    hexa = [polar(128, 140, 16, a) for a in range(30, 390, 60)]
    ic.path(_pts(hexa), fill="#1E2026")
    ic.circle(128, 140, 5, fill="#FAD83B")
    for x, y, k, deg in ((198, 70, 1.5, -14), (58, 56, 1.2, 12)):
        with ic.g(transform=f"translate({x} {y}) rotate({deg}) scale({k})"):
            ic.ellipse(-1, -7, 6, 4, fill="#fff", opacity=0.8, transform="rotate(-20 -1 -7)")
            ic.ellipse(0, 0, 9, 6.4, fill="#FAD83B")
            ic.rect(-2.5, -6, 3, 12, fill="#1E1A14")
            ic.circle(8, -0.5, 4, fill="#1E1A14")


@soft("pgadmin4")
def pgadmin(ic):
    tile(ic, "#2C4B6C", "#10223A")
    soft_shadow(ic, 128, 214, 86, 11)
    ic.rect(60, 184, 136, 28, rx=4, fill=two(ic, "#3A3F46", "#1C1F23"))
    ic.rect(54, 176, 148, 13, rx=5, fill=two(ic, "#6A7078", "#454A52"))
    ic.rect(98, 193, 60, 12, rx=3, fill=two(ic, *BRASS))
    glaze = two(ic, "#5A94CC", "#2A5A86")
    trim = dict(fill="none", stroke="#F2F6FA", stroke_width=5)
    outline = dict(fill="none", stroke="#0C1E32", stroke_width=10)
    ears = ["M86 70 C52 52 26 80 34 118 C40 146 66 150 84 134 C92 120 94 92 86 70Z",
            "M170 70 C204 52 230 80 222 118 C216 146 190 150 172 134 C164 120 162 92 170 70Z"]
    for d in ears:
        ic.path(d, **outline)
        ic.path(d, fill=glaze)
        ic.path(d, **trim)
    trunk = [(128, 118), (126, 146), (124, 168), (146, 176), (164, 182), (172, 164), (160, 160)]
    ic.path(_taper(trunk, 34, 14), **outline)
    ic.path(_taper(trunk, 34, 14), fill=glaze)
    ic.path(_taper(trunk, 34, 14), **trim)
    head = "M128 42 C160 42 178 66 176 98 C174 124 156 136 128 136 C100 136 82 124 80 98 C78 66 96 42 128 42Z"
    ic.path(head, **outline)
    ic.path(head, fill=glaze)
    ic.path(head, **trim)
    ic.path(_taper(trunk[:4], 34, 26), fill=glaze)
    ic.path("M108 128 C104 142 108 152 116 156 C112 146 112 138 114 130Z", fill="#FBF8F0")
    ic.path("M148 128 C152 142 148 152 140 156 C144 146 144 138 142 130Z", fill="#FBF8F0")
    for x in (106, 150):
        ic.ellipse(x, 96, 7.5, 9, fill="#F2F6FA")
        ic.circle(x + 1, 97, 5, fill="#0C1E32")


@soft("mongodb-compass")
def compass(ic):
    tile(ic, "#14473D", "#03201C")
    cx, cy = 128, 132
    soft_shadow(ic, 128, 220, 86, 10)
    ic.circle(cx, 30, 12, fill="none", stroke="#D3A34E", stroke_width=8)
    ic.rect(cx - 12, 40, 24, 14, rx=4, fill=two(ic, *BRASS))
    ic.circle(cx, cy, 88, fill=two(ic, *BRASS))
    ic.circle(cx, cy, 74, fill=two(ic, "#FFFDF7", "#ECE3CF"))
    for k in range(12):
        big = k % 3 == 0
        x1, y1 = polar(cx, cy, 68, k * 30)
        x2, y2 = polar(cx, cy, 68 - (12 if big else 7), k * 30)
        ic.line(x1, y1, x2, y2, stroke="#C8372D" if k == 0 else "#2A2C30", stroke_width=5 if big else 3,
                stroke_linecap="round")
    leaf = (f"M{cx + 1} {cy - 48} C{cx + 22} {cy - 26} {cx + 20} {cy + 6} {cx + 4} {cy + 28}"
            f" L{cx} {cy + 46} L{cx - 4} {cy + 28} C{cx - 18} {cy + 8} {cx - 22} {cy - 22} {cx + 1} {cy - 48}Z")
    ic.path(leaf, fill=two(ic, "#3EE07E", "#00804E"))
    ic.line(cx + 0.5, cy - 38, cx, cy + 40, stroke="#C9FADB", stroke_width=2.5, stroke_linecap="round", opacity=0.8)
    ic.circle(cx, cy, 8, fill=two(ic, *BRASS))


@soft("podman-desktop")
def podman(ic):
    tile(ic, "#5A3A88", "#22103E")
    soft_shadow(ic, 120, 214, 92, 11)
    coat = two(ic, "#B8A9DC", "#6E5C9C")
    ic.ellipse(124, 204, 94, 14, fill="#8A78B8")
    ic.ellipse(124, 200, 94, 13, fill=two(ic, "#FFFFFF", "#DCD4F0"))
    ic.path("M64 200 C44 206 30 198 32 186 C42 192 56 192 68 188z", fill="#4E3E78")
    ic.path("M58 202 C40 168 66 126 120 108 L170 112 C176 140 172 172 162 198 C130 208 90 208 58 202Z", fill=coat)
    ic.path("M94 204 C90 176 108 142 138 128 C156 140 160 176 154 202 C134 207 112 207 94 204Z", fill="#E6DDF4", opacity=0.5)
    ic.path("M148 150 C164 158 182 176 188 194 C180 198 168 196 158 188 C150 180 144 168 148 150Z", fill="#5E4C8C")
    ic.ellipse(140, 104, 36, 32, fill=coat, transform="rotate(-24 140 104)")
    ic.ellipse(168, 86, 18, 14, fill="#E2D9F2", transform="rotate(-30 168 86)")
    ic.ellipse(176, 76, 7, 5.4, fill="#1A1028", transform="rotate(-30 176 76)")
    for x, y in ((128, 100), (150, 90)):
        ic.circle(x, y, 7.5, fill="#140A22")
    with ic.g(transform="rotate(-10 176 52)"):
        x, y, w, h = 138, 28, 78, 40
        ic.rect(x, y, w, h, rx=5, fill=two(ic, "#B464D6", "#7A2496"))
        for i in range(1, 6):
            ic.rect(x + i * 13 - 2, y + 6, 4, h - 12, rx=2, fill="#5A1470", opacity=0.45)
