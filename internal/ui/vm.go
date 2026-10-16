package ui

import (
	"fmt"

	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/gtkx"
	"github.com/lyricat/inua/internal/i18n"
	"github.com/lyricat/inua/internal/vm"
)

// vmState is the shell's Windows VM: the manager it drives and the window it
// shows, when one is open.
type vmState struct {
	manager *vmService
	win     *vmWindow
}

// VMManager is the UI-facing boundary for VM inspection and lifecycle actions.
// Implementations should perform long-running operations asynchronously and
// report changes with Update; all methods are invoked from GTK callbacks.
type VMManager interface {
	Snapshot() VMSnapshot
	AcceptProfile(vm.Config) error
	Configure(vm.Config) error
	Install() error
	Start() error
	Connect() error
	Console() error
	Stop() error
	Remove() error
	RemoveData() error
}

// VMSnapshot is a presentation-ready view of VM state.
type VMSnapshot struct {
	Config       vm.Config
	State        vm.State
	Doctor       string
	Progress     float64
	ProgressText string
	Busy         bool
	Available    bool
	HasConfig    bool
	Recommended  vm.Profile
	Host         vm.Host
	Err          error
}

type vmWindow struct {
	win                                                 *gtk.ApplicationWindow
	refs                                                gtkx.Scope
	manager                                             VMManager
	stateSub, doctor, progressText                      gtk.Label
	stateMark, notice, profileSummary                   gtk.Label
	progress                                            gtk.ProgressBar
	memory, cpus, disk                                  gtk.SpinButton
	advanced                                            gtk.Revealer
	advancedToggle                                      gtk.Button
	accept, configure, install, start, connect, console gtk.Button
	stop, remove, removeData                            gtk.Button
	closed                                              bool
	removeArmed                                         bool
	dataArmed                                           bool
	operationBusy                                       bool
	onClick                                             func(gtk.Button)
	onClose                                             func(gtk.Window) bool
}

// OpenVMManager builds the manager window. The layout goes through the
// shell's own loader, like every other window: gtkx.Load takes markup, not a
// file name, and passing the name was what made the shell panic on open.
func OpenVMManager(s *shellUI, manager VMManager) *vmWindow {
	v := &vmWindow{manager: manager, win: &gtk.ApplicationWindow{}}
	builder := s.load("vm.ui", &v.refs)
	builder.Get("vm", v.win)
	builder.Get("state_sub", &v.stateSub)
	builder.Get("state_mark", &v.stateMark)
	builder.Get("notice", &v.notice)
	builder.Get("profile_summary", &v.profileSummary)
	builder.Get("doctor", &v.doctor)
	builder.Get("progress", &v.progress)
	builder.Get("progress_text", &v.progressText)
	builder.Get("memory", &v.memory)
	builder.Get("cpus", &v.cpus)
	builder.Get("disk", &v.disk)
	builder.Get("advanced_toggle", &v.advancedToggle)
	builder.Get("advanced", &v.advanced)
	builder.Get("accept", &v.accept)
	builder.Get("configure", &v.configure)
	builder.Get("install", &v.install)
	builder.Get("start", &v.start)
	builder.Get("connect", &v.connect)
	builder.Get("console", &v.console)
	builder.Get("stop", &v.stop)
	builder.Get("remove", &v.remove)
	builder.Get("remove_data", &v.removeData)
	builder.Close()
	v.onClick = func(b gtk.Button) { v.clicked(b) }
	for _, b := range []*gtk.Button{&v.advancedToggle, &v.accept, &v.configure, &v.install,
		&v.start, &v.connect, &v.console, &v.stop, &v.remove, &v.removeData} {
		b.ConnectClicked(&v.onClick)
	}
	// The window is destroyed on close, like the settings window; the shell
	// drops its reference and makes the next open build a new one.
	v.onClose = func(gtk.Window) bool {
		s.closeVMManager()
		return false
	}
	v.win.ConnectCloseRequest(&v.onClose)
	v.Update(manager.Snapshot())
	v.win.Present()
	return v
}

// clicked dispatches the window's buttons by their id, one handler for all
// of them (puregotk makes one native trampoline per function).
func (v *vmWindow) clicked(b gtk.Button) {
	switch b.GetName() {
	case "advanced_toggle":
		v.advanced.SetRevealChild(!v.advanced.GetRevealChild())
	case "accept":
		v.acceptProfile()
	case "configure":
		v.configureProfile()
	case "install":
		v.run(v.manager.Install)
	case "start":
		v.run(v.manager.Start)
	case "connect":
		v.run(v.manager.Connect)
	case "console":
		v.run(v.manager.Console)
	case "stop":
		v.run(v.manager.Stop)
	case "remove":
		if !v.removeArmed {
			v.removeArmed = true
			v.remove.SetLabel(i18n.T("Confirm remove VM"))
			return
		}
		v.removeArmed = false
		v.remove.SetLabel(i18n.T("Remove VM"))
		v.run(v.manager.Remove)
	case "remove_data":
		if !v.dataArmed {
			v.dataArmed = true
			v.removeData.SetLabel(i18n.T("Confirm delete disk data"))
			return
		}
		v.dataArmed = false
		v.removeData.SetLabel(i18n.T("Delete disk data"))
		v.run(v.manager.RemoveData)
	}
}

// Update refreshes the window on the GTK main thread: the headline state, the
// notice when it cannot be used, the profile summary, the host checks and
// which actions make sense now.
func (v *vmWindow) Update(s VMSnapshot) {
	gtkx.Post(func() {
		if v.closed || v.win == nil {
			return
		}
		state := s.State
		if s.Err != nil {
			v.stateSub.SetText(i18n.T("Something went wrong"))
			v.notice.SetText(fmt.Sprintf("%s: %v", i18n.T("Error"), s.Err))
			v.notice.SetVisible(true)
		} else if !s.Available {
			v.stateSub.SetText(i18n.T("Unavailable"))
			v.notice.SetText(i18n.T("This system does not provide what the Windows VM needs; the checks below say what is missing."))
			v.notice.SetVisible(true)
		} else {
			v.stateSub.SetText(vmStateText(state, s.HasConfig))
			v.notice.SetVisible(false)
		}
		// The status mark: filled while the guest is up.
		toggle(&v.stateMark.Widget, "on", state == vm.StateRunning)

		// The guest's profile: what it is, or what it would be.
		cfg := s.Config
		if !s.HasConfig {
			cfg = vm.DefaultConfig()
			cfg.MemoryMiB, cfg.CPUs, cfg.DiskGiB = s.Recommended.MemoryMiB, s.Recommended.CPUs, s.Recommended.DiskGiB
		}
		v.profileSummary.SetText(fmt.Sprintf("%s %s · %s %s · %s %s",
			humanMiB(cfg.MemoryMiB), i18n.T("RAM"),
			fmt.Sprint(cfg.CPUs), i18n.T("CPU"),
			fmt.Sprint(cfg.DiskGiB), i18n.T("GiB")))

		doctor := s.Doctor
		if doctor == "" {
			doctor = i18n.T("Everything the guest needs is here.")
		}
		v.doctor.SetText(doctor)
		v.progress.SetFraction(s.Progress)
		v.progressText.SetText(s.ProgressText)

		v.remove.SetLabel(i18n.T("Remove"))
		v.removeData.SetLabel(i18n.T("Delete"))
		v.accept.SetSensitive(s.Available && !s.Busy && !s.HasConfig)
		v.configure.SetSensitive(s.Available && !s.Busy)
		v.install.SetSensitive(s.Available && !s.Busy)
		v.start.SetSensitive(s.Available && s.HasConfig && !s.Busy && state != vm.StateRunning)
		v.connect.SetSensitive(s.Available && !s.Busy && state == vm.StateRunning)
		v.console.SetSensitive(s.Available && s.HasConfig && !s.Busy)
		v.stop.SetSensitive(s.Available && !s.Busy && (state == vm.StateRunning || state == vm.StateStarting))
		v.remove.SetSensitive(s.Available && s.HasConfig && !s.Busy && state != vm.StateRunning)
		// Deleting the disk data is available even after the VM is removed, so a
		// user can clear the leftover guest image once the container is gone.
		v.removeData.SetSensitive(s.Available && !s.Busy && state != vm.StateRunning)
	})
}

// vmStateText is the headline for a state, in the shell's voice.
func vmStateText(state vm.State, hasConfig bool) string {
	switch {
	case !hasConfig:
		return i18n.T("Not set up yet")
	case state == vm.StateRunning:
		return i18n.T("Windows is running")
	case state == vm.StateStarting:
		return i18n.T("Starting, or installing Windows")
	case state == vm.StateStopping:
		return i18n.T("Stopping")
	case state == vm.StateStopped:
		return i18n.T("Stopped")
	case state == vm.StateFailed:
		return i18n.T("Failed")
	}
	return i18n.T("Not set up yet")
}

// humanMiB shows a memory size the way the other windows do.
func humanMiB(mib int) string {
	if mib >= 1024 {
		return fmt.Sprintf("%d GiB", mib/1024)
	}
	return fmt.Sprintf("%d MiB", mib)
}

func (v *vmWindow) configFromEditors() vm.Config {
	c := vm.DefaultConfig()
	c.MemoryMiB = int(v.memory.GetValueAsInt())
	c.CPUs = int(v.cpus.GetValueAsInt())
	c.DiskGiB = int(v.disk.GetValueAsInt())
	return c
}

func (v *vmWindow) acceptProfile() {
	s := v.manager.Snapshot()
	c := vm.DefaultConfig()
	c.MemoryMiB = s.Recommended.MemoryMiB
	c.CPUs = s.Recommended.CPUs
	c.DiskGiB = s.Recommended.DiskGiB
	v.run(func() error { return v.manager.AcceptProfile(c) })
}

func (v *vmWindow) configureProfile() {
	v.advanced.SetRevealChild(true)
	v.run(func() error { return v.manager.Configure(v.configFromEditors()) })
}

func (v *vmWindow) run(f func() error) {
	if v.closed || v.operationBusy {
		return
	}
	s := v.manager.Snapshot()
	if s.Busy {
		return
	}
	v.operationBusy = true
	s.Busy, s.Err = true, nil
	v.Update(s)
	go func() {
		err := f()
		s := v.manager.Snapshot()
		s.Err = err
		s.Busy = false
		gtkx.Post(func() { v.operationBusy = false; v.Update(s) })
	}()
}
