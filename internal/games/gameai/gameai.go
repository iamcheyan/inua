// Package gameai is the user's AI as the games' hosts have it, without
// GTK: inua-assistant --answer started (internal/assistant/answer), the
// AI players' names, and, for a host no one sits at (a game the lobby
// hosts, a desktop's game a visitor sets up), an assistant kept running
// and started again when it ends. The players themselves are played by
// fortuneai and checkersai, which fall back to the computer when the AI
// does not answer.
package gameai

import (
	"context"
	"errors"
	"sync"
	"time"

	"github.com/lyricat/inua/internal/assistant/answer"
	"github.com/lyricat/inua/internal/i18n"
)

// AI is the user's AI as a host offers it to the one who sets a game up:
// Choose asks a profile ("" the default) to pick one of options; Profiles
// are the profiles it may ask, the default first, none while it cannot
// answer.
type AI interface {
	Choose(ctx context.Context, profile, instructions, state string, options []string) (int, error)
	Profiles() []string
}

// Start starts inua-assistant --answer; the error is why the AI cannot
// play, for the user.
func Start(ctx context.Context) (*answer.Client, error) {
	prog, err := answer.Program()
	if err != nil {
		return nil, errors.New(i18n.T("inua-assistant is not installed"))
	}
	c, err := answer.Start(ctx, prog, "--answer")
	return c, Err(err)
}

// Err says an error of the AI's in the user's words.
func Err(err error) error {
	if errors.Is(err, context.DeadlineExceeded) {
		return errors.New(i18n.T("the AI did not answer in time"))
	}
	return err
}

// Names names n AI players asking the default profile: "AI", or "AI 1" …
func Names(n int) []string {
	if n == 1 {
		return []string{i18n.T("AI")}
	}
	var names []string
	for k := range n {
		names = append(names, i18n.Tf("AI %d", k+1))
	}
	return names
}

// Of is a started inua-assistant --answer as an AI.
func Of(c *answer.Client) AI { return client{c} }

type client struct{ *answer.Client }

func (c client) Profiles() []string { return names(c.Client.Profiles) }

func names(ps []answer.Profile) []string {
	var out []string
	for _, p := range ps {
		out = append(out, p.Name)
	}
	return out
}

// Chooser is a started assistant: what it is asked with, and its end.
type Chooser interface {
	Choose(ctx context.Context, profile, instructions, state string, options []string) (int, error)
	Close()
}

// Launch starts inua-assistant --answer for an Assistant.
func Launch(ctx context.Context) (Chooser, []string, error) {
	c, err := Start(ctx)
	if err != nil {
		return nil, nil, err
	}
	return c, names(c.Profiles), nil
}

// Retry is how long an Assistant waits after a start before it starts
// again: when the start failed, or the program ended.
var Retry = time.Minute

// Assistant is the user's AI for a host that runs on its own (the
// lobby): started at once in the background, offered while it answers,
// and started again, at most once a Retry, when it could not start or
// has ended. A question to it meanwhile fails, and the game's driver has
// the computer play that turn.
type Assistant struct {
	launch func(context.Context) (Chooser, []string, error)

	mu       sync.Mutex
	c        Chooser
	profiles []string
	starting bool
	closed   bool
	tried    time.Time
	err      error
}

// NewAssistant starts an assistant with launch (Launch).
func NewAssistant(launch func(context.Context) (Chooser, []string, error)) *Assistant {
	a := &Assistant{launch: launch}
	a.mu.Lock()
	a.startLocked()
	a.mu.Unlock()
	return a
}

// startLocked starts the program in the background, unless it runs, is
// starting, or was tried less than a Retry ago. Called with mu held.
func (a *Assistant) startLocked() {
	if a.c != nil || a.starting || a.closed || !a.tried.IsZero() && time.Since(a.tried) < Retry {
		return
	}
	a.starting, a.tried = true, time.Now()
	go func() {
		ctx, cancel := context.WithTimeout(context.Background(), time.Minute)
		defer cancel()
		c, profiles, err := a.launch(ctx)
		if err == nil && len(profiles) == 0 {
			c.Close()
			c, err = nil, errors.New(i18n.T("no profile of Settings → AI makes decisions"))
		}
		a.mu.Lock()
		defer a.mu.Unlock()
		a.starting = false
		if a.closed {
			if c != nil {
				c.Close()
			}
			return
		}
		a.c, a.profiles, a.err = c, profiles, err
	}()
}

// Profiles are the profiles the AI may ask, the default first; none while
// it is starting or cannot start, when it tries again (after a Retry).
func (a *Assistant) Profiles() []string {
	a.mu.Lock()
	defer a.mu.Unlock()
	if a.c == nil {
		a.startLocked()
		return nil
	}
	return a.profiles
}

// Err is why the AI could not start, nil while it runs or starts.
func (a *Assistant) Err() error {
	a.mu.Lock()
	defer a.mu.Unlock()
	return a.err
}

// Choose asks profile ("" the default) to pick one of options. A program
// that has ended is started again for the next question.
func (a *Assistant) Choose(ctx context.Context, profile, instructions, state string, options []string) (int, error) {
	a.mu.Lock()
	c := a.c
	if c == nil {
		a.startLocked()
	}
	a.mu.Unlock()
	if c == nil {
		return -1, errors.New(i18n.T("the AI is not running"))
	}
	i, err := c.Choose(ctx, profile, instructions, state, options)
	if errors.Is(err, answer.ErrClosed) {
		a.mu.Lock()
		if a.c == c {
			a.c, a.profiles = nil, nil
			a.startLocked()
		}
		a.mu.Unlock()
	}
	return i, Err(err)
}

// Close ends the program.
func (a *Assistant) Close() {
	a.mu.Lock()
	defer a.mu.Unlock()
	a.closed = true
	if a.c != nil {
		a.c.Close()
		a.c, a.profiles = nil, nil
	}
}
