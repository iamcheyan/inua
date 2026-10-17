package backup

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"
)

// Every is how often the shell offers to push when the settings say "every
// few hours"; Settings offers the others.
var Intervals = []struct {
	Key, Title string
	Every      time.Duration
}{
	{"hourly", "Every hour", time.Hour},
	{"few", "Every few hours", 4 * time.Hour},
	{"daily", "Once a day", 24 * time.Hour},
	{"weekly", "Once a week", 7 * 24 * time.Hour},
}

// IntervalNamed finds an interval by its key, and its length.
func IntervalNamed(key string) (time.Duration, bool) {
	for _, i := range Intervals {
		if i.Key == key {
			return i.Every, true
		}
	}
	return 0, false
}

// Setup is where the backup goes and what it carries, kept in
// $XDG_CONFIG_HOME/inua/backup.json with the token in the Secret Service
// beside it. A file of its own rather than config.toml: the settings window
// writes config.toml, and a token has no place in either.
type Setup struct {
	// Repo is "owner/name" of a repository the token may write.
	Repo string `json:"repo"`
	// Branch is the branch pushed to; the repository's default when empty.
	Branch string `json:"branch,omitempty"`
	// Parts are the keys of Parts to carry.
	Parts []string `json:"parts"`
	// Interval is a key of Intervals.
	Interval string `json:"interval"`
	// Enabled turns the scheduled push on; a push made by hand runs anyway.
	Enabled bool `json:"enabled"`
	// Committer is the name and address the commits carry, so a repository
	// of one's own desktop does not read as a stranger's.
	CommitterName  string `json:"committer_name,omitempty"`
	CommitterEmail string `json:"committer_email,omitempty"`
}

// Dir is where the setup and the sync's state live: beside config.toml.
func Dir(configDir string) string { return filepath.Join(configDir, "inua") }

func setupPath(configDir string) string { return filepath.Join(Dir(configDir), "backup.json") }
func statePath(configDir string) string { return filepath.Join(Dir(configDir), "backup-state.json") }

// LoadSetup reads the setup; false when there is none.
func LoadSetup(configDir string) (Setup, bool) {
	var s Setup
	b, err := os.ReadFile(setupPath(configDir))
	if err != nil || json.Unmarshal(b, &s) != nil || s.Repo == "" {
		return Setup{}, false
	}
	return s.withDefaults(), true
}

// withDefaults fills what a setup made by an older build left out.
func (s Setup) withDefaults() Setup {
	if len(s.Parts) == 0 {
		s.Parts = DefaultParts()
	}
	if s.Interval == "" {
		s.Interval = "few"
	}
	if s.Branch == "" {
		s.Branch = "main"
	}
	return s
}

// Validate checks a setup before it is saved and says what is wrong.
func (s Setup) Validate() error {
	if _, err := ParseRepo(s.Repo); err != nil {
		return err
	}
	if len(s.Parts) == 0 {
		return errors.New("choose at least one part to carry")
	}
	for _, k := range s.Parts {
		if _, ok := PartNamed(k); !ok {
			return fmt.Errorf("unknown part %q", k)
		}
	}
	if _, ok := IntervalNamed(s.Interval); !ok {
		return fmt.Errorf("unknown interval %q", s.Interval)
	}
	return nil
}

// SaveSetup writes the setup, readable by the user alone as it names a
// repository and a schedule.
func SaveSetup(configDir string, s Setup) error {
	if err := s.Validate(); err != nil {
		return err
	}
	if s.Branch == "" {
		s.Branch = "main"
	}
	b, err := json.MarshalIndent(s, "", "  ")
	if err != nil {
		return err
	}
	if err := os.MkdirAll(Dir(configDir), 0o755); err != nil {
		return err
	}
	tmp := setupPath(configDir) + ".tmp"
	if err := os.WriteFile(tmp, b, 0o600); err != nil {
		return err
	}
	return os.Rename(tmp, setupPath(configDir))
}

// State is what the last push saw, so Settings can say when it ran and what
// went wrong, and so a push can tell a change it made from one another
// computer made.
type State struct {
	Last     time.Time `json:"last,omitzero"`
	Commit   string    `json:"commit,omitempty"`
	Error    string    `json:"error,omitempty"`
	Pushed   int       `json:"pushed,omitempty"`  // files written
	Removed  int       `json:"removed,omitempty"` // paths deleted
	RepoKey  string    `json:"repo_key,omitempty"`
	LocalSum string    `json:"local_sum,omitempty"` // what was carried, hashed
}

// LoadState reads the last push's record; a missing one is a zero State.
func LoadState(configDir string) State {
	var st State
	b, err := os.ReadFile(statePath(configDir))
	if err != nil || json.Unmarshal(b, &st) != nil {
		return State{}
	}
	return st
}

// SaveState records a push's outcome.
func SaveState(configDir string, st State) error {
	b, err := json.MarshalIndent(st, "", "  ")
	if err != nil {
		return err
	}
	if err := os.MkdirAll(Dir(configDir), 0o755); err != nil {
		return err
	}
	tmp := statePath(configDir) + ".tmp"
	if err := os.WriteFile(tmp, b, 0o600); err != nil {
		return err
	}
	return os.Rename(tmp, statePath(configDir))
}

// Result is what a push did, in the words Settings shows.
type Result struct {
	Pushed  int       // files written
	Removed int       // paths deleted
	Commit  string    // the commit made, empty when nothing changed
	When    time.Time // when the push ran
	Missing []string  // parts with nothing to carry yet
	URL     string    // the backup's page, when one was made
}

// Push collects the chosen parts and pushes what changed. It is the work
// behind `inua backup push` and behind the schedule.
func Push(ctx context.Context, configDir string, s Setup, api *API) (Result, error) {
	if err := s.Validate(); err != nil {
		return Result{}, err
	}
	repo, err := ParseRepo(s.Repo)
	if err != nil {
		return Result{}, err
	}
	files, missing, err := Collect(configDir, s.Parts)
	if err != nil {
		return Result{}, err
	}
	if len(files) == 0 {
		return Result{Missing: missing, When: time.Now()},
			errors.New("there is nothing to carry yet: none of the chosen parts has a file")
	}
	branch := s.Branch
	if branch == "" {
		branch = "main"
	}
	_, _, remote, err := api.Head(ctx, repo, branch)
	if err != nil {
		return Result{}, err
	}
	write, remove := Changed(files, remote)
	message := CommitMessage(write, remove)
	commit, pushed, err := api.Push(ctx, repo, branch, write, remove, message)
	if err != nil {
		return Result{}, err
	}
	res := Result{Pushed: len(write), Removed: len(remove), When: time.Now(), Missing: missing}
	if pushed {
		res.Commit = commit
		res.URL = WebURL(repo, branch)
	}
	return res, nil
}

// Due says whether a scheduled push is due now: the interval has passed
// since the last push, or the last one failed.
func Due(configDir string, s Setup, now time.Time) bool {
	if !s.Enabled {
		return false
	}
	every, ok := IntervalNamed(s.Interval)
	if !ok {
		every = 4 * time.Hour
	}
	st := LoadState(configDir)
	if st.Error != "" {
		return true
	}
	if st.Last.IsZero() {
		return true
	}
	return now.Sub(st.Last) >= every
}

// NextPush is when the schedule next pushes, for Settings to say. The zero
// time when it is off.
func NextPush(configDir string, s Setup) time.Time {
	if !s.Enabled {
		return time.Time{}
	}
	every, ok := IntervalNamed(s.Interval)
	if !ok {
		every = 4 * time.Hour
	}
	st := LoadState(configDir)
	base := st.Last
	if base.IsZero() {
		return time.Now()
	}
	return base.Add(every)
}

// NormaliseParts orders and de-duplicates the chosen parts, so a setup
// saved twice reads the same.
func NormaliseParts(keys []string) []string {
	seen := make(map[string]bool, len(keys))
	out := make([]string, 0, len(keys))
	for _, k := range keys {
		k = strings.TrimSpace(k)
		if k == "" || seen[k] {
			continue
		}
		if _, ok := PartNamed(k); !ok {
			continue
		}
		seen[k] = true
		out = append(out, k)
	}
	// The order Settings lists them in, whatever order they arrived.
	ordered := make([]string, 0, len(out))
	for _, p := range Parts {
		if seen[p.Key] {
			ordered = append(ordered, p.Key)
		}
	}
	return ordered
}

// TitleOf is a part's title for a summary line.
func TitleOf(key string) string {
	if p, ok := PartNamed(key); ok {
		return p.Title
	}
	return key
}

// TitlesOf joins several parts' titles for a summary line.
func TitlesOf(keys []string) string {
	titles := make([]string, 0, len(keys))
	for _, k := range keys {
		titles = append(titles, TitleOf(k))
	}
	return strings.Join(titles, ", ")
}
