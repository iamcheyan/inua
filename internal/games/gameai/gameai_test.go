package gameai

import (
	"context"
	"errors"
	"slices"
	"sync"
	"testing"
	"time"

	"github.com/lyricat/inua/internal/assistant/answer"
)

// fakeChooser is a started assistant: it picks option pick, or has ended.
type fakeChooser struct {
	mu     sync.Mutex
	ended  bool
	closed bool
}

func (c *fakeChooser) Choose(context.Context, string, string, string, []string) (int, error) {
	c.mu.Lock()
	defer c.mu.Unlock()
	if c.ended {
		return -1, answer.ErrClosed
	}
	return 1, nil
}

func (c *fakeChooser) Close() {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.closed = true
}

// launcher starts fake assistants, failing while fail is set.
type launcher struct {
	mu      sync.Mutex
	fail    bool
	started []*fakeChooser
}

func (l *launcher) launch(context.Context) (Chooser, []string, error) {
	l.mu.Lock()
	defer l.mu.Unlock()
	if l.fail {
		return nil, nil, errors.New("inua-assistant is not installed")
	}
	c := &fakeChooser{}
	l.started = append(l.started, c)
	return c, []string{"quick", "deep"}, nil
}

func (l *launcher) count() int {
	l.mu.Lock()
	defer l.mu.Unlock()
	return len(l.started)
}

func waitFor(t *testing.T, what string, ok func() bool) {
	t.Helper()
	for range 500 {
		if ok() {
			return
		}
		time.Sleep(5 * time.Millisecond)
	}
	t.Fatalf("never %s", what)
}

// An assistant starts at once and is offered once it answers; one that
// has ended is started again for the next question.
func TestAssistant(t *testing.T) {
	old := Retry
	Retry = 50 * time.Millisecond
	t.Cleanup(func() { Retry = old })
	l := &launcher{}
	a := NewAssistant(l.launch)
	waitFor(t, "ready", func() bool { return len(a.Profiles()) == 2 })
	if i, err := a.Choose(context.Background(), "", "pick", "", []string{"a", "b"}); i != 1 || err != nil {
		t.Fatalf("Choose = %d, %v", i, err)
	}

	l.mu.Lock()
	l.started[0].ended = true
	l.mu.Unlock()
	if _, err := a.Choose(context.Background(), "", "pick", "", []string{"a", "b"}); !errors.Is(err, answer.ErrClosed) {
		t.Fatalf("Choose of an ended assistant: %v", err)
	}
	if a.Profiles() != nil && l.count() == 1 {
		t.Error("an ended assistant still offered")
	}
	time.Sleep(Retry)
	waitFor(t, "started again", func() bool { return len(a.Profiles()) == 2 && l.count() == 2 })
	if i, err := a.Choose(context.Background(), "", "pick", "", []string{"a", "b"}); i != 1 || err != nil {
		t.Fatalf("Choose after the start again = %d, %v", i, err)
	}

	a.Close()
	if !l.started[1].closed || a.Profiles() != nil {
		t.Error("Close left the assistant running")
	}
	if _, err := a.Choose(context.Background(), "", "pick", "", []string{"a", "b"}); err == nil {
		t.Error("a closed assistant answered")
	}
	time.Sleep(2 * Retry)
	if l.count() != 2 {
		t.Error("a closed assistant started again")
	}
}

// An assistant that cannot start is not offered, says why, and tries
// again after Retry, not at every question.
func TestAssistantFails(t *testing.T) {
	old := Retry
	Retry = 100 * time.Millisecond
	t.Cleanup(func() { Retry = old })
	l := &launcher{fail: true}
	a := NewAssistant(l.launch)
	waitFor(t, "the failure", func() bool { return a.Err() != nil })
	for range 5 {
		if a.Profiles() != nil {
			t.Fatal("offered while it cannot start")
		}
		if _, err := a.Choose(context.Background(), "", "", "", []string{"a"}); err == nil {
			t.Fatal("answered while it cannot start")
		}
	}
	if l.count() != 0 {
		t.Fatal("started")
	}
	l.mu.Lock()
	l.fail = false
	l.mu.Unlock()
	time.Sleep(Retry)
	waitFor(t, "started after the retry", func() bool { return len(a.Profiles()) == 2 })
	if a.Err() != nil {
		t.Errorf("Err = %v once running", a.Err())
	}
}

// AI players asking the default profile are named as on the desktop.
func TestNames(t *testing.T) {
	if got := Names(1); !slices.Equal(got, []string{"AI"}) {
		t.Errorf("Names(1) = %q", got)
	}
	if got := Names(3); !slices.Equal(got, []string{"AI 1", "AI 2", "AI 3"}) {
		t.Errorf("Names(3) = %q", got)
	}
}
