// Package clipboard stores the text and image history used by the clipboard
// panel. It also reads Anchor Shell's existing JSON format without migration.
package clipboard

import (
	"crypto/sha256"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"
	"unicode/utf8"

	"golang.org/x/sys/unix"
)

const DefaultLimit = 300
var Limit = DefaultLimit
const MaxPayload = 32 << 20

type Entry struct {
	Type       string `json:"type"`
	Text       string `json:"text,omitempty"`
	MIME       string `json:"mime,omitempty"`
	Path       string `json:"path,omitempty"`
	CapturedAt string `json:"capturedAt,omitempty"`
}

// HistoryPath reuses an existing desktop history before creating Inua's own.
func HistoryPath() string {
	root := os.Getenv("XDG_STATE_HOME")
	if root == "" {
		home, _ := os.UserHomeDir()
		root = filepath.Join(home, ".local", "state")
	}
	for _, desktop := range []string{"inua", "labwc", "omarchy"} {
		p := filepath.Join(root, desktop, "clipboard-history.json")
		if _, err := os.Stat(p); err == nil {
			return p
		}
	}
	return filepath.Join(root, "inua", "clipboard-history.json")
}

func Read(path string) ([]Entry, error) {
	data, err := os.ReadFile(path)
	if os.IsNotExist(err) {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	var entries []Entry
	if err := json.Unmarshal(data, &entries); err != nil {
		return nil, err
	}
	return entries, nil
}

func same(a, b Entry) bool {
	return a.Type == b.Type && a.Text == b.Text && a.Path == b.Path && a.MIME == b.MIME
}

// Update serializes writers, including the Anchor Shell capture backend, and
// replaces the history atomically so readers never see a partial JSON file.
func Update(path string, change func([]Entry) []Entry) error {
	dir := filepath.Dir(path)
	if err := os.MkdirAll(dir, 0700); err != nil {
		return err
	}
	lock, err := os.OpenFile(path+".lock", os.O_CREATE|os.O_RDWR, 0600)
	if err != nil {
		return err
	}
	defer lock.Close()
	if err := unix.Flock(int(lock.Fd()), unix.LOCK_EX); err != nil {
		return err
	}
	defer unix.Flock(int(lock.Fd()), unix.LOCK_UN)
	entries, err := Read(path)
	if err != nil {
		return err
	}
	entries = change(entries)
	if len(entries) > Limit {
		entries = entries[:Limit]
	}
	data, err := json.MarshalIndent(entries, "", "  ")
	if err != nil {
		return err
	}
	f, err := os.CreateTemp(dir, ".clipboard-history-*")
	if err != nil {
		return err
	}
	defer os.Remove(f.Name())
	defer f.Close()
	if _, err = f.Write(append(data, '\n')); err != nil {
		return err
	}
	if err = f.Close(); err != nil {
		return err
	}
	return os.Rename(f.Name(), path)
}

func Add(path string, entry Entry) error {
	return Update(path, func(entries []Entry) []Entry {
		next := []Entry{entry}
		for _, old := range entries {
			if !same(old, entry) {
				next = append(next, old)
			}
		}
		return next
	})
}
func Delete(path string, entry Entry) error {
	return Update(path, func(entries []Entry) []Entry {
		next := make([]Entry, 0, len(entries))
		for _, old := range entries {
			if !same(old, entry) {
				next = append(next, old)
			}
		}
		return next
	})
}
func Clear(path string) error { return Update(path, func([]Entry) []Entry { return []Entry{} }) }

// Capture is called by wl-paste --watch. Sensitive and oversized selections
// are ignored. Clipboard bytes never pass through a shell or command argument.
func Capture(path string, r io.Reader) error {
	switch os.Getenv("CLIPBOARD_STATE") {
	case "sensitive", "nil", "clear":
		return nil
	}
	data, err := io.ReadAll(io.LimitReader(r, MaxPayload+1))
	if err != nil {
		return err
	}
	if len(data) == 0 || len(data) > MaxPayload {
		return nil
	}
	mime := http.DetectContentType(data)
	entry := Entry{Type: "text"}
	if strings.HasPrefix(mime, "image/") {
		dir := filepath.Join(filepath.Dir(path), "clipboard-images")
		if err := os.MkdirAll(dir, 0700); err != nil {
			return err
		}
		name := fmt.Sprintf("%x.%s", sha256.Sum256(data), strings.TrimPrefix(mime, "image/"))
		entry.CapturedAt = time.Now().Format("Monday 15:04")
		entry.Type, entry.MIME, entry.Path = "image", mime, filepath.Join(dir, name)
		if err := os.WriteFile(entry.Path, data, 0600); err != nil {
			return err
		}
	} else {
		if !utf8.Valid(data) || strings.ContainsRune(string(data), 0) {
			return nil
		}
		entry.Text = string(data)
	}
	return Add(path, entry)
}
