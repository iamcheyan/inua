package ui

import (
	"codeberg.org/puregotk/puregotk/v4/gdk"
	"codeberg.org/puregotk/puregotk/v4/glib"
	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/gtkx"
	"github.com/lyricat/inua/internal/i18n"
	"github.com/lyricat/inua/internal/layershell"
	"github.com/lyricat/inua/internal/shell"
	"github.com/lyricat/inua/internal/system"
)

// osdMS is how long the display stays up, and its fade.
const osdMS = 1200

// osd is the on-screen display: one card, an icon and a word, answering a
// change to the volume, the brightness, Wi-Fi or Bluetooth from whatever
// made it (the keys, the scroll on the status button, the control center).
type osd struct {
	win     *gtk.ApplicationWindow
	icon    gtk.Image
	word    gtk.Label
	refs    gtkx.Scope
	mon     *gdk.Monitor // the monitor it was built for, our reference
	hideGen uintptr      // the showing the hide timer belongs to
	fading  bool
}

// osdChanged says what the last update changed.
type osdChanged struct {
	kind string // "", "volume", "mute", "brightness", "wifi", "bluetooth"
	icon string
	word string
}

// osdState remembers what the last osd look was, to tell a change from an
// unrelated update.
type osdState struct {
	volume    float64
	muted     bool
	wifiOn    bool
	wifiKind  string
	wifiName  string
	btOn      bool
	btConnect string // the connected device's name, "" for none
}

// ensureOsd builds the display's window on the monitor the pointer is on.
// It survives; the card's contents change.
func (s *shellUI) ensureOsd(mon *gdk.Monitor) {
	o := &s.osd
	if o.win != nil {
		if o.mon != mon { // the pointer moved to another screen
			o.mon = mon
			if s.layer {
				layershell.SetMonitor(o.win.GoPointer(), mon.GoPointer())
			}
		}
		return
	}
	o.mon = mon // the bar's reference, borrowed
	o.win = &gtk.ApplicationWindow{}
	ui := s.load("osd.ui", &o.refs)
	ui.Get("osd", o.win)
	ui.Get("osd_icon", &o.icon)
	ui.Get("osd_text", &o.word)
	ui.Close()
	o.win.SetApplication(s.app)
	if s.layer {
		w := o.win.GoPointer()
		layershell.InitForWindow(w)
		layershell.SetNamespace(w, "inua-osd")
		layershell.SetLayer(w, layershell.LayerOverlay)
		layershell.SetKeyboardMode(w, layershell.KeyboardNone)
		s.placeOsd(w, mon)
	} else {
		o.win.SetTitle(i18n.T("inua osd"))
	}
	o.win.SetVisible(false)
}

// placeOsd anchors the display's window where the settings put it, on the
// monitor given.
func (s *shellUI) placeOsd(w uintptr, mon *gdk.Monitor) {
	top, left := false, false
	switch s.cfg.Osd.Position {
	case "top-right":
		top, left = true, false
	case "top-left":
		top, left = true, true
	case "bottom-center":
		top, left = false, true
	case "bottom-right":
		top, left = false, false
	case "bottom-left":
		top, left = false, true
	default: // "top-center"
		top, left = true, true
	}
	layershell.SetMonitor(w, mon.GoPointer())
	layershell.SetAnchor(w, layershell.EdgeTop, top)
	layershell.SetAnchor(w, layershell.EdgeBottom, !top)
	layershell.SetAnchor(w, layershell.EdgeLeft, left)
	layershell.SetAnchor(w, layershell.EdgeRight, !left)
}

// showOsd puts the icon and the word up for osdMS, replacing what was
// there.
func (s *shellUI) showOsd(c osdChanged) {
	if !s.cfg.Osd.Enable || c.kind == "" {
		return
	}
	mon := s.focusedMonitor()
	if mon == nil {
		return
	}
	s.ensureOsd(mon)
	o := &s.osd
	o.icon.SetFromIconName(c.icon)
	o.word.SetLabel(c.word)
	o.win.SetVisible(true)
	o.win.Present()
	o.fading = false
	toggle(&o.win.Widget, "fading", false)
	o.hideGen++
	glib.TimeoutAdd(osdMS, &s.onOsdHide, o.hideGen)
}

// bindOsdHandlers points the display's timers at their rules, once.
func (s *shellUI) bindOsdHandlers() {
	s.onOsdHide = func(data uintptr) bool {
		o := &s.osd
		if o.win == nil || data != o.hideGen {
			return false
		}
		o.fading = true
		toggle(&o.win.Widget, "fading", true)
		glib.TimeoutAdd(osdFade, &s.onOsdGone, data)
		return false
	}
	s.onOsdGone = func(data uintptr) bool {
		o := &s.osd
		if o.win == nil || data != o.hideGen || !o.fading {
			return false
		}
		o.win.SetVisible(false)
		o.fading = false
		return false
	}
}

// osdVolume builds the change for a volume or mute change.
func osdVolume(a system.AudioState, muted bool) osdChanged {
	switch {
	case !a.Available:
		return osdChanged{}
	case muted:
		return osdChanged{kind: "mute", icon: shell.VolumeIcon(a), word: i18n.T("Muted")}
	case a.Volume <= 0:
		return osdChanged{kind: "volume", icon: shell.VolumeIcon(a), word: shell.Percent(a.Volume)}
	default:
		return osdChanged{kind: "volume", icon: shell.VolumeIcon(a), word: shell.Percent(a.Volume)}
	}
}

// osdWifi builds the change for a Wi-Fi or connection change.
func osdWifi(n system.NetworkState, on bool) osdChanged {
	var word string
	switch {
	case on && n.Name != "":
		word = n.Name
	case on:
		word = i18n.T("Wi-Fi on")
	default:
		word = i18n.T("Wi-Fi off")
	}
	return osdChanged{kind: "wifi", icon: shell.NetIcon(n), word: word}
}

// osdBluetooth builds the change for a Bluetooth power or connection
// change.
func osdBluetooth(b system.BluetoothState) osdChanged {
	var word string
	switch {
	case len(b.Connected) > 0:
		word = b.Connected[0]
	case b.Powered:
		word = i18n.T("Bluetooth on")
	default:
		word = i18n.T("Bluetooth off")
	}
	icon := "bluetooth-active-symbolic"
	if !b.Powered {
		icon = "bluetooth-disabled-symbolic"
	}
	return osdChanged{kind: "bluetooth", icon: icon, word: word}
}

// checkOsd diffs the system state against the last look and shows the
// display for what changed. It runs in update, so every path to a change
// passes here once.
func (s *shellUI) checkOsd(st *shell.System) {
	o := &s.osdSeen
	c := osdChanged{}
	vol := st.Audio.Volume
	if vol != o.volume || st.Audio.Muted != o.muted {
		c = osdVolume(st.Audio, st.Audio.Muted)
	}
	if st.Net.WifiEnabled != o.wifiOn || st.Net.Kind != o.wifiKind || st.Net.Name != o.wifiName {
		c = osdWifi(st.Net, st.Net.WifiEnabled)
	}
	bt := ""
	if len(st.BT.Connected) > 0 {
		bt = st.BT.Connected[0]
	}
	if st.BT.Powered != o.btOn || bt != o.btConnect {
		c = osdBluetooth(st.BT)
	}
	*o = osdState{
		volume: vol, muted: st.Audio.Muted,
		wifiOn: st.Net.WifiEnabled, wifiKind: st.Net.Kind, wifiName: st.Net.Name,
		btOn: st.BT.Powered, btConnect: bt,
	}
	if c.kind != "" {
		s.showOsd(c)
	}
}

// osdFade is the fade out, matching .osd-card's transition.
const osdFade = 200
