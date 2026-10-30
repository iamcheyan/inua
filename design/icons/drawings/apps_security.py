"""The inua-objects theme, security and sync batch: KeePassXC, Bitwarden,
Passwords and Keys, Nextcloud, Syncthing, Transmission, qBittorrent,
FileZilla, Proton VPN, OneKey, TradingView, Fcitx
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


# CJK characters as strokes on a unit square (the fonts have none):
# Cangjie radicals and a few words.
_HAN = {
    "中": ["M.18 .28H.82V.66H.18Z", "M.5 .04V.98"],
    "文": ["M.47 .04L.55 .18", "M.08 .3H.92", "M.26 .34Q.45 .8 .9 .96", "M.74 .34Q.55 .8 .1 .96"],
    "日": ["M.22 .08H.78V.94H.22Z", "M.22 .5H.78"],
    "田": ["M.14 .12H.86V.9H.14Z", "M.14 .51H.86", "M.5 .12V.9"],
    "口": ["M.18 .18H.82V.84H.18Z"],
    "山": ["M.5 .08V.86", "M.16 .34V.86H.84V.34"],
    "人": ["M.52 .08Q.45 .6 .1 .94", "M.5 .4Q.62 .75 .92 .94"],
    "十": ["M.08 .45H.92", "M.5 .06V.96"],
    "大": ["M.08 .36H.92", "M.5 .06Q.5 .7 .1 .96", "M.53 .46Q.65 .78 .92 .96"],
    "一": ["M.06 .5H.94"],
    "木": ["M.08 .32H.92", "M.5 .04V.98", "M.48 .36Q.35 .7 .08 .86", "M.52 .36Q.65 .7 .92 .86"],
    "土": ["M.18 .38H.82", "M.5 .1V.88", "M.06 .88H.94"],
}


def _han(ic, ch, x, y, size, color, width=None, **kw):
    w = width if width is not None else size * 0.1
    d = "".join(_HAN[ch])
    ic.path(d, fill="none", stroke=color, stroke_width=w / size, stroke_linecap="round", stroke_linejoin="round",
            transform=f"translate({x} {y}) scale({size})", **kw)


def _shield(cx, top, w, h):
    """A heater shield, its top edge at top, w wide, h tall."""
    hw = w / 2
    return (f"M{cx} {top}L{cx + hw} {top + h * 0.1}V{top + h * 0.45}"
            f"C{cx + hw} {top + h * 0.75} {cx + hw * 0.45} {top + h * 0.9} {cx} {top + h}"
            f"C{cx - hw * 0.45} {top + h * 0.9} {cx - hw} {top + h * 0.75} {cx - hw} {top + h * 0.45}"
            f"V{top + h * 0.1}Z")


# --- KeePassXC: a steel safe, its door green enamel ------------------------

@icon("keepassxc", kind="app", names=["appimagekit-org.keepassxc.KeePassXC", "keepassxc", "org.keepassxc.KeePassXC"],
      title="KeePassXC")
def keepassxc(ic):
    tile(ic, "#41484E", "#16191C")
    shadow(ic, 128, 214, 100, 12)
    # feet
    for x in (52, 184):
        ic.rect(x, 200, 20, 12, rx=3, fill="#141618")
    # the body
    ic.rect(32, 32, 192, 174, rx=16, fill=ic.lin([(0, "#5C6560"), (0.5, "#363D3A"), (1, "#1C211F")], 0, 0, 1, 1))
    ic.rect(32.75, 32.75, 190.5, 172.5, rx=15.25, fill="none", stroke="#fff", stroke_opacity=0.18, stroke_width=1.5)
    # the door's frame, cut in
    ic.rect(44, 44, 168, 150, rx=10, fill="#0E1110")
    # hinges, left
    for y in (64, 160):
        ic.rect(38, y, 12, 22, rx=3, fill=steel(ic))
        ic.line(38, y + 11, 50, y + 11, stroke="#000", stroke_opacity=0.35)
    # the door: green enamel, a bevel
    door = ic.lin([(0, "#7CCB5A"), (0.55, "#4E9F3A"), (1, "#2C6A22")], 0, 0, 1, 1)
    ic.rect(48, 47, 162, 145, rx=8, fill="#000", opacity=0.45, transform="translate(2 3)")
    ic.rect(46, 46, 162, 144, rx=8, fill=door)
    ic.rect(46.75, 46.75, 160.5, 142.5, rx=7.25, fill="none", stroke="#D9F5C6", stroke_opacity=0.55, stroke_width=1.5)
    ic.rect(56, 56, 142, 124, rx=5, fill="none", stroke="#1E4A16", stroke_opacity=0.45, stroke_width=2)
    ic.rect(57, 57, 142, 124, rx=5, fill="none", stroke="#C8F0A8", stroke_opacity=0.35, stroke_width=1)
    # the dial
    dx, dy = 102, 108
    ic.circle(dx + 2, dy + 4, 38, fill="#000", opacity=0.35)
    ic.circle(dx, dy, 38, fill=ic.lin([(0, "#F2F4F6"), (0.5, "#A9AFB6"), (1, "#4D535A")], 0, 0, 1, 1))
    ic.circle(dx, dy, 33, fill=ic.lin([(0, "#3A3D42"), (1, "#111214")], 0, 0, 1, 1))
    for k in range(40):
        a = k * 9
        x1, y1 = polar(dx, dy, 32, a)
        x2, y2 = polar(dx, dy, 32 - (6 if k % 5 == 0 else 3), a)
        ic.line(x1, y1, x2, y2, stroke="#F1F1EF", stroke_width=1.3 if k % 5 == 0 else 0.7, opacity=0.9)
    for n, a in (("0", 0), ("10", 90), ("20", 180), ("30", 270)):
        x, y = polar(dx, dy, 19, a)
        ic.text(n, x, y + 2.6, 7.5, font="mono-semibold", anchor="middle", fill="#F1F1EF")
    ic.circle(dx, dy, 12, fill=ic.lin([(0, "#F2F4F6"), (1, "#6F767E")], 0, 0, 1, 1))
    ic.circle(dx, dy, 12, fill="none", stroke="#3A3E44", stroke_width=2, stroke_dasharray="1.2 1.4", opacity=0.6)
    ic.circle(dx - 3, dy - 3, 3, fill="#fff", opacity=0.6)
    ic.path(f"M{dx} {dy - 39}l-4 -7h8z", fill="#F2C45C")
    ic.path(f"M{dx - 30} {dy - 10}a32 32 0 0 1 22-22 34 34 0 0 0-22 22z", fill="#fff", opacity=0.3)
    # the handle: three spokes
    hx, hy = 172, 112
    for a in (0, 120, 240):
        ex, ey = polar(hx, hy, 24, a + 30)
        ic.line(hx + 1.5, hy + 3, ex + 1.5, ey + 3, stroke="#000", stroke_opacity=0.35, stroke_width=6,
                stroke_linecap="round")
    for a in (0, 120, 240):
        ex, ey = polar(hx, hy, 24, a + 30)
        ic.line(hx, hy, ex, ey, stroke="#A9AFB6", stroke_width=5, stroke_linecap="round")
        ic.circle(ex, ey, 5.5, fill=ic.lin([(0, "#F2F4F6"), (1, "#6F767E")], 0, 0, 1, 1))
    ic.circle(hx, hy, 10, fill=ic.lin([(0, "#F2F4F6"), (1, "#5D636B")], 0, 0, 1, 1))
    ic.circle(hx, hy, 3.5, fill="#3A3E44")
    # the keyhole plate under the dial
    ic.rect(156, 140, 32, 30, rx=4, fill=brass(ic))
    ic.circle(172, 151, 4.2, fill="#1A1208")
    ic.path("M170 152 l-2 10 h8 l-2 -10z", fill="#1A1208")
    for sx, sy in ((159.5, 143.5), (184.5, 143.5), (159.5, 166.5), (184.5, 166.5)):
        ic.circle(sx, sy, 1.3, fill="#5E4012")
    # the maker's plate
    ic.rect(66, 158, 76, 18, rx=3, fill=brass(ic))
    ic.rect(66.5, 158.5, 75, 17, rx=2.5, fill="none", stroke="#FFF1C8", stroke_opacity=0.5)
    _engraved(ic, "KeePassXC", 104, 171, 10.5, "#4A3410", font="sans-bold", anchor="middle", light="#FFF1C8",
              dark="#2A1C06", lo=0.6, do=0.3)
    # the lamp: locked
    ic.circle(200, 40, 3.6, fill="#7CF7A6")
    ic.circle(200, 40, 6, fill="#7CF7A6", opacity=0.2)
    # light across the door
    ic.path("M46 54a8 8 0 0 1 8-8h70L66 190H54a8 8 0 0 1-8-8z", fill=glare(ic, 0.9))


@small("keepassxc")
def keepassxc16(ic):
    tile(ic, "#41484E", "#16191C")
    ic.rect(2, 2.5, 12, 11, rx=1.4, fill="#2A302D")
    ic.rect(3, 3.5, 10, 9, rx=0.8, fill="#5DB043")
    ic.circle(6.5, 8, 2.6, fill="#C3C8CE")
    ic.circle(6.5, 8, 1.6, fill="#1A1C1E")
    ic.path("M11 6.5 V9.5 M9.6 8 H12.4", stroke="#E3E6EA", stroke_width=0.9, stroke_linecap="round")
    ic.rect(3.5, 13.5, 2, 1, fill="#141618")
    ic.rect(10.5, 13.5, 2, 1, fill="#141618")


# --- Bitwarden: a shield badge on a navy leather holder ---------------------

@icon("bitwarden", kind="app", names=["appimagekit-bitwarden", "bitwarden", "com.bitwarden.desktop"],
      title="Bitwarden")
def bitwarden(ic):
    tile(ic, "#3F78D6", "#183A80")
    shadow(ic, 128, 216, 92, 12)
    # the holder: navy leather, stitched
    ic.rect(50, 30, 156, 186, rx=18, fill="#000", opacity=0.3, transform="translate(2 4)")
    ic.rect(50, 30, 156, 186, rx=18, fill=ic.lin([(0, "#2C3A5C"), (1, "#0E1528")], 0, 0, 1, 1))
    grain = ic.define('<pattern id="{id}" width="5" height="5" patternUnits="userSpaceOnUse">'
                      '<circle cx="1" cy="1" r=".9" fill="#fff" opacity=".05"/>'
                      '<circle cx="3.5" cy="3.5" r=".9" fill="#000" opacity=".2"/></pattern>', "p")
    ic.rect(50, 30, 156, 186, rx=18, fill=f"url(#{grain})")
    ic.rect(50.75, 30.75, 154.5, 184.5, rx=17.25, fill="none", stroke="#fff", stroke_opacity=0.16, stroke_width=1.5)
    ic.rect(58, 38, 140, 170, rx=12, fill="none", stroke="#C9D3F0", stroke_opacity=0.45, stroke_width=1.3,
            stroke_dasharray="4 3")
    # the badge
    outer = _shield(128, 46, 120, 140)
    ic.path(outer, fill="#000", opacity=0.45, transform="translate(3 5)")
    ic.path(outer, fill=ic.lin([(0, "#F4F6F8"), (0.45, "#B7BDC4"), (1, "#5D636B")], 0, 0, 1, 1))
    ic.path(outer, fill="none", stroke="#fff", stroke_opacity=0.6, stroke_width=1)
    inner = _shield(128, 55, 104, 122)
    ic.path(inner, fill="#20242A", opacity=0.6, transform="translate(-0.8 -0.8)")
    ic.path(inner, fill=ic.lin([(0, "#3C8CFF"), (0.6, "#175DDC"), (1, "#0D3A96")], 0, 0, 1, 1))
    # the mark, in white enamel: a shield, its right half filled
    mk = _shield(128, 70, 66, 82)
    ic.path(mk, fill="none", stroke="#0B2A70", stroke_opacity=0.5, stroke_width=8, transform="translate(1 1.5)")
    ic.path(mk, fill="none", stroke="#F7F9FC", stroke_width=7, stroke_linejoin="round")
    ic.path("M128 74 L157 82 V107 C157 125 145 137 128 146 Z", fill="#F7F9FC")
    # the light on the enamel
    ic.path("M78 72 L128 58 V96 Q100 104 78 130 Z", fill="#fff", opacity=0.16)
    ic.path("M72 68 L124 52", stroke="#fff", stroke_opacity=0.8, stroke_width=1.5, stroke_linecap="round")
    _engraved(ic, "BITWARDEN", 128, 202, 9, "#D8C27A", font="mono-semibold", anchor="middle", spacing=2.4,
              light="#000", dark="#000", lo=0.4, do=0)


@small("bitwarden")
def bitwarden16(ic):
    tile(ic, "#3F78D6", "#183A80")
    ic.path(_shield(8, 1.6, 11, 13), fill="#C3C8CE")
    ic.path(_shield(8, 2.6, 9, 11), fill="#175DDC")
    ic.path(_shield(8, 4.3, 5.4, 7), fill="none", stroke="#fff", stroke_width=0.9)
    ic.path("M8 4.6 L10.6 5.3 V7.4 C10.6 9 9.6 10 8 10.8Z", fill="#fff")


# --- Passwords and Keys: a key ring, its keys and paper tags ----------------

def _key(ic, metal, length, teeth, bow="round"):
    """A key in its own frame: the hole for the ring at the origin, the
    blade down the +y axis."""
    edge = "#000"
    ic.circle(1.5, 15, 15, fill=edge, opacity=0.3, transform="translate(1.5 2)")
    ic.rect(-4, 26, 9, length, rx=1.5, fill=edge, opacity=0.3, transform="translate(2.5 2)")
    # the blade, its bits on the right
    blade = f"M-4 26H4"
    y = 34
    for t in teeth:
        blade += f"V{y}l{t} 3l-{t} 3"
        y += 6
    blade += f"V{26 + length}l-4 5l-4 -5Z"
    ic.path(blade, fill=metal)
    ic.line(-1, 30, -1, 24 + length, stroke="#000", stroke_opacity=0.25, stroke_width=1.5)
    ic.rect(-7, 26, 14, 5, rx=1.5, fill=metal)
    if bow == "round":
        ic.circle(0, 13, 15, fill=metal)
        ic.circle(0, 13, 15, fill="none", stroke="#fff", stroke_opacity=0.35, stroke_width=1,
                  stroke_dasharray="20 80")
        ic.circle(0, 13, 10, fill="none", stroke="#000", stroke_opacity=0.15, stroke_width=1)
    else:  # a black plastic head
        ic.rect(-15, -2, 30, 30, rx=9, fill=ic.lin([(0, "#4A4E55"), (1, "#141517")], 0, 0, 1, 1))
        ic.rect(-14.5, -1.5, 29, 29, rx=8.5, fill="none", stroke="#fff", stroke_opacity=0.15)
    ic.circle(0, 0, 4.2, fill="#2A2018")


def _tag(ic, label, sub, tint):
    """A paper tag in its own frame: its hole at the origin, hanging down +y."""
    body = "M-10 -8H10L22 4V84H-22V4Z"
    ic.path(body, fill="#000", opacity=0.3, transform="translate(2 3)")
    ic.path(body, fill=paper(ic, "cream"))
    ic.path("M-22 4L-10 -8H10L22 4", fill="none", stroke="#fff", stroke_width=1.2, opacity=0.8)
    ic.rect(-22, 64, 44, 20, fill=tint)
    ic.circle(0, 0, 6, fill="#D9CDB4")
    ic.circle(0, 0, 3.4, fill="#2A2018")
    ic.text(label, 0, 36, 16, font="hand", anchor="middle", fill="#2E3A55")
    ic.text(sub, 0, 48, 5.5, font="mono", anchor="middle", fill="#8C887F")
    ic.line(-14, 54, 14, 54, stroke="#8C887F", stroke_opacity=0.4, stroke_width=0.8)


@icon("seahorse", kind="app", names=["org.gnome.seahorse.Application", "seahorse", "seahorse-preferences"],
      title="Passwords and Keys")
def seahorse(ic):
    tile(ic, "#3E7E8A", "#173D46")
    shadow(ic, 128, 214, 84, 10, 0.7)
    rx_, ry_, rr = 124, 66, 22
    # the hook's plate on the wall
    ic.rect(104, 16, 40, 22, rx=6, fill="#000", opacity=0.3, transform="translate(2 3)")
    ic.rect(104, 16, 40, 22, rx=6, fill=brass(ic))
    ic.rect(104.5, 16.5, 39, 21, rx=5.5, fill="none", stroke="#FFF1C8", stroke_opacity=0.5)
    _screw(ic, 112, 27, 3.2, 20)
    _screw(ic, 136, 27, 3.2, 70)
    # tags, then keys, all hanging from the ring
    for a, label, sub, tint, swing in ((118, "email", "imap · 993", "#2463AE", 36), (242, "Wi-Fi", "home · 5 GHz", "#C8372D", -36)):
        tx, ty = polar(rx_, ry_, rr + 14, a)
        hx, hy = polar(rx_, ry_, rr, a)
        ic.line(hx, hy, tx, ty, stroke="#E8DCC0", stroke_width=1.6)
        with ic.g(transform=f"translate({tx:.1f} {ty:.1f}) rotate({a - 180 + swing})"):
            _tag(ic, label, sub, tint)
    keys = (
        (200, ic.lin([(0, "#F2F4F6"), (0.5, "#B7BDC4"), (1, "#5D636B")], 0, 0, 1, 1), 66, (3, 5, 2, 4, 3, 5), "round", 8),
        (160, ic.lin([(0, "#E9ECEF"), (1, "#7A818A")], 0, 0, 1, 1), 56, (5, 3, 4, 2, 5), "fob", -6),
        (180, ic.lin([(0, "#F4C6A0"), (0.5, "#C77B4A"), (1, "#6E3A1A")], 0, 0, 1, 1), 76, (4, 2, 5, 3, 4, 2, 5), "round", 0),
    )
    for a, metal, length, teeth, bow, swing in keys:
        hx, hy = polar(rx_, ry_, rr, a)
        with ic.g(transform=f"translate({hx:.1f} {hy:.1f}) rotate({a - 180 + swing})"):
            _key(ic, metal, length, teeth, bow)
    # the ring, its two turns
    ic.circle(rx_ + 2, ry_ + 3, rr, fill="none", stroke="#000", stroke_opacity=0.35, stroke_width=7)
    ic.circle(rx_, ry_, rr, fill="none", stroke=steel(ic, False), stroke_width=6)
    ic.circle(rx_ + 1.5, ry_ - 1, rr - 1, fill="none", stroke=steel(ic, False), stroke_width=4,
              stroke_dasharray="50 200", transform=f"rotate(-60 {rx_} {ry_})")
    ic.circle(rx_, ry_, rr + 2.6, fill="none", stroke="#fff", stroke_opacity=0.5, stroke_width=1,
              stroke_dasharray="30 200", transform=f"rotate(-170 {rx_} {ry_})")
    # the hook, through the ring
    hook = "M124 30 V40 a5 5 0 0 0 10 0 V36"
    ic.path(hook, fill="none", stroke="#000", stroke_opacity=0.3, stroke_width=5, transform="translate(2 3)")
    ic.path(hook, fill="none", stroke=brass(ic, 0, 0, 1, 0), stroke_width=4.5, stroke_linecap="round")
    ic.path("M122.8 31 V40", fill="none", stroke="#FFF1C8", stroke_opacity=0.7, stroke_width=1)


@small("seahorse")
def seahorse16(ic):
    tile(ic, "#3E7E8A", "#173D46")
    ic.rect(6.5, 1, 3, 1.6, rx=0.5, fill="#D2A458")
    ic.path("M3.6 6.4 L1.6 12.6 L4.4 13.6 L6.2 7.4z", fill="#F6F1E6")
    ic.path("M1.9 11.6 L4.9 12.6 L4.4 13.6 L1.6 12.6z", fill="#C8372D")
    ic.path("M12.4 6.4 L14.4 12.6 L11.6 13.6 L9.8 7.4z", fill="#F6F1E6")
    ic.path("M14.1 11.6 L11.1 12.6 L11.6 13.6 L14.4 12.6z", fill="#2463AE")
    ic.circle(8, 7.6, 1.8, fill="#C77B4A")
    ic.rect(7.4, 8.6, 1.2, 5.4, fill="#C77B4A")
    ic.circle(8, 4.6, 2.2, fill="none", stroke="#C3C8CE", stroke_width=1)


# --- Nextcloud: a blue enamel sign ------------------------------------------

def _nc_mark(ic, cx, cy, s, color, **kw):
    ic.circle(cx, cy, 22 * s, fill="none", stroke=color, stroke_width=9 * s, **kw)
    for dx in (-46, 46):
        ic.circle(cx + dx * s, cy, 11 * s, fill="none", stroke=color, stroke_width=6.5 * s, **kw)


@icon("nextcloud", kind="app", names=["Nextcloud", "com.nextcloud.desktopclient.nextcloud", "goa-account-owncloud",
                                      "nextcloud"], title="Nextcloud")
def nextcloud(ic):
    tile(ic, "#3B4A5A", "#18212B")
    shadow(ic, 128, 206, 104, 12)
    ic.rect(22, 58, 212, 140, rx=18, fill="#000", opacity=0.4, transform="translate(4 8)")
    # the sheet's thickness, below and right
    ic.rect(23, 61, 213, 141, rx=18, fill="#04304F")
    # iron under the enamel, its rim
    ic.rect(22, 58, 212, 140, rx=18, fill="#0A3C66")
    ic.rect(22, 58, 212, 140, rx=18, fill=ic.lin([(0, "#2FA4EC"), (0.5, "#0082C9"), (1, "#035C93")], 0, 0, 0.6, 1))
    ic.rect(22.75, 58.75, 210.5, 138.5, rx=17.25, fill="none", stroke="#BFE6FF", stroke_opacity=0.55,
            stroke_width=1.5)
    # the raised white border
    ic.rect(34, 70, 188, 116, rx=10, fill="none", stroke="#03466F", stroke_opacity=0.5, stroke_width=4,
            transform="translate(0.8 1.2)")
    ic.rect(34, 70, 188, 116, rx=10, fill="none", stroke="#F6FAFD", stroke_width=3.5)
    # the mark, white enamel, a little raised
    _nc_mark(ic, 129, 112, 1.0, "#03466F", opacity=0.45)
    _nc_mark(ic, 128, 111, 1.0, "#F6FAFD")
    ic.text("Nextcloud", 129, 167, 26, font="sans-semibold", anchor="middle", fill="#03466F", opacity=0.45)
    ic.text("Nextcloud", 128, 166, 26, font="sans-semibold", anchor="middle", fill="#F6FAFD")
    # chips at the edge, showing the iron
    for x, y, d in ((228, 150, "c2 -3 4 -1 6 2 c-1 3-4 4-6 2z"), (30, 186, "c3 -1 5 1 4 4 c-2 1-4 0-4-4z"),
                    (60, 60, "c2 -1 6 -1 7 1 c-2 2-5 2-7-1z")):
        ic.path(f"M{x} {y}{d}", fill="#2A2522")
        ic.path(f"M{x} {y}{d}", fill="none", stroke="#9C5A2A", stroke_opacity=0.7, stroke_width=0.8)
    for x, y in ((40, 76), (216, 76), (40, 180), (216, 180)):
        ic.circle(x, y, 5.5, fill="#03466F", opacity=0.5)
        _screw(ic, x, y, 4.2, slot=30 + x % 50)
    # the sheen on the domed enamel
    ic.path("M22 86a28 28 0 0 1 28-28h104L72 198H50a28 28 0 0 1-28-28z", fill=glare(ic, 1.1))
    ic.path("M44 62 H210", stroke="#fff", stroke_opacity=0.5, stroke_width=1.5, stroke_linecap="round")


@small("nextcloud")
def nextcloud16(ic):
    tile(ic, "#3B4A5A", "#18212B")
    ic.rect(1.5, 3.5, 13, 9, rx=1.4, fill="#0082C9")
    ic.circle(8, 8, 1.9, fill="none", stroke="#fff", stroke_width=1)
    ic.circle(4.3, 8, 1, fill="none", stroke="#fff", stroke_width=0.8)
    ic.circle(11.7, 8, 1, fill="none", stroke="#fff", stroke_width=0.8)


# --- Syncthing: its mark as a brass mechanism on a wooden base -------------

@icon("syncthing", kind="app", names=["me.kozec.syncthingtk", "syncthing", "syncthing-gtk", "syncthingtray"],
      title="Syncthing")
def syncthing(ic):
    tile(ic, "#2C7FA6", "#0F3A52")
    shadow(ic, 128, 214, 86, 11)
    cx, cy, r = 128, 102, 70
    # the base, turned wood
    ic.path("M60 196 v10 a68 12 0 0 0 136 0 v-10z", fill=wood(ic, "#8A5530", "#3E200E"))
    ic.ellipse(128, 196, 68, 12, fill=wood(ic, "#C48A55", "#7A4A22"))
    ic.ellipse(128, 196, 68, 12, fill="none", stroke="#fff", stroke_opacity=0.2)
    ic.ellipse(128, 195, 40, 6.5, fill="none", stroke="#5E3518", stroke_opacity=0.35)
    _engraved(ic, "SYNCTHING", 128, 214, 6.5, "#F6DDA0", font="mono-semibold", anchor="middle", spacing=2.2,
              light="#000", dark="#000", lo=0.5, do=0)
    # the post
    ic.path("M122 168 h12 l4 26 h-20z", fill=brass(ic, 0, 0, 1, 0))
    ic.ellipse(128, 194, 12, 3, fill="#5E4012")
    # the ring
    ic.circle(cx + 2, cy + 4, r, fill="none", stroke="#000", stroke_opacity=0.3, stroke_width=13)
    ic.circle(cx, cy, r, fill="none", stroke=brass(ic), stroke_width=12)
    ic.circle(cx, cy, r + 6, fill="none", stroke="#FFF1C8", stroke_opacity=0.5, stroke_width=1,
              stroke_dasharray="120 400", transform=f"rotate(-140 {cx} {cy})")
    ic.circle(cx, cy, r - 6, fill="none", stroke="#3A2A10", stroke_opacity=0.4, stroke_width=1)
    for k in range(72):
        x1, y1 = polar(cx, cy, r + 4, k * 5)
        x2, y2 = polar(cx, cy, r + (0 if k % 6 else -3), k * 5)
        ic.line(x1, y1, x2, y2, stroke="#4A3410", stroke_opacity=0.55, stroke_width=0.7)
    # the hub, and the rods out to the three nodes on the ring
    hx, hy = 138, 112
    nodes = [polar(cx, cy, r, a) for a in (40, 156, 282)]
    for nx, ny in nodes:
        ic.line(hx + 1.5, hy + 3, nx + 1.5, ny + 3, stroke="#000", stroke_opacity=0.3, stroke_width=5)
    for nx, ny in nodes:
        ic.line(hx, hy, nx, ny, stroke=steel(ic, False), stroke_width=4.5, stroke_linecap="round")
        ic.line(hx - 1, hy - 1, nx - 1, ny - 1, stroke="#fff", stroke_opacity=0.35, stroke_width=1)
    ball = ic.rad([(0, "#B8EBFF"), (0.35, "#2EA8E0"), (1, "#08456E")], cx=0.35, cy=0.3, r=0.75)
    for nx, ny in nodes:
        ic.circle(nx + 1.5, ny + 3, 15, fill="#000", opacity=0.35)
        ic.circle(nx, ny, 15, fill=ball)
        ic.ellipse(nx - 5, ny - 6, 5, 3, fill="#fff", opacity=0.6, transform=f"rotate(-35 {nx - 5} {ny - 6})")
    ic.circle(hx + 1, hy + 2, 10, fill="#000", opacity=0.35)
    ic.circle(hx, hy, 10, fill=ic.rad([(0, "#FFF2C8"), (0.5, "#C99645"), (1, "#5E4012")], cx=0.35, cy=0.3, r=0.75))


@small("syncthing")
def syncthing16(ic):
    tile(ic, "#2C7FA6", "#0F3A52")
    ic.circle(8, 7.2, 5, fill="none", stroke="#D2A458", stroke_width=1.2)
    pts = [polar(8, 7.2, 5, a) for a in (40, 156, 282)]
    for x, y in pts:
        ic.line(8.6, 7.9, x, y, stroke="#E3E6EA", stroke_width=0.8)
    for x, y in pts:
        ic.circle(x, y, 1.6, fill="#3DB6EC")
    ic.rect(7.4, 12.2, 1.2, 1.4, fill="#D2A458")
    ic.rect(4.5, 13.4, 7, 1.3, rx=0.6, fill="#8A5530")


# --- Transmission: a red radio transmitter, its aerial up -------------------

@icon("transmission", kind="app", names=["com.transmissionbt.Transmission", "transmission", "transmission-gtk",
                                         "transmission-qt"], title="Transmission")
def transmission(ic):
    tile(ic, "#4C5866", "#1C232B")
    shadow(ic, 124, 214, 104, 12)
    ic.add('<g transform="translate(128 120) scale(1.07) translate(-128 -120)">')
    # the aerial, behind the cabinet, and its waves
    tip = (204, 30)
    for r, op in ((9, 0.8), (16, 0.55), (23, 0.3)):
        for a1, a2 in ((50, 130), (230, 310)):
            x1, y1 = polar(tip[0], tip[1], r, a1)
            x2, y2 = polar(tip[0], tip[1], r, a2)
            ic.path(f"M{x1:.1f} {y1:.1f}A{r} {r} 0 0 1 {x2:.1f} {y2:.1f}", fill="none", stroke="#FFD9C8",
                    stroke_opacity=op, stroke_width=2.6, stroke_linecap="round")
    for y1, y2, w in ((90, 64, 5), (64, 42, 3.6), (42, 28, 2.4)):
        ic.line(204, y1, 204, y2, stroke=steel(ic), stroke_width=w, stroke_linecap="butt")
        ic.line(203, y1, 203, y2, stroke="#fff", stroke_opacity=0.5, stroke_width=0.8)
    ic.circle(204, 26, 4, fill=ic.rad([(0, "#fff"), (1, "#7A818A")], cx=0.35, cy=0.3))
    ic.rect(198, 86, 12, 10, rx=2, fill=steel(ic))
    # the carrying handle
    ic.path("M62 92 V80 a10 10 0 0 1 10 -10 h56 a10 10 0 0 1 10 10 V92", fill="none", stroke="#16181B",
            stroke_width=8, stroke_linecap="round")
    ic.path("M62 92 V80 a10 10 0 0 1 10 -10 h56 a10 10 0 0 1 10 10 V92", fill="none", stroke="#3A3E44",
            stroke_width=6, stroke_linecap="round")
    ic.path("M64 82 a8 8 0 0 1 8 -8 h56", fill="none", stroke="#fff", stroke_opacity=0.25, stroke_width=1.2)
    # the cabinet, red enamel
    ic.rect(28, 90, 196, 116, rx=14, fill="#000", opacity=0.35, transform="translate(2 4)")
    ic.rect(28, 90, 196, 116, rx=14, fill=ic.lin([(0, "#F0624E"), (0.5, "#D23A28"), (1, "#8E1A10")], 0, 0, 0.5, 1))
    ic.rect(28.75, 90.75, 194.5, 114.5, rx=13.25, fill="none", stroke="#FFC4B8", stroke_opacity=0.5, stroke_width=1.5)
    # the panel
    ic.rect(38, 104, 176, 92, rx=7, fill="#5A0E08", opacity=0.6, transform="translate(-0.8 -0.8)")
    ic.rect(38, 104, 176, 92, rx=7, fill=ic.lin([(0, "#F7F2E7"), (1, "#D8D0BF")]))
    # the tuning dial
    dx, dy = 80, 148
    ic.circle(dx, dy, 34, fill="#2A2C30")
    ic.circle(dx, dy, 32, fill=ic.rad([(0, "#FFFDF7"), (1, "#E6DCC6")], cx=0.45, cy=0.4, r=0.65))
    for k in range(25):
        a = -120 + k * 10
        x1, y1 = polar(dx, dy, 30, a)
        x2, y2 = polar(dx, dy, 30 - (6 if k % 4 == 0 else 3), a)
        ic.line(x1, y1, x2, y2, stroke="#2A2C30", stroke_width=1.2 if k % 4 == 0 else 0.7)
    for n, a in (("7", -120), ("14", -40), ("21", 40), ("28", 120)):
        x, y = polar(dx, dy, 18, a)
        ic.text(n, x, y + 2.5, 7, font="mono-semibold", anchor="middle", fill="#2A2C30")
    ic.text("MHz", dx, dy + 24, 5.5, font="mono", anchor="middle", fill="#8C887F")
    ic.circle(dx + 1, dy + 2, 11, fill="#000", opacity=0.3)
    ic.circle(dx, dy, 11, fill=ic.lin([(0, "#4A4E55"), (1, "#111214")], 0, 0, 1, 1))
    ic.circle(dx, dy, 11, fill="none", stroke="#fff", stroke_opacity=0.25, stroke_dasharray="1.5 1.5")
    with ic.g(transform=f"rotate(28 {dx} {dy})"):
        ic.rect(dx - 1, dy - 30, 2, 28, rx=1, fill="#C8372D")
    ic.circle(dx - 3, dy - 3, 2.5, fill="#fff", opacity=0.4)
    # the meter
    mx, my, mw, mh = 124, 112, 80, 40
    ic.rect(mx - 2, my - 2, mw + 4, mh + 4, rx=4, fill="#2A2C30")
    ic.rect(mx, my, mw, mh, rx=2.5, fill=ic.lin([(0, "#FFF6D8"), (1, "#E9D7A0")]))
    pc = (mx + mw / 2, my + mh + 14)
    for k in range(11):
        a = -42 + k * 8.4
        x1, y1 = polar(pc[0], pc[1], 44, a)
        x2, y2 = polar(pc[0], pc[1], 44 - (6 if k % 5 == 0 else 3.5), a)
        ic.line(x1, y1, x2, y2, stroke="#C8372D" if k >= 8 else "#2A2C30", stroke_width=1)
    ic.path(f"M{polar(pc[0], pc[1], 44, -42)[0]:.1f} {polar(pc[0], pc[1], 44, -42)[1]:.1f}"
            f"A44 44 0 0 1 {polar(pc[0], pc[1], 44, 42)[0]:.1f} {polar(pc[0], pc[1], 44, 42)[1]:.1f}",
            fill="none", stroke="#2A2C30", stroke_width=0.8)
    ic.text("TX", mx + 6, my + mh - 5, 7, font="mono-semibold", fill="#2A2C30")
    ic.text("SWR", mx + mw - 6, my + mh - 5, 6, font="mono", anchor="end", fill="#8C887F")
    with ic.g(transform=f"rotate(22 {pc[0]} {pc[1]})"):
        ic.line(pc[0], pc[1] - 8, pc[0], pc[1] - 46, stroke="#1E2024", stroke_width=1.3)
    ic.path(f"M{mx} {my + 2.5}a2.5 2.5 0 0 1 2.5 -2.5h30L{mx + 12} {my + mh}h-9.5a2.5 2.5 0 0 1 -2.5 -2.5z",
            fill="#fff", opacity=0.35)
    # knobs, a switch and the lamp
    for kx in (136, 164):
        ic.circle(kx + 1, 172 + 2, 9, fill="#000", opacity=0.3)
        ic.circle(kx, 172, 9, fill=ic.lin([(0, "#E9ECEF"), (1, "#5D636B")], 0, 0, 1, 1))
        ic.circle(kx, 172, 5, fill=ic.lin([(0, "#5D636B"), (1, "#C3C8CE")], 0, 0, 1, 1))
    ic.text("VOL", 136, 189, 5.5, font="mono", anchor="middle", fill="#55534E")
    ic.text("SQL", 164, 189, 5.5, font="mono", anchor="middle", fill="#55534E")
    ic.circle(196, 166, 5.5, fill="#5A0E08")
    ic.circle(196, 166, 4.2, fill=ic.rad([(0, "#FFD27A"), (1, "#E0482A")], cx=0.4, cy=0.35))
    ic.circle(196, 166, 9, fill="#FF8A4A", opacity=0.18)
    ic.text("ON AIR", 196, 182, 5.5, font="mono-semibold", anchor="middle", fill="#B42A1F")
    _engraved(ic, "TRANSMISSION", 126, 101, 7, "#FFE6DE", font="mono-semibold", anchor="middle", spacing=2.2,
              light="#000", dark="#000", lo=0.3, do=0)
    ic.add("</g>")


@small("transmission")
def transmission16(ic):
    tile(ic, "#4C5866", "#1C232B")
    ic.line(12.5, 6, 12.5, 1.8, stroke="#C3C8CE", stroke_width=0.8)
    ic.rect(1.5, 6, 13, 8, rx=1.2, fill="#D23A28")
    ic.rect(2.5, 7, 11, 6, rx=0.6, fill="#F2ECDF")
    ic.circle(5.4, 10, 2.2, fill="#2A2C30")
    ic.circle(5.4, 10, 1.6, fill="#FBF7EC")
    ic.rect(8.5, 8, 4, 2.4, rx=0.3, fill="#E9D7A0")
    ic.circle(11.6, 11.8, 0.7, fill="#E0482A")


# --- qBittorrent: a parcel, tied with twine, its blue globe stamp -----------

@icon("qbittorrent", kind="app", names=["org.qbittorrent.qBittorrent", "qbittorrent"], title="qBittorrent")
def qbittorrent(ic):
    tile(ic, "#3D76B5", "#1A3D69")
    shadow(ic, 130, 210, 104, 12)
    F = (36, 98, 168, 206)  # the front face: x1 y1 x2 y2
    ox, oy = 50, -34      # the depth, to the back right
    top = [(F[0], F[1]), (F[2], F[1]), (F[2] + ox, F[1] + oy), (F[0] + ox, F[1] + oy)]
    side = [(F[2], F[1]), (F[2] + ox, F[1] + oy), (F[2] + ox, F[3] + oy), (F[2], F[3])]
    ic.poly(top, fill=ic.lin([(0, "#F6DCA2"), (1, "#DDB56C")], 0, 0, 1, 1))
    ic.poly(side, fill=ic.lin([(0, "#B3833C"), (1, "#8A6026")], 0, 0, 1, 1))
    ic.rect(F[0], F[1], F[2] - F[0], F[3] - F[1], fill=ic.lin([(0, "#EBC77C"), (1, "#C69447")]))
    # the tape along the top's seam
    mid = F[1] + oy / 2
    ic.poly([(F[0] + ox / 2 - 10, mid), (F[2] + ox / 2 - 10, mid), (F[2] + ox / 2 + 10, mid), (F[0] + ox / 2 + 10, mid)],
            fill="#fff", opacity=0.2)
    ic.line(F[0], F[1], F[2], F[1], stroke="#FFF1C8", stroke_width=1.5, opacity=0.9)
    ic.line(F[2], F[1], F[2], F[3], stroke="#6E4A1A", stroke_opacity=0.5)
    ic.line(F[0] + ox, F[1] + oy, F[2] + ox, F[1] + oy, stroke="#FFF6DC", stroke_opacity=0.7)
    # twine: around both ways
    tw = dict(stroke="#F4EBD6", stroke_width=2.6, stroke_linecap="round")
    sh = dict(stroke="#6E4A1A", stroke_opacity=0.4, stroke_width=2.6)
    tx = 104  # the twine on the front
    for st in (sh, tw):
        d = 1 if st is sh else 0
        ic.line(tx + d, F[1], tx + d, F[3], **st)
        ic.line(tx + ox, F[1] + oy, tx, F[1], **st)
        ic.line(F[2] + ox / 2, F[1] + oy / 2 + d, F[2] + ox / 2, F[3] + oy / 2 + d, **st)
        ic.line(F[0] + ox / 2, F[1] + oy / 2 + d, F[2] + ox / 2, F[1] + oy / 2 + d, **st)
    # the bow, where they cross on top
    kx, ky = tx + ox / 2, F[1] + oy / 2
    for a in (-1, 1):
        ic.path(f"M{kx} {ky} q{a * 14} -14 {a * 18} -4 q{-a * 4} 8 {-a * 18} 4z", fill="none", stroke="#F4EBD6",
                stroke_width=2.4)
    ic.path(f"M{kx} {ky} q-4 10 -10 14 M{kx} {ky} q6 9 12 12", fill="none", stroke="#F4EBD6", stroke_width=2.2,
            stroke_linecap="round")
    ic.circle(kx, ky, 3, fill="#E8DCC0")
    # the label, right of the twine
    ic.rect(116, 112, 46, 36, fill="#000", opacity=0.15, transform="translate(1 1.5)")
    ic.rect(116, 112, 46, 36, fill=paper(ic, "white"))
    ic.text("TO:", 120, 121, 5.5, font="mono-semibold", fill="#8C887F")
    ic.text("~/Down-", 120, 132, 9, font="hand", fill="#2E3A55")
    ic.text("loads", 124, 142, 9, font="hand", fill="#2E3A55")
    ic.rect(116, 152, 46, 44, fill=paper(ic, "white"))
    for k in range(14):
        w = (1.6, 0.8, 1.2, 0.6)[k % 4]
        ic.rect(120 + k * 2.7, 156, w, 24, fill="#2A2C30")
    ic.text("ubuntu.iso", 139, 190, 5.6, font="mono", anchor="middle", fill="#55534E")
    # the stamp, blue ink, the globe and "qb"
    sx, sy = 70, 152
    ink = "#1F5FB0"
    with ic.g(transform=f"rotate(-14 {sx} {sy})", opacity=0.88):
        ic.circle(sx, sy, 28, fill="none", stroke=ink, stroke_width=2.6)
        ic.circle(sx, sy, 23, fill="none", stroke=ink, stroke_width=1)
        ic.circle(sx, sy, 17, fill=ink)
        for e in (6, 12):
            ic.ellipse(sx, sy, e, 17, fill="none", stroke="#E3BA6C", stroke_width=1)
        ic.line(sx - 17, sy, sx + 17, sy, stroke="#E3BA6C", stroke_width=1)
        ic.line(sx - 15, sy - 8, sx + 15, sy - 8, stroke="#E3BA6C", stroke_width=0.8)
        ic.line(sx - 15, sy + 8, sx + 15, sy + 8, stroke="#E3BA6C", stroke_width=0.8)
        ic.text("qb", sx, sy + 6.5, 19, font="sans-bold", anchor="middle", fill="#fff", stroke=ink, stroke_width=3,
                paint_order="stroke")
        for a in range(0, 360, 30):
            if a in (0, 180):
                continue
            x, y = polar(sx, sy, 25.5, a)
            ic.circle(x, y, 0.9, fill=ink)
        ic.text("POST", sx, sy - 19, 5, font="mono-semibold", anchor="middle", fill=ink)


@small("qbittorrent")
def qbittorrent16(ic):
    tile(ic, "#3D76B5", "#1A3D69")
    ic.poly([(2, 6), (11, 6), (14, 3.5), (5, 3.5)], fill="#F3D493")
    ic.poly([(11, 6), (14, 3.5), (14, 11.5), (11, 14)], fill="#9C7231")
    ic.rect(2, 6, 9, 8, fill="#DDB56C")
    ic.circle(5.6, 10, 2.6, fill="#1F5FB0")
    ic.line(8.8, 6, 8.8, 14, stroke="#F4EBD6", stroke_width=0.6)


# --- FileZilla: a red lorry, FZ on its box ---------------------------------

def _wheel(ic, x, y, r=19):
    ic.circle(x, y, r, fill="#151618")
    ic.circle(x, y, r, fill="none", stroke="#3A3D42", stroke_width=2, stroke_dasharray="2 2.4")
    ic.circle(x, y, r * 0.55, fill=ic.lin([(0, "#F2F4F6"), (1, "#6F767E")], 0, 0, 1, 1))
    ic.circle(x, y, r * 0.22, fill="#3A3E44")
    for a in range(0, 360, 72):
        hx, hy = polar(x, y, r * 0.38, a)
        ic.circle(hx, hy, 1.3, fill="#3A3E44")


@icon("filezilla", kind="app", names=["filezilla", "org.filezillaproject.Filezilla"], title="FileZilla")
def filezilla(ic):
    tile(ic, "#3E7480", "#173C45")
    shadow(ic, 128, 204, 108, 11)
    red = ic.lin([(0, "#F25A3E"), (0.5, "#D9341E"), (1, "#9A1C0E")])
    # the chassis
    ic.rect(28, 168, 196, 14, rx=3, fill="#1E2024")
    # the box
    ic.rect(28, 58, 140, 112, rx=6, fill="#000", opacity=0.3, transform="translate(2 3)")
    ic.rect(28, 58, 140, 112, rx=6, fill=ic.lin([(0, "#F7F2E7"), (1, "#D2C9B6")], 0, 0, 1, 1))
    ic.line(32, 59, 164, 59, stroke="#fff", stroke_width=1.5)
    for x in (62, 96, 130):
        ic.line(x, 62, x, 166, stroke="#000", stroke_opacity=0.06, stroke_width=1.5)
    # the mark on its side: red, Fz
    ic.rect(40, 70, 64, 64, rx=10, fill="#7A1208", transform="translate(1 1.5)")
    ic.rect(40, 70, 64, 64, rx=10, fill=red)
    ic.text("Fz", 72, 118, 42, font="sans-bold", anchor="middle", spacing=-1, fill="#7A1208",
            transform="translate(1 1.5)")
    ic.text("Fz", 72, 118, 42, font="sans-bold", anchor="middle", spacing=-1, fill="#FFF6EC")
    ic.path("M40 80a10 10 0 0 1 10-10h40L58 134h-8a10 10 0 0 1-10-10z", fill="#fff", opacity=0.14)
    ic.text("FileZilla", 112, 90, 14, font="sans-bold", fill="#B42A1F")
    ic.text("FTP · SFTP", 112, 102, 6.5, font="mono-semibold", spacing=0.6, fill="#55534E")
    ic.text("FAST FREIGHT", 112, 128, 6, font="mono", spacing=0.6, fill="#8C887F")
    ic.rect(112, 132, 48, 2, fill="#B42A1F", opacity=0.7)
    # the cab
    cab = "M170 92 h26 a10 10 0 0 1 9 6 l16 34 a12 12 0 0 1 1 5 v33 h-52z"
    ic.path(cab, fill="#000", opacity=0.3, transform="translate(2 3)")
    ic.path(cab, fill=red)
    ic.path("M174 100 h20 a6 6 0 0 1 5.4 3.4 l12 25.6 h-37.4z", fill="#1A2630")
    ic.path("M174 100 h20 a6 6 0 0 1 5.4 3.4 l12 25.6 h-37.4z", fill=glare(ic, 1.6))
    ic.path("M176 103 h10 l-8 22 h-2z", fill="#fff", opacity=0.25)
    ic.line(172, 93, 196, 93, stroke="#FFC4B8", stroke_width=1.5, opacity=0.8)
    ic.line(176, 140, 186, 140, stroke="#5A0E08", stroke_width=2, stroke_linecap="round")
    ic.line(172, 132, 172, 168, stroke="#5A0E08", stroke_opacity=0.5)
    ic.rect(214, 152, 10, 8, rx=2, fill="#FFD27A")
    ic.rect(212, 164, 14, 6, rx=2, fill=steel(ic))
    # wheels
    for x in (62, 104, 194):
        _wheel(ic, x, 182)
    ic.path("M44 170 a20 20 0 0 1 36 0 M86 170 a20 20 0 0 1 36 0 M176 170 a20 20 0 0 1 36 0", fill="none",
            stroke="#1E2024", stroke_width=4)


@small("filezilla")
def filezilla16(ic):
    tile(ic, "#3E7480", "#173C45")
    ic.rect(1.5, 3.5, 9, 7.5, rx=0.6, fill="#F2ECDF")
    ic.rect(2.5, 4.5, 4.5, 4.5, rx=0.8, fill="#D9341E")
    ic.path("M11 6 h2 l1.5 3 v2.5 h-3.5z", fill="#D9341E")
    ic.rect(1.5, 11, 13, 1.2, fill="#1E2024")
    for x in (4, 12):
        ic.circle(x, 12.6, 1.5, fill="#151618")
        ic.circle(x, 12.6, 0.6, fill="#C3C8CE")


# --- Proton VPN: a violet glass prism ---------------------------------------

@icon("proton-vpn", kind="app", names=["com.protonvpn.www", "proton-vpn", "proton-vpn-logo", "protonvpn"],
      title="Proton VPN")
def proton_vpn(ic):
    tile(ic, "#4F3E8E", "#1E1544")
    shadow(ic, 132, 204, 102, 12)
    A, L, R = (110, 34), (34, 190), (186, 190)  # the front face
    ox, oy = 34, -12
    # the side face, darker
    ic.poly([A, (A[0] + ox, A[1] + oy), (R[0] + ox, R[1] + oy), R],
            fill=ic.lin([(0, "#4B2FB8"), (1, "#1C0E5C")], 0, 0, 1, 1))
    ic.line(A[0], A[1], A[0] + ox, A[1] + oy, stroke="#E5DBFF", stroke_width=1.5, opacity=0.8)
    ic.line(R[0], R[1], R[0] + ox, R[1] + oy, stroke="#000", stroke_opacity=0.3)
    # the front face: teal at the top to violet
    ic.poly([A, L, R], fill=ic.lin([(0, "#7FF3D8"), (0.35, "#6D9CFF"), (0.7, "#6D4AFF"), (1, "#3A1FA8")],
                                   0.2, 0, 0.6, 1))
    # the mark, cut into the glass: a triangle in a triangle
    inner = [(110, 78), (68, 166), (152, 166)]
    ic.poly(inner, fill="none", stroke="#1E0E6A", stroke_opacity=0.4, stroke_width=7, stroke_linejoin="round",
            transform="translate(1 1.5)")
    ic.poly(inner, fill="none", stroke="#F2EEFF", stroke_opacity=0.9, stroke_width=6, stroke_linejoin="round")
    ic.poly([(110, 108), (88, 154), (132, 154)], fill="#F2EEFF", opacity=0.85)
    # edges and light
    ic.line(A[0], A[1], L[0], L[1], stroke="#fff", stroke_width=2, opacity=0.85)
    ic.line(L[0], L[1], R[0], R[1], stroke="#1C0E5C", stroke_width=1.5, opacity=0.6)
    ic.poly([A, (92, 72), (54, 168), (40, 180)], fill="#fff", opacity=0.22)
    ic.text("PROTON VPN", 110, 184, 8, font="mono-semibold", anchor="middle", spacing=1.8, fill="#F2EEFF", opacity=0.7)


@small("proton-vpn")
def proton_vpn16(ic):
    tile(ic, "#4F3E8E", "#1E1544")
    ic.poly([(9.5, 2), (12.5, 1.5), (14, 13), (11.5, 13.6)], fill="#3A1FA8")
    ic.poly([(7, 2), (1.6, 13.6), (12, 13.6)], fill="#6D6DFF")
    ic.poly([(7, 6), (4.6, 11.4), (9.4, 11.4)], fill="#F2EEFF")
    ic.line(7, 2, 1.6, 13.6, stroke="#8FF5DC", stroke_width=0.8)


# --- OneKey: a hardware wallet on its cable ---------------------------------

@icon("onekey", kind="app", names=["onekey", "so.onekey.app.wallet"], title="OneKey")
def onekey(ic):
    tile(ic, "#2E8A52", "#0F3F25")
    shadow(ic, 128, 214, 76, 11)
    # the cable, out of the bottom and away right
    ic.path("M128 206 C128 226 160 222 184 212 S206 200 212 196", fill="none", stroke="#000", stroke_opacity=0.3,
            stroke_width=8, transform="translate(1 3)")
    ic.path("M128 206 C128 226 160 222 184 212 S206 200 212 196", fill="none", stroke="#E9ECEF", stroke_width=7)
    ic.path("M128 206 C128 224 160 220 182 210", fill="none", stroke="#fff", stroke_opacity=0.7, stroke_width=1.5)
    with ic.g(transform="rotate(56 212 196)"):
        ic.rect(206, 181, 12, 17, rx=3, fill="#000", opacity=0.3, transform="translate(2 1)")
        ic.rect(206, 181, 12, 17, rx=3, fill="#E9ECEF")
        ic.rect(208, 172, 8, 10, rx=1, fill=steel(ic))
    ic.rect(121, 196, 14, 14, rx=3, fill=steel(ic))
    # the body
    ic.rect(66, 28, 124, 174, rx=22, fill="#000", opacity=0.4, transform="translate(3 4)")
    ic.rect(66, 28, 124, 174, rx=22, fill=ic.lin([(0, "#3C4044"), (0.4, "#1E2023"), (1, "#0A0B0C")], 0, 0, 1, 1))
    ic.rect(66.75, 28.75, 122.5, 172.5, rx=21.25, fill="none", stroke="#fff", stroke_opacity=0.18, stroke_width=1.5)
    # the lanyard hole
    ic.circle(172, 44, 5, fill="#050607")
    ic.circle(172, 44, 5, fill="none", stroke="#fff", stroke_opacity=0.15)
    # the screen
    ic.rect(80, 52, 96, 96, rx=8, fill="#050607")
    ic.rect(84, 56, 88, 88, rx=4, fill="#0B0D0E")
    # on it: the mark, a black tile with a 1 and a keyhole, and what to sign
    ic.rect(110, 62, 36, 36, rx=10, fill="#00B812")
    ic.rect(110, 62, 36, 36, rx=10, fill="none", stroke="#fff", stroke_opacity=0.25)
    ic.text("1", 128, 89, 27, font="sans-bold", anchor="middle", fill="#0B0D0E")
    ic.text("Send", 128, 112, 8, font="sans-semibold", anchor="middle", fill="#E9ECEF")
    ic.text("0.25 BTC", 128, 123, 9, font="mono-semibold", anchor="middle", fill="#fff")
    ic.rect(92, 130, 72, 10, rx=5, fill="#00B812")
    ic.text("Confirm", 128, 137.6, 6.5, font="sans-semibold", anchor="middle", fill="#0B0D0E")
    ic.path("M84 60a4 4 0 0 1 4-4h40L94 144h-6a4 4 0 0 1-4-4z", fill=glare(ic, 1.2))
    # the buttons: a four-way pad and two keys
    bx, by = 128, 172
    ic.circle(bx + 1, by + 2, 18, fill="#000", opacity=0.4)
    ic.circle(bx, by, 18, fill=ic.lin([(0, "#3A3D42"), (1, "#141517")], 0, 0, 1, 1))
    ic.circle(bx, by, 18, fill="none", stroke="#fff", stroke_opacity=0.2)
    for a in (0, 90, 180, 270):
        x, y = polar(bx, by, 12, a)
        ic.path(f"M{x:.1f} {y:.1f}m0 -2.6l2.6 4h-5.2z", fill="#9AA1A9", transform=f"rotate({a} {x:.1f} {y:.1f})")
    ic.circle(bx, by, 6, fill=ic.lin([(0, "#4A4E55"), (1, "#1A1B1E")], 0, 0, 1, 1))
    ic.circle(bx, by, 6, fill="none", stroke="#00B812", stroke_opacity=0.8, stroke_width=1.2)
    for x, glyph in ((90, "x"), (166, "ok")):
        ic.circle(x + 0.6, 172 + 1.4, 8, fill="#000", opacity=0.4)
        ic.circle(x, 172, 8, fill=ic.lin([(0, "#3A3D42"), (1, "#141517")], 0, 0, 1, 1))
        ic.circle(x, 172, 8, fill="none", stroke="#fff", stroke_opacity=0.2)
        if glyph == "x":
            ic.path(f"M{x - 3} 169 l6 6 M{x + 3} 169 l-6 6", stroke="#E05A4A", stroke_width=1.6, stroke_linecap="round")
        else:
            ic.path(f"M{x - 3.5} 172 l2.5 2.6 l4.5 -5", fill="none", stroke="#00D21A", stroke_width=1.6,
                    stroke_linecap="round", stroke_linejoin="round")
    ic.text("OneKey", 128, 196, 6, font="mono-semibold", anchor="middle", spacing=1.6, fill="#9AA1A9", opacity=0.6)


@small("onekey")
def onekey16(ic):
    tile(ic, "#2E8A52", "#0F3F25")
    ic.rect(4, 1.5, 8, 12.5, rx=1.6, fill="#1A1C1E")
    ic.rect(5, 2.6, 6, 6, rx=0.6, fill="#050607")
    ic.rect(6.2, 3.8, 3.6, 3.6, rx=0.9, fill="#00B812")
    ic.circle(8, 11.2, 1.3, fill="#4A4E55")
    ic.rect(7.3, 14, 1.4, 1.2, fill="#C3C8CE")


# --- TradingView: a monitor showing a chart, the mark on its chin -----------

@icon("tradingview", kind="app", names=["tradingview"], title="TradingView")
def tradingview(ic):
    tile(ic, "#2F3A50", "#10151F")
    shadow(ic, 128, 214, 80, 10)
    # stand and foot
    ic.path("M112 170 h32 l8 34 h-48z", fill=ic.lin([(0, "#E3E6EA"), (0.5, "#B7BDC4"), (1, "#7A818A")], 0, 0, 1, 0))
    ic.rect(80, 202, 96, 10, rx=5, fill=ic.lin([(0, "#E9ECEF"), (1, "#8A9098")]))
    ic.line(84, 203, 172, 203, stroke="#fff", stroke_opacity=0.8)
    # the monitor: aluminium, a chin
    ic.rect(22, 34, 212, 146, rx=10, fill="#000", opacity=0.35, transform="translate(2 4)")
    ic.rect(22, 34, 212, 146, rx=10, fill=ic.lin([(0, "#F2F4F6"), (0.6, "#C3C8CE"), (1, "#8A9098")], 0, 0, 0.4, 1))
    ic.rect(22.75, 34.75, 210.5, 144.5, rx=9.25, fill="none", stroke="#fff", stroke_opacity=0.8, stroke_width=1.5)
    ic.rect(28, 40, 200, 116, rx=4, fill="#0B0D10")
    # the chart
    sx, sy, sw, sh = 32, 44, 192, 108
    ic.rect(sx, sy, sw, sh, rx=2, fill="#131722")
    for k in range(1, 5):
        ic.line(sx, sy + k * sh / 5, sx + sw - 30, sy + k * sh / 5, stroke="#fff", stroke_opacity=0.06)
    for k in range(1, 6):
        ic.line(sx + k * 28, sy + 14, sx + k * 28, sy + sh, stroke="#fff", stroke_opacity=0.06)
    ic.text("BTCUSD · 1D", sx + 6, sy + 10, 6.5, font="mono-semibold", fill="#D1D4DC")
    ic.text("+2.41%", sx + 62, sy + 10, 6.5, font="mono-semibold", fill="#26A69A")
    # candles: open, close, high, low (screen y)
    candles = [(130, 120, 112, 136), (120, 126, 116, 132), (126, 110, 106, 128), (110, 114, 102, 120),
               (114, 98, 92, 118), (98, 104, 94, 110), (104, 90, 84, 108), (90, 96, 86, 102),
               (96, 80, 72, 100), (80, 86, 76, 92), (86, 70, 62, 90), (70, 76, 66, 82), (76, 62, 56, 80)]
    for i, (o, c, h, l) in enumerate(candles):
        x = sx + 10 + i * 12
        up = c < o
        col = "#26A69A" if up else "#EF5350"
        ic.line(x, h, x, l, stroke=col, stroke_width=1.2)
        ic.rect(x - 3.5, min(o, c), 7, max(abs(o - c), 1.5), fill=col)
    # the moving average
    ic.path("M42 130 C70 124 90 112 112 108 S150 92 170 82 S192 68 194 66", fill="none", stroke="#2962FF",
            stroke_width=1.8)
    # the price axis
    ic.rect(sx + sw - 28, sy, 28, sh, fill="#131722")
    ic.line(sx + sw - 28, sy, sx + sw - 28, sy + sh, stroke="#fff", stroke_opacity=0.1)
    for k, p in enumerate(("71,200", "69,800", "68,400", "67,000")):
        ic.text(p, sx + sw - 3, sy + 30 + k * 22, 5.2, font="mono", anchor="end", fill="#787B86")
    ic.rect(sx + sw - 28, 58, 28, 9, rx=1.5, fill="#26A69A")
    ic.text("72,410", sx + sw - 3, 64.8, 5.4, font="mono-semibold", anchor="end", fill="#fff")
    ic.line(sx + 10 + 12 * 12, 62, sx + sw - 28, 62, stroke="#26A69A", stroke_dasharray="2 2", stroke_opacity=0.7)
    ic.path("M28 44a4 4 0 0 1 4-4h90L66 156H32a4 4 0 0 1-4-4z", fill=glare(ic, 0.8))
    # the mark on the chin: a T, a dot, a slant
    k_ = 0.5
    with ic.g(transform="translate(128 168)"):
        ic.path("M-24 -6 h14 v12 h-6 v-6 h-8z", fill="#131722")
        ic.circle(-1.5, -2.5, 3.5, fill="#131722")
        ic.path("M6 6 l7 -12 h8 l-7 12z", fill="#131722")
    ic.circle(200, 168, 1.6, fill="#7CF7A6", opacity=k_ + 0.3)


@small("tradingview")
def tradingview16(ic):
    tile(ic, "#2F3A50", "#10151F")
    ic.rect(1.5, 2.5, 13, 9.5, rx=1, fill="#C3C8CE")
    ic.rect(2.3, 3.3, 11.4, 7.2, rx=0.4, fill="#131722")
    for i, (y, h, c) in enumerate(((7, 2.5, "#EF5350"), (6, 2.5, "#26A69A"), (5.5, 2, "#EF5350"), (4, 3, "#26A69A"))):
        ic.rect(3.6 + i * 2.4, y, 1.4, h, fill=c)
    ic.rect(7, 12, 2, 1.6, fill="#9AA1A9")
    ic.rect(5, 13.4, 6, 1, rx=0.5, fill="#C3C8CE")


# --- Fcitx: a keyboard with Cangjie radicals, the candidates on a card -----

_CANGJIE = {"W": "田", "R": "口", "U": "山", "O": "人", "A": "日", "D": "木", "G": "土", "J": "十", "K": "大",
            "L": "中", "M": "一"}


@icon("fcitx", kind="app", names=["cs-keyboard", "fcitx", "fcitx-setting", "fcitx_ubuntukylin",
                                  "gnome-settings-accessibility-keyboard", "gnome-settings-accessibility-technologies",
                                  "kimtoy", "ktouch", "org.fcitx.Fcitx5", "org.kde.ktouch", "org.xfce.settings.keyboard",
                                  "preferences-desktop-keyboard", "system-config-keyboard", "yast-keyboard"],
      title="Fcitx")
def fcitx(ic):
    tile(ic, "#565C8C", "#23264A")
    shadow(ic, 128, 214, 108, 11)
    # the card of candidates, in a brass stand behind the keyboard
    ic.rect(42, 30, 172, 64, rx=8, fill="#000", opacity=0.3, transform="translate(2 4)")
    ic.rect(42, 30, 172, 64, rx=8, fill=paper(ic, "cream"))
    ic.line(48, 31, 208, 31, stroke="#fff", stroke_width=1.5)
    ic.text("zhongwen", 54, 50, 13, font="mono-semibold", fill="#2E3A55")
    ic.rect(125, 39, 1.6, 14, fill="#2463AE")
    ic.line(54, 54, 124, 54, stroke="#2E3A55", stroke_opacity=0.5, stroke_dasharray="2 1.6")
    ic.rect(50, 60, 66, 26, rx=5, fill="#2463AE")
    ic.text("1", 56, 78, 9, font="mono-semibold", fill="#fff", opacity=0.75)
    _han(ic, "中", 66, 63, 20, "#fff", width=2.4)
    _han(ic, "文", 89, 63, 20, "#fff", width=2.4)
    ic.text("2", 124, 78, 9, font="mono-semibold", fill="#8C887F")
    _han(ic, "中", 134, 63, 20, "#2A2C30", width=2.2)
    ic.text("3", 164, 78, 9, font="mono-semibold", fill="#8C887F")
    _han(ic, "文", 174, 63, 20, "#2A2C30", width=2.2)
    ic.path("M196 50 l4 -4 l4 4", fill="none", stroke="#8C887F", stroke_width=1.4, stroke_linecap="round")
    ic.path("M196 74 l4 4 l4 -4", fill="none", stroke="#8C887F", stroke_width=1.4, stroke_linecap="round")
    # the keyboard
    ic.rect(18, 100, 220, 108, rx=14, fill="#000", opacity=0.35, transform="translate(2 4)")
    ic.rect(18, 100, 220, 108, rx=14, fill=ic.lin([(0, "#D9DCE3"), (1, "#8E93A0")], 0, 0, 0.3, 1))
    ic.rect(18.75, 100.75, 218.5, 106.5, rx=13.25, fill="none", stroke="#fff", stroke_opacity=0.7, stroke_width=1.5)
    ic.rect(26, 108, 204, 92, rx=8, fill="#3A3D48")
    rows = ("QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM")
    kw, kh, gap = 18, 19, 2.2
    cap = ic.lin([(0, "#FFFFFF"), (1, "#E2E4EA")])
    for r, row in enumerate(rows):
        x0 = 30 + r * 7
        y = 112 + r * (kh + 2.6)
        for i, ch in enumerate(row):
            x = x0 + i * (kw + gap)
            ic.rect(x, y + 1.6, kw, kh, rx=3, fill="#1E2028")
            ic.rect(x, y, kw, kh, rx=3, fill=cap)
            ic.rect(x + 2, y + 0.8, kw - 4, 1, rx=0.5, fill="#fff")
            ic.text(ch, x + 2.6, y + 8, 6.5, font="sans-semibold", fill="#2A2C30")
            if ch in _CANGJIE:
                _han(ic, _CANGJIE[ch], x + 8.6, y + 8.8, 8, "#C8372D", width=1.2)
    # the bottom row: a switch key, the space bar, a key lit for the input method
    y = 112 + 3 * (kh + 2.6)
    for x, w, fill in ((30, 30, "#2463AE"), (64, 128, None), (196, 30, None)):
        ic.rect(x, y + 1.6, w, kh, rx=3, fill="#1E2028")
        ic.rect(x, y, w, kh, rx=3, fill=fill or cap)
        ic.rect(x + 2, y + 0.8, w - 4, 1, rx=0.5, fill="#fff", opacity=0.5 if fill else 1)
    _han(ic, "中", 38, y + 3, 13, "#fff", width=1.7)
    ic.text("ctrl", 211, y + 12.5, 7, font="sans-semibold", anchor="middle", fill="#2A2C30")
    ic.text("fcitx", 128, y + 12.5, 7, font="mono", anchor="middle", spacing=1, fill="#8C887F")


@small("fcitx")
def fcitx16(ic):
    tile(ic, "#565C8C", "#23264A")
    ic.rect(3, 1.5, 10, 5, rx=1, fill="#F6F1E6")
    ic.path("M6 2.6 V6 M4.6 3.4 H7.4 V5 H4.6Z", fill="none", stroke="#2463AE", stroke_width=0.7)
    ic.rect(1, 7.5, 14, 7, rx=1.2, fill="#B7BCC8")
    ic.rect(1.8, 8.2, 12.4, 5.6, rx=0.6, fill="#3A3D48")
    for r in range(2):
        for i in range(5):
            ic.rect(2.4 + i * 2.4 + r * 0.6, 8.7 + r * 2, 1.8, 1.5, rx=0.3, fill="#F2F3F6")
    ic.rect(4.6, 12.5, 6.8, 1, rx=0.3, fill="#F2F3F6")
    ic.rect(2.4, 12.5, 1.8, 1, rx=0.3, fill="#2463AE")
