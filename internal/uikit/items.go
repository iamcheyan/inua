package uikit

import (
	"strconv"
	"sync"

	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/gtkx"
)

// Item is a line of a menu NewMenu makes.
type Item struct {
	Label string
	Keys  string // its keys, in a keycap at the line's end
	// Run is what it does; nil, with no Items, greys the line out.
	Run func()
	// Items are a submenu, opened in the menu's place, with a line back.
	Items []Item
	// Mark is "check" or "radio" for a line turned on, "off" for one of
	// those turned off: it keeps the mark's room.
	Mark string
	// Separator is a hairline between groups of lines, in place of a line.
	Separator bool
}

// The items' menus: what each button does, and the menu it is in.
var items struct {
	mu   sync.Mutex
	by   map[uintptr]itemLine // by button
	pops map[uintptr][]uintptr
}

type itemLine struct {
	pop   *gtk.Popover
	stack *gtk.Stack
	item  Item
	page  string // the submenu it opens, or the page it goes back to
	back  bool
}

// onItem is every item's click: a submenu opens in place, a line back goes
// back, any other line closes the menu and then does its work.
var onItem = func(b gtk.Button) {
	items.mu.Lock()
	l, ok := items.by[b.GoPointer()]
	items.mu.Unlock()
	switch {
	case !ok:
	case l.back || len(l.item.Items) > 0:
		l.stack.SetVisibleChildName(l.page)
	case l.item.Run != nil:
		l.pop.Popdown()
		gtkx.Post(l.item.Run)
	}
}

// onItemsDestroy forgets a menu's lines with it.
var onItemsDestroy = func(w gtk.Widget) {
	items.mu.Lock()
	for _, b := range items.pops[w.GoPointer()] {
		delete(items.by, b)
	}
	delete(items.pops, w.GoPointer())
	items.mu.Unlock()
}

// NewMenu is a menu of items (design/ui.md, Menus) opening at at: the
// shared `.menu-item` lines, a submenu in the menu's place. The caller
// owns the popover's reference, as with gtk.NewPopover, and parents it.
func NewMenu(list []Item, at MenuAt) *gtk.Popover {
	pop := gtk.NewPopover()
	stack := gtk.NewStack()
	stack.SetTransitionType(gtk.StackTransitionTypeSlideLeftRightValue)
	stack.SetTransitionDuration(160)
	stack.SetVhomogeneous(false)
	stack.SetHhomogeneous(false)
	stack.SetInterpolateSize(true)
	n := 0
	var page func(list []Item, name, back, title string)
	page = func(list []Item, name, back, title string) {
		box := gtk.NewBox(gtk.OrientationVerticalValue, 0)
		box.AddCssClass("menu-items")
		if back != "" {
			addLine(box, pop, stack, Item{Label: title}, back, true, false)
			sep := gtk.NewSeparator(gtk.OrientationHorizontalValue)
			gtkx.Append(box, &sep.Widget)
		}
		marks := false
		for _, it := range list {
			marks = marks || it.Mark != ""
		}
		for _, it := range list {
			if it.Separator {
				sep := gtk.NewSeparator(gtk.OrientationHorizontalValue)
				gtkx.Append(box, &sep.Widget)
				continue
			}
			sub := ""
			if len(it.Items) > 0 {
				n++
				sub = "s" + strconv.Itoa(n)
				page(it.Items, sub, name, it.Label)
			}
			addLine(box, pop, stack, it, sub, false, marks)
		}
		stack.AddNamed(&box.Widget, name)
		box.Unref()
	}
	page(list, "main", "", "")
	stack.SetVisibleChildName("main")
	pop.SetChild(&stack.Widget)
	stack.Unref()
	pop.ConnectDestroy(&onItemsDestroy)
	Menu(pop, at)
	return pop
}

// addLine adds an item's line to a page: its mark's room when the page
// has marks, its label, its keys or a submenu's arrow; back is the line
// going back to page.
func addLine(box *gtk.Box, pop *gtk.Popover, stack *gtk.Stack, it Item, page string, back, marks bool) {
	b := gtk.NewButton()
	b.AddCssClass("menu-item")
	row := gtk.NewBox(gtk.OrientationHorizontalValue, 8)
	if back {
		img := gtk.NewImageFromIconName("go-previous-symbolic")
		gtkx.Append(row, &img.Widget)
	}
	if marks {
		mark := gtk.NewLabel(map[string]string{"check": "✓", "radio": "●"}[it.Mark])
		mark.AddCssClass("menu-mark")
		mark.SetSizeRequest(14, -1)
		gtkx.Append(row, &mark.Widget)
	}
	l := gtk.NewLabel(it.Label)
	l.SetXalign(0)
	l.SetHexpand(true)
	gtkx.Append(row, &l.Widget)
	switch {
	case len(it.Items) > 0:
		img := gtk.NewImageFromIconName("go-next-symbolic")
		gtkx.Append(row, &img.Widget)
	case it.Keys != "":
		k := gtk.NewLabel(it.Keys)
		k.AddCssClass("menu-key")
		gtkx.Append(row, &k.Widget)
	}
	b.SetChild(&row.Widget)
	row.Unref()
	b.SetSensitive(back || it.Run != nil || len(it.Items) > 0)
	b.ConnectClicked(&onItem)
	items.mu.Lock()
	if items.by == nil {
		items.by, items.pops = map[uintptr]itemLine{}, map[uintptr][]uintptr{}
	}
	items.by[b.GoPointer()] = itemLine{pop: pop, stack: stack, item: it, page: page, back: back}
	items.pops[pop.GoPointer()] = append(items.pops[pop.GoPointer()], b.GoPointer())
	items.mu.Unlock()
	gtkx.Append(box, &b.Widget)
}
