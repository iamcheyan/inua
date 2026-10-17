package main

import (
	"bufio"
	"context"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	"golang.org/x/term"

	"github.com/godbus/dbus/v5"

	"github.com/lyricat/inua/internal/apps/backup"
	"github.com/lyricat/inua/internal/config"
	"github.com/lyricat/inua/internal/keyring"
)

// cmdBackup is `inua backup`: the setup carried to a GitHub repository.
//
//	inua backup                          what the setup is, and when it last ran
//	inua backup push [--repo owner/name] [--token T] [--branch B]
//	                                     carry the chosen parts now
//	inua backup pull [--repo owner/name] [--token T] [--branch B] [--parts a,b]
//	                                     bring another computer's copy here
//	inua backup parts                    the parts that can be carried
//	inua backup token [-delete]          the token in the Secret Service
func cmdBackup(args []string) error {
	if len(args) == 0 {
		return backupStatus()
	}
	switch args[0] {
	case "push":
		return backupPush(args[1:])
	case "pull":
		return backupPull(args[1:])
	case "parts":
		for _, p := range backup.Parts {
			mark := " "
			if contains(backup.DefaultParts(), p.Key) {
				mark = "*"
			}
			fmt.Printf("%s %-10s %s\n", mark, p.Key, p.Title)
		}
		fmt.Println("\n* is carried by a new setup")
		return nil
	case "token":
		return backupToken(args[1:])
	default:
		return fmt.Errorf("unknown command %q (inua backup [push|pull|parts|token])", args[0])
	}
}

// configDir is inua's configuration directory, where backup.json sits
// beside config.toml, honouring a $XDG_CONFIG_HOME the session set.
func configDir() string {
	return filepath.Dir(filepath.Dir(config.DefaultPath()))
}

// backupStatus says what the setup is, without touching the network.
func backupStatus() error {
	dir := configDir()
	s, ok := backup.LoadSetup(dir)
	if !ok {
		fmt.Println("inua: no backup setup yet.")
		fmt.Println("Open Settings → Backup, or run `inua backup push --repo owner/name`.")
		return nil
	}
	st := backup.LoadState(dir)
	fmt.Printf("repository  %s (branch %s)\n", s.Repo, branchOf(s))
	fmt.Printf("parts       %s\n", backup.TitlesOf(s.Parts))
	if s.Enabled {
		fmt.Printf("schedule    %s\n", s.Interval)
		if next := backup.NextPush(dir, s); !next.IsZero() {
			fmt.Printf("next        %s\n", humanUntil(next))
		}
	} else {
		fmt.Println("schedule    off; push by hand")
	}
	switch {
	case st.Last.IsZero():
		fmt.Println("last        never")
	case st.Error != "":
		fmt.Printf("last        %s, failed: %s\n", humanUntil(st.Last), st.Error)
	default:
		fmt.Printf("last        %s, %d written, %d removed\n", humanUntil(st.Last), st.Pushed, st.Removed)
		if st.Commit != "" {
			fmt.Printf("commit      %s\n", st.Commit)
		}
	}
	return nil
}

func branchOf(s backup.Setup) string {
	if s.Branch == "" {
		return "main"
	}
	return s.Branch
}

// humanUntil says how long ago or from now, the way a person reads it.
func humanUntil(t time.Time) string {
	d := time.Since(t)
	switch {
	case d < 0:
		d = -d
		return "in " + shortDuration(d)
	case d < time.Minute:
		return "just now"
	default:
		return shortDuration(d) + " ago"
	}
}

func shortDuration(d time.Duration) string {
	switch {
	case d < time.Minute:
		return fmt.Sprintf("%ds", int(d.Seconds()))
	case d < time.Hour:
		return fmt.Sprintf("%dm", int(d.Minutes()))
	case d < 24*time.Hour:
		return fmt.Sprintf("%dh", int(d.Hours()))
	default:
		return fmt.Sprintf("%dd", int(d.Hours()/24))
	}
}

// backupFlags are the switches push and pull share: a repository, token and
// branch given for one run, over the saved setup.
type backupFlags struct {
	repo, token, branch string
	parts               string
}

func parseBackupFlags(name string, args []string) (backupFlags, error) {
	var f backupFlags
	for i := 0; i < len(args); i++ {
		switch a := args[i]; {
		case a == "--repo" && i+1 < len(args):
			i++
			f.repo = args[i]
		case a == "--token" && i+1 < len(args):
			i++
			f.token = args[i]
		case a == "--branch" && i+1 < len(args):
			i++
			f.branch = args[i]
		case a == "--parts" && i+1 < len(args):
			i++
			f.parts = args[i]
		default:
			return f, fmt.Errorf("unknown argument %q (inua backup %s [--repo owner/name] [--token T] [--branch B] [--parts a,b])", a, name)
		}
	}
	return f, nil
}

// backupPush carries the chosen parts now.
func backupPush(args []string) error {
	f, err := parseBackupFlags("push", args)
	if err != nil {
		return err
	}
	dir := configDir()
	s, ok := backup.LoadSetup(dir)
	if !ok {
		// A first push from the command line: name a repository and go.
		if f.repo == "" {
			return errors.New("no backup setup yet: inua backup push --repo owner/name")
		}
		s = backup.Setup{
			Repo: f.repo, Branch: orMain(f.branch), Parts: backup.DefaultParts(),
			Interval: "few", Enabled: true,
		}
	}
	if f.repo != "" {
		s.Repo = f.repo
	}
	if f.branch != "" {
		s.Branch = f.branch
	}
	if f.parts != "" {
		s.Parts = backup.NormaliseParts(strings.Split(f.parts, ","))
	}
	if s.Branch == "" {
		s.Branch = "main"
	}

	token, err := backupTokenValue(f.token)
	if err != nil {
		return err
	}
	api := backup.GitHub(token)

	branch, err := api.Check(context.Background(), mustRepo(s.Repo))
	if err != nil {
		return err
	}
	if f.branch == "" && s.Branch != branch {
		// The repository names its own branch: push where a reader looks.
		s.Branch = branch
	}

	res, err := backup.Push(context.Background(), dir, s, api)
	if err != nil {
		backup.SaveState(dir, backup.State{
			Last: time.Now(), Error: err.Error(), RepoKey: s.Repo,
		})
		return err
	}
	state := backup.State{Last: res.When, Commit: res.Commit, Pushed: res.Pushed, Removed: res.Removed, RepoKey: s.Repo}
	backup.SaveState(dir, state)
	if err := backup.SaveSetup(dir, s); err != nil {
		return err
	}

	for _, part := range res.Missing {
		fmt.Printf("inua: %s has no file yet; carried at the next push\n", part)
	}
	if res.Commit == "" {
		fmt.Println("inua: nothing changed since the last push")
		return nil
	}
	fmt.Printf("inua: backed up %d file(s)", res.Pushed)
	if res.Removed > 0 {
		fmt.Printf(", removed %d", res.Removed)
	}
	fmt.Printf(" to %s\n%s\n", s.Repo, res.URL)
	return nil
}

func orMain(b string) string {
	if b == "" {
		return "main"
	}
	return b
}

// backupPull brings another computer's copy into this one, writing only
// what is not here: a part this computer already has is left alone, so a
// pull never overwrites what someone edited.
func backupPull(args []string) error {
	f, err := parseBackupFlags("pull", args)
	if err != nil {
		return err
	}
	dir := configDir()
	s, ok := backup.LoadSetup(dir)
	if !ok {
		if f.repo == "" {
			return errors.New("no backup setup yet: inua backup pull --repo owner/name")
		}
		s = backup.Setup{Repo: f.repo, Branch: orMain(f.branch), Parts: backup.DefaultParts(), Interval: "few"}
	}
	if f.repo != "" {
		s.Repo = f.repo
	}
	if f.branch != "" {
		s.Branch = f.branch
	}
	parts := s.Parts
	if f.parts != "" {
		parts = backup.NormaliseParts(strings.Split(f.parts, ","))
	}

	token, err := backupTokenValue(f.token)
	if err != nil {
		return err
	}
	api := backup.GitHub(token)
	repo := mustRepo(s.Repo)
	ctx := context.Background()
	if _, err := api.Check(ctx, repo); err != nil {
		return err
	}

	total, kept := 0, 0
	for _, key := range parts {
		part, ok := backup.PartNamed(key)
		if !ok {
			continue
		}
		files, err := api.Pull(ctx, repo, branchOf(s), part)
		if err != nil {
			return err
		}
		for _, file := range files {
			dest := filepath.Join(dir, filepath.FromSlash(file.Path))
			if existing, err := os.ReadFile(dest); err == nil {
				if backup.BlobSum(existing) == file.Sum {
					continue
				}
				// Here, and different: this computer's copy is the one
				// someone used, so it stays and the pull says so.
				fmt.Printf("inua: %s: kept this computer's copy\n", file.Path)
				kept++
				continue
			}
			if err := os.MkdirAll(filepath.Dir(dest), 0o755); err != nil {
				return err
			}
			if err := os.WriteFile(dest, file.Data, 0o644); err != nil {
				return err
			}
			fmt.Printf("inua: wrote %s\n", file.Path)
			total++
		}
	}
	if total == 0 && kept == 0 {
		fmt.Println("inua: this computer already has everything in the backup")
	}
	return nil
}

func mustRepo(s string) backup.Repo {
	r, err := backup.ParseRepo(s)
	if err != nil {
		// Push and Pull validate first; an unparsable address has been
		// refused by then, and an empty one is a setup with no repository.
		return backup.Repo{}
	}
	return r
}

// backupTokenValue takes the token from the flag, else the Secret Service.
func backupTokenValue(flagValue string) (string, error) {
	if flagValue != "" {
		return flagValue, nil
	}
	token, ok, err := storedToken()
	if err != nil {
		return "", err
	}
	if !ok || token == "" {
		return "", errors.New("no GitHub token yet: Settings → Backup, or `inua backup token` to store one")
	}
	return token, nil
}

// tokenLabel and tokenAttrs name the token in the Secret Service: one item,
// beside the apps' other secrets.
const (
	tokenLabel = "inua: GitHub backup token"
	tokenUser  = "inua-backup"
)

func tokenAttrs() map[string]string {
	return map[string]string{"application": "inua", "purpose": "backup-github", "username": tokenUser}
}

// cmdBackupToken stores a token read from the terminal, or deletes it.
func backupToken(args []string) error {
	deleteOnly := false
	for _, a := range args {
		switch a {
		case "-delete", "--delete":
			deleteOnly = true
		default:
			return fmt.Errorf("unknown argument %q (inua backup token [-delete])", a)
		}
	}
	bus, err := dbus.ConnectSessionBus()
	if err != nil {
		return fmt.Errorf("the session bus: %w", err)
	}
	defer bus.Close()
	conn, err := keyring.Connect(bus, keyring.AlgDH)
	if err != nil {
		return fmt.Errorf("the Secret Service: %w", err)
	}
	if deleteOnly {
		if err := conn.Delete(tokenAttrs()); err != nil {
			return err
		}
		fmt.Println("inua: the GitHub token is gone")
		return nil
	}
	fmt.Fprint(os.Stderr, "GitHub token (contents:read and write on the one repository, hidden as you type): ")
	token, err := readSecret()
	if err != nil {
		return err
	}
	if token == "" {
		return errors.New("an empty token is not stored")
	}
	api := backup.GitHub(token)
	if _, err := api.Check(context.Background(), backup.Repo{Owner: "-", Name: "-"}); err != nil &&
		!strings.Contains(err.Error(), "no such repository") {
		// A refused token is worth saying now; a repository that does not
		// exist yet is not, as the token itself may still be good.
		return fmt.Errorf("the token was refused: %w", err)
	}
	if err := conn.Store(context.Background(), tokenLabel, tokenAttrs(), []byte(token)); err != nil {
		return err
	}
	fmt.Println("inua: the token is in the Secret Service, where the backup reads it")
	return nil
}

func contains(list []string, v string) bool {
	for _, s := range list {
		if s == v {
			return true
		}
	}
	return false
}

// storedToken reads the token from the Secret Service; false when none is
// stored.
func storedToken() (string, bool, error) {
	bus, err := dbus.ConnectSessionBus()
	if err != nil {
		return "", false, fmt.Errorf("the session bus: %w", err)
	}
	defer bus.Close()
	conn, err := keyring.Connect(bus, keyring.AlgDH)
	if err != nil {
		return "", false, fmt.Errorf("the Secret Service: %w", err)
	}
	defer conn.Close()
	secret, found, err := conn.Lookup(context.Background(), tokenAttrs())
	if err != nil {
		return "", false, err
	}
	if !found {
		return "", false, nil
	}
	return string(secret), true, nil
}

// readSecret reads a line from the terminal without echoing it.
func readSecret() (string, error) {
	fd := int(os.Stdin.Fd())
	if !term.IsTerminal(fd) {
		// Piped: read the line as it comes, for a script or a test.
		line, err := bufio.NewReader(os.Stdin).ReadString('\n')
		if err != nil && line == "" {
			return "", err
		}
		return strings.TrimRight(line, "\r\n"), nil
	}
	b, err := term.ReadPassword(fd)
	fmt.Fprintln(os.Stderr)
	if err != nil {
		return "", err
	}
	return strings.TrimSpace(string(b)), nil
}
