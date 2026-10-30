"""The inua-objects theme, tier 2, talk and mail: WhatsApp, Teams, Skype,
Evolution, Geary, Fractal, Dino, Pidgin, HexChat, Ferdium, Mattermost,
Rocket.Chat, Proton Mail, Mailspring, Betterbird, Tuta
(docs/feat/object-icons.md, Part 2). Each is its own object, not an
envelope or a bubble: a rotary telephone, a speakerphone, a headset, a card
file, a letterbox, a walkie-talkie, a tin dinosaur, a carrier pigeon, a
telegraph key, a switchboard, a ship's bell, a tin rocket, a safe, a spring
balance, a birdhouse and a postman's satchel."""

import math

from lib import (brass, glare, graphite, icon, leather, paper, polar, shadow, small, steel, tile, wood)


# --- shared --------------------------------------------------------------

def _screw(ic, x, y, r=2.6):
    ic.circle(x, y, r, fill=steel(ic, False))
    ic.line(x - r * 0.7, y + r * 0.7, x + r * 0.7, y - r * 0.7, stroke="#3A3E44", stroke_width=max(0.6, r * 0.35))


def _rim(ic, cx, cy, r, w=1.5, light=0.22, dark=0.25):
    """A lit edge on a disc: light top left, dark bottom right."""
    ic.path(f"M{cx - r * 0.92:.1f} {cy + r * 0.38:.1f}A{r} {r} 0 0 1 {cx + r * 0.38:.1f} {cy - r * 0.92:.1f}",
            fill="none", stroke="#fff", stroke_opacity=light, stroke_width=w, stroke_linecap="round")
    ic.path(f"M{cx + r * 0.92:.1f} {cy - r * 0.38:.1f}A{r} {r} 0 0 1 {cx - r * 0.38:.1f} {cy + r * 0.92:.1f}",
            fill="none", stroke="#000", stroke_opacity=dark, stroke_width=w, stroke_linecap="round")


def _wa_handset(ic, cx, cy, r, fg):
    """The handset inside WhatsApp's bubble, on a 20 unit grid around (cx, cy)."""
    k = r / 10
    d = ("M-4.4 -5.6c-1.2 .2-2.2 1.6-1.8 3.4c.8 3.8 4.4 7.6 8.4 8.6c1.8 .4 3.2-.6 3.4-1.8"
         "l.2-1.2-3-1.6-1.6 1.4c-2-.8-3.6-2.4-4.4-4.4l1.4-1.6-1.6-3z")
    ic.path(d, fill=fg, transform=f"translate({cx:.2f} {cy:.2f}) scale({k:.3f})")


# --- WhatsApp: a green rotary telephone ------------------------------------

@icon("whatsapp", kind="app", names=["com.github.eneshecan.WhatsAppForLinux", "io.github.mimbrero.WhatsAppDesktop",
                                     "wazzapp", "whatsapp", "whatsapp-desktop", "whatsapp-for-linux",
                                     "whatsapp-nativefier", "whatsdesk"], title="WhatsApp")
def whatsapp(ic):
    tile(ic, "#1D6F58", "#0A3A2E")
    shadow(ic, 128, 214, 100, 12)
    green = ic.lin([(0, "#5BE38F"), (0.5, "#25C463"), (1, "#128043")], 0, 0, 0.6, 1)
    # the body: a sloped case on a darker foot
    ic.path("M40 208a8 8 0 0 1-7-10l22-80a14 14 0 0 1 13-10h120a14 14 0 0 1 13 10l22 80a8 8 0 0 1-7 10z",
            fill="#0B5A2E")
    ic.path("M44 200a8 8 0 0 1-7-10l20-72a14 14 0 0 1 13-10h116a14 14 0 0 1 13 10l20 72a8 8 0 0 1-7 10z",
            fill=green)
    ic.path("M58 120a12 12 0 0 1 12-9h116", fill="none", stroke="#fff", stroke_opacity=0.55, stroke_width=2,
            stroke_linecap="round")
    # the dial plate, its finger wheel and holes
    cx, cy = 128, 156
    ic.circle(cx + 1.5, cy + 3, 43, fill="#000", opacity=0.25)
    ic.circle(cx, cy, 43, fill=ic.lin([(0, "#F6FBF7"), (1, "#C9D8CE")], 0, 0, 1, 1))
    for i in range(10):
        x, y = polar(cx, cy, 31, -150 + i * 27)
        ic.circle(x, y, 7.4, fill="#0E4E2B")
        ic.circle(x - 0.6, y - 0.8, 7.4, fill="none", stroke="#000", stroke_opacity=0.3, stroke_width=1)
        ic.text("1234567890"[i], x, y + 3.2, 8.5, font="sans-semibold", anchor="middle", fill="#E9F6EE")
    ic.circle(cx, cy, 43, fill="none", stroke="#0B5A2E", stroke_opacity=0.5, stroke_width=1.5)
    _rim(ic, cx, cy, 42, 1.4, 0.6, 0.2)
    # the finger stop
    fx, fy = polar(cx, cy, 44, 140)
    ic.path(f"M{fx:.1f} {fy:.1f}l8 6", stroke=steel(ic, False), stroke_width=4, stroke_linecap="round")
    # the centre: WhatsApp's mark
    ic.circle(cx, cy, 19, fill=ic.lin([(0, "#3BD877"), (1, "#16994C")]))
    ic.circle(cx, cy, 19, fill="none", stroke="#0B5A2E", stroke_width=1.2)
    _wa_bubble(ic, cx + 0.6, cy - 0.4, 11, "#fff")
    # the handset across the cradle
    hs = "M48 92c0-14 12-22 26-24 36-6 72-6 108 0 14 2 26 10 26 24 0 6-4 10-10 10-8 0-12-6-14-10" \
         "-34-6-78-6-112 0-2 4-6 10-14 10-6 0-10-4-10-10z"
    ic.path(hs, fill="#000", opacity=0.3, transform="translate(3 9)")
    ic.path(hs, fill=green)
    ic.path("M56 84c4-8 12-12 20-13 34-5 70-5 104 0", fill="none", stroke="#fff", stroke_opacity=0.6,
            stroke_width=2.4, stroke_linecap="round")
    for x in (64, 192):
        ic.ellipse(x, 98, 20, 6, fill="#0E6A36", opacity=0.9)
        ic.ellipse(x, 97, 20, 5, fill=green)
    # the cradle's two forks
    for x in (92, 164):
        ic.rect(x - 7, 104, 14, 10, rx=3, fill="#0E6A36")


def _wa_bubble(ic, cx, cy, r, fg):
    t0x, t0y = polar(cx, cy, r, 222)
    t1x, t1y = polar(cx, cy, r, 198)
    ic.path(f"M{t0x:.1f} {t0y:.1f}A{r} {r} 0 1 1 {t1x:.1f} {t1y:.1f}L{cx - r * 1.12:.1f} {cy + r * 1.12:.1f}z",
            fill="none", stroke=fg, stroke_width=r * 0.17, stroke_linejoin="round")
    _wa_handset(ic, cx, cy, r * 0.62, fg)


@small("whatsapp")
def whatsapp16(ic):
    tile(ic, "#1D6F58", "#0A3A2E")
    ic.path("M2.5 13.5l1.6-6a1 1 0 0 1 1-.7h5.8a1 1 0 0 1 1 .7l1.6 6z", fill="#25C463")
    ic.path("M2.5 5.2c0-1.4 1.2-2 2.4-2.2a19 19 0 0 1 6.2 0c1.2.2 2.4.8 2.4 2.2 0 .6-1.2.8-1.6 0"
            "-2.6-.5-5.2-.5-7.8 0-.4.8-1.6.6-1.6 0z", fill="#25C463")
    ic.circle(8, 10.4, 2.6, fill="#F2FAF4")
    ic.circle(8, 10.4, 1.1, fill="#128043")


# --- Microsoft Teams: a conference speakerphone ----------------------------

def _teams_mark(ic, cx, cy, s):
    """Teams' mark, redrawn: a tile with a T, two people behind it; s is
    the tile's side."""
    k = s / 40
    ic.circle(cx + 30 * k, cy - 18 * k, 9 * k, fill="#9EA3F5")
    ic.path(f"M{cx + 14 * k:.1f} {cy - 6 * k:.1f}h26a{4 * k:.1f} {4 * k:.1f} 0 0 1 {4 * k:.1f} {4 * k:.1f}"
            .replace("h26", f"h{26 * k:.1f}") + f"v{16 * k:.1f}a{12 * k:.1f} {12 * k:.1f} 0 0 1-{24 * k:.1f} 0z",
            fill="#7B83EB")
    ic.circle(cx + 6 * k, cy - 26 * k, 12 * k, fill="#7B83EB")
    ic.path(f"M{cx - 10 * k:.1f} {cy - 12 * k:.1f}h{40 * k:.1f}v{26 * k:.1f}a{18 * k:.1f} {18 * k:.1f} 0 0 1"
            f"-{36 * k:.1f} 0z", fill="#5059C9")
    ic.rect(cx - 24 * k, cy - 20 * k, s, s, rx=4 * k, fill=ic.lin([(0, "#6A70DC"), (1, "#3F45B0")], 0, 0, 1, 1))
    ic.text("T", cx - 4 * k, cy + 10.5 * k, 31 * k, font="sans-bold", anchor="middle", fill="#fff")


@icon("teams", kind="app", names=["appimagekit-teams-for-linux", "com.github.IsmaelMartinez.teams_for_linux",
                                  "com.microsoft.Teams", "teams", "teams-for-linux"], title="Microsoft Teams")
def teams(ic):
    tile(ic, "#5B5FC7", "#2A2C7A")
    shadow(ic, 128, 196, 108, 16)
    cx, cy = 128, 128
    # the puck: its side, then its top
    ic.path(f"M{cx - 104} {cy}v22a104 52 0 0 0 208 0v-22z", fill=ic.lin([(0, "#3A3D45"), (0.5, "#24262B"),
                                                                          (1, "#101114")], 0, 0, 1, 0))
    ic.path(f"M{cx - 104} {cy + 10}a104 52 0 0 0 208 0", fill="none", stroke="#fff", stroke_opacity=0.08,
            stroke_width=1.5)
    ic.ellipse(cx, cy, 104, 52, fill=ic.lin([(0, "#4B4F58"), (1, "#202227")], 0, 0, 0.4, 1))
    # the speaker cloth
    mesh = ic.define('<pattern id="{id}" width="4" height="3" patternUnits="userSpaceOnUse">'
                     '<circle cx="1" cy="1" r=".75" fill="#000" opacity=".45"/>'
                     '<circle cx="3" cy="2.5" r=".7" fill="#fff" opacity=".07"/></pattern>', "p")
    ic.ellipse(cx, cy, 96, 47, fill=f"url(#{mesh})")
    ic.path(f"M{cx - 103} {cy - 6}A104 52 0 0 1 {cx + 20} {cy - 51.5}", fill="none", stroke="#fff", stroke_opacity=0.3,
            stroke_width=2, stroke_linecap="round")
    # the light ring, lit in Teams' purple
    ic.ellipse(cx, cy, 62, 31, fill="none", stroke="#7B83EB", stroke_opacity=0.35, stroke_width=9)
    ic.ellipse(cx, cy, 62, 31, fill="none", stroke="#B9BDFF", stroke_width=2.6)
    # the middle disc and the mark on it
    ic.ellipse(cx, cy + 3, 48, 24, fill="#0E0F12")
    ic.ellipse(cx, cy, 48, 24, fill=ic.lin([(0, "#E9EAF2"), (1, "#B8BAC9")], 0, 0, 1, 1))
    with ic.g(transform=f"translate({cx} {cy}) scale(1 0.5) translate({-cx} {-cy})"):
        _teams_mark(ic, cx - 2, cy + 4, 40)
    # the buttons on the rim's front
    for i, (x, sym) in enumerate(((86, "−"), (128, "mic"), (170, "+"))):
        y = cy + 40 - abs(x - cx) * 0.12
        ic.ellipse(x, y + 1.5, 11, 4.5, fill="#000", opacity=0.5)
        ic.ellipse(x, y, 11, 4.5, fill="#31343B" if sym != "mic" else "#C4314B")
        if sym == "mic":
            ic.rect(x - 1.4, y - 2.6, 2.8, 4, rx=1.4, fill="#fff")
        else:
            ic.rect(x - 3.5, y - 0.5, 7, 1, fill="#D7D9E2")
            if sym == "+":
                ic.rect(x - 0.5, y - 2.4, 1, 4.8, fill="#D7D9E2")
    ic.text("TEAMS ROOM", cx, cy + 62, 6.5, font="mono-semibold", anchor="middle", spacing=1.6, fill="#9EA3C8")


@small("teams")
def teams16(ic):
    tile(ic, "#5B5FC7", "#2A2C7A")
    ic.path("M1.5 8v2.4a6.5 3.4 0 0 0 13 0V8z", fill="#1A1B1F")
    ic.ellipse(8, 8, 6.5, 3.4, fill="#3E414A")
    ic.ellipse(8, 8, 5, 2.5, fill="none", stroke="#B9BDFF", stroke_width=0.7)
    ic.circle(11, 4.6, 1.3, fill="#9EA3F5")
    ic.rect(5, 3.2, 5.4, 5.4, rx=0.8, fill="#5059C9")
    ic.path("M6.1 4.6h3.2M7.7 4.6v3.2", stroke="#fff", stroke_width=1.1)


# --- Skype: a headset, Skype's mark on its ear cup -----------------------

def _skype_mark(ic, cx, cy, r):
    blob = ic.lin([(0, "#36C5FA"), (1, "#0089D0")], 0, 0, 1, 1)
    ic.circle(cx - r * 0.42, cy - r * 0.42, r * 0.56, fill=blob)
    ic.circle(cx + r * 0.42, cy + r * 0.42, r * 0.56, fill=blob)
    ic.circle(cx, cy, r * 0.82, fill=blob)
    ic.text("S", cx, cy + r * 0.48, r * 1.36, font="sans-bold", anchor="middle", fill="#fff")


@icon("skype", kind="app", names=["com.skype.Client", "ms-skype", "skype", "skypeforlinux"], title="Skype")
def skype(ic):
    tile(ic, "#1E86C8", "#0B4775")
    shadow(ic, 128, 214, 98, 12)
    # the headband: steel slider, padded band
    ic.path("M54 140V116a74 74 0 0 1 148 0v24", fill="none", stroke="#000", stroke_opacity=0.25, stroke_width=16,
            transform="translate(2 4)")
    ic.path("M54 140V116a74 74 0 0 1 148 0v24", fill="none", stroke=steel(ic), stroke_width=7)
    ic.path("M62 104a68 68 0 0 1 132 0", fill="none", stroke=graphite(ic), stroke_width=18, stroke_linecap="round")
    ic.path("M66 92a64 64 0 0 1 72 -40", fill="none", stroke="#fff", stroke_opacity=0.22, stroke_width=3,
            stroke_linecap="round")
    for x in (80, 96, 112, 128, 144, 160, 176):
        a = math.degrees(math.asin((x - 128) / 66))
        px, py = polar(128, 116, 66, a)
        ic.circle(px, py + 1, 0.9, fill="#fff", opacity=0.25)
    # the mic boom from the right cup to the mouth
    ic.path("M196 186c-8 18-36 24-62 20", fill="none", stroke="#000", stroke_opacity=0.25, stroke_width=7,
            stroke_linecap="round", transform="translate(2 3)")
    ic.path("M196 186c-8 18-36 24-62 20", fill="none", stroke=graphite(ic), stroke_width=5, stroke_linecap="round")
    ic.ellipse(126, 204, 13, 10, fill="#1A1B1E")
    ic.ellipse(124, 202, 9, 6, fill="#fff", opacity=0.1)
    ic.ellipse(126, 204, 13, 10, fill="none", stroke="#33C2F7", stroke_opacity=0.6, stroke_width=1)
    # the cups: cushion, shell, cap
    for x, side in ((56, -1), (200, 1)):
        ic.rect(x - 8 * side - 14, 124, 28, 76, rx=14, fill="#141518")
        ic.rect(x - 30, 120, 60, 84, rx=28, fill=graphite(ic))
        ic.rect(x - 29.25, 120.75, 58.5, 82.5, rx=27.25, fill="none", stroke="#fff", stroke_opacity=0.16,
                stroke_width=1.5)
        ic.rect(x - 22, 128, 44, 68, rx=21, fill=ic.lin([(0, "#2C2E33"), (1, "#16171A")], 0, 0, 1, 1))
        ic.rect(x - 4, 112, 8, 14, rx=3, fill=steel(ic))
    _skype_mark(ic, 56, 162, 21)
    ic.ellipse(48, 144, 6, 9, fill="#fff", opacity=0.18, transform="rotate(25 48 144)")
    ic.text("skype", 200, 166, 11, font="sans-semibold", anchor="middle", fill="#36C5FA", opacity=0.85)
    ic.circle(200, 178, 2, fill="#36C5FA")


@small("skype")
def skype16(ic):
    tile(ic, "#1E86C8", "#0B4775")
    ic.path("M3.6 9V7a4.4 4.4 0 0 1 8.8 0v2", fill="none", stroke="#2A2C30", stroke_width=1.6)
    ic.rect(1.8, 8, 4, 6, rx=2, fill="#2A2C30")
    ic.rect(10.2, 8, 4, 6, rx=2, fill="#2A2C30")
    ic.circle(3.8, 11, 1.6, fill="#33C2F7")


# --- Evolution: a rotary card file of contacts ------------------------------

@icon("evolution", kind="app", names=["evolution", "evolution-mail", "org.gnome.Evolution"], title="Evolution")
def evolution(ic):
    tile(ic, "#6C7A84", "#323C44")
    shadow(ic, 128, 214, 100, 12)
    ax, ay = 128, 168  # the axle
    # the stand
    ic.path("M60 214l14-34h108l14 34z", fill=ic.lin([(0, "#3A3D42"), (1, "#16171A")]))
    ic.line(74, 180.5, 182, 180.5, stroke="#fff", stroke_opacity=0.2)
    # the cards behind, fanned back
    card = paper(ic, "cream")
    for a, tab in ((-26, 74), (18, 150), (-18, 96), (11, 120), (-9, 70), (5, 104)):
        with ic.g(transform=f"rotate({a} {ax} {ay})"):
            ic.rect(tab, 56, 30, 10, rx=2, fill="#CF372D" if tab in (96, 120) else "#B9C2C7")
            ic.rect(62, 64, 132, 96, rx=4, fill=ic.lin([(0, "#EDE6D8"), (1, "#C9C0AE")]))
            ic.rect(62, 64, 132, 96, rx=4, fill="none", stroke="#000", stroke_opacity=0.14)
    # the card in front
    ic.rect(62, 66, 132, 96, rx=4, fill="#000", opacity=0.22, transform="translate(2 3)")
    ic.rect(62, 64, 132, 96, rx=4, fill=card)
    ic.path("M140 64v-8a3 3 0 0 1 3-3h30a3 3 0 0 1 3 3v8z", fill=ic.lin([(0, "#EC5145"), (1, "#B32A20")]))
    ic.text("D", 158, 63, 9, font="sans-bold", anchor="middle", fill="#fff")
    for y in (90, 102, 114, 126, 138, 150):
        ic.line(70, y + 3, 186, y + 3, stroke="#7FA6C9", stroke_opacity=0.35)
    ic.line(70, 78, 186, 78, stroke="#CF372D", stroke_opacity=0.6)
    ic.text("Dana Okafor", 72, 75, 11, font="sans-semibold", fill="#2C3338")
    ic.text("dana@okafor.studio", 72, 91, 7.5, font="mono", fill="#3D4A54")
    ic.text("+44 20 7946 0018", 72, 103, 7.5, font="mono", fill="#3D4A54")
    ic.text("lunch Tue 12:30", 74, 128, 13, font="hand", fill="#3B4A63")
    # the holes the rails go through
    for x in (100, 156):
        ic.ellipse(x, 158, 6, 3, fill="#2A2C30")
    # the knobs on the axle
    for x, s in ((44, 1), (212, -1)):
        ic.rect(min(x, x + 16 * s), ay - 3, 16, 6, fill=steel(ic, False))
        ic.ellipse(x, ay, 13, 40, fill="#16171A", transform="translate(2 3)", opacity=0.6)
        ic.ellipse(x, ay, 13, 40, fill=ic.lin([(0, "#F2F4F6"), (0.4, "#B5BBC2"), (1, "#5D636B")], 0, 0, 1, 1))
        ic.ellipse(x, ay, 9, 32, fill=ic.lin([(0, "#8A9098"), (1, "#D8DCE0")], 0, 0, 1, 1))
        for k in range(-3, 4):
            ic.line(x - 8, ay + k * 8, x + 8, ay + k * 8, stroke="#000", stroke_opacity=0.12)
    ic.text("EVOLUTION", 128, 203, 7.5, font="mono-semibold", anchor="middle", spacing=2, fill="#C3CACD")


@small("evolution")
def evolution16(ic):
    tile(ic, "#6C7A84", "#323C44")
    ic.path("M4 14l1-2.5h6l1 2.5z", fill="#1E2024")
    ic.rect(3.5, 3.6, 9, 7, rx=0.6, fill="#F6F1E6")
    ic.rect(9, 2.4, 2.6, 1.4, rx=0.3, fill="#CF372D")
    ic.rect(4.5, 5, 5, 0.9, fill="#2C3338")
    ic.rect(4.5, 7, 6, 0.6, fill="#7FA6C9")
    ic.ellipse(2.4, 11, 1.1, 3, fill="#B5BBC2")
    ic.ellipse(13.6, 11, 1.1, 3, fill="#B5BBC2")


# --- Geary: a yellow letterbox on a post, its flag up -----------------------

@icon("geary", kind="app", names=["claws-mail", "deepin-mail", "email", "geary", "instantbird", "internet-mail",
                                  "io.elementary.mail", "kmail", "kube-mail", "mail-client", "mailnag",
                                  "org.claws_mail.Claws-Mail", "org.gnome.Geary", "org.xfce.mailreader",
                                  "preferences-mail", "sylpheed", "unity-mail", "xfce-mail", "xfce-newmail",
                                  "xfmail", "yast-mail"], title="Geary")
def geary(ic):
    tile(ic, "#7A4E6A", "#3C2032")
    shadow(ic, 134, 216, 76, 10)
    # the post
    ic.rect(122, 150, 26, 66, fill=wood(ic, "#A8774A", "#5E3A1C"))
    ic.line(123, 150, 123, 216, stroke="#fff", stroke_opacity=0.2, stroke_width=2)
    ic.rect(100, 150, 70, 10, rx=2, fill=wood(ic, "#8E6238", "#4E2F14"))
    # the box's long side, half-round on top
    body = "M58 64h130a36 36 0 0 1 36 36v54H58z"
    ic.path(body, fill="#000", opacity=0.3, transform="translate(3 4)")
    ic.path(body, fill=ic.lin([(0, "#FFE58A"), (0.45, "#F7BF3A"), (1, "#C98A12")], 0, 0, 0.3, 1))
    ic.path("M76 70h112a30 30 0 0 1 28 22", fill="none", stroke="#fff", stroke_opacity=0.6, stroke_width=2.4,
            stroke_linecap="round")
    for x in (110, 150, 190):
        ic.path(f"M{x} 64.6v89.4", stroke="#9A6A0E", stroke_opacity=0.35, stroke_width=1.5)
        ic.path(f"M{x + 1.5} 64.6v89.4", stroke="#fff", stroke_opacity=0.25, stroke_width=1)
    # a letter, pushed in past the door
    with ic.g(transform="rotate(-18 76 70)"):
        ic.rect(60, 40, 52, 34, rx=2, fill=paper(ic, "white"))
        ic.path("M60 41l26 14 26-14", fill="none", stroke="#C9BFA9", stroke_width=1.2)
        ic.rect(100, 44, 8, 9, fill="#E0483A")
    # the door: the round-topped end toward us
    door = "M34 156V102c0-22 11-40 24-40s24 18 24 40v54z"
    ic.path(door, fill="#000", opacity=0.3, transform="translate(3 2)")
    ic.path(door, fill=ic.lin([(0, "#FCD567"), (0.6, "#E9A71E"), (1, "#B07810")], 0, 0, 1, 1))
    ic.path("M37 150V102c0-20 10-36 21-36s21 16 21 36v48z", fill="none", stroke="#9A6A0E", stroke_opacity=0.4,
            stroke_width=1.5)
    ic.path("M36 120v-18c0-18 9-34 20-37", fill="none", stroke="#fff", stroke_opacity=0.55, stroke_width=2,
            stroke_linecap="round")
    ic.rect(50, 104, 16, 7, rx=3, fill="#000", opacity=0.3, transform="translate(1 2)")
    ic.rect(50, 104, 16, 7, rx=3, fill=steel(ic))
    # the name, painted on the side
    ic.text("GEARY", 152, 122, 20, font="sans-bold", anchor="middle", spacing=2.6, fill="#70445E")
    ic.text("No. 26", 152, 140, 9, font="mono-semibold", anchor="middle", spacing=1, fill="#70445E", opacity=0.7)
    # the flag, raised: a red arm on a pivot
    ic.rect(204, 46, 10, 74, rx=2, fill="#000", opacity=0.25, transform="translate(3 3)")
    ic.rect(204, 46, 10, 74, rx=2, fill=ic.lin([(0, "#F25B4B"), (1, "#B42A1F")], 0, 0, 1, 0))
    ic.rect(204, 34, 30, 22, rx=2, fill=ic.lin([(0, "#F25B4B"), (1, "#B42A1F")]))
    ic.line(205, 35, 233, 35, stroke="#fff", stroke_opacity=0.4, stroke_width=1.5)
    _screw(ic, 209, 112, 3.2)


@small("geary")
def geary16(ic):
    tile(ic, "#7A4E6A", "#3C2032")
    ic.rect(7, 10, 2, 5, fill="#8E6238")
    ic.path("M2 10V6.5a2.5 2.5 0 0 1 2.5-2.5h7a2.5 2.5 0 0 1 2.5 2.5V10z", fill="#F7BF3A")
    ic.path("M2 10V6.5a2.5 2.5 0 0 1 1.4-2.2V10z", fill="#C98A12")
    ic.rect(12, 1.5, 1, 5, fill="#E0483A")
    ic.rect(12, 1.5, 2.6, 1.8, fill="#E0483A")


# --- Fractal: a walkie-talkie, a Sierpinski triangle on it ----------------

def _sierpinski(ic, x, y, s, depth, **kw):
    if depth == 0:
        ic.poly([(x, y + s), (x + s / 2, y), (x + s, y + s)], **kw)
        return
    h = s / 2
    _sierpinski(ic, x + h / 2, y, h, depth - 1, **kw)
    _sierpinski(ic, x, y + h, h, depth - 1, **kw)
    _sierpinski(ic, x + h, y + h, h, depth - 1, **kw)


@icon("fractal", kind="app", names=["fractal", "org.gnome.Fractal"], title="Fractal")
def fractal(ic):
    tile(ic, "#3F6FB2", "#1A3866")
    shadow(ic, 128, 218, 66, 10)
    # the antenna and the knobs on top
    ic.rect(88, 18, 13, 52, rx=6.5, fill="#16171A")
    ic.rect(89.5, 20, 3, 44, rx=1.5, fill="#fff", opacity=0.18)
    ic.rect(150, 46, 18, 20, rx=3, fill=steel(ic))
    for x in range(152, 168, 3):
        ic.line(x, 48, x, 64, stroke="#000", stroke_opacity=0.25)
    ic.rect(124, 54, 16, 12, rx=3, fill="#E0483A")
    # the body
    ic.rect(72, 66, 112, 154, rx=20, fill="#000", opacity=0.3, transform="translate(3 4)")
    ic.rect(72, 66, 112, 152, rx=20, fill=ic.lin([(0, "#5F95DE"), (0.5, "#3B6CB5"), (1, "#22477E")], 0, 0, 1, 1))
    ic.rect(72.75, 66.75, 110.5, 150.5, rx=19.25, fill="none", stroke="#fff", stroke_opacity=0.28,
            stroke_width=1.5)
    # the push-to-talk key on the left side
    ic.rect(64, 104, 10, 40, rx=4, fill=graphite(ic))
    # the screen
    ic.rect(84, 78, 88, 40, rx=6, fill="#12233C")
    ic.rect(88, 82, 80, 32, rx=3, fill=ic.lin([(0, "#BFE3D6"), (1, "#8FC4B2")]))
    ic.text("CH 03", 92, 96, 11, font="mono-semibold", fill="#1C3A33")
    ic.text("#gnome", 92, 109, 8, font="mono-semibold", fill="#1C3A33", opacity=0.75)
    for k in range(4):
        ic.rect(152 + k * 3.4, 94 - k * 3, 2.4, 3 + k * 3, fill="#1C3A33")
    ic.path("M88 85a3 3 0 0 1 3-3h50l-16 32H88z", fill="#fff", opacity=0.18)
    # the speaker grille
    for y in range(128, 166, 7):
        ic.rect(86, y, 84, 3.6, rx=1.8, fill="#14294A")
        ic.rect(86, y + 3, 84, 1, rx=0.5, fill="#fff", opacity=0.15)
    # the badge: a Sierpinski triangle
    ic.rect(94, 170, 68, 42, rx=6, fill="#14294A", opacity=0.6, transform="translate(1 1.5)")
    ic.rect(94, 170, 68, 42, rx=6, fill=ic.lin([(0, "#F4F7FB"), (1, "#D5DEEA")]))
    _sierpinski(ic, 110, 174, 36, 3, fill=ic.lin([(0, "#4E8AD8"), (1, "#2A4F8E")]))
    # the rubber grip down the sides, the LED, the belt clip's edge
    for x in (74, 176):
        for y in range(126, 166, 6):
            ic.rect(x, y, 6, 3, rx=1.5, fill="#14294A", opacity=0.5)
    ic.circle(166, 71, 2.4, fill="#7CF7A6")
    ic.circle(166, 71, 5, fill="#7CF7A6", opacity=0.25)


@small("fractal")
def fractal16(ic):
    tile(ic, "#3F6FB2", "#1A3866")
    ic.rect(5, 1, 1.4, 4, rx=0.7, fill="#16171A")
    ic.rect(4, 4, 8, 11, rx=1.6, fill="#5F95DE")
    ic.rect(5, 5, 6, 3, rx=0.5, fill="#BFE3D6")
    ic.poly([(6, 13), (8, 9.4), (10, 13)], fill="#E9EDF3")


# --- Dino: a tin wind-up dinosaur -----------------------------------------

@icon("dino", kind="app", names=["dino", "im.dino.Dino"], title="Dino")
def dino(ic):
    tile(ic, "#2D5560", "#13282F")
    shadow(ic, 124, 210, 92, 11)
    tin = ic.lin([(0, "#C4E8A0"), (0.5, "#8CCB5E"), (1, "#4E8C2C")], 0, 0, 0.4, 1)
    leg = ic.lin([(0, "#9AD46C"), (1, "#3E7A22")], 0, 0, 1, 1)
    dark = "#3E7A22"
    with ic.g(transform="translate(-6 10) scale(0.92) translate(11 -8)"):
        # the far legs
        for x in (92, 164):
            ic.path(f"M{x - 4} 160c-2 14-4 30-4 42h18c2-12 4-28 4-40z", fill="#35661C")
        # body, neck, head, tail in one outline
        d = ("M30 176c18 0 36-6 50-22 8-20 30-34 58-34 22 0 38 8 46-6 6-12 2-30 6-48 4-16 18-24 32-20 "
             "12 3 18 14 14 24-4 8-14 10-20 10-6 0-8 6-8 14 0 22-2 44-12 62-10 18-30 26-54 26h-60"
             "c-18 0-36 6-52 6-6 0-6-12 0-12z")
        ic.path(d, fill="#000", opacity=0.25, transform="translate(3 4)")
        ic.path(d, fill=tin)
        # the back's plates, along the spine
        for i, (x, y) in enumerate(((96, 128), (114, 120), (134, 118), (154, 120), (172, 116))):
            ic.poly([(x - 9, y + 4), (x, y - 12 + (i % 2) * 2), (x + 9, y + 4)], fill="#E9A23B")
            ic.poly([(x - 9, y + 4), (x, y - 12 + (i % 2) * 2), (x, y + 4)], fill="#F6C46A")
        ic.path(d, fill="none", stroke="#fff", stroke_opacity=0.25, stroke_width=1.2)
        ic.path("M191 98c1-14 0-26 2-34 3-10 10-14 18-12", fill="none", stroke="#fff", stroke_opacity=0.5,
                stroke_width=2, stroke_linecap="round")
        # spots printed on the tin
        for x, y, r in ((150, 140, 5), (168, 150, 3.5), (186, 132, 4), (82, 166, 3.5), (196, 110, 3)):
            ic.circle(x, y, r, fill="#5E9E36", opacity=0.7)
        # the near legs: round thighs, toes
        for x in (74, 146):
            ic.path(f"M{x - 6} 160c0-10 30-10 30 0 0 16-2 30-4 42h-22c-2-12-4-26-4-42z", fill=leg)
            ic.path(f"M{x - 10} 210a4 4 0 0 1 0-8h30a4 4 0 0 1 0 8z", fill="#2E5A18")
            for t in (x - 6, x + 3, x + 12):
                ic.circle(t, 205, 2.6, fill="#F0E6CC")
        # tin seam with its rivets
        ic.path("M84 150c14 16 52 20 98 4", fill="none", stroke=dark, stroke_width=1.5, stroke_dasharray="1 5",
                stroke_linecap="round")
        # the face
        ic.circle(208, 62, 5.5, fill="#fff")
        ic.circle(209.5, 62, 2.8, fill="#1A1B1E")
        ic.circle(210.5, 61, 0.9, fill="#fff")
        ic.path("M216 76c-6 3-12 3-17 0", fill="none", stroke=dark, stroke_width=1.8, stroke_linecap="round")
        ic.circle(224, 66, 1.4, fill=dark)
        # Dino's bubble, a decal on its side
        ic.path("M100 138h48a10 10 0 0 1 10 10v12a10 10 0 0 1-10 10h-30l-10 8 2-8h-10a10 10 0 0 1-10-10v-12"
                "a10 10 0 0 1 10-10z", fill="#F0F0F0")
        ic.path("M100 138h48a10 10 0 0 1 10 10", fill="none", stroke="#fff", stroke_width=1.2)
        ic.text("hi!", 120, 161, 17, font="hand", anchor="middle", fill="#048C7F")
        ic.circle(144, 154, 3.4, fill="#41555F")
        # the wind-up key
        ic.rect(56, 148, 22, 6, rx=2, fill=brass(ic))
        ic.path("M50 132c-9 0-11 9-6 14l6 6 6-6c5-5 3-14-6-14zM50 172c-9 0-11-9-6-14l6-6 6 6c5 5 3 14-6 14z",
                fill=brass(ic))
        ic.path("M46 136c-3 2-3 6 0 8", fill="none", stroke="#fff", stroke_opacity=0.6, stroke_width=1.2)
        ic.circle(50, 152, 4, fill=brass(ic, 1, 1, 0, 0))


@small("dino")
def dino16(ic):
    tile(ic, "#2D5560", "#13282F")
    ic.path("M1.5 11.5c2 0 3-1 4-2.4 1-1.4 2.4-2 4-2 1.4 0 2-1 2-3 .2-1.6 1.6-2.4 2.8-1.6.8.6.6 1.8-.6 2"
            "-.6 0-.8.4-.8 1.2 0 3-1 6.3-4 6.3H5c-1.2 0-2.4.4-3.5.4z", fill="#8CCB5E")
    ic.rect(5, 12, 1.6, 2.6, fill="#4E8C2C")
    ic.rect(9.4, 12, 1.6, 2.6, fill="#4E8C2C")
    ic.circle(13.6, 3.2, 0.5, fill="#1A1B1E")
    ic.poly([(6.5, 8), (7.5, 6.4), (8.5, 8)], fill="#E9A23B")


# --- Pidgin: a carrier pigeon, a note on its leg --------------------------

@icon("pidgin", kind="app", names=["im.pidgin.Pidgin", "pidgin"], title="Pidgin")
def pidgin(ic):
    tile(ic, "#7A5A9E", "#3A2552")
    shadow(ic, 128, 208, 92, 11)
    # the perch: a round wooden rail, pegged into the tile's sides
    ic.rect(24, 184, 208, 16, rx=8, fill="#000", opacity=0.3, transform="translate(2 4)")
    ic.rect(24, 184, 208, 16, rx=8, fill=wood(ic))
    ic.line(32, 187.5, 224, 187.5, stroke="#fff", stroke_opacity=0.3, stroke_width=2, stroke_linecap="round")
    plum = ic.lin([(0, "#CDB4EA"), (0.5, "#9A78C2"), (1, "#5D3E80")], 0, 0, 0.5, 1)
    # the tail, a fan down to the left, dark at its tip
    tail = "M74 134L22 168c-6 4-4 14 2 16l72-8z"
    ic.path(tail, fill="#5D3E80")
    ic.path("M34 160L22 168c-6 4-4 14 2 16l16-2z", fill="#2E1C42")
    for k in (0, 1, 2):
        ic.path(f"M80 {142 + k * 10}L{28 + k * 2} {172 + k * 4}", stroke="#B79AD8", stroke_opacity=0.35,
                stroke_width=1.2)
    # the body
    body = "M64 148c6-40 40-60 80-60 18 0 30 4 40 12 14 12 16 34 8 52-10 20-32 30-60 30-30 0-56-10-68-34z"
    ic.path(body, fill="#000", opacity=0.25, transform="translate(2 4)")
    ic.path(body, fill=plum)
    # the neck's sheen, green and violet
    ic.path("M146 92c16 0 32 10 36 26-10 8-26 6-38-2-4-10-4-18 2-24z",
            fill=ic.lin([(0, "#7BE0A8", 0.9), (0.55, "#A27CF0", 0.85), (1, "#A27CF0", 0)], 0, 0, 1, 1))
    # the wing, its two dark bars, its feathers
    wing = "M74 142c10-28 40-40 72-34 18 4 26 18 20 34-8 20-38 26-62 22-14-2-26-10-30-22z"
    ic.path(wing, fill=ic.lin([(0, "#B89CDA"), (1, "#674690")], 0, 0, 0.6, 1))
    ic.path("M108 122c14-6 28-4 40 4-12-2-26-2-40 2z", fill="#3A2552", opacity=0.85)
    ic.path("M100 136c18-6 36-4 52 4-16-2-34-2-52 2z", fill="#3A2552", opacity=0.85)
    for i in range(3):
        y = 146 + i * 6
        ic.path(f"M{86 + i * 6} {y}q34 -4 70 -8", fill="none", stroke="#3A2552", stroke_opacity=0.3,
                stroke_width=1.2)
    ic.path("M80 128c14-16 40-22 64-16", fill="none", stroke="#fff", stroke_opacity=0.45, stroke_width=2,
            stroke_linecap="round")
    # the head
    ic.circle(168, 78, 24, fill=ic.lin([(0, "#C2A6E2"), (1, "#6E4E94")], 0, 0, 1, 1))
    ic.path("M150 66a22 22 0 0 1 26-10", fill="none", stroke="#fff", stroke_opacity=0.5, stroke_width=2,
            stroke_linecap="round")
    ic.path("M188 74l22 7-22 5z", fill="#F38C25")
    ic.path("M188 74l22 7h-22z", fill="#FACDA3")
    ic.ellipse(188, 74.5, 4, 3, fill="#F4EEF8")
    ic.circle(176, 74, 5.6, fill="#F38C25")
    ic.circle(176, 74, 3.2, fill="#1A1B1E")
    ic.circle(175, 73, 1.1, fill="#fff")
    # the feet round the perch
    for x in (118, 146):
        ic.path(f"M{x} 176v10", stroke="#E07A2A", stroke_width=5, stroke_linecap="round")
        ic.path(f"M{x - 7} 190q7-6 14 0", fill="none", stroke="#E07A2A", stroke_width=3.4, stroke_linecap="round")
    # the message, rolled in a brass tube on its leg
    ic.rect(140, 170, 26, 11, rx=5.5, fill="#000", opacity=0.3, transform="translate(1 2)")
    ic.rect(140, 170, 26, 11, rx=5.5, fill=brass(ic, 0, 0, 0, 1))
    ic.rect(164, 171.5, 12, 8, rx=1, fill=paper(ic, "cream"))
    ic.line(167, 174, 174, 174, stroke="#7A5A9E", stroke_width=0.8)
    ic.line(143, 172, 162, 172, stroke="#fff", stroke_opacity=0.6)


@small("pidgin")
def pidgin16(ic):
    tile(ic, "#7A5A9E", "#3A2552")
    ic.rect(1.5, 12.6, 13, 1.6, rx=0.8, fill="#9A6A3E")
    ic.path("M3.5 10c.4-3 2.6-4.4 5.4-4.4 2.4 0 3.4 1.6 3 3.4C11.4 11 9.6 12 7.6 12 5.6 12 4.2 11.4 3.5 10z",
            fill="#9472BC")
    ic.path("M3.5 10L1.2 11.6l3.6-.4z", fill="#5D3E80")
    ic.circle(11, 5, 2, fill="#9472BC")
    ic.path("M12.8 4.4l1.8.8-1.8.6z", fill="#F38C25")
    ic.circle(11.5, 4.8, 0.5, fill="#1A1B1E")


# --- HexChat: a telegraph key on a walnut base ------------------------------

@icon("hexchat", kind="app", names=["hexchat", "io.github.Hexchat"], title="HexChat")
def hexchat(ic):
    tile(ic, "#3E4858", "#1A1F28")
    shadow(ic, 128, 214, 106, 12)
    # the wires out of the back
    ic.path("M196 136c24-2 22-34 44-40", fill="none", stroke="#C8372D", stroke_width=3.4)
    ic.path("M204 140c22 0 30-22 36-24", fill="none", stroke="#1A1B1E", stroke_width=3.4)
    # the base: a walnut block, its top and front
    ic.path("M22 174l22-50h168l22 50z", fill=wood(ic, "#A86E40", "#5A3416"))
    ic.path("M22 174h212v24a8 8 0 0 1-8 8H30a8 8 0 0 1-8-8z", fill=ic.lin([(0, "#6E4320"), (1, "#3A200A")]))
    ic.line(44, 124.8, 212, 124.8, stroke="#fff", stroke_opacity=0.35, stroke_width=1.5)
    ic.line(22, 174.6, 234, 174.6, stroke="#E0A86E", stroke_opacity=0.6)
    for y, a in ((134, 0.25), (146, 0.2), (160, 0.25)):
        ic.path(f"M{44 - (y - 124) * 0.44:.1f} {y}q60 -4 120 1t{48 + (y - 124) * 0.88:.1f} -1", fill="none",
                stroke="#3E220C", stroke_opacity=a, stroke_width=1)
    # the brass front plate
    ic.rect(94, 180, 68, 18, rx=3, fill=brass(ic))
    ic.line(96, 180.8, 160, 180.8, stroke="#fff", stroke_opacity=0.6)
    ic.text("HEXCHAT", 128, 193, 9, font="mono-semibold", anchor="middle", spacing=1.2, fill="#4A3410")
    for x in (99, 157):
        _screw(ic, x, 189, 1.6)
    # the trunnion pillars, the spring post, the contact
    ic.ellipse(156, 156, 16, 5, fill="#2A1606", opacity=0.5)
    ic.rect(144, 128, 8, 28, rx=2, fill=brass(ic))
    ic.rect(160, 128, 8, 28, rx=2, fill=brass(ic))
    ic.ellipse(196, 150, 10, 3.5, fill="#2A1606", opacity=0.5)
    ic.rect(190, 124, 12, 26, rx=2, fill=brass(ic))
    ic.path("M192 124v-6h8v6", fill=steel(ic, False))
    for y in range(126, 140, 3):
        ic.line(186, y, 206, y - 2, stroke="#C3C8CE", stroke_width=1.2)
    ic.ellipse(76, 160, 12, 4, fill="#2A1606", opacity=0.5)
    ic.rect(68, 146, 16, 14, rx=2, fill=brass(ic))
    ic.ellipse(76, 146, 8, 2.5, fill="#F6DDA0")
    # the lever
    lever = "M62 132L204 124v9L62 142z"
    ic.path(lever, fill="#000", opacity=0.3, transform="translate(3 12)")
    ic.path(lever, fill=brass(ic, 0, 0, 0, 1))
    ic.line(64, 132.4, 202, 124.4, stroke="#fff", stroke_opacity=0.7, stroke_width=1.2)
    ic.circle(156, 131, 5, fill=steel(ic, False))
    ic.circle(156, 131, 1.6, fill="#3A3E44")
    # the knob: a hexagonal cap in HexChat's amber on a short stem
    ic.rect(68, 110, 10, 26, rx=2, fill=brass(ic))
    hexd = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in (polar(73, 92, 30, a) for a in range(30, 390, 60))) + "Z"
    ic.path(hexd, fill="#000", opacity=0.3, transform="translate(3 5)")
    ic.path(hexd, fill=ic.lin([(0, "#FFD36A"), (0.5, "#EDB01F"), (1, "#A8740C")], 0, 0, 1, 1))
    hexi = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in (polar(73, 92, 22, a) for a in range(30, 390, 60))) + "Z"
    ic.path(hexi, fill=ic.lin([(0, "#D99A12"), (1, "#FFD36A")], 0, 0, 1, 1))
    ic.text("#", 73, 102, 28, font="sans-bold", anchor="middle", fill="#5A3A06", opacity=0.85)
    p = [polar(73, 92, 30, a) for a in (270, 330, 30)]
    ic.path("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in p), fill="none", stroke="#fff", stroke_opacity=0.65,
            stroke_width=1.6, stroke_linejoin="round")


@small("hexchat")
def hexchat16(ic):
    tile(ic, "#3E4858", "#1A1F28")
    ic.path("M1.5 11l1.2-2.4h10.6L14.5 11v2.4H1.5z", fill="#7A4A22")
    ic.path("M4 8.2L13 7.6v.8L4 9.2z", fill="#C99645")
    hexd = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in (polar(4.6, 5.4, 3.2, a) for a in range(30, 390, 60))) + "Z"
    ic.path(hexd, fill="#EDB01F")
    ic.path("M3.6 4v3M5.4 4v3M3 5h3M3 6.4h3", stroke="#5A3A06", stroke_width=0.6)


# --- Ferdium: a telephone switchboard, its cords patched -----------------

@icon("ferdium", kind="app", names=["ferdium", "org.ferdium.Ferdium"], title="Ferdium")
def ferdium(ic):
    tile(ic, "#6A5CD6", "#2E2478")
    shadow(ic, 128, 214, 102, 12)
    # the cabinet
    ic.rect(32, 36, 192, 174, rx=10, fill="#000", opacity=0.3, transform="translate(3 4)")
    ic.rect(32, 36, 192, 174, rx=10, fill=wood(ic, "#B07A48", "#5E3518"))
    ic.rect(32.75, 36.75, 190.5, 172.5, rx=9.25, fill="none", stroke="#fff", stroke_opacity=0.18, stroke_width=1.5)
    # the brass name plate
    ic.rect(88, 44, 80, 16, rx=3, fill=brass(ic))
    ic.text("FERDIUM", 128, 56, 9, font="mono-semibold", anchor="middle", spacing=2, fill="#4A3410")
    # the jack panel: dark, rows of lamps and jacks
    ic.rect(44, 66, 168, 90, rx=4, fill=ic.lin([(0, "#2B2440"), (1, "#151122")]))
    ic.rect(44, 66, 168, 90, rx=4, fill="none", stroke="#000", stroke_opacity=0.4)
    cols = [62 + i * 26.4 for i in range(6)]
    lit = {(1, 0): "#8471F2", (3, 1): "#F2C45C", (4, 0): "#8471F2", (0, 2): "#7CF7A6"}
    for r, y in enumerate((80, 110, 140)):
        for c, x in enumerate(cols):
            col = lit.get((c, r))
            ic.circle(x, y - 8, 3.2, fill=col or "#3E3657")
            if col:
                ic.circle(x, y - 8, 6, fill=col, opacity=0.25)
                ic.circle(x - 1, y - 9, 1, fill="#fff", opacity=0.8)
            ic.circle(x, y + 4, 6, fill=brass(ic))
            ic.circle(x, y + 4, 3, fill="#0C0A12")
    # the shelf with plugs at rest, then the patch cords up into the panel
    ic.rect(32, 160, 192, 22, fill=wood(ic, "#8E5E32", "#4E2C12"))
    ic.line(32, 160.6, 224, 160.6, stroke="#fff", stroke_opacity=0.25, stroke_width=1.2)
    cords = (("#8471F2", 66, 88, 114), ("#E0483A", 98, 140, 84), ("#F2C45C", 130, 167, 144),
             ("#3FB98A", 162, 114, 84), ("#4F9BE8", 194, 194, 114))
    for col, sx, jx, jy in cords:
        ic.path(f"M{sx} 168C{sx} 196 {jx} 196 {jx} {jy + 10}", fill="none", stroke="#000", stroke_opacity=0.3,
                stroke_width=5, transform="translate(1.5 2)")
        ic.path(f"M{sx} 168C{sx} 196 {jx} 196 {jx} {jy + 10}", fill="none", stroke=col, stroke_width=4)
        ic.rect(jx - 3.5, jy + 2, 7, 10, rx=1.5, fill=steel(ic))
        ic.rect(sx - 4, 164, 8, 12, rx=2, fill="#1A1B1E")
        ic.rect(sx - 3, 165, 2, 10, rx=1, fill="#fff", opacity=0.2)


@small("ferdium")
def ferdium16(ic):
    tile(ic, "#6A5CD6", "#2E2478")
    ic.rect(2, 2, 12, 12, rx=1.2, fill="#9A6A3E")
    ic.rect(3, 3.5, 10, 6, rx=0.5, fill="#1E1830")
    for x in (4.6, 8, 11.4):
        for y in (5, 8):
            ic.circle(x, y, 0.9, fill="#C99645")
    ic.path("M4.6 8C4.6 12 8 12 8 5", fill="none", stroke="#8471F2", stroke_width=0.9)
    ic.path("M11.4 8C11.4 12 6 13 4.6 5", fill="none", stroke="#E0483A", stroke_width=0.9)


# --- Mattermost: a ship's bell on its bracket, the mark on an enamel plate ----

@icon("mattermost-desktop", kind="app", names=["com.mattermost.Desktop", "mattermost", "mattermost-desktop",
                                                "mattermost-desktop-bin"], title="Mattermost")
def mattermost(ic):
    tile(ic, "#2A4378", "#101E3C")
    cx = 128
    shadow(ic, 128, 218, 80, 10)
    dark = "#5E4012"
    # the bracket: a plate on the wall, an arm out over the bell, a scroll under it
    ic.rect(30, 22, 16, 58, rx=4, fill="#000", opacity=0.3, transform="translate(2 3)")
    ic.rect(30, 22, 16, 58, rx=4, fill=brass(ic))
    for y in (32, 70):
        ic.circle(38, y, 3, fill=ic.rad([(0, "#F6DDA0"), (1, "#7E5A20")], cx=0.35, cy=0.3, r=0.8))
        ic.line(36, y - 2, 40, y + 2, stroke=dark, stroke_width=1)
    ic.path("M46 70C60 70 70 52 96 40", fill="none", stroke="#000", stroke_opacity=0.3, stroke_width=6,
            stroke_linecap="round", transform="translate(2 3)")
    ic.path("M46 70C60 70 70 52 96 40", fill="none", stroke=brass(ic), stroke_width=6, stroke_linecap="round")
    ic.circle(58, 62, 5, fill="none", stroke=brass(ic), stroke_width=3)
    # the shackle round the arm
    ic.circle(cx, 38, 9, fill="none", stroke=brass(ic, 1, 1, 0, 0), stroke_width=4.5)
    ic.rect(44, 30, 116, 9, rx=4.5, fill="#000", opacity=0.3, transform="translate(2 3)")
    ic.rect(44, 30, 116, 9, rx=4.5, fill=ic.lin([(0, "#F6DDA0"), (0.5, "#C99645"), (1, "#7E5A20")]))
    ic.circle(160, 34.5, 6, fill=brass(ic))
    ic.path(f"M{cx - 9} 38a9 9 0 0 0 18 0", fill="none", stroke=brass(ic), stroke_width=4.5)
    # the crown
    ic.rect(cx - 10, 44, 20, 14, rx=3, fill=ic.lin([(0, "#8A6425"), (0.3, "#F6DDA0"), (1, "#6A4A18")], 0, 0, 1, 0))
    # the clapper, under the mouth
    ic.line(cx, 180, cx, 200, stroke="#6A4A18", stroke_width=4)
    ic.circle(cx, 204, 8, fill=ic.rad([(0, "#F6DDA0"), (0.5, "#C99645"), (1, "#5E4012")], cx=0.35, cy=0.3, r=0.8))
    # the bell, polished: a light down its left, dark to the right
    bell = ("M98 72C98 60 110 55 128 55S158 60 158 72L164 136C166 160 178 170 198 176C206 179 206 192 196 192"
            "H60C50 192 50 179 58 176C78 170 90 160 92 136Z")
    ic.path(bell, fill="#000", opacity=0.3, transform="translate(3 4)")
    ic.path(bell, fill=ic.lin([(0, "#7E5A20"), (0.12, "#D9AF62"), (0.27, "#FBEBC0"), (0.5, "#C99645"),
                               (0.8, "#8A6425"), (1, "#5E4012")], 52, 0, 204, 0, units="userSpaceOnUse"))
    ic.path("M110 66C104 70 104 76 104 84L100 140C98 160 86 170 70 177", fill="none", stroke="#fff",
            stroke_opacity=0.45, stroke_width=3, stroke_linecap="round")
    # the raised rings: at the shoulder, the waist and the lip
    for y, xl, xr, bow in ((76, 97.6, 158.4, 3), (150, 88, 168, 5), (178, 56, 200, 7)):
        ic.path(f"M{xl} {y + 1.6}Q{cx} {y + bow + 1.6} {xr} {y + 1.6}", fill="none", stroke=dark,
                stroke_opacity=0.7, stroke_width=1.6)
        ic.path(f"M{xl} {y}Q{cx} {y + bow} {xr} {y}", fill="none", stroke="#FFF2CC", stroke_opacity=0.7,
                stroke_width=1.2)
    ic.path("M60 192Q128 197 196 192", fill="none", stroke=dark, stroke_width=2)
    # the name, engraved round the waist
    ic.text("MATTERMOST", cx + 0.6, 168.6, 9, font="sans-semibold", anchor="middle", spacing=1.6, fill="#FFF2CC",
            opacity=0.6)
    ic.text("MATTERMOST", cx, 168, 9, font="sans-semibold", anchor="middle", spacing=1.6, fill="#4A3210")
    # the enamel plate, pinned on: Mattermost's ring, cut through on a slant
    ic.rect(103, 84, 52, 54, rx=7, fill="#000", opacity=0.35, transform="translate(1.5 2)")
    ic.rect(101, 82, 54, 56, rx=8, fill=brass(ic))
    ic.rect(104, 85, 48, 50, rx=6, fill=ic.lin([(0, "#2E5296"), (1, "#14275A")]))
    mx, my = cx, 110
    ring = (f"M{polar(mx, my, 15, 55)[0]:.1f} {polar(mx, my, 15, 55)[1]:.1f}"
            f"A15 15 0 1 1 {polar(mx, my, 15, 20)[0]:.1f} {polar(mx, my, 15, 20)[1]:.1f}")
    ic.path(ring, fill="none", stroke="#E3F6FD", stroke_width=5.5, stroke_linecap="round")
    blade = (f"M{polar(mx, my, 17, 37)[0]:.1f} {polar(mx, my, 17, 37)[1]:.1f}"
             f"L{polar(mx, my, 7, 230)[0]:.1f} {polar(mx, my, 7, 230)[1]:.1f}"
             f"A4.5 4.5 0 0 1 {polar(mx, my, 1, 180)[0]:.1f} {polar(mx, my, 1, 180)[1]:.1f}Z")
    ic.path(blade, fill="#E3F6FD")
    for x, y in ((107.5, 88.5), (148.5, 88.5), (107.5, 131.5), (148.5, 131.5)):
        ic.circle(x, y, 1.6, fill="#F6DDA0")
    ic.path("M106 88a3 3 0 0 1 3-3h20L106 112z", fill="#fff", opacity=0.14)


@small("mattermost-desktop")
def mattermost16(ic):
    tile(ic, "#2A4378", "#101E3C")
    ic.rect(2, 1.8, 9, 1.2, rx=0.6, fill="#C99645")
    ic.path("M6 4.4C6 3.6 6.8 3.2 8 3.2S10 3.6 10 4.4L10.4 9C10.6 10.6 11.6 11.2 13 11.6V12.8H3V11.6C4.4 11.2 5.4"
            " 10.6 5.6 9Z", fill="#D9A852")
    ic.path("M6.6 4.6L6.3 9.4C6.1 10.6 5.4 11.2 4.2 11.8", fill="none", stroke="#FBEBC0", stroke_width=0.6)
    ic.rect(6.2, 5.2, 3.6, 3.6, rx=0.6, fill="#1E3A7A")
    ic.circle(8, 7, 1.1, fill="none", stroke="#E3F6FD", stroke_width=0.6)
    ic.circle(8, 13.9, 1, fill="#C99645")


# --- Rocket.Chat: a tin rocket, its bubble on the fin -----------------------

@icon("rocketchat-desktop", kind="app", names=["chat.rocket.RocketChat", "rocketchat", "rocketchat-desktop"],
      title="Rocket.Chat")
def rocketchat(ic):
    tile(ic, "#2C3352", "#121528")
    shadow(ic, 128, 220, 62, 9)
    red = ic.lin([(0, "#FF8A96"), (0.4, "#F5455C"), (1, "#A81A30")], 0, 0, 1, 0)
    white = ic.lin([(0, "#FFFFFF"), (0.5, "#E8E6EE"), (1, "#A9A6B6")], 0, 0, 1, 0)
    # the exhaust, a little flame
    ic.path("M106 190c0 22 22 38 22 38s22-16 22-38z", fill="#F28A3C")
    ic.path("M112 190c0 18 16 30 16 30s16-12 16-30z", fill="#F2C45C")
    ic.path("M120 190c0 12 8 20 8 20s8-8 8-20z", fill="#FFF3C4")
    # the fins
    ic.path("M92 140L52 186l4 12 40-14z", fill=red)
    ic.path("M164 140L204 186l-4 12-40-14z", fill=red)
    ic.path("M52 186l4 12 40-14", fill="none", stroke="#000", stroke_opacity=0.25)
    # the body
    body = "M128 20C96 44 86 90 90 140c2 24 6 40 10 52h56c4-12 8-28 10-52 4-50-6-96-38-120z"
    ic.path(body, fill="#000", opacity=0.3, transform="translate(3 4)")
    ic.path(body, fill=white)
    clip = ic.clip(f'<path d="{body}"/>')
    with ic.g(clip_path=clip):
        ic.rect(60, 0, 140, 58, fill=red)
        ic.rect(60, 150, 140, 60, fill=red)
        ic.rect(60, 146, 140, 4, fill="#7A1020", opacity=0.6)
        ic.rect(60, 58, 140, 3, fill="#7A1020", opacity=0.4)
        for y in (78, 128, 170):
            for x in range(86, 172, 10):
                ic.circle(x, y, 1.2, fill="#7A7790" if y != 170 else "#7A1020", opacity=0.6)
    ic.path("M100 50c6-14 14-24 26-30", fill="none", stroke="#fff", stroke_opacity=0.7, stroke_width=2.4,
            stroke_linecap="round")
    # the porthole
    ic.circle(128, 100, 22, fill=steel(ic, False))
    ic.circle(128, 100, 16, fill=ic.rad([(0, "#5A6A9A"), (1, "#141A30")], cx=0.35, cy=0.35, r=0.8))
    ic.circle(128, 100, 16, fill=glare(ic, 1.4))
    ic.path("M117 96a12 12 0 0 1 9-9", fill="none", stroke="#fff", stroke_opacity=0.7, stroke_width=2,
            stroke_linecap="round")
    for a in range(0, 360, 45):
        _screw(ic, *polar(128, 100, 19, a), 1.2)
    # the middle fin, toward us, Rocket.Chat's bubble on it
    ic.path("M128 150c-8 0-10 4-10 10v44h20v-44c0-6-2-10-10-10z", fill=ic.lin([(0, "#F5455C"), (1, "#A81A30")]))
    ic.path("M120 176c0-5 3-8 8-8s8 3 8 8-3 8-8 8h-3l-4 3v-4c-1-2-1-4-1-7z", fill="#fff")
    for x in (125, 128, 131):
        ic.circle(x, 176, 0.9, fill="#F5455C")
    ic.text("RC-1", 128, 142, 9, font="mono-semibold", anchor="middle", spacing=1, fill="#fff")


@small("rocketchat-desktop")
def rocketchat16(ic):
    tile(ic, "#2C3352", "#121528")
    ic.path("M5.6 9L3 12.6l.4.8L6 12.2zM10.4 9L13 12.6l-.4.8L10 12.2z", fill="#F5455C")
    ic.path("M8 1.2C6 2.8 5.4 6 5.8 9.4L6.4 13h3.2l.6-3.6C10.6 6 10 2.8 8 1.2z", fill="#EFEDF3")
    ic.path("M8 1.2C7 2 6.4 3 6.1 4.2h3.8C9.6 3 9 2 8 1.2z", fill="#F5455C")
    ic.circle(8, 6.6, 1.3, fill="#2C3352")
    ic.path("M6.4 13h3.2l-1.6 2z", fill="#F2C45C")


# --- Proton Mail: a purple strongbox, a letter in its slot -----------------

@icon("proton-mail", kind="app", names=["me.proton.Mail", "proton-mail"], title="Proton Mail")
def protonmail(ic):
    tile(ic, "#5B3FD6", "#261670")
    shadow(ic, 128, 214, 98, 12)
    ic.rect(40, 54, 176, 156, rx=12, fill="#000", opacity=0.3, transform="translate(3 4)")
    ic.rect(40, 54, 176, 156, rx=12, fill=ic.lin([(0, "#8E73FF"), (0.5, "#6D4AFF"), (1, "#3A1FB0")], 0, 0, 1, 1))
    ic.rect(40.75, 54.75, 174.5, 154.5, rx=11.25, fill="none", stroke="#fff", stroke_opacity=0.3, stroke_width=1.5)
    # the letter slot on top, a letter going in
    ic.rect(80, 64, 96, 10, rx=5, fill="#1A1040")
    with ic.g(transform="rotate(-4 128 60)"):
        ic.rect(86, 26, 84, 44, rx=2, fill=paper(ic, "white"))
        ic.path("M86 28l42 22 42-22", fill="none", stroke="#C9C2E0", stroke_width=1.4)
        ic.text("to: you@proton.me", 92, 64, 7, font="mono", fill="#5B3FD6")
    ic.rect(80, 69, 96, 5, fill="#1A1040")
    ic.line(82, 75, 174, 75, stroke="#fff", stroke_opacity=0.35)
    # the door
    ic.rect(54, 86, 148, 112, rx=8, fill="#2E1890", opacity=0.6)
    ic.rect(56, 86, 146, 110, rx=8, fill=ic.lin([(0, "#7C5CFF"), (1, "#4A2BD0")], 0, 0, 1, 1))
    ic.path("M60 196V94a8 8 0 0 1 8-8h126", fill="none", stroke="#fff", stroke_opacity=0.3, stroke_width=1.5)
    for y in (98, 184):
        ic.rect(46, y - 8, 12, 18, rx=3, fill=steel(ic, False))
    # the dial
    cx, cy = 106, 140
    ic.circle(cx + 2, cy + 3, 30, fill="#000", opacity=0.3)
    ic.circle(cx, cy, 30, fill=steel(ic, False))
    ic.circle(cx, cy, 24, fill=ic.lin([(0, "#3A3E44"), (1, "#16171A")], 0, 0, 1, 1))
    for k in range(40):
        x1, y1 = polar(cx, cy, 23, k * 9)
        x2, y2 = polar(cx, cy, 23 - (5 if k % 5 == 0 else 2.5), k * 9)
        ic.line(x1, y1, x2, y2, stroke="#E9E4FF", stroke_width=1 if k % 5 == 0 else 0.6)
    ic.circle(cx, cy, 11, fill=steel(ic, False))
    ic.path(f"M{cx} {cy - 31}l-3-5h6z", fill="#F2C45C")
    # the handle
    ic.rect(150, 112, 12, 56, rx=6, fill="#000", opacity=0.3, transform="translate(2 3)")
    ic.rect(150, 112, 12, 56, rx=6, fill=steel(ic))
    ic.circle(156, 140, 9, fill=steel(ic, False))
    # Proton's mark, engraved on a plate: a P cut from a rounded block
    ic.rect(140, 176, 50, 14, rx=3, fill="#E9E4FF", opacity=0.92)
    ic.text("PROTON", 165, 186.5, 8, font="mono-semibold", anchor="middle", spacing=1.2, fill="#3A1FB0")


@small("proton-mail")
def protonmail16(ic):
    tile(ic, "#5B3FD6", "#261670")
    ic.rect(5, 1.5, 6, 4, fill="#FFFFFF")
    ic.rect(2, 4.5, 12, 10, rx=1.2, fill="#8E73FF")
    ic.rect(4.5, 4.5, 7, 1, fill="#1A1040")
    ic.circle(7, 10, 2.6, fill="#2A2C30")
    ic.circle(7, 10, 1, fill="#C3C8CE")
    ic.rect(10.5, 8, 1.4, 4, rx=0.7, fill="#D4D8DD")


# --- Mailspring: a hanging spring balance, a bundle of letters on it ------

@icon("mailspring", kind="app", names=["com.getmailspring.Mailspring", "mailspring"], title="Mailspring")
def mailspring(ic):
    tile(ic, "#1F7F8A", "#0B3F46")
    shadow(ic, 128, 222, 64, 8)
    cx = 128
    # the ring it hangs from
    ic.circle(cx, 24, 10, fill="none", stroke=brass(ic), stroke_width=5)
    # the body: a brass tube with a window down its face
    ic.rect(cx - 26, 32, 52, 120, rx=10, fill="#000", opacity=0.3, transform="translate(3 4)")
    ic.rect(cx - 26, 32, 52, 120, rx=10, fill=brass(ic, 0, 0, 1, 0))
    ic.rect(cx - 26, 32, 52, 120, rx=10, fill="none", stroke="#fff", stroke_opacity=0.25, stroke_width=1.5)
    ic.rect(cx - 16, 44, 32, 98, rx=4, fill="#0E2A2E")
    # the spring, coiled behind the glass
    for k in range(10):
        y = 48 + k * 6.6
        ic.path(f"M{cx - 12} {y}q12 6 24 0", fill="none", stroke="#46D8DA", stroke_width=2.2)
        ic.path(f"M{cx - 12} {y}q12 6 24 0", fill="none", stroke="#fff", stroke_opacity=0.35, stroke_width=0.7,
                transform="translate(0 -0.8)")
    # the pointer and the scale beside the window
    ic.rect(cx - 15, 116, 30, 4, rx=1, fill="#E0483A")
    for k in range(9):
        y = 50 + k * 10
        ic.line(cx + 16, y, cx + 22 if k % 2 == 0 else cx + 19, y, stroke="#3A2A10", stroke_width=1.2)
        ic.line(cx - 16, y, cx - 22 if k % 2 == 0 else cx - 19, y, stroke="#3A2A10", stroke_width=1.2)
    ic.rect(cx - 16, 44, 32, 98, rx=4, fill=glare(ic, 1.2))
    ic.text("250 g", cx + 34, 121, 9, font="mono-semibold", fill="#E3FBFB")
    # the hook and the bundle of letters, tied with string
    ic.path(f"M{cx} 152v12a8 8 0 1 1-8 8", fill="none", stroke=steel(ic, False), stroke_width=4,
            stroke_linecap="round")
    with ic.g(transform=f"rotate(-3 {cx} 190)"):
        for i, (dx, c) in enumerate(((6, "#E4DCCB"), (3, "#EFE9DD"), (0, "#FFFFFF"))):
            ic.rect(cx - 62 + dx, 176 + dx * 1.5, 124, 38, rx=3, fill=c, stroke="#000", stroke_opacity=0.08)
        ic.path(f"M{cx - 62} 180l62 18 62-18", fill="none", stroke="#D0C8B6", stroke_width=1.4)
        ic.rect(cx - 2, 176, 4, 38, fill="#46D8DA")
        ic.rect(cx - 62, 193, 124, 4, fill="#46D8DA")
        ic.text("mailspring", cx - 56, 210, 8, font="mono", fill="#1F7F8A")
        # a stamp in Mailspring's colours, its mark a springing swallow's V
        ic.rect(cx + 34, 180, 22, 26, fill="#fff", stroke="#B9C2C7", stroke_dasharray="2 2")
        ic.rect(cx + 37, 183, 16, 20, fill="#35D5D7")
        ic.path(f"M{cx + 39} 189l6 8 6-8-6 3z", fill="#fff")
    ic.path(f"M{cx - 2} 176l2-10 2 10", fill="none", stroke="#46D8DA", stroke_width=1.5)


@small("mailspring")
def mailspring16(ic):
    tile(ic, "#1F7F8A", "#0B3F46")
    ic.circle(8, 1.6, 0.9, fill="none", stroke="#C99645", stroke_width=0.6)
    ic.rect(6.2, 2.4, 3.6, 7, rx=0.8, fill="#C99645")
    ic.rect(7, 3.2, 2, 5.4, fill="#0E2A2E")
    ic.path("M7.2 4h1.6M7.2 5.2h1.6M7.2 6.4h1.6M7.2 7.6h1.6", stroke="#46D8DA", stroke_width=0.5)
    ic.rect(2.5, 10.5, 11, 4, rx=0.4, fill="#FFFFFF")
    ic.rect(2.5, 12.2, 11, 0.7, fill="#35D5D7")


# --- Betterbird: a birdhouse, a letter in its door --------------------------

@icon("betterbird", kind="app", names=["betterbird", "eu.betterbird.Betterbird"], title="Betterbird")
def betterbird(ic):
    tile(ic, "#2F5F9E", "#122E58")
    shadow(ic, 128, 218, 58, 8)
    # the pole
    ic.rect(119, 170, 18, 50, fill=wood(ic, "#8E6238", "#4E2F14"))
    # the house: its walls
    walls = "M56 104L128 50 200 104V182a6 6 0 0 1-6 6H62a6 6 0 0 1-6-6z"
    ic.path(walls, fill="#000", opacity=0.3, transform="translate(3 4)")
    ic.path(walls, fill=ic.lin([(0, "#F7F2E7"), (1, "#D8CDB6")], 0, 0, 1, 1))
    for x in range(72, 200, 16):
        ic.line(x, 80 if x < 128 else 80, x, 188, stroke="#9C8A6A", stroke_opacity=0.25)
    # the roof, two warm boards
    ic.path("M36 112L128 38l92 74-10 8-82-66-82 66z", fill="#000", opacity=0.3, transform="translate(2 5)")
    ic.path("M36 112L128 38v18L46 120z", fill=ic.lin([(0, "#F6C34E"), (1, "#D48A14")], 0, 0, 1, 1))
    ic.path("M220 112L128 38v18l82 64z", fill=ic.lin([(0, "#EF4334"), (1, "#A8231A")], 0, 0, 1, 1))
    ic.path("M38 111L128 39", stroke="#fff", stroke_opacity=0.5, stroke_width=1.6)
    # the door: a round hole, a letter put through it
    ic.circle(128, 122, 22, fill="#2A1C10")
    ic.circle(128, 122, 22, fill="none", stroke="#9C8A6A", stroke_width=3)
    ic.path("M108 116a22 22 0 0 1 32-14", fill="none", stroke="#000", stroke_opacity=0.35, stroke_width=4)
    with ic.g(transform="rotate(-12 128 128)"):
        ic.rect(100, 120, 56, 30, rx=2, fill=paper(ic, "white"))
        ic.path("M100 121l28 15 28-15", fill="none", stroke="#C9BFA9", stroke_width=1.2)
    # the perch
    ic.rect(122, 158, 12, 16, rx=2, fill="#000", opacity=0.25, transform="translate(2 2)")
    ic.ellipse(128, 166, 7, 5, fill=wood(ic, "#B07A48", "#6E4220"))
    # the bird, painted on the gable: Betterbird's, its wing over a letter
    ic.text("BETTERBIRD", 128, 182, 7, font="mono-semibold", anchor="middle", spacing=1.4, fill="#7A6A4A")
    ic.path("M114 82c4-6 12-8 18-4l6-4-2 6c2 4 0 10-6 12-6 2-12 0-16-6l-6 0z", fill="#EF4334")
    ic.path("M122 84c4 4 10 4 14 0", fill="none", stroke="#EEB43F", stroke_width=2.4, stroke_linecap="round")
    ic.circle(132, 80, 1.3, fill="#1A1B1E")


@small("betterbird")
def betterbird16(ic):
    tile(ic, "#2F5F9E", "#122E58")
    ic.rect(7.2, 12, 1.6, 3.5, fill="#8E6238")
    ic.path("M3.5 7L8 3.6 12.5 7v5a.5.5 0 0 1-.5.5H4a.5.5 0 0 1-.5-.5z", fill="#F2EBDD")
    ic.path("M2 7.6L8 2.6v1.4L3 8.2z", fill="#EEB43F")
    ic.path("M14 7.6L8 2.6v1.4l5 4.2z", fill="#EF4334")
    ic.circle(8, 8.4, 1.6, fill="#2A1C10")


# --- Tuta: a postman's satchel in red leather, buckled -------------------

@icon("tuta", kind="app", names=["appimagekit-tutanota-desktop", "com.tutanota.Tutanota", "tuta",
                                 "tutanota-desktop"], title="Tuta")
def tuta(ic):
    tile(ic, "#9A2234", "#4E0A16")
    shadow(ic, 128, 214, 100, 12)
    # the strap, over the top
    ic.path("M48 120C40 30 216 30 208 120", fill="none", stroke="#000", stroke_opacity=0.3, stroke_width=16,
            transform="translate(2 4)")
    ic.path("M48 120C40 30 216 30 208 120", fill="none", stroke=leather(ic, "#C42E46", "#6E0A1C"), stroke_width=14)
    ic.path("M48 120C40 30 216 30 208 120", fill="none", stroke="#F7C6CE", stroke_opacity=0.4, stroke_width=1,
            stroke_dasharray="3 3")
    ic.path("M52 92C64 52 120 44 150 47", fill="none", stroke="#fff", stroke_opacity=0.3, stroke_width=1.5,
            transform="translate(-4 -5)", stroke_linecap="round")
    for x in (48, 208):
        ic.rect(x - 9, 104, 18, 14, rx=3, fill=steel(ic, False))
    # letters in the bag
    for i, (x, a) in enumerate(((64, -8), (98, 3), (140, -5))):
        with ic.g(transform=f"rotate({a} {x + 30} 120)"):
            ic.rect(x, 84, 60, 40, rx=2, fill=("#F2ECDF", "#FFFFFF", "#EAF0F8")[i], stroke="#000",
                    stroke_opacity=0.1)
            if i == 1:
                ic.rect(x + 42, 88, 12, 14, fill="#D93951")
                ic.line(x + 8, 96, x + 34, 96, stroke="#9A9284", stroke_width=1.2)
                ic.line(x + 8, 102, x + 28, 102, stroke="#9A9284", stroke_width=1.2)
    # the bag
    ic.rect(34, 108, 188, 104, rx=16, fill="#000", opacity=0.3, transform="translate(3 4)")
    ic.rect(34, 108, 188, 104, rx=16, fill=leather(ic, "#C42E46", "#6E0A1C"))
    ic.rect(42, 116, 172, 88, rx=10, fill="none", stroke="#F7C6CE", stroke_opacity=0.4, stroke_width=1.2,
            stroke_dasharray="4 3")
    # the flap, a rounded tongue to the buckle
    flap = "M30 110a8 8 0 0 1 8-8h180a8 8 0 0 1 8 8v28c0 14-12 24-26 24h-40c-10 0-14 6-16 14h-28c-2-8-6-14-16-14h-40c-14 0-26-10-26-24z"
    ic.path(flap, fill="#000", opacity=0.35, transform="translate(1 5)")
    ic.path(flap, fill=ic.lin([(0, "#F0607A"), (0.5, "#D93951"), (1, "#9E1A30")], 0, 0, 0.3, 1))
    ic.path("M32 136V110a6 6 0 0 1 6-6h180", fill="none", stroke="#fff", stroke_opacity=0.4, stroke_width=1.6,
            stroke_linecap="round")
    ic.path("M38 112h180v24c0 10-9 18-20 18h-42c-10 0-16 6-18 12h-20c-2-6-8-12-18-12h-42c-11 0-20-8-20-18z",
            fill="none", stroke="#FFD9DF", stroke_opacity=0.55, stroke_width=1.2, stroke_dasharray="4 3")
    # the name, stamped in white
    ic.text("tuta", 128, 145, 32, font="sans-bold", anchor="middle", fill="#5E0A18", opacity=0.55,
            transform="translate(0 1.6)")
    ic.text("tuta", 128, 145, 32, font="sans-bold", anchor="middle", fill="#FFF1F3")
    # the strap down from the flap and its buckle
    ic.rect(119, 166, 18, 38, rx=3, fill=leather(ic, "#D93951", "#7A0F22"))
    for y in (190, 197):
        ic.circle(128, y, 1.6, fill="#4E0A16")
    ic.rect(110, 164, 36, 22, rx=5, fill="none", stroke="#000", stroke_opacity=0.3, stroke_width=4.5,
            transform="translate(1 2)")
    ic.rect(110, 164, 36, 22, rx=5, fill="none", stroke=steel(ic), stroke_width=4.5)
    ic.path("M112 166h32", stroke="#fff", stroke_opacity=0.6, stroke_width=1)
    ic.rect(126, 162, 4, 26, rx=2, fill=steel(ic, False))


@small("tuta")
def tuta16(ic):
    tile(ic, "#9A2234", "#4E0A16")
    ic.path("M3 7C3 2 13 2 13 7", fill="none", stroke="#5E0A18", stroke_width=1.2)
    ic.rect(4, 4.6, 6, 3, fill="#FFFFFF")
    ic.rect(2, 6.5, 12, 7.5, rx=1.2, fill="#B42238")
    ic.path("M2 6.5h12v3a1.5 1.5 0 0 1-1.5 1.5h-9A1.5 1.5 0 0 1 2 9.5z", fill="#E44E66")
    ic.rect(7, 9.4, 2, 2.4, rx=0.3, fill="none", stroke="#D4D8DD", stroke_width=0.6)
