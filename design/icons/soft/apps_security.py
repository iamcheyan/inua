"""The soft drawings of the security and sync batch
(drawings/apps_security.py): KeePassXC, Bitwarden, Passwords and Keys,
Nextcloud, Syncthing, Transmission, qBittorrent, FileZilla, Proton VPN,
OneKey, TradingView and Fcitx. The same objects, about half the detail,
no text."""

from lib import bar, polar, soft, soft_shadow, tile, two

BRASS = ("#E2B45E", "#B88433")
STEEL = ("#AEB4BB", "#8D949C")
CREAM = ("#FFFDF7", "#F1EADB")


def _shield(cx, top, w, h):
    """A heater shield, its top edge at top, w wide, h tall."""
    hw = w / 2
    return (f"M{cx} {top}L{cx + hw} {top + h * 0.1}V{top + h * 0.45}"
            f"C{cx + hw} {top + h * 0.75} {cx + hw * 0.45} {top + h * 0.9} {cx} {top + h}"
            f"C{cx - hw * 0.45} {top + h * 0.9} {cx - hw} {top + h * 0.75} {cx - hw} {top + h * 0.45}"
            f"V{top + h * 0.1}Z")


def _zhong(ic, x, y, size, colour, width):
    """中, the input method's mark, as two strokes on a unit square."""
    ic.path("M.18 .28H.82V.66H.18Z M.5 .04V.98", fill="none", stroke=colour, stroke_width=width / size,
            stroke_linecap="round", stroke_linejoin="round", transform=f"translate({x} {y}) scale({size})")


@soft("keepassxc")
def keepassxc(ic):
    tile(ic, "#41484E", "#16191C")
    soft_shadow(ic, 128, 216, 100, 12)
    for x in (52, 184):
        ic.rect(x, 198, 20, 14, rx=5, fill="#141618")
    ic.rect(32, 32, 192, 174, rx=22, fill=two(ic, "#56605A", "#262C29"))
    ic.rect(44, 44, 168, 150, rx=14, fill="#0E1110")
    for y in (64, 158):
        ic.rect(36, y, 14, 24, rx=5, fill=two(ic, *STEEL))
    ic.rect(46, 46, 162, 144, rx=12, fill=two(ic, "#6CBD4C", "#3A8030"))
    # the dial
    dx, dy = 102, 108
    ic.circle(dx, dy, 38, fill=two(ic, "#D6DBE0", "#8D949C"))
    ic.circle(dx, dy, 32, fill="#1E2023")
    for k in range(8):
        x1, y1 = polar(dx, dy, 29, k * 45)
        x2, y2 = polar(dx, dy, 21, k * 45)
        ic.line(x1, y1, x2, y2, stroke="#F1F1EF", stroke_width=3.5, stroke_linecap="round")
    ic.circle(dx, dy, 12, fill=two(ic, "#E9ECEF", "#9AA1A9"))
    ic.path(f"M{dx} {dy - 38}l-6 -9h12z", fill="#F2C45C")
    # the handle: three spokes
    hx, hy = 172, 106
    for a in (0, 120, 240):
        ex, ey = polar(hx, hy, 22, a + 30)
        ic.line(hx, hy, ex, ey, stroke="#B7BDC4", stroke_width=7, stroke_linecap="round")
        ic.circle(ex, ey, 7, fill=two(ic, "#E9ECEF", "#9AA1A9"))
    ic.circle(hx, hy, 11, fill=two(ic, "#E9ECEF", "#9AA1A9"))
    # the keyhole plate and the maker's plate
    ic.rect(154, 140, 36, 34, rx=7, fill=two(ic, *BRASS))
    ic.circle(172, 152, 5, fill="#1A1208")
    ic.path("M169.5 153 l-2.5 12 h10 l-2.5 -12z", fill="#1A1208")
    ic.rect(64, 158, 78, 20, rx=6, fill=two(ic, *BRASS))
    bar(ic, 76, 164.5, 54, 7, fill="#7A5418")


@soft("bitwarden")
def bitwarden(ic):
    tile(ic, "#3F78D6", "#183A80")
    soft_shadow(ic, 128, 218, 92, 12)
    ic.rect(50, 30, 156, 186, rx=24, fill=two(ic, "#2C3A5C", "#121A30"))
    outer = _shield(128, 46, 120, 140)
    ic.path(outer, fill=two(ic, "#E4E8EC", "#9AA1A9"))
    ic.path(_shield(128, 56, 102, 120), fill=two(ic, "#3C8CFF", "#1450C0"))
    mk = _shield(128, 72, 64, 80)
    ic.path(mk, fill="none", stroke="#F7F9FC", stroke_width=9, stroke_linejoin="round")
    ic.path("M128 76 L156 83.5 V108 C156 125 145 136 128 146 Z", fill="#F7F9FC")
    bar(ic, 96, 196, 64, 6, fill="#D8C27A", opacity=0.8)


def _key(ic, fill, length, bow):
    """A key in its own frame: the ring's hole at the origin, the blade down +y."""
    ic.path(f"M-6 24H6V{30 + length * 0.2}h6v9h-6v{length * 0.2}h8v9h-8V{24 + length}l-6 7l-6 -7Z", fill=fill)
    if bow == "round":
        ic.circle(0, 12, 17, fill=fill)
    else:
        ic.rect(-16, -3, 32, 32, rx=11, fill="#26282C")
    ic.circle(0, 0, 5, fill="#2A2018")


def _tag(ic, tint):
    """A paper tag: its hole at the origin, hanging down +y."""
    ic.path("M-10 -8H10L24 6V80a4 4 0 0 1 -4 4H-20a4 4 0 0 1 -4 -4V6Z", fill=two(ic, *CREAM))
    ic.path("M-24 62H24V80a4 4 0 0 1 -4 4H-20a4 4 0 0 1 -4 -4Z", fill=tint)
    bar(ic, -14, 26, 28, 8, fill="#2E3A55")
    bar(ic, -10, 42, 20, 5, fill="#B9B4AA")
    ic.circle(0, 0, 4, fill="#2A2018")


@soft("seahorse")
def seahorse(ic):
    tile(ic, "#3E7E8A", "#173D46")
    soft_shadow(ic, 128, 216, 84, 10)
    rx_, ry_, rr = 124, 66, 22
    ic.rect(102, 14, 44, 24, rx=8, fill=two(ic, *BRASS))
    for a, tint, swing in ((118, "#2463AE", 36), (242, "#C8372D", -36)):
        tx, ty = polar(rx_, ry_, rr + 14, a)
        hx, hy = polar(rx_, ry_, rr, a)
        ic.line(hx, hy, tx, ty, stroke="#E8DCC0", stroke_width=3)
        with ic.g(transform=f"translate({tx:.1f} {ty:.1f}) rotate({a - 180 + swing})"):
            _tag(ic, tint)
    for a, fill, length, bow, swing in ((200, two(ic, "#E4E8EC", "#9AA1A9"), 66, "round", 8),
                                        (160, two(ic, "#D6DBE0", "#8D949C"), 56, "fob", -6),
                                        (180, two(ic, "#E9A878", "#A85E2E"), 76, "round", 0)):
        hx, hy = polar(rx_, ry_, rr, a)
        with ic.g(transform=f"translate({hx:.1f} {hy:.1f}) rotate({a - 180 + swing})"):
            _key(ic, fill, length, bow)
    ic.circle(rx_, ry_, rr, fill="none", stroke=two(ic, "#D6DBE0", "#8D949C"), stroke_width=8)
    ic.path("M124 30 V40 a5 5 0 0 0 10 0 V36", fill="none", stroke="#C8973F", stroke_width=6, stroke_linecap="round")


@soft("nextcloud")
def nextcloud(ic):
    tile(ic, "#3B4A5A", "#18212B")
    soft_shadow(ic, 128, 208, 104, 12)
    ic.rect(22, 58, 212, 140, rx=24, fill=two(ic, "#1C98E0", "#0466A4"))
    ic.rect(34, 70, 188, 116, rx=14, fill="none", stroke="#F6FAFD", stroke_width=5)
    cx, cy = 128, 110
    ic.circle(cx, cy, 22, fill="none", stroke="#F6FAFD", stroke_width=11)
    for dx in (-46, 46):
        ic.circle(cx + dx, cy, 11, fill="none", stroke="#F6FAFD", stroke_width=8)
    bar(ic, 74, 152, 108, 16, fill="#F6FAFD")


@soft("syncthing")
def syncthing(ic):
    tile(ic, "#2C7FA6", "#0F3A52")
    soft_shadow(ic, 128, 216, 86, 11)
    cx, cy, r = 128, 102, 70
    ic.path("M60 196 v10 a68 12 0 0 0 136 0 v-10z", fill="#6A3E1E")
    ic.ellipse(128, 196, 68, 12, fill=two(ic, "#C99260", "#9A6434"))
    ic.path("M120 168 h16 l4 26 h-24z", fill=two(ic, *BRASS))
    ic.circle(cx, cy, r, fill="none", stroke=two(ic, *BRASS), stroke_width=14)
    hx, hy = 138, 112
    nodes = [polar(cx, cy, r, a) for a in (40, 156, 282)]
    for nx, ny in nodes:
        ic.line(hx, hy, nx, ny, stroke="#B7BDC4", stroke_width=6, stroke_linecap="round")
    for nx, ny in nodes:
        ic.circle(nx, ny, 17, fill=two(ic, "#5CC4F0", "#1470A8"))
    ic.circle(hx, hy, 11, fill=two(ic, *BRASS))


@soft("transmission")
def transmission(ic):
    tile(ic, "#4C5866", "#1C232B")
    soft_shadow(ic, 124, 218, 104, 12)
    with ic.g(transform="translate(128 120) scale(1.07) translate(-128 -120)"):
        tip = (204, 30)
        for r, op in ((10, 0.8), (19, 0.45)):
            for a1, a2 in ((50, 130), (230, 310)):
                x1, y1 = polar(tip[0], tip[1], r, a1)
                x2, y2 = polar(tip[0], tip[1], r, a2)
                ic.path(f"M{x1:.1f} {y1:.1f}A{r} {r} 0 0 1 {x2:.1f} {y2:.1f}", fill="none", stroke="#FFD9C8",
                        stroke_opacity=op, stroke_width=4, stroke_linecap="round")
        ic.line(204, 92, 204, 30, stroke="#B7BDC4", stroke_width=5, stroke_linecap="round")
        ic.circle(204, 28, 5, fill="#D6DBE0")
        ic.path("M62 92 V80 a10 10 0 0 1 10 -10 h56 a10 10 0 0 1 10 10 V92", fill="none", stroke="#2E3236",
                stroke_width=9, stroke_linecap="round")
        ic.rect(28, 90, 196, 116, rx=20, fill=two(ic, "#EC5844", "#B02818"))
        ic.rect(38, 106, 176, 90, rx=10, fill=two(ic, "#F7F2E7", "#DED6C6"))
        # the tuning dial
        dx, dy = 80, 150
        ic.circle(dx, dy, 32, fill="#FFFDF7", stroke="#2A2C30", stroke_width=3)
        for k in range(7):
            x1, y1 = polar(dx, dy, 27, -120 + k * 40)
            x2, y2 = polar(dx, dy, 20, -120 + k * 40)
            ic.line(x1, y1, x2, y2, stroke="#2A2C30", stroke_width=3, stroke_linecap="round")
        ic.circle(dx, dy, 11, fill=two(ic, "#4A4E55", "#1A1B1E"))
        ic.line(dx, dy, *polar(dx, dy, 28, 28), stroke="#C8372D", stroke_width=3.5, stroke_linecap="round")
        # the meter
        mx, my, mw, mh = 124, 114, 80, 40
        ic.rect(mx - 3, my - 3, mw + 6, mh + 6, rx=7, fill="#2A2C30")
        ic.rect(mx, my, mw, mh, rx=4, fill="#FFF2CC")
        pc = (mx + mw / 2, my + mh + 14)
        ic.path(f"M{polar(*pc, 42, -40)[0]:.1f} {polar(*pc, 42, -40)[1]:.1f}"
                f"A42 42 0 0 1 {polar(*pc, 42, 40)[0]:.1f} {polar(*pc, 42, 40)[1]:.1f}",
                fill="none", stroke="#2A2C30", stroke_width=3, stroke_linecap="round")
        ic.line(pc[0], pc[1] - 8, *polar(*pc, 46, 22), stroke="#1E2024", stroke_width=2.5, stroke_linecap="round")
        # knobs and the lamp
        for kx in (136, 164):
            ic.circle(kx, 176, 9, fill=two(ic, "#D6DBE0", "#7A818A"))
        ic.circle(196, 172, 7, fill="#FF8A4A")
        bar(ic, 96, 96, 60, 6, fill="#FFE6DE", opacity=0.8)


@soft("qbittorrent")
def qbittorrent(ic):
    tile(ic, "#3D76B5", "#1A3D69")
    soft_shadow(ic, 130, 212, 104, 12)
    F = (36, 98, 168, 206)
    ox, oy = 50, -34
    ic.poly([(F[0], F[1]), (F[2], F[1]), (F[2] + ox, F[1] + oy), (F[0] + ox, F[1] + oy)], fill="#F2D394",
            stroke="#F2D394", stroke_width=4, stroke_linejoin="round")
    ic.poly([(F[2], F[1]), (F[2] + ox, F[1] + oy), (F[2] + ox, F[3] + oy), (F[2], F[3])], fill="#A87A36",
            stroke="#A87A36", stroke_width=4, stroke_linejoin="round")
    ic.rect(F[0], F[1], F[2] - F[0], F[3] - F[1], rx=3, fill=two(ic, "#E8C27A", "#C99A4E"))
    # twine, both ways
    tw = dict(stroke="#F4EBD6", stroke_width=4, stroke_linecap="round")
    tx = 104
    ic.line(tx, F[1], tx, F[3], **tw)
    ic.line(tx + ox, F[1] + oy, tx, F[1], **tw)
    ic.line(F[2] + ox / 2, F[1] + oy / 2, F[2] + ox / 2, F[3] + oy / 2, **tw)
    ic.line(F[0] + ox / 2, F[1] + oy / 2, F[2] + ox / 2, F[1] + oy / 2, **tw)
    # the label
    ic.rect(116, 114, 44, 34, rx=4, fill=two(ic, "#FFFFFF", "#ECE8DF"))
    bar(ic, 122, 122, 30, 7, fill="#2E3A55")
    bar(ic, 122, 134, 22, 6, fill="#B9B4AA")
    ic.rect(116, 156, 44, 38, rx=4, fill=two(ic, "#FFFFFF", "#ECE8DF"))
    for k in range(6):
        ic.rect(122 + k * 5.8, 162, 3 if k % 2 else 2, 22, fill="#2A2C30")
    # the stamp: the globe in a ring
    sx, sy = 70, 152
    ink = "#1F5FB0"
    ic.circle(sx, sy, 27, fill="none", stroke=ink, stroke_width=4)
    ic.circle(sx, sy, 18, fill=ink)
    ic.ellipse(sx, sy, 8, 18, fill="none", stroke="#E3BA6C", stroke_width=2.5)
    ic.line(sx - 18, sy, sx + 18, sy, stroke="#E3BA6C", stroke_width=2.5)


@soft("filezilla")
def filezilla(ic):
    tile(ic, "#3E7480", "#173C45")
    soft_shadow(ic, 128, 206, 108, 11)
    red = two(ic, "#EE5236", "#B8281A")
    ic.rect(28, 166, 196, 16, rx=5, fill="#1E2024")
    ic.rect(28, 58, 140, 112, rx=10, fill=two(ic, "#F7F2E7", "#DAD2C0"))
    # the mark: F and z, white on red
    ic.rect(40, 70, 64, 64, rx=14, fill=red)
    ic.path("M52 82h22v9h-12v6h10v9h-10v14h-10z", fill="#FFF6EC")
    ic.path("M76 96h20v7l-10 10h10v7h-21v-7l10-10h-9z", fill="#FFF6EC")
    bar(ic, 114, 82, 44, 11, fill="#B42A1F")
    bar(ic, 114, 100, 34, 6, fill="#8C887F")
    ic.rect(114, 124, 46, 4, rx=2, fill="#B42A1F", opacity=0.7)
    # the cab
    ic.path("M170 92 h26 a12 12 0 0 1 10.6 6.4 l15.4 32.6 a12 12 0 0 1 1 5 v34 h-53z", fill=red)
    ic.path("M176 100 h18 a6 6 0 0 1 5.4 3.4 l12 25.6 h-35.4z", fill="#1E2C36")
    ic.rect(212, 150, 12, 10, rx=3, fill="#FFD27A")
    for x in (62, 104, 194):
        ic.circle(x, 182, 20, fill="#151618")
        ic.circle(x, 182, 10, fill=two(ic, "#E4E8EC", "#8D949C"))


@soft("proton-vpn")
def proton_vpn(ic):
    tile(ic, "#4F3E8E", "#1E1544")
    soft_shadow(ic, 132, 206, 102, 12)
    A, L, R = (110, 34), (34, 190), (186, 190)
    ox, oy = 34, -12
    ic.poly([A, (A[0] + ox, A[1] + oy), (R[0] + ox, R[1] + oy), R], fill=two(ic, "#4B2FB8", "#24137A"),
            stroke="#24137A", stroke_width=4, stroke_linejoin="round")
    ic.poly([A, L, R], fill=ic.lin([(0, "#7FE8DA"), (0.45, "#6D8CFF"), (1, "#4A2CC0")], 0.2, 0, 0.6, 1),
            stroke="#6D7CFF", stroke_width=4, stroke_linejoin="round")
    ic.poly([(110, 80), (70, 164), (150, 164)], fill="none", stroke="#F2EEFF", stroke_width=9,
            stroke_linejoin="round")
    ic.poly([(110, 112), (90, 152), (130, 152)], fill="#F2EEFF", stroke="#F2EEFF", stroke_width=3,
            stroke_linejoin="round")


@soft("onekey")
def onekey(ic):
    tile(ic, "#2E8A52", "#0F3F25")
    soft_shadow(ic, 128, 216, 76, 11)
    ic.path("M128 206 C128 226 160 222 184 212 S206 200 212 196", fill="none", stroke="#E9ECEF", stroke_width=9,
            stroke_linecap="round")
    with ic.g(transform="rotate(56 212 196)"):
        ic.rect(205, 180, 14, 18, rx=4, fill="#E9ECEF")
        ic.rect(208, 171, 8, 10, rx=2, fill=two(ic, *STEEL))
    ic.rect(66, 28, 124, 174, rx=28, fill=two(ic, "#33373B", "#121315"))
    ic.circle(172, 44, 5.5, fill="#050607")
    ic.rect(82, 54, 92, 92, rx=10, fill="#0B0D0E")
    # the mark, a 1 on green, what to sign, and the button to confirm it
    ic.rect(110, 62, 36, 36, rx=11, fill="#00B812")
    ic.path("M124 72l8-4h4v24h-8v-14l-4 2z", fill="#0B0D0E")
    bar(ic, 104, 106, 48, 7, fill="#E9ECEF")
    bar(ic, 96, 118, 64, 7, fill="#9AA1A9")
    ic.rect(94, 130, 68, 10, rx=5, fill="#00B812")
    # the pad and two keys
    ic.circle(128, 172, 18, fill=two(ic, "#3A3D42", "#1A1B1E"))
    ic.circle(128, 172, 7, fill="#1A1B1E", stroke="#00B812", stroke_width=2.5)
    for x, col in ((90, "#E05A4A"), (166, "#00D21A")):
        ic.circle(x, 172, 9, fill=two(ic, "#3A3D42", "#1A1B1E"))
        ic.circle(x, 172, 3.5, fill=col)


@soft("tradingview")
def tradingview(ic):
    tile(ic, "#2F3A50", "#10151F")
    soft_shadow(ic, 128, 216, 80, 10)
    ic.path("M112 170 h32 l8 34 h-48z", fill=two(ic, "#C9CED4", "#9AA1A9"))
    ic.rect(78, 200, 100, 12, rx=6, fill=two(ic, "#E4E8EC", "#9AA1A9"))
    ic.rect(22, 34, 212, 146, rx=16, fill=two(ic, "#EEF0F2", "#B4BAC1"))
    ic.rect(30, 42, 196, 112, rx=7, fill="#131722")
    # candles and the moving average
    candles = [(130, 120, 112, 136), (120, 126, 116, 132), (126, 110, 106, 128), (110, 114, 102, 120),
               (114, 98, 92, 118), (98, 104, 94, 110), (104, 90, 84, 108), (90, 96, 86, 102),
               (96, 80, 72, 100), (86, 70, 62, 90), (76, 62, 56, 80)]
    for i, (o, c, h, l) in enumerate(candles):
        x = 46 + i * 14.5
        col = "#26A69A" if c < o else "#EF5350"
        ic.line(x, h, x, l, stroke=col, stroke_width=2.5, stroke_linecap="round")
        ic.rect(x - 4.5, min(o, c), 9, max(abs(o - c), 3), rx=1.5, fill=col)
    ic.path("M42 132 C70 126 90 114 112 110 S150 94 170 84 S192 70 196 66", fill="none", stroke="#2962FF",
            stroke_width=3.5, stroke_linecap="round")
    bar(ic, 40, 52, 40, 7, fill="#D1D4DC", opacity=0.7)
    ic.rect(200, 58, 26, 11, rx=3, fill="#26A69A")
    # the mark on the chin
    with ic.g(transform="translate(128 167)"):
        ic.path("M-24 -6 h14 v12 h-6 v-6 h-8z", fill="#131722")
        ic.circle(-1.5, -2.5, 3.5, fill="#131722")
        ic.path("M6 6 l7 -12 h8 l-7 12z", fill="#131722")


@soft("fcitx")
def fcitx(ic):
    tile(ic, "#565C8C", "#23264A")
    soft_shadow(ic, 128, 216, 108, 11)
    # the card of candidates, the first chosen
    ic.rect(42, 30, 172, 64, rx=12, fill=two(ic, *CREAM))
    bar(ic, 54, 40, 62, 10, fill="#2E3A55")
    ic.rect(122, 37, 3, 16, rx=1.5, fill="#2463AE")
    ic.rect(50, 58, 66, 28, rx=8, fill="#2463AE")
    _zhong(ic, 70, 61, 22, "#fff", 4)
    for x in (128, 168):
        bar(ic, x, 68, 30, 8, fill="#8C887F")
    # the keyboard
    ic.rect(18, 100, 220, 108, rx=18, fill=two(ic, "#D9DCE3", "#9DA2AE"))
    ic.rect(26, 108, 204, 92, rx=10, fill="#3A3D48")
    kw, kh, gap = 18, 19, 2.2
    cap = two(ic, "#FFFFFF", "#E2E4EA")
    for r, n in enumerate((10, 9, 7)):
        y = 112 + r * (kh + 2.6)
        for i in range(n):
            ic.rect(30 + r * 7 + i * (kw + gap), y, kw, kh, rx=5, fill=cap)
    y = 112 + 3 * (kh + 2.6)
    for x, w, fill in ((30, 30, "#2463AE"), (64, 128, cap), (196, 30, cap)):
        ic.rect(x, y, w, kh, rx=5, fill=fill)
    _zhong(ic, 38, y + 3, 13, "#fff", 2.6)
