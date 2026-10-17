package ui

import (
	"context"
	"log"
	"strings"
	"time"

	"codeberg.org/puregotk/puregotk/v4/glib"

	"github.com/lyricat/inua/internal/apps/backup"
	"github.com/lyricat/inua/internal/gtkx"
	"github.com/lyricat/inua/internal/i18n"
	"github.com/lyricat/inua/internal/notify"
)

// backupTick is how often the shell looks at the schedule. It is not the
// interval itself: the check is a file read, and five minutes is often
// enough for an hour's interval to be met within five minutes of it.
const backupTick = 5 * time.Minute

// startBackupSchedule has the shell offer a push when the setup is due, so
// the settings are carried without anyone opening Settings. A push is not
// retried in a tight loop: Due() asks again only after the interval, or at
// once after a failure, which the tick bounds.
func (s *shellUI) startBackupSchedule() {
	s.onBackupTick = func(uintptr) bool {
		s.checkBackupSchedule()
		return true
	}
	// The first check waits a moment: a login is busy enough already.
	glib.TimeoutAdd(2*60*1000, &s.onBackupTick, 0)
}

// checkBackupSchedule pushes once when the schedule says it is due.
func (s *shellUI) checkBackupSchedule() {
	dir := s.backupConfigDir()
	setup, ok := backup.LoadSetup(dir)
	if !ok || !backup.Due(dir, setup, time.Now()) {
		return
	}
	token, ok, err := storedBackupToken()
	if err != nil || !ok || token == "" {
		// The setup says "carry it" but no token can write it: say so once
		// in the log rather than once per tick in a notification.
		if err == nil {
			return
		}
		log.Printf("backup: the keyring: %v", err)
		return
	}
	api := backup.GitHub(token)
	go func() {
		res, err := backup.Push(context.Background(), dir, setup, api)
		gtkx.Post(func() {
			if err != nil {
				backup.SaveState(dir, backup.State{Last: res.When, Error: err.Error(), RepoKey: setup.Repo})
				log.Printf("backup: %v", err)
				// A failed scheduled push is worth a banner once: it means
				// the settings stopped being carried.
				s.postNote(backupNote(i18n.T("The settings were not carried"), err.Error(), true))
				return
			}
			backup.SaveState(dir, backup.State{
				Last: res.When, Commit: res.Commit, Pushed: res.Pushed,
				Removed: res.Removed, RepoKey: setup.Repo,
			})
			if res.Commit != "" {
				log.Printf("backup: %d file(s) carried to %s", res.Pushed, setup.Repo)
			}
		})
	}()
}

// backupNote is the banner a failed carry shows.
func backupNote(summary, body string, urgent bool) notify.Notification {
	n := notify.Notification{
		App: i18n.T("Backup"), Entry: "inua-backup", Icon: "go-cloud-symbolic",
		Summary: summary, Body: notify.Markup(notifyEscape(body)), Time: time.Now(),
	}
	if urgent {
		n.Urgency = notify.Critical
	}
	return n
}

// notifyEscape keeps a message's own markup from breaking the banner.
func notifyEscape(s string) string {
	r := strings.NewReplacer("&", "&amp;", "<", "&lt;", ">", "&gt;")
	return r.Replace(s)
}
