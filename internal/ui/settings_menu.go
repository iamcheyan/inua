package ui

import (
	"fmt"
	"slices"
	"strings"

	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/gtkx"
	"github.com/lyricat/inua/internal/i18n"
)

// showAppMenuSettings lists the applications whose menus the bar leaves
// alone, and the ones it shows while its own switch is off, each with a
// button that takes it off the list.
func (s *shellUI) showAppMenuSettings() {
	st := &s.settings
	s.fillAppMenuList(&st.appMenuOff, s.cfg.Bar.MenuOff, "menu_off")
	s.fillAppMenuList(&st.appMenuOn, s.cfg.Bar.MenuOn, "menu_on")
	s.fillAppMenuChoices(&st.appMenuOffAdd, &st.appMenuOffAdds, &st.appMenuOffModel, s.cfg.Bar.MenuOff)
	s.fillAppMenuChoices(&st.appMenuOnAdd, &st.appMenuOnAdds, &st.appMenuOnModel, s.cfg.Bar.MenuOn)
}

// fillAppMenuChoices gives dd the applications that could go on a list:
// those with a window now, by desktop ID, less the ones already on it.
// The choice's label is the application's name; ids keeps the IDs, which
// is what the list stores.
func (s *shellUI) fillAppMenuChoices(dd *gtk.DropDown, ids *[]string, keep **gtk.StringList, already []string) {
	var choices []string
	seen := map[string]bool{}
	for _, id := range already {
		seen[strings.ToLower(id)] = true
	}
	for _, w := range s.snap.Toplevels {
		if w.Class == "" {
			continue
		}
		id := w.Class
		if e := s.dockState.apps.ForClass(w.Class); e != nil {
			id = e.ID
		}
		if seen[strings.ToLower(id)] {
			continue
		}
		seen[strings.ToLower(id)] = true
		choices = append(choices, id)
	}
	slices.Sort(choices)
	*ids = choices
	labels := make([]string, len(choices))
	for i, id := range choices {
		labels[i] = id
		if e := s.dockState.apps.ByID(id); e != nil {
			labels[i] = e.Name
		}
	}
	if len(labels) == 0 {
		labels = []string{" "} // a DropDown needs one entry, or it offers the old ones
	}
	list := gtk.NewStringList(labels)
	*keep = list // the dropdown holds it, but Go must too
	dd.SetModel(list)
	dd.SetSelected(0)
	dd.SetSensitive(len(choices) > 0)
}

// fillAppMenuList fills box with one row per entry of list: the
// application's name and icon when it is installed, its plain name
// otherwise, and a button that removes it ("menu-off-remove:<id>").
func (s *shellUI) fillAppMenuList(box *gtk.Box, list []string, kind string) {
	gtkx.Clear(box)
	if len(list) == 0 {
		l := gtk.NewLabel(i18n.T("Nothing listed"))
		l.AddCssClass("sub")
		l.SetXalign(0)
		l.AddCssClass("row")
		gtkx.Append(box, &l.Widget)
		return
	}
	for _, id := range list {
		row := gtk.NewBox(gtk.OrientationHorizontalValue, 10)
		row.AddCssClass("row")
		img := gtk.NewImage()
		name := id
		if e := s.dockState.apps.ByID(id); e != nil {
			setIcon(img, e.Icon)
			name = e.Name
		} else if e := s.dockState.apps.ForClass(id); e != nil {
			setIcon(img, e.Icon)
			name = e.Name
		} else {
			img.SetFromIconName("application-x-executable-symbolic")
			name = i18n.Tf("%s (not installed)", id)
		}
		img.SetPixelSize(24)
		gtkx.Append(row, &img.Widget)
		l := gtk.NewLabel(name)
		l.AddCssClass("title")
		l.SetXalign(0)
		l.SetHexpand(true)
		gtkx.Append(row, &l.Widget)
		btn := gtk.NewButtonFromIconName("window-close-symbolic")
		btn.AddCssClass("plain")
		btn.SetName(fmt.Sprintf("%s-remove:%s", kind, id))
		btn.SetTooltipText(i18n.T("Show its menu again"))
		btn.SetValign(gtk.AlignCenterValue)
		btn.ConnectClicked(&s.onSettingsButton)
		gtkx.Append(row, &btn.Widget)
		gtkx.Append(box, &row.Widget)
	}
}

// pickAppMenuChoice is the ID selected in dd, from the choices ids gave
// it; "" when nothing is selected.
func pickAppMenuChoice(dd *gtk.DropDown, ids []string) string {
	i := int(dd.GetSelected())
	if i < 0 || i >= len(ids) {
		return ""
	}
	return ids[i]
}
