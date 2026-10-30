package lobby

import "github.com/lyricat/inua/internal/i18n"

// webTexts are the page's words in the lobby's language; formats keep
// their verbs (%s, %d) for the page to fill in.
func webTexts() map[string]any {
	return map[string]any{
		"title":        i18n.T("Game Lobby"),
		"sub":          i18n.T("Join a game at a table, or watch one. A host opens a game here from Small Fortune or Chinese Checkers in inua."),
		"table":        i18n.T("TABLE %d"),
		"free":         i18n.T("Free"),
		"freeNote":     i18n.T("A host can open a game here."),
		"away":         i18n.T("The host’s connection dropped: waiting for it to come back…"),
		"reconnecting": i18n.T("Reconnecting…"),
		"lobby":        i18n.T("Waiting to start"),
		"room":         i18n.T("Open seats: %d"),
		"playing":      i18n.T("Playing"),
		"over":         i18n.T("Over"),
		"join":         i18n.T("Join"),
		"watch":        i18n.T("Watch"),
		"leads":        i18n.T("%s sets up the game"),
		"open":         i18n.T("Open seat"),
		"local":        i18n.T("at the host's screen"),
		"visitor":      i18n.T("in a browser"),
		"computer":     i18n.T("computer"),
		"ai":           i18n.T("AI"),
		"reconnect":    i18n.T("Connection lost: trying again…"),
		"games": map[string]string{
			"small-fortune":    i18n.T("Small Fortune"),
			"chinese-checkers": i18n.T("Chinese Checkers"),
		},
	}
}
