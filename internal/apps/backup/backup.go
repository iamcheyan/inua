// Package backup keeps a copy of the settings worth carrying to another
// computer in a GitHub repository, written on a schedule.
//
// What goes there is a file per part: the shell's settings, its themes and
// icons, the Hyprland settings inua writes, the shortcuts, the light apps'
// own state and, if asked, the assistant's profiles (never their keys,
// which stay in the Secret Service). The parts are chosen in Settings and
// collected as files, so what is pushed is readable: a repository of a
// person's own desktop, not a sealed blob.
//
// The push is one commit per change. The remote file is read first, and a
// file that has not changed here since the last push is left alone, so a
// computer that keeps its settings still says nothing. Where both sides
// changed, this computer's copy wins and the other is kept in the commit
// message, which is what makes a wrong direction recoverable.
package backup

import (
	"cmp"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"slices"
	"strings"
)

// Part is one piece of the setup that can be carried: a name for the
// switch, and what it is.
type Part struct {
	Key   string
	Title string
	// Paths are absolute or, when Relative, under the configuration
	// directory; a directory is taken whole.
	Paths    []string
	Relative bool
	// Skip are file names left out of a directory: caches, locks, and
	// anything holding a secret.
	Skip []string
	// Default is whether a setup made before the part existed carries it.
	Default bool
}

// Parts, in the order Settings lists them.
var Parts = []Part{
	{
		Key: "settings", Title: "The shell's settings",
		Paths: []string{"inua/config.toml"}, Relative: true, Default: true,
	},
	{
		Key: "style", Title: "Style, themes and icons",
		Paths: []string{"inua/style.css", "inua/themes", "inua/icons"}, Relative: true, Default: true,
	},
	{
		Key: "hyprland", Title: "Hyprland settings",
		Paths: []string{"hypr/inua.conf", "hypr/inua.lua"}, Relative: true, Default: true,
	},
	{
		Key: "apps", Title: "The light apps' state",
		Paths: []string{"inua/apps"}, Relative: true, Default: true,
	},
	{
		Key: "assistant", Title: "The assistant's profiles",
		Paths: []string{"inua/assistant"}, Relative: true, Default: false,
		// Settings' own file holds the profiles; the folder is where a
		// conversation's history is kept, which is not carried.
		Skip: []string{"history", "sessions"},
	},
}

// PartNamed finds a part by its key.
func PartNamed(key string) (Part, bool) {
	for _, p := range Parts {
		if p.Key == key {
			return p, true
		}
	}
	return Part{}, false
}

// DefaultParts are the keys a new setup starts with.
func DefaultParts() []string {
	var keys []string
	for _, p := range Parts {
		if p.Default {
			keys = append(keys, p.Key)
		}
	}
	return keys
}

// File is one file of a part, at the path it takes in the repository.
type File struct {
	Path string // slash-separated, under the repository's root
	Data []byte
	// Sum is the file's name in a repository (BlobSum), which is what a
	// remote tree reports, so the two can be compared.
	Sum string
}

// Collect reads the chosen parts under configDir. A part whose files are
// all missing is left out rather than failing: a new computer has none of
// them yet. The error is for a read that failed for another reason.
func Collect(configDir string, keys []string) ([]File, []string, error) {
	var files []File
	var missing []string
	for _, key := range keys {
		part, ok := PartNamed(key)
		if !ok {
			return nil, nil, fmt.Errorf("unknown part %q", key)
		}
		got, none, err := collectPart(configDir, part)
		if err != nil {
			return nil, nil, err
		}
		if none {
			missing = append(missing, part.Title)
			continue
		}
		files = append(files, got...)
	}
	slices.SortFunc(files, func(a, b File) int { return cmp.Compare(a.Path, b.Path) })
	return files, missing, nil
}

// collectPart reads one part; none when it has no file at all.
func collectPart(configDir string, part Part) (files []File, none bool, err error) {
	none = true
	for _, rel := range part.Paths {
		full := rel
		if part.Relative {
			full = filepath.Join(configDir, rel)
		}
		info, err := os.Stat(full)
		if errors.Is(err, os.ErrNotExist) {
			continue
		}
		if err != nil {
			return nil, false, err
		}
		none = false
		if !info.IsDir() {
			data, err := os.ReadFile(full)
			if err != nil {
				return nil, false, err
			}
			files = append(files, File{Path: filepath.ToSlash(rel), Data: data, Sum: BlobSum(data)})
			continue
		}
		walked, err := collectDir(full, filepath.ToSlash(rel), part.Skip)
		if err != nil {
			return nil, false, err
		}
		files = append(files, walked...)
	}
	return files, none, nil
}

// collectDir reads every file of a directory that is not skipped.
func collectDir(dir, prefix string, skip []string) ([]File, error) {
	var files []File
	err := filepath.WalkDir(dir, func(path string, d os.DirEntry, err error) error {
		if err != nil {
			return err
		}
		if d.IsDir() {
			if slices.Contains(skip, d.Name()) {
				return filepath.SkipDir
			}
			return nil
		}
		if slices.Contains(skip, d.Name()) {
			return nil
		}
		rel, err := filepath.Rel(dir, path)
		if err != nil {
			return err
		}
		data, err := os.ReadFile(path)
		if err != nil {
			return err
		}
		files = append(files, File{
			Path: prefix + "/" + filepath.ToSlash(rel),
			Data: data,
			Sum:  BlobSum(data),
		})
		return nil
	})
	return files, err
}

// Root is the folder inside the repository the files are written under, so
// a repository may hold other things too.
const Root = "inua"

// RepoPath is where a collected file goes in the repository.
func RepoPath(f File) string { return Root + "/" + f.Path }

// Changed compares what is here with what the repository holds, by path and
// hash. It returns the files to write and the paths to delete, both sorted.
func Changed(local []File, remote map[string]string) (write []File, remove []string) {
	here := make(map[string]string, len(local))
	for _, f := range local {
		here[RepoPath(f)] = f.Sum
		if remote[RepoPath(f)] != f.Sum {
			write = append(write, f)
		}
	}
	for path := range remote {
		if !strings.HasPrefix(path, Root+"/") {
			continue // not ours to remove
		}
		if _, ok := here[path]; !ok {
			remove = append(remove, path)
		}
	}
	slices.SortFunc(write, func(a, b File) int { return cmp.Compare(a.Path, b.Path) })
	slices.Sort(remove)
	return write, remove
}

// CommitMessage says what a push did, in the words git history is read
// with, and names the files it touched.
func CommitMessage(write []File, remove []string) string {
	var b strings.Builder
	switch {
	case len(write) == 0 && len(remove) == 0:
		return "inua: no change"
	case len(write) > 0 && len(remove) == 0:
		b.WriteString("inua: back up the settings\n")
	default:
		b.WriteString("inua: back up the settings, and drop what is gone\n")
	}
	for _, f := range write {
		fmt.Fprintf(&b, "\nA\t%s", RepoPath(f))
	}
	for _, p := range remove {
		fmt.Fprintf(&b, "\nD\t%s", p)
	}
	return b.String()
}
