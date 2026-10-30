package termui

import "codeberg.org/puregotk/puregotk/v4/gtk"

// Narrow windows fold column 2, then column 1, so the terminals keep
// their width (section 3); Ctrl+Shift+S and Ctrl+Shift+B show a folded
// one anyway, or fold one the window has room for.

// narrow are the widths below which each column folds by itself.
var narrow = [2]int{720, 1040}

// wantFolds is which columns should show now.
func (a *App) wantFolds() [2]bool {
	w := int(a.win.GetWidth())
	var show [2]bool
	for i := range show {
		show[i] = !a.fold[i] && (w == 0 || w >= narrow[i] || a.peek[i])
	}
	return show
}

// folds is which columns show.
func (a *App) folds() [2]bool {
	return [2]bool{a.cols.col1Reveal.GetRevealChild(), a.cols.col2.GetVisible()}
}

func (a *App) applyFolds() {
	show := a.wantFolds()
	if r := a.cols.col1Reveal; r.GetRevealChild() != show[0] {
		if r.GetTransitionDuration() > 0 && r.GetMapped() && gtk.SettingsGetDefault().GetPropertyGtkEnableAnimations() {
			a.holdSizes(true) // until it has slid
		}
		r.SetRevealChild(show[0]) // it slides, its grip with it
	}
	a.cols.col2.SetVisible(show[1])
	a.cols.grips[1].SetVisible(show[1])
	a.cols.sidebarShowHead.SetVisible(!show[0])
}

// toggleColumn shows or hides column i: in a window too narrow for it, for
// now; else as the user keeps it.
func (a *App) toggleColumn(i int) {
	if w := int(a.win.GetWidth()); w > 0 && w < narrow[i] && !a.fold[i] {
		a.peek[i] = !a.peek[i]
	} else {
		a.fold[i] = !a.fold[i]
		a.peek[i] = false
	}
	a.applyFolds()
}
