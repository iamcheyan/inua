package clipboard

import (
	"bytes"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"testing"
)

func TestTextCapturePreservesPayloadAndDeduplicates(t *testing.T) {
	t.Setenv("CLIPBOARD_STATE", "data")
	path := filepath.Join(t.TempDir(), "clipboard-history.json")
	text := " 中文\n$(never execute) `nor this` 100%\n"
	for range 2 {
		if err := Capture(path, strings.NewReader(text)); err != nil {
			t.Fatal(err)
		}
	}
	entries, err := Read(path)
	if err != nil || len(entries) != 1 || entries[0].Text != text {
		t.Fatalf("capture did not preserve and deduplicate text: %v", err)
	}
	info, err := os.Stat(path)
	if err != nil || info.Mode().Perm() != 0600 {
		t.Fatal("history must be private")
	}
}
func TestSensitiveClipboardIsNotStored(t *testing.T) {
	path := filepath.Join(t.TempDir(), "history.json")
	for _, state := range []string{"sensitive", "nil", "clear"} {
		t.Setenv("CLIPBOARD_STATE", state)
		if err := Capture(path, strings.NewReader("do not store")); err != nil {
			t.Fatal(err)
		}
	}
	if _, err := os.Stat(path); !os.IsNotExist(err) {
		t.Fatal("sensitive selection created history")
	}
}
func TestImageCapture(t *testing.T) {
	t.Setenv("CLIPBOARD_STATE", "data")
	path := filepath.Join(t.TempDir(), "history.json")
	data := []byte("\x89PNG\r\n\x1a\nimage payload")
	if err := Capture(path, bytes.NewReader(data)); err != nil {
		t.Fatal(err)
	}
	entries, err := Read(path)
	if err != nil || len(entries) != 1 || entries[0].MIME != "image/png" {
		t.Fatal("image was not classified correctly", err)
	}
	got, err := os.ReadFile(entries[0].Path)
	if err != nil || !bytes.Equal(got, data) {
		t.Fatal("image bytes changed", err)
	}
}
func TestConcurrentUpdatesAndDeleteByIdentity(t *testing.T) {
	path := filepath.Join(t.TempDir(), "history.json")
	var wg sync.WaitGroup
	for i := range 30 {
		wg.Add(1)
		go func() {
			defer wg.Done()
			if err := Add(path, Entry{Type: "text", Text: fmt.Sprint(i)}); err != nil {
				t.Error(err)
			}
		}()
	}
	wg.Wait()
	entries, err := Read(path)
	if err != nil || len(entries) != 30 {
		t.Fatal("concurrent writers lost history", err)
	}
	selected := entries[10]
	if err := Add(path, Entry{Type: "text", Text: "new selection"}); err != nil {
		t.Fatal(err)
	}
	if err := Delete(path, selected); err != nil {
		t.Fatal(err)
	}
	entries, err = Read(path)
	if err != nil || len(entries) != 30 {
		t.Fatal("delete removed incorrect number of items", err)
	}
	for _, e := range entries {
		if same(e, selected) {
			t.Fatal("stale selection was not deleted")
		}
	}
}
func TestReuseAnchorHistory(t *testing.T) {
	root := t.TempDir()
	t.Setenv("XDG_STATE_HOME", root)
	path := filepath.Join(root, "labwc", "clipboard-history.json")
	if err := Add(path, Entry{Type: "text", Text: "existing"}); err != nil {
		t.Fatal(err)
	}
	if got := HistoryPath(); got != path {
		t.Fatal("did not reuse existing Anchor Shell history")
	}
}
