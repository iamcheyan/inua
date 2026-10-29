package annotui

import (
	"codeberg.org/puregotk/puregotk/v4/gdk"
	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/annotate"
	"github.com/lyricat/inua/internal/gtkx"
	"github.com/lyricat/inua/internal/i18n"
)

// The toolbar: the tools (a second click on the one chosen puts it down,
// leaving the pointer to the host), the inks, undo and redo. The host
// adds its own buttons at the end.

var toolNames = map[annotate.Tool]string{
	annotate.Arrow:     i18n.M("Arrow"),
	annotate.Rect:      i18n.M("Rectangle"),
	annotate.Pen:       i18n.M("Pen"),
	annotate.Highlight: i18n.M("Highlighter"),
	annotate.Text:      i18n.M("Text"),
	annotate.Step:      i18n.M("Numbered step"),
	annotate.Pixelate:  i18n.M("Pixelate"),
}

type toolbar struct {
	e          *Editor
	box        *gtk.Box
	tools      map[annotate.Tool]*gtk.ToggleButton
	inks       []*gtk.ToggleButton
	undo, redo *gtk.Button
	syncing    bool

	onTool, onInk  func(gtk.ToggleButton)
	onUndo, onRedo func(gtk.Button)
}

func newToolbar(e *Editor) *toolbar {
	t := &toolbar{e: e, tools: map[annotate.Tool]*gtk.ToggleButton{}}
	t.box = gtk.NewBox(gtk.OrientationHorizontalValue, 2)
	t.box.AddCssClass("annot-bar")
	t.onTool = func(b gtk.ToggleButton) {
		if t.syncing {
			return
		}
		tool := annotate.Tool(b.GetName())
		if !b.GetActive() {
			if e.tool == tool {
				e.SetTool("")
			}
			return
		}
		e.SetTool(tool)
	}
	for _, tool := range annotate.Tools {
		b := gtk.NewToggleButton()
		b.SetName(string(tool))
		b.SetIconName("annot-" + string(tool) + "-symbolic")
		b.SetTooltipText(i18n.T(toolNames[tool]))
		b.AddCssClass("annot-tool")
		b.ConnectToggled(&t.onTool)
		t.tools[tool] = b
		t.box.Append(&b.Widget)
	}
	t.sep()

	t.onInk = func(b gtk.ToggleButton) {
		if t.syncing || !b.GetActive() {
			t.sync() // an ink stays chosen
			return
		}
		for i, ib := range t.inks {
			if ib.GoPointer() == b.GoPointer() {
				e.ink = i
			}
		}
		t.sync()
		e.changed()
	}
	for i := range annotate.Inks {
		b := gtk.NewToggleButton()
		b.AddCssClass("annot-ink")
		b.SetChild(swatch(annotate.Inks[i]))
		b.SetTooltipText(i18n.T(inkNames[i]))
		b.ConnectToggled(&t.onInk)
		t.inks = append(t.inks, b)
		t.box.Append(&b.Widget)
	}
	t.sep()

	t.undo = gtk.NewButtonFromIconName("edit-undo-symbolic")
	t.undo.SetTooltipText(i18n.T("Undo (Ctrl+Z)"))
	t.onUndo = func(gtk.Button) { e.Undo() }
	t.undo.ConnectClicked(&t.onUndo)
	t.redo = gtk.NewButtonFromIconName("edit-redo-symbolic")
	t.redo.SetTooltipText(i18n.T("Redo (Ctrl+Shift+Z)"))
	t.onRedo = func(gtk.Button) { e.Redo() }
	t.redo.ConnectClicked(&t.onRedo)
	for _, b := range []*gtk.Button{t.undo, t.redo} {
		b.AddCssClass("annot-tool")
		t.box.Append(&b.Widget)
	}
	t.sync()
	return t
}

var inkNames = []string{i18n.M("Red"), i18n.M("Amber"), i18n.M("Green"), i18n.M("Blue"), i18n.M("White"), i18n.M("Black")}

func (t *toolbar) sep() {
	s := gtk.NewSeparator(gtk.OrientationVerticalValue)
	t.box.Append(&s.Widget)
}

// sync shows the tool and the ink chosen, and whether there is anything
// to undo or redo.
func (t *toolbar) sync() {
	t.syncing = true
	for tool, b := range t.tools {
		b.SetActive(t.e.tool == tool)
	}
	t.tools[annotate.Pixelate].SetSensitive(t.e.src != nil) // once its pixels are read
	for i, b := range t.inks {
		b.SetActive(i == t.e.ink)
	}
	t.undo.SetSensitive(t.e.Doc.CanUndo())
	t.redo.SetSensitive(t.e.Doc.CanRedo())
	t.syncing = false
}

// swatch is an ink's colour, a small square: the ink is the picture's, not
// the theme's, so it is drawn, not styled.
func swatch(ink annotate.Ink) *gtk.Widget {
	c := gdk.RGBA{Red: float32(ink.R), Green: float32(ink.G), Blue: float32(ink.B), Alpha: 1}
	w := gtkx.NewCanvas(&gtkx.Canvas{Min: 14, Natural: 14, Snapshot: func(w *gtk.Widget, s *gtk.Snapshot) {
		s.AppendColor(&c, rect(0, 0, float32(w.GetWidth()), float32(w.GetHeight())))
	}})
	w.SetHalign(gtk.AlignCenterValue)
	w.SetValign(gtk.AlignCenterValue)
	w.AddCssClass("annot-swatch")
	return w
}
