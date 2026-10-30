"""Soft drawings of inua's tools, second batch: Pass, GPG, Tailscale,
Remote, MobileLink, System Monitor, Disk Usage, Stocks. The same objects
as drawings/inua_b.py, about half the detail, no text."""

import math

from lib import bar, mark, polar, soft, soft_shadow, tile, two

ACCENT, WARN, OK = "#2E6FC4", "#E2A23B", "#3FA57E"
UP, DOWN = "#2E9A5A", "#C8372D"


def arc(cx, cy, r, a0, a1):
    x0, y0 = polar(cx, cy, r, a0)
    x1, y1 = polar(cx, cy, r, a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f"M{x0:.1f} {y0:.1f}A{r} {r} 0 {large} 1 {x1:.1f} {y1:.1f}"


def steel(ic):
    return two(ic, "#D4D8DD", "#9AA1A9")


@soft("Pass")
def pass_(ic):
    tile(ic, "#8A3540", "#4A141E")
    soft_shadow(ic, 128, 212, 106, 12)
    ic.rect(200, 110, 40, 32, rx=8, fill="#3E2A1C")
    ic.rect(20, 48, 202, 158, rx=14, fill=two(ic, "#664833", "#2E1D12"))
    ic.rect(28, 60, 186, 140, rx=5, fill="#D3C9B5")
    ic.rect(28, 56, 92, 140, rx=5, fill=two(ic, "#FCF9F2", "#EEE6D5"))
    ic.rect(122, 56, 92, 140, rx=5, fill=two(ic, "#FCF9F2", "#EEE6D5"))
    dot = "#26201C"

    def entry(x, y, w, n):
        bar(ic, x, y, w, 6, fill="#A49E91")
        for k in range(n):
            ic.circle(x + 3.5 + k * 9, y + 16, 3.4, fill=dot)

    bar(ic, 36, 66, 58, 11, fill="#3B2A22")
    for y, w, n in ((90, 46, 7), (116, 36, 6), (142, 44, 7), (168, 34, 5)):
        entry(36, y, w, n)
    for y, w, n in ((66, 32, 6), (92, 26, 5), (118, 38, 6)):
        entry(130, y, w, n)
    bar(ic, 132, 172, 46, 7, fill="#2463AE", transform="rotate(-4 155 176)")
    ic.path("M190 50h12v164l-6-6-6 6z", fill=two(ic, "#3E6AB0", "#284C86"))
    ic.rect(220, 102, 22, 48, rx=7, fill=two(ic, "#E2B45E", "#B88433"))
    ic.rect(227, 114, 8, 24, rx=4, fill="#4A3210")


def _key(ic, bow, shaft, hole):
    """The key, on its own axis: bow at 0,0, the tip at x 158."""
    ic.circle(0, 0, 28, fill=bow)
    ic.rect(22, -10, 12, 20, rx=4, fill=bow)
    ic.rect(30, -7.5, 126, 15, rx=5, fill=shaft)
    ic.path("M100 7v10h6v7h8v-5h7v9h8v-7h7v11h8V7z", fill=shaft, stroke=shaft, stroke_width=2,
            stroke_linejoin="round")
    ic.circle(-12, 0, 8, fill=hole)


@soft("GPG")
def gpg(ic):
    tile(ic, "#7A8240", "#384016")
    soft_shadow(ic, 136, 214, 98, 11)
    with ic.g(transform="rotate(-8 76 150)"):
        ic.path("M50 104H100L116 120V194a7 7 0 0 1-7 7H41a7 7 0 0 1-7-7V120z", fill=two(ic, "#FCF9F2", "#E9E1CF"))
        ic.circle(75, 120, 10, fill="#E3BC72")
        ic.circle(75, 120, 5, fill="#4E5626")
        bar(ic, 42, 138, 44, 5, fill="#A49E91")
        for y, w in ((150, 62), (165, 62), (180, 38)):
            bar(ic, 42, y, w, 9, fill="#2A2C30")
    ic.path("M72 116C64 104 58 96 54 86M78 116C76 102 70 94 60 86", fill="none", stroke="#EFE6CF",
            stroke_width=2.5, stroke_linecap="round")
    ring_c, ring_r = (64, 56), 33.6
    ring = dict(fill="none", stroke="#AEB4BB", stroke_width=7)
    ic.circle(*ring_c, ring_r, **ring)
    brass = two(ic, "#E2B45E", "#B88433")
    with ic.g(transform="translate(100 84) rotate(40)"):
        _key(ic, brass, "#CC9A47", "#5E6830")
        mark(ic, 0, -10, 20, fill="#8A6020", opacity=0.8)
    hx, hy = 100 + math.cos(math.radians(40)) * -12, 84 + math.sin(math.radians(40)) * -12
    ic.circle(*ring_c, ring_r, clip_path=ic.clip(f'<circle cx="{hx:.2f}" cy="{hy:.2f}" r="8"/>'), **ring)


@soft("Tailscale")
def tailscale(ic):
    tile(ic, "#3E4855", "#151B23")
    soft_shadow(ic, 128, 202, 104, 12)
    for x, a in ((66, -12), (190, 12)):
        with ic.g(transform=f"rotate({a} {x} 112)"):
            ic.rect(x - 7, 22, 14, 92, rx=7, fill="#24272C")
            ic.rect(x - 10, 100, 20, 16, rx=5, fill="#34373D")
    ic.path("M48 108H208L226 126H30z", fill=two(ic, "#F4F5F6", "#D2D6DA"), stroke="#E2E5E8", stroke_width=4,
            stroke_linejoin="round")
    ic.rect(30, 126, 196, 66, rx=12, fill=two(ic, "#E6E9EC", "#B0B7BF"))
    ic.rect(42, 136, 60, 46, rx=9, fill="#0E1013")
    lit = {(1, 0), (1, 1), (1, 2), (2, 1)}
    for r in range(3):
        for c in range(3):
            ic.circle(56 + c * 16, 145 + r * 14, 5, fill="#F6FAFF" if (r, c) in lit else "#3A3F47")
    bar(ic, 112, 139, 58, 8, fill="#3A4048")
    bar(ic, 112, 152, 42, 6, fill="#8A9098")
    for x in (150, 176, 202):
        ic.rect(x - 9, 170, 18, 14, rx=3, fill="#121417")
    for x, col, end in ((150, "#E2B23E", (210, 214)), (176, "#3D7BD0", (236, 196))):
        ic.path(f"M{x} 186C{x} 206 {end[0] - 30} {end[1]} {end[0]} {end[1]}", fill="none", stroke=col,
                stroke_width=7, stroke_linecap="round")
        ic.rect(x - 8, 172, 16, 16, rx=3, fill="#E8ECEF")
        ic.rect(x - 6, 184, 12, 7, rx=3, fill=col)
    ic.path("M226 160C240 162 244 176 240 190", fill="none", stroke="#16181B", stroke_width=5,
            stroke_linecap="round")


@soft("Remote")
def remote(ic):
    tile(ic, "#5E7489", "#283646")
    soft_shadow(ic, 128, 208, 108, 11)
    for i, r in enumerate((9, 18, 27)):
        ic.path(arc(128, 38, r, -42, 42), fill="none", stroke="#E9F1F8", stroke_opacity=0.9 - i * 0.2,
                stroke_width=6, stroke_linecap="round")
    ic.rect(36, 44, 184, 126, rx=14, fill=two(ic, "#454B53", "#2E3338"))
    ic.rect(44, 54, 168, 108, rx=7, fill=two(ic, "#F0AE7C", "#8A5E98"))
    ic.path("M44 140C80 124 110 132 140 120S190 112 212 118V155a7 7 0 0 1-7 7H51a7 7 0 0 1-7-7z", fill="#3B3166",
            opacity=0.75)
    ic.path("M44 61a7 7 0 0 1 7-7h154a7 7 0 0 1 7 7v3H44z", fill="#14121C", opacity=0.75)
    ic.rect(56, 72, 88, 62, rx=7, fill="#F7F5F0")
    for k, col in enumerate(("#5B8BC6", "#E0A35A", "#6FA37A", "#B36C8C", "#7D7AC2", "#D07B5A")):
        ic.rect(62 + (k % 3) * 26, 86 + (k // 3) * 22, 22, 17, rx=4, fill=col)
    ic.rect(124, 100, 76, 48, rx=7, fill="#0C1A12")
    bar(ic, 131, 110, 40, 6, fill="#4FBF78")
    bar(ic, 131, 121, 30, 6, fill="#4FBF78", opacity=0.55)
    ic.rect(131, 131, 7, 10, rx=1.5, fill="#7CF7A6")
    ic.path("M150 92l0 34 8-8 6 13 5-2-6-13h11z", fill="#fff", stroke="#16191C", stroke_width=3,
            stroke_linejoin="round")
    ic.path("M24 170H232L242 186a5 5 0 0 1-5 5H19a5 5 0 0 1-5-5z", fill=two(ic, "#E3E6EA", "#A3AAB2"))
    ic.rect(108, 171, 40, 5, rx=2.5, fill="#8D949C")


def coil(p0, p1, turns, r):
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    px, py = -uy, ux
    pts = []
    steps = int(turns * 16)
    for i in range(steps + 1):
        t = i / steps
        th = 2 * math.pi * turns * t
        a = r * (math.cos(th) - 1) * (0 if i in (0, steps) else 1)
        b = r * math.sin(th)
        pts.append((x0 + dx * t + ux * a + px * b, y0 + dy * t + uy * a + py * b))
    return "L" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


@soft("MobileLink")
def mobilelink(ic):
    tile(ic, "#2E8285", "#103F42")
    soft_shadow(ic, 128, 206, 106, 12)
    with ic.g(transform="translate(14 0)"):
        ic.rect(22, 46, 164, 116, rx=14, fill=two(ic, "#454B53", "#2E3338"))
        ic.rect(30, 55, 148, 99, rx=7, fill=two(ic, "#2C5E66", "#173E44"))
        ic.rect(38, 70, 94, 64, rx=8, fill="#F4F6F5")
        bar(ic, 46, 78, 42, 9, fill="#1E2A2C")
        bar(ic, 46, 92, 54, 6, fill="#A0AEB0")
        bar(ic, 46, 104, 70, 7, fill="#DCE3E2")
        bar(ic, 46, 104, 56, 7, fill="#2F9A8E")
        bar(ic, 46, 119, 50, 6, fill="#2F7F80")
        ic.path("M12 162H196L204 175a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z", fill=two(ic, "#E3E6EA", "#A3AAB2"))
    cable = "M24 174C18 184 22 196 36 196" + coil((36, 196), (156, 200), 6, 7) + "C162 200 176 204 184 210"
    ic.path(cable, fill="none", stroke="#E8ECEF", stroke_width=4, stroke_linejoin="round", stroke_linecap="round")
    with ic.g(transform="rotate(-9 200 212)"):
        ic.rect(164, 66, 70, 146, rx=16, fill=two(ic, "#454B53", "#1E2024"))
        ic.rect(169, 72, 60, 134, rx=11, fill=two(ic, "#3FA6A0", "#1A4A60"))
        ic.rect(192, 77, 14, 4, rx=2, fill="#0A0B0D")
        bar(ic, 182, 90, 34, 14, fill="#F4FAF9")
        bar(ic, 186, 109, 26, 5, fill="#D4ECEA")
        ic.rect(173, 124, 52, 34, rx=8, fill="#F4F6F5")
        ic.circle(183, 134, 6, fill="#2E8285")
        mark(ic, 179, 130, 8, fill="#fff")
        bar(ic, 192, 131, 24, 6, fill="#1E2A2C")
        bar(ic, 178, 145, 40, 5, fill="#8A9698")
        bar(ic, 186, 198, 26, 4, fill="#fff", opacity=0.7)


@soft("SystemMonitor")
def systemmonitor(ic):
    tile(ic, "#33664A", "#12301F")
    soft_shadow(ic, 128, 210, 104, 12)
    ic.path("M68 50V40a10 10 0 0 1 10-10H178a10 10 0 0 1 10 10V50", fill="none", stroke="#AEB4BB",
            stroke_width=8, stroke_linecap="round")
    ic.path("M40 46H216L230 60H26z", fill=two(ic, "#F6F2E8", "#D9D2C2"), stroke="#EDE8DB", stroke_width=4,
            stroke_linejoin="round")
    for x in (44, 198):
        ic.rect(x, 194, 14, 10, rx=3, fill="#2A2C30")
    ic.rect(26, 60, 204, 138, rx=14, fill=two(ic, "#E6E1D3", "#B5AD99"))
    ic.rect(36, 70, 128, 104, rx=14, fill="#2A2C2A")
    sx, sy, sw, sh = 44, 78, 112, 88
    ic.rect(sx, sy, sw, sh, rx=9, fill="#0C2416")
    grid = dict(stroke="#4FBF78", stroke_opacity=0.2, stroke_width=1.5)
    for i in (1, 2, 3):
        ic.line(sx + sw * i / 4, sy + 4, sx + sw * i / 4, sy + sh - 4, **grid)
        ic.line(sx + 4, sy + sh * i / 4, sx + sw - 4, sy + sh * i / 4, **grid)
    ys = [150, 149, 150, 146, 128, 110, 130, 148, 150, 142, 104, 122, 146, 150, 148, 150]
    pts = [(sx + 8 + i * (sw - 16) / (len(ys) - 1), y) for i, y in enumerate(ys)]
    ic.path("M" + "L".join(f"{x:.1f} {y}" for x, y in pts), fill="none", stroke="#7CF7A6", stroke_width=4,
            stroke_linejoin="round", stroke_linecap="round")
    bar(ic, sx + 8, sy + 9, 50, 7, fill="#7CF7A6", opacity=0.5)
    knob = two(ic, "#4F535A", "#1E2024")
    for x, a in ((184, -40), (212, 30)):
        ic.circle(x, 94, 12, fill=knob)
        ic.rect(x - 1.5, 83, 3, 8, rx=1.5, fill="#F1EDE3", transform=f"rotate({a} {x} 94)")
    for x in (176, 192, 208):
        ic.circle(x, 124, 6, fill="#2A2C30")
    for x in (182, 208):
        ic.circle(x, 158, 9, fill=steel(ic))
        ic.circle(x, 158, 4, fill="#C99645")
    mark(ic, 40, 179, 11, fill="#5A5446")
    bar(ic, 56, 182, 40, 6, fill="#8A8270")
    ic.circle(156, 184, 4, fill="#7CF7A6")
    ic.path("M182 166C182 196 210 200 238 196", fill="none", stroke="#1A1C1E", stroke_width=5,
            stroke_linecap="round")


@soft("DiskUsage")
def diskusage(ic):
    tile(ic, "#B5693C", "#5E2C12")
    soft_shadow(ic, 128, 222, 86, 10)
    ic.rect(50, 24, 156, 198, rx=16, fill=two(ic, "#E6E9EC", "#A3AAB2"))
    ic.path("M60 46a12 12 0 0 1 12-12h112a12 12 0 0 1 12 12v124a12 12 0 0 1-12 12h-8l-14 14h-90a12 12 0 0 1-12-12z",
            fill=two(ic, "#5D636B", "#8D949C"))
    cx, cy, R = 128, 106, 66
    ic.circle(cx, cy, R, fill=two(ic, "#EEF1F4", "#B4BBC3"))
    for r, end, col in ((54, 248, ACCENT), (42, 118, WARN), (30, 296, OK)):
        ic.circle(cx, cy, r, fill="none", stroke="#2A2E33", stroke_opacity=0.15, stroke_width=9)
        ic.path(arc(cx, cy, r, 0, end), fill="none", stroke=col, stroke_width=9, stroke_linecap="round")
    ic.circle(cx, cy, 16, fill=steel(ic))
    ic.circle(cx, cy, 5, fill="#6B727B")
    px, py = 178, 178
    hx, hy = polar(cx, cy, 54, 120)
    ang = math.degrees(math.atan2(hy - py, hx - px))
    L = math.hypot(hx - px, hy - py)
    ic.path("M186 196a18 14 0 0 1 10-24l8 2v24z", fill="#2A2C30")
    with ic.g(transform=f"translate({px} {py}) rotate({ang:.1f})"):
        ic.path(f"M0 -11L{L - 6} -4L{L - 6} 4L0 11z", fill="#C3C8CE", stroke="#C3C8CE", stroke_width=3,
                stroke_linejoin="round")
        ic.rect(L - 6, -5.5, 12, 11, rx=3, fill="#2A2C30")
    ic.circle(px, py, 14, fill=two(ic, "#4F535A", "#1E2024"))
    ic.circle(px, py, 6, fill=steel(ic))
    mark(ic, 72, 186, 12, fill="#2A2E33", opacity=0.75)
    bar(ic, 89, 189, 34, 7, fill="#2A2E33", opacity=0.6)
    bar(ic, 72, 204, 56, 5, fill="#2A2E33", opacity=0.4)


@soft("Stocks")
def stocks(ic):
    tile(ic, "#2F5E4E", "#10291F")
    soft_shadow(ic, 128, 212, 106, 12)
    ic.rect(38, 36, 182, 176, rx=4, fill="#CFC9BB", transform="rotate(5 128 124)")
    with ic.g(transform="rotate(-3 128 124)"):
        ic.rect(30, 30, 194, 180, rx=4, fill=two(ic, "#F6F3EA", "#DCD6C8"))
        bar(ic, 40, 40, 88, 13, fill="#1E1E20")
        bar(ic, 170, 44, 44, 5, fill="#8C887F")
        ic.rect(40, 58, 174, 3, rx=1.5, fill="#1E1E20")
        bar(ic, 40, 69, 52, 15, fill="#1E1E20")
        ic.poly([(98, 83), (106, 70), (114, 83)], fill=UP, stroke=UP, stroke_width=2, stroke_linejoin="round")
        bar(ic, 120, 69, 62, 15, fill=UP)
        bar(ic, 40, 91, 110, 5, fill="#8C887F")
        bx, by, bw, bh = 40, 103, 110, 68
        ic.rect(bx, by, bw, bh, rx=4, fill="#FBF9F3")
        candles = [(160, 152, 148, 164), (152, 156, 147, 160), (156, 142, 138, 159), (142, 134, 129, 146),
                   (134, 138, 130, 141), (138, 124, 119, 141), (124, 114, 110, 127)]
        for k, (o, c, hi, lo) in enumerate(candles):
            x = bx + 12 + k * 14.5
            col = UP if c < o else DOWN
            ic.line(x, hi, x, lo, stroke=col, stroke_width=2, stroke_linecap="round")
            ic.rect(x - 4, min(o, c), 8, max(abs(o - c), 3), rx=1.5, fill=col)
        for k, up in enumerate((True, True, False, True, False)):
            y = 106 + k * 13.5
            bar(ic, 160, y, 22, 6, fill="#1E1E20")
            bar(ic, 186, y, 16, 6, fill="#8C887F")
            if up:
                ic.poly([(205, y + 6), (213, y + 6), (209, y)], fill=UP)
            else:
                ic.poly([(205, y), (213, y), (209, y + 6)], fill=DOWN)
        for col in range(3):
            for j in range(3):
                bar(ic, 40 + col * 59, 180 + j * 8.5, 52 if (j + col) % 3 != 2 else 34, 4.5, fill="#A49E91")
