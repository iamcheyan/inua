package fortunenet

import (
	"testing"

	"github.com/lyricat/inua/internal/games"
)

// lobbyUntil reads lobby messages until one satisfies ok.
func (b *browser) lobbyUntil(ok func(lobbyMsg) bool) lobbyMsg {
	b.t.Helper()
	for {
		var m lobbyMsg
		b.expect("lobby", &m)
		if ok(m) {
			return m
		}
	}
}

// With no one at the host's screen, the first visitor sets the game up
// and starts it; the second may not.
func TestVisitorLead(t *testing.T) {
	x := newTestHost(t, nil, 1)
	ann, _ := x.join(t, "Ann", "")
	m := ann.lobbyUntil(func(m lobbyMsg) bool { return m.Lead })
	if len(m.Cities) != len(games.FortuneCities) || m.MaxRivals != 3 || m.Setup.Rivals != 1 {
		t.Fatalf("Ann's lobby %+v", m)
	}
	bob, _ := x.join(t, "Bob", "")
	bob.lobbyUntil(func(m lobbyMsg) bool { return !m.Lead && m.LeadName == "Ann" })

	// Bob may not; Ann may, within what the game offers.
	bob.send(inMsg{T: "setup", Setup: Setup{City: 1, Rounds: 90, Cash: 3000, Dice: 1, Rivals: 2}})
	ann.send(inMsg{T: "setup", Setup: Setup{City: 0, Rounds: 45, Cash: 3000, Dice: 1, Rivals: 2}})
	ann.send(inMsg{T: "setup", Setup: Setup{City: 2, Rounds: 90, Cash: 3000, Dice: 1, Rivals: 3}}) // five players
	ann.send(inMsg{T: "setup", Setup: Setup{City: 2, Rounds: 90, Cash: 3000, Dice: 1, BuildOnBuy: true, Rivals: 2}})
	ann.lobbyUntil(func(m lobbyMsg) bool { return m.Setup.City == 2 })
	x.do(func() {
		s := x.Settings
		if s.City != 2 || s.Rounds != 90 || s.Cash != 3000 || s.Dice != 1 || !s.BuildOnBuy || s.Rivals != 2 || len(s.RivalNames) != 2 {
			t.Errorf("settings %+v", s)
		}
		if x.Room() != 0 {
			t.Errorf("room %d", x.Room())
		}
	})

	bob.send(inMsg{T: "start"})
	ann.send(inMsg{T: "start"})
	var st stateMsg
	ann.expect("state", &st)
	if !st.Lead {
		t.Error("Ann does not lead the game")
	}
	x.do(func() {
		g := x.Game
		if g == nil || len(g.Players) != 4 || g.City != 2 || g.Rounds != 90 || !g.OneDie {
			t.Fatalf("game %+v", g)
		}
		if st := x.Status(); st.State != "playing" || st.Lead != "Ann" || len(st.Seats) != 4 {
			t.Errorf("status %+v", st)
		}
	})
}

// With someone at the host's screen, no visitor leads.
func TestHostLeads(t *testing.T) {
	x := newTestHost(t, []string{"Host"}, 1)
	ann, _ := x.join(t, "Ann", "")
	m := ann.lobbyUntil(func(m lobbyMsg) bool { return len(m.Seats) == 2 })
	if m.Lead || !m.HostLeads || m.Cities != nil {
		t.Errorf("lobby %+v", m)
	}
	ann.send(inMsg{T: "start"})
	ann.send(inMsg{T: "setup", Setup: Setup{City: 1, Rounds: 30, Cash: 1000, Dice: 2}})
	x.join(t, "Bob", "")
	x.do(func() {
		if x.Game != nil || x.Settings.City != 0 {
			t.Errorf("a visitor set up the host's game")
		}
	})
}
