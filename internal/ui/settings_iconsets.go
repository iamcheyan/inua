package ui

import (
	"cmp"
	"slices"
	"strings"

	"codeberg.org/puregotk/puregotk/v4/gdk"
	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/config"
	"github.com/lyricat/inua/internal/gtkx"
	"github.com/lyricat/inua/internal/i18n"
	"github.com/lyricat/inua/internal/shell"
	"github.com/lyricat/inua/internal/uikit"
	layouts "github.com/lyricat/inua/ui"
)

// The icons on the Appearance page: the app styles (style.app_style) as
// tiles like the theme swatches, each showing a few of its apps, a click
// choosing one and a right click opening Preview All, every app it draws
// in a window of its own; the line icons (style.icons) in a menu, with
// Preview All, every icon of the set, beside it.

// What an app style's tile shows: four of inua's apps and two others it
// draws.
var tileApps = []string{"io.github.lyricat.Inua.Files", "io.github.lyricat.Inua.Term", "io.github.lyricat.Inua.Mail", "io.github.lyricat.Inua.Clock", "firefox", "vlc"}

// buildAppStyleTiles makes a tile for each of inua's app styles.
func (s *shellUI) buildAppStyleTiles(names map[string]string) {
	st := &s.settings
	st.appstyles.RemoveAll()
	st.styleTiles = map[string]*gtk.Button{}
	var later iconFill
	defer func() { later.start() }() // the jobs added below
	for _, style := range config.InuaThemes {
		ground := gtk.NewBox(gtk.OrientationHorizontalValue, 8)
		theme := s.styleTheme(style)
		for _, name := range tileApps {
			gtkx.Append(ground, &later.image(theme, name, 28).Widget)
		}
		st.styleTiles[style] = s.iconTile(&st.appstyles, "appstyle:"+style, names[style], ground)
	}
}

// iconTile adds a tile to grid: ground, then title under it; named name,
// for a click to choose it and a right click to open its menu.
func (s *shellUI) iconTile(grid *gtk.FlowBox, name, title string, ground *gtk.Box) *gtk.Button {
	btn := gtk.NewButton()
	btn.SetName(name)
	btn.AddCssClass("swatch")
	btn.AddCssClass("iconset")
	btn.SetTooltipText(i18n.Tf("%s · right-click to preview every icon", title))
	box := gtk.NewBox(gtk.OrientationVerticalValue, 6)
	ground.AddCssClass("ground")
	gtkx.Append(box, &ground.Widget)
	label := gtk.NewLabel(title)
	label.SetXalign(0)
	label.SetEllipsize(3) // end
	gtkx.Append(box, &label.Widget)
	btn.SetChild(&box.Widget)
	box.Unref()
	btn.ConnectClicked(&s.onSettingsButton)
	menu := gtk.NewGestureClick()
	menu.SetButton(3)
	menu.ConnectPressed(&s.onIconSetMenu)
	btn.AddController(&menu.EventController)
	grid.Append(&btn.Widget)
	btn.Unref() // the flow box holds it
	return btn
}

// lineTheme is the theme a set of line icons takes them from: Phosphor's,
// a set of the user's over them, the system's or an installed theme.
// styleTheme is an app style's: the style once installed, else the
// system's, whose chain ends at the objects installed in hicolor. Both
// are kept while the settings are open.
func (s *shellUI) lineTheme(set string) *gtk.IconTheme {
	c := s.cfg
	name := set
	switch {
	case set == "phosphor":
		name = iconThemeName
		_ = s.writeIconTheme(name, "")
	case set == "system":
		name = s.icons.system
	case s.isUserIconSet(set):
		name = "inua-icons-" + set
		_ = s.writeIconTheme(name, c.IconSetPath(set))
	}
	return s.keptTheme("line:"+set, name)
}

func (s *shellUI) styleTheme(style string) *gtk.IconTheme {
	name := s.icons.system
	if config.IsIconTheme(style) {
		name = style
	}
	return s.keptTheme("style:"+style, name)
}

// keptTheme is a GtkIconTheme of name, made once under key.
func (s *shellUI) keptTheme(key, name string) *gtk.IconTheme {
	st := &s.settings
	if t, ok := st.setThemes[key]; ok {
		return t
	}
	t := gtk.NewIconTheme()
	if s.icons.dir != "" {
		t.AddSearchPath(s.icons.dir)
	}
	t.SetThemeName(name)
	if st.setThemes == nil {
		st.setThemes = map[string]*gtk.IconTheme{}
	}
	st.setThemes[key] = t
	return t
}

// iconFill fills images with their icons off the main thread: looking an
// icon up first reads its theme's whole chain, a quarter of a second for
// a large one (Papirus), and there may be dozens of themes. A GtkIconTheme
// takes lookups from any thread (as Files' does); the images are set on
// the main thread, each held till then, so one whose window has closed
// meanwhile is still there to set.
type iconFill []iconJob

type iconJob struct {
	img   *gtk.Image
	theme *gtk.IconTheme
	name  string
	size  int32
}

// image is an empty image that start fills with name from theme at size.
func (f *iconFill) image(theme *gtk.IconTheme, name string, size int32) *gtk.Image {
	img := gtk.NewImage()
	img.SetPixelSize(size)
	img.Ref() // till it is filled
	theme.Ref()
	*f = append(*f, iconJob{img, theme, name, size})
	return img
}

// start looks the icons up, a goroutine for each theme, and sets each
// as it comes.
func (f iconFill) start() {
	byTheme := map[uintptr][]iconJob{}
	var order []uintptr
	for _, j := range f {
		k := j.theme.GoPointer()
		if _, ok := byTheme[k]; !ok {
			order = append(order, k)
		}
		byTheme[k] = append(byTheme[k], j)
	}
	for _, k := range order {
		go func(jobs []iconJob) {
			for _, j := range jobs {
				p := j.theme.LookupIcon(j.name, []string{"image-missing"}, j.size, 1, gtk.TextDirLtrValue, 0)
				gtkx.Post(func() {
					j.img.SetFromPaintable(p)
					p.Unref()
					j.img.Unref()
					j.theme.Unref()
				})
			}
		}(byTheme[k])
	}
}

// styleMenu opens an app style's menu, Preview All, at a right click on
// its tile.
func (s *shellUI) styleMenu(btn *gtk.Widget, x, y float64) {
	st := &s.settings
	st.iconSetMenu = strings.TrimPrefix(btn.GetName(), "appstyle:")
	style := st.iconSetMenu
	pop := uikit.NewMenu([]uikit.Item{
		{Label: i18n.T("Preview All…"), Run: func() { s.previewAppStyle(style) }},
	}, uikit.AtPointer)
	pop.SetParent(btn)
	pop.SetPointingTo(&gdk.Rectangle{X: int32(x), Y: int32(y), Width: 1, Height: 1})
	pop.ConnectClosed(&s.onThemeMenuClosed)
	pop.Unref() // the tile holds it
	pop.Popup()
}

// isUserIconSet reports whether set is one of the user's, a folder beside
// config.toml.
func (s *shellUI) isUserIconSet(set string) bool {
	c := s.cfg
	return c.IconSetPath(set) != "" && slices.Contains(c.IconSetNames(), set) && !slices.Contains(config.IconSets, set)
}

// previewIconSet opens a window of every line icon of a set.
func (s *shellUI) previewIconSet(set string) {
	st := &s.settings
	theme := s.lineTheme(set)
	title := cmp.Or(st.iconSetTitles[set], set)
	body, later, open := s.previewWindow(title)
	if body == nil {
		return
	}
	grid := previewGrid(12)
	entries, _ := layouts.FS.ReadDir("icons")
	for _, e := range entries {
		name, ok := strings.CutSuffix(e.Name(), ".svg")
		if !ok {
			continue
		}
		img := later.image(theme, name, 24)
		img.AddCssClass("preview-icon")
		img.SetTooltipText(name)
		grid.Append(&img.Widget)
		img.Unref()
	}
	gtkx.Append(body, &grid.Widget)
	open()
}

// previewAppStyle opens a window of every app an app style draws: inua's
// own, then the others.
func (s *shellUI) previewAppStyle(style string) {
	st := &s.settings
	theme := s.styleTheme(style)
	body, later, open := s.previewWindow(cmp.Or(st.styleTitles[style], style))
	if body == nil {
		return
	}
	appCell := func(grid *gtk.FlowBox, icon, name string) {
		cell := gtk.NewBox(gtk.OrientationVerticalValue, 6)
		cell.AddCssClass("preview-app")
		img := later.image(theme, icon, 48)
		img.SetHalign(gtk.AlignCenterValue)
		gtkx.Append(cell, &img.Widget)
		l := gtk.NewLabel(name)
		l.SetEllipsize(3) // end
		l.SetMaxWidthChars(12)
		gtkx.Append(cell, &l.Widget)
		grid.Append(&cell.Widget)
		cell.Unref()
	}
	gtkx.Append(body, &label(i18n.T("inua's apps"), "kicker").Widget)
	grid := previewGrid(6)
	for _, e := range shell.LightApps(s.dockState.apps) {
		if strings.HasPrefix(e.Icon, "io.github.lyricat.Inua.") {
			appCell(grid, e.Icon, e.Name)
		}
	}
	gtkx.Append(body, &grid.Widget)
	if others := config.DrawnApps(style); len(others) > 0 {
		gtkx.Append(body, &label(i18n.Tf("Other apps · %d", len(others)), "kicker").Widget)
		grid := previewGrid(6)
		for _, name := range others {
			title := name
			if e := s.dockState.apps.ByID(name); e != nil {
				title = e.Name
			}
			appCell(grid, name, title)
		}
		gtkx.Append(body, &grid.Widget)
	}
	open()
}

// previewWindow makes a preview's window, its body to fill (nil without
// the settings), an iconFill for the body's images, and open, which fills
// them and shows the window.
func (s *shellUI) previewWindow(title string) (*gtk.Box, *iconFill, func()) {
	st := &s.settings
	if st.win == nil {
		return nil, nil, nil
	}
	win := gtk.NewWindow()
	win.SetTransientFor(&st.win.Window)
	win.SetDestroyWithParent(true)
	win.SetModal(true)
	win.SetDefaultSize(760, 620)
	win.SetTitle(i18n.Tf("%s: every icon", title))
	win.AddCssClass("settings")
	win.AddCssClass("icon-preview")
	body := gtk.NewBox(gtk.OrientationVerticalValue, 14)
	body.AddCssClass("preview-body")
	gtkx.Append(body, &label(title, "preview-title").Widget)
	later := &iconFill{}
	open := func() {
		scroll := gtk.NewScrolledWindow()
		scroll.SetPolicy(gtk.PolicyNeverValue, gtk.PolicyAutomaticValue)
		scroll.SetChild(&body.Widget)
		body.Unref()
		win.SetChild(&scroll.Widget)
		scroll.Unref()
		keys := gtk.NewEventControllerKey()
		keys.ConnectKeyPressed(&s.onPreviewKey)
		win.AddController(&keys.EventController)
		later.start()
		win.Present()
	}
	return body, later, open
}

// previewGrid is a grid of up to cols a line.
func previewGrid(cols uint32) *gtk.FlowBox {
	g := gtk.NewFlowBox()
	g.SetSelectionMode(gtk.SelectionNoneValue)
	g.SetHomogeneous(true)
	g.SetMaxChildrenPerLine(cols)
	g.SetMinChildrenPerLine(min(cols, 4))
	g.SetRowSpacing(10)
	g.SetColumnSpacing(10)
	return g
}
