"""inua's tools, second batch: Pass, GPG, Tailscale, Remote, MobileLink,
System Monitor, Disk Usage, Stocks (docs/feat/object-icons.md, Part 1)."""

import math

from lib import (brass, enamel, glare, glass_dark, graphite, icon, leather, mark, paper, polar, shadow, small, steel,
                 tile)

ACCENT, WARN, OK = "#2E6FC4", "#E2A23B", "#3FA57E"  # inua's ring colours, lit for an object
UP, DOWN = "#2E9A5A", "#C8372D"


def arc(cx, cy, r, a0, a1):
    """An arc's path from angle a0 to a1 (degrees, 0 up, clockwise)."""
    x0, y0 = polar(cx, cy, r, a0)
    x1, y1 = polar(cx, cy, r, a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f"M{x0:.2f} {y0:.2f}A{r} {r} 0 {large} 1 {x1:.2f} {y1:.2f}"


def coil(p0, p1, turns, r, along=1.3):
    """A coiled cable seen from the side, from p0 to p1: loops of radius r."""
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    px, py = -uy, ux
    pts = []
    steps = int(turns * 18)
    for i in range(steps + 1):
        t = i / steps
        th = 2 * math.pi * turns * t
        a = r * along * (math.cos(th) - 1) * (0 if i in (0, steps) else 1)
        b = r * math.sin(th)
        pts.append((x0 + dx * t + ux * a + px * b, y0 + dy * t + uy * a + py * b))
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def screw(ic, x, y, r=3.2):
    ic.circle(x, y, r, fill=steel(ic, horizontal=False))
    ic.circle(x, y, r, fill="none", stroke="#000", stroke_opacity=0.3, stroke_width=0.8)
    ic.line(x - r * 0.6, y + r * 0.3, x + r * 0.6, y - r * 0.3, stroke="#3A3F46", stroke_width=0.9)


# --- Pass: a leather notebook, a page of passwords, a ribbon, a brass clasp ---

@icon("Pass")
def pass_(ic):
    tile(ic, "#8A3540", "#4A141E")
    shadow(ic, 128, 212, 106, 12)
    # the clasp's strap, from under the back cover
    ic.rect(200, 110, 40, 32, rx=6, fill=leather(ic, "#5B4030", "#26180F"))
    ic.rect(200, 110.75, 39, 1.2, fill="#fff", opacity=0.12)
    # the cover, open
    ic.rect(20, 52, 202, 158, rx=10, fill="#140B07")
    ic.rect(20, 48, 202, 158, rx=10, fill=leather(ic, "#664833", "#2A1A10"))
    ic.rect(20.75, 48.75, 200.5, 156.5, rx=9.25, fill="none", stroke="#fff", stroke_opacity=0.14, stroke_width=1.5)
    ic.rect(25, 53, 192, 148, rx=7, fill="none", stroke="#D8B48A", stroke_opacity=0.35, stroke_dasharray="3 2.5")
    # the pages, a stack under each side
    for i in (3, 2, 1):
        ic.rect(28, 56 + i * 1.4, 92, 142, rx=2, fill="#CFC5B1" if i % 2 else "#E6DECC")
        ic.rect(122, 56 + i * 1.4, 92, 142, rx=2, fill="#CFC5B1" if i % 2 else "#E6DECC")
    ic.rect(28, 56, 92, 140, rx=2, fill=ic.lin([(0, "#FCF9F2"), (0.8, "#F1EADB"), (1, "#D9CFBC")], 0, 0, 1, 0))
    ic.rect(122, 56, 92, 140, rx=2, fill=ic.lin([(0, "#D3C9B5"), (0.18, "#F3EDE0"), (1, "#FBF8F1")], 0, 0, 1, 0))
    ic.line(121, 56, 121, 196, stroke="#7A6A55", stroke_opacity=0.35, stroke_width=1.2)
    # ruled lines
    for y in range(92, 196, 12):
        ic.line(36, y + 0.5, 112, y + 0.5, stroke="#9FB4CC", stroke_opacity=0.35, stroke_width=0.7)
        ic.line(130, y + 0.5, 206, y + 0.5, stroke="#9FB4CC", stroke_opacity=0.35, stroke_width=0.7)

    def entry(x, y, label, n):
        ic.text(label, x, y, 7, font="sans-medium", fill="#5A534A")
        for k in range(n):
            ic.circle(x + 3 + k * 7.6, y + 9.5, 2.5, fill="#26201C")

    ic.text("Passwords", 36, 80, 19, font="hand", fill="#3B2A22")
    entry(36, 99, "mail · inua.dev", 9)
    entry(36, 123, "github.com", 8)
    entry(36, 147, "bank · savings", 9)
    entry(36, 171, "wifi · home", 7)
    ic.text("ssh · nest", 130, 75, 7, font="sans-medium", fill="#5A534A")
    for k in range(8):
        ic.circle(133 + k * 7.6, 84.5, 2.5, fill="#26201C")
    entry(130, 99, "router", 6)
    entry(130, 123, "work vpn", 8)
    entry(130, 147, "photos", 7)
    ic.text("new in May", 132, 180, 13, font="hand", fill="#2463AE", transform="rotate(-4 160 176)")
    # the ribbon, from under the head of the right page
    ic.path("M190 50h11v164l-5.5-6-5.5 6z", fill="#000", opacity=0.22, transform="translate(2 2)")
    ic.path("M190 50h11v164l-5.5-6-5.5 6z", fill=ic.lin([(0, "#3E6AB0"), (1, "#1F3D6C")], 0, 0, 1, 0))
    ic.line(191.5, 52, 191.5, 210, stroke="#fff", stroke_opacity=0.25, stroke_width=1)
    # the clasp: brass, a slot, two rivets
    ic.rect(220, 102, 22, 48, rx=5, fill="#000", opacity=0.3, transform="translate(2 3)")
    ic.rect(220, 102, 22, 48, rx=5, fill=brass(ic))
    ic.rect(220.75, 102.75, 20.5, 46.5, rx=4.25, fill="none", stroke="#FFF1C8", stroke_opacity=0.6, stroke_width=1.5)
    ic.rect(227, 114, 8, 24, rx=4, fill="#4A3210")
    ic.rect(228, 115, 6, 2, rx=1, fill="#000", opacity=0.4)
    ic.circle(231, 108, 2, fill="#8A6424")
    ic.circle(231, 144, 2, fill="#8A6424")


@small("Pass")
def pass16(ic):
    tile(ic, "#8A3540", "#4A141E")
    ic.rect(1.5, 3.5, 12.5, 9.5, rx=1, fill="#4E3626")
    ic.rect(2.3, 4.2, 5.3, 8, fill="#F6F1E6")
    ic.rect(7.9, 4.2, 5.3, 8, fill="#EAE2D0")
    for k in range(3):
        ic.circle(3.4 + k * 1.6, 7, 0.65, fill="#26201C")
        ic.circle(3.4 + k * 1.6, 9.6, 0.65, fill="#26201C")
    ic.path("M11 3.5h1.3v10l-.65-.7-.65.7z", fill="#3E6AB0")
    ic.rect(13.2, 6.5, 2, 3.6, rx=0.5, fill="#D9A84E")


# --- GPG: a brass key on a ring, a paper tag typed with its fingerprint -------

def _key(ic, bow, shaft, hole):
    """The key, on its own axis: bow at 0,0, the tip at x 158."""
    ic.circle(0, 0, 28, fill=bow)
    ic.rect(22, -10, 10, 20, rx=2.5, fill=bow)
    ic.rect(30, -7, 126, 14, rx=3, fill=shaft)
    ic.path("M100 7v10h6v7h8v-5h7v9h8v-7h7v11h8V7z", fill=shaft)
    ic.circle(-12, 0, 7.5, fill=hole)


@icon("GPG")
def gpg(ic):
    tile(ic, "#7A8240", "#384016")
    shadow(ic, 136, 214, 98, 11)
    # the tag, on the desk, its string through the ring
    with ic.g(transform="rotate(-8 76 150)"):
        tag = "M50 104H100L116 120V196a5 5 0 0 1-5 5H39a5 5 0 0 1-5-5V120z"
        ic.path(tag, fill="#000", opacity=0.25, transform="translate(2 3)")
        ic.path(tag, fill=paper(ic, "cream"))
        ic.path("M50 104H100L116 120", fill="none", stroke="#fff", stroke_width=1.5, opacity=0.8)
        ic.circle(75, 120, 9, fill=paper(ic, "kraft"))
        ic.circle(75, 120, 4.5, fill="#4E5626")
        ic.text("GPG · ed25519", 42, 144, 7, font="mono", fill="#6A665D")
        ic.text("4A9F 0C21", 42, 160, 12.5, font="mono-semibold", fill="#2A2C30")
        ic.text("7D3E B815", 42, 175, 12.5, font="mono-semibold", fill="#2A2C30")
        ic.text("E64A …", 42, 190, 12.5, font="mono-semibold", fill="#2A2C30")
    ic.path("M72 116C64 104 58 96 54 86M78 116C76 102 70 94 60 86", fill="none", stroke="#EFE6CF",
            stroke_width=1.6, stroke_linecap="round")
    # the ring, the key through it
    ring_c, ring_r = (64, 56), 33.6
    ic.circle(*ring_c, ring_r, fill="none", stroke="#2E3312", stroke_opacity=0.35, stroke_width=6,
              transform="translate(2 3)")
    ic.circle(*ring_c, ring_r, fill="none", stroke=steel(ic, horizontal=False), stroke_width=5.5)
    ic.path(arc(*ring_c, ring_r - 1.5, 280, 350), fill="none", stroke="#fff", stroke_opacity=0.7, stroke_width=1.2,
            stroke_linecap="round")
    with ic.g(transform="translate(104 90) rotate(40)", opacity=0.3):
        _key(ic, "#1E2208", "#1E2208", "none")
    with ic.g(transform="translate(100 84) rotate(40)"):
        _key(ic, brass(ic), ic.lin([(0, "#F6DDA0"), (0.5, "#C99645"), (1, "#8A6424")]), "#5E6830")
        ic.circle(0, 0, 21, fill="none", stroke="#7E5A20", stroke_opacity=0.5, stroke_width=1.5)
        ic.path(arc(0, 0, 26.5, 260, 350), fill="none", stroke="#FFF4D2", stroke_opacity=0.8, stroke_width=1.5)
        ic.line(34, -5.5, 152, -5.5, stroke="#FFF4D2", stroke_opacity=0.6, stroke_width=1.2)
        ic.line(36, 1, 150, 1, stroke="#6E4E18", stroke_opacity=0.45, stroke_width=1.6)
        mark(ic, -1, -10, 20, fill="#7E5A20", opacity=0.75)
    # the ring again where it shows through the key's hole
    hx, hy = 100 + math.cos(math.radians(40)) * -12, 84 + math.sin(math.radians(40)) * -12
    ic.circle(*ring_c, ring_r, fill="none", stroke=steel(ic, horizontal=False), stroke_width=5.5,
              clip_path=ic.clip(f'<circle cx="{hx:.2f}" cy="{hy:.2f}" r="7.5"/>'))


@small("GPG")
def gpg16(ic):
    tile(ic, "#7A8240", "#384016")
    ic.circle(4.5, 4.5, 2.6, fill="none", stroke="#C3C8CE", stroke_width=0.9)
    with ic.g(transform="translate(6.2 6.2) rotate(40)"):
        ic.circle(0, 0, 2.6, fill="#D9A84E")
        ic.rect(1.8, -0.75, 7.6, 1.5, fill="#D9A84E")
        ic.rect(6.6, 0.6, 2.8, 1.4, fill="#D9A84E")
        ic.circle(-0.8, 0, 0.8, fill="#4E5626")
    ic.path("M2.2 9.5h3.5l1.3 1.3v3.4H2.2z", fill="#F6F1E6")


# --- Tailscale: a small router, antennas up, nine LEDs in Tailscale's grid ---

@icon("Tailscale")
def tailscale(ic):
    tile(ic, "#3E4855", "#151B23")
    shadow(ic, 128, 202, 104, 12)
    # antennas, behind
    for x, a in ((66, -12), (190, 12)):
        with ic.g(transform=f"rotate({a} {x} 112)"):
            ic.rect(x - 6, 22, 12, 92, rx=6, fill=ic.lin([(0, "#4A4F57"), (0.4, "#2B2E33"), (1, "#16181B")], 0, 0, 1, 0))
            ic.rect(x - 3.5, 26, 2, 70, rx=1, fill="#fff", opacity=0.15)
            ic.rect(x - 9, 100, 18, 16, rx=4, fill=graphite(ic))
    # body: top face, front face
    ic.path("M46 108H210L226 126H30z", fill=ic.lin([(0, "#F4F5F6"), (1, "#C9CDD2")]))
    for x in range(78, 182, 8):
        ic.path(f"M{x} 113h4l1 9h-6z", fill="#8A9098", opacity=0.6)
    ic.rect(30, 126, 196, 66, rx=8, fill=enamel(ic, "#E6E9EC", "#A3AAB2"))
    ic.line(34, 126.8, 222, 126.8, stroke="#fff", stroke_width=1.6)
    ic.rect(30, 186, 196, 6, rx=3, fill="#000", opacity=0.12)
    # the LED panel
    ic.rect(42, 136, 60, 46, rx=6, fill="#0E1013")
    ic.rect(42, 136, 60, 46, rx=6, fill=glare(ic, 0.7))
    lit = {(1, 0), (1, 1), (1, 2), (2, 1)}
    halo = ic.rad([(0, "#E8F4FF", 0.55), (1, "#E8F4FF", 0)])
    for r in range(3):
        for c in range(3):
            x, y = 56 + c * 16, 145 + r * 14
            if (r, c) in lit:
                ic.circle(x, y, 9, fill=halo)
                ic.circle(x, y, 4.4, fill="#F6FAFF")
            else:
                ic.circle(x, y, 4.4, fill="#3A3F47")
                ic.circle(x - 1, y - 1, 1.4, fill="#fff", opacity=0.12)
    # name, address and ports
    ic.text("INUA NODE", 112, 145, 8, font="mono-semibold", spacing=1, fill="#3A4048")
    ic.text("100.101.42.7", 112, 156, 7, font="mono", fill="#6A7078")
    for i, (label, x) in enumerate((("WAN", 150), ("LAN 1", 176), ("LAN 2", 202))):
        ic.text(label, x, 168, 5.5, font="mono-semibold", anchor="middle", fill="#5A6068")
        ic.rect(x - 9, 171, 18, 13, rx=1.5, fill="#121417")
        ic.rect(x - 6, 172, 12, 2, fill="#C9A44E")
        ic.circle(x + 7, 166, 1.4, fill="#7CF7A6" if i < 2 else "#5A6068")
    # cables
    for x, col, end in ((150, "#E2B23E", (210, 214)), (176, "#3D7BD0", (236, 196))):
        d = f"M{x} 186C{x} 206 {end[0] - 30} {end[1]} {end[0]} {end[1]}"
        ic.path(d, fill="none", stroke="#000", stroke_opacity=0.3, stroke_width=7, transform="translate(1.5 2.5)")
        ic.path(d, fill="none", stroke=col, stroke_width=6.5, stroke_linecap="round")
        ic.path(f"M{x - 1.8} 188C{x - 1.8} 202 {x + 8} 208 {x + 22} {end[1] - 1}", fill="none", stroke="#fff",
                stroke_opacity=0.35, stroke_width=1.3, stroke_linecap="round")
        ic.rect(x - 8, 173, 16, 15, rx=2, fill="#E8ECEF", opacity=0.9)
        ic.rect(x - 6, 175, 12, 4, rx=1, fill="#C9A44E", opacity=0.8)
        ic.rect(x - 5.5, 186, 11, 6, rx=2, fill=col)
        ic.rect(x - 4, 187, 2, 4, rx=1, fill="#fff", opacity=0.3)
    # the power lead, from the side
    ic.path("M226 160C240 162 244 176 240 190", fill="none", stroke="#16181B", stroke_width=4.5,
            stroke_linecap="round")
    ic.rect(222, 155, 8, 10, rx=2, fill="#2A2C30")


@small("Tailscale")
def tailscale16(ic):
    tile(ic, "#3E4855", "#151B23")
    ic.rect(3.2, 2, 1.2, 6.5, rx=0.6, fill="#2B2E33", transform="rotate(-12 3.8 8)")
    ic.rect(11.6, 2, 1.2, 6.5, rx=0.6, fill="#2B2E33", transform="rotate(12 12.2 8)")
    ic.rect(1.5, 7, 13, 6, rx=1, fill="#DCE0E4")
    ic.rect(2.5, 7.7, 5.3, 4.6, rx=0.5, fill="#0E1013")
    for r in range(3):
        for c in range(3):
            on = (r, c) in {(1, 0), (1, 1), (1, 2), (2, 1)}
            ic.circle(3.6 + c * 1.55, 8.6 + r * 1.4, 0.5, fill="#F6FAFF" if on else "#4A4F57")


# --- Remote: a laptop showing another desktop, signal arcs ------------------

@icon("Remote")
def remote(ic):
    tile(ic, "#5E7489", "#283646")
    shadow(ic, 128, 208, 108, 11)
    # signal, from the camera
    for i, r in enumerate((9, 17, 25)):
        ic.path(arc(128, 40, r, -42, 42), fill="none", stroke="#E9F1F8", stroke_opacity=0.9 - i * 0.2,
                stroke_width=4.5, stroke_linecap="round")
    # lid
    ic.rect(36, 44, 184, 126, rx=10, fill=ic.lin([(0, "#4A5058"), (0.06, "#2E3238"), (1, "#16191C")]))
    ic.rect(36.75, 44.75, 182.5, 124.5, rx=9.25, fill="none", stroke="#fff", stroke_opacity=0.14, stroke_width=1.5)
    ic.circle(128, 49.5, 1.8, fill="#0A0B0D")
    sx, sy, sw, sh = 44, 54, 168, 108
    clip = ic.clip(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="4"/>')
    with ic.g(clip_path=clip):
        ic.rect(sx, sy, sw, sh, fill=ic.lin([(0, "#F2B27A"), (0.55, "#C2708A"), (1, "#5A4A8C")], 0, 0, 0.6, 1))
        ic.path(f"M{sx} 140 C80 124 110 132 140 120 S190 112 {sx + sw} 118 V{sy + sh}H{sx}z", fill="#3B3166",
                opacity=0.7)
        ic.path(f"M{sx} 150 C90 140 130 150 170 138 S200 136 {sx + sw} 140 V{sy + sh}H{sx}z", fill="#241F45",
                opacity=0.8)
        ic.rect(sx, sy, sw, 9, fill="#14121C", opacity=0.75)
        ic.text("nest", sx + 5, sy + 6.8, 6, font="mono-semibold", fill="#F2EEF6")
        ic.text("12:40", sx + sw - 5, sy + 6.8, 6, font="mono-semibold", anchor="end", fill="#F2EEF6")
        # a window of files
        ic.rect(56, 72, 88, 62, rx=4, fill="#000", opacity=0.25, transform="translate(1.5 2)")
        ic.rect(56, 72, 88, 62, rx=4, fill="#F7F5F0")
        ic.rect(56, 72, 88, 11, rx=4, fill="#E3DFD6")
        ic.rect(56, 79, 88, 4, fill="#E3DFD6")
        ic.text("Photos — nest", 62, 80.5, 6, font="sans-semibold", fill="#4E4C47")
        for k, col in enumerate(("#5B8BC6", "#E0A35A", "#6FA37A", "#B36C8C", "#7D7AC2", "#D07B5A")):
            x, y = 62 + (k % 3) * 26, 89 + (k // 3) * 22
            ic.rect(x, y, 22, 17, rx=2, fill=col)
            ic.path(f"M{x} {y + 17}l7-8 5 5 4-3 6 6z", fill="#fff", opacity=0.35)
        # a terminal
        ic.rect(124, 100, 76, 48, rx=4, fill="#000", opacity=0.3, transform="translate(1.5 2)")
        ic.rect(124, 100, 76, 48, rx=4, fill="#0C1A12")
        dim = dict(font="mono-semibold", fill="#4FBF78")
        ic.text("$ uptime", 130, 113, 6.5, **dim)
        ic.text("up 41 days", 130, 123, 6.5, font="mono", fill="#4FBF78", opacity=0.7)
        ic.text("$", 130, 133, 6.5, **dim)
        ic.rect(136, 127.5, 4, 6.5, fill="#7CF7A6")
    # the pointer, someone else's
    ic.path("M150 92l0 34 8-8 6 13 5-2-6-13h11z", fill="#000", opacity=0.3, transform="translate(2 2.5)")
    ic.path("M150 92l0 34 8-8 6 13 5-2-6-13h11z", fill="#fff", stroke="#16191C", stroke_width=2,
            stroke_linejoin="round")
    ic.path(f"M{sx} {sy + 4}a4 4 0 0 1 4-4h86L80 {sy + sh}H{sx + 4}a4 4 0 0 1-4-4z", fill=glare(ic, 0.6))
    # base
    ic.path("M24 170H232L242 186a4 4 0 0 1-4 5H18a4 4 0 0 1-4-5z", fill=ic.lin([(0, "#E3E6EA"), (1, "#9AA1A9")]))
    ic.line(26, 170.8, 230, 170.8, stroke="#fff", stroke_width=1.5)
    ic.path("M14 186a4 4 0 0 0 4 5H238a4 4 0 0 0 4-5z", fill="#000", opacity=0.18)
    ic.rect(108, 171, 40, 4, rx=2, fill="#6B727B", opacity=0.5)


@small("Remote")
def remote16(ic):
    tile(ic, "#5E7489", "#283646")
    ic.rect(2.5, 3, 11, 8, rx=1, fill="#23272C")
    ic.rect(3.3, 3.8, 9.4, 6.4, fill="#D88A7E")
    ic.rect(4.2, 5, 4.2, 3.4, fill="#F7F5F0")
    ic.path("M9 5.5v4.2l1-1 .8 1.6.7-.3-.8-1.6h1.4z", fill="#fff", stroke="#16191C", stroke_width=0.4)
    ic.path("M1.5 11h13l.6 1.4H.9z", fill="#C3C8CE")


# --- MobileLink: a phone leaning on a laptop, a coiled cable -------------------

@icon("MobileLink")
def mobilelink(ic):
    tile(ic, "#2E8285", "#103F42")
    shadow(ic, 128, 206, 106, 12)
    # laptop, behind
    with ic.g(transform="translate(14 0)"):
        ic.rect(22, 46, 164, 116, rx=10, fill=ic.lin([(0, "#4A5058"), (0.06, "#2E3238"), (1, "#16191C")]))
        ic.rect(22.75, 46.75, 162.5, 114.5, rx=9.25, fill="none", stroke="#fff", stroke_opacity=0.14, stroke_width=1.5)
        sx, sy, sw, sh = 30, 55, 148, 99
        ic.rect(sx, sy, sw, sh, rx=4, fill=ic.lin([(0, "#2C5E66"), (1, "#123238")], 0, 0, 0.5, 1))
        ic.rect(sx, sy, sw, 8, fill="#0B1E22", opacity=0.7)
        ic.text("Phone", sx + 5, sy + 6, 5.5, font="mono-semibold", fill="#CFE6E6")
        # the link panel on the laptop
        ic.rect(38, 70, 94, 64, rx=5, fill="#F4F6F5")
        ic.text("Pixel 8", 46, 84, 9, font="sans-semibold", fill="#1E2A2C")
        ic.text("linked · 82%", 46, 95, 6.5, font="mono", fill="#5A6A6C")
        ic.rect(46, 102, 70, 5, rx=2.5, fill="#DCE3E2")
        ic.rect(46, 102, 57, 5, rx=2.5, fill="#2F9A8E")
        ic.text("Files  ·  Clipboard", 46, 120, 6.5, font="sans-medium", fill="#3C4A4C")
        ic.text("Send to phone", 46, 129, 6.5, font="sans-medium", fill="#2F7F80")
        ic.path(f"M{sx} {sy + 4}a4 4 0 0 1 4-4h70L60 {sy + sh}H{sx + 4}a4 4 0 0 1-4-4z", fill=glare(ic, 0.5))
        ic.path("M12 162H196L204 175a4 4 0 0 1-4 5H8a4 4 0 0 1-4-5z", fill=ic.lin([(0, "#E3E6EA"), (1, "#9AA1A9")]))
        ic.line(14, 162.8, 194, 162.8, stroke="#fff", stroke_width=1.5)
        ic.path("M4 175a4 4 0 0 0 4 5H200a4 4 0 0 0 4-5z", fill="#000", opacity=0.18)
    # the cable, coiled on the desk, from the laptop's side to the phone
    cable = "M24 174C18 184 22 196 36 196" + coil((36, 196), (156, 200), 9, 6.5, along=1.0).replace("M", "L", 1) \
        + "C162 200 176 204 184 210"
    ic.path(cable, fill="none", stroke="#0A2A2C", stroke_opacity=0.4, stroke_width=4, transform="translate(1.5 2)")
    ic.path(cable, fill="none", stroke="#E8ECEF", stroke_width=3, stroke_linejoin="round")
    ic.path(cable, fill="none", stroke="#9AA6AE", stroke_width=1, stroke_opacity=0.6, transform="translate(0.6 0.8)")
    # the phone, leaning left on the lid
    with ic.g(transform="rotate(-9 200 212)"):
        ic.rect(164, 66, 70, 146, rx=13, fill="#000", opacity=0.3, transform="translate(-3 2)")
        ic.rect(164, 66, 70, 146, rx=13, fill=ic.lin([(0, "#5A6068"), (0.08, "#2B2E33"), (1, "#121417")], 0, 0, 1, 1))
        ic.rect(164.75, 66.75, 68.5, 144.5, rx=12.25, fill="none", stroke="#fff", stroke_opacity=0.2,
                stroke_width=1.5)
        ic.rect(169, 72, 60, 134, rx=9, fill=ic.lin([(0, "#3FA6A0"), (0.6, "#1D5E66"), (1, "#16314A")]))
        ic.rect(193, 76, 12, 3, rx=1.5, fill="#0A0B0D")
        ic.text("9:41", 199, 104, 18, font="sans-semibold", anchor="middle", fill="#F4FAF9")
        ic.text("Fri 30 October", 199, 115, 6.5, font="sans-medium", anchor="middle", fill="#D4ECEA")
        ic.rect(173, 124, 52, 34, rx=6, fill="#F4F6F5", opacity=0.96)
        ic.circle(182, 133, 5, fill="#2E8285")
        mark(ic, 178.5, 129.5, 7, fill="#fff")
        ic.text("Laptop", 190, 135, 6.5, font="sans-semibold", fill="#1E2A2C")
        ic.text("Copied: Itinerary", 177, 146, 5.5, font="sans", fill="#4A5658")
        ic.text("Nov 2 · 07:12", 177, 154, 5.5, font="sans", fill="#4A5658")
        ic.rect(186, 199, 26, 2.5, rx=1.25, fill="#fff", opacity=0.7)
        ic.path("M169 81a9 9 0 0 1 9-9h40L176 206a9 9 0 0 1-7-9z", fill=glare(ic, 0.6))


@small("MobileLink")
def mobilelink16(ic):
    tile(ic, "#2E8285", "#103F42")
    ic.rect(1.5, 3, 9.5, 7, rx=0.8, fill="#23272C")
    ic.rect(2.2, 3.7, 8.1, 5.6, fill="#2C5E66")
    ic.path("M.8 10h11l.4 1H.4z", fill="#C3C8CE")
    with ic.g(transform="rotate(-9 12 14)"):
        ic.rect(9.5, 4.5, 5, 9.5, rx=1, fill="#16181B")
        ic.rect(10.1, 5.2, 3.8, 8, rx=0.5, fill="#3FA6A0")
        ic.rect(10.4, 7, 3.2, 1.8, rx=0.4, fill="#F4F6F5")


# --- System Monitor: an oscilloscope, a green trace -----------------------------

@icon("SystemMonitor")
def systemmonitor(ic):
    tile(ic, "#33664A", "#12301F")
    shadow(ic, 128, 210, 104, 12)
    # handle
    ic.path("M68 50V38a8 8 0 0 1 8-8H180a8 8 0 0 1 8 8V50", fill="none", stroke="#1C2A20", stroke_opacity=0.35,
            stroke_width=7, transform="translate(2 2)")
    ic.path("M68 50V38a8 8 0 0 1 8-8H180a8 8 0 0 1 8 8V50", fill="none", stroke=steel(ic, horizontal=False),
            stroke_width=6, stroke_linecap="round")
    # body: top and front
    ic.path("M38 46H218L230 60H26z", fill=ic.lin([(0, "#F6F2E8"), (1, "#D5CEBD")]))
    ic.rect(26, 60, 204, 138, rx=10, fill=enamel(ic, "#E6E1D3", "#ABA38F"))
    ic.line(30, 60.8, 226, 60.8, stroke="#fff", stroke_width=1.6)
    ic.rect(26, 190, 204, 8, rx=4, fill="#000", opacity=0.1)
    for x in (44, 202):
        ic.rect(x, 196, 14, 8, rx=2, fill="#2A2C30")
    # the screen in its bezel
    ic.rect(36, 70, 128, 104, rx=12, fill=ic.lin([(0, "#1A1C1A"), (1, "#3A3D38")], 0, 0, 1, 1))
    sx, sy, sw, sh = 44, 78, 112, 88
    ic.rect(sx, sy, sw, sh, rx=8, fill=glass_dark(ic, "#0F4426"))
    for i in range(1, 10):
        x = sx + sw * i / 10
        ic.line(x, sy + 3, x, sy + sh - 3, stroke="#4FBF78", stroke_opacity=0.32 if i == 5 else 0.14,
                stroke_width=0.7)
    for i in range(1, 8):
        y = sy + sh * i / 8
        ic.line(sx + 3, y, sx + sw - 3, y, stroke="#4FBF78", stroke_opacity=0.32 if i == 4 else 0.14,
                stroke_width=0.7)
    # the trace: load, mostly low, two bursts
    ys = [150, 148, 151, 146, 149, 132, 112, 128, 145, 150, 147, 149, 140, 120, 104, 118, 138, 148, 151, 146, 149,
          147, 150, 142, 146, 149]
    pts = [(sx + 4 + i * (sw - 8) / (len(ys) - 1), y) for i, y in enumerate(ys)]
    d = "M" + "L".join(f"{x:.1f} {y}" for x, y in pts)
    ic.path(d, fill="none", stroke="#5CFF9A", stroke_opacity=0.22, stroke_width=6, stroke_linejoin="round",
            stroke_linecap="round")
    ic.path(d, fill="none", stroke="#A8FFC8", stroke_width=1.8, stroke_linejoin="round", stroke_linecap="round")
    ic.text("CPU 12% · 3.1 GHz", sx + 6, sy + 13, 8.5, font="mono-semibold", fill="#7CF7A6")
    ic.text("500 ms/div", sx + sw - 5, sy + sh - 5, 6, font="mono", anchor="end", fill="#4FBF78", opacity=0.8)
    ic.path(f"M{sx} {sy + 8}a8 8 0 0 1 8-8h50L{sx + 20} {sy + sh}H{sx + 8}a8 8 0 0 1-8-8z", fill=glare(ic, 0.8))
    # the controls
    for x, label in ((184, "VOLTS"), (212, "TIME")):
        ic.text(label, x, 80, 5.5, font="mono-semibold", anchor="middle", fill="#5A5446")
        ic.circle(x + 1, 98.5, 12, fill="#000", opacity=0.22)
        ic.circle(x, 97, 12, fill=graphite(ic))
        ic.circle(x, 97, 8.5, fill=ic.lin([(0, "#5A5F66"), (1, "#24272B")], 0, 0, 1, 1))
        ic.circle(x, 97, 12, fill="none", stroke="#fff", stroke_opacity=0.12)
        ic.rect(x - 1, 86, 2, 7, rx=1, fill="#F1EDE3", transform=f"rotate({-40 if x < 200 else 30} {x} 97)")
    for x in (176, 192, 208):
        ic.circle(x, 126, 6, fill=graphite(ic))
        ic.circle(x, 126, 6, fill="none", stroke="#fff", stroke_opacity=0.14)
        ic.rect(x - 0.6, 121, 1.2, 4, fill="#F1EDE3")
    ic.text("CH1", 182, 148, 5.5, font="mono-semibold", anchor="middle", fill="#5A5446")
    ic.text("CH2", 208, 148, 5.5, font="mono-semibold", anchor="middle", fill="#5A5446")
    for x in (182, 208):
        ic.circle(x, 162, 8, fill=steel(ic, horizontal=False))
        ic.circle(x, 162, 4, fill="#C99645")
        ic.circle(x, 162, 1.5, fill="#3A2A10")
    # brand
    mark(ic, 40, 178, 10, fill="#5A5446")
    ic.text("INUA  SM-1", 54, 186.5, 7, font="mono-semibold", spacing=0.6, fill="#5A5446")
    ic.circle(156, 183, 3, fill="#7CF7A6")
    ic.circle(156, 183, 3, fill="none", stroke="#2A5A3A", stroke_width=0.8)
    # the probe's lead
    ic.path("M182 170C182 196 210 200 238 196", fill="none", stroke="#1A1C1E", stroke_width=4.5,
            stroke_linecap="round")


@small("SystemMonitor")
def systemmonitor16(ic):
    tile(ic, "#33664A", "#12301F")
    ic.rect(1.5, 3.5, 13, 9.5, rx=1, fill="#DDD7C8")
    ic.rect(2.5, 4.5, 7.5, 7.5, rx=0.8, fill="#0B2A17")
    ic.path("M3 10 L4.5 10 L5.5 6 L6.5 9 L7.5 7.5 L9.5 10", fill="none", stroke="#7CF7A6", stroke_width=0.9,
            stroke_linejoin="round", stroke_linecap="round")
    ic.circle(12.3, 6.2, 1.2, fill="#2A2C30")
    ic.circle(12.3, 9.8, 1.2, fill="#2A2C30")


# --- Disk Usage: an open hard disk, its platter in inua's ring colours --------

@icon("DiskUsage")
def diskusage(ic):
    tile(ic, "#B5693C", "#5E2C12")
    shadow(ic, 128, 222, 86, 10)
    # casing, and its well
    ic.rect(50, 24, 156, 198, rx=12, fill="#000", opacity=0.25, transform="translate(2 3)")
    ic.rect(50, 24, 156, 198, rx=12, fill=ic.lin([(0, "#EEF0F2"), (0.5, "#BFC4CA"), (1, "#868D96")], 0, 0, 1, 1))
    ic.rect(50.75, 24.75, 154.5, 196.5, rx=11.25, fill="none", stroke="#fff", stroke_opacity=0.6, stroke_width=1.5)
    ic.path("M60 44a10 10 0 0 1 10-10h116a10 10 0 0 1 10 10v128a10 10 0 0 1-10 10h-10l-14 14h-92a10 10 0 0 1-10-10z",
            fill=ic.lin([(0, "#5D636B"), (1, "#A9AFB6")], 0, 0, 1, 1))
    for x, y in ((58, 32), (198, 32), (58, 214), (198, 214), (128, 214)):
        screw(ic, x, y, 3)
    # platter
    cx, cy, R = 128, 106, 66
    ic.circle(cx + 2, cy + 3, R, fill="#000", opacity=0.3)
    ic.circle(cx, cy, R, fill=ic.rad([(0, "#F4F6F8"), (0.7, "#B9C0C8"), (1, "#8A929C")], cx=0.4, cy=0.35, r=0.75))
    sheen = ic.lin([(0, "#fff", 0), (0.5, "#fff", 0.55), (1, "#fff", 0)], 0, 0, 1, 1)
    ic.path(f"M{cx} {cy}L{cx - 50} {cy - 43}A66 66 0 0 1 {cx - 12} {cy - 65}z", fill=sheen)
    ic.path(f"M{cx} {cy}L{cx + 50} {cy + 43}A66 66 0 0 1 {cx + 12} {cy + 65}z", fill=sheen, opacity=0.6)
    # usage rings: home, caches, the agents'
    for r, end, col in ((56, 248, ACCENT), (44, 118, WARN), (32, 296, OK)):
        ic.circle(cx, cy, r, fill="none", stroke="#2A2E33", stroke_opacity=0.18, stroke_width=8)
        ic.path(arc(cx, cy, r, 0, end), fill="none", stroke=col, stroke_width=8, stroke_linecap="round")
        ic.path(arc(cx, cy, r + 2.6, 4, min(end, 80) - 4), fill="none", stroke="#fff", stroke_opacity=0.35,
                stroke_width=1.2, stroke_linecap="round")
    ic.circle(cx, cy, R, fill="none", stroke="#5D636B", stroke_opacity=0.6, stroke_width=1.2)
    # spindle
    ic.circle(cx, cy, 17, fill=steel(ic, horizontal=False))
    ic.circle(cx, cy, 17, fill="none", stroke="#3A3F46", stroke_opacity=0.5)
    for k in range(6):
        x, y = polar(cx, cy, 10.5, k * 60 + 30)
        ic.circle(x, y, 1.8, fill="#4A5058")
    ic.circle(cx, cy, 5, fill=ic.rad([(0, "#E8ECEF"), (1, "#6B727B")], cx=0.35, cy=0.35))
    # the read arm, from its pivot, its head over the blue ring
    px, py = 178, 178
    hx, hy = polar(cx, cy, 54, 120)
    ang = math.degrees(math.atan2(hy - py, hx - px))
    L = math.hypot(hx - px, hy - py)
    ic.path("M186 196a18 14 0 0 1 10-24l8 2v24z", fill="#2A2C30")
    with ic.g(transform=f"translate({px} {py}) rotate({ang:.1f})", opacity=0.3):
        ic.path(f"M0 -10L{L - 6} -3L{L + 6} -3L{L + 6} 3L{L - 6} 3L0 10z", fill="#000", transform="translate(2 4)")
    with ic.g(transform=f"translate({px} {py}) rotate({ang:.1f})"):
        ic.path(f"M0 -10L{L - 6} -3L{L + 6} -3L{L + 6} 3L{L - 6} 3L0 10z",
                fill=ic.lin([(0, "#E3E6EA"), (0.5, "#A9AFB6"), (1, "#6B727B")]))
        ic.path(f"M14 -2.5L{L - 12} -1.2L{L - 12} 1.2L14 2.5z", fill="#5D636B", opacity=0.6)
        ic.rect(L - 4, -4.5, 9, 9, rx=1.5, fill="#2A2C30")
        ic.line(4, -8.6, L - 6, -2.4, stroke="#fff", stroke_opacity=0.7, stroke_width=1)
    ic.circle(px, py, 13, fill=graphite(ic))
    ic.circle(px, py, 13, fill="none", stroke="#fff", stroke_opacity=0.18)
    ic.circle(px, py, 6, fill=steel(ic, horizontal=False))
    ic.circle(px, py, 2, fill="#2A2C30")
    # the casing's marking
    mark(ic, 72, 187, 11, fill="#2A2E33", opacity=0.75)
    ic.text("INUA", 87, 196, 9, font="mono-semibold", spacing=1, fill="#2A2E33", opacity=0.8)
    ic.text("2 TB · 7200 RPM", 72, 208, 6.5, font="mono", fill="#2A2E33", opacity=0.7)


@small("DiskUsage")
def diskusage16(ic):
    tile(ic, "#B5693C", "#5E2C12")
    ic.rect(3, 1.5, 10, 13, rx=1.2, fill="#C3C8CE")
    ic.circle(8, 7, 4.4, fill="#E8ECEF")
    ic.path(arc(8, 7, 3.6, 0, 250), fill="none", stroke=ACCENT, stroke_width=1.3)
    ic.path(arc(8, 7, 2.1, 0, 290), fill="none", stroke=OK, stroke_width=1.2)
    ic.circle(8, 7, 0.8, fill="#5D636B")
    ic.path("M11.5 12.8L7.6 9.7", stroke="#4A5058", stroke_width=1, stroke_linecap="round")


# --- Stocks: a newspaper's market page --------------------------------------

@icon("Stocks")
def stocks(ic):
    tile(ic, "#2F5E4E", "#10291F")
    shadow(ic, 128, 212, 106, 12)
    with ic.g(transform="rotate(5 128 124)"):
        ic.rect(38, 36, 182, 176, rx=2, fill=paper(ic, "newsprint"))
        ic.rect(38, 36, 182, 176, rx=2, fill="#000", opacity=0.12)
    with ic.g(transform="rotate(-3 128 124)"):
        ic.rect(30, 30, 194, 180, rx=2, fill="#000", opacity=0.25, transform="translate(2 3)")
        ic.rect(30, 30, 194, 180, rx=2, fill=ic.lin([(0, "#F4F1E8"), (1, "#D9D3C4")], 0, 0, 1, 1))
        ic.line(30, 30.8, 224, 30.8, stroke="#fff", stroke_width=1.5)
        # masthead
        ic.text("MARKETS", 40, 52, 17, font="sans-bold", spacing=1.5, fill="#1E1E20")
        ic.text("Friday, 30 October 2026", 214, 51, 6, font="mono", anchor="end", fill="#55534E")
        ic.line(40, 58, 214, 58, stroke="#1E1E20", stroke_width=1.6)
        ic.line(40, 61, 214, 61, stroke="#1E1E20", stroke_width=0.6)
        # headline, the price in green
        w = ic.text("INUA ", 40, 84, 21, font="sans-bold", fill="#1E1E20")
        ic.poly([(40 + w, 82), (48 + w, 70), (56 + w, 82)], fill=UP)
        ic.text("+2.4%", 60 + w, 84, 21, font="sans-bold", fill=UP)
        ic.text("Desk makers rally on a quiet Friday", 40, 95, 7.5, font="sans-medium", fill="#55534E")
        # the chart
        bx, by, bw, bh = 40, 102, 110, 70
        ic.rect(bx, by, bw, bh, fill="#FBF9F3", stroke="#B8B2A4", stroke_width=0.8)
        for i in range(1, 4):
            ic.line(bx + 2, by + bh * i / 4, bx + bw - 2, by + bh * i / 4, stroke="#B8B2A4", stroke_width=0.5,
                    stroke_dasharray="2 2")
        candles = [(150, 160, 146, 163), (160, 154, 151, 164), (154, 146, 143, 157), (146, 151, 141, 154),
                   (151, 139, 135, 153), (139, 132, 128, 142), (132, 138, 129, 141), (138, 126, 122, 140),
                   (126, 118, 114, 129), (118, 122, 115, 125), (122, 110, 106, 124)]
        for k, (o, c, hi, lo) in enumerate(candles):
            x = bx + 9 + k * 9.2
            col = UP if c < o else DOWN
            ic.line(x, hi, x, lo, stroke=col, stroke_width=1.2)
            ic.rect(x - 3, min(o, c), 6, max(abs(o - c), 1.5), fill=col)
        ic.text("INUA · 1 month", bx + 4, by + 9, 6, font="mono-semibold", fill="#55534E")
        # the table
        rows = [("INUA", "42.18", True), ("NEST", "17.05", True), ("KYTO", "88.40", False), ("HKDO", "9.72", True),
                ("WASH", "31.66", False), ("RINK", "5.14", True)]
        ic.line(158, 102, 158, 172, stroke="#B8B2A4", stroke_width=0.6)
        for k, (sym, price, up) in enumerate(rows):
            y = 110 + k * 11.6
            ic.text(sym, 164, y, 7, font="mono-semibold", fill="#1E1E20")
            ic.text(price, 207, y, 7, font="mono", anchor="end", fill="#3A3836")
            if up:
                ic.poly([(209, y - 1), (215, y - 1), (212, y - 6)], fill=UP)
            else:
                ic.poly([(209, y - 6), (215, y - 6), (212, y - 1)], fill=DOWN)
        # columns of text
        for col in range(3):
            x = 40 + col * 59
            for j in range(4):
                ln = 52 if (j + col) % 4 != 3 else 34
                ic.rect(x, 180 + j * 6.5, ln, 2.4, fill="#8C887F", opacity=0.7)
        # the fold
        ic.rect(30, 118, 194, 6, fill=ic.lin([(0, "#000", 0), (0.5, "#000", 0.08), (1, "#fff", 0.2)]))


@small("Stocks")
def stocks16(ic):
    tile(ic, "#2F5E4E", "#10291F")
    ic.rect(2, 2, 12, 12, rx=0.6, fill="#EEEADF")
    ic.rect(3.2, 3.2, 6, 1.4, fill="#1E1E20")
    for k, (top, h, col) in enumerate(((9, 3, UP), (8, 2.5, DOWN), (6.5, 3.5, UP), (5.5, 2.5, UP))):
        x = 3.6 + k * 2.4
        ic.rect(x - 0.15, top - 0.8, 0.3, h + 1.6, fill=col)
        ic.rect(x - 0.7, top, 1.4, h, fill=col)
