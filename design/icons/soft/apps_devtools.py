"""The soft drawings of the developer tools: GitHub Desktop, Postman,
Insomnia, DBeaver, Docker Desktop, Vim, Neovim, Emacs. The objects of
drawings/apps_devtools.py with about half the detail, no text."""

import math

from lib import bar, soft, soft_shadow, tile, two


def _f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def _crescent(cx, cy, r, cx2, cy2, r2):
    """The part of circle (cx, cy, r) outside circle (cx2, cy2, r2)."""
    dx, dy = cx2 - cx, cy2 - cy
    d = math.hypot(dx, dy)
    a = (r * r - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(max(r * r - a * a, 0))
    mx, my = cx + a * dx / d, cy + a * dy / d
    p1 = (mx + h * dy / d, my - h * dx / d)
    p2 = (mx - h * dy / d, my + h * dx / d)
    return (f"M{_f(p1[0])} {_f(p1[1])}A{_f(r)} {_f(r)} 0 1 0 {_f(p2[0])} {_f(p2[1])}"
            f"A{_f(r2)} {_f(r2)} 0 0 1 {_f(p1[0])} {_f(p1[1])}Z")


def _octocat(ic, cx, cy, s, **kw):
    """GitHub's cat, as in drawings/: head, ears, body, the tail curled."""
    k = s / 40

    def p(x, y):
        return f"{_f(cx + x * k)} {_f(cy + y * k)}"
    d = (f"M{p(-9, 40)}L{p(-9, 24)}"
         f"C{p(-15, 24)} {p(-19, 22)} {p(-22, 17)}"
         f"C{p(-24, 13)} {p(-26, 11)} {p(-30, 10)}"
         f"C{p(-25, 6)} {p(-20, 9)} {p(-17, 13)}"
         f"C{p(-14, 17)} {p(-12, 17)} {p(-10, 17)}"
         f"L{p(-10, 13)}"
         f"C{p(-20, 11)} {p(-25, 5)} {p(-25, -4)}"
         f"C{p(-25, -9)} {p(-23, -13)} {p(-21, -16)}"
         f"C{p(-22, -20)} {p(-22, -25)} {p(-20, -29)}"
         f"C{p(-15, -29)} {p(-11, -26)} {p(-8, -24)}"
         f"C{p(-3, -25)} {p(3, -25)} {p(8, -24)}"
         f"C{p(11, -26)} {p(15, -29)} {p(20, -29)}"
         f"C{p(22, -25)} {p(22, -20)} {p(21, -16)}"
         f"C{p(23, -13)} {p(25, -9)} {p(25, -4)}"
         f"C{p(25, 5)} {p(20, 11)} {p(10, 13)}"
         f"L{p(10, 40)}Z")
    ic.path(d, **kw)


@soft("github-desktop")
def github_desktop(ic):
    tile(ic, "#6A4CA8", "#2B1A57")
    soft_shadow(ic, 128, 214, 96, 12)
    with ic.g(transform="rotate(-6 120 110)"):
        ic.rect(34, 38, 168, 140, rx=10, fill=two(ic, "#FFFFFF", "#ECE8DF"))
        ic.path("M34 64V48a10 10 0 0 1 10-10h148a10 10 0 0 1 10 10v16z", fill="#24292F")
        bar(ic, 46, 48, 30, 7, fill="#F0F3F6")
        ic.line(54, 74, 54, 170, stroke="#8250DF", stroke_width=5)
        ic.path("M54 86 C70 90 70 98 70 106 L70 118 C70 128 66 132 54 136", fill="none",
                stroke="#2DA44E", stroke_width=5)
        for x, y, c in ((54, 80, "#8250DF"), (70, 102, "#2DA44E"), (54, 140, "#8250DF")):
            ic.circle(x, y, 7, fill="#fff", stroke=c, stroke_width=4)
        for y, w in ((77, 70), (99, 60), (121, 48)):
            bar(ic, 88, y, w, 7, fill="#B7B2A8")
    cx, cy, r = 160, 152, 52
    ic.circle(cx, cy, r, fill=two(ic, "#AEB4BB", "#8D949C"))
    ic.circle(cx, cy, r - 7, fill=two(ic, "#2E333B", "#0D1117"))
    clip = ic.clip(f'<circle cx="{cx}" cy="{cy}" r="{r - 9}"/>')
    with ic.g(clip_path=clip):
        _octocat(ic, cx, cy, r - 9, fill="#F4F6F8")


def _rocket(ic, cx, cy, k, **kw):
    def p(x, y):
        return f"{_f(cx + x * k)} {_f(cy + y * k)}"
    ic.path(f"M{p(0, -14)}C{p(5, -9)} {p(6, -2)} {p(5, 6)}L{p(-5, 6)}C{p(-6, -2)} {p(-5, -9)} {p(0, -14)}Z"
            f"M{p(-5, 0)}L{p(-10, 8)}L{p(-5, 7)}Z M{p(5, 0)}L{p(10, 8)}L{p(5, 7)}Z", **kw)


@soft("postman")
def postman(ic):
    tile(ic, "#4A4D57", "#1E2026")
    soft_shadow(ic, 128, 214, 98, 12)
    ic.path("M48 120 C40 60 70 24 128 24 C186 24 216 60 208 120", fill="none", stroke="#C25A2A",
            stroke_width=14)
    with ic.g(transform="rotate(-8 100 90)"):
        ic.rect(62, 58, 84, 56, rx=6, fill=two(ic, "#D9B988", "#C49C64"))
    with ic.g(transform="rotate(6 150 90)"):
        ic.rect(110, 52, 92, 62, rx=6, fill=two(ic, "#FFFDF7", "#F1EADB"))
        ic.rect(174, 58, 20, 24, rx=3, fill="#FF6C37")
        bar(ic, 120, 64, 24, 7, fill="#2E8540")
        bar(ic, 120, 78, 44, 6, fill="#A49E91")
    ic.rect(36, 98, 184, 110, rx=22, fill=two(ic, "#F07A3E", "#B8461A"))
    ic.path("M40 108 a12 12 0 0 1 12-12 H204 a12 12 0 0 1 12 12 V140 C216 160 180 172 128 172 "
            "C76 172 40 160 40 140 Z", fill=two(ic, "#FF9A62", "#E0602A"))
    ic.circle(128, 128, 22, fill="#C24A1A")
    with ic.g(transform="rotate(35 128 128)"):
        _rocket(ic, 128, 128, 1.15, fill="#FFF3EA")
    ic.rect(118, 164, 20, 36, rx=5, fill="#B8461A")
    ic.rect(115, 172, 26, 18, rx=5, fill="none", stroke="#E2B45E", stroke_width=5)


@soft("insomnia")
def insomnia(ic):
    tile(ic, "#4E2E96", "#1A0B44")
    ic.circle(128, 104, 104, fill=ic.rad([(0, "#B48CFF", 0.3), (1, "#4E2E96", 0)]))
    soft_shadow(ic, 128, 216, 70, 10)
    ic.rect(80, 174, 96, 38, rx=12, fill=two(ic, "#8A5A34", "#4A2C16"))
    ic.rect(84, 166, 88, 12, rx=5, fill=two(ic, "#E2B45E", "#B88433"))
    ic.circle(128, 100, 78, fill=two(ic, "#D6BEFF", "#6A38D6"))
    ic.path(_crescent(122, 104, 44, 146, 84, 36), fill="#FFFFFF")
    ic.circle(100, 118, 7, fill="#E3D2FF")
    ic.circle(114, 138, 4.5, fill="#E3D2FF")
    zs = dict(fill="none", stroke="#fff", stroke_linecap="round", stroke_linejoin="round")
    ic.path("M152 96h14l-14 16h14", stroke_width=5, **zs)
    ic.path("M172 76h10l-10 12h10", stroke_width=4, opacity=0.8, **zs)


@soft("dbeaver")
def dbeaver(ic):
    tile(ic, "#3D7884", "#173A44")
    soft_shadow(ic, 124, 216, 92, 11)
    fur = two(ic, "#A87444", "#6A3E1C")
    ic.ellipse(196, 184, 42, 17, fill="#6E5848", transform="rotate(-24 196 186)")
    ic.ellipse(124, 150, 62, 64, fill=fur)
    ic.ellipse(124, 162, 40, 44, fill=two(ic, "#D6A876", "#B08050"))
    for x in (86, 162):
        ic.ellipse(x, 206, 20, 9, fill="#5A3418")
    for x in (88, 160):
        ic.circle(x, 58, 13, fill="#5A3416")
        ic.circle(x, 58, 6, fill="#C99068")
    ic.ellipse(124, 84, 46, 40, fill=two(ic, "#B07A48", "#8A5A30"))
    for x in (104, 144):
        ic.circle(x, 76, 7.5, fill="#140A04")
    ic.ellipse(124, 100, 25, 17, fill="#E0BC94")
    ic.path("M114 89 h20 a4 4 0 0 1 3 6 l-7 7 a4 4 0 0 1 -6 0 l-7 -7 a4 4 0 0 1 3 -6z", fill="#1E120A")
    ic.rect(117, 106, 22, 16, rx=4, fill="#F5D38E", transform="translate(-4 0)")
    ic.rect(123.5, 106, 1.5, 15, fill="#B0782C")
    x, y, w, h = 92, 138, 64, 52
    ic.rect(x, y, w, h, fill=two(ic, "#AEB4BB", "#8D949C"))
    ic.ellipse(x + w / 2, y + h, w / 2, 10, fill="#8D949C")
    for yy in (y + 18, y + 36):
        ic.path(f"M{x} {yy}a{w / 2} 10 0 0 0 {w} 0", fill="none", stroke="#5D636B", stroke_width=3)
    ic.ellipse(x + w / 2, y, w / 2, 10, fill="#DDE1E5")
    for px in (90, 158):
        ic.ellipse(px, 156, 11, 14, fill="#7E4E26")


@soft("docker-desktop")
def docker(ic):
    tile(ic, "#2457A0", "#0C2552")
    soft_shadow(ic, 128, 214, 100, 11)
    body = ("M26 154 C26 142 30 134 42 134 H186 C196 134 202 128 204 118 C204 110 198 102 190 98"
            " C200 92 212 96 218 106 C222 94 232 88 244 90 C238 98 230 108 226 120 C222 134 214 142 212 152"
            " C202 186 166 206 118 206 C70 206 32 188 26 154 Z")
    ic.path(body, fill=two(ic, "#3FA6F5", "#1666C8"))
    ic.path("M30 168 C48 190 84 202 118 202 C160 202 196 188 208 160 C176 178 146 182 112 182 C76 182 50 178 30 168Z",
            fill="#E8F3FF")
    ic.circle(60, 154, 7.5, fill="#0B2A55")
    light, mid, white = "#5CB5FF", "#2C6FC0", "#F4F8FC"
    rows = [(108, 44, [light, mid, white, light, mid]), (82, 70, [mid, light, mid]), (56, 96, [white])]
    for y, x0, colours in rows:
        for i, c in enumerate(colours):
            ic.rect(x0 + i * 26, y, 23, 23, rx=4, fill=c)
    ic.path("M20 198 C40 190 56 206 76 198 C96 190 112 206 132 198 C152 190 168 206 188 198 C208 190 224 206 236 200"
            " L236 208 C220 214 200 214 128 214 C60 214 36 214 20 208Z", fill="#7CC4FF", opacity=0.35)


def _diamond(cx, cy, r):
    return [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]


@soft("gvim")
def vim(ic):
    tile(ic, "#2E5A40", "#0E2618")
    soft_shadow(ic, 128, 216, 80, 11)
    cx, cy = 128, 118
    ic.poly(_diamond(cx, cy, 96), fill=two(ic, "#C3C8CE", "#8D949C"), stroke="#C3C8CE", stroke_width=10,
            stroke_linejoin="round")
    ic.poly(_diamond(cx, cy, 80), fill="#3E454C", stroke="#3E454C", stroke_width=6, stroke_linejoin="round")
    ic.poly(_diamond(cx, cy, 76), fill=two(ic, "#4FBF4A", "#1E7A26"), stroke="#3AA03C", stroke_width=4,
            stroke_linejoin="round")
    pts = [(80, 76), (118, 76), (118, 87), (111, 87), (132, 142), (153, 87), (146, 87), (146, 76),
           (178, 76), (178, 87), (171, 87), (140, 166), (122, 166), (88, 87), (80, 87)]
    ic.poly(pts, fill=two(ic, "#F4F6F8", "#C3C8CE"), stroke="#2A3036", stroke_width=4, stroke_linejoin="round")


@soft("nvim")
def neovim(ic):
    tile(ic, "#24384A", "#0A141E")
    soft_shadow(ic, 128, 214, 92, 11)
    t = (10, -6)

    def slab(pts, front, depth):
        back = [(x + t[0], y + t[1]) for x, y in pts]
        n = len(pts)
        for i in range(n):
            a, b = pts[i], pts[(i + 1) % n]
            ex, ey = b[0] - a[0], b[1] - a[1]
            if ex * t[1] - ey * t[0] < 0:
                ic.poly([a, b, back[(i + 1) % n], back[i]], fill=depth, stroke=depth, stroke_width=1.5,
                        stroke_linejoin="round")
        ic.poly(pts, fill=front, stroke=front, stroke_width=1.5, stroke_linejoin="round")

    slab([(156, 72), (186, 54), (186, 194), (156, 212)], two(ic, "#A6E070", "#4A9A34"), "#2C6E22")
    slab([(64, 52), (94, 34), (186, 176), (156, 212)], two(ic, "#56C8E8", "#4FAE52"), "#2E8C8C")
    slab([(64, 52), (94, 34), (94, 194), (64, 212)], two(ic, "#56C2F6", "#1A62BC"), "#0E3E80")


SWIRL = ("M160 82 C130 70 92 76 94 96 C96 116 160 108 160 128"
         " C160 150 96 140 94 160 C92 176 130 180 162 166")


@soft("emacs")
def emacs(ic):
    tile(ic, "#55408A", "#1F1340")
    soft_shadow(ic, 128, 218, 84, 11)
    cx, cy = 128, 122
    ic.circle(cx, cy, 96, fill=two(ic, "#C3C8CE", "#8D949C"))
    ic.circle(cx, cy, 72, fill="#3E454C")
    ic.circle(cx, cy, 68, fill=two(ic, "#8C68D0", "#43277E"))
    ic.path(SWIRL, fill="none", stroke="#F4F2F8", stroke_width=18, stroke_linecap="round")
