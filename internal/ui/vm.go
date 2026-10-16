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
	status, doctor, progressText                        gtk.Label
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
	builder.Get("vm_status", &v.status)
	builder.Get("vm_doctor", &v.doctor)
	builder.Get("vm_progress", &v.progress)
	builder.Get("vm_progress_text", &v.progressText)
	builder.Get("vm_memory", &v.memory)
	builder.Get("vm_cpus", &v.cpus)
	builder.Get("vm_disk", &v.disk)
	builder.Get("vm_advanced_toggle", &v.advancedToggle)
	builder.Get("vm_advanced", &v.advanced)
	builder.Get("vm_accept", &v.accept)
	builder.Get("vm_configure", &v.configure)
	builder.Get("vm_install", &v.install)
	builder.Get("vm_start", &v.start)
	builder.Get("vm_connect", &v.connect)
	builder.Get("vm_console", &v.console)
	builder.Get("vm_stop", &v.stop)
	builder.Get("vm_remove", &v.remove)
	builder.Get("vm_remove_data", &v.removeData)
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

// Update refreshes status and action availability on the GTK main thread.
func (v *vmWindow) Update(s VMSnapshot) {
	gtkx.Post(func() {
		if v.closed || v.win == nil {
			return
		}
		text := string(s.State)
		if text == "" {
			text = i18n.T("Not configured")
		}
		if s.Err != nil {
			text = fmt.Sprintf("%s: %v", i18n.T("Error"), s.Err)
		}
		if !s.Available {
			text = i18n.T("VM operations are unavailable on this system")
		}
		v.remove.SetLabel(i18n.T("Remove VM"))
		v.removeData.SetLabel(i18n.T("Delete disk data"))
		v.status.SetText(text)
		if s.Doctor == "" {
			s.Doctor = i18n.T("No issues reported")
		}
		v.doctor.SetText(s.Doctor)
		v.progress.SetFraction(s.Progress)
		v.progressText.SetText(s.ProgressText)
		v.accept.SetSensitive(s.Available && !s.Busy && !s.HasConfig)
		v.configure.SetSensitive(s.Available && !s.Busy)
		v.install.SetSensitive(s.Available && s.HasConfig && !s.Busy)
		v.start.SetSensitive(s.Available && s.HasConfig && !s.Busy)
		v.connect.SetSensitive(s.Available && !s.Busy && s.State == vm.StateRunning)
		v.stop.SetSensitive(s.Available && !s.Busy && s.State == vm.StateRunning)
		v.remove.SetSensitive(s.Available && s.HasConfig && !s.Busy && s.State != vm.StateRunning)
		// Deleting the disk data is available even after the VM is removed, so a
		// user can clear the leftover guest image once the container is gone.
		v.removeData.SetSensitive(s.Available && !s.Busy && s.State != vm.StateRunning)
	})
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
