"""The soft drawings the style was fixed on (the artifact "Quieter Object
Icons"): Files, Mail, Terminal, Music, Calculator, Clock, and VLC and
Telegram for the theme. The same objects as drawings/, about half the
detail, no text."""

from lib import bar, mark, soft, soft_shadow, tile, two


@soft("Files")
def files(ic):
    tile(ic, "#557797", "#2C4660")
    soft_shadow(ic, 128, 212, 96, 13)
    ic.path("M40 82a12 12 0 0 1 12-12h38a12 12 0 0 1 9 4l8 10h97a12 12 0 0 1 12 12v100H40z", fill=two(ic, "#B58A45", "#9C7231"))
    with ic.g(transform="rotate(-5 128 130)"):
        ic.rect(62, 58, 132, 120, rx=8, fill=two(ic, "#FFFFFF", "#ECE8DF"))
        bar(ic, 80, 78, 70, fill="#557797")
        bar(ic, 80, 94, 96)
        bar(ic, 80, 110, 84)
    ic.path("M32 118a10 10 0 0 1 10-10h172a10 10 0 0 1 10 10l-8 82a12 12 0 0 1-12 11H52a12 12 0 0 1-12-11z",
            fill=two(ic, "#EDC67A", "#D9A957"))
    ic.rect(42, 108, 172, 4, rx=2, fill="#FFF1CC", opacity=0.8)
    ic.rect(150, 174, 50, 16, rx=4, fill="#FFF8E8")
    bar(ic, 158, 180, 30, 4, fill="#557797")


@soft("Mail")
def mail(ic):
    tile(ic, "#3D79A6", "#1F4467")
    soft_shadow(ic, 128, 210, 98, 12)
    ic.rect(30, 66, 196, 136, rx=14, fill=two(ic, "#F7F1E4", "#EAE1CE"))
    ic.path("M34 196 L116 136 a18 18 0 0 1 24 0 L222 196", fill="#EDE4D1")
    ic.path("M30 80a14 14 0 0 1 14-14h168a14 14 0 0 1 14 14 L140 146 a18 18 0 0 1-24 0z", fill=two(ic, "#FFFDF8", "#F3ECDD"))
    ic.rect(176, 80, 32, 38, rx=4, fill="#FFFDF7")
    ic.rect(181, 85, 22, 28, rx=2, fill="#2F6FB8")
    ic.circle(192, 96, 5, fill="#F2C45C")
    ic.circle(128, 148, 22, fill=ic.rad([(0, "#D04A35"), (1, "#9E2A1A")], cx=0.4, cy=0.35, r=0.7))
    mark(ic, 114, 134, 28, fill="#F7D9D2")


@soft("Term")
def term(ic):
    tile(ic, "#22282D", "#0B0E10")
    soft_shadow(ic, 128, 222, 70, 9)
    ic.path("M112 186h32l5 24h-42z", fill="#8D949C")
    ic.rect(84, 206, 88, 12, rx=6, fill=two(ic, "#AEB4BB", "#8D949C"))
    ic.rect(28, 40, 200, 150, rx=22, fill=two(ic, "#454B53", "#2E3338"))
    ic.rect(42, 54, 172, 122, rx=12, fill="#0C2416")
    ic.path("M60 86 L80 104 L60 122", fill="none", stroke="#7CF7A6", stroke_width=10, stroke_linecap="round", stroke_linejoin="round")
    ic.rect(92, 112, 30, 10, rx=3, fill="#7CF7A6")
    bar(ic, 60, 140, 96, 8, fill="#7CF7A6", opacity=0.3)
    bar(ic, 60, 156, 64, 8, fill="#7CF7A6", opacity=0.3)


@soft("Music")
def music(ic):
    tile(ic, "#7A4C8E", "#3D2150")
    soft_shadow(ic, 128, 214, 100, 12)
    ic.circle(160, 120, 84, fill=two(ic, "#26262A", "#121214"))
    for r in (50, 64, 76):
        ic.circle(160, 120, r, fill="none", stroke="#fff", stroke_opacity=0.1, stroke_width=2)
    ic.circle(160, 120, 26, fill=two(ic, "#F2C25E", "#D99B35"))
    ic.circle(160, 120, 4, fill="#121214")
    ic.rect(28, 38, 150, 160, rx=10, fill=two(ic, "#F7F2E7", "#E2DACA"))
    ic.circle(92, 104, 44, fill="none", stroke="#2F6FB8", stroke_width=12)
    ic.circle(92, 104, 24, fill="none", stroke="#E07A3F", stroke_width=12)
    ic.circle(92, 104, 8, fill="#1E1E20")
    bar(ic, 44, 166, 80, 9, fill="#1E1E20")
    bar(ic, 44, 182, 48, 6, fill="#A49E91")


@soft("Calculator")
def calculator(ic):
    tile(ic, "#C27236", "#7A3C14")
    soft_shadow(ic, 128, 226, 74, 9)
    ic.rect(62, 28, 132, 198, rx=22, fill=two(ic, "#3F4349", "#2A2C31"))
    ic.rect(74, 42, 108, 44, rx=8, fill=two(ic, "#C9D5B2", "#B4C29C"))
    for x in (128, 146, 164):
        ic.rect(x, 54, 12, 20, rx=3, fill="#2B3324", opacity=0.75)
    for r, y in enumerate((98, 123, 148, 173, 198)):
        for c, x in enumerate((74, 102, 130, 158)):
            if r == 4 and c == 2:
                continue
            w = 50 if (r == 4 and c == 1) else 22
            ic.rect(x, y, w, 19, rx=6, fill="#F29A3C" if c == 3 else "#6A6F78")


@soft("Clock")
def clock(ic):
    tile(ic, "#2E4468", "#141F35")
    soft_shadow(ic, 128, 222, 88, 11)
    ic.circle(128, 124, 96, fill=two(ic, "#E2B45E", "#B88433"))
    ic.circle(128, 124, 82, fill=two(ic, "#FFFDF7", "#F1EADB"))
    for h in range(12):
        big = h % 3 == 0
        ic.rect(124 if big else 125.5, 50, 8 if big else 5, 18 if big else 10, rx=2.5,
                fill="#2A2C30", transform=f"rotate({h * 30} 128 124)")
    ic.rect(122.5, 80, 11, 50, rx=5.5, fill="#2A2C30", transform="rotate(-60 128 124)")
    ic.rect(123.5, 58, 9, 72, rx=4.5, fill="#2A2C30", transform="rotate(60 128 124)")
    with ic.g(transform="rotate(196 128 124)"):
        ic.rect(126.5, 56, 3, 84, rx=1.5, fill="#D23B2F")
    ic.circle(128, 124, 8, fill="#D23B2F")


@soft("vlc")
def vlc(ic):
    tile(ic, "#E8862B", "#B5541A")
    soft_shadow(ic, 128, 214, 90, 12)
    ic.rect(44, 186, 168, 26, rx=10, fill=two(ic, "#F59A34", "#D9741A"))
    ic.path("M112 36h32l52 156H60z", fill=two(ic, "#FF9A2E", "#F07F14"))
    ic.path("M100 74h56l12 36H88z", fill="#FFFFFF")
    ic.path("M82 128h92l12 36H70z", fill="#FFFFFF")


@soft("telegram")
def telegram(ic):
    tile(ic, "#3BA3DC", "#1E6FA8")
    soft_shadow(ic, 122, 206, 80, 10)
    ic.path("M36 120 L214 52 L178 190 L128 160 Z", fill=two(ic, "#FFFFFF", "#E8F2F9"))
    ic.path("M128 160 L214 52 L104 150 L110 192 Z", fill="#CFE1EE")
    ic.path("M104 150 L110 192 L134 166 Z", fill="#A9C6DB")
