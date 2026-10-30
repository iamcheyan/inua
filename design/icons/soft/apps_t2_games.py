"""The soft drawings of the games and emulators (t2-games): the same
objects as drawings/apps_t2_games.py, about half the detail, no text."""

from lib import bar, polar, soft, soft_shadow, tile, two


def _f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def _block(ic, x, y, w, h, n=8, depth=(2, 1, 2, 3, 2, 1, 2, 2), specks=((2, 5), (5, 4), (6, 7))):
    """A grass block, flat faces: its top face's left corner at (x, y), w
    its half-width, h its sides' height. The grass hangs down the sides in
    steps of n cells; a few darker cells in the dirt."""
    fx, fy = x + w, y + w / 2
    ic.poly([(x, y), (x + w, y - w / 2), (x + 2 * w, y), (fx, fy)], fill=two(ic, "#8AD055", "#6DB33F"))
    faces = (
        (f"matrix({_f(w / n)} {_f(w / 2 / n)} 0 {_f(h / n)} {_f(x)} {_f(y)})", "#8B5A2B", "#6DB33F", "#6A4220"),
        (f"matrix({_f(w / n)} {_f(-w / 2 / n)} 0 {_f(h / n)} {_f(fx)} {_f(fy)})", "#694320", "#4F8A2C", "#52331A"),
    )
    for k, (m, dirt, grass, speck) in enumerate(faces):
        ic.path(f"M0 0h{n}v{n}h-{n}z", fill=dirt, transform=m)
        d = "".join(f"M{i} 0h1v{depth[(i + 3 * k) % len(depth)]}h-1z" for i in range(n))
        ic.path(d, fill=grass, transform=m)
        ic.path("".join(f"M{i} {j}h1v1h-1z" for i, j in specks), fill=speck, transform=m)


@soft("prismlauncher")
def prismlauncher(ic):
    tile(ic, "#24345A", "#0D1428")
    soft_shadow(ic, 150, 212, 76, 11)
    _block(ic, 96, 150, 58, 40, 6, depth=(2, 1, 2, 1, 2, 2), specks=((1, 4), (4, 3)))
    ax, ay, lx, ly, rx, ry = 94, 30, 46, 116, 142, 116
    ox, oy = (ax + rx) / 2 + 2, (ay + ry) / 2
    for k, c in enumerate(["#E8686A", "#F4A35E", "#F6D86A", "#99CD61", "#4D9DE0", "#9E7BD8"]):
        ex, ey = 132 + k * 12, 146 - k * 3.2
        ic.poly([(ox + k * 1.6, oy + k * 2.6), (ox + k * 1.6 + 1.4, oy + k * 2.6 + 4), (ex + 14, ey + 3), (ex, ey)],
                fill=c)
    lmx, lmy = (ax + lx) / 2, (ay + ly) / 2
    ic.poly([(0, 28), (0, 42), (lmx + 2, lmy + 5), (lmx - 2, lmy - 5)], fill="#FFFFFF", opacity=0.85)
    gx, gy = (ax + lx + rx) / 3, (ay + ly + ry) / 3
    pts = [(ax, ay), ((ax + rx) / 2, (ay + ry) / 2), (rx, ry), ((lx + rx) / 2, ly), (lx, ly), ((ax + lx) / 2, (ay + ly) / 2)]
    for k, c in enumerate(["#99CD61", "#6CC0B0", "#4D9DE0", "#9E7BD8", "#E8686A", "#F4A35E"]):
        ic.poly([(gx, gy), pts[k], pts[(k + 1) % 6]], fill=c)
    ic.poly([(ax, ay), (rx, ry), (lx, ly)], fill="none", stroke="#FFFFFF", stroke_width=4, stroke_linejoin="round")


@soft("minecraft")
def minecraft(ic):
    tile(ic, "#82BCEB", "#3874AA")
    for x, y, w in ((26, 46, 40), (180, 30, 34)):
        ic.rect(x, y, w, 10, rx=3, fill="#fff", opacity=0.6)
        ic.rect(x + 8, y - 8, w - 18, 8, rx=3, fill="#fff", opacity=0.6)
    soft_shadow(ic, 128, 214, 92, 12)
    _block(ic, 44, 82, 84, 92)


@soft("retroarch")
def retroarch(ic):
    tile(ic, "#5E4590", "#271746")
    soft_shadow(ic, 128, 218, 78, 11)
    ic.path("M76 22H180a14 14 0 0 1 14 14V172a42 42 0 0 1-42 42H76a14 14 0 0 1-14-14V36a14 14 0 0 1 14-14Z",
            fill=two(ic, "#EEEBE4", "#C9C4BA"))
    ic.path("M82 36H174a8 8 0 0 1 8 8V110a20 20 0 0 1-20 20H82a8 8 0 0 1-8-8V44a8 8 0 0 1 8-8Z", fill="#3C3848")
    ic.rect(95, 46, 74, 68, rx=6, fill="#1A2448")
    d = "".join(f"M{i} {j}h1v1h-1z" for j, row in enumerate(_INVADER) for i, c in enumerate(row) if c == "X")
    ic.path(d, fill="#EEF0FF", transform="translate(104.5 60) scale(5)")
    ic.circle(85, 70, 4, fill="#E8463C")
    bar(ic, 76, 140, 58, 9, fill="#3B3360")
    # the controls
    ic.path("M89 158h14v13h13v14h-13v13h-14v-13h-13v-14h13z", fill="#2E2B36", stroke="#2E2B36", stroke_width=3,
            stroke_linejoin="round")
    for x, y in ((170, 166), (148, 180)):
        ic.circle(x, y, 11, fill=two(ic, "#D2558F", "#9A2862"))
    for x in (108, 130):
        ic.rect(x, 200, 16, 6, rx=3, fill="#6A6672", transform=f"rotate(-24 {x + 8} 203)")


_INVADER = ["..X.....X..",
            "...X...X...",
            "..XXXXXXX..",
            ".XX.XXX.XX.",
            "XXXXXXXXXXX",
            "X.XXXXXXX.X",
            "X.X.....X.X",
            "...XX.XX..."]


_DOLPHIN = ("M58 150C58 98 86 56 132 48C166 42 194 58 204 86C208 98 214 106 224 114C216 120 204 116 196 110"
            "C190 106 184 102 178 98C160 82 134 78 112 88C92 98 78 122 72 152Z")


@soft("dolphin-emu")
def dolphin(ic):
    tile(ic, "#1F4478", "#0A1A36")
    soft_shadow(ic, 128, 214, 80, 11)
    ic.circle(132, 148, 60, fill=two(ic, "#E8ECF0", "#AEB6C1"))
    ic.path("M132 148L92 104A60 60 0 0 1 132 88Z", fill="#FF8AD8", opacity=0.22)
    ic.path("M132 148L172 192A60 60 0 0 1 132 208Z", fill="#7FE3FF", opacity=0.3)
    ic.circle(132, 148, 18, fill="#F4F6F8")
    ic.circle(132, 148, 7, fill="#1F4478")
    fin = "#1E66B8"
    ic.path("M62 146C56 156 44 162 34 164C44 172 58 170 66 162C72 170 82 176 92 178C88 166 80 156 72 146Z", fill=fin)
    ic.path("M108 58C114 38 130 26 146 24C138 34 136 44 140 52Z", fill=fin)
    ic.path(_DOLPHIN, fill=two(ic, "#62BDF6", "#1E62B4"))
    ic.path("M168 92C168 104 162 114 152 122C164 118 174 108 180 98Z", fill=fin)
    ic.circle(188, 86, 4, fill="#0B1D38")


@soft("pcsx2")
def pcsx2(ic):
    tile(ic, "#5B636E", "#25292F")
    soft_shadow(ic, 124, 204, 104, 12)
    dx, dy = 34, -40
    x0, x1, y0, y1 = 22, 196, 136, 190
    ic.poly([(x0, y0), (x1, y0), (x1 + dx, y0 + dy), (x0 + dx, y0 + dy)], fill="#3150BE", stroke="#3150BE",
            stroke_width=4, stroke_linejoin="round")
    ic.poly([(x1, y0), (x1 + dx, y0 + dy), (x1 + dx, y1 + dy), (x1, y1)], fill="#121D62", stroke="#121D62",
            stroke_width=4, stroke_linejoin="round")
    ic.rect(x0, y0, x1 - x0, y1 - y0, rx=3, fill=two(ic, "#2440A8", "#14246E"))
    ic.rect(x0 + 10, y0 + 12, 118, 10, rx=5, fill="#0A1240")
    bar(ic, x0 + 10, y0 + 32, 54, 9, fill="#E6ECFF")
    bar(ic, x0 + 74, y0 + 33, 50, 6, fill="#5FA8FF")
    for k in range(2):
        ic.circle(x0 + 146 + k * 18, y0 + 20, 6, fill="#0A1240")
        ic.circle(x0 + 146 + k * 18, y0 + 34, 2.5, fill=("#5FFF9E", "#5FA8FF")[k])
    m = f"matrix(1 0 {dx / 80:.3f} {dy / 80:.3f} 118 112)"
    with ic.g(transform=m):
        ic.circle(0, 0, 54, fill=two(ic, "#5A8EF0", "#1C3EA8"))
        ic.circle(0, 0, 18, fill="#D8E2F2")
        ic.circle(0, 0, 7, fill="#0A1240")


@soft("ppsspp")
def ppsspp(ic):
    tile(ic, "#E39A3B", "#8E500E")
    soft_shadow(ic, 128, 188, 112, 12)
    ic.rect(86, 68, 30, 14, rx=6, fill="#1A1B1F")
    ic.rect(140, 68, 30, 14, rx=6, fill="#1A1B1F")
    ic.path("M64 76H192a48 48 0 0 1 0 96H64a48 48 0 0 1 0-96Z", fill=two(ic, "#3A3D44", "#121316"))
    ic.rect(68, 88, 120, 70, rx=6, fill="#0A2546")
    ic.circle(128, 114, 22, fill=two(ic, "#6CC0FA", "#1A6AC8"))
    ic.rect(108, 105, 40, 18, rx=9, fill="#FFFFFF")
    ic.rect(119, 109, 18, 10, rx=2, fill="#1A6AC8")
    bar(ic, 100, 142, 56, 8, fill="#E9F4FF")
    ic.path("M35 106h10v6h6v10h-6v6h-10v-6h-6v-10h6z", fill="#4A4D55", stroke="#4A4D55", stroke_width=3,
            stroke_linejoin="round")
    ic.circle(42, 152, 7, fill="#55585F")
    for ox, oy in ((0, -12), (12, 0), (0, 12), (-12, 0)):
        ic.circle(216 + ox, 120 + oy, 6, fill="#4A4D55")


@soft("ryujinx")
def ryujinx(ic):
    tile(ic, "#3E3342", "#151018")
    soft_shadow(ic, 128, 212, 100, 12)
    ic.path("M60 48V176H44a20 20 0 0 1-20-20V68a20 20 0 0 1 20-20Z", fill=two(ic, "#5ED6F0", "#1E92B2"))
    ic.path("M196 48H212a20 20 0 0 1 20 20V156a20 20 0 0 1-20 20H196Z", fill=two(ic, "#FF7A70", "#C8362E"))
    for cx, cy in ((42, 84), (214, 128)):
        ic.circle(cx, cy, 9, fill="#26282E")
    for ox, oy in ((0, -9), (9, 0), (0, 9), (-9, 0)):
        ic.circle(214 + ox, 84 + oy, 3.6, fill="#26282E")
    ic.rect(60, 46, 136, 132, rx=8, fill="#26282E")
    ic.rect(68, 54, 120, 104, rx=5, fill="#141A28")
    t = "translate(91 64) scale(1.06)"
    ic.path("M0 24L6 19L20 17L34 10L42 9L66 0L50 15L70 13L54 22L58 28L66 36L56 38L62 48L52 48L54 58L42 52"
            "L38 44L30 40L10 40L6 36L24 32L2 28Z", fill=two(ic, "#8AEEFF", "#26A6D0"), transform=t)
    ic.path("M42 9L66 0L50 15L70 13L54 22L48 18ZM56 26L66 36L56 38L62 48L52 48L54 58L46 54L50 42L52 32Z",
            fill="#F0473E", transform=t)
    ic.path("M8 32L24 30C32 31 38 34 44 40", fill="none", stroke="#0E4A62", stroke_width=2.6,
            stroke_linecap="round", transform=t)
    ic.circle(91 + 8 * 1.06, 64 + 22 * 1.06, 2.6, fill="#0E3A4A")
    ic.rect(44, 150, 168, 58, rx=8, fill=two(ic, "#3E4048", "#1A1B20"))
    ic.path("M120 180a8 8 0 0 1 8-8v16a8 8 0 0 1-8-8z", fill="#3BC6E0")
    ic.path("M136 180a8 8 0 0 1-8 8v-16a8 8 0 0 1 8 8z", fill="#FF5F55")


@soft("itch")
def itch(ic):
    tile(ic, "#2A5556", "#0E2526")
    soft_shadow(ic, 128, 214, 82, 11)
    ic.path("M64 30H176L200 54V196a12 12 0 0 1-12 12H68a12 12 0 0 1-12-12V38a8 8 0 0 1 8-8Z",
            fill=two(ic, "#FF6A66", "#C8343A"))
    for k in range(3):
        bar(ic, 70, 40 + k * 9, 100, 4, fill="#A82430", opacity=0.6)
    ic.rect(70, 74, 116, 112, rx=10, fill="#E2454A")
    mx, my, mw = 98, 86, 60
    ic.rect(mx, my, mw, 13, rx=4, fill="#FFFFFF")
    for k in range(5):
        ic.path(f"M{mx + k * 12} {my + 10}h12v3a6 6 0 0 1-12 0z", fill="#FFFFFF")
    ic.path(f"M{mx + 3} {my + 23}h{mw - 6}v24a4 4 0 0 1-4 4h-14a8 8 0 0 0-16 0h-14a4 4 0 0 1-4-4z", fill="#FFFFFF")
    for ex in (mx + 21, mx + 39):
        ic.circle(ex, my + 34, 4.5, fill="#E2454A")
    bar(ic, 100, 156, 56, 11, fill="#FFFFFF")
    ic.path("M120 194l8 7 8-7z", fill="#A82430")


@soft("0ad")
def zeroad(ic):
    tile(ic, "#3A6C8A", "#14303F")
    soft_shadow(ic, 132, 214, 86, 11)
    ic.path("M56 86C64 40 112 22 160 30C196 36 222 62 224 100L206 102C202 74 184 58 158 54C120 48 86 62 76 92Z",
            fill=two(ic, "#E2483A", "#94201A"))
    ic.rect(129, 60, 14, 28, rx=4, fill="#B88433")
    ic.path("M64 112C66 84 96 70 132 70C172 70 196 96 196 132C196 156 200 176 210 196C192 200 162 196 146 186"
            "C140 170 130 164 118 166C112 180 106 196 82 204C76 190 72 170 70 150C64 146 60 130 64 112Z",
            fill=two(ic, "#E8B865", "#A86C2C"))
    ic.path("M66 110C92 102 160 102 194 118", fill="none", stroke="#8A5420", stroke_width=4, stroke_linecap="round")
    ic.path("M63 122C76 116 96 116 110 122C104 130 88 134 66 132Z", fill="#2A1606")
    ic.path("M67 131L83 131L79 168L73 168Z", fill="#2A1606", stroke="#2A1606", stroke_width=2,
            stroke_linejoin="round")


@soft("supertuxkart")
def supertuxkart(ic):
    tile(ic, "#5E9C3F", "#244E16")
    soft_shadow(ic, 128, 212, 104, 12)
    ic.rect(41, 104, 10, 40, fill="#2A2C30")
    ic.rect(20, 96, 50, 14, rx=5, fill="#2E3036")
    ic.ellipse(120, 126, 32, 34, fill="#1E2024")
    ic.ellipse(132, 132, 18, 24, fill="#F4F2EE")
    ic.circle(122, 76, 29, fill="#1E2024")
    ic.path("M112 80C112 66 120 60 130 60C142 60 150 70 150 82C150 96 140 102 130 102C120 102 112 94 112 80Z",
            fill="#F7F5F0")
    for ex in (125, 141):
        ic.ellipse(ex, 76, 3.6, 4.6, fill="#111")
    ic.path("M122 88C130 84 148 84 156 90C150 96 136 98 124 94Z", fill=two(ic, "#FFC23A", "#E88A18"))
    ic.path("M146 116C156 112 166 114 172 120L168 126C160 122 152 122 146 124Z", fill="#1E2024")
    ic.line(176, 124, 186, 152, stroke="#2A2C30", stroke_width=5, stroke_linecap="round")
    ic.ellipse(174, 122, 4, 13, fill="none", stroke="#1A1B1F", stroke_width=5, transform="rotate(20 174 122)")
    ic.path("M30 184V150Q30 138 42 138H96L106 150H150Q174 150 200 158L226 166Q234 170 230 180L214 186H30Z",
            fill=two(ic, "#FF6A3A", "#C8320E"))
    ic.circle(124, 166, 14, fill="#FFFFFF")
    ic.path("M120 158l6-4h4v24h-6v-15l-3 2z", fill="#1E1F24")
    for x, y, r in ((72, 186, 24), (194, 188, 21)):
        ic.circle(x, y, r, fill="#1A1A1D")
        ic.circle(x, y, r * 0.48, fill=two(ic, "#AEB4BB", "#8D949C"))


@soft("wesnoth")
def wesnoth(ic):
    tile(ic, "#5C4428", "#1F160B")
    soft_shadow(ic, 128, 218, 80, 11)
    ic.path("M120 58H136L135 206L128 222L121 206Z", fill=two(ic, "#D4D8DD", "#8D949C"))
    ic.rect(122, 24, 12, 30, rx=4, fill="#5A2E14")
    ic.circle(128, 20, 8, fill="#D9A84A")
    ic.path("M88 52C100 56 112 56 128 54C144 56 156 56 168 52C170 58 166 62 160 62H96C90 62 86 58 88 52Z",
            fill="#D9A84A")
    cx, cy = 128, 134
    ic.circle(cx, cy, 74, fill=two(ic, "#AEB4BB", "#6E757E"))
    ic.circle(cx, cy, 64, fill=two(ic, "#A87444", "#6A3E1C"))
    ic.circle(cx, cy, 47, fill="#E2B45E")
    ic.circle(cx, cy, 44, fill=two(ic, "#B83A2A", "#7A1C12"))
    ic.path("M100 150L95 114L113 130L128 102L143 130L161 114L156 150Z", fill=two(ic, "#F2CB72", "#C8953E"),
            stroke="#E2B45E", stroke_width=3, stroke_linejoin="round")
    ic.rect(98, 145, 60, 12, rx=3, fill="#C8953E")
    for x, y in ((95, 111), (128, 99), (161, 111)):
        ic.circle(x, y, 4.5, fill="#F2CB72")
    ic.path("M40 186L64 182L64 208L48 204L54 196Z", fill="#B9A882")
    ic.path("M216 186L192 182L192 208L208 204L202 196Z", fill="#B9A882")
    ic.path("M60 180C100 188 156 188 196 180V204C156 212 100 212 60 204Z", fill=two(ic, "#F7F2E7", "#DDD4C2"))
    bar(ic, 92, 191, 72, 9, fill="#4A2A14")
