package ui

import (
	"context"
	"path/filepath"
	"strings"
	"time"

	"codeberg.org/puregotk/puregotk/v4/gio"
	"codeberg.org/puregotk/puregotk/v4/gtk"
	"github.com/godbus/dbus/v5"

	"github.com/lyricat/inua/internal/apps/backup"
	"github.com/lyricat/inua/internal/config"
	"github.com/lyricat/inua/internal/gtkx"
	"github.com/lyricat/inua/internal/i18n"
	"github.com/lyricat/inua/internal/keyring"
)

// backupSettings is the Backup page: the repository the settings are
// carried to, the token that writes them, what goes, and how often.
//
// It is kept beside config.toml in a file of its own (backup.json), because
// the settings window writes config.toml and a repository's schedule has no
// place in the shell's settings; the token is not in either, but in the
// Secret Service.
type backupSettings struct {
	repo, token                             gtk.Entry
	interval                                gtk.DropDown
	enable                                  gtk.Switch
	parts                                   gtk.Box
	switches                                []*gtk.Switch
	tokenState, checkState, state           gtk.Label
	check, now, open, tokenSave, tokenClear gtk.Button
	intervalKeys                            []string
	busy                                    bool // a push is running
}

// getBackupSettings finds the page's widgets, wires them to the handlers
// the other pages use, and fills them from the setup.
func (s *shellUI) getBackupSettings(ui *gtkx.Builder) {
	b := &s.settings.backup
	ui.Get("backup_repo", &b.repo)
	ui.Get("backup_token", &b.token)
	ui.Get("backup_interval", &b.interval)
	ui.Get("backup_enable", &b.enable)
	ui.Get("backup_parts", &b.parts)
	ui.Get("backup_token_state", &b.tokenState)
	ui.Get("backup_check_state", &b.checkState)
	ui.Get("backup_state", &b.state)
	ui.Get("backup_check", &b.check)
	ui.Get("backup_now", &b.now)
	ui.Get("backup_open", &b.open)
	ui.Get("backup_token_save", &b.tokenSave)
	ui.Get("backup_token_clear", &b.tokenClear)

	for _, it := range backup.Intervals {
		b.intervalKeys = append(b.intervalKeys, it.Key)
	}

	s.settings.entries[b.repo.GoPointer()] = &b.repo
	gtkx.ConnectChanged(&b.repo, &s.onSettingsEntry)
	b.enable.ConnectStateSet(&s.onSettingsSwitch)
	s.settings.drops[b.interval.GoPointer()] = &b.interval
	gtkx.ConnectNotify(&b.interval, "selected", &s.onSettingsDrop)
	for _, btn := range []*gtk.Button{&b.check, &b.now, &b.open, &b.tokenSave, &b.tokenClear} {
		btn.ConnectClicked(&s.onSettingsButton)
	}
	s.fillBackup()
}

// backupConfigDir is where the setup and its state live: the directory the
// shell's own settings are read from.
func (s *shellUI) backupConfigDir() string {
	if s.cfg.Dir != "" {
		return s.cfg.Dir
	}
	return parentDir(config.DefaultPath(), 2)
}

// fillBackup reads the setup into the controls.
func (s *shellUI) fillBackup() {
	b := &s.settings.backup
	setup, ok := backup.LoadSetup(s.backupConfigDir())
	if !ok {
		setup = backup.Setup{Parts: backup.DefaultParts(), Interval: "few"}
	}
	b.repo.SetText(setup.Repo)
	titles := make([]string, 0, len(backup.Intervals))
	for _, it := range backup.Intervals {
		titles = append(titles, it.Title)
	}
	list := gtk.NewStringList(titles)
	b.interval.SetModel(list)
	b.interval.SetSelected(uint32(indexIn(b.intervalKeys, setup.Interval)))
	b.enable.SetActive(setup.Enabled)
	s.fillBackupParts(setup.Parts)
	s.refreshBackupState()
}

// fillBackupParts puts a switch per part, in Settings' order.
func (s *shellUI) fillBackupParts(chosen []string) {
	b := &s.settings.backup
	b.switches = nil
	for child := b.parts.GetFirstChild(); child != nil; {
		next := child.GetNextSibling()
		b.parts.Remove(child)
		child = next
	}
	for _, part := range backup.Parts {
		row := gtk.NewBox(gtk.OrientationHorizontalValue, 8)
		sw := gtk.NewSwitch()
		sw.SetActive(indexIn(chosen, part.Key) >= 0)
		// A switch in the parts list saves the page, as the others do.
		sw.SetName("backup_" + part.Key)
		sw.ConnectStateSet(&s.onSettingsSwitch)
		label := gtk.NewLabel(part.Title)
		label.SetXalign(0)
		label.SetHexpand(true)
		row.Append(&sw.Widget)
		row.Append(&label.Widget)
		b.parts.Append(&row.Widget)
		b.switches = append(b.switches, sw)
	}
	b.parts.Show()
}

// refreshBackupState says what the last push did and whether a token is
// stored, without touching the network.
func (s *shellUI) refreshBackupState() {
	b := &s.settings.backup
	st := backup.LoadState(s.backupConfigDir())
	switch {
	case st.Last.IsZero():
		b.state.SetText(i18n.M("Not carried yet."))
	case st.Error != "":
		b.state.SetText(i18n.Tf("Last try %s failed: %s", shortAgo(st.Last), st.Error))
	default:
		b.state.SetText(i18n.Tf("Last carried %s: %d written, %d removed",
			shortAgo(st.Last), st.Pushed, st.Removed))
	}
	if token, ok, err := storedBackupToken(); err != nil {
		b.tokenState.SetText(i18n.Tf("The keyring could not be read: %s", err))
	} else if ok && token != "" {
		b.tokenState.SetText(i18n.M("A token is kept in the keyring"))
	} else {
		b.tokenState.SetText(i18n.M("No token yet: the backup cannot write"))
	}
}

// onBackupSave stores what the page says; onSettingsEntry, the interval and
// the switches call it when one of them changed.
func (s *shellUI) onBackupSave() {
	if s.settings.filling {
		return
	}
	b := &s.settings.backup
	dir := s.backupConfigDir()
	old, _ := backup.LoadSetup(dir)
	chosen := make([]string, 0, len(b.switches))
	for i, sw := range b.switches {
		if i < len(backup.Parts) && sw.GetActive() {
			chosen = append(chosen, backup.Parts[i].Key)
		}
	}
	interval := "few"
	if i := int(b.interval.GetSelected()); i >= 0 && i < len(b.intervalKeys) {
		interval = b.intervalKeys[i]
	}
	repo := strings.TrimSpace(b.repo.GetText())
	if repo == "" && !b.enable.GetActive() {
		return // nothing typed yet: not an edit worth saving
	}
	next := backup.Setup{
		Repo: repo, Branch: old.Branch, Parts: backup.NormaliseParts(chosen),
		Interval: interval, Enabled: b.enable.GetActive(),
		CommitterName: old.CommitterName, CommitterEmail: old.CommitterEmail,
	}
	if next.Branch == "" {
		next.Branch = "main"
	}
	if err := next.Validate(); err != nil {
		// The page says what is missing instead of writing a setup that
		// cannot push.
		b.checkState.SetText(err.Error())
		return
	}
	if err := backup.SaveSetup(dir, next); err != nil {
		b.checkState.SetText(err.Error())
		return
	}
	b.checkState.SetText(i18n.M("Saved."))
	s.refreshBackupState()
}

// onBackupCheck asks GitHub whether the token may write the repository,
// before anyone waits for a scheduled push to say so.
func (s *shellUI) onBackupCheck() {
	b := &s.settings.backup
	repo, err := backup.ParseRepo(strings.TrimSpace(b.repo.GetText()))
	if err != nil {
		b.checkState.SetText(err.Error())
		return
	}
	token, ok, err := storedBackupToken()
	if err != nil || !ok || token == "" {
		b.checkState.SetText(i18n.M("Save a token first."))
		return
	}
	b.checkState.SetText(i18n.M("Checking…"))
	api := backup.GitHub(token)
	go func() {
		branch, err := api.Check(context.Background(), repo)
		gtkx.Post(func() {
			if err != nil {
				b.checkState.SetText(err.Error())
				return
			}
			b.checkState.SetText(i18n.Tf("The token may write it; its branch is %s.", branch))
		})
	}()
}

// onBackupNow pushes at once, taking the schedule's turn by hand.
func (s *shellUI) onBackupNow() {
	b := &s.settings.backup
	if b.busy {
		return
	}
	dir := s.backupConfigDir()
	setup, ok := backup.LoadSetup(dir)
	if !ok {
		b.state.SetText(i18n.M("Save a repository and a token first."))
		return
	}
	token, ok, err := storedBackupToken()
	if err != nil || !ok || token == "" {
		b.state.SetText(i18n.M("Save a token first."))
		return
	}
	b.busy = true
	b.now.SetSensitive(false)
	b.state.SetText(i18n.M("Carrying…"))
	api := backup.GitHub(token)
	go func() {
		res, err := backup.Push(context.Background(), dir, setup, api)
		gtkx.Post(func() {
			b.busy = false
			b.now.SetSensitive(true)
			if err != nil {
				backup.SaveState(dir, backup.State{Last: res.When, Error: err.Error(), RepoKey: setup.Repo})
				b.state.SetText(err.Error())
				return
			}
			backup.SaveState(dir, backup.State{
				Last: res.When, Commit: res.Commit, Pushed: res.Pushed,
				Removed: res.Removed, RepoKey: setup.Repo,
			})
			if res.Commit == "" {
				b.state.SetText(i18n.M("Nothing changed since the last push."))
			} else {
				b.state.SetText(i18n.Tf("Carried %d file(s); %d removed", res.Pushed, res.Removed))
			}
			s.refreshBackupState()
		})
	}()
}

// onBackupOpen opens the repository's folder in a browser.
func (s *shellUI) onBackupOpen() {
	b := &s.settings.backup
	repo, err := backup.ParseRepo(strings.TrimSpace(b.repo.GetText()))
	if err != nil {
		b.checkState.SetText(err.Error())
		return
	}
	setup, _ := backup.LoadSetup(s.backupConfigDir())
	branch := setup.Branch
	if branch == "" {
		branch = "main"
	}
	if _, err := gio.AppInfoLaunchDefaultForUri(backup.WebURL(repo, branch), nil); err != nil {
		b.checkState.SetText(err.Error())
	}
}

// onBackupTokenSave stores the typed token in the Secret Service.
func (s *shellUI) onBackupTokenSave() {
	b := &s.settings.backup
	token := strings.TrimSpace(b.token.GetText())
	if token == "" {
		b.tokenState.SetText(i18n.M("Type the token first."))
		return
	}
	if err := putBackupToken(token); err != nil {
		b.tokenState.SetText(err.Error())
		return
	}
	b.token.SetText("")
	b.tokenState.SetText(i18n.M("The token is in the keyring"))
}

// onBackupTokenClear forgets the stored token.
func (s *shellUI) onBackupTokenClear() {
	b := &s.settings.backup
	if err := dropBackupToken(); err != nil {
		b.tokenState.SetText(err.Error())
		return
	}
	b.tokenState.SetText(i18n.M("No token yet: the backup cannot write"))
}

// storedBackupToken reads the token from the Secret Service.
func storedBackupToken() (string, bool, error) {
	conn, err := backupKeyring()
	if err != nil {
		return "", false, err
	}
	defer conn.Close()
	secret, found, err := conn.Lookup(context.Background(), backupTokenAttrs())
	if err != nil {
		return "", false, err
	}
	return string(secret), found, nil
}

func putBackupToken(token string) error {
	conn, err := backupKeyring()
	if err != nil {
		return err
	}
	defer conn.Close()
	return conn.Store(context.Background(), backupTokenLabel, backupTokenAttrs(), []byte(token))
}

func dropBackupToken() error {
	conn, err := backupKeyring()
	if err != nil {
		return err
	}
	defer conn.Close()
	return conn.Delete(backupTokenAttrs())
}

func backupKeyring() (*keyring.Client, error) {
	bus, err := dbus.ConnectSessionBus()
	if err != nil {
		return nil, err
	}
	return keyring.Connect(bus, keyring.AlgDH)
}

const backupTokenLabel = "inua: GitHub backup token"

func backupTokenAttrs() map[string]string {
	return map[string]string{"application": "inua", "purpose": "backup-github", "username": "inua-backup"}
}

// shortAgo says how long ago, as the page reads it.
func shortAgo(t time.Time) string {
	d := time.Since(t)
	switch {
	case d < time.Minute:
		return i18n.M("just now")
	case d < time.Hour:
		return i18n.Tf("%d minutes ago", int(d.Minutes()))
	case d < 24*time.Hour:
		return i18n.Tf("%d hours ago", int(d.Hours()))
	default:
		return i18n.Tf("%d days ago", int(d.Hours()/24))
	}
}

func indexIn(list []string, v string) int {
	for i, s := range list {
		if s == v {
			return i
		}
	}
	return 0
}

// parentDir climbs n directories.
func parentDir(path string, n int) string {
	for range n {
		path = filepath.Dir(path)
	}
	return path
}

// backupButton dispatches the Backup page's own buttons by their builder
// id, the way the other pages do.
func (s *shellUI) backupButton(name string) bool {
	switch name {
	case "backup_check":
		s.onBackupCheck()
	case "backup_now":
		s.onBackupNow()
	case "backup_open":
		s.onBackupOpen()
	case "backup_token_save":
		s.onBackupTokenSave()
	case "backup_token_clear":
		s.onBackupTokenClear()
	default:
		return false
	}
	return true
}
