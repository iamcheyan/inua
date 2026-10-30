package fortunenet

import (
	"context"
	"errors"
	"slices"
	"sync"
	"testing"

	"github.com/lyricat/inua/internal/games"
)

// fakeAI is the user's AI as a host offers it: it picks the first option,
// or fails, and counts the questions.
type fakeAI struct {
	mu       sync.Mutex
	profiles []string
	fail     bool
	asked    int
	asking   []string // the profiles asked
}

func (a *fakeAI) Choose(_ context.Context, profile, _, _ string, _ []string) (int, error) {
	a.mu.Lock()
	defer a.mu.Unlock()
	a.asked++
	a.asking = append(a.asking, profile)
	if a.fail {
		return -1, errors.New("the model is away")
	}
	return 0, nil
}

func (a *fakeAI) Profiles() []string { return a.profiles }

func (a *fakeAI) count() int {
	a.mu.Lock()
	defer a.mu.Unlock()
	return a.asked
}

// newLeadHost is a host no one plays at, offering ai to the lead visitor.
func newLeadHost(t *testing.T, ai *fakeAI) *testHost {
	t.Helper()
	x := &testHost{}
	opt := Options{
		Settings: games.FortuneSettings{Rivals: 1, Rounds: 30, Cash: 1500},
		Run:      func(f func()) { x.mu.Lock(); defer x.mu.Unlock(); f() },
		Seed:     1,
	}
	if ai != nil {
		opt.LeadAI = ai
	}
	x.Host = NewHost(opt)
	if err := x.Serve("127.0.0.1:0"); err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { x.do(func() { x.Close() }) })
	return x
}

// With the host's AI offered, the lead visitor asks for AI players beside
// the computer's; the AI plays them, asking its default profile.
func TestLeadAI(t *testing.T) {
	ai := &fakeAI{profiles: []string{"quick", "deep"}}
	x := newLeadHost(t, ai)
	ann, _ := x.join(t, "Ann", "")
	m := ann.lobbyUntil(func(m lobbyMsg) bool { return m.Lead })
	if m.MaxAIs != 2 || m.Setup.AIs != 0 {
		t.Fatalf("Ann may have %d AI players (%d asked for), want 2", m.MaxAIs, m.Setup.AIs)
	}
	ann.send(inMsg{T: "setup", Setup: Setup{City: 0, Rounds: 30, Cash: 2000, Dice: 2, Rivals: 1, AIs: 3}}) // five players
	ann.send(inMsg{T: "setup", Setup: Setup{City: 0, Rounds: 30, Cash: 2000, Dice: 2, Rivals: 1, AIs: 2}})
	m = ann.lobbyUntil(func(m lobbyMsg) bool { return m.Setup.AIs == 2 })
	if m.AIs != 2 || m.MaxRivals != 1 || m.Room != 0 {
		t.Errorf("lobby %+v", m)
	}
	x.do(func() {
		if !slices.Equal(x.Settings.AIs, []string{"AI 1", "AI 2"}) {
			t.Errorf("AI players %q", x.Settings.AIs)
		}
		if st := x.Status(); len(st.Seats) != 4 || st.Seats[1].Kind != "ai" {
			t.Errorf("status %+v", st)
		}
	})
	ann.send(inMsg{T: "start"})
	ann.until(func(stateMsg) bool { return true })
	x.do(func() {
		if kinds := []SeatKind{x.Seats[1].Kind, x.Seats[2].Kind, x.Seats[3].Kind}; !slices.Equal(kinds, []SeatKind{AI, AI, Computer}) {
			t.Errorf("seats %v", kinds)
		}
		x.Game.SetAway(0, true) // the computer plays Ann's turns
		x.Flush()
	})
	x.eventually(t, "the AI to be asked", func() bool { return ai.count() > 0 })
	ai.mu.Lock()
	defer ai.mu.Unlock()
	for _, p := range ai.asking {
		if p != "" {
			t.Errorf("asked profile %q, not the default", p)
		}
	}
}

// When the AI does not answer, the computer plays the AI players' turns
// and the game goes on.
func TestLeadAIFails(t *testing.T) {
	ai := &fakeAI{profiles: []string{"quick"}, fail: true}
	x := newLeadHost(t, ai)
	ann, _ := x.join(t, "Ann", "")
	ann.lobbyUntil(func(m lobbyMsg) bool { return m.Lead && m.MaxAIs == 2 })
	ann.send(inMsg{T: "setup", Setup: Setup{City: 0, Rounds: 30, Cash: 2000, Dice: 2, Rivals: 0, AIs: 1}})
	ann.lobbyUntil(func(m lobbyMsg) bool { return m.Setup.AIs == 1 })
	ann.send(inMsg{T: "start"})
	ann.until(func(stateMsg) bool { return true })
	x.do(func() {
		if x.Game.Players[1].Name != "AI" || !x.Game.Players[1].AI {
			t.Errorf("player %+v", x.Game.Players[1])
		}
		x.Game.SetAway(0, true)
		x.Flush()
	})
	x.eventually(t, "the game to go on without the AI", func() bool {
		return x.Game.Round >= 5 && ai.count() >= 3
	})
}

// No AI is offered with none given, while it does not answer, or when
// someone plays at the host's screen; asking for AI players then changes
// nothing.
func TestLeadNoAI(t *testing.T) {
	for name, ai := range map[string]*fakeAI{"none": nil, "not answering": {}} {
		t.Run(name, func(t *testing.T) {
			x := newLeadHost(t, ai)
			ann, _ := x.join(t, "Ann", "")
			m := ann.lobbyUntil(func(m lobbyMsg) bool { return m.Lead })
			if m.MaxAIs != 0 {
				t.Errorf("Ann may have %d AI players", m.MaxAIs)
			}
			ann.send(inMsg{T: "setup", Setup: Setup{City: 1, Rounds: 30, Cash: 2000, Dice: 2, Rivals: 1, AIs: 1}})
			ann.lobbyUntil(func(m lobbyMsg) bool { return m.Setup.City == 1 })
			x.do(func() {
				if len(x.Settings.AIs) != 0 {
					t.Errorf("AI players %q", x.Settings.AIs)
				}
			})
		})
	}
	x := newTestHost(t, []string{"Host"}, 1)
	x.do(func() {
		x.SetAI(&fakeAI{profiles: []string{"quick"}})
		if x.MaxAIs() != 0 {
			t.Errorf("a visitor may have AI players in the host's game")
		}
	})
}

// The AI players are named as the desktop names them; the host's names
// for its profiles stay.
func TestAINames(t *testing.T) {
	for _, c := range []struct {
		had  []string
		n    int
		want []string
	}{
		{nil, 1, []string{"AI"}},
		{[]string{"AI"}, 2, []string{"AI 1", "AI 2"}},
		{[]string{"AI 1", "AI 2"}, 1, []string{"AI"}},
		{[]string{"quick"}, 3, []string{"quick", "AI 2", "AI 3"}},
		{[]string{"quick", "deep"}, 1, []string{"quick"}},
	} {
		if got := aiNames(c.had, c.n); !slices.Equal(got, c.want) {
			t.Errorf("aiNames(%q, %d) = %q, want %q", c.had, c.n, got, c.want)
		}
	}
}
