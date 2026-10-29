package appui

import (
	"codeberg.org/puregotk/puregotk/v4/gio"
	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/i18n"
)

// MenuAction is one app-specific command in a MenuBar. Name is local to its
// MenuSpec prefix; Label is an i18n message key. Activate runs on GTK's main
// thread when the user invokes the command.
type MenuAction struct {
	Name     string
	Label    string
	Activate func(gio.SimpleAction, uintptr)
}

// MenuSpec groups one window's actions under a unique GAction prefix. Prefix
// is required when multiple windows share an application action namespace.
type MenuSpec struct {
	Prefix string
}

// MenuSection groups related commands with a separator.
type MenuSection struct {
	Actions []MenuAction
}

// MenuGroup is a top-level menu, such as File, Edit, or Help.
type MenuGroup struct {
	Title    string // i18n message key
	Sections []MenuSection
}

// MenuBar owns the menu model and its local GTK menu bar. Keep it reachable
// for as long as the window is open; GTK owns the attached widget as well.
type MenuBar struct {
	Model  *gio.Menu
	Widget *gtk.PopoverMenuBar
	group  *gio.SimpleActionGroup
}

// NewMenuBar creates app-specific GActions and a GMenu model. Prefix is
// prepended to each action name in the application's GAction namespace, so
// separate windows can use identical local names. Labels and group titles are
// translated with i18n.T. Every action requires a name, label, and callback.
func NewMenuBar(c *Ctx, groups []MenuGroup) *MenuBar {
	bar := gio.NewMenu()
	actions := gio.NewSimpleActionGroup()
	for _, group := range groups {
		submenu := gio.NewMenu()
		for _, section := range group.Sections {
			items := gio.NewMenu()
			for _, item := range section.Actions {
				actionName := item.Name
				action := gio.NewSimpleAction(actionName, nil)
				action.ConnectActivate(&item.Activate)
				actions.AddAction(action)
				action.Unref()
				items.Append(i18n.T(item.Label), "app."+actionName)
			}
			submenu.AppendSection("", &items.MenuModel)
			items.Unref()
		}
		bar.AppendSubmenu(i18n.T(group.Title), &submenu.MenuModel)
		submenu.Unref()
	}
	widget := gtk.NewPopoverMenuBarFromModel(&bar.MenuModel)
	widget.InsertActionGroup("app", actions)
	return &MenuBar{Model: bar, Widget: widget, group: actions}
}

// AppendLocal inserts the menu bar at the start of a vertical window layout.
// Use gtkx.Prepend or gtkx.Append around the widget for container layouts.
func (m *MenuBar) AppendLocal(box *gtk.Box) {
	box.Prepend(&m.Widget.Widget)
}
