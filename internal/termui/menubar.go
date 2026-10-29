package termui

import (
	"codeberg.org/puregotk/puregotk/v4/gio"

	"github.com/lyricat/inua/internal/appui"
	"github.com/lyricat/inua/internal/i18n"
	"github.com/lyricat/inua/internal/term/settings"
)

// menuBar gives the window's actions, as the command palette has them, in
// menus. The keys stay the window's own (chord): the menus show none, so a
// chord never runs twice.
func (a *App) menuBar() {
	a.onMenuItem = func(act gio.SimpleAction, _ uintptr) {
		switch name := act.GetName(); name {
		case "quit":
			a.c.App.Quit()
		default:
			a.do(name, a.focusedPane())
		}
	}
	groups := []appui.MenuGroup{
		{Title: "Terminal", Sections: []appui.MenuSection{{Actions: []appui.MenuAction{{Name: "settings", Label: "Settings", Activate: a.onMenuItem}}}, {Actions: []appui.MenuAction{{Name: "restart_host", Label: "Restart Host", Activate: a.onMenuItem}}}, {Actions: []appui.MenuAction{{Name: "quit", Label: "Quit", Activate: a.onMenuItem}}}}},
		{Title: "Shell", Sections: []appui.MenuSection{{Actions: []appui.MenuAction{{Name: "new_session", Label: "New Session", Activate: a.onMenuItem}, {Name: "new_workspace", Label: "New Workspace", Activate: a.onMenuItem}}}, {Actions: []appui.MenuAction{{Name: "split_right", Label: "Split Right", Activate: a.onMenuItem}, {Name: "split_down", Label: "Split Down", Activate: a.onMenuItem}, {Name: "close_pane", Label: "Close Pane", Activate: a.onMenuItem}}}, {Actions: []appui.MenuAction{{Name: "rename", Label: "Rename", Activate: a.onMenuItem}}}}},
		{Title: "Edit", Sections: []appui.MenuSection{{Actions: []appui.MenuAction{{Name: "copy", Label: "Copy", Activate: a.onMenuItem}, {Name: "paste", Label: "Paste", Activate: a.onMenuItem}}}, {Actions: []appui.MenuAction{{Name: "find", Label: "Find", Activate: a.onMenuItem}, {Name: "copy_mode", Label: "Copy Mode", Activate: a.onMenuItem}}}}},
		{Title: "View", Sections: []appui.MenuSection{{Actions: []appui.MenuAction{{Name: "zoom", Label: "Zoom", Activate: a.onMenuItem}, {Name: "equalize", Label: "Equalize", Activate: a.onMenuItem}, {Name: "next_layout", Label: "Next Layout", Activate: a.onMenuItem}, {Name: "swap", Label: "Swap", Activate: a.onMenuItem}}}, {Actions: []appui.MenuAction{{Name: "fold_workspaces", Label: "Fold Workspaces", Activate: a.onMenuItem}, {Name: "fold_sessions", Label: "Fold Sessions", Activate: a.onMenuItem}}}, {Actions: []appui.MenuAction{{Label: "Font", Children: []appui.MenuAction{{Name: "font_larger", Label: "Larger Font", Activate: a.onMenuItem}, {Name: "font_smaller", Label: "Smaller Font", Activate: a.onMenuItem}, {Name: "font_reset", Label: "Reset Font", Activate: a.onMenuItem}}}}}}},
		{Title: "Window", Sections: []appui.MenuSection{{Actions: []appui.MenuAction{{Name: "previous_session", Label: "Previous Session", Activate: a.onMenuItem}, {Name: "next_session", Label: "Next Session", Activate: a.onMenuItem}}}, {Actions: []appui.MenuAction{{Name: "next_waiting", Label: "Next Waiting", Activate: a.onMenuItem}, {Name: "next_idle", Label: "Next Idle", Activate: a.onMenuItem}, {Name: "agents", Label: "Agents", Activate: a.onMenuItem}}}}},
		{Title: "Help", Sections: []appui.MenuSection{{Actions: []appui.MenuAction{{Name: "palette", Label: "Command Palette", Activate: a.onMenuItem}, {Name: "keys", Label: "Keyboard Shortcuts", Activate: a.onMenuItem}}}}},
	}
	labels := make(map[string]string, len(settings.Actions))
	for _, act := range settings.Actions {
		labels[act.Name] = i18n.T(act.Label)
	}
	for gi := range groups {
		for si := range groups[gi].Sections {
			for ai := range groups[gi].Sections[si].Actions {
				item := &groups[gi].Sections[si].Actions[ai]
				if label := labels[item.Name]; label != "" {
					item.Label = label
				}
			}
		}
	}
	bar := appui.NewMenuBar(a.c, groups)
	a.c.App.SetMenubar(&bar.Model.MenuModel)
	a.win.SetShowMenubar(true)
}

// focusedPane is the pane that has the keys, or nil.
func (a *App) focusedPane() *termPane {
	for _, t := range a.tiles {
		if p := t.pane; p != nil && p.widget.HasFocus() {
			return p
		}
	}
	return nil
}
