"""The inua-objects theme, remote desktops, VPNs and secrets: Remmina,
AnyDesk, TeamViewer, RustDesk, Parsec, WireGuard, Mullvad VPN, 1Password,
Proton Pass, Authenticator, Cryptomator, VeraCrypt
(docs/feat/object-icons.md, Part 2)."""

from lib import (brass, glare, graphite, icon, paper, polar, shadow, small, steel, tile, wood)


# --- shared --------------------------------------------------------------

def _engraved(ic, s, x, y, size, fill, light="#fff", dark="#000", lo=0.35, do=0.35, **kw):
    """Text cut into a surface: a light edge below right, a dark one above left."""
    ic.text(s, x + 0.6, y + 0.6, size, fill=light, opacity=lo, **kw)
    ic.text(s, x - 0.5, y - 0.5, size, fill=dark, opacity=do, **kw)
    ic.text(s, x, y, size, fill=fill, **kw)


def _screw(ic, x, y, r=4, slot=30):
    ic.circle(x + 0.6, y + 0.8, r, fill="#000", opacity=0.3)
    ic.circle(x, y, r, fill=ic.lin([(0, "#E9ECEF"), (1, "#6F767E")], 0, 0, 1, 1))
    with ic.g(transform=f"rotate({slot} {x} {y})"):
        ic.rect(x - r * 0.75, y - 0.6, r * 1.5, 1.2, fill="#3A3E44")


def _cursor(ic, x, y, k=1.0, fill="#fff", edge="#1A1C20"):
    """A pointer arrow, its tip at (x, y)."""
    d = (f"M{x} {y}l0 {17 * k}l{4.2 * k} {-4 * k}l{3 * k} {6.6 * k}l{2.8 * k} {-1.3 * k}"
         f"l{-3 * k} {-6.4 * k}l{6 * k} 0z")
    ic.path(d, fill="#000", opacity=0.3, transform="translate(1 1.5)")
    ic.path(d, fill=fill, stroke=edge, stroke_width=1.1 * k, stroke_linejoin="round")


def _padlock(ic, cx, top, w, body_fill, shackle="#C3C8CE"):
    """A padlock: its shackle's top at top, w wide; returns the body's top."""
    h = w * 0.82
    by = top + w * 0.55
    sw = w * 0.16
    ic.path(f"M{cx - w * 0.3} {by + 2}V{top + w * 0.3}a{w * 0.3} {w * 0.3} 0 0 1 {w * 0.6} 0V{by + 2}",
            fill="none", stroke="#000", stroke_opacity=0.35, stroke_width=sw, transform="translate(1.5 2)")
    ic.path(f"M{cx - w * 0.3} {by + 2}V{top + w * 0.3}a{w * 0.3} {w * 0.3} 0 0 1 {w * 0.6} 0V{by + 2}",
            fill="none", stroke=shackle, stroke_width=sw)
    ic.path(f"M{cx - w * 0.3 - sw * 0.3} {by}V{top + w * 0.3}a{w * 0.3 + sw * 0.3} {w * 0.3 + sw * 0.3} 0 0 1 "
            f"{w * 0.3} {-(w * 0.3)}", fill="none", stroke="#fff", stroke_opacity=0.6, stroke_width=sw * 0.25)
    ic.rect(cx - w / 2 + 1.5, by + 2.5, w, h, rx=w * 0.12, fill="#000", opacity=0.35)
    ic.rect(cx - w / 2, by, w, h, rx=w * 0.12, fill=body_fill)
    ic.rect(cx - w / 2 + 0.75, by + 0.75, w - 1.5, h - 1.5, rx=w * 0.12, fill="none", stroke="#fff",
            stroke_opacity=0.35, stroke_width=1.5)
    return by, h


# --- Remmina: a tablet on its folio stand, a remote desktop on it ------------

@icon("remmina", kind="app", names=["org.remmina.Remmina", "remmina"], title="Remmina")
def remmina(ic):
    tile(ic, "#3E7AA8", "#173A5C")
    shadow(ic, 128, 210, 104, 12)
    # the folio's back flap, propping it up
    ic.path("M70 204 L96 150 H160 L186 204 Z", fill=ic.lin([(0, "#2A4868"), (1, "#122236")]))
    ic.line(74, 202, 98, 152, stroke="#fff", stroke_opacity=0.15, stroke_width=1.5)
    with ic.g(transform="rotate(-3 128 128)"):
        # the tablet
        ic.rect(26, 48, 204, 150, rx=18, fill="#000", opacity=0.35, transform="translate(2 4)")
        ic.rect(26, 48, 204, 150, rx=18, fill=ic.lin([(0, "#4A5058"), (0.1, "#2A2E33"), (1, "#121417")]))
        ic.rect(26.75, 48.75, 202.5, 148.5, rx=17.25, fill="none", stroke="#fff", stroke_opacity=0.18,
                stroke_width=1.5)
        ic.circle(128, 55.5, 2, fill="#2F3B48")
        # the screen: a remote desktop
        sx, sy, sw, sh = 37, 62, 182, 126
        clip = ic.clip(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="5"/>')
        with ic.g(clip_path=clip):
            ic.rect(sx, sy, sw, sh, fill=ic.lin([(0, "#7FC2E8"), (0.6, "#3C87C4"), (1, "#22528A")], 0, 0, 1, 1))
            ic.path(f"M{sx} {sy + 104} Q{sx + 60} {sy + 70} {sx + 120} {sy + 96} T{sx + sw} {sy + 84} V{sy + sh} "
                    f"H{sx}z", fill="#1E4A7A", opacity=0.6)
            # Remmina's own bar on top: the connection's name
            ic.rect(sx, sy, sw, 15, fill="#16222F", opacity=0.92)
            ic.circle(sx + 9, sy + 7.5, 3, fill="#5BD06A")
            ic.text("Remmina  ·  RDP studio-pc", sx + 16, sy + 11, 8, font="mono-semibold", fill="#DCE7F2")
            for i, c in enumerate(("#E8EEF4", "#E8EEF4", "#E05A4B")):
                ic.rect(sx + sw - 34 + i * 11, sy + 4, 7, 7, rx=1.5, fill=c, opacity=0.85)
            # the far computer's window
            ic.rect(sx + 22, sy + 28, 112, 78, rx=4, fill="#000", opacity=0.25, transform="translate(2 3)")
            ic.rect(sx + 22, sy + 28, 112, 78, rx=4, fill="#FBFAF7")
            ic.rect(sx + 22, sy + 28, 112, 13, rx=4, fill="#E3E7EC")
            ic.rect(sx + 22, sy + 36, 112, 5, fill="#E3E7EC")
            for i, c in enumerate(("#E05A4B", "#E9B949", "#5BBF6A")):
                ic.circle(sx + 30 + i * 8, sy + 34.5, 2.4, fill=c)
            ic.text("Quarterly.ods", sx + 78, sy + 37.5, 7, font="sans-semibold", anchor="middle", fill="#4E5560")
            for r in range(4):
                for c in range(3):
                    ic.rect(sx + 30 + c * 33, sy + 48 + r * 13, 30, 10, fill="#EEF1F4" if r else "#D4E6F6")
            ic.rect(sx + 96, sy + 61, 30, 10, fill="none", stroke="#2F7FD0", stroke_width=1.5)
            ic.text("1,024", sx + 124, sy + 69, 7, font="mono-semibold", anchor="end", fill="#2B3B4E")
            # a second window, behind on the right
            ic.rect(sx + 120, sy + 52, 54, 60, rx=4, fill="#2A3340")
            ic.rect(sx + 120, sy + 52, 54, 10, rx=4, fill="#3A4554")
            for k in range(4):
                ic.rect(sx + 126, sy + 68 + k * 9, 30 - k * 5, 3, rx=1.5, fill="#8FD7A0", opacity=0.7)
            # the far side's taskbar
            ic.rect(sx, sy + sh - 11, sw, 11, fill="#0F1A26", opacity=0.85)
            for k in range(5):
                ic.rect(sx + 8 + k * 12, sy + sh - 8, 7, 5, rx=1, fill="#9CC8EC", opacity=0.8 if k else 1)
            ic.text("14:32", sx + sw - 6, sy + sh - 3, 6.5, font="mono", anchor="end", fill="#DCE7F2")
            _cursor(ic, sx + 88, sy + 74, 0.9)
            ic.path(f"M{sx} {sy}h96L{sx + 30} {sy + sh}H{sx}z", fill=glare(ic, 1.1))


@small("remmina")
def remmina16(ic):
    tile(ic, "#3E7AA8", "#173A5C")
    ic.rect(1.5, 3, 13, 10, rx=1.3, fill="#24282D")
    ic.rect(2.5, 4, 11, 8, rx=0.5, fill="#4C98D2")
    ic.rect(2.5, 4, 11, 1.2, fill="#16222F")
    ic.rect(4, 6, 6.5, 4.6, rx=0.3, fill="#FBFAF7")
    ic.path("M9.5 7.5v3.6l1-.9 .8 1.4 .6-.3-.7-1.3h1.3z", fill="#1A1C20")


# --- AnyDesk: a white remote control, its red diamond badge -----------------

def _anydesk_mark(ic, cx, cy, r, red="#EF443B", white="#FFFFFF"):
    """Two diamonds, one in the other."""
    def dia(rr):
        return f"M{cx} {cy - rr}L{cx + rr} {cy}L{cx} {cy + rr}L{cx - rr} {cy}Z"
    ic.path(dia(r), fill=red, stroke=red, stroke_width=r * 0.18, stroke_linejoin="round")
    ic.path(dia(r * 0.62), fill=white, stroke=white, stroke_width=r * 0.1, stroke_linejoin="round")
    ic.path(dia(r * 0.3), fill=red, stroke=red, stroke_width=r * 0.06, stroke_linejoin="round")


@icon("anydesk", kind="app", names=["anydesk", "com.anydesk.Anydesk"], title="AnyDesk")
def anydesk(ic):
    tile(ic, "#C2453B", "#6A1A14")
    shadow(ic, 128, 214, 70, 11)
    with ic.g(transform="rotate(-18 128 124)"):
        x, y, w, h = 88, 22, 80, 206
        ic.rect(x, y, w, h, rx=30, fill="#000", opacity=0.35, transform="translate(4 6)")
        ic.rect(x, y, w, h, rx=30, fill=ic.lin([(0, "#FFFFFF"), (0.5, "#ECECEA"), (1, "#BDBDB9")], 0, 0, 1, 0))
        ic.rect(x + 0.75, y + 0.75, w - 1.5, h - 1.5, rx=29, fill="none", stroke="#fff", stroke_width=1.5)
        ic.rect(x + 66, y + 20, 8, h - 40, rx=4, fill="#000", opacity=0.06)
        # the IR window at the tip
        ic.path(f"M{x + 22} {y + 3}h36a28 28 0 0 1 14 6H{x + 8}a28 28 0 0 1 14 -6z", fill="#2A1A1A")
        # power
        ic.circle(x + 60, y + 26, 7, fill="#B32A22")
        ic.circle(x + 60, y + 25, 7, fill="#EF443B")
        ic.path(f"M{x + 57} {y + 22}a4 4 0 1 0 6 0", fill="none", stroke="#fff", stroke_width=1.4,
                stroke_linecap="round")
        ic.line(x + 60, y + 20, x + 60, y + 25, stroke="#fff", stroke_width=1.4, stroke_linecap="round")
        # the ring of arrows and OK
        cx, cy = x + 40, y + 66
        ic.circle(cx, cy + 1.5, 26, fill="#9A9A96")
        ic.circle(cx, cy, 26, fill=ic.lin([(0, "#4C4F55"), (1, "#24262A")], 0, 0, 1, 1))
        for a in (0, 90, 180, 270):
            ax, ay = polar(cx, cy, 19, a)
            ic.path(f"M{ax} {ay - 3}l3 5h-6z", fill="#D7D7D3", transform=f"rotate({a} {ax} {ay})")
        ic.circle(cx, cy + 1, 11, fill="#111214")
        ic.circle(cx, cy, 11, fill=ic.lin([(0, "#F4F4F2"), (1, "#C7C7C3")], 0, 0, 1, 1))
        ic.text("OK", cx, cy + 3, 8, font="sans-bold", anchor="middle", fill="#3A3C40")
        # number keys
        n = 1
        for r in range(3):
            for c in range(3):
                kx, ky = x + 18 + c * 22, y + 102 + r * 19
                ic.rect(kx - 8, ky - 5, 16, 12, rx=5, fill="#A9A9A5")
                ic.rect(kx - 8, ky - 6, 16, 12, rx=5, fill=ic.lin([(0, "#5A5D63"), (1, "#2C2E33")]))
                ic.text(str(n), kx, ky + 3, 7.5, font="sans-semibold", anchor="middle", fill="#F1F1EF")
                n += 1
        # the badge: red enamel in a chrome bezel
        bx, by = x + 40, y + 178
        ic.circle(bx + 1, by + 2, 17, fill="#000", opacity=0.25)
        ic.circle(bx, by, 17, fill=steel(ic, False))
        ic.circle(bx, by, 14.5, fill="#FFFFFF")
        _anydesk_mark(ic, bx, by, 10.5)
        ic.path(f"M{bx - 12} {by - 4}a13 13 0 0 1 9 -9", fill="none", stroke="#fff", stroke_opacity=0.9,
                stroke_width=1.5, stroke_linecap="round")
        ic.text("AnyDesk", bx, by - 21, 7, font="sans-bold", anchor="middle", fill="#B32A22")
        # the plastic's sheen, down the left
        ic.rect(x + 7, y + 30, 5, h - 60, rx=2.5, fill="#fff", opacity=0.8)


@small("anydesk")
def anydesk16(ic):
    tile(ic, "#C2453B", "#6A1A14")
    with ic.g(transform="rotate(-18 8 8)"):
        ic.rect(5, 1.2, 6, 13.6, rx=2.4, fill="#F4F4F2")
        ic.circle(8, 4.6, 1.7, fill="#3A3C40")
        ic.path("M8 8.6 L10.3 10.9 L8 13.2 L5.7 10.9Z", fill="#EF443B")
        ic.path("M8 10 L8.9 10.9 L8 11.8 L7.1 10.9Z", fill="#fff")


# --- TeamViewer: two monitors, the blue double-arrow badge between them ------

def _monitor(ic, x, y, w, h, stand=True):
    if stand:
        ic.path(f"M{x + w / 2 - 10} {y + h - 2}h20l5 {22}h-30z", fill=steel(ic))
        ic.rect(x + w / 2 - 24, y + h + 18, 48, 7, rx=3.5, fill=steel(ic))
    ic.rect(x, y, w, h, rx=8, fill="#000", opacity=0.35, transform="translate(2 4)")
    ic.rect(x, y, w, h, rx=8, fill=ic.lin([(0, "#4A5058"), (0.1, "#2D3238"), (1, "#15181B")]))
    ic.rect(x + 0.75, y + 0.75, w - 1.5, h - 1.5, rx=7.25, fill="none", stroke="#fff", stroke_opacity=0.14,
            stroke_width=1.5)
    return x + 6, y + 6, w - 12, h - 14


def _tv_desktop(ic, sx, sy, sw, sh, light=True):
    clip = ic.clip(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="3"/>')
    with ic.g(clip_path=clip):
        ic.rect(sx, sy, sw, sh, fill=ic.lin([(0, "#BFE0FA"), (1, "#5FA6E0")] if light else
                                         [(0, "#2E5A86"), (1, "#14304E")], 0, 0, 1, 1))
        ic.rect(sx + sw * 0.12, sy + sh * 0.18, sw * 0.56, sh * 0.5, rx=2, fill="#FFFFFF", opacity=0.95)
        ic.rect(sx + sw * 0.12, sy + sh * 0.18, sw * 0.56, sh * 0.1, rx=2, fill="#D9E2EC")
        for k in range(3):
            ic.rect(sx + sw * 0.17, sy + sh * (0.36 + k * 0.09), sw * (0.4 - k * 0.08), sh * 0.04, fill="#9AA6B2")
        ic.rect(sx, sy + sh - 6, sw, 6, fill="#0E2238", opacity=0.8)
        ic.path(f"M{sx} {sy}h{sw * 0.5}L{sx + sw * 0.15} {sy + sh}H{sx}z", fill=glare(ic))


@icon("teamviewer", kind="app", names=["TeamViewer", "com.teamviewer.TeamViewer", "teamviewer"], title="TeamViewer")
def teamviewer(ic):
    tile(ic, "#2F6FB4", "#0E3466")
    shadow(ic, 128, 212, 108, 12)
    # the far monitor, left and behind
    s = _monitor(ic, 18, 48, 120, 90)
    _tv_desktop(ic, *s, light=False)
    # the near monitor, right
    s = _monitor(ic, 106, 70, 132, 100)
    _tv_desktop(ic, *s)
    # the badge, between them: blue enamel, a white ring and the double arrow
    cx, cy, r = 112, 150, 38
    ic.circle(cx + 2, cy + 4, r + 4, fill="#000", opacity=0.35)
    ic.circle(cx, cy, r + 4, fill=steel(ic, False))
    ic.circle(cx, cy, r, fill=ic.rad([(0, "#5BB6FF"), (0.6, "#1A85EE"), (1, "#0A4FA8")], cx=0.35, cy=0.3, r=0.8))
    ic.circle(cx, cy, r - 4.5, fill="none", stroke="#fff", stroke_width=3)
    arrow = (f"M{cx - 25} {cy}l12 -11v6.5"
             f"c6 -3.5 20 -3.5 26 0v-6.5l12 11l-12 11v-6.5c-6 3.5 -20 3.5 -26 0v6.5z")
    ic.path(arrow, fill="#0A3D85", opacity=0.45, transform="translate(1 1.5)")
    ic.path(arrow, fill="#fff")
    ic.path(f"M{cx - 30} {cy - 12}a32 32 0 0 1 26 -22 34 34 0 0 0 -26 22z", fill="#fff", opacity=0.45)


@small("teamviewer")
def teamviewer16(ic):
    tile(ic, "#2F6FB4", "#0E3466")
    ic.rect(1.5, 2.5, 7.5, 5.5, rx=0.6, fill="#2A2E33")
    ic.rect(6.5, 4, 8, 6, rx=0.6, fill="#2A2E33")
    ic.rect(7.3, 4.8, 6.4, 4.2, fill="#8EC6F2")
    ic.circle(7, 10.5, 4, fill="#1A85EE")
    ic.circle(7, 10.5, 4, fill="none", stroke="#fff", stroke_width=0.5)
    ic.path("M4.3 10.5l1.4-1.4v.8h2.6v-.8l1.4 1.4-1.4 1.4v-.8H5.7v.8z", fill="#fff")


# --- RustDesk: a rust-orange toolbox, a screen set in its side --------------

@icon("rustdesk", kind="app", names=["com.rustdesk.RustDesk", "rustdesk"], title="RustDesk")
def rustdesk(ic):
    tile(ic, "#2D4C7C", "#11223F")
    shadow(ic, 128, 212, 104, 12)
    enamel_o = ic.lin([(0, "#F08A4B"), (0.5, "#D2622B"), (1, "#8E3512")], 0, 0, 1, 1)
    # the handle, steel, folded up
    ic.path("M86 70 V50 a10 10 0 0 1 10 -10 h64 a10 10 0 0 1 10 10 V70", fill="none", stroke="#000",
            stroke_opacity=0.35, stroke_width=9, transform="translate(2 3)")
    ic.path("M86 70 V50 a10 10 0 0 1 10 -10 h64 a10 10 0 0 1 10 10 V70", fill="none", stroke=steel(ic),
            stroke_width=8)
    ic.rect(104, 34, 48, 12, rx=6, fill=ic.lin([(0, "#3A3C40"), (1, "#151618")]))
    for x in (80, 164):
        ic.rect(x, 60, 12, 18, rx=3, fill=steel(ic))
    # the lid
    ic.rect(28, 70, 200, 34, rx=7, fill="#000", opacity=0.35, transform="translate(2 4)")
    ic.rect(28, 70, 200, 34, rx=7, fill=enamel_o)
    ic.line(34, 71.5, 222, 71.5, stroke="#FFD2B0", stroke_width=2, opacity=0.8)
    ic.rect(28, 98, 200, 6, fill="#000", opacity=0.18)
    # the box
    ic.path("M34 104 H222 L216 206 a6 6 0 0 1 -6 6 H46 a6 6 0 0 1 -6 -6 Z", fill="#000", opacity=0.3,
            transform="translate(2 3)")
    ic.path("M34 104 H222 L216 206 a6 6 0 0 1 -6 6 H46 a6 6 0 0 1 -6 -6 Z", fill=enamel_o)
    ic.line(34, 104.5, 222, 104.5, stroke="#5A1E08", stroke_opacity=0.6, stroke_width=1.5)
    ic.line(35, 106, 41, 205, stroke="#FFD2B0", stroke_opacity=0.5, stroke_width=1.5)
    # rust, worn through the paint at the edges
    for px, py, pr in ((44, 196, 5), (52, 202, 3), (210, 120, 4), (206, 196, 6), (214, 188, 3), (40, 80, 3),
                       (218, 86, 4), (70, 74, 2), (190, 200, 3)):
        ic.circle(px, py, pr, fill="#6E2A0E", opacity=0.55)
        ic.circle(px - 0.6, py - 0.6, pr * 0.5, fill="#A8521E", opacity=0.6)
    # latches
    for x in (54, 186):
        ic.rect(x, 88, 16, 26, rx=3, fill="#000", opacity=0.3, transform="translate(1 2)")
        ic.rect(x, 88, 16, 26, rx=3, fill=steel(ic))
        ic.rect(x + 3, 104, 10, 6, rx=1.5, fill="#4A4E54")
    # the screen in the side, glass in a black bezel
    ic.rect(70, 120, 116, 72, rx=8, fill="#14161A")
    ic.rect(70.75, 120.75, 114.5, 70.5, rx=7.25, fill="none", stroke="#fff", stroke_opacity=0.15,
            stroke_width=1.5)
    sx, sy, sw, sh = 77, 127, 102, 58
    clip = ic.clip(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="3"/>')
    with ic.g(clip_path=clip):
        ic.rect(sx, sy, sw, sh, fill=ic.lin([(0, "#2A6BE8"), (1, "#0D2E80")], 0, 0, 1, 1))
        ic.rect(sx + 10, sy + 10, 58, 36, rx=2, fill="#F4F6FA")
        ic.rect(sx + 10, sy + 10, 58, 7, rx=2, fill="#D2DAE6")
        ic.text("ID 418 205 773", sx + 14, sy + 27, 6, font="mono-semibold", fill="#2A3442")
        ic.rect(sx + 14, sy + 33, 34, 7, rx=2, fill="#2A6BE8")
        ic.text("Connect", sx + 31, sy + 38.5, 5, font="sans-semibold", anchor="middle", fill="#fff")
        _cursor(ic, sx + 46, sy + 36, 0.7)
        ic.path(f"M{sx} {sy}h{sw * 0.55}L{sx + 18} {sy + sh}H{sx}z", fill=glare(ic, 1.2))
    # the maker's plate under the screen
    ic.rect(98, 196, 60, 11, rx=2, fill=brass(ic))
    ic.text("RUSTDESK", 128, 204.5, 7, font="mono-semibold", anchor="middle", spacing=1.4, fill="#4A3410")


@small("rustdesk")
def rustdesk16(ic):
    tile(ic, "#2D4C7C", "#11223F")
    ic.path("M5.5 5V3.2h5V5", fill="none", stroke="#C3C8CE", stroke_width=1)
    ic.rect(1.5, 5, 13, 2.4, rx=0.6, fill="#E87A3D")
    ic.rect(2, 7.4, 12, 6.2, rx=0.6, fill="#D2622B")
    ic.rect(4.8, 8.4, 6.4, 4, rx=0.4, fill="#14161A")
    ic.rect(5.4, 9, 5.2, 2.8, fill="#2A6BE8")


# --- Parsec: a gamepad on a star chart, the mark on its middle --------------

def _parsec_mark(ic, cx, cy, s, fill):
    """Three bars, staggered."""
    for dx, dy, w in ((-0.15, -1, 1.0), (0.15, 0, 1.0), (-0.15, 1, 1.0)):
        ic.rect(cx + dx * s - w * s * 0.5, cy + dy * s * 0.42 - s * 0.13, w * s, s * 0.26, rx=s * 0.13, fill=fill)


@icon("parsec", kind="app", names=["com.parsecgaming.parsec", "parsec", "parsecd"], title="Parsec")
def parsec(ic):
    tile(ic, "#3A3A6E", "#14142E")
    shadow(ic, 128, 212, 104, 12)
    # the star chart, a sheet on the desk
    with ic.g(transform="rotate(-7 128 110)"):
        ic.rect(36, 30, 186, 150, rx=3, fill="#000", opacity=0.3, transform="translate(2 4)")
        ic.rect(36, 30, 186, 150, rx=3, fill=ic.lin([(0, "#1F2C5A"), (1, "#0E1636")], 0, 0, 1, 1))
        ic.rect(42, 36, 174, 138, fill="none", stroke="#C9B577", stroke_opacity=0.5)
        for r in (30, 52, 74):
            ic.circle(140, 98, r, fill="none", stroke="#9FB0E0", stroke_opacity=0.25, stroke_dasharray="2 3")
        ic.line(42, 98, 216, 98, stroke="#9FB0E0", stroke_opacity=0.2)
        ic.line(140, 36, 140, 174, stroke="#9FB0E0", stroke_opacity=0.2)
        stars = [(64, 54, 2.2), (86, 64, 1.6), (108, 50, 2.6), (124, 70, 1.8), (160, 52, 3), (188, 64, 1.8),
                 (200, 84, 2.2), (176, 88, 1.4), (58, 84, 1.4), (76, 98, 1.2), (196, 46, 1.2), (150, 82, 1.1)]
        ic.path("M64 54 L86 64 L108 50 L124 70 L160 52 L188 64 L200 84", fill="none", stroke="#E9D7A0",
                stroke_opacity=0.55, stroke_width=1)
        for x, y, r in stars:
            ic.circle(x, y, r, fill="#F6E7B6")
        # one parsec: a measured span with its ticks
        ic.line(108, 50, 160, 52, stroke="#F2C45C", stroke_width=1.6)
        ic.circle(160, 52, 6, fill="none", stroke="#F2C45C", stroke_width=1.2)
        ic.text("1 pc", 134, 46, 7, font="mono-semibold", anchor="middle", fill="#F2C45C")
        ic.text("3.26 ly", 56, 168, 7, font="mono", fill="#C9B577", opacity=0.8)
    # the gamepad
    pad = ("M66 112 C66 100 76 94 88 94 H168 C180 94 190 100 190 112 L208 176 C213 196 196 210 180 200"
           " L160 184 H96 L76 200 C60 210 43 196 48 176 Z")
    ic.path(pad, fill="#000", opacity=0.4, transform="translate(3 6)")
    ic.path(pad, fill=ic.lin([(0, "#F4F5F7"), (0.55, "#D6D9DE"), (1, "#9EA3AB")], 0, 0, 1, 1))
    ic.path(pad, fill="none", stroke="#fff", stroke_width=1.5, opacity=0.8)
    # d-pad
    dx, dy = 90, 128
    ic.circle(dx, dy, 18, fill="#C2C6CC")
    ic.path(f"M{dx - 5} {dy - 15}h10v10h10v10h-10v10h-10v-10h-10v-10h10z", fill="#1E2024", transform="translate(0 1)")
    ic.path(f"M{dx - 5} {dy - 15}h10v10h10v10h-10v10h-10v-10h-10v-10h10z", fill="#3A3D43")
    # face buttons
    bx, by = 166, 128
    for (ox, oy), c in (((0, -11), "#F2C45C"), ((11, 0), "#E5574A"), ((0, 11), "#5BBF6A"), ((-11, 0), "#4C8FE0")):
        ic.circle(bx + ox, by + oy + 1.2, 6, fill="#000", opacity=0.35)
        ic.circle(bx + ox, by + oy, 6, fill=c)
        ic.circle(bx + ox - 1.6, by + oy - 1.6, 1.8, fill="#fff", opacity=0.55)
    # sticks
    for sx in (108, 148):
        ic.circle(sx, 160, 14, fill="#5F646B")
        ic.circle(sx, 160, 11, fill="#000", opacity=0.35, transform="translate(1 1.5)")
        ic.circle(sx, 160, 11, fill=ic.rad([(0, "#5A5E65"), (1, "#202226")], cx=0.35, cy=0.3, r=0.8))
        ic.circle(sx, 160, 7, fill="none", stroke="#fff", stroke_opacity=0.12, stroke_dasharray="1 1.4")
    # the mark on the middle
    ic.rect(110, 104, 36, 28, rx=7, fill="#1B1C22")
    ic.rect(110.5, 104.5, 35, 27, rx=6.5, fill="none", stroke="#fff", stroke_opacity=0.2)
    _parsec_mark(ic, 128, 118, 15, "#F3F4F6")


@small("parsec")
def parsec16(ic):
    tile(ic, "#3A3A6E", "#14142E")
    ic.circle(3.5, 3.5, 0.6, fill="#F6E7B6")
    ic.circle(12, 2.6, 0.7, fill="#F6E7B6")
    ic.path("M3.5 6.5C3.5 5.7 4 5.2 4.8 5.2H11.2C12 5.2 12.5 5.7 12.5 6.5L13.8 11.3C14.1 12.6 12.8 13.4 11.9"
            " 12.7L10.6 11.6H5.4L4.1 12.7C3.2 13.4 1.9 12.6 2.2 11.3Z", fill="#E4E6EA")
    ic.rect(4.2, 7.7, 3, 1, fill="#3A3D43")
    ic.rect(5.2, 6.7, 1, 3, fill="#3A3D43")
    ic.circle(11, 7.3, 0.8, fill="#E5574A")
    ic.circle(10, 8.6, 0.8, fill="#5BBF6A")
    ic.rect(7, 6.2, 2, 2.2, rx=0.4, fill="#1B1C22")


# --- WireGuard: a network plug, its boot red with the serpent badge ----------

def _serpent(ic, cx, cy, r, fill):
    """A serpent curled almost to a ring, its head inside, an eye."""
    sw = r * 0.34
    ic.path(f"M{polar(cx, cy, r * 0.66, 200)[0]:.1f} {polar(cx, cy, r * 0.66, 200)[1]:.1f}"
            f"A{r * 0.66} {r * 0.66} 0 1 1 {polar(cx, cy, r * 0.66, 128)[0]:.1f} "
            f"{polar(cx, cy, r * 0.66, 128)[1]:.1f}", fill="none", stroke=fill, stroke_width=sw,
            stroke_linecap="round")
    # the crest along its back
    for a in (262, 290, 318, 346):
        b1 = polar(cx, cy, r * 0.8, a - 8)
        tip = polar(cx, cy, r * 1.02, a)
        b2 = polar(cx, cy, r * 0.8, a + 8)
        ic.poly([b1, tip, b2], fill=fill)
    # the head, turned in
    hx, hy = polar(cx, cy, r * 0.62, 156)
    ic.ellipse(hx - r * 0.12, hy - r * 0.08, r * 0.36, r * 0.25, fill=fill,
               transform=f"rotate(-30 {hx - r * 0.12:.1f} {hy - r * 0.08:.1f})")
    ic.circle(hx - r * 0.26, hy - r * 0.1, r * 0.07, fill="#881713")
    # the tongue
    ic.path(f"M{hx - r * 0.42:.1f} {hy + r * 0.05:.1f}l{-r * 0.14:.1f} {-r * 0.06:.1f}m{r * 0.14:.1f} "
            f"{r * 0.06:.1f}l{-r * 0.12:.1f} {r * 0.1:.1f}", stroke=fill, stroke_width=r * 0.05,
            stroke_linecap="round")


@icon("wireguard", kind="app", names=["wireguard"], title="WireGuard")
def wireguard(ic):
    tile(ic, "#8E2A26", "#3E0C0A")
    shadow(ic, 140, 214, 92, 11)
    # the cable, down to the desk, round in a loop and away behind the plug
    cable = "M128 150 C128 196 150 206 186 204 C224 202 230 160 206 138 C190 124 170 120 150 112"
    ic.path(cable, fill="none", stroke="#000", stroke_opacity=0.35, stroke_width=17, stroke_linecap="round",
            transform="translate(2 4)")
    ic.path(cable, fill="none", stroke=ic.lin([(0, "#4A4E55"), (1, "#18191C")], 0, 0, 1, 1), stroke_width=15,
            stroke_linecap="round")
    ic.path("M123 168 C126 192 146 199 184 198 C214 196 222 166 206 146", fill="none", stroke="#fff",
            stroke_opacity=0.2, stroke_width=2.5, stroke_linecap="round")
    # the clear housing: the plug's head
    hx, hy, hw, hh = 92, 34, 72, 66
    ic.rect(hx, hy, hw, hh, rx=6, fill="#000", opacity=0.3, transform="translate(2 4)")
    ic.rect(hx, hy, hw, hh, rx=6, fill=ic.lin([(0, "#F4F7F9", 0.85), (1, "#B9C3CB", 0.75)], 0, 0, 1, 1))
    ic.rect(hx + 0.75, hy + 0.75, hw - 1.5, hh - 1.5, rx=5.25, fill="none", stroke="#fff", stroke_width=1.5)
    # the eight contacts, gold
    for k in range(8):
        x = hx + 10 + k * 7.4
        ic.rect(x, hy + 4, 4, 18, rx=1, fill=brass(ic, 0, 0, 1, 0))
    # the wires inside, coloured pairs
    wires = ("#F2A35C", "#E57A2A", "#7CCB8A", "#3A7ADF", "#E8EEF4", "#2E9E5B", "#B7865A", "#6E4A2A")
    for k, c in enumerate(wires):
        x = hx + 12 + k * 7.4
        ic.line(x, hy + 24, x + (128 - x) * 0.4, hy + hh - 2, stroke=c, stroke_width=3.2, opacity=0.85)
    ic.rect(hx + 6, hy + 40, hw - 12, 8, rx=1, fill="#fff", opacity=0.35)
    ic.path(f"M{hx + 4} {hy + 6}h20L{hx + 8} {hy + hh - 6}h-4z", fill="#fff", opacity=0.45)
    # the boot: red rubber, ribbed at the neck
    top = hy + hh - 4
    boot = (f"M{hx - 4} {top + 4}a4 4 0 0 1 4 -4h{hw}a4 4 0 0 1 4 4V{top + 48}L{136} {top + 76}h-16"
            f"L{hx - 4} {top + 48}z")
    ic.path(boot, fill="#000", opacity=0.35, transform="translate(2 4)")
    ic.path(boot, fill=ic.lin([(0, "#D8463E"), (0.55, "#A51F18"), (1, "#5E0E0A")], 0, 0, 1, 1))
    ic.path(f"M{hx - 2} {top + 1.5}h{hw + 4}", stroke="#FFB0A8", stroke_opacity=0.6, stroke_width=1.5)
    ic.line(hx - 2.5, top + 6, hx - 2.5, top + 46, stroke="#FFB0A8", stroke_opacity=0.35, stroke_width=1.5)
    for k in range(4):
        y_ = top + 58 + k * 4.5
        half = 40 - (y_ - top - 48) * (32 / 28)
        ic.line(128 - half + 2, y_, 128 + half - 2, y_, stroke="#3E0806", stroke_opacity=0.5, stroke_width=1.2)
    # the badge on the boot: the serpent in white on red enamel
    cx, cy = 128, top + 24
    ic.circle(cx + 1, cy + 2, 22, fill="#000", opacity=0.3)
    ic.circle(cx, cy, 22, fill=steel(ic, False))
    ic.circle(cx, cy, 19, fill=ic.rad([(0, "#C02A22"), (1, "#7A120D")], cx=0.35, cy=0.3, r=0.8))
    _serpent(ic, cx, cy, 16, "#FFFFFF")
    ic.path(f"M{cx - 16} {cy - 6}a17 17 0 0 1 12 -12", fill="none", stroke="#fff", stroke_opacity=0.45,
            stroke_width=1.5, stroke_linecap="round")
    ic.text("WIREGUARD", 128, top + 51, 5.5, font="mono-semibold", anchor="middle", spacing=0.6,
            fill="#FFE2DE", opacity=0.75)


@small("wireguard")
def wireguard16(ic):
    tile(ic, "#8E2A26", "#3E0C0A")
    ic.path("M8 11.5 C8 14.2 11 14.4 12.6 13.2 C14 12 13.6 9.6 11.6 8.6", fill="none", stroke="#25272B",
            stroke_width=1.5, stroke_linecap="round")
    ic.rect(5.2, 1.8, 5.6, 4.6, rx=0.5, fill="#E4EAEE")
    for k in range(4):
        ic.rect(5.8 + k * 1.2, 2.3, 0.6, 1.6, fill="#C99645")
    ic.path("M4.6 6.2h6.8l-.8 5.6h-5.2z", fill="#B3241C")
    ic.circle(8, 8.9, 1.9, fill="none", stroke="#fff", stroke_width=0.8)


# --- Mullvad VPN: the mole by its tunnel, under a hill ----------------------

@icon("mullvad-vpn", kind="app", names=["mullvad-vpn", "net.mullvad.MullvadVPN"], title="Mullvad VPN")
def mullvad(ic):
    tile(ic, "#2E5A86", "#122A46")
    shadow(ic, 128, 214, 108, 11)
    # the hill
    hill = "M16 212 C30 132 72 70 128 68 C184 70 226 132 240 212 Z"
    ic.path(hill, fill=ic.lin([(0, "#7AA35A"), (0.35, "#4E7A3A"), (1, "#2A4A22")], 0, 0, 1, 1))
    ic.path("M28 170 C42 118 80 78 128 74", fill="none", stroke="#C8E6A0", stroke_opacity=0.45, stroke_width=2)
    for x, y in ((172, 92), (196, 132), (66, 118), (210, 172), (44, 162), (84, 104)):
        ic.path(f"M{x} {y}l2 -6 2 6 M{x + 3} {y}l3 -5 1 5", fill="none", stroke="#2A4A22", stroke_width=1.2,
                opacity=0.7)
    # the tunnel: a stone arch, dark inside
    cx, cy, ro, ri = 128, 150, 58, 42
    arch = f"M{cx - ro} 212 V{cy} a{ro} {ro} 0 0 1 {2 * ro} 0 V212 Z"
    ic.path(arch, fill="#000", opacity=0.3, transform="translate(2.5 0)")
    ic.path(arch, fill=ic.lin([(0, "#C4BFB2"), (1, "#6E6A60")], 0, 0, 1, 1))
    inner = f"M{cx - ri} 212 V{cy} a{ri} {ri} 0 0 1 {2 * ri} 0 V212 Z"
    ic.path(inner, fill=ic.rad([(0, "#05080C"), (0.7, "#0E141A"), (1, "#2A2E30")], cx=0.5, cy=0.75, r=0.7))
    for k in range(11):
        a = -90 + k * 18
        x1, y1 = polar(cx, cy, ri, a)
        x2, y2 = polar(cx, cy, ro, a)
        ic.line(x1, y1, x2, y2, stroke="#4A463E", stroke_width=1.3)
    for y in (172, 194):
        for x0 in (cx - ro, cx + ri):
            ic.line(x0, y, x0 + ro - ri, y, stroke="#4A463E", stroke_width=1.3)
    ic.path(f"M{cx - ro + 1} 208 V{cy} a{ro - 1} {ro - 1} 0 0 1 {ro - 1} {-(ro - 1)}", fill="none", stroke="#fff",
            stroke_opacity=0.5, stroke_width=1.5)
    # the keystone's plate
    ic.rect(cx - 30, cy - ro - 10, 60, 15, rx=2, fill="#000", opacity=0.3, transform="translate(1 2)")
    ic.rect(cx - 30, cy - ro - 10, 60, 15, rx=2, fill=brass(ic))
    ic.text("MULLVAD", cx, cy - ro + 1, 8.5, font="mono-semibold", anchor="middle", spacing=1.2, fill="#4A3410")
    # the mole, looking out of the mouth
    fur = ic.rad([(0, "#F6CC66"), (0.55, "#D69A34"), (1, "#7A4E14")], cx=0.38, cy=0.3, r=0.8)
    head = "M92 212 C90 176 104 156 128 156 C152 156 166 176 164 212 Z"
    ic.path(head, fill=fur)
    ic.path("M96 196 C96 176 108 162 126 160", fill="none", stroke="#FFE9B8", stroke_opacity=0.8, stroke_width=2,
            stroke_linecap="round")
    ic.ellipse(128, 194, 15, 11, fill="#FFE3A0", opacity=0.55)
    for side in (-1, 1):
        ic.circle(128 + side * 15, 178, 2.6, fill="#1A1208")
        ic.circle(128 + side * 15 - 0.7, 177.3, 0.9, fill="#fff")
        for k in (-1, 0, 1):
            ic.line(128 + side * 10, 192 + k * 2, 128 + side * 30, 188 + k * 6, stroke="#5A3A10", stroke_width=0.7,
                    opacity=0.6)
    ic.ellipse(128, 189, 8, 6, fill="#E98A92")
    ic.ellipse(126, 187, 3, 1.8, fill="#fff", opacity=0.6)
    # the earth at the mouth, and the big pink hands on it
    ic.path("M30 212 C70 200 100 202 128 204 C160 206 196 200 226 212 Z", fill="#6B4A2A")
    ic.path("M60 212 C84 204 112 204 128 206 C150 208 176 204 196 212Z", fill="#8A6438")
    for px, rot in ((100, 20), (156, -20)):
        with ic.g(transform=f"rotate({rot} {px} 204)"):
            ic.ellipse(px + 1, 205.5, 14, 8, fill="#5A2A1A", opacity=0.35)
            ic.ellipse(px, 204, 14, 8, fill="#E07E88")
            for k in range(5):
                ic.ellipse(px - 10 + k * 5, 196.5, 1.6, 4, fill="#F6C2C6")
            ic.ellipse(px - 2, 201, 7, 2, fill="#fff", opacity=0.25)


@small("mullvad-vpn")
def mullvad16(ic):
    tile(ic, "#2E5A86", "#122A46")
    ic.path("M1 14.5 C2 7.5 5 4.2 8 4.2 C11 4.2 14 7.5 15 14.5Z", fill="#4E7A3A")
    ic.path("M3.5 14.5 V9.5 a4.5 4.5 0 0 1 9 0 V14.5Z", fill="#A8A397")
    ic.path("M5 14.5 V9.8 a3 3 0 0 1 6 0 V14.5Z", fill="#0A0E12")
    ic.path("M5.4 14.5 C5.4 11.5 6.4 10 8 10 C9.6 10 10.6 11.5 10.6 14.5Z", fill="#E0A940")
    ic.circle(8, 12.6, 0.9, fill="#E98A92")
    ic.rect(6.2, 4.6, 3.6, 1.4, rx=0.3, fill="#D2A458")


# --- 1Password: a round vault door, its keyhole badge in the middle ----------

@icon("1password", kind="app", names=["1password", "appimagekit-1password", "com.onepassword.OnePassword"],
      title="1Password")
def onepassword(ic):
    tile(ic, "#2A6FD0", "#0C2F6A")
    cx, cy = 128, 120
    shadow(ic, 128, 216, 92, 12)
    # the frame in the wall, and the hinge on the right
    ic.circle(cx, cy, 102, fill=ic.lin([(0, "#2B3036"), (1, "#0E1012")], 0, 0, 1, 1))
    ic.rect(214, 92, 20, 56, rx=6, fill=steel(ic))
    ic.line(214, 120, 234, 120, stroke="#000", stroke_opacity=0.35)
    # the door
    ic.circle(cx + 2, cy + 5, 94, fill="#000", opacity=0.45)
    ic.circle(cx, cy, 94, fill=ic.lin([(0, "#F1F3F5"), (0.45, "#A9B0B8"), (1, "#4D535A")], 0, 0, 1, 1))
    ic.circle(cx, cy, 82, fill=ic.lin([(0, "#5D636B"), (0.5, "#9EA5AD"), (1, "#D9DDE1")], 0, 0, 1, 1))
    ic.circle(cx, cy, 78, fill=ic.lin([(0, "#DDE1E5"), (0.55, "#9AA1A9"), (1, "#5A6067")], 0, 0, 1, 1))
    # the bolts round the rim
    for k in range(16):
        x, y = polar(cx, cy, 88, k * 22.5)
        ic.circle(x + 0.5, y + 0.8, 3.2, fill="#000", opacity=0.3)
        ic.circle(x, y, 3.2, fill=ic.lin([(0, "#F4F6F8"), (1, "#6F767E")], 0, 0, 1, 1))
    # brushed rings
    for r in (64, 50):
        ic.circle(cx, cy, r, fill="none", stroke="#fff", stroke_opacity=0.25, stroke_width=1)
        ic.circle(cx, cy, r + 1.2, fill="none", stroke="#000", stroke_opacity=0.12, stroke_width=1)
    # the wheel's spokes, behind the badge
    for a in (45, 135, 225, 315):
        ex, ey = polar(cx, cy, 70, a)
        ic.line(cx + 2, cy + 3, ex + 2, ey + 3, stroke="#000", stroke_opacity=0.3, stroke_width=9,
                stroke_linecap="round")
        ic.line(cx, cy, ex, ey, stroke=ic.lin([(0, "#F1F3F5"), (1, "#5D636B")], 0, 0, 1, 1), stroke_width=8,
                stroke_linecap="round")
        ic.circle(ex, ey, 8, fill=ic.lin([(0, "#F4F6F8"), (1, "#5D636B")], 0, 0, 1, 1))
    # the badge: blue enamel, a white ring, the keyhole bar
    r = 40
    ic.circle(cx + 2, cy + 4, r + 4, fill="#000", opacity=0.35)
    ic.circle(cx, cy, r + 4, fill=ic.lin([(0, "#F4F6F8"), (1, "#5D636B")], 0, 0, 1, 1))
    ic.circle(cx, cy, r, fill=ic.rad([(0, "#3D96FF"), (0.6, "#0A6BE8"), (1, "#04408F")], cx=0.35, cy=0.3, r=0.8))
    ic.circle(cx, cy, r - 7, fill="none", stroke="#fff", stroke_width=4.5)
    bar = f"M{cx - 5} {cy - 20}h10v16l-3.5 3.5 3.5 3.5v17h-10v-14l3.5 -3.5 -3.5 -3.5z"
    ic.path(bar, fill="#04306A", opacity=0.45, transform="translate(1 1.5)")
    ic.path(bar, fill="#fff")
    ic.path(f"M{cx - 30} {cy - 12}a32 32 0 0 1 22 -20 34 34 0 0 0 -22 20z", fill="#fff", opacity=0.45)
    # the light on the steel
    ic.path(f"M{cx - 86} {cy - 20}a88 88 0 0 1 56 -66 92 92 0 0 0 -56 66z", fill="#fff", opacity=0.55)


@small("1password")
def onepassword16(ic):
    tile(ic, "#2A6FD0", "#0C2F6A")
    ic.circle(8, 8, 6.6, fill="#B7BDC4")
    for k in range(8):
        x, y = polar(8, 8, 5.7, k * 45)
        ic.circle(x, y, 0.5, fill="#5D636B")
    ic.circle(8, 8, 3.9, fill="#0A6BE8")
    ic.circle(8, 8, 3.1, fill="none", stroke="#fff", stroke_width=0.6)
    ic.rect(7.4, 6, 1.2, 4, rx=0.3, fill="#fff")


# --- Proton Pass: a violet key card on a badge reel -------------------------

@icon("proton-pass", kind="app", names=["me.proton.Pass", "proton-pass"], title="Proton Pass")
def proton_pass(ic):
    tile(ic, "#4A3690", "#1A1040")
    shadow(ic, 132, 210, 100, 12)
    # the reel, clipped to nothing: a round case and its cord
    rx_, ry_ = 62, 44
    # its belt clip, behind
    ic.rect(rx_ - 7, ry_ - 30, 14, 26, rx=4, fill=steel(ic))
    ic.circle(rx_ + 2, ry_ + 3, 20, fill="#000", opacity=0.35)
    ic.circle(rx_, ry_, 20, fill=graphite(ic))
    ic.circle(rx_, ry_, 19, fill="none", stroke="#fff", stroke_opacity=0.18, stroke_width=1.5)
    ic.circle(rx_, ry_, 14, fill=ic.lin([(0, "#A27BFF"), (1, "#5A3AD0")], 0, 0, 1, 1))
    ic.circle(rx_, ry_, 14, fill="none", stroke="#2A1460", stroke_opacity=0.5)
    ic.text("P", rx_, ry_ + 5, 14, font="sans-bold", anchor="middle", fill="#F1EAFF")
    with ic.g(transform="translate(-8 6) rotate(14 140 136)"):
        x, y, w, h = 52, 78, 176, 112
        ic.rect(x, y, w, h, rx=12, fill="#000", opacity=0.4, transform="translate(3 6)")
        ic.rect(x, y, w, h, rx=12, fill=ic.lin([(0, "#E3A6FF"), (0.35, "#A27BFF"), (0.75, "#6D4AFF"),
                                                (1, "#3E23B0")], 0, 0, 1, 1))
        ic.rect(x + 0.75, y + 0.75, w - 1.5, h - 1.5, rx=11.25, fill="none", stroke="#fff", stroke_opacity=0.55,
                stroke_width=1.5)
        # the slot for the cord, punched
        ic.rect(x + 14, y + 9, 26, 6, rx=3, fill="#2A1460")
        ic.rect(x + 14, y + 9, 26, 6, rx=3, fill="none", stroke="#fff", stroke_opacity=0.35)
        # the chip
        ic.rect(x + 16, y + 34, 32, 26, rx=5, fill=brass(ic))
        for k in (1, 2):
            ic.line(x + 16, y + 34 + k * 8.7, x + 48, y + 34 + k * 8.7, stroke="#7E5A20", stroke_width=1)
        ic.line(x + 32, y + 34, x + 32, y + 60, stroke="#7E5A20", stroke_width=1)
        ic.rect(x + 26, y + 41, 12, 12, rx=2, fill="none", stroke="#7E5A20", stroke_width=1)
        # the mark: a rounded P, its bowl a keyhole
        mx, my = x + 128, y + 48
        mk = (f"M{mx - 18} {my + 28}V{my - 18}a6 6 0 0 1 6 -6h14a20 20 0 0 1 0 40h-8v10a4 4 0 0 1 -4 4h-4"
              f"a4 4 0 0 1 -4 -4z")
        ic.path(mk, fill="#2A1460", opacity=0.35, transform="translate(1.5 2)")
        ic.path(mk, fill=ic.lin([(0, "#FFFFFF"), (1, "#E6DCFF")], 0, 0, 1, 1))
        ic.circle(mx + 1, my + 2, 6, fill="#6D4AFF")
        ic.path(f"M{mx - 1.5} {my + 6}h5l1.5 10h-8z", fill="#6D4AFF")
        # the name
        ic.text("Proton Pass", x + 16, y + 84, 13, font="sans-semibold", fill="#fff")
        ic.text("ACCESS  ·  LEVEL 4", x + 16, y + 98, 7, font="mono-semibold", spacing=0.8, fill="#F1EAFF",
                opacity=0.75)
        # the sheen
        ic.path(f"M{x + 12} {y}h70L{x + 30} {y + h}H{x + 12}a12 12 0 0 1 -12 -12V{y + 12}a12 12 0 0 1 12 -12z",
                fill="#fff", opacity=0.12)
    # the cord from the reel, through the card's slot on a split ring
    ic.path(f"M{rx_ + 8} {ry_ + 18} C{rx_ + 14} {ry_ + 28} 76 76 82 80", fill="none", stroke="#1A1C20",
            stroke_width=2.4, stroke_linecap="round")
    ic.circle(84, 83, 5, fill="none", stroke=steel(ic, False), stroke_width=2)


@small("proton-pass")
def proton_pass16(ic):
    tile(ic, "#4A3690", "#1A1040")
    with ic.g(transform="rotate(12 8 8)"):
        ic.rect(1.6, 4, 12.8, 8.4, rx=1.2, fill="#8C62FF")
        ic.rect(3, 6.2, 2.6, 2, rx=0.4, fill="#D9B060")
        ic.path("M8.8 10.8V5.8h2.2a1.5 1.5 0 0 1 0 3h-1v2z", fill="#fff")


# --- Authenticator: a key fob counting a six-digit code down ----------------

@icon("authenticator", kind="app", names=["authenticator", "com.belmoussaoui.Authenticator", "gnome-twofactorauth"],
      title="Authenticator")
def authenticator(ic):
    tile(ic, "#2E7C78", "#103A38")
    shadow(ic, 124, 196, 104, 12)
    with ic.g(transform="rotate(-10 128 128)"):
        # the key ring through its eye, on the right
        ic.circle(214, 110, 22, fill="none", stroke="#000", stroke_opacity=0.35, stroke_width=5,
                  transform="translate(2 3)")
        ic.circle(214, 110, 22, fill="none", stroke=steel(ic, False), stroke_width=4.5)
        ic.path("M194 104 a22 22 0 0 1 14 -16", fill="none", stroke="#fff", stroke_opacity=0.7, stroke_width=1.2)
        # the body: a lozenge of grey plastic with a blue end
        body = "M28 96 a32 32 0 0 1 32 -32 H180 a34 34 0 0 1 34 34 v24 a34 34 0 0 1 -34 34 H60 a32 32 0 0 1 -32 -32z"
        ic.path(body, fill="#000", opacity=0.4, transform="translate(3 6)")
        ic.path(body, fill=ic.lin([(0, "#E9ECEF"), (0.5, "#B9BFC6"), (1, "#7B828B")], 0, 0, 0, 1))
        ic.path("M180 64 a34 34 0 0 1 34 34 v24 a34 34 0 0 1 -34 34 H170 V64z",
                fill=ic.lin([(0, "#58A9E8"), (1, "#1A5A9A")], 0, 0, 0, 1))
        ic.circle(196, 110, 7, fill="#0E2E50")
        ic.circle(196, 110, 7, fill="none", stroke="#fff", stroke_opacity=0.3)
        ic.path(body, fill="none", stroke="#fff", stroke_opacity=0.6, stroke_width=1.5)
        # the window and its LCD
        ic.rect(42, 80, 120, 50, rx=8, fill="#1A1C20")
        ic.rect(48, 86, 108, 38, rx=3, fill=ic.lin([(0, "#D2E2D8"), (1, "#A7BFB0")]))
        ic.text("888888", 152, 116, 24, font="mono-semibold", anchor="end", fill="#1E2A22", opacity=0.07)
        ic.text("482913", 152, 116, 24, font="mono-semibold", anchor="end", fill="#1E2A22")
        # the countdown: bars down the left of the digits
        for k in range(6):
            ic.rect(52, 90 + k * 5.4, 6, 3.2, fill="#1E2A22", opacity=0.85 if k >= 2 else 0.1)
        ic.path("M48 89 a3 3 0 0 1 3 -3 h70 L96 124 H51 a3 3 0 0 1 -3 -3z", fill="#fff", opacity=0.18)
        # the maker's print and a code light
        ic.text("2FA  ·  30 s", 48, 146, 8, font="mono-semibold", spacing=0.8, fill="#3A4048")
        ic.circle(152, 143, 3.2, fill="#4FD07A")
        ic.circle(151.2, 142.2, 1.1, fill="#fff", opacity=0.7)
        # the light along the top
        ic.path("M50 67 H176", stroke="#fff", stroke_width=2, stroke_linecap="round", opacity=0.8)


@small("authenticator")
def authenticator16(ic):
    tile(ic, "#2E7C78", "#103A38")
    with ic.g(transform="rotate(-10 8 8)"):
        ic.circle(13.4, 8, 1.6, fill="none", stroke="#C3C8CE", stroke_width=0.7)
        ic.rect(1.2, 5, 12.6, 6, rx=2.6, fill="#C7CCD2")
        ic.path("M11.4 5h-.2v6h.2a2.6 2.6 0 0 0 2.6 -2.6v-.8A2.6 2.6 0 0 0 11.4 5z", fill="#3B86C8")
        ic.rect(2.4, 6.2, 8, 3.6, rx=0.5, fill="#1A1C20")
        for k in range(3):
            ic.rect(3.2 + k * 2.4, 7.4, 1.6, 1.4, fill="#BFD8C8")


# --- Cryptomator: a green crate, padlocked, on its way to the cloud ----------

@icon("cryptomator", kind="app", names=["appimagekit-org.cryptomator.Cryptomator", "cryptomator",
                                         "org.cryptomator.Cryptomator"], title="Cryptomator")
def cryptomator(ic):
    tile(ic, "#2F5E44", "#10281C")
    shadow(ic, 128, 214, 102, 12)
    # a cloud behind, where it is going
    cloud = "M150 70 a22 22 0 0 1 40 -14 a18 18 0 0 1 30 14 a16 16 0 0 1 0 32 H160 a16 16 0 0 1 -10 -32z"
    ic.path(cloud, fill=ic.lin([(0, "#FFFFFF"), (1, "#C9D8D0")], 0, 0, 0, 1), opacity=0.92)
    ic.path("M156 66 a22 22 0 0 1 36 -12", fill="none", stroke="#fff", stroke_width=2)
    green = ic.lin([(0, "#79C66A"), (0.5, "#4AA147"), (1, "#25682A")], 0, 0, 1, 1)
    # the crate: a box of planks, painted green
    x, y, w, h = 36, 92, 184, 116
    ic.rect(x, y, w, h, rx=6, fill="#000", opacity=0.35, transform="translate(2 4)")
    ic.rect(x, y, w, h, rx=6, fill=green)
    for k in range(1, 4):
        ic.line(x + 4, y + k * h / 4, x + w - 4, y + k * h / 4, stroke="#1A4A1C", stroke_opacity=0.55,
                stroke_width=1.5)
        ic.line(x + 4, y + k * h / 4 + 1.5, x + w - 4, y + k * h / 4 + 1.5, stroke="#C8F0B0", stroke_opacity=0.3)
    # wood showing where the paint is worn
    for px, py, pw in ((52, 100, 18), (172, 134, 12), (88, 196, 22), (190, 196, 10)):
        ic.rect(px, py, pw, 3, rx=1.5, fill="#C48A55", opacity=0.6)
    # the frame: corner boards
    for bx in (x, x + w - 16):
        ic.rect(bx, y, 16, h, rx=4, fill=ic.lin([(0, "#5DB052"), (1, "#22602A")], 0, 0, 1, 1))
        ic.line(bx + 1, y + 2, bx + 1, y + h - 2, stroke="#D8F5C0", stroke_opacity=0.4, stroke_width=1.5)
    ic.rect(x, y, w, 14, rx=4, fill=ic.lin([(0, "#8AD27A"), (1, "#3E8E3C")]))
    ic.line(x + 4, y + 1, x + w - 4, y + 1, stroke="#E8FFD8", stroke_opacity=0.7, stroke_width=1.5)
    # steel corners and nails
    for cx_, cy_ in ((x + 8, y + 8), (x + w - 8, y + 8), (x + 8, y + h - 8), (x + w - 8, y + h - 8)):
        ic.circle(cx_, cy_, 2.4, fill=steel(ic, False))
    # the stencil
    ic.text("CRYPTOMATOR", x + 30, y + h - 14, 11, font="sans-condensed", spacing=1.2, fill="#F2F6EE", opacity=0.75)
    ic.text("VAULT 01", x + w - 22, y + 36, 7.5, font="mono-semibold", anchor="end", spacing=1, fill="#F2F6EE",
            opacity=0.6)
    # the hasp and the padlock
    ic.rect(116, y + 8, 24, 40, rx=3, fill=steel(ic))
    ic.circle(128, y + 38, 4.5, fill="#2A2C30")
    by, bh = _padlock(ic, 128, y + 22, 50, ic.lin([(0, "#8DE07A"), (0.5, "#49B04A"), (1, "#1F6A22")], 0, 0, 1, 1))
    ic.circle(128, by + 15, 5, fill="#123A14")
    ic.path(f"M125.5 {by + 17}l-2 12h9l-2 -12z", fill="#123A14")
    ic.path(f"M107 {by + 6}h16L111 {by + bh - 4}h-4z", fill="#fff", opacity=0.22)


@small("cryptomator")
def cryptomator16(ic):
    tile(ic, "#2F5E44", "#10281C")
    ic.path("M10 4.2a1.6 1.6 0 0 1 3-.4 1.2 1.2 0 0 1 .4 2.3H10.6a1 1 0 0 1-.6-1.9z", fill="#E8F0EA")
    ic.rect(1.5, 6.5, 13, 7.5, rx=0.6, fill="#4AA147")
    ic.rect(1.5, 6.5, 13, 1.2, fill="#7CC86A")
    ic.path("M6.5 9.4V8.3a1.5 1.5 0 0 1 3 0v1.1", fill="none", stroke="#D8DDE2", stroke_width=0.9)
    ic.rect(5.7, 9.2, 4.6, 3.6, rx=0.6, fill="#8DE07A")
    ic.circle(8, 10.7, 0.6, fill="#123A14")


# --- VeraCrypt: a hard drive, locked, its key lying across it ---------------

@icon("veracrypt", kind="app", names=["veracrypt", "veracrypt.xpm"], title="VeraCrypt")
def veracrypt(ic):
    tile(ic, "#36507A", "#141F38")
    shadow(ic, 128, 214, 96, 12)
    with ic.g(transform="rotate(-6 128 120)"):
        # the drive: aluminium, seen from the top
        x, y, w, h = 52, 26, 150, 190
        ic.rect(x, y, w, h, rx=8, fill="#000", opacity=0.4, transform="translate(3 6)")
        ic.rect(x, y, w, h, rx=8, fill=ic.lin([(0, "#F0F2F4"), (0.5, "#B5BCC4"), (1, "#7A828C")], 0, 0, 1, 1))
        ic.rect(x + 0.75, y + 0.75, w - 1.5, h - 1.5, rx=7.25, fill="none", stroke="#fff", stroke_opacity=0.7,
                stroke_width=1.5)
        # the platter's dome and the actuator's, pressed into the lid
        ic.circle(x + 75, y + 62, 46, fill="none", stroke="#fff", stroke_opacity=0.6, stroke_width=2,
                  transform="translate(0.8 0.8)")
        ic.circle(x + 75, y + 62, 46, fill="none", stroke="#5D636B", stroke_opacity=0.5, stroke_width=1.5)
        ic.circle(x + 75, y + 62, 10, fill=ic.lin([(0, "#6F767E"), (1, "#E9ECEF")], 0, 0, 1, 1))
        for k in range(6):
            sx, sy = polar(x + 75, y + 62, 6, k * 60)
            ic.circle(sx, sy, 1.1, fill="#3A3E44")
        for sx, sy in ((x + 10, y + 10), (x + w - 10, y + 10), (x + 10, y + h - 10), (x + w - 10, y + h - 10),
                       (x + w - 10, y + 92)):
            _screw(ic, sx, sy, 3.6, 20)
        # the label
        lx, ly, lw, lh = x + 14, y + 118, w - 28, 58
        ic.rect(lx, ly, lw, lh, rx=3, fill=paper(ic, "white"))
        ic.rect(lx, ly, lw, 16, rx=3, fill=ic.lin([(0, "#3A7ADF"), (1, "#1E4E9A")]))
        ic.rect(lx, ly + 12, lw, 4, fill="#1E4E9A")
        ic.text("VeraCrypt", lx + 8, ly + 12, 10.5, font="sans-bold", fill="#fff")
        ic.text("VOLUME  2 TB", lx + 8, ly + 29, 7, font="mono-semibold", fill="#3A4048")
        ic.text("AES-256 · XTS", lx + 8, ly + 39, 7, font="mono", fill="#5A6068")
        ic.text("S/N 7C41 09E2", lx + 8, ly + 49, 6, font="mono", fill="#8C887F")
        for k in range(16):
            ic.rect(lx + 84 + k * 2.1, ly + 26, 1.2 if k % 3 else 0.8, 22, fill="#2A2C30")
        ic.path(f"M{x} {y + 8}a8 8 0 0 1 8 -8h50L{x} {y + 120}z", fill="#fff", opacity=0.2)
    # the padlock, closed, hung from the drive's corner
    by, bh = _padlock(ic, 58, 66, 40, ic.lin([(0, "#F6DDA0"), (0.45, "#C99645"), (1, "#7E5A20")], 0, 0, 1, 1))
    ic.circle(58, by + 12, 4, fill="#3A2A10")
    ic.path(f"M56 {by + 14}l-1.6 9h7.2l-1.6 -9z", fill="#3A2A10")
    # the key, lying across, its bow blue enamel with a V
    with ic.g(transform="rotate(32 160 120)"):
        kx, ky = 150, 112
        blade = (f"M{kx + 20} {ky - 5}H{kx + 96}v10h-6v6h-6v-6h-6v8h-6v-8H{kx + 20}z")
        ic.path(blade, fill="#000", opacity=0.35, transform="translate(2 4)")
        ic.path(blade, fill=steel(ic, False))
        ic.line(kx + 22, ky - 4, kx + 94, ky - 4, stroke="#fff", stroke_opacity=0.7)
        ic.circle(kx + 2, ky + 4, 24, fill="#000", opacity=0.35)
        ic.circle(kx, ky, 24, fill=steel(ic, False))
        ic.circle(kx, ky, 20, fill=ic.rad([(0, "#4C9AF0"), (1, "#14408A")], cx=0.35, cy=0.3, r=0.8))
        ic.circle(kx - 11, ky, 4, fill="#0E1E3A")
        ic.path(f"M{kx - 3} {ky - 9}l6 18l6 -18", fill="none", stroke="#fff", stroke_width=3.6,
                stroke_linecap="round", stroke_linejoin="round", transform=f"rotate(-32 {kx + 3} {ky})")
        ic.path(f"M{kx - 18} {ky - 6}a19 19 0 0 1 12 -12", fill="none", stroke="#fff", stroke_opacity=0.5,
                stroke_width=1.5)


@small("veracrypt")
def veracrypt16(ic):
    tile(ic, "#36507A", "#141F38")
    ic.rect(3, 1.5, 10, 13, rx=0.8, fill="#BCC2C9")
    ic.circle(8, 5.3, 3, fill="none", stroke="#7A828C", stroke_width=0.6)
    ic.rect(4, 9.2, 8, 4.2, rx=0.4, fill="#fff")
    ic.rect(4, 9.2, 8, 1.4, fill="#2A6AD0")
    ic.path("M11 9.6 L14.6 5.4 M13.6 6.6 L14.6 7.4", stroke="#DDE1E5", stroke_width=1.1, stroke_linecap="round")
    ic.circle(10.6, 10.4, 2.3, fill="#2A6AD0")
    ic.circle(10.6, 10.4, 2.3, fill="none", stroke="#DDE1E5", stroke_width=0.6)
