"""The inua-objects theme, code editors: VS Code, VSCodium, Sublime Text,
Zed, Cursor, the JetBrains IDEs and Android Studio
(docs/feat/object-icons.md, Part 2).

The family: the JetBrains IDEs are hardcover notebooks in their products'
gradients with the black two-letter badge on the cover and a card of code
in them; VS Code and VSCodium are their folded marks as enamel pins on a
page of code; Sublime an orange S inlaid in a slate; Zed a keycap; Cursor
its cube; Android Studio a drafting compass on a blueprint."""

from lib import glare, graphite, icon, paper, shadow, small, steel, tile


def _pts(pts, dx=0, dy=0, k=1.0):
    return [(dx + x * k, dy + y * k) for x, y in pts]


# --- the JetBrains IDEs: hardcover notebooks ---------------------------------

def _notebook(ic, abbr, name, stops, ground, code, card="#FFFDF7"):
    """A closed hardcover notebook, a card of code slipped in at the top,
    the cover in the product's gradient and its black badge."""
    tile(ic, *ground)
    shadow(ic, 130, 214, 92, 12)
    with ic.g(transform="rotate(-4 128 128)"):
        # the card of code, standing out of the pages
        with ic.g(transform="rotate(7 150 60)"):
            ic.rect(100, 8, 100, 70, rx=3, fill="#000", opacity=0.18, transform="translate(2 2)")
            ic.rect(100, 8, 100, 70, rx=3, fill=card)
            ic.rect(100, 8, 100, 6, rx=3, fill=stops[0][1])
            for i in range(3):
                ic.line(100, 37.5 + i * 9.5, 200, 37.5 + i * 9.5, stroke="#7FA7D9", stroke_opacity=0.35,
                        stroke_width=0.6)
            for i, (s, col) in enumerate(code):
                ic.text(s, 106, 25 + i * 9.5, 7.6, font="mono-semibold", fill=col)
        # the back board and the page block
        ic.rect(52, 42, 152, 172, rx=9, fill="#15161A")
        ic.rect(50, 38, 150, 170, rx=6, fill=paper(ic, "cream"))
        for i in range(5):
            ic.line(58, 203 - i * 2.2, 196, 203 - i * 2.2, stroke="#B7AD98", stroke_width=0.6)
            ic.line(195 - i * 2.2, 46, 195 - i * 2.2, 202, stroke="#B7AD98", stroke_width=0.6)
        # the cover
        ic.rect(44, 34, 150, 170, rx=9, fill=ic.lin(stops, 0, 0, 1, 1))
        ic.rect(44, 34, 150, 170, rx=9, fill=ic.lin([(0, "#fff", 0.26), (0.45, "#fff", 0.05), (1, "#000", 0.22)],
                                                     0, 0, 1, 1))
        # the spine's hinge
        ic.rect(44, 34, 18, 170, rx=9, fill="#000", opacity=0.16)
        ic.line(62.5, 36, 62.5, 202, stroke="#000", stroke_opacity=0.28, stroke_width=1.5)
        ic.line(64.5, 36, 64.5, 202, stroke="#fff", stroke_opacity=0.25, stroke_width=1)
        ic.rect(44.75, 34.75, 148.5, 168.5, rx=8.25, fill="none", stroke="#fff", stroke_opacity=0.3,
                stroke_width=1.5)
        # the product's name, blind-stamped at the top
        ic.text(name, 78, 58, 9, font="sans-semibold", spacing=1.6, fill="#000", opacity=0.22,
                transform="translate(0.6 0.8)")
        ic.text(name, 78, 58, 9, font="sans-semibold", spacing=1.6, fill="#fff", opacity=0.85)
        # the badge: a black square, two letters and a bar
        ic.rect(80, 122, 66, 66, fill="#000", opacity=0.25, transform="translate(2 3)")
        ic.rect(80, 122, 66, 66, fill="#000")
        ic.rect(80.5, 122.5, 65, 65, fill="none", stroke="#fff", stroke_opacity=0.12)
        ic.text(abbr, 87, 152, 25, font="sans-bold", spacing=-0.5, fill="#fff")
        ic.rect(87, 172, 26, 4.5, fill="#fff")
        # the elastic band, round the cover's edge
        ic.rect(172, 32, 8, 174, rx=1.5, fill="#000", opacity=0.25, transform="translate(1.5 1)")
        ic.rect(172, 32, 8, 174, rx=1.5, fill=ic.lin([(0, "#3A3C42"), (0.5, "#1B1C20"), (1, "#0C0C0E")],
                                                    0, 0, 1, 0))
        ic.line(174, 34, 174, 204, stroke="#fff", stroke_opacity=0.18, stroke_width=1)
        # the ribbon marker, out at the foot
        ic.path("M150 206v18l5-4 5 4v-18z", fill=stops[-1][1])
        ic.path("M150 206v18l5-4 5 4v-18z", fill="#000", opacity=0.2)


def _notebook16(ic, ground, stops, abbr_color="#fff"):
    tile(ic, *ground)
    ic.rect(3.6, 2.6, 9.6, 11.4, rx=1, fill="#F2ECDF")
    ic.rect(2.8, 2, 9.6, 11.4, rx=1, fill=ic.lin(stops, 0, 0, 1, 1))
    ic.rect(4.8, 7.4, 5, 5, fill="#000")
    ic.rect(5.6, 10.6, 2.2, 0.8, fill=abbr_color)
    ic.rect(10.6, 2, 0.8, 11.4, fill="#16171A")


IDEA = [(0, "#FC801D"), (0.45, "#FE2857"), (1, "#7B3BF0")]


@icon("intellij-idea", kind="app", title="IntelliJ IDEA",
      names=["com.jetbrains.IntelliJ-IDEA-Community", "com.jetbrains.IntelliJ-IDEA-Ultimate", "idea",
             "idea-community", "idea-ultimate", "intellij", "intellij-idea", "intellij-idea-ce",
             "intellij-idea-community", "intellij-idea-ue-bundled-jre", "intellij-idea-ultimate",
             "intellij-idea-ultimate-edition", "intellij_idea"])
def intellij(ic):
    _notebook(ic, "IJ", "INTELLIJ IDEA", IDEA, ("#4A3270", "#22143A"),
              [("class App {", "#0033B3"), ("  void run() {", "#3A3A40"), ("    go();", "#871094")])


@small("intellij-idea")
def intellij16(ic):
    _notebook16(ic, ("#4A3270", "#22143A"), IDEA)


PYCHARM = [(0, "#FCF84A"), (0.5, "#21D789"), (1, "#07A3D2")]


@icon("pycharm", kind="app", title="PyCharm",
      names=["com.jetbrains.PyCharm-Community", "com.jetbrains.PyCharm-Professional", "pycharm",
             "pycharm-community", "pycharm-education", "pycharm-professional"])
def pycharm(ic):
    _notebook(ic, "PC", "PYCHARM", PYCHARM, ("#1F6050", "#0C2E26"),
              [("def main():", "#0033B3"), ("  print(\"hi\")", "#3A3A40"), ("main()", "#067D17")])


@small("pycharm")
def pycharm16(ic):
    _notebook16(ic, ("#1F6050", "#0C2E26"), PYCHARM)


GOLAND = [(0, "#3BEA62"), (0.5, "#0D7BF7"), (1, "#8F4AF7")]


@icon("goland", kind="app", title="GoLand", names=["com.jetbrains.GoLand", "goland"])
def goland(ic):
    _notebook(ic, "GO", "GOLAND", GOLAND, ("#2B4C8C", "#121F45"),
              [("func main() {", "#0033B3"), ("  fmt.Println(", "#3A3A40"), ("    \"hello\")", "#067D17")])


@small("goland")
def goland16(ic):
    _notebook16(ic, ("#2B4C8C", "#121F45"), GOLAND)


WEBSTORM = [(0, "#FCF84A"), (0.45, "#07C3F2"), (1, "#087CFA")]


@icon("webstorm", kind="app", title="WebStorm", names=["com.jetbrains.WebStorm", "webstorm"])
def webstorm(ic):
    _notebook(ic, "WS", "WEBSTORM", WEBSTORM, ("#1A5E86", "#0A2C46"),
              [("const app =", "#0033B3"), ("  express();", "#3A3A40"), ("app.listen(80);", "#1750EB")])


@small("webstorm")
def webstorm16(ic):
    _notebook16(ic, ("#1A5E86", "#0A2C46"), WEBSTORM)


DATAGRIP = [(0, "#22D88F"), (0.5, "#9775F8"), (1, "#FF45ED")]


@icon("datagrip", kind="app", title="DataGrip", names=["com.jetbrains.DataGrip", "datagrip", "jetbrains-datagrip"])
def datagrip(ic):
    _notebook(ic, "DG", "DATAGRIP", DATAGRIP, ("#3E3478", "#1A1540"),
              [("SELECT id, name", "#0033B3"), ("FROM users", "#0033B3"), ("WHERE age > 30;", "#3A3A40")])


@small("datagrip")
def datagrip16(ic):
    _notebook16(ic, ("#3E3478", "#1A1540"), DATAGRIP)


# --- VS Code and VSCodium: their folded marks as enamel pins on a page --------

def _page(ic, lines, title):
    """A sheet of code, lying a little turned on the desk."""
    with ic.g(transform="rotate(-6 120 124)"):
        ic.rect(38, 40, 150, 172, rx=4, fill="#000", opacity=0.2, transform="translate(2 3)")
        ic.rect(38, 40, 150, 172, rx=4, fill=paper(ic, "white"))
        ic.text(title, 50, 60, 8.5, font="sans-semibold", fill="#3A3F4A")
        ic.line(50, 67, 176, 67, stroke="#000", stroke_opacity=0.1)
        for i, (s, col) in enumerate(lines):
            ic.text(f"{i + 1}", 56, 82 + i * 11, 6.5, font="mono", anchor="end", fill="#A9A59B")
            ic.text(s, 62, 82 + i * 11, 7.2, font="mono-semibold", fill=col)


# the VS Code mark, simplified, on a 100 grid: the strip behind, the strip in
# front, the panel on the right
VS_BACK = [(66, 2), (78, 12), (14, 74), (4, 66)]
VS_FRONT = [(66, 98), (78, 88), (14, 26), (4, 34)]
VS_PANEL = [(70, 4), (98, 16), (98, 84), (70, 96), (74, 74), (74, 26)]


def _vs_pin(ic, x, y, k, tones, rim="#0B3B6A"):
    """The folded mark as a thick enamel pin, its top left at (x, y), k px
    a unit; tones: back strip, front strip, panel (light, dark)."""
    back, front, (pl, pd) = tones
    for dx, dy, col, op in ((3, 5, "#000", 0.3), (1.6, 2.6, rim, 1)):
        for shape in (VS_BACK, VS_FRONT, VS_PANEL):
            ic.poly(_pts(shape, x + dx, y + dy, k), fill=col, opacity=op, stroke=col, stroke_width=3,
                    stroke_linejoin="round")
    ic.poly(_pts(VS_BACK, x, y, k), fill=back, stroke=back, stroke_width=2, stroke_linejoin="round")
    ic.poly(_pts(VS_FRONT, x, y, k), fill=front, stroke=front, stroke_width=2, stroke_linejoin="round")
    # the fold's shade where the front strip meets the panel
    ic.poly(_pts([(70, 26), (74, 26), (74, 74), (70, 96), (66, 98), (64, 92)], x, y, k), fill="#000", opacity=0.18)
    ic.poly(_pts(VS_PANEL, x, y, k), fill=ic.lin([(0, pl), (1, pd)], 0, 0, 0.6, 1), stroke=pl, stroke_width=2,
            stroke_linejoin="round")
    # the enamel's gloss
    ic.poly(_pts([(72, 7), (95, 18), (95, 40), (74, 34)], x, y, k), fill="#fff", opacity=0.22)
    ic.poly(_pts([(16, 27), (66, 75), (70, 72), (22, 25)], x, y, k), fill="#fff", opacity=0.18)


@icon("code", kind="app", title="Visual Studio Code",
      names=["code", "com.visualstudio.code", "visual-studio-code", "vscode"])
def vscode(ic):
    tile(ic, "#2A6FB0", "#0F3A66")
    shadow(ic, 132, 214, 96, 12)
    kw, ty, st, fn = "#AF00DB", "#267F99", "#A31515", "#795E26"
    _page(ic, [("import * as vs", kw), ("  from \"vscode\";", st), ("", kw),
               ("export function", kw), ("  activate() {", fn), ("  vs.window", ty),
               ("    .show(\"hi\");", st), ("}", "#3A3F4A")], "extension.ts")
    shadow(ic, 168, 196, 64, 10, 0.8)
    _vs_pin(ic, 98, 70, 1.16, ("#0B5DA8", "#1180D8", ("#3DB0FF", "#0B6CC0")))


@small("code")
def vscode16(ic):
    tile(ic, "#2A6FB0", "#0F3A66")
    ic.rect(1.5, 2, 7, 10, rx=0.6, fill="#F6F4EF")
    k, x, y = 0.12, 3.6, 3.2
    ic.poly(_pts(VS_BACK, x, y, k), fill="#0B5DA8")
    ic.poly(_pts(VS_FRONT, x, y, k), fill="#1180D8")
    ic.poly(_pts(VS_PANEL, x, y, k), fill="#3DB0FF")


@icon("vscodium", kind="app", title="VSCodium", names=["com.vscodium.codium", "vscodium"])
def vscodium(ic):
    tile(ic, "#2E8C9E", "#124652")
    shadow(ic, 132, 214, 96, 12)
    kw, st = "#0451A5", "#A31515"
    _page(ic, [("{", "#3A3F4A"), (" \"telemetry", kw), ("  .telemetryLevel\":", kw), ("    \"off\",", st),
               (" \"update.mode\":", kw), ("    \"manual\"", st), ("}", "#3A3F4A")], "settings.json")
    shadow(ic, 168, 196, 64, 10, 0.8)
    _vs_pin(ic, 98, 70, 1.16, ("#2C7FB8", "#5FB4E8", ("#B4E7FF", "#4BA6DC")), rim="#1B4F70")


@small("vscodium")
def vscodium16(ic):
    tile(ic, "#2E8C9E", "#124652")
    ic.rect(1.5, 2, 7, 10, rx=0.6, fill="#F6F4EF")
    k, x, y = 0.12, 3.6, 3.2
    ic.poly(_pts(VS_BACK, x, y, k), fill="#2C7FB8")
    ic.poly(_pts(VS_FRONT, x, y, k), fill="#5FB4E8")
    ic.poly(_pts(VS_PANEL, x, y, k), fill="#B4E7FF")


# --- Sublime Text: an orange S inlaid in a slate ------------------------------

S_BARS = [  # on a 100 grid: the top, the fold, the foot
    ([(18, 40), (82, 14), (82, 36), (18, 62)], 0),
    ([(18, 40), (82, 66), (82, 88), (18, 62)], 1),
    ([(18, 66), (82, 40), (82, 62), (18, 88)], 2),
]


def _s_mark(ic, x, y, k, tones):
    # the fold first, then the top and the foot over it
    for idx in (1, 0, 2):
        pts, t = S_BARS[idx]
        ic.poly(_pts(pts, x, y, k), fill=tones[t])


@icon("sublime-text", kind="app", title="Sublime Text",
      names=["com.sublimetext.three", "sublime-text", "sublime-text-2", "sublime-text-3", "sublime_text"])
def sublime(ic):
    tile(ic, "#B4622A", "#5E2A0E")
    shadow(ic, 128, 214, 96, 12)
    # the slate: its edge, then its face
    ic.rect(36, 44, 184, 172, rx=24, fill="#121316")
    ic.rect(36, 34, 184, 170, rx=24, fill=ic.lin([(0, "#4C5058"), (0.5, "#2C2F35"), (1, "#1C1E22")], 0, 0, 1, 1))
    ic.rect(36.75, 34.75, 182.5, 168.5, rx=23.25, fill="none", stroke="#fff", stroke_opacity=0.16, stroke_width=1.5)
    ic.line(60, 205, 196, 205, stroke="#fff", stroke_opacity=0.06, stroke_width=2)
    # the inlay's recess, then the S in orange enamel
    x, y, k = 70, 46, 1.16
    for shape, _ in S_BARS:
        ic.poly(_pts(shape, x - 1.5, y - 1.5, k), fill="#000", opacity=0.5, stroke="#000", stroke_width=2,
                stroke_linejoin="round")
    _s_mark(ic, x, y, k, (ic.lin([(0, "#FFB25A"), (1, "#FF8A1F")], 0, 0, 1, 0), "#C9530C",
                          ic.lin([(0, "#FF9A2E"), (1, "#F07A12")], 0, 0, 1, 0)))
    ic.poly(_pts([(18, 40), (82, 14), (82, 18), (18, 44)], x, y, k), fill="#fff", opacity=0.35)
    ic.poly(_pts([(18, 66), (82, 40), (82, 44), (18, 70)], x, y, k), fill="#fff", opacity=0.25)
    # engraved under it
    ic.text("sublime text", 128, 172, 12, font="sans-semibold", anchor="middle", spacing=1.2, fill="#000",
            opacity=0.5, transform="translate(0 -0.8)")
    ic.text("sublime text", 128, 172, 12, font="sans-semibold", anchor="middle", spacing=1.2, fill="#8A8F98")
    ic.text("BUILD 4200", 128, 186, 6.5, font="mono", anchor="middle", spacing=1.4, fill="#6A6F78")
    ic.path("M36 64a30 30 0 0 1 30-30h80L60 200a24 24 0 0 1-24-24z", fill=glare(ic, 0.6))


@small("sublime-text")
def sublime16(ic):
    tile(ic, "#B4622A", "#5E2A0E")
    ic.rect(2, 2.5, 12, 11.5, rx=2, fill="#16171A")
    ic.rect(2, 2, 12, 11, rx=2, fill="#383B42")
    _s_mark(ic, 3, 2, 0.1, ("#FFA03A", "#B9500C", "#FF8A1F"))


# --- Zed: a keycap with its mark ---------------------------------------------

def _zed_mark(ic, x, y, k, col, w):
    """The Z in its open square, redrawn: strokes on a 100 grid."""
    d = (f"M{x + 22 * k:.1f} {y + 12 * k:.1f}H{x + 88 * k:.1f}V{y + 70 * k:.1f}"
         f"M{x + 78 * k:.1f} {y + 88 * k:.1f}H{x + 12 * k:.1f}V{y + 30 * k:.1f}"
         f"M{x + 34 * k:.1f} {y + 32 * k:.1f}H{x + 66 * k:.1f}L{x + 34 * k:.1f} {y + 68 * k:.1f}H{x + 66 * k:.1f}")
    ic.path(d, fill="none", stroke=col, stroke_width=w, stroke_linejoin="miter", stroke_linecap="square")


@icon("zed", kind="app", title="Zed", names=["dev.zed.Zed", "zed", "zed-editor"])
def zed(ic):
    tile(ic, "#2F5FB8", "#14306A")
    shadow(ic, 128, 214, 96, 13)
    # the keycap's skirt, wider at the foot
    ic.path("M42 70a22 22 0 0 1 22-22h128a22 22 0 0 1 22 22l10 118a20 20 0 0 1-20 22H52a20 20 0 0 1-20-22z",
            fill=ic.lin([(0, "#2E3036"), (1, "#0E0F12")], 0, 0, 1, 1))
    ic.path("M32 188a20 20 0 0 0 20 22h152a20 20 0 0 0 20-22", fill="none", stroke="#000", stroke_opacity=0.4,
            stroke_width=2)
    ic.path("M42 70a22 22 0 0 1 22-22h4L60 210h-8a20 20 0 0 1-20-22z", fill="#fff", opacity=0.07)
    ic.path("M42 70a22 22 0 0 1 22-22", fill="none", stroke="#fff", stroke_opacity=0.25, stroke_width=1.5)
    # its top, dished
    ic.rect(56, 44, 144, 136, rx=20, fill=ic.lin([(0, "#3E4148"), (1, "#1A1B1F")], 0, 0, 1, 1))
    ic.rect(62, 50, 132, 124, rx=16, fill=ic.rad([(0, "#2A2C32"), (0.8, "#202227"), (1, "#2E3037")],
                                                  cx=0.5, cy=0.55, r=0.7))
    ic.rect(56.75, 44.75, 142.5, 134.5, rx=19.25, fill="none", stroke="#fff", stroke_opacity=0.16,
            stroke_width=1.5)
    # the legend, printed
    _zed_mark(ic, 84, 68, 0.88, "#F4F6FA", 9)
    ic.text("zed", 186, 166, 8, font="mono-semibold", anchor="end", fill="#8E95A3")
    ic.path("M62 66a16 16 0 0 1 16-16h70L84 174h-6a16 16 0 0 1-16-16z", fill=glare(ic, 0.5))


@small("zed")
def zed16(ic):
    tile(ic, "#2F5FB8", "#14306A")
    ic.rect(2, 3, 12, 11, rx=2, fill="#0F1013")
    ic.rect(3, 2, 10, 10, rx=1.6, fill="#2C2E34")
    ic.path("M5.6 4.4H11V9.6M10.4 10.6H5V5.4", fill="none", stroke="#F4F6FA", stroke_width=0.8)
    ic.path("M6.6 5.9H9.4L6.6 8.6H9.4", fill="none", stroke="#F4F6FA", stroke_width=1.1, stroke_linejoin="round")


# --- Cursor: its cube, in smoked glass and graphite ---------------------------

@icon("cursor", kind="app", title="Cursor", names=["co.anysphere.cursor", "cursor", "cursor-editor"])
def cursor(ic):
    tile(ic, "#34363C", "#0F1012")
    shadow(ic, 128, 212, 84, 12)
    cx, top, r = 128, 30, 92
    hw = r * 0.866
    mid = top + r          # the near corner
    T = (cx, top)
    L1, R1 = (cx - hw, top + r / 2), (cx + hw, top + r / 2)
    L2, R2 = (cx - hw, top + r * 1.5), (cx + hw, top + r * 1.5)
    B = (cx, top + 2 * r)
    C = (cx, mid)
    # the three faces
    ic.poly([T, R1, C, L1], fill=ic.lin([(0, "#8E929A"), (1, "#5C6068")], 0, 0, 1, 1))
    ic.poly([L1, C, B, L2], fill=ic.lin([(0, "#3E4148"), (1, "#24262B")]))
    ic.poly([C, R1, R2, B], fill=ic.lin([(0, "#2A2C31"), (1, "#141518")]))
    # the mark's facet: a pointer of light, from the near corner to the far one
    ic.poly([C, R1, (cx + hw * 0.0, top + r * 0.0)], fill=ic.lin([(0, "#FFFFFF"), (1, "#C9CCD2")], 1, 0, 0, 1))
    ic.poly([C, R1, R2], fill=ic.lin([(0, "#E9EBEE"), (1, "#9A9EA6")], 0, 0, 1, 1), opacity=0.9)
    # the edges, bevelled: a thin light chamfer on each near edge
    ic.poly([T, R1, C, L1], fill="none", stroke="#fff", stroke_opacity=0.4, stroke_width=1.5,
            stroke_linejoin="round")
    ic.line(L1[0] + 1, L1[1] + 1, L2[0] + 1, L2[1] - 1, stroke="#fff", stroke_opacity=0.22, stroke_width=2)
    ic.line(C[0], C[1] + 1, B[0], B[1] - 1, stroke="#fff", stroke_opacity=0.3, stroke_width=2)
    ic.line(*C, *R1, stroke="#fff", stroke_opacity=0.7, stroke_width=1.2)
    ic.poly([T, R1, R2, B, L2, L1], fill="none", stroke="#000", stroke_opacity=0.4, stroke_width=1.5,
            stroke_linejoin="round")
    # the light across the top, and a glint at the near corner
    def lerp(p, q, t):
        return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
    ic.poly([lerp(L1, T, 0.25), lerp(L1, T, 0.5), lerp(C, R1, 0.5), lerp(C, R1, 0.25)], fill="#fff", opacity=0.1)
    ic.circle(*C, 2.2, fill="#fff", opacity=0.8)
    # engraved on the left face
    with ic.g(transform=f"matrix(0.866 0.5 0 1 {cx - hw} {top + r / 2})"):
        ic.text("CURSOR", 12, 74, 10, font="sans-semibold", spacing=2.4, fill="#000", opacity=0.5,
                transform="translate(0 0.8)")
        ic.text("CURSOR", 12, 74, 10, font="sans-semibold", spacing=2.4, fill="#80858E")


@small("cursor")
def cursor16(ic):
    tile(ic, "#34363C", "#0F1012")
    cx, top, r = 8, 1.6, 6.4
    hw = r * 0.866
    T, C, B = (cx, top), (cx, top + r), (cx, top + 2 * r)
    L1, R1 = (cx - hw, top + r / 2), (cx + hw, top + r / 2)
    L2, R2 = (cx - hw, top + r * 1.5), (cx + hw, top + r * 1.5)
    ic.poly([T, R1, C, L1], fill="#7E828A")
    ic.poly([L1, C, B, L2], fill="#3A3D44")
    ic.poly([C, R1, R2], fill="#E9EBEE")
    ic.poly([C, R2, B], fill="#1E2024")
    ic.poly([C, R1, T], fill="#F4F5F7")


# --- Android Studio: a drafting compass on a blueprint -----------------------

GREEN = "#3DDC84"


@icon("android-studio", kind="app", title="Android Studio",
      names=["android-studio", "androidstudio", "com.google.AndroidStudio", "studio"])
def android_studio(ic):
    tile(ic, "#1C5A6E", "#082C3A")
    shadow(ic, 128, 214, 100, 12)
    # the blueprint, flat on the desk
    with ic.g(transform="rotate(-4 128 160)"):
        ic.rect(28, 112, 200, 100, rx=3, fill="#000", opacity=0.25, transform="translate(2 3)")
        ic.rect(28, 112, 200, 100, rx=3, fill=ic.lin([(0, "#2C6BD8"), (1, "#1747A0")], 0, 0, 1, 1))
        grid = ic.define('<pattern id="{id}" width="10" height="10" patternUnits="userSpaceOnUse">'
                         '<path d="M10 0V10H0" fill="none" stroke="#fff" stroke-opacity=".14" stroke-width=".8"/>'
                         '</pattern>', "p")
        ic.rect(28, 112, 200, 100, rx=3, fill=f"url(#{grid})")
        # a phone, drafted
        ic.rect(44, 124, 46, 80, rx=7, fill="none", stroke="#E8F0FF", stroke_width=1.6)
        ic.rect(49, 134, 36, 58, fill="none", stroke="#E8F0FF", stroke_width=0.9, opacity=0.7)
        ic.text("360dp", 67, 120, 6.5, font="mono", anchor="middle", fill="#E8F0FF", opacity=0.85)
        ic.text("activity_main.xml", 220, 205, 6.5, font="mono", anchor="end", fill="#E8F0FF", opacity=0.85)
        # the arc the compass has drawn
    # the arc the compass is drawing, round its needle
    ic.path("M139.6 124.3A72 72 0 0 1 186 186", fill="none", stroke="#fff", stroke_width=1.6, opacity=0.9)
    # the compass: two legs from the head
    hx, hy = 150, 60
    for (fx, fy), w in (((114, 194), 8), ((188, 186), 8)):
        ic.line(hx, hy + 18, fx + 2, fy + 3, stroke="#000", stroke_opacity=0.3, stroke_width=w,
                stroke_linecap="round")
    ic.line(hx - 3, hy + 18, 116, 176, stroke=steel(ic), stroke_width=8, stroke_linecap="round")
    ic.line(hx + 3, hy + 18, 184, 168, stroke=steel(ic), stroke_width=8, stroke_linecap="round")
    ic.line(hx - 5, hy + 20, 113, 174, stroke="#fff", stroke_opacity=0.5, stroke_width=1.5)
    ic.line(hx + 1, hy + 20, 181, 168, stroke="#fff", stroke_opacity=0.4, stroke_width=1.5)
    # the needle on the left, the lead on the right
    ic.path("M112 174l8 4-6 16z", fill="#9AA1A9")
    ic.path("M181 166l9 3-1 10-4 7-3-9z", fill="#2A2C30")
    ic.path("M188 179l-3 7-1-6z", fill="#555")
    # the knuckle
    ic.rect(hx - 9, hy + 12, 18, 14, rx=3, fill=steel(ic, horizontal=False))
    ic.circle(hx, hy + 19, 3, fill="#5D636B")
    # the head: the robot's, in green enamel, antennae and eyes
    ic.line(hx - 11, hy - 20, hx - 18, hy - 33, stroke="#2BA866", stroke_width=4, stroke_linecap="round")
    ic.line(hx + 11, hy - 20, hx + 18, hy - 33, stroke="#2BA866", stroke_width=4, stroke_linecap="round")
    ic.path(f"M{hx - 30} {hy + 12}a30 30 0 0 1 60 0z", fill="#1C7A48", transform="translate(0 2.5)")
    ic.path(f"M{hx - 30} {hy + 12}a30 30 0 0 1 60 0z",
            fill=ic.rad([(0, "#7DF0AE"), (0.6, GREEN), (1, "#26A862")], cx=0.35, cy=0.3, r=0.8))
    ic.circle(hx - 12, hy - 1, 3.8, fill="#073042")
    ic.circle(hx + 12, hy - 1, 3.8, fill="#073042")
    ic.path(f"M{hx - 20} {hy - 8}a24 24 0 0 1 18 -12", fill="none", stroke="#fff", stroke_opacity=0.55,
            stroke_width=2.5, stroke_linecap="round")


@small("android-studio")
def android_studio16(ic):
    tile(ic, "#1C5A6E", "#082C3A")
    ic.rect(1.5, 8.5, 13, 5.5, rx=0.5, fill="#2459C0")
    ic.path("M8 6 L5 13.5 M8 6 L11.5 13", stroke="#C3C8CE", stroke_width=1.2, stroke_linecap="round")
    ic.path("M4.5 6.2a3.5 3.5 0 0 1 7 0z", fill=GREEN)
    ic.circle(6.8, 5.2, 0.5, fill="#073042")
    ic.circle(9.2, 5.2, 0.5, fill="#073042")
