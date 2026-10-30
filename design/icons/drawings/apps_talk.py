"""The inua-objects theme, talk: Thunderbird, Telegram, Signal, Discord,
Slack, Element, Zoom, Mixin Messenger (docs/feat/object-icons.md, Part 2).
Each has its own object, so the chat apps do not all become one bubble."""

from lib import (glare, graphite, icon, paper, polar, shadow, small, steel, tile)


def _screw(ic, x, y, r=3.2):
    ic.circle(x, y, r, fill=steel(ic, horizontal=False))
    ic.line(x - r * 0.6, y + r * 0.35, x + r * 0.6, y - r * 0.35, stroke="#3C4148", stroke_width=0.9)


# --- Thunderbird: a blue bird curled round a letter -------------------------

@icon("thunderbird", kind="app", names=["org.mozilla.Thunderbird", "thunderbird", "thunderbird-bin",
                                        "thunderbird-icon", "thunderbird-mozilla-build"], title="Thunderbird")
def thunderbird(ic):
    tile(ic, "#34507E", "#16243F")
    shadow(ic, 128, 214, 92, 12)
    # the letter, held in the bird's curl
    with ic.g(transform="rotate(-4 140 140)"):
        ic.rect(76, 98, 132, 92, rx=7, fill="#000", opacity=0.25, transform="translate(3 4)")
        ic.rect(76, 98, 132, 92, rx=7, fill=paper(ic, "cream"))
        ic.path("M78 186 L130 146 a14 14 0 0 1 18 0 L206 186", fill="#EFE7D6", stroke="#000", stroke_opacity=0.07)
        ic.path("M80 104 L131 148 a12 12 0 0 0 16 0 L204 104", fill="#000", opacity=0.08)
        ic.path("M76 105a7 7 0 0 1 7-7h118a7 7 0 0 1 7 7 L148 152 a13 13 0 0 1-16 0z",
                fill=ic.lin([(0, "#FFFDF8"), (1, "#E9E1CF")]))
        ic.line(83, 99, 201, 99, stroke="#fff", stroke_width=1.6, opacity=0.9)
        ic.text("for Sam", 182, 178, 13, font="hand", anchor="middle", fill="#5A6B8C", opacity=0.8)
    # the bird, one sweep: tail under the letter, wing up the left, the
    # back rising into the head, which looks right over the letter
    body = ic.lin([(0, "#8ACBFF"), (0.4, "#2E83F0"), (1, "#3B33B8")], 0.3, 0, 0.7, 1)
    bird = ("M206 180 C184 204 150 216 116 212 C64 206 30 160 40 110 C48 64 94 36 140 36"
            " C150 26 166 22 182 26 C198 30 208 42 212 56 C206 66 196 74 180 78"
            " C150 80 98 84 80 104 C68 124 72 164 108 182 C138 196 176 196 206 180 Z")
    # the crest, swept back behind the head
    ic.path("M156 30 C146 14 126 8 106 12 C124 16 138 24 146 36 Z", fill="#3F8EF2")
    ic.path("M150 40 C136 28 116 24 98 28 C116 30 130 38 138 46 Z", fill="#2367D8")
    ic.path(bird, fill="#000", opacity=0.22, transform="translate(3 4)")
    ic.path(bird, fill=body)
    # feathers along the wing, a lighter blue, and the shade under the tail
    ic.path("M60 92 C70 68 96 54 124 50 C100 62 82 80 74 104 Z", fill="#A8DBFF", opacity=0.7)
    ic.path("M48 132 C50 108 60 92 72 82 C66 98 64 116 66 134 Z", fill="#A8DBFF", opacity=0.4)
    ic.path("M62 170 C72 186 92 198 116 202 C96 204 76 196 62 182 Z", fill="#1E1F7A", opacity=0.35)
    ic.path("M140 38 C96 38 50 62 41 110", fill="none", stroke="#fff", stroke_opacity=0.45, stroke_width=2,
            stroke_linecap="round")
    # the face: a pale cheek, the eye, the beak
    ic.path("M150 50 C160 40 176 36 190 40 C200 44 206 50 210 58 C202 66 190 72 176 74 C160 74 150 64 150 50Z",
            fill=ic.rad([(0, "#CFEBFF"), (1, "#5FA8F8", 0)], cx=0.55, cy=0.45, r=0.6), opacity=0.8)
    ic.path("M211 52 L226 60 L206 66 Z", fill=ic.lin([(0, "#FFD978"), (1, "#E09A2A")]))
    ic.circle(188, 48, 4.4, fill="#10183A")
    ic.circle(186.7, 46.6, 1.4, fill="#fff")
    ic.path("M146 34 C158 26 174 24 188 28", fill="none", stroke="#fff", stroke_opacity=0.55,
            stroke_width=1.8, stroke_linecap="round")


@small("thunderbird")
def thunderbird16(ic):
    tile(ic, "#34507E", "#16243F")
    ic.rect(5.2, 6.4, 8.4, 6.2, rx=0.6, fill="#F6F1E6")
    ic.path("M5.5 6.9 L9.4 10 L13.3 6.9", fill="none", stroke="#C9BFA9", stroke_width=0.7)
    ic.path("M13.4 11.8 C11.6 13.6 9.6 14.2 7.6 14 C4.2 13.6 1.9 10.8 2.2 7.4 C2.6 4.2 5.4 2.4 8.4 2.4"
            " C9.2 1.6 10.6 1.4 11.8 1.8 C12.8 2.2 13.4 3 13.6 3.8 C12.8 4.8 11.6 5.2 10.4 5.2"
            " C8.4 5.2 6 5.6 5.2 7.2 C4.6 8.8 5 10.8 7 11.8 C9 12.8 11.4 12.8 13.4 11.8Z", fill="#3C8CF2")
    ic.path("M13.6 3.2 L15 3.8 L13.4 4.4Z", fill="#F2C45C")
    ic.circle(11.6, 3.2, 0.55, fill="#10183A")


# --- Telegram: a paper plane folded from a note, in flight ------------------

@icon("telegram", kind="app", names=["io.github.tdesktop_x64.TDesktop", "org.telegram.desktop", "telegram",
                                     "telegram-desktop", "telegram-desktop-bin"], title="Telegram")
def telegram(ic):
    tile(ic, "#2D8CCB", "#123F6A")
    shadow(ic, 118, 214, 74, 9, strength=0.8)
    # where it came from
    ic.path("M24 206 C52 196 66 180 78 164", fill="none", stroke="#fff", stroke_opacity=0.35, stroke_width=2.5,
            stroke_dasharray="6 7", stroke_linecap="round")
    N, L, C, B, K = (220, 50), (32, 122), (104, 142), (162, 200), (120, 186)
    pts = lambda *ps: "M" + "L".join(f"{x} {y}" for x, y in ps) + "Z"
    # the shadow it casts on itself, then the far wing, the keel, the near wing
    ic.path(pts(N, C, B), fill=ic.lin([(0, "#E3EEF7"), (1, "#A9C3DA")], 0, 0, 0.4, 1))
    ic.path(pts(C, K, (140, 152)), fill=ic.lin([(0, "#86A6C4"), (1, "#5B7FA2")]))
    ic.path(pts(N, (140, 152), K), fill=ic.lin([(0, "#C2D6E8"), (1, "#8FAECB")], 1, 0, 0, 1))
    wing = pts(N, L, C)
    ic.path(wing, fill=ic.lin([(0, "#FFFFFF"), (1, "#E6EEF5")], 0, 0, 0.6, 1))
    # the note it was folded from: ruled lines and a line of writing
    clipw = ic.clip(f'<path d="{wing}"/>')
    with ic.g(clip_path=clipw):
        with ic.g(transform="rotate(-20.6 126 96)"):
            for k in range(6):
                ic.line(20, 84 + k * 11, 240, 84 + k * 11, stroke="#7FB2DC", stroke_opacity=0.45, stroke_width=1)
            ic.text("see you at 7?", 92, 103, 15, font="hand", fill="#2D6FA8", opacity=0.75)
    ic.path(pts(N, L, C), fill="none", stroke="#fff", stroke_width=1.5, stroke_linejoin="round", opacity=0.7)
    ic.line(N[0], N[1], C[0], C[1], stroke="#5D88B0", stroke_opacity=0.55, stroke_width=1.5)
    ic.line(N[0], N[1], L[0], L[1], stroke="#fff", stroke_width=2.2, stroke_linecap="round")
    ic.line(N[0], N[1], B[0], B[1], stroke="#4E7598", stroke_opacity=0.35, stroke_width=1.2)


@small("telegram")
def telegram16(ic):
    tile(ic, "#2D8CCB", "#123F6A")
    ic.path("M14 3 L6.6 9.6 L10.2 13.6 Z", fill="#B8CFE3")
    ic.path("M6.6 9.6 L7.6 12.8 L9 10.9 Z", fill="#6E92B5")
    ic.path("M14 3 L1.8 7.8 L6.6 9.6 Z", fill="#FFFFFF")


# --- Signal: a blue walkie-talkie, its grille ringed in broken dashes --------

@icon("signal-desktop", kind="app", names=["org.signal.Signal", "signal-desktop", "signal-desktop-beta"],
      title="Signal")
def signal(ic):
    tile(ic, "#3E4C68", "#18202F")
    shadow(ic, 128, 216, 64, 10)
    # antenna and knob, behind the case
    ic.rect(84, 14, 16, 52, rx=8, fill=ic.lin([(0, "#3A3E45"), (0.4, "#5A6069"), (1, "#16181B")], 0, 0, 1, 0))
    for y in range(24, 56, 6):
        ic.line(85, y, 99, y, stroke="#000", stroke_opacity=0.35, stroke_width=1.2)
    ic.rect(146, 30, 22, 30, rx=4, fill=ic.lin([(0, "#3A3E45"), (0.4, "#646A73"), (1, "#16181B")], 0, 0, 1, 0))
    for x in range(149, 167, 4):
        ic.line(x, 32, x, 58, stroke="#000", stroke_opacity=0.3, stroke_width=1.2)
    # the push-to-talk key on the left side
    ic.rect(56, 92, 16, 46, rx=5, fill=ic.lin([(0, "#2A2D33"), (1, "#121316")]))
    # the case
    case = ic.lin([(0, "#6F9CFA"), (0.5, "#3A76F0"), (1, "#1F4FB8")], 0, 0, 1, 1)
    ic.rect(64, 56, 128, 156, rx=22, fill=case)
    ic.rect(64.75, 56.75, 126.5, 154.5, rx=21.25, fill="none", stroke="#fff", stroke_opacity=0.35,
            stroke_width=1.5)
    ic.path("M176 57a22 22 0 0 1 16 21v112a22 22 0 0 1-22 22H86a22 22 0 0 1-12-4c40 2 90-2 98-14 6-10 6-80 4-137z",
            fill="#0E2A6E", opacity=0.3)
    # the speaker grille
    ic.circle(128, 110, 40, fill="#163C94")
    ic.circle(128, 110, 31, fill=ic.rad([(0, "#22252B"), (1, "#0D0E10")], cx=0.4, cy=0.35, r=0.75))
    for row in range(-3, 4):
        for col in range(-3, 4):
            x, y = 128 + col * 8 + (4 if row % 2 else 0), 110 + row * 7
            if (x - 128) ** 2 + (y - 110) ** 2 < 25 ** 2:
                ic.circle(x, y, 2, fill="#000")
                ic.circle(x - 0.5, y - 0.6, 1, fill="#fff", opacity=0.12)
    # the ring of the mark, broken into dashes, and its tail
    ic.circle(128, 110, 36, fill="none", stroke="#F4F7FF", stroke_width=5, stroke_dasharray="16.5 6.1",
              stroke_dashoffset=3, transform="rotate(-80 128 110)")
    ic.path("M98 134 L90 148 L106 143", fill="none", stroke="#F4F7FF", stroke_width=5, stroke_linejoin="round",
            stroke_linecap="round")
    # the display and keys
    ic.rect(88, 158, 80, 26, rx=4, fill="#0F1F45")
    ic.rect(91, 161, 74, 20, rx=2, fill=ic.lin([(0, "#BFD9D2"), (1, "#93B3AB")]))
    ic.text("CH 01", 96, 175.5, 10, font="mono-semibold", fill="#20302C")
    # a padlock, drawn: the font has none
    ic.path("M150 168 v-3 a4 4 0 0 1 8 0 v3", fill="none", stroke="#20302C", stroke_width=1.6)
    ic.rect(148, 167.5, 12, 9, rx=1.5, fill="#20302C")
    ic.path("M91 163a2 2 0 0 1 2-2h50L131 181H93a2 2 0 0 1-2-2z", fill="#fff", opacity=0.18)
    for x in (98, 128, 158):
        ic.rect(x - 10, 192, 20, 9, rx=4.5, fill="#173E99")
        ic.rect(x - 10, 191, 20, 8, rx=4, fill=ic.lin([(0, "#5D8EF6"), (1, "#2F63D6")]))
    ic.circle(176, 72, 3.2, fill="#7CF7A6")
    ic.circle(176, 72, 6, fill="#7CF7A6", opacity=0.2)
    _screw(ic, 78, 70, 2.6)


@small("signal-desktop")
def signal16(ic):
    tile(ic, "#3E4C68", "#18202F")
    ic.rect(5.2, 1.2, 1.6, 4, rx=0.8, fill="#2A2D33")
    ic.rect(4, 3.5, 8, 11, rx=1.6, fill="#3A76F0")
    ic.circle(8, 7.4, 2.2, fill="#111317")
    ic.circle(8, 7.4, 2.75, fill="none", stroke="#F4F7FF", stroke_width=0.9, stroke_dasharray="2.1 0.75")
    ic.path("M5.9 9.2 L5.3 10.4 L6.6 10", fill="none", stroke="#F4F7FF", stroke_width=0.8)
    ic.rect(5.5, 11.2, 5, 1.6, rx=0.4, fill="#BFD9D2")


# --- Discord: a blurple game pad, the mark's face as its badge --------------

def _face(ic, cx, cy, k, fill, eyes):
    """Discord's face, redrawn: a pad-shaped head with two eyes; k scales."""
    t = f"translate({cx} {cy}) scale({k})"
    ic.path("M-11 -6 Q-6 -9.4 -3 -9.4 L-2 -7.3 Q0 -7.7 2 -7.3 L3 -9.4 Q6 -9.4 11 -6 Q14.2 0 13.2 7.4"
            " Q10 10.2 6.2 11 L4.6 8.6 Q0 9.6 -4.6 8.6 L-6.2 11 Q-10 10.2 -13.2 7.4 Q-14.2 0 -11 -6Z",
            fill=fill, transform=t)
    ic.ellipse(-4.6, 1.4, 2.3, 2.6, fill=eyes, transform=t)
    ic.ellipse(4.6, 1.4, 2.3, 2.6, fill=eyes, transform=t)


@icon("discord", kind="app", names=["com.discordapp.Discord", "discord", "discord-bin", "discord-ptb", "gtkcord"],
      title="Discord")
def discord(ic):
    tile(ic, "#3B3E48", "#1A1B20")
    shadow(ic, 128, 208, 100, 11)
    pad = ("M76 74h104c26 0 36 14 42 40l10 50c4 20-8 32-22 28c-10-3-15-11-21-22l-9-16H76l-9 16"
           "c-6 11-11 19-21 22c-14 4-26-8-22-28l10-50c6-26 16-40 42-40z")
    ic.path(pad, fill="#000", opacity=0.3, transform="translate(2 5)")
    ic.path(pad, fill=ic.lin([(0, "#8C96FA"), (0.45, "#5865F2"), (1, "#3B44B0")], 0, 0, 0.3, 1))
    ic.path("M232 164l-10-50c-2-8-4-14-8-20c4 30 2 72-8 98c10 2 30-4 26-28z", fill="#1E2380", opacity=0.3)
    ic.path("M67 176c-6 11-11 19-21 22c-8 2-16-1-20-8c14 2 26-8 34-28l7 4z", fill="#1E2380", opacity=0.25)
    ic.path("M189 176c6 11 11 19 21 22c-10 0-22-8-30-24z", fill="#1E2380", opacity=0.2)
    ic.path("M44 102c6-18 16-26 34-26h100c18 0 28 8 34 26", fill="none", stroke="#fff", stroke_opacity=0.45,
            stroke_width=2, stroke_linecap="round")
    # shoulder buttons' edge on the top
    ic.path("M58 76 c4-6 12-9 24-9h12v7H76z", fill="#3B44B0")
    ic.path("M198 76 c-4-6-12-9-24-9h-12v7h18z", fill="#3B44B0")
    # the d-pad
    with ic.g(transform="translate(70 116)"):
        ic.circle(0, 0, 20, fill="#454FC6")
        ic.path("M-5 -15h10v10h10v10h-10v10h-10v-10h-10v-10h10z", fill="#1A1C2E", transform="translate(1 1.5)")
        ic.path("M-5 -15h10v10h10v10h-10v10h-10v-10h-10v-10h10z", fill=ic.lin([(0, "#3A3D52"), (1, "#20222F")]))
        ic.path("M-4 -14h8", stroke="#fff", stroke_opacity=0.25, stroke_width=1.2)
        ic.path("M0 -11 l-2.5 3.5h5z M0 11 l-2.5 -3.5h5z M-11 0 l3.5 -2.5v5z M11 0 l-3.5 -2.5v5z",
                fill="#8C96FA", opacity=0.8)
    # the face buttons
    with ic.g(transform="translate(186 116)"):
        ic.circle(0, 0, 22, fill="#454FC6")
        for dx, dy in ((0, -12), (12, 0), (0, 12), (-12, 0)):
            ic.circle(dx + 0.8, dy + 1.6, 6.5, fill="#1A1C2E")
            ic.circle(dx, dy, 6.5, fill=ic.rad([(0, "#FFFFFF"), (1, "#C9CDF5")], cx=0.35, cy=0.3, r=0.8))
    # the sticks
    for x in (100, 156):
        ic.circle(x, 150, 17, fill="#2E3591")
        ic.circle(x + 1, 152, 12.5, fill="#0E0F18", opacity=0.6)
        ic.circle(x, 150, 12.5, fill=ic.rad([(0, "#4A4E62"), (1, "#1E2030")], cx=0.35, cy=0.3, r=0.8))
        ic.circle(x, 150, 8, fill="none", stroke="#000", stroke_opacity=0.35, stroke_width=1.2)
        ic.circle(x - 3, 146.5, 3, fill="#fff", opacity=0.15)
    # the badge: the face pressed in white enamel
    ic.circle(128.6, 109.6, 19, fill="#2E3591")
    ic.circle(128, 108, 19, fill=ic.rad([(0, "#FFFFFF"), (1, "#D9DCF8")], cx=0.35, cy=0.3, r=0.8))
    ic.circle(128, 108, 19, fill="none", stroke="#3B44B0", stroke_opacity=0.5, stroke_width=1.2)
    _face(ic, 128, 108.5, 1.02, "#5865F2", "#FFFFFF")
    for x in (99, 157):
        ic.rect(x - 5, 95, 10, 4.5, rx=2.25, fill="#2E3591")


@small("discord")
def discord16(ic):
    tile(ic, "#3B3E48", "#1A1B20")
    ic.path("M4.8 4.5h6.4c1.6 0 2.3.9 2.6 2.5l.7 3.4c.3 1.4-1 2.1-1.8 1.3l-1.6-1.9H5l-1.6 1.9"
            "c-.8.8-2.1.1-1.8-1.3l.7-3.4c.3-1.6 1-2.5 2.5-2.5z", fill="#5865F2")
    ic.ellipse(6.4, 7.3, 1, 1.1, fill="#fff")
    ic.ellipse(9.6, 7.3, 1, 1.1, fill="#fff")


# --- Slack: a corkboard, four notes pinned in the mark's pinwheel -------------

@icon("slack", kind="app", names=["com.slack.Slack", "slack"], title="Slack")
def slack(ic):
    tile(ic, "#5B2D5E", "#2A0F2C")
    shadow(ic, 128, 214, 98, 11)
    # the frame and the cork
    ic.rect(26, 34, 204, 178, rx=10, fill=ic.lin([(0, "#D9A46A"), (0.5, "#A86E38"), (1, "#6E421C")], 0, 0, 1, 1))
    ic.rect(26.75, 34.75, 202.5, 176.5, rx=9.25, fill="none", stroke="#FFE2B8", stroke_opacity=0.35,
            stroke_width=1.5)
    ic.rect(37, 45, 182, 156, rx=3, fill="#5A3412")
    ic.rect(38, 46, 180, 154, rx=2.5, fill=ic.rad([(0, "#D3A672"), (1, "#A9784A")], cx=0.35, cy=0.3, r=0.85))
    dots = ic.define('<pattern id="{id}" width="9" height="7" patternUnits="userSpaceOnUse">'
                     '<circle cx="2" cy="2" r=".9" fill="#5E3814" opacity=".35"/>'
                     '<circle cx="6.5" cy="5" r=".7" fill="#5E3814" opacity=".3"/>'
                     '<circle cx="4.5" cy="1" r=".6" fill="#FFF0D6" opacity=".25"/></pattern>', "p")
    ic.rect(38, 46, 180, 154, fill=f"url(#{dots})")
    ic.path("M38 48.5h180", stroke="#000", stroke_opacity=0.25, stroke_width=3)
    # the notes: a pinwheel of four, in the mark's colours
    x0, y0, L, S, g = 55, 52, 88, 56, 2.5
    notes = [
        ((x0, y0, L, S), "#36C5F0", "#1B88B3", "#0D4F6C", "#general", -2, (x0 + 14, y0 + 12)),
        ((x0 + L, y0, S, L), "#2EB67D", "#1C8457", "#0B4A2E", "ship", 2, (x0 + L + S / 2, y0 + 12)),
        ((x0 + S, y0 + L, L, S), "#ECB22E", "#C48A12", "#5E3F00", "standup 10", -1.5,
         (x0 + S + L - 14, y0 + L + 12)),
        ((x0, y0 + S, S, L), "#E01E5A", "#A90F3D", "#FFFFFF", "lunch?", 2.5, (x0 + S / 2, y0 + S + 12)),
    ]
    for (x, y, w, h), light, dark, ink, words, rot, pin in notes:
        x, y, w, h = x + g, y + g, w - 2 * g, h - 2 * g
        with ic.g(transform=f"rotate({rot} {x + w / 2} {y + h / 2})"):
            ic.rect(x + 2, y + 4, w, h, rx=2, fill="#3A1E06", opacity=0.35)
            ic.rect(x, y, w, h, rx=2, fill=ic.lin([(0, light), (1, dark)], 0, 0, 0.4, 1))
            ic.path(f"M{x + w} {y + h - 12} L{x + w - 12} {y + h} H{x + w - 2} a2 2 0 0 0 2-2z",
                    fill="#000", opacity=0.18)
            ic.line(x + 1, y + 0.8, x + w - 1, y + 0.8, stroke="#fff", stroke_opacity=0.45, stroke_width=1.2)
            if w > h:
                ic.text(words, x + w / 2, y + h / 2 + 11, 17, font="hand", anchor="middle", fill=ink,
                        opacity=0.85)
            else:
                ic.text(words, x + w / 2, y + h / 2 + 8, 15, font="hand", anchor="middle", fill=ink,
                        opacity=0.85, transform=f"rotate(-90 {x + w / 2} {y + h / 2 + 3})")
    # pins
    for (_, light, dark, *_r), (px, py) in zip(notes, [n[6] for n in notes]):
        ic.ellipse(px + 2.5, py + 3.5, 5.5, 3.5, fill="#000", opacity=0.3)
        ic.circle(px, py, 5.6, fill=ic.rad([(0, "#F4F4F2"), (1, "#8A8C90")], cx=0.35, cy=0.3, r=0.8))
        ic.circle(px - 1.6, py - 1.8, 1.6, fill="#fff", opacity=0.9)


@small("slack")
def slack16(ic):
    tile(ic, "#5B2D5E", "#2A0F2C")
    ic.rect(1.8, 2.2, 12.4, 11.6, rx=1, fill="#B98654")
    ic.rect(3.2, 3.4, 5.8, 3.4, rx=0.3, fill="#36C5F0")
    ic.rect(9.2, 3.4, 3.6, 5.8, rx=0.3, fill="#2EB67D")
    ic.rect(7, 9.4, 5.8, 3.2, rx=0.3, fill="#ECB22E")
    ic.rect(3.2, 7, 3.6, 5.6, rx=0.3, fill="#E01E5A")


# --- Element: a glazed periodic-table tile, "El", number 1 -------------------

def _ceramic(ic, x, y, s, light, mid, dark, edge):
    """A square glazed tile, s px a side, its fired edge below and right."""
    ic.rect(x + 4, y + 7, s, s, rx=14, fill="#000", opacity=0.35)
    ic.rect(x + 3, y + 5, s, s, rx=14, fill=edge)
    ic.rect(x, y, s, s, rx=14, fill=ic.lin([(0, light), (0.45, mid), (1, dark)], 0, 0, 1, 1))
    ic.rect(x + 1, y + 1, s - 2, s - 2, rx=13, fill="none", stroke="#fff", stroke_opacity=0.45, stroke_width=2)
    ic.rect(x + 9, y + 9, s - 18, s - 18, rx=8, fill="none", stroke="#000", stroke_opacity=0.12, stroke_width=1.5)


@icon("element-desktop", kind="app", names=["Element", "element", "element-desktop", "element-desktop-bin",
                                            "im.riot.Riot", "io.element.Element", "riot"], title="Element")
def element(ic):
    tile(ic, "#2B4A43", "#0F201C")
    shadow(ic, 128, 214, 98, 11)
    # the tile behind: cream, the one before it in the row
    with ic.g(transform="rotate(10 186 82)"):
        _ceramic(ic, 124, 28, 108, "#FFFDF6", "#EDE6D6", "#C9BFA9", "#9C927E")
        ic.text("2", 136, 50, 13, font="sans-semibold", fill="#3A6B5E")
        ic.text("Mx", 206, 76, 26, font="sans-bold", anchor="middle", fill="#3A6B5E", opacity=0.9)
    # the tile in front, Element's green
    x, y, s = 40, 58, 148
    _ceramic(ic, x, y, s, "#6FF0C8", "#0DBD8B", "#077A59", "#05553E")
    # the glaze: a pool of light top left, a streak across
    ic.path(f"M{x + 6} {y + 50}C{x + 6} {y + 18} {x + 18} {y + 6} {x + 52} {y + 6}C{x + 30} {y + 14} {x + 16} "
            f"{y + 28} {x + 6} {y + 50}z", fill="#fff", opacity=0.55)
    ic.path(f"M{x + 20} {y + s - 10}L{x + s - 10} {y + 20}L{x + s - 10} {y + 40}L{x + 40} {y + s - 10}z",
            fill="#fff", opacity=0.07)
    ink, sh = "#F4FFFA", "#04503A"
    def say(t, tx, ty, size, font, anchor="start", spacing=0, op=1):
        ic.text(t, tx + 0.8, ty + 1.4, size, font=font, anchor=anchor, spacing=spacing, fill=sh, opacity=0.5 * op)
        ic.text(t, tx, ty, size, font=font, anchor=anchor, spacing=spacing, fill=ink, opacity=op)
    say("1", x + 14, y + 30, 22, "sans-semibold")
    say("1.008", x + s - 14, y + 26, 12, "mono-semibold", anchor="end", op=0.85)
    say("El", x + s / 2, y + 98, 72, "sans-bold", anchor="middle")
    say("Element", x + s / 2, y + 120, 16, "sans-semibold", anchor="middle")
    say("matrix", x + s / 2, y + 135, 10, "mono-semibold", anchor="middle", spacing=1, op=0.8)


@small("element-desktop")
def element16(ic):
    tile(ic, "#2B4A43", "#0F201C")
    ic.rect(8.4, 1.4, 6, 6, rx=1, fill="#E9E2D2", transform="rotate(10 11.4 4.4)")
    ic.rect(2.4, 4.6, 10, 10, rx=1.4, fill="#077A59")
    ic.rect(2, 4, 10, 10, rx=1.4, fill="#0DBD8B")
    ic.path("M4.2 7h3.2M4.2 9h2.6M4.2 11h3.2M4.4 6.6v4.8M9.4 6.6v4.8", stroke="#F4FFFA", stroke_width=1.1)


# --- Zoom: a webcam on its clip, the mark printed on it --------------------

@icon("zoom", kind="app", names=["zoom"], title="Zoom")
def zoom(ic):
    tile(ic, "#2F6FE4", "#103684")
    shadow(ic, 128, 210, 66, 10)
    # the clip it stands on
    ic.path("M120 132h16l4 40h-24z", fill=steel(ic))
    ic.rect(76, 176, 104, 30, rx=9, fill=graphite(ic))
    ic.rect(76.75, 176.75, 102.5, 28.5, rx=8.25, fill="none", stroke="#fff", stroke_opacity=0.14,
            stroke_width=1.5)
    ic.circle(128, 176, 11, fill=graphite(ic))
    ic.circle(128, 176, 4, fill=steel(ic, horizontal=False))
    ic.rect(86, 198, 84, 4, rx=2, fill="#000", opacity=0.35)
    # the body
    ic.rect(30, 52, 196, 90, rx=45, fill="#000", opacity=0.3, transform="translate(2 5)")
    ic.rect(30, 52, 196, 90, rx=45, fill=ic.lin([(0, "#FFFFFF"), (0.6, "#E3E8EF"), (1, "#AEB8C6")]))
    ic.path("M44 70a44 44 0 0 1 31-16.8h106", fill="none", stroke="#fff", stroke_width=2, stroke_linecap="round")
    ic.path("M226 97a45 45 0 0 1-45 45H75a45 45 0 0 1-38-21c30 12 110 14 189-24z", fill="#5B6B85",
            opacity=0.18)
    # the lens
    cx, cy = 128, 97
    ic.circle(cx, cy, 40, fill=ic.lin([(0, "#B9C2CE"), (1, "#7C8796")]))
    ic.circle(cx, cy, 35, fill=graphite(ic))
    ic.circle(cx, cy, 27, fill="#0B5CFF")
    ic.circle(cx, cy, 24, fill=ic.rad([(0, "#1B3E8C"), (0.55, "#0A1736"), (1, "#03060F")], cx=0.4, cy=0.4,
                                     r=0.7))
    ic.circle(cx, cy, 13, fill="none", stroke="#3A6FE0", stroke_opacity=0.5, stroke_width=1.5)
    ic.circle(cx, cy, 6, fill="#02040A")
    ic.circle(cx - 9, cy - 9, 5, fill="#fff", opacity=0.6)
    ic.circle(cx + 9, cy + 10, 2.2, fill="#9FC1FF", opacity=0.5)
    ic.path(f"M{cx - 24} {cy}a24 24 0 0 1 24-24v6a18 18 0 0 0-18 18z", fill="#fff", opacity=0.15)
    # the mark, printed at the left: a camera in a blue rounded square
    with ic.g(transform="translate(52 82)"):
        ic.rect(0, 0, 30, 30, rx=8, fill=ic.lin([(0, "#3D84FF"), (1, "#0B5CFF")]))
        ic.rect(5.5, 9.5, 13, 11, rx=2.6, fill="#fff")
        ic.path("M19.5 13.6 L25 10.2 V19.8 L19.5 16.4 Z", fill="#fff", stroke="#fff", stroke_width=1,
                stroke_linejoin="round")
    ic.text("zoom", 67, 128, 9, font="sans-bold", anchor="middle", fill="#0B5CFF")
    # the light and the microphones at the right
    ic.circle(190, 86, 4.5, fill="#0D2A1A")
    ic.circle(190, 86, 3, fill="#4DF08A")
    ic.circle(190, 86, 7, fill="#4DF08A", opacity=0.18)
    for k in range(4):
        ic.circle(182 + k * 5.4, 108, 1.4, fill="#59616D")


@small("zoom")
def zoom16(ic):
    tile(ic, "#2F6FE4", "#103684")
    ic.rect(7.2, 9, 1.6, 3.4, fill="#9AA1A9")
    ic.rect(5, 12, 6, 2, rx=0.8, fill="#2A2C30")
    ic.rect(1.8, 3.5, 12.4, 6.4, rx=3.2, fill="#F4F6F9")
    ic.circle(8, 6.7, 2.6, fill="#0B5CFF")
    ic.circle(8, 6.7, 1.5, fill="#081430")


# --- Mixin Messenger: a blue leather wallet, the mark stamped in foil ---------

def _mixin_mark(ic, cx, cy, k, fill, **kw):
    """Mixin's mark, redrawn: a hexagon between two slanted bars; k scales."""
    t = f"translate({cx} {cy}) scale({k})"
    ic.path("M-30 -24 L-19 -17 V17 L-30 24 Z M30 -24 L19 -17 V17 L30 24 Z", fill=fill, transform=t,
            stroke=fill, stroke_width=2.4, stroke_linejoin="round", **kw)
    hexd = "M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in (polar(0, 0, 11.5, a) for a in range(0, 360, 60))) + "Z"
    ic.path(hexd, fill=fill, transform=t, stroke=fill, stroke_width=2.4, stroke_linejoin="round", **kw)


@icon("mixin", kind="app", names=["mixin", "one.mixin.messenger"], title="Mixin Messenger")
def mixin(ic):
    tile(ic, "#3A4766", "#161D30")
    shadow(ic, 128, 210, 100, 12)
    # a card in it, and a note
    with ic.g(transform="rotate(-7 120 80)"):
        ic.rect(60, 40, 112, 70, rx=7, fill=ic.lin([(0, "#2AB0FA"), (1, "#2B5EE8")], 0, 0, 1, 1))
        ic.rect(74, 54, 18, 13, rx=2.5, fill=ic.lin([(0, "#F6DDA0"), (1, "#B8883A")]))
        ic.text("MIXIN", 160, 58, 9, font="mono-semibold", anchor="end", spacing=1.4, fill="#fff", opacity=0.85)
    with ic.g(transform="rotate(5 160 70)"):
        ic.rect(136, 36, 68, 58, rx=2, fill=paper(ic, "white"))
        ic.text("XIN  0.42", 144, 56, 8.5, font="mono-semibold", fill="#2B5EE8")
        ic.text("to Lin", 144, 72, 13, font="hand", fill="#55534E")
    # the wallet
    leather = ic.lin([(0, "#4FA6F8"), (0.5, "#2C71E6"), (1, "#1B45A8")], 0, 0, 1, 1)
    ic.rect(28, 76, 200, 128, rx=16, fill="#000", opacity=0.3, transform="translate(2 5)")
    ic.rect(28, 76, 200, 128, rx=16, fill=leather)
    ic.path("M44 78h168", stroke="#fff", stroke_opacity=0.35, stroke_width=2)
    # the pocket's mouth and stitching
    ic.rect(28, 76, 200, 12, rx=6, fill="#000", opacity=0.18)
    ic.rect(36, 90, 184, 106, rx=10, fill="none", stroke="#BFE0FF", stroke_opacity=0.65, stroke_width=1.4,
            stroke_dasharray="4 3")
    ic.path("M228 92v96a16 16 0 0 1-16 16H44c80-6 150-30 184-112z", fill="#0B2A70", opacity=0.22)
    # the strap and its snap
    strap = "M186 74h28v74a14 14 0 0 1-28 0z"
    ic.path(strap, fill="#000", opacity=0.3, transform="translate(1.5 3)")
    ic.path(strap, fill=ic.lin([(0, "#3F92F2"), (1, "#1D4CB4")], 0, 0, 1, 1))
    ic.path("M189 78v68a11 11 0 0 0 22 0V78", fill="none", stroke="#BFE0FF", stroke_opacity=0.6,
            stroke_width=1.2, stroke_dasharray="4 3")
    ic.circle(200, 146, 7, fill=steel(ic, horizontal=False))
    ic.circle(200, 146, 3.4, fill="none", stroke="#5D636B", stroke_width=1)
    ic.circle(198, 144, 1.6, fill="#fff", opacity=0.7)
    # the mark, stamped in silver foil: pressed in, lit at its lower edge
    _mixin_mark(ic, 128.8, 143.4, 1.25, "#0E2E7A", opacity=0.6)
    _mixin_mark(ic, 128, 142, 1.25, ic.lin([(0, "#FFFFFF"), (0.5, "#E1E9F5"), (1, "#AFC0DA")], 0, 0, 1, 1))
    ic.text("MESSENGER", 128, 186, 8, font="mono-semibold", anchor="middle", spacing=2.6, fill="#D6E6FF",
            opacity=0.75)


@small("mixin")
def mixin16(ic):
    tile(ic, "#3A4766", "#161D30")
    ic.rect(4, 2.6, 7, 4, rx=0.5, fill="#F4F6F9")
    ic.rect(1.8, 5, 12.4, 8.6, rx=1.4, fill="#2C71E6")
    ic.path("M4.4 7.2 L5.6 7.9 V11 L4.4 11.7Z M11.6 7.2 L10.4 7.9 V11 L11.6 11.7Z", fill="#fff")
    ic.path("M8 8.1 L9.3 8.85 V10.35 L8 11.1 L6.7 10.35 V8.85Z", fill="#fff")
