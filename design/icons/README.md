# inua's object icons

Every app drawn as the object it stands for, in vector, on inua's tile:
inua's own icons (`config/apps/`) and the `inua-objects` icon theme for
other apps (`config/icons/inua-objects/`). The plan, the list of icons and
the decisions are in `docs/feat/object-icons.md` (not committed); the
first six (`drawings/core.py`) set the style.

```sh
python3 design/icons/build.py                         # everything
python3 design/icons/build.py --sheet-dir=bin/sheet-x calendar weather
```

The second form builds only those icons and writes a contact sheet,
`bin/sheet-x/sheet.png`: each icon at 160, 64, 32, 24 px and its 16 px
drawing, on inua's dark and light grounds. Look at it after every change.
Needs Python 3 with fontTools, and Chrome for the sheet.

## The style

- **The object is the app**: Files is a manila folder, Mail an envelope,
  Clock a brass clock. Choose the object a person would put on a desk, not
  a symbol: a barometer for Weather, not a sun.
- **Tile**: `tile(ic, top, bottom)`: the app's ground hue, lighter at the
  top. Deep, a little desaturated (see core.py); the object brings the
  bright colours.
- **One light from the top left**: highlights along top and left edges,
  the darker side below and right; glass gets `glare(ic)` from the top
  left; metal a gradient lighter to the top left (`brass`, `steel`).
- **One shadow**: `shadow(ic, cx, cy, rx, ry)` under the object, where it
  touches the desk (about y 205–226, rx 70–100, ry 9–13).
- **Size**: the object fills the tile well, about 180–200 px of the 256,
  centred a little above the middle (the shadow takes the bottom).
- **Materials**: use the kit's (`paper`, `brass`, `steel`, `graphite`,
  `wood`, `felt`, `leather`, `enamel`, `wax`, `glass_dark`) before
  making a gradient of your own; keep the same tones across icons.
- **Real detail**: real text where the real object has it (a date, a
  label, a reading, a headline), set with `ic.text` in the kit's fonts;
  real small parts (screws, perforations, ticks, legends); inua's mark
  (`mark(ic, …)`) where a maker's mark would be. Text is outlined at build,
  so it costs bytes: a few lines, not paragraphs.
- **Depth**: two or three layers (a back, the object, a front edge), each
  with its own small shadow or edge highlight. Not flat, not photographic.
- **No** `filter`, blur, live `<text>`, images, or masks: gradients,
  paths, shapes, clip paths and patterns only. Under 80 KB a file.

## The soft set

`soft/` draws the same objects for the `inua-objects-soft` theme, with
`@soft("Name")` (the name of the `@icon`; kind, names and title are its).
`soft/core.py` set the style: the same object, tile, colours and
composition, about half the detail; a flat colour or one gentle gradient
a surface (`two`), `soft_shadow` under it, no glare, no text (writing is
`bar`s, a mark a simple shape). The 16 px drawing is shared, and the soft
theme inherits the objects, so an app not drawn soft keeps its object.
`--soft` puts the soft drawings on the sheet.

The flat set (`inua-objects-flat`) is the soft drawings drawn on
`Icon(flat=True)`: each gradient becomes one colour, its lit side, the
tile one colour and `soft_shadow` a hard one. An icon that needs more has
its own drawing, `@flat("Name")`, drawn the same way; `--flat` shows them.

## The 16 px drawing

`@small("Name")` on a 16 grid: the same tile (`tile(ic, …)` makes it
small), the object's silhouette and two or three shapes in its colours, no
text, no gradients needed. It must read at 16 px: test it on the sheet.

## The kit (`lib.py`)

```python
from lib import icon, small, tile, shadow, glare, paper, brass, steel, graphite, wood, felt, leather, enamel, wax, glass_dark, mark, polar

@icon("Calendar")                      # inua's: config/apps/io.github.lyricat.Inua.Calendar.svg
@icon("firefox", kind="app", names=["org.mozilla.firefox", "firefox-esr"], title="Firefox")
def draw(ic):                          # ic: lib.Icon on a 256 grid
    ic.rect(x, y, w, h, rx=…, fill=…, stroke=…, opacity=…)   # any SVG attribute; _ becomes -
    ic.circle / ic.ellipse / ic.path(d) / ic.line / ic.poly(points)
    ic.lin(stops, x1, y1, x2, y2) / ic.rad(stops, cx, cy, r)  # -> "url(#…)"; stops (offset, colour[, opacity])
    with ic.g(transform="rotate(-6 128 130)"): …
    ic.text("Field notes", x, baseline, size, font="sans-semibold", anchor="start|middle|end", spacing=0, fill=…)
    ic.define('<pattern id="{id}" …>…</pattern>') / ic.clip("<rect …/>")
```

Fonts: `sans`, `sans-medium`, `sans-semibold`, `sans-bold`,
`sans-condensed`, `mono`, `mono-semibold`, `hand` (Caveat). A character a
font has not (❯, ⌫, emoji) stops the build: draw it as a shape.

For an app of the theme, `names` lists every icon name its desktop entries
use (`Icon=` lines: `firefox`, `org.mozilla.firefox`); the file is named
after the first argument and linked under the others.

## Brands (the theme)

Other apps' marks are their owners' trademarks. Where the mark already is
an object (VLC's cone, Telegram's paper plane, Obsidian's crystal), draw
that object in the house style. Otherwise draw the app's job as an object
in the brand's colours, with a simplified mark on it, as a stamp, print or
engraving (as inua's mark is pressed into Mail's seal). Never copy a logo's
artwork: redraw it, simplified. The exception is a mark whose licence
allows a remix, kept in `brands/` with its notice and drawn with
`brand(name)`: Firefox's (MPL 2.0), Chrome's (public domain) and
Chromium's (BSD), each on the tile as it is with inua's light over it.
