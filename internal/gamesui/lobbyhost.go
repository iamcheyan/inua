package gamesui

import (
	"context"
	"errors"
	"strings"
	"time"

	"codeberg.org/puregotk/puregotk/v4/gtk"
	"github.com/makiuchi-d/gozxing"

	"github.com/lyricat/inua/internal/apps/store"
	"github.com/lyricat/inua/internal/apps/tailscale"
	"github.com/lyricat/inua/internal/games/lobbyservice"
	"github.com/lyricat/inua/internal/gtkx"
	"github.com/lyricat/inua/internal/i18n"
)

// The Game Lobby window's own lobby: inua-game-lobby run on this computer
// in a user service (lobbyservice), so its games go on when the window
// closes. A switch runs it or stops it, where it listens is this
// computer's network or its tailnet, and while it runs the window shows
// the address others open, with its QR code, and its tables. Starting and
// stopping run off the main thread; an error shows under the section.

type lobbyHost struct {
	room   *lobbyRoom
	on     *gtk.Switch
	where  [2]*gtk.ToggleButton // this network, Tailscale
	state  *gtk.Label
	shown  *gtk.Box // the address and QR code, while it runs
	link   *gtk.Label
	note   *gtk.Label
	err    *gtk.Label
	qr     *gozxing.BitMatrix
	canvas *canvas

	cfg   lobbyservice.Config
	local string // the address the window connects to while it runs; "" when it does not
	// busy is set while a start or a stop runs: the controls wait.
	busy bool
	// setting is set while the controls are set from here, not by a click.
	setting bool

	onSwitch func(gtk.Switch, bool) bool
	onWhere  func(gtk.ToggleButton)
	onCopy   func(gtk.Button)
}

// lobbyStartTimeout bounds a start: the AI, the network may be slow.
const lobbyStartTimeout = 30 * time.Second

const hostQR = 116

// hostSection builds the section at the window's top and reads how the
// service stands.
func (p *lobbyRoom) hostSection(f *frame) {
	h := &lobbyHost{room: p}
	p.host = h
	var prefs lobbyPrefs
	store.Load("game-lobby", &prefs)
	h.cfg = prefs.Host

	sec := gtk.NewBox(gtk.OrientationVerticalValue, 10)
	sec.AddCssClass("lobby-host")
	head := gtk.NewBox(gtk.OrientationHorizontalValue, 14)
	text := gtk.NewBox(gtk.OrientationVerticalValue, 2)
	text.SetHexpand(true)
	text.SetValign(gtk.AlignCenterValue)
	title := gtk.NewLabel(i18n.T("Run a lobby on this computer"))
	title.AddCssClass("fortune-option")
	title.SetXalign(0)
	gtkx.Append(text, &title.Widget)
	sub := gtk.NewLabel(i18n.T("Its games go on when this window closes, and the AI may play in them."))
	sub.AddCssClass("fortune-city-sub")
	sub.SetXalign(0)
	sub.SetWrap(true)
	gtkx.Append(text, &sub.Widget)
	gtkx.Append(head, &text.Widget)

	where := gtk.NewBox(gtk.OrientationHorizontalValue, 0)
	where.AddCssClass("segmented")
	where.SetValign(gtk.AlignCenterValue)
	h.onWhere = func(b gtk.ToggleButton) {
		if !h.setting && b.GetActive() {
			h.setWhere(lobbyservice.Where(b.GetName()))
		}
	}
	tailnet := i18n.T("no address: is Tailscale up?")
	if ip, err := tailscale.LocalIP(); err == nil {
		tailnet = ip
	}
	for i, w := range []struct {
		where       lobbyservice.Where
		name, about string
	}{
		{lobbyservice.Network, i18n.T("This network"), i18n.T("Every address of this computer: anyone on its networks can open the lobby")},
		{lobbyservice.Tailscale, i18n.T("Tailscale"), i18n.T("Tailscale") + " · " + tailnet + ": " + i18n.T("only the devices on the tailnet can open the lobby")},
	} {
		b := gtk.NewToggleButtonWithLabel(w.name)
		b.SetName(string(w.where))
		b.SetTooltipText(w.about)
		if i > 0 {
			b.SetGroup(h.where[0])
		}
		b.ConnectToggled(&h.onWhere)
		h.where[i] = b
		gtkx.Append(where, &b.Widget)
	}
	h.setting = true
	h.where[0].SetActive(h.cfg.Where != lobbyservice.Tailscale)
	h.where[1].SetActive(h.cfg.Where == lobbyservice.Tailscale)
	h.setting = false
	gtkx.Append(head, &where.Widget)

	h.state = gtk.NewLabel("")
	h.state.AddCssClass("lobby-host-state")
	h.state.SetValign(gtk.AlignCenterValue)
	gtkx.Append(head, &h.state.Widget)

	h.on = gtk.NewSwitch()
	h.on.SetValign(gtk.AlignCenterValue)
	h.on.SetTooltipText(i18n.T("Run the lobby, or stop it and the games at it"))
	h.onSwitch = func(_ gtk.Switch, on bool) bool {
		if !h.setting {
			h.turn(on)
		}
		return false
	}
	h.on.ConnectStateSet(&h.onSwitch)
	gtkx.Append(head, &h.on.Widget)
	gtkx.Append(sec, &head.Widget)

	// While it runs: the address others open, and its QR code.
	h.shown = gtk.NewBox(gtk.OrientationHorizontalValue, 16)
	h.shown.AddCssClass("lobby-host-link")
	h.shown.SetVisible(false)
	h.canvas = newCanvas(hostQR, hostQR, func(pn pen) { drawQR(pn, h.qr, hostQR) })
	h.canvas.area.SetSizeRequest(hostQR, hostQR)
	h.canvas.area.SetFocusable(false)
	h.canvas.area.SetValign(gtk.AlignStartValue)
	h.canvas.area.SetHexpand(false)
	h.canvas.area.AddCssClass("game-qr")
	gtkx.Append(h.shown, &h.canvas.area.Widget)
	col := gtk.NewBox(gtk.OrientationVerticalValue, 6)
	col.SetValign(gtk.AlignCenterValue)
	col.SetHexpand(true)
	k := gtk.NewLabel(i18n.T("OTHERS OPEN"))
	k.AddCssClass("kicker")
	k.SetXalign(0)
	gtkx.Append(col, &k.Widget)
	h.link = gtk.NewLabel("")
	h.link.AddCssClass("lobby-host-addr")
	h.link.SetXalign(0)
	h.link.SetSelectable(true)
	h.link.SetWrap(true)
	h.link.SetWrapMode(2) // PANGO_WRAP_WORD_CHAR
	gtkx.Append(col, &h.link.Widget)
	h.note = gtk.NewLabel("")
	h.note.AddCssClass("fortune-city-sub")
	h.note.SetXalign(0)
	h.note.SetWrap(true)
	gtkx.Append(col, &h.note.Widget)
	h.onCopy = func(gtk.Button) {
		clip := h.link.GetClipboard()
		clip.SetText(h.link.GetText())
		clip.Unref()
	}
	cp := button(i18n.T("Copy"), &h.onCopy)
	cp.AddCssClass("small")
	cp.SetHalign(gtk.AlignStartValue)
	gtkx.Append(col, &cp.Widget)
	gtkx.Append(h.shown, &col.Widget)
	gtkx.Append(sec, &h.shown.Widget)

	h.err = gtk.NewLabel("")
	h.err.AddCssClass("lobby-host-error")
	h.err.SetXalign(0)
	h.err.SetWrap(true)
	h.err.SetSelectable(true)
	h.err.SetVisible(false)
	gtkx.Append(sec, &h.err.Widget)
	gtkx.Append(&f.body, &sec.Widget)

	h.show(lobbyservice.Stopped)
	h.refresh()
}

// refresh reads how the service stands, and connects to its lobby while
// it runs.
func (h *lobbyHost) refresh() {
	go func() {
		ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()
		st := lobbyservice.Status(ctx)
		gtkx.Post(func() {
			if h.busy {
				return
			}
			h.show(st)
			switch st {
			case lobbyservice.Running:
				h.connect()
			case lobbyservice.Stopped:
				h.disconnect() // stopped elsewhere
			case lobbyservice.Failed:
				h.fail(errors.New(i18n.Tf("The lobby stopped with an error and is started again: %s says why.", lobbyservice.LogHint)))
			}
		})
	}()
}

// turn runs the lobby, or stops it.
func (h *lobbyHost) turn(on bool) {
	cfg := h.cfg
	h.save()
	h.busy = true
	h.fail(nil)
	if on {
		h.show(lobbyservice.Starting)
	} else {
		h.disconnect()
	}
	go func() {
		ctx, cancel := context.WithTimeout(context.Background(), lobbyStartTimeout)
		defer cancel()
		var err error
		if on {
			err = lobbyservice.Start(ctx, cfg)
		} else {
			lobbyservice.Stop(ctx)
		}
		st := lobbyservice.Status(ctx)
		gtkx.Post(func() {
			h.busy = false
			h.fail(err)
			if err != nil && st == lobbyservice.Starting {
				st = lobbyservice.Failed
			}
			h.show(st)
			if st == lobbyservice.Running && err == nil {
				h.connect()
			}
		})
	}()
}

// setWhere keeps where the lobby listens, and runs it there when it runs.
func (h *lobbyHost) setWhere(w lobbyservice.Where) {
	if h.cfg.Where == w || h.cfg.Where == "" && w == lobbyservice.Network {
		h.cfg.Where = w
		return
	}
	h.cfg.Where = w
	h.save()
	if h.on.GetActive() && !h.busy {
		h.disconnect()
		h.turn(true)
	}
}

// save keeps where the lobby listens.
func (h *lobbyHost) save() {
	var prefs lobbyPrefs
	store.Load("game-lobby", &prefs)
	if prefs.Host != h.cfg {
		prefs.Host = h.cfg
		store.Save("game-lobby", prefs)
	}
}

// show sets the controls for the service's state.
func (h *lobbyHost) show(st lobbyservice.State) {
	h.setting = true
	h.on.SetActive(st != lobbyservice.Stopped)
	h.on.SetState(st != lobbyservice.Stopped)
	h.setting = false
	h.on.SetSensitive(!h.busy)
	for _, b := range h.where {
		b.SetSensitive(!h.busy)
	}
	h.state.SetText(map[lobbyservice.State]string{
		lobbyservice.Stopped: i18n.T("off"), lobbyservice.Starting: i18n.T("starting…"),
		lobbyservice.Running: i18n.T("listening"), lobbyservice.Failed: i18n.T("failed"),
	}[st])
	for _, c := range []string{"on", "warn"} {
		h.state.RemoveCssClass(c)
	}
	switch st {
	case lobbyservice.Running:
		h.state.AddCssClass("on")
	case lobbyservice.Failed:
		h.state.AddCssClass("warn")
	}
	if st != lobbyservice.Running {
		h.shown.SetVisible(false)
	}
}

// fail shows why the lobby did not start, in the user's words; nil hides
// it.
func (h *lobbyHost) fail(err error) {
	switch {
	case errors.Is(err, tailscale.ErrNoAddress):
		err = errors.New(i18n.T("This computer has no Tailscale address: is Tailscale up? (tailscale up)"))
	case errors.Is(err, context.DeadlineExceeded):
		err = errors.New(i18n.Tf("The lobby did not start in time: %s says why.", lobbyservice.LogHint))
	}
	h.err.SetVisible(err != nil)
	if err != nil {
		h.err.SetText(err.Error())
	}
}

// connect shows where others open the lobby, and has the window watch
// its tables.
func (h *lobbyHost) connect() {
	local, err := h.cfg.Local()
	if err != nil {
		h.fail(err)
		return
	}
	public, err := h.cfg.Public()
	switch {
	case errors.Is(err, lobbyservice.ErrNoNetwork):
		h.link.SetText("http://" + local)
		h.note.SetText(i18n.T("This computer is on no network a browser could reach it from."))
	case err != nil:
		h.fail(err)
		return
	case h.cfg.Where == lobbyservice.Tailscale:
		h.link.SetText(public)
		h.note.SetText(i18n.T("Open it on a device on the tailnet."))
	default:
		h.link.SetText(public)
		h.note.SetText(i18n.T("Open it in a browser on this network."))
	}
	h.qr = qrOf(h.link.GetText())
	h.canvas.redraw()
	h.shown.SetVisible(true)
	h.local = local
	r := h.room
	if strings.TrimSpace(r.addr.GetText()) != local {
		r.addr.SetText(local)
		r.reset()
	}
}

// disconnect stops showing the lobby that runs here: the window goes
// back to the lobby it was given before.
func (h *lobbyHost) disconnect() {
	h.shown.SetVisible(false)
	if h.local == "" {
		return
	}
	r := h.room
	was := h.local
	h.local = ""
	if strings.TrimSpace(r.addr.GetText()) == was {
		var prefs lobbyPrefs
		store.Load("game-lobby", &prefs)
		r.addr.SetText(prefs.Address)
		r.reset()
	}
}
