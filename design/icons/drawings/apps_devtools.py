"""The inua-objects theme, developer tools: GitHub Desktop, Postman,
Insomnia, DBeaver, Docker Desktop, Vim, Neovim, Emacs
(docs/feat/object-icons.md, Part 2). Marks are redrawn, simplified."""

import math

from lib import (brass, glare, graphite, icon, paper, polar, shadow, small, steel, tile)


def _f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def _crescent(cx, cy, r, cx2, cy2, r2):
    """The part of circle (cx, cy, r) outside circle (cx2, cy2, r2), as a
    path; the circles must cross."""
    dx, dy = cx2 - cx, cy2 - cy
    d = math.hypot(dx, dy)
    a = (r * r - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(max(r * r - a * a, 0))
    mx, my = cx + a * dx / d, cy + a * dy / d
    p1 = (mx + h * dy / d, my - h * dx / d)
    p2 = (mx - h * dy / d, my + h * dx / d)
    return (f"M{_f(p1[0])} {_f(p1[1])}A{_f(r)} {_f(r)} 0 1 0 {_f(p2[0])} {_f(p2[1])}"
            f"A{_f(r2)} {_f(r2)} 0 0 1 {_f(p1[0])} {_f(p1[1])}Z")


def _ring_text(ic, s, cx, cy, r, start, step, size, **kw):
    """Letters set one by one round a ring, upright along the radius,
    from angle start (0 up, clockwise), step degrees apart."""
    for i, ch in enumerate(s):
        if ch == " ":
            continue
        with ic.g(transform=f"rotate({_f(start + i * step)} {cx} {cy})"):
            ic.text(ch, cx, cy - r, size, anchor="middle", **kw)


# --- GitHub Desktop: a commit log card, and an enamel badge of the cat ------

def _octocat(ic, cx, cy, s, **kw):
    """The cat of GitHub's mark, redrawn plainly: a round head with two
    ears, the body down to the badge's edge, a tail curled at the left;
    s is the badge's radius."""
    k = s / 40
    def p(x, y):
        return f"{_f(cx + x * k)} {_f(cy + y * k)}"
    d = (f"M{p(-9, 40)}L{p(-9, 24)}"
         f"C{p(-15, 24)} {p(-19, 22)} {p(-22, 17)}"  # the tail, up the left
         f"C{p(-24, 13)} {p(-26, 11)} {p(-30, 10)}"
         f"C{p(-25, 6)} {p(-20, 9)} {p(-17, 13)}"
         f"C{p(-14, 17)} {p(-12, 17)} {p(-10, 17)}"
         f"L{p(-10, 13)}"
         f"C{p(-20, 11)} {p(-25, 5)} {p(-25, -4)}"  # the head's left
         f"C{p(-25, -9)} {p(-23, -13)} {p(-21, -16)}"
         f"C{p(-22, -20)} {p(-22, -25)} {p(-20, -29)}"  # the left ear
         f"C{p(-15, -29)} {p(-11, -26)} {p(-8, -24)}"
         f"C{p(-3, -25)} {p(3, -25)} {p(8, -24)}"
         f"C{p(11, -26)} {p(15, -29)} {p(20, -29)}"  # the right ear
         f"C{p(22, -25)} {p(22, -20)} {p(21, -16)}"
         f"C{p(23, -13)} {p(25, -9)} {p(25, -4)}"
         f"C{p(25, 5)} {p(20, 11)} {p(10, 13)}"
         f"L{p(10, 40)}Z")
    ic.path(d, **kw)


@icon("github-desktop", kind="app",
      names=["appimagekit-github-desktop", "github-desktop", "io.github.shiftey.Desktop"], title="GitHub Desktop")
def github_desktop(ic):
    tile(ic, "#6A4CA8", "#2B1A57")
    shadow(ic, 128, 214, 96, 12)
    # the commit log, an index card behind
    with ic.g(transform="rotate(-6 120 110)"):
        ic.rect(34, 38, 168, 140, rx=5, fill="#000", opacity=0.25, transform="translate(3 4)")
        ic.rect(34, 38, 168, 140, rx=5, fill=paper(ic, "white"))
        ic.rect(34, 38, 168, 22, rx=5, fill="#24292F")
        ic.rect(34, 52, 168, 8, fill="#24292F")
        ic.text("inua", 44, 53, 9, font="sans-semibold", fill="#F0F3F6")
        ic.text("main", 72, 53, 8, font="mono", fill="#8B949E")
        ic.text("Fetch origin", 192, 53, 7, font="sans-medium", anchor="end", fill="#C9D1D9")
        # the graph: main straight, a branch off and back
        ic.line(50, 70, 50, 170, stroke="#8250DF", stroke_width=3)
        ic.path("M50 84 C64 88 64 96 64 104 L64 118 C64 128 60 132 50 136", fill="none",
                stroke="#2DA44E", stroke_width=3)
        for y in (74, 92, 112, 136, 156):
            on = y in (92, 112)
            x = 64 if on else 50
            ic.circle(x, y, 4.5, fill="#fff", stroke="#2DA44E" if on else "#8250DF", stroke_width=2.5)
        rows = [("Dock: keep the gap", "2h"), ("Icons: devtools set", "3h"), ("Tray menu on click", "5h"),
                ("Merge branch 'icons'", "1d"), ("Fix focus on close", "2d")]
        for (msg, when), y in zip(rows, (77, 95, 115, 139, 159)):
            ic.text(msg, 78, y, 7.5, font="sans-medium", fill="#24292F")
            ic.text(when, 192, y, 6.5, font="mono", anchor="end", fill="#8C887F")
            ic.line(76, y + 7, 194, y + 7, stroke="#000", stroke_opacity=0.07)
    # the badge, enamel in a steel rim, a pin's shadow under it
    cx, cy, r = 160, 152, 52
    ic.ellipse(cx + 4, cy + 52, 44, 8, fill="#000", opacity=0.25)
    ic.circle(cx + 1.5, cy + 4, r, fill="#1A1430")
    ic.circle(cx, cy, r, fill=steel(ic, horizontal=False))
    ic.circle(cx, cy, r - 5, fill=ic.rad([(0, "#3A3F47"), (1, "#0D1117")], cx=0.4, cy=0.35, r=0.8))
    ic.circle(cx, cy, r - 5, fill="none", stroke="#000", stroke_opacity=0.5, stroke_width=1.5)
    clip = ic.clip(f'<circle cx="{cx}" cy="{cy}" r="{r - 8}"/>')
    with ic.g(clip_path=clip):
        _octocat(ic, cx + 0.8, cy + 1.2, r - 8, fill="#000", opacity=0.45)
        _octocat(ic, cx, cy, r - 8, fill=ic.lin([(0, "#FFFFFF"), (1, "#D9DEE5")]))
    ic.path(f"M{cx - 44} {cy - 6}a44 44 0 0 1 50-38 50 50 0 0 0-50 38z", fill="#fff", opacity=0.35)


@small("github-desktop")
def github_desktop16(ic):
    tile(ic, "#6A4CA8", "#2B1A57")
    ic.rect(2, 2.5, 9.5, 8, rx=0.6, fill="#F4F2EE", transform="rotate(-6 7 6)")
    ic.line(4, 4.5, 4, 9.5, stroke="#8250DF", stroke_width=0.9)
    ic.circle(9.8, 9.8, 5.6, fill="#C3C8CE")
    ic.circle(9.8, 9.8, 4.9, fill="#161B22")
    _octocat(ic, 9.8, 9.9, 4.6, fill="#fff")


# --- Postman: an orange leather satchel of letters, a tag on its strap ------

def _rocket(ic, cx, cy, k, **kw):
    """Postman's little rocket, redrawn: a body, a fin each side, a port."""
    def p(x, y):
        return f"{_f(cx + x * k)} {_f(cy + y * k)}"
    ic.path(f"M{p(0, -14)}C{p(5, -9)} {p(6, -2)} {p(5, 6)}L{p(-5, 6)}C{p(-6, -2)} {p(-5, -9)} {p(0, -14)}Z"
            f"M{p(-5, 0)}L{p(-10, 8)}L{p(-5, 7)}Z M{p(5, 0)}L{p(10, 8)}L{p(5, 7)}Z"
            f"M{p(-3, 8)}L{p(0, 14)}L{p(3, 8)}Z", **kw)


@icon("postman", kind="app", names=["com.getpostman.Postman", "postman"], title="Postman")
def postman(ic):
    tile(ic, "#4A4D57", "#1E2026")
    shadow(ic, 128, 214, 98, 12)
    # the strap, behind everything, up over the top
    ic.path("M48 120 C40 60 70 24 128 24 C186 24 216 60 208 120", fill="none", stroke="#7A3416", stroke_width=15)
    ic.path("M48 120 C40 60 70 24 128 24 C186 24 216 60 208 120", fill="none", stroke="#C25A2A", stroke_width=11)
    ic.path("M48 120 C40 60 70 24 128 24 C186 24 216 60 208 120", fill="none", stroke="#FFC09A",
            stroke_width=1, stroke_dasharray="3 3", opacity=0.6, transform="translate(-3 0)")
    # the letters, standing up out of the bag
    with ic.g(transform="rotate(-8 100 90)"):
        ic.rect(62, 58, 84, 56, rx=3, fill=paper(ic, "kraft"))
        ic.path("M62 60 L104 86 L146 60", fill="none", stroke="#9C7231", stroke_width=1.5)
    with ic.g(transform="rotate(6 150 90)"):
        ic.rect(110, 52, 92, 62, rx=3, fill=paper(ic, "cream"), stroke="#000", stroke_opacity=0.08)
        ic.rect(176, 58, 18, 22, rx=1, fill="#FF6C37")
        ic.rect(179, 61, 12, 16, fill="none", stroke="#fff", stroke_width=1, opacity=0.8)
        ic.text("GET", 118, 70, 8, font="mono-semibold", fill="#2E8540")
        ic.text("/api/v1/mail", 118, 81, 7, font="mono", fill="#55534E")
    # the bag
    leather = ic.lin([(0, "#FF8A50"), (0.55, "#E8622C"), (1, "#B3431A")], 0, 0, 0.4, 1)
    ic.rect(36, 100, 184, 108, rx=18, fill="#9A3814")
    ic.rect(36, 98, 184, 106, rx=18, fill=leather)
    ic.rect(36.75, 98.75, 182.5, 104.5, rx=17.25, fill="none", stroke="#FFD2B6", stroke_opacity=0.35, stroke_width=1.5)
    ic.rect(44, 106, 168, 90, rx=12, fill="none", stroke="#FFD9C2", stroke_opacity=0.5, stroke_dasharray="3 3")
    # the flap
    ic.path("M40 104 a8 8 0 0 1 8-8 H208 a8 8 0 0 1 8 8 V140 C216 160 180 172 128 172 C76 172 40 160 40 140 Z",
            fill="#000", opacity=0.22, transform="translate(0 4)")
    ic.path("M40 104 a8 8 0 0 1 8-8 H208 a8 8 0 0 1 8 8 V140 C216 160 180 172 128 172 C76 172 40 160 40 140 Z",
            fill=ic.lin([(0, "#FF9A62"), (1, "#D9541F")]))
    ic.path("M48 106 H208 V139 C208 154 176 164 128 164 C80 164 48 154 48 139 Z", fill="none",
            stroke="#FFE0CC", stroke_opacity=0.55, stroke_dasharray="3 3")
    ic.line(48, 97.5, 208, 97.5, stroke="#FFE3D2", stroke_width=2, opacity=0.8)
    # the mark, pressed into the flap
    ic.circle(128, 128, 21, fill="#C24A1A")
    ic.circle(128, 128, 21, fill="none", stroke="#8A2E0C", stroke_opacity=0.6, stroke_width=2)
    ic.circle(127.3, 127.3, 21, fill="none", stroke="#FFD0B4", stroke_opacity=0.45)
    with ic.g(transform="rotate(35 128 128)"):
        _rocket(ic, 128.6, 128.6, 1.05, fill="#7A2A0C", opacity=0.5)
        _rocket(ic, 128, 128, 1.05, fill="#FFF3EA")
    # the buckle strap
    ic.rect(119, 164, 18, 34, rx=3, fill="#B8461A")
    ic.rect(117, 174, 22, 16, rx=3, fill="none", stroke=ic.lin([(0, "#F6DDA0"), (1, "#8A6224")]), stroke_width=3.5)
    ic.line(128, 176, 128, 188, stroke="#7E5A20", stroke_width=2.5)
    # the tag on the strap
    ic.line(207, 116, 212, 140, stroke="#5A4A3A", stroke_width=1.2)
    with ic.g(transform="rotate(10 212 150)"):
        ic.path("M198 142 l8-6 h20 v34 h-28z", fill=paper(ic, "cream"), stroke="#000", stroke_opacity=0.1)
        ic.circle(206, 142, 2, fill="#4A4D57")
        ic.text("200", 212, 157, 8, font="mono-semibold", anchor="middle", fill="#2E8540")
        ic.text("OK", 212, 166, 7, font="mono-semibold", anchor="middle", fill="#2E8540")


@small("postman")
def postman16(ic):
    tile(ic, "#4A4D57", "#1E2026")
    ic.path("M3.5 8 C3 3.5 5 2 8 2 C11 2 13 3.5 12.5 8", fill="none", stroke="#C25A2A", stroke_width=1)
    ic.rect(5, 4, 6, 4, fill="#FCF9F2", transform="rotate(5 8 6)")
    ic.rect(2, 6.5, 12, 7, rx=1.4, fill="#E8622C")
    ic.path("M2 7.3a.8.8 0 0 1 .8-.8h10.4a.8.8 0 0 1 .8.8V9.6C14 11 11 11.4 8 11.4 5 11.4 2 11 2 9.6z", fill="#FF8D55")
    ic.circle(8, 9, 1.5, fill="#FFF3EA")


# --- Insomnia: a night lamp, a crescent moon glowing in a purple globe ------

@icon("insomnia", kind="app", names=["insomnia", "rest.insomnia.Insomnia"], title="Insomnia")
def insomnia(ic):
    tile(ic, "#4E2E96", "#1A0B44")
    ic.circle(128, 108, 108, fill=ic.rad([(0, "#B48CFF", 0.35), (0.6, "#7A4BE0", 0.12), (1, "#4E2E96", 0)]))
    shadow(ic, 128, 216, 70, 10)
    # the base: turned walnut, a brass band
    ic.rect(80, 176, 96, 36, rx=8, fill=ic.lin([(0, "#3A2414"), (0.3, "#8A5A34"), (0.6, "#6A4222"), (1, "#2E1A0C")], 0, 0, 1, 0))
    ic.ellipse(128, 212, 48, 6, fill="#2A170A")
    ic.rect(80, 176, 96, 36, rx=8, fill="none", stroke="#fff", stroke_opacity=0.08)
    ic.rect(86, 168, 84, 10, rx=3, fill=ic.lin([(0, "#7E5A20"), (0.35, "#F6DDA0"), (0.6, "#C99645"), (1, "#5E4214")], 0, 0, 1, 0))
    ic.circle(158, 194, 4.5, fill="#1E1208")
    ic.circle(158, 194, 3, fill=brass(ic))
    # the globe, frosted glass lit from inside
    ic.circle(128, 100, 78, fill=ic.rad([(0, "#F3ECFF"), (0.35, "#C8A8FF"), (0.75, "#8752EA"), (1, "#5226B8")],
                                        cx=0.45, cy=0.45, r=0.6))
    # the moon: the mark's crescent, a disc with a bite of shadow out of it
    ic.path(_crescent(122, 104, 44, 146, 84, 36), fill="#4A1FA8", opacity=0.25, transform="translate(2 3)")
    ic.path(_crescent(122, 104, 44, 146, 84, 36),
            fill=ic.rad([(0, "#FFFFFF"), (0.7, "#FBF6FF"), (1, "#E3D2FF")], cx=0.35, cy=0.6, r=0.7))
    for x, y, r in ((96, 118, 6), (110, 136, 4), (88, 96, 3.5), (120, 124, 2.5)):
        ic.circle(x, y, r, fill="#D7C2FF", opacity=0.55)
    ic.text("z", 158, 112, 15, font="sans-semibold", fill="#fff", opacity=0.9)
    ic.text("z", 172, 96, 11, font="sans-semibold", fill="#fff", opacity=0.75)
    ic.text("z", 182, 83, 8, font="sans-semibold", fill="#fff", opacity=0.6)
    ic.circle(128, 100, 78, fill="none", stroke="#fff", stroke_opacity=0.35, stroke_width=1.5)
    ic.path("M62 74a72 72 0 0 1 66-46 78 78 0 0 0-66 46z", fill="#fff", opacity=0.6)
    ic.path("M128 100m-78 0a78 78 0 0 0 156 0 74 74 0 0 1-156 0z", fill="#2A0E70", opacity=0.3)


@small("insomnia")
def insomnia16(ic):
    tile(ic, "#4E2E96", "#1A0B44")
    ic.rect(5, 11.5, 6, 2.5, rx=0.6, fill="#7A4E2C")
    ic.circle(8, 7, 5, fill="#A57CF5")
    ic.path(_crescent(7.6, 7.3, 3, 9.2, 5.9, 2.4), fill="#fff")


# --- DBeaver: a beaver, holding a database ------------------------------------

@icon("dbeaver", kind="app", names=["dbeaver", "dbeaver-ee", "io.dbeaver.DBeaverCommunity"], title="DBeaver")
def dbeaver(ic):
    tile(ic, "#3D7884", "#173A44")
    shadow(ic, 124, 216, 92, 11)
    fur = ic.lin([(0, "#B07A48"), (0.6, "#7E4E26"), (1, "#4E2C12")], 0, 0, 1, 1)
    # the tail, flat and scaled, out to the right
    with ic.g(transform="rotate(-24 196 186)"):
        ic.ellipse(196, 186, 42, 17, fill="#2A1C14")
        ic.ellipse(196, 184, 42, 17, fill=ic.lin([(0, "#6A5446"), (1, "#3A2A20")]))
        scales = ic.define('<pattern id="{id}" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                           '<path d="M0 0h7v7" fill="none" stroke="#1E140E" stroke-opacity=".5"/></pattern>', "p")
        ic.ellipse(196, 184, 40, 15, fill=f"url(#{scales})")
        ic.path("M158 180 a42 17 0 0 1 60 -12", fill="none", stroke="#fff", stroke_opacity=0.2, stroke_width=1.5)
    # the body, sitting up
    ic.ellipse(124, 150, 62, 64, fill=fur)
    ic.ellipse(124, 160, 40, 46, fill=ic.lin([(0, "#D6A876"), (1, "#9C6A3C")]))
    # the feet
    for x in (86, 162):
        ic.ellipse(x, 208, 20, 9, fill="#3A2210")
        ic.ellipse(x, 206, 19, 8, fill="#6A4020")
    # the head
    for x in (88, 160):
        ic.circle(x, 58, 12, fill="#5A3416")
        ic.circle(x, 58, 6, fill="#C99068")
    ic.ellipse(124, 84, 46, 40, fill=fur)
    ic.ellipse(124, 84, 46, 40, fill="none", stroke="#fff", stroke_opacity=0.1, stroke_width=1.5)
    for x in (104, 144):
        ic.circle(x, 76, 7, fill="#140A04")
        ic.circle(x - 2, 73.5, 2.4, fill="#fff")
    ic.ellipse(124, 100, 25, 17, fill=ic.lin([(0, "#E4C098"), (1, "#B98A5C")]))
    ic.path("M114 89 h20 a4 4 0 0 1 3 6 l-7 7 a4 4 0 0 1 -6 0 l-7 -7 a4 4 0 0 1 3 -6z", fill="#1E120A")
    ic.ellipse(120, 91, 4, 1.6, fill="#fff", opacity=0.4)
    ic.line(124, 104, 124, 108, stroke="#5A3416", stroke_width=1.5)
    for s in (-1, 1):
        for i, dy in enumerate((-2, 3)):
            ic.line(124 + s * 16, 100 + dy, 124 + s * 34, 96 + dy * 2 + i, stroke="#2A1608", stroke_opacity=0.5)
    # the teeth
    ic.rect(117, 107, 14, 15, rx=2, fill="#B0782C")
    ic.rect(117, 107, 6.6, 14, rx=1.5, fill="#F5D38E")
    ic.rect(124.4, 107, 6.6, 14, rx=1.5, fill="#F5D38E")
    # the database, held up in both paws
    x, y, w, h = 92, 138, 64, 52
    ic.rect(x, y, w, h, fill=steel(ic))
    ic.ellipse(x + w / 2, y + h, w / 2, 9, fill=ic.lin([(0, "#6B727B"), (0.5, "#A9AFB6"), (1, "#5D636B")], 0, 0, 1, 0))
    for yy in (y + 17, y + 34):
        ic.path(f"M{x} {yy}a{w / 2} 9 0 0 0 {w} 0", fill="none", stroke="#3E444B", stroke_width=2)
        ic.path(f"M{x} {yy + 2}a{w / 2} 9 0 0 0 {w} 0", fill="none", stroke="#fff", stroke_opacity=0.4)
    ic.rect(x, y, w, h, fill="none")
    ic.ellipse(x + w / 2, y, w / 2, 9, fill=ic.lin([(0, "#E4E8EC"), (1, "#A9AFB6")], 0, 0, 1, 1))
    ic.ellipse(x + w / 2, y, w / 2, 9, fill="none", stroke="#5D636B", stroke_opacity=0.6)
    ic.text("SQL", x + w / 2 - 4, y + 31, 8, font="mono-semibold", anchor="middle", fill="#3E444B")
    ic.circle(x + w / 2 + 12, y + 28.5, 2.2, fill="#5BE37A")
    ic.circle(x + w / 2 + 12, y + 46, 2.2, fill="#5BE37A", opacity=0.6)
    for px in (90, 158):
        ic.ellipse(px, 158, 11, 14, fill="#5E3618")
        ic.ellipse(px - 1, 155, 9, 11, fill="#8E5A2E")


@small("dbeaver")
def dbeaver16(ic):
    tile(ic, "#3D7884", "#173A44")
    ic.ellipse(12, 12.5, 3, 1.4, fill="#4A3A30", transform="rotate(-24 12 12.5)")
    ic.circle(5.5, 3.6, 1.2, fill="#5A3416")
    ic.circle(10.5, 3.6, 1.2, fill="#5A3416")
    ic.ellipse(8, 10, 4.6, 4.6, fill="#8E5A2E")
    ic.ellipse(8, 5.6, 3.6, 3.2, fill="#9E6A38")
    ic.circle(6.6, 5, 0.6, fill="#140A04")
    ic.circle(9.4, 5, 0.6, fill="#140A04")
    ic.rect(7.3, 7, 1.4, 1.4, fill="#F5D38E")
    ic.rect(6, 9.6, 4, 3.4, fill="#B4BAC1")
    ic.ellipse(8, 9.6, 2, 0.7, fill="#E4E8EC")


# --- Docker Desktop: the whale, carrying its containers ------------------------

def _container(ic, x, y, w, h, light, dark):
    """A shipping container side on: corrugated, a frame, its shadow."""
    ic.rect(x, y, w, h, rx=1.5, fill=ic.lin([(0, light), (1, dark)]))
    for i in range(1, int(w // 4)):
        ic.line(x + i * 4, y + 3, x + i * 4, y + h - 3, stroke="#000", stroke_opacity=0.18, stroke_width=1.2)
        ic.line(x + i * 4 + 1.2, y + 3, x + i * 4 + 1.2, y + h - 3, stroke="#fff", stroke_opacity=0.18)
    ic.rect(x + 0.5, y + 0.5, w - 1, h - 1, rx=1.5, fill="none", stroke=dark, stroke_width=1.5)
    ic.line(x + 1.5, y + 1.2, x + w - 1.5, y + 1.2, stroke="#fff", stroke_opacity=0.45)


@icon("docker-desktop", kind="app", names=["docker-desktop"], title="Docker Desktop")
def docker(ic):
    tile(ic, "#2457A0", "#0C2552")
    shadow(ic, 128, 214, 100, 11)
    # the whale, head to the left, its tail up behind
    body = ("M26 154 C26 142 30 134 42 134 H186 C196 134 202 128 204 118 C204 110 198 102 190 98"
            " C200 92 212 96 218 106 C222 94 232 88 244 90 C238 98 230 108 226 120 C222 134 214 142 212 152"
            " C202 186 166 206 118 206 C70 206 32 188 26 154 Z")
    ic.path(body, fill="#062048", transform="translate(0 4)", opacity=0.6)
    ic.path(body, fill=ic.lin([(0, "#5CB5FF"), (0.5, "#2496ED"), (1, "#1361C2")], 0, 0, 0.3, 1))
    ic.path("M30 168 C48 190 84 202 118 202 C160 202 196 188 208 160 C176 178 146 182 112 182 C76 182 50 178 30 168Z",
            fill="#E8F3FF", opacity=0.9)
    ic.line(40, 135.2, 186, 135.2, stroke="#C9E6FF", stroke_width=2, opacity=0.9)
    ic.path("M204 118 C204 110 198 102 190 98 C200 92 212 96 218 106", fill="none", stroke="#C9E6FF",
            stroke_width=1.5, opacity=0.6)
    ic.circle(60, 154, 7, fill="#0B2A55")
    ic.circle(58, 152, 2.4, fill="#fff")
    ic.path("M30 172 C40 176 52 176 60 172", fill="none", stroke="#1361C2", stroke_width=1.5, opacity=0.5)
    # the containers, five, three and one
    blue = ("#4FA9F5", "#1A6FCB")
    navy = ("#2C6FC0", "#123F80")
    white = ("#F4F8FC", "#B8C7D8")
    rows = [(110, [blue, navy, white, blue, navy]), (84, [navy, blue, navy]), (58, [white])]
    for y, colours in rows:
        n = len(colours)
        x0 = 106 - n * 13 + 26 if n != 5 else 44
        if n == 3:
            x0 = 70
        if n == 1:
            x0 = 96
        for i, (lt, dk) in enumerate(colours):
            x = x0 + i * 26
            ic.rect(x + 2, y + 3, 24, 23, fill="#000", opacity=0.22)
            _container(ic, x, y, 24, 24, lt, dk)
    # the sea it rides on
    ic.path("M20 196 C40 188 56 204 76 196 C96 188 112 204 132 196 C152 188 168 204 188 196 C208 188 224 204 236 198"
            " L236 206 C220 214 200 214 128 214 C60 214 36 214 20 206Z", fill="#7CC4FF", opacity=0.35)


@small("docker-desktop")
def docker16(ic):
    tile(ic, "#2457A0", "#0C2552")
    ic.path("M2 8.5 H11.5 C12.5 8.5 13 7.5 13 6.5 C13.8 6.3 14.5 6.6 14.6 7.4 C14 7.8 13.6 8.6 13.3 9.4"
            " C12.6 11.8 10.4 13 7.6 13 C4.4 13 2.3 11.5 2 10 Z", fill="#2496ED")
    ic.path("M2.3 10.6 C4 12.2 6 12.6 7.6 12.6 C9.8 12.6 11.6 12 12.6 10.6 C10 11.4 5 11.4 2.3 10.6Z", fill="#E8F3FF")
    for x, y in ((3, 6.5), (5, 6.5), (7, 6.5), (9, 6.5), (5, 4.5), (7, 4.5), (6, 2.5)):
        ic.rect(x, y, 1.7, 1.7, fill="#8FCBFF" if y != 2.5 else "#F4F8FC")


# --- Vim: a diamond enamel badge, its V in silver -----------------------------

def _diamond(cx, cy, r):
    return [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]


def _vee(ic, dx=0, dy=0, **kw):
    pts = [(80, 76), (118, 76), (118, 87), (111, 87), (132, 142), (153, 87), (146, 87), (146, 76),
           (178, 76), (178, 87), (171, 87), (140, 166), (122, 166), (88, 87), (80, 87)]
    ic.poly([(x + dx, y + dy) for x, y in pts], **kw)


@icon("gvim", kind="app", names=["gvim", "org.vim.Vim", "vim", "vim-qt"], title="Vim")
def vim(ic):
    tile(ic, "#2E5A40", "#0E2618")
    shadow(ic, 128, 216, 80, 11)
    cx, cy = 128, 118
    ic.poly(_diamond(cx + 2, cy + 6, 96), fill="#0A1A10", opacity=0.55)
    ic.poly(_diamond(cx, cy, 96), fill=steel(ic, horizontal=False))
    ic.poly(_diamond(cx, cy, 93), fill="none", stroke="#fff", stroke_opacity=0.4, stroke_width=1.5)
    ic.poly(_diamond(cx, cy, 82), fill="#3E454C")
    ic.poly(_diamond(cx, cy, 80), fill=ic.lin([(0, "#5FCB5A"), (0.55, "#2E9A34"), (1, "#16661E")], 0, 0, 0.6, 1))
    ic.poly(_diamond(cx, cy, 80), fill="none", stroke="#0E4A14", stroke_opacity=0.5, stroke_width=1.5)
    ic.poly([(cx, cy - 80), (cx + 80, cy), (cx - 80, cy)], fill="#fff", opacity=0.08)
    _vee(ic, 2, 3, fill="#0A3A10", opacity=0.6)
    _vee(ic, fill=ic.lin([(0, "#F2F4F6"), (0.5, "#C3C8CE"), (1, "#8A929B")]), stroke="#2A3036",
         stroke_width=2.5, stroke_linejoin="round")
    _vee(ic, -0.8, -0.8, fill="none", stroke="#fff", stroke_opacity=0.5, stroke_width=0.8, stroke_linejoin="round")
    # engraved on the rim
    with ic.g(transform=f"rotate(45 {cx - 44.5} {cy + 44.5})"):
        ic.text("VIM 9.1", cx - 44.5, cy + 47.5 - 3, 7, font="mono-semibold", anchor="middle", spacing=1.2,
                fill="#2E343A")
    with ic.g(transform=f"rotate(-45 {cx + 44.5} {cy + 44.5})"):
        ic.text(":wq", cx + 44.5, cy + 47.5 - 3, 7, font="mono-semibold", anchor="middle", spacing=1.2,
                fill="#2E343A")
    ic.path(f"M{cx - 96} {cy}L{cx} {cy - 96}L{cx + 6} {cy - 90}L{cx - 90} {cy}Z", fill="#fff", opacity=0.3)


@small("gvim")
def vim16(ic):
    tile(ic, "#2E5A40", "#0E2618")
    ic.poly(_diamond(8, 8, 7), fill="#C3C8CE")
    ic.poly(_diamond(8, 8, 5.8), fill="#2E9A34")
    ic.poly([(4.8, 5), (7.2, 5), (8.2, 8.4), (9.4, 5), (11.2, 5), (8.9, 11), (7.5, 11)], fill="#F2F4F6")


# --- Neovim: the N as three slabs of coloured glass ----------------------------

@icon("nvim", kind="app",
      names=["io.neovim.nvim", "neovim", "nvim", "nvim-gtk", "nvim-qt", "org.daa.NeovimGtk", "pynvim"], title="Neovim")
def neovim(ic):
    tile(ic, "#24384A", "#0A141E")
    shadow(ic, 128, 214, 92, 11)
    # light through the glass, coloured, on the desk
    ic.ellipse(84, 210, 34, 6, fill=ic.rad([(0, "#3FB6F2", 0.5), (1, "#3FB6F2", 0)]))
    ic.ellipse(176, 210, 34, 6, fill=ic.rad([(0, "#7CD050", 0.5), (1, "#7CD050", 0)]))
    t = (10, -6)  # the glass's thickness, back and to the right

    def slab(pts, front, side, top, edge):
        """A slab of glass: its faces seen from the front, the top and the
        right, then the front, its glare and a bright edge."""
        back = [(x + t[0], y + t[1]) for x, y in pts]
        n = len(pts)
        for i in range(n):
            a, b = pts[i], pts[(i + 1) % n]
            c, d = back[i], back[(i + 1) % n]
            # a face shows when its edge faces up or right
            ex, ey = b[0] - a[0], b[1] - a[1]
            if ex * t[1] - ey * t[0] < 0:
                ic.poly([a, b, d, c], fill=top if abs(ex) > abs(ey) else side)
        ic.poly(pts, fill=front)
        ic.poly(pts, fill=glare(ic, 1.6))
        ic.poly(pts, fill="none", stroke=edge, stroke_width=1.2, stroke_linejoin="round", stroke_opacity=0.75)

    # right bar, green; the diagonal, teal into green; left bar, blue
    slab([(156, 72), (186, 54), (186, 194), (156, 212)],
         ic.lin([(0, "#A6E070", 0.92), (1, "#3E8A2E", 0.92)]), "#2C6E22", "#CFF2A8", "#E4FAD0")
    slab([(64, 52), (94, 34), (186, 176), (156, 212)],
         ic.lin([(0, "#56C8E8", 0.85), (1, "#4FAE52", 0.85)], 0, 0, 1, 1), "#2E8C8C", "#B8ECF6", "#D8F6FF")
    slab([(64, 52), (94, 34), (94, 194), (64, 212)],
         ic.lin([(0, "#56C2F6", 0.95), (1, "#1458B2", 0.95)]), "#0E3E80", "#B6E2FF", "#D8F0FF")
    ic.line(67.5, 56, 67.5, 204, stroke="#fff", stroke_width=2.5, stroke_linecap="round", opacity=0.55)
    ic.line(73, 62, 73, 140, stroke="#fff", stroke_width=1, stroke_linecap="round", opacity=0.35)
    ic.line(159.5, 78, 159.5, 204, stroke="#fff", stroke_width=2, stroke_linecap="round", opacity=0.45)


@small("nvim")
def neovim16(ic):
    tile(ic, "#24384A", "#0A141E")
    ic.poly([(10, 4.6), (12, 3.4), (12, 12.6), (10, 13.4)], fill="#6CC04A")
    ic.poly([(4, 3), (6, 2), (12, 11.4), (10, 13.4)], fill="#4FBFC4")
    ic.poly([(4, 3), (6, 2), (6, 11.8), (4, 13)], fill="#2496ED")


# --- Emacs: a medallion, the purple swirl raised in silver -------------------

SWIRL = ("M160 82 C130 70 92 76 94 96 C96 116 160 108 160 128"
         " C160 150 96 140 94 160 C92 176 130 180 162 166")


@icon("emacs", kind="app",
      names=["appimagekit-emacs", "deepin-emacs", "emacs", "emacs-nox", "emacs-snapshot", "gnome-emacs",
             "org.gnu.emacs", "xemacs"], title="Emacs")
def emacs(ic):
    tile(ic, "#55408A", "#1F1340")
    shadow(ic, 128, 218, 84, 11)
    cx, cy = 128, 122
    ic.circle(cx + 2, cy + 6, 96, fill="#120A26", opacity=0.6)
    ic.circle(cx, cy, 96, fill=steel(ic, horizontal=False))
    ic.circle(cx, cy, 93, fill="none", stroke="#fff", stroke_opacity=0.45, stroke_width=1.5)
    ic.circle(cx, cy, 90, fill="none", stroke="#5D636B", stroke_opacity=0.35, stroke_width=4, stroke_dasharray="1 3")
    _ring_text(ic, "GNU EMACS", cx, cy, 77, -42, 10.5, 9, font="mono-semibold", fill="#4A4F57")
    for i, ch in enumerate("M-x"):
        with ic.g(transform=f"rotate({-(i - 1) * 9} {cx} {cy})"):
            ic.text(ch, cx, cy + 77 + 6.5, 9, font="mono-semibold", anchor="middle", fill="#4A4F57")
    ic.circle(cx, cy, 70, fill="#3E454C")
    ic.circle(cx, cy, 68, fill=ic.rad([(0, "#9C7BD8"), (0.6, "#6A44B0"), (1, "#3A2272")], cx=0.38, cy=0.32, r=0.8))
    ic.circle(cx, cy, 68, fill="none", stroke="#1E0E44", stroke_opacity=0.5, stroke_width=2)
    with ic.g(transform="translate(128 124) scale(0.98) translate(-128 -124)"):
        ic.path(SWIRL, fill="none", stroke="#1E0E44", stroke_opacity=0.6, stroke_width=17, stroke_linecap="round",
                transform="translate(2 3)")
        ic.path(SWIRL, fill="none", stroke="#2A3036", stroke_width=17, stroke_linecap="round")
        ic.path(SWIRL, fill="none", stroke=ic.lin([(0, "#FFFFFF"), (0.5, "#D4D8DD"), (1, "#9AA1A9")], 0, 0, 1, 1,
                                                  units=None), stroke_width=14, stroke_linecap="round")
        ic.path(SWIRL, fill="none", stroke="#fff", stroke_opacity=0.6, stroke_width=2, stroke_linecap="round",
                transform="translate(-2.5 -3)")
    ic.path(f"M{cx - 86} {cy - 10}a88 88 0 0 1 80-78 94 94 0 0 0-80 78z", fill="#fff", opacity=0.5)


@small("emacs")
def emacs16(ic):
    tile(ic, "#55408A", "#1F1340")
    ic.circle(8, 8, 6.5, fill="#C3C8CE")
    ic.circle(8, 8, 5.2, fill="#7450C0")
    ic.path("M10.2 5.2 C8.6 4.4 5.8 4.8 6 6.2 C6.2 7.6 10 7 10 8.4 C10 9.8 6 9.4 6 10.6 C6 11.4 8.4 11.6 10.2 10.8",
            fill="none", stroke="#fff", stroke_width=1.2, stroke_linecap="round")
