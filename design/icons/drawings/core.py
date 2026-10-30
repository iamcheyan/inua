"""The six studies the style was fixed on: Files, Mail, Terminal, Music,
Calculator, Clock (the artifact "Inua Desk Icons")."""

from lib import (brass, glare, graphite, icon, mark, paper, polar, shadow, small, steel, tile, wax)


# --- Files: a manila folder, papers in it ------------------------------------

@icon("Files")
def files(ic):
    tile(ic, "#557797", "#2C4660")
    shadow(ic, 128, 212, 96, 13)
    ic.path("M40 80a10 10 0 0 1 10-10h42a10 10 0 0 1 8 4l8 10h98a10 10 0 0 1 10 10v104a8 8 0 0 1-8 8H48a8 8 0 0 1-8-8z",
            fill=paper(ic, "kraft-dark"))
    ic.path("M50 72h40a8 8 0 0 1 6 3", stroke="#E8C682", stroke_width=1.5, fill="none", opacity=0.7)
    with ic.g(transform="rotate(-6 128 130)"):
        ic.rect(60, 56, 132, 124, rx=4, fill=paper(ic, "white"))
        ic.text("Itinerary", 74, 76, 9, font="sans-semibold", fill="#6A665D")
        ic.text("Nov 2 · 07:12 Nozomi 9", 74, 88, 6.2, font="mono", fill="#8C887F")
        ic.text("Kyoto  09:26 · car 7", 74, 97, 6.2, font="mono", fill="#8C887F")
    with ic.g(transform="rotate(4 128 130)"):
        ic.rect(68, 64, 128, 120, rx=4, fill="#FFFFFF", stroke="#000", stroke_opacity=0.06)
        ic.text("Field notes", 82, 84, 11, font="sans-semibold", fill="#2C4660")
        ic.text("Oct 30 · Hokkaido", 82, 95, 6.2, font="mono", fill="#8C887F")
        ic.text("The ridge path opens onto", 82, 106, 7, fill="#4E4C47")
        ic.text("the lake by noon; the fog", 82, 115, 7, fill="#4E4C47")
    ic.path("M32 116a8 8 0 0 1 8-8h176a8 8 0 0 1 8 8l-9 88a10 10 0 0 1-10 9H51a10 10 0 0 1-10-9z",
            fill=ic.lin([(0, "#F3D493"), (0.5, "#E3BA6C"), (1, "#C69447")]))
    ic.line(40, 109.2, 216, 109.2, stroke="#FFF4D8", stroke_width=2, stroke_linecap="round", opacity=0.85)
    ic.line(44, 205, 212, 205, stroke="#7C5520", stroke_opacity=0.35, stroke_width=2)
    ic.rect(150, 176, 52, 18, rx=3, fill="#FCF7EA", opacity=0.92)
    ic.text("Trips 2026", 176, 190, 14, font="hand", anchor="middle", fill="#3B4A63")


@small("Files")
def files16(ic):
    tile(ic, "#557797", "#2C4660")
    ic.path("M2.5 5a1 1 0 0 1 1-1h3l1 1h5a1 1 0 0 1 1 1v6.5h-11z", fill="#B98A42")
    ic.rect(4, 4.5, 8, 6, fill="#FFFFFF")
    ic.path("M2 7.5a.8.8 0 0 1 .8-.8h10.4a.8.8 0 0 1 .8.8l-.6 5a.8.8 0 0 1-.8.7H3.4a.8.8 0 0 1-.8-.7z", fill="#EBC77C")


# --- Mail: an envelope, sealed in wax with inua's mark, and a stamp ----------

@icon("Mail")
def mail(ic):
    tile(ic, "#3D79A6", "#1F4467")
    shadow(ic, 128, 210, 98, 12)
    ic.rect(30, 66, 196, 136, rx=10, fill=paper(ic, "cream"))
    ic.path("M32 196 L116 132 a18 18 0 0 1 24 0 L224 196", fill="#F1EADB", stroke="#000", stroke_opacity=0.07)
    ic.line(32, 72, 104, 138, stroke="#000", stroke_opacity=0.08, stroke_width=1.5)
    ic.line(224, 72, 152, 138, stroke="#000", stroke_opacity=0.08, stroke_width=1.5)
    ic.path("M34 79 L118 151 a16 16 0 0 0 20 0 L222 79", fill="#000", opacity=0.10)
    ic.path("M30 76a10 10 0 0 1 10-10h176a10 10 0 0 1 10 10 L138 146 a16 16 0 0 1-20 0z",
            fill=ic.lin([(0, "#FFFDF8"), (1, "#ECE4D3")]))
    ic.line(40, 67.5, 216, 67.5, stroke="#fff", stroke_width=2, opacity=0.9)
    with ic.g(transform="translate(176 80)"):
        ic.rect(0, 0, 34, 40, rx=2, fill="#FFFDF7", stroke="#C9BFA9", stroke_dasharray="2 2")
        ic.rect(5, 5, 24, 30, fill="#2463AE")
        ic.path("M8 28 l7-10 5 6 4-5 5 9z", fill="#F2F5F8", opacity=0.9)
        ic.circle(22, 12, 3, fill="#F2C45C")
    ic.path("M128 124c13 0 25 8 24 22 2 6-4 9-2 15-3 9-14 14-23 13-11 2-22-6-24-16-4-5 1-12-1-17 4-10 14-17 26-17z",
            fill=wax(ic))
    ic.circle(128, 148, 17, fill="#A9301F")
    ic.circle(128, 148, 17, fill="none", stroke="#5A140B", stroke_opacity=0.6, stroke_width=2)
    ic.circle(127.3, 147.3, 17, fill="none", stroke="#FF9A84", stroke_opacity=0.3, stroke_width=1)
    mark(ic, 114.6, 134.6, 28, fill="#5E150B", opacity=0.75)
    mark(ic, 113.4, 133.4, 28, fill="#F59A86", opacity=0.55)
    mark(ic, 114, 134, 28, fill="#B53523")
    ic.ellipse(121, 133, 7, 3.5, fill="#fff", opacity=0.28, transform="rotate(-25 121 133)")


@small("Mail")
def mail16(ic):
    tile(ic, "#3D79A6", "#1F4467")
    ic.rect(2, 4, 12, 8.5, rx=1, fill="#F6F1E6")
    ic.path("M2.3 4.6 L8 9 L13.7 4.6", fill="none", stroke="#C9BFA9", stroke_width=0.9)
    ic.circle(8, 9, 1.8, fill="#B53523")


# --- Terminal: a black-glass screen on a stand, a test run on it -------------

@icon("Term")
def term(ic):
    tile(ic, "#22282D", "#0B0E10")
    shadow(ic, 128, 222, 70, 9)
    ic.path("M112 186h32l6 26h-44z", fill=steel(ic))
    ic.rect(86, 208, 84, 10, rx=5, fill=steel(ic))
    ic.rect(28, 40, 200, 150, rx=18, fill=ic.lin([(0, "#4A5058"), (0.08, "#30353B"), (1, "#16191C")]))
    ic.rect(28.75, 40.75, 198.5, 148.5, rx=17.25, fill="none", stroke="#fff", stroke_opacity=0.12, stroke_width=1.5)
    ic.rect(40, 52, 176, 122, rx=9, fill=ic.rad([(0, "#103A22"), (1, "#050B08")], cx=0.35, cy=0.4, r=0.8))
    dim = dict(font="mono-semibold", fill="#4FBF78", opacity=0.6)
    ic.text("~/inua $ go test ./...", 50, 72, 10, **dim)
    ic.text("ok   internal/ui     0.04s", 50, 86, 10, **dim)
    ic.text("ok   internal/shell  0.07s", 50, 100, 10, **dim)
    ic.text("PASS · 412 tests", 50, 114, 10, font="mono-semibold", fill="#F2C45C", opacity=0.75)
    ic.path("M53 133 L62 141.5 L53 150", fill="none", stroke="#7CF7A6", stroke_width=3.2, stroke_linecap="round", stroke_linejoin="round")
    ic.rect(70, 133, 10, 17, fill="#7CF7A6")
    scan = ic.define('<pattern id="{id}" width="4" height="3" patternUnits="userSpaceOnUse">'
                     '<rect width="4" height="1" fill="#000" opacity=".35"/></pattern>', "p")
    ic.rect(40, 52, 176, 122, rx=9, fill=f"url(#{scan})", opacity=0.5)
    ic.path("M40 61a9 9 0 0 1 9-9h86L64 174H49a9 9 0 0 1-9-9z", fill=glare(ic))
    ic.circle(128, 182, 2.2, fill="#7CF7A6", opacity=0.7)


@small("Term")
def term16(ic):
    tile(ic, "#22282D", "#0B0E10")
    ic.rect(2, 3, 12, 9, rx=1.5, fill="#3A4047")
    ic.rect(3, 4, 10, 7, rx=0.8, fill="#07150D")
    ic.path("M4.5 6 L6.5 7.5 L4.5 9", fill="none", stroke="#7CF7A6", stroke_width=1.1, stroke_linecap="round", stroke_linejoin="round")
    ic.rect(7.5, 8.3, 3, 1, fill="#7CF7A6")
    ic.rect(5.5, 12.5, 5, 1.2, rx=0.6, fill="#9AA1A9")


# --- Music: a record slid out of its sleeve -----------------------------------

@icon("Music")
def music(ic):
    tile(ic, "#7A4C8E", "#3D2150")
    shadow(ic, 128, 214, 100, 12)
    ic.circle(160, 120, 84, fill=ic.rad([(0, "#2A2A2E"), (0.7, "#141416"), (1, "#0A0A0B")]))
    for r in range(42, 80, 6):
        ic.circle(160, 120, r, fill="none", stroke="#fff", stroke_opacity=0.06)
    sheen = ic.lin([(0, "#fff", 0), (0.5, "#fff", 0.22), (1, "#fff", 0)], 0, 0, 1, 1)
    ic.path("M160 120 L222 62 A84 84 0 0 1 238 96 Z", fill=sheen)
    ic.path("M160 120 L98 178 A84 84 0 0 1 82 144 Z", fill=sheen, opacity=0.7)
    ic.circle(160, 120, 28, fill=ic.rad([(0, "#F6CB6A"), (1, "#C98E2A")], cx=0.4, cy=0.35, r=0.7))
    ic.circle(160, 120, 21, fill="none", stroke="#8A5A12", stroke_opacity=0.35)
    ic.text("INUA", 160, 111, 6, font="mono-semibold", anchor="middle", spacing=1, fill="#6B4510")
    ic.text("33⅓", 160, 135, 5.5, font="mono", anchor="middle", fill="#6B4510")
    ic.circle(160, 120, 3.5, fill="#0A0A0B")
    ic.rect(32, 41, 150, 160, rx=5, fill="#000", opacity=0.35)
    ic.rect(28, 38, 150, 160, rx=5, fill=ic.lin([(0, "#F7F2E7"), (1, "#D8D0BF")], 0, 0, 1, 1))
    ic.circle(92, 104, 44, fill="none", stroke="#2463AE", stroke_width=10)
    ic.circle(92, 104, 26, fill="none", stroke="#E07A3F", stroke_width=10)
    ic.circle(92, 104, 9, fill="#1E1E20")
    ic.text("Small Hours", 44, 173, 12, font="sans-semibold", fill="#1E1E20")
    ic.text("SIDE A · 33⅓ RPM", 44, 185, 6.5, font="mono", spacing=0.6, fill="#55534E")
    ic.line(178, 46, 178, 190, stroke="#000", stroke_opacity=0.12, stroke_width=2)


@small("Music")
def music16(ic):
    tile(ic, "#7A4C8E", "#3D2150")
    ic.circle(10, 8, 5.2, fill="#141416")
    ic.circle(10, 8, 1.8, fill="#E2B04A")
    ic.rect(2.5, 3, 7, 10, rx=0.6, fill="#F2ECDF")
    ic.circle(6, 7, 2.2, fill="none", stroke="#2463AE", stroke_width=1.1)


# --- Calculator: a pocket calculator ----------------------------------------

@icon("Calculator")
def calculator(ic):
    tile(ic, "#C27236", "#7A3C14")
    shadow(ic, 128, 226, 74, 9)
    ic.rect(62, 28, 132, 198, rx=18, fill=graphite(ic))
    ic.rect(62.75, 28.75, 130.5, 196.5, rx=17.25, fill="none", stroke="#fff", stroke_opacity=0.14, stroke_width=1.5)
    ic.rect(72, 40, 112, 48, rx=6, fill="#141517")
    ic.rect(76, 44, 104, 40, rx=3, fill=ic.lin([(0, "#C9D5B2"), (1, "#A6B58E")]))
    ic.text("88888", 174, 74, 24, font="mono-semibold", anchor="end", fill="#2B3324", opacity=0.07)
    ic.text("1,024", 174, 74, 24, font="mono-semibold", anchor="end", fill="#2B3324")
    ic.path("M76 47a3 3 0 0 1 3-3h101L160 84H79a3 3 0 0 1-3-3z", fill="#fff", opacity=0.12)
    key = ic.lin([(0, "#6A6F78"), (1, "#3E4248")])
    op = ic.lin([(0, "#F7B05A"), (1, "#D47A24")])
    legends = [["C", "±", "%", "÷"], ["7", "8", "9", "×"], ["4", "5", "6", "−"], ["1", "2", "3", "+"], ["0", ".", "", "="]]
    for r, y in enumerate((100, 124, 148, 172, 196)):
        for c, x in enumerate((74, 102, 130, 158)):
            orange = c == 3
            ic.rect(x, y + 2, 22, 18, rx=4, fill="#7A3E0C" if orange else "#1A1B1E")
            ic.rect(x, y, 22, 18, rx=4, fill=op if orange else key)
            ic.rect(x + 3, y + 1.2, 16, 1.2, rx=0.6, fill="#fff", opacity=0.4 if orange else 0.25)
            if legends[r][c]:
                ic.text(legends[r][c], x + 11, y + 13, 10, font="sans-semibold", anchor="middle", fill="#F1F1EF")
    # ⌫, which the font has not: a key with a cross
    ic.path("M136 205 l3-4h11v8h-11z", fill="none", stroke="#F1F1EF", stroke_width=1.3, stroke_linejoin="round")
    ic.path("M142 203.2 l3.5 3.6 M145.5 203.2 l-3.5 3.6", stroke="#F1F1EF", stroke_width=1.2, stroke_linecap="round")


@small("Calculator")
def calculator16(ic):
    tile(ic, "#C27236", "#7A3C14")
    ic.rect(4, 2, 8, 12, rx=1.2, fill="#2A2C30")
    ic.rect(5, 3, 6, 2.5, rx=0.4, fill="#B9C7A5")
    for y in (7, 9, 11):
        for x in (5, 7.25, 9.5):
            ic.rect(x, y, 1.5, 1.2, rx=0.2, fill="#F2A24A" if x == 9.5 else "#8A8F97")


# --- Clock: a brass clock at ten past ten -----------------------------------

@icon("Clock")
def clock(ic):
    tile(ic, "#2E4468", "#141F35")
    shadow(ic, 128, 222, 88, 11)
    ic.circle(128, 124, 98, fill=brass(ic))
    ic.circle(128, 124, 89, fill=brass(ic, 1, 1, 0, 0))
    ic.circle(128, 124, 83, fill=ic.rad([(0, "#FFFDF7"), (1, "#E8E0CE")], cx=0.45, cy=0.4, r=0.65))
    ic.circle(128, 124, 83, fill="none", stroke="#000", stroke_opacity=0.18, stroke_width=2)
    ic.circle(128, 124, 78.5, fill="none", stroke="#2A2C30", stroke_width=4, stroke_dasharray="0.9 7.32",
              stroke_dashoffset=0.45, transform="rotate(-90 128 124)", opacity=0.7)
    for h in range(12):
        if h % 3 == 0:
            ic.rect(125.5, 47, 5, 15, rx=1.5, fill="#2A2C30", transform=f"rotate({h * 30} 128 124)")
        else:
            ic.rect(126.5, 47, 3, 10, rx=1, fill="#2A2C30", transform=f"rotate({h * 30} 128 124)")
    for n, deg in (("12", 0), ("3", 90), ("6", 180), ("9", 270)):
        x, y = polar(128, 124, 52, deg)
        ic.text(n, x, y + 5, 15, font="sans-medium", anchor="middle", fill="#2A2C30")
    ic.text("INUA", 128, 154, 7.5, font="mono-semibold", anchor="middle", spacing=2.4, fill="#6A665D")
    ic.text("QUARTZ", 128, 163, 5, font="mono", anchor="middle", spacing=1, fill="#8C887F")
    with ic.g(transform="translate(2 3)", opacity=0.18, fill="#000"):
        ic.rect(124.5, 78, 7, 50, rx=3.5, transform="rotate(-60 128 124)")
        ic.rect(125.5, 56, 5, 72, rx=2.5, transform="rotate(60 128 124)")
    ic.rect(124.5, 78, 7, 50, rx=3.5, fill="#23262B", transform="rotate(-60 128 124)")
    ic.rect(125.5, 56, 5, 72, rx=2.5, fill="#23262B", transform="rotate(60 128 124)")
    with ic.g(transform="rotate(196 128 124)"):
        ic.rect(127, 52, 2, 88, rx=1, fill="#C8372D")
        ic.circle(128, 136, 5, fill="#C8372D")
    ic.circle(128, 124, 7, fill=brass(ic))
    ic.circle(128, 124, 2.2, fill="#3A2A10")
    ic.path("M60 96a72 72 0 0 1 88-50 84 84 0 0 0-88 50z", fill="#fff", opacity=0.55)


@small("Clock")
def clock16(ic):
    tile(ic, "#2E4468", "#141F35")
    ic.circle(8, 8, 6, fill="#C99645")
    ic.circle(8, 8, 4.9, fill="#FBF7EC")
    ic.path("M8 8 L5.6 6.6 M8 8 L10.6 5.4", stroke="#23262B", stroke_width=1, stroke_linecap="round")
