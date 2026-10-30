package shell

import (
	"fmt"
	"slices"
	"strings"

	"github.com/lyricat/inua/internal/desktop"
	"github.com/lyricat/inua/internal/i18n"
)

// ItemAction is one of the things a launcher result can do besides its
// own (Enter's), which Tab opens: ID names it for the view, Title is its
// label.
type ItemAction struct {
	ID, Title string
}

// ItemActions are what result r can do: an app opened, another window of
// it opened (windows of them open), its own actions ("own-0" its first),
// kept in the dock or taken out of it (pinned), its windows closed; a
// window focused, closed, floated, made fullscreen or centred; an answer
// copied, an address opened. Nil for a result with nothing more than
// Enter does.
func ItemActions(r Result, pinned bool, windows int) []ItemAction {
	switch {
	case r.Entry != nil:
		acts := []ItemAction{{"open", i18n.T("Open")}}
		// The shell's tools have one window; an app with a New Window of
		// its own shows that one.
		own := slices.ContainsFunc(r.Entry.Actions, func(a desktop.Action) bool { return a.ID == "new-window" })
		if windows > 0 && !own && !strings.HasPrefix(r.Entry.ID, "inua:") {
			acts = append(acts, ItemAction{"new", i18n.T("New Window")})
		}
		for i, a := range r.Entry.Actions {
			acts = append(acts, ItemAction{fmt.Sprintf("own-%d", i), a.Name})
		}
		if pinned {
			acts = append(acts, ItemAction{"unpin", i18n.T("Remove from Dock")})
		} else {
			acts = append(acts, ItemAction{"pin", i18n.T("Keep in Dock")})
		}
		switch {
		case windows == 1:
			acts = append(acts, ItemAction{"quit", i18n.T("Quit")})
		case windows > 1:
			acts = append(acts, ItemAction{"quit", i18n.Tf("Quit (%d windows)", windows)})
		}
		return acts
	case r.Address != "":
		return []ItemAction{
			{"focus", i18n.T("Switch to")},
			{"close-window", i18n.T("Close")},
			{"float", i18n.T("Toggle Floating")},
			{"fullscreen", i18n.T("Toggle Fullscreen")},
			{"center", i18n.T("Center")},
		}
	case r.Copy != "":
		return []ItemAction{{"copy", i18n.T("Copy")}}
	case r.URL != "":
		return []ItemAction{{"open-url", i18n.T("Open")}, {"copy-url", i18n.T("Copy Address")}}
	}
	return nil
}
