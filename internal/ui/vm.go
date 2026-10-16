package ui

import (
	"fmt"
	"strings"

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
	// Fix applies a failing check's remedy, asking for the password through
	// the session's polkit agent when it needs one.
	Fix(vm.Remedy) (done string, relogin bool, err error)
}

// vmPhase is the window's page: what the guest's state means for the user.
type vmPhase string

const (
	phasePrereq       vmPhase = "prereq"       // the host is missing something
	phaseSetup        vmPhase = "setup"        // ready to install
	phaseProvisioning vmPhase = "provisioning" // pulling, or Windows is installing
	phaseReady        vmPhase = "ready"        // installed; start, connect, stop
)

// VMSnapshot is a presentation-ready view of VM state.
type VMSnapshot struct {
	Config       vm.Config
	State        vm.State
	Checks       []vm.DoctorItem // the host checks, shown on the prereq page
	Progress     float64
	ProgressText string
	Busy         bool
	Available    bool
	HasConfig    bool
	Recommended  vm.Profile
	Host         vm.Host
	Err          error
}

// phase is which page the state calls for.
func (s VMSnapshot) phase() vmPhase {
	if !s.Available {
		return phasePrereq
	}
	if !s.HasConfig {
		return phaseSetup
	}
	// A configured guest that is not ready yet is still being provisioned:
	// Docker is pulling the image, or Windows is installing for the first time.
	switch s.State {
	case vm.StateStarting, vm.StateStopping:
		return phaseProvisioning
	case vm.StateUnknown, vm.StateFailed:
		if s.Busy {
			return phaseProvisioning
		}
		return phaseReady
	}
	return phaseReady
}

// failedChecks are the host checks that did not pass.
func (s VMSnapshot) failedChecks() []vm.DoctorItem {
	var out []vm.DoctorItem
	for _, c := range s.Checks {
		if !c.OK {
			out = append(out, c)
		}
	}
	return out
}

type vmWindow struct {
	win     *gtk.ApplicationWindow
	refs    gtkx.Scope
	manager VMManager

	// Headline, shared by every page.
	sub, mark gtk.Label

	stack gtk.Stack

	// prereq
	checkRows gtk.Box

	// setup
	setupSummary                               gtk.Label
	profileDesc                                gtk.Label
	accept, advancedToggle, configure, install gtk.Button
	advanced                                   gtk.Revealer
	memory, cpus, disk                         gtk.SpinButton

	// provisioning
	progress          gtk.ProgressBar
	progressText      gtk.Label
	console, provStop gtk.Button

	// ready
	readySummary             gtk.Label
	readyMemory              gtk.SpinButton
	readyCPUs                gtk.SpinButton
	diskSize                 gtk.Label
	readySave                gtk.Button
	rowStart                 gtk.Box
	rowConnect               gtk.Box
	rowStop                  gtk.Box
	start, connect           gtk.Button
	consoleReady             gtk.Button
	stop, remove, removeData gtk.Button

	closed        bool
	removeArmed   bool
	dataArmed     bool
	operationBusy bool
	checkRefs     gtkx.Scope // the rows built for the current check list
	fixButtons    []fixTarget
	fixNote       string // what a fix did, shown until the next refresh
	onClick       func(gtk.Button)
	onClose       func(gtk.Window) bool
}

// OpenVMManager builds the manager window. The layout goes through the
// shell's own loader, like every other window: gtkx.Load takes markup, not a
// file name, and passing the name was what made the shell panic on open.
func OpenVMManager(s *shellUI, manager VMManager) *vmWindow {
	v := &vmWindow{manager: manager, win: &gtk.ApplicationWindow{}}
	builder := s.load("vm.ui", &v.refs)
	builder.Get("vm", v.win)
	builder.Get("vm_sub", &v.sub)
	builder.Get("vm_mark", &v.mark)
	builder.Get("vm_stack", &v.stack)
	builder.Get("vm_check_rows", &v.checkRows)
	builder.Get("vm_setup_summary", &v.setupSummary)
	builder.Get("vm_profile_desc", &v.profileDesc)
	builder.Get("vm_accept", &v.accept)
	builder.Get("vm_advanced_toggle", &v.advancedToggle)
	builder.Get("vm_advanced", &v.advanced)
	builder.Get("vm_memory", &v.memory)
	builder.Get("vm_cpus", &v.cpus)
	builder.Get("vm_disk", &v.disk)
	builder.Get("vm_configure", &v.configure)
	builder.Get("vm_install", &v.install)
	builder.Get("vm_progress", &v.progress)
	builder.Get("vm_progress_text", &v.progressText)
	builder.Get("vm_console", &v.console)
	builder.Get("vm_prov_stop", &v.provStop)
	builder.Get("vm_ready_summary", &v.readySummary)
	builder.Get("vm_ready_memory", &v.readyMemory)
	builder.Get("vm_ready_cpus", &v.readyCPUs)
	builder.Get("vm_disk_size", &v.diskSize)
	builder.Get("vm_ready_save", &v.readySave)
	builder.Get("vm_row_start", &v.rowStart)
	builder.Get("vm_row_connect", &v.rowConnect)
	builder.Get("vm_row_stop", &v.rowStop)
	builder.Get("vm_start", &v.start)
	builder.Get("vm_connect", &v.connect)
	builder.Get("vm_console_ready", &v.consoleReady)
	builder.Get("vm_stop", &v.stop)
	builder.Get("vm_remove", &v.remove)
	builder.Get("vm_remove_data", &v.removeData)
	builder.Close()
	v.onClick = func(b gtk.Button) { v.clicked(b) }
	for _, b := range []*gtk.Button{&v.accept, &v.advancedToggle, &v.configure, &v.install,
		&v.console, &v.provStop, &v.readySave, &v.start, &v.connect, &v.consoleReady,
		&v.stop, &v.remove, &v.removeData} {
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
		v.run(func() error { return v.manager.Configure(v.setupConfig()) })
	case "ready_save":
		v.run(func() error { return v.manager.Configure(v.readyConfig()) })
	case "install":
		v.run(v.manager.Install)
	case "start":
		v.run(v.manager.Start)
	case "connect":
		v.run(v.manager.Connect)
	case "console", "console_ready":
		v.run(v.manager.Console)
	case "prov_stop", "stop":
		v.run(v.manager.Stop)
	case "remove":
		if !v.removeArmed {
			v.removeArmed = true
			v.remove.SetLabel(i18n.T("Confirm remove"))
			return
		}
		v.removeArmed = false
		v.remove.SetLabel(i18n.T("Remove"))
		v.run(v.manager.Remove)
	case "remove_data":
		if !v.dataArmed {
			v.dataArmed = true
			v.removeData.SetLabel(i18n.T("Confirm delete"))
			return
		}
		v.dataArmed = false
		v.removeData.SetLabel(i18n.T("Delete"))
		v.run(v.manager.RemoveData)
	case "fix":
		for _, t := range v.fixButtons {
			if t.btn.GoPointer() == b.GoPointer() {
				v.applyFix(t.remedy)
				return
			}
		}
	}
}

// applyFix runs a remedy. The polkit dialog it may open lives on the main
// thread, so the work goes to a goroutine (as the other actions do) and the
// result comes back to the window.
func (v *vmWindow) applyFix(r vm.Remedy) {
	if v.operationBusy {
		return
	}
	v.operationBusy = true
	go func() {
		_, relogin, err := v.manager.Fix(r)
		gtkx.Post(func() {
			v.operationBusy = false
			switch {
			case err != nil:
				v.fixNote = i18n.Tf("The fix did not work: %v", err)
			case relogin:
				// A process's group list is fixed when it starts, so the
				// change is real but this session cannot see it yet.
				v.fixNote = i18n.T("Done. Log out and back in for it to take effect.")
			default:
				v.fixNote = i18n.T("Done.")
			}
			v.Update(v.manager.Snapshot())
		})
	}()
}

// Update refreshes the window on the GTK main thread: it picks the page the
// guest's state calls for, fills the headline, and shows only the controls
// that can do something useful there.
func (v *vmWindow) Update(s VMSnapshot) {
	gtkx.Post(func() {
		if v.closed || v.win == nil {
			return
		}
		v.stack.SetVisibleChildName(string(s.phase()))
		// A fix's outcome outranks the state line: it is what the user just
		// did, and a group change only takes hold at the next login. It stays
		// up until something else replaces it.
		if v.fixNote != "" {
			v.sub.SetText(v.fixNote)
		} else {
			v.sub.SetText(vmStateText(s))
		}
		toggle(&v.mark.Widget, "on", s.State == vm.StateRunning && s.Err == nil)

		switch s.phase() {
		case phasePrereq:
			v.showChecks(s.failedChecks())
		case phaseSetup:
			v.showSetup(s)
		case phaseProvisioning:
			v.showProvisioning(s)
		case phaseReady:
			v.showReady(s)
		}
	})
}

// showChecks lists what the host is missing, one row each, in the user's
// language: the platform reports a reason, not a sentence.
func (v *vmWindow) showChecks(items []vm.DoctorItem) {
	v.checkRefs.Release()
	v.fixButtons = nil
	gtkx.Clear(&v.checkRows)
	for _, c := range items {
		row := gtk.NewBox(gtk.OrientationHorizontalValue, 12)
		row.AddCssClass("row")

		mark := gtk.NewLabel("")
		mark.AddCssClass("mark")
		mark.SetValign(gtk.AlignCenterValue)
		gtkx.Append(row, &mark.Widget)

		text := gtk.NewBox(gtk.OrientationVerticalValue, 2)
		text.SetHexpand(true)
		text.SetValign(gtk.AlignCenterValue)
		name := gtk.NewLabel(vmCheckName(c.Name))
		name.AddCssClass("label")
		name.SetXalign(0)
		text2 := gtk.NewLabel(vmCheckReason(c.Reason))
		text2.AddCssClass("sub")
		text2.SetXalign(0)
		text2.SetWrap(true)
		gtkx.Append(text, &name.Widget)
		gtkx.Append(text, &text2.Widget)
		gtkx.Append(row, &text.Widget)

		// What the user can do about it: a button when Inua can apply the
		// fix itself, the platform's instructions when it cannot.
		switch {
		case c.Remedy != nil:
			label := i18n.T("Fix")
			if c.Remedy.Group != "" {
				label = i18n.Tf("Add me to %s", c.Remedy.Group)
			}
			btn := gtk.NewButtonWithLabel(label)
			btn.AddCssClass("outlined")
			btn.SetValign(gtk.AlignCenterValue)
			btn.SetName("fix")
			v.fixButtons = append(v.fixButtons, fixTarget{btn: *btn, remedy: *c.Remedy})
			btn.ConnectClicked(&v.onClick)
			gtkx.Append(row, &btn.Widget)
		default:
			// A package to install, named for this distribution.
			if hint := vmPackageHint(c.Name); hint != "" {
				hintLabel := gtk.NewLabel(hint)
				hintLabel.AddCssClass("sub")
				hintLabel.AddCssClass("vm-hint")
				hintLabel.SetValign(gtk.AlignCenterValue)
				gtkx.Append(row, &hintLabel.Widget)
			}
		}
		gtkx.Append(&v.checkRows, &row.Widget)
	}
}

// fixTarget ties a button to the remedy it applies.
type fixTarget struct {
	btn    gtk.Button
	remedy vm.Remedy
}

// vmPackageHint is how to install a missing tool on this distribution, as a
// line the user can copy. The window never runs a package manager: choosing
// packages and changing a system is the user's call, not a button's.
func vmPackageHint(check string) string {
	pkg := map[string]string{
		"docker":           "docker",
		"docker-compose":   "docker-compose",
		"freerdp":          "freerdp",
		"xdg-open":         "xdg-utils",
		"operating system": "",
		"secret service":   "gnome-keyring",
	}[strings.ToLower(check)]
	if pkg == "" {
		return ""
	}
	return i18n.T("Install") + ": " + pkg
}

// vmCheckName is a check's name. The platform names them in English; these
// are the ones the window shows.
func vmCheckName(name string) string {
	switch name {
	case "Operating system":
		return i18n.T("Operating system")
	case "KVM":
		return i18n.T("Hardware virtualization (KVM)")
	case "Docker":
		return i18n.T("Docker")
	case "Docker Compose v2":
		return i18n.T("Docker Compose v2")
	case "FreeRDP":
		return i18n.T("FreeRDP")
	case "Browser opener":
		return i18n.T("Browser opener")
	case "Disk":
		return i18n.T("Disk space")
	case "TUN":
		return i18n.T("Network device (TUN)")
	case "Secret Service":
		return i18n.T("Secret Service")
	}
	return name
}

// vmCheckReason words why a check failed.
func vmCheckReason(r vm.DoctorReason) string {
	switch r {
	case vm.ReasonMissing:
		return i18n.T("Not installed on this system.")
	case vm.ReasonDenied:
		return i18n.T("Installed, but your user may not use it.")
	case vm.ReasonStopped:
		return i18n.T("Installed, but not running.")
	case vm.ReasonTooOld:
		return i18n.T("This Linux distribution is not supported.")
	}
	return i18n.T("Could not be checked.")
}

// showSetup fills the page shown before anything is installed: the profile
// to use, and the one action that means "install now".
func (v *vmWindow) showSetup(s VMSnapshot) {
	c := vm.DefaultConfig()
	c.MemoryMiB, c.CPUs, c.DiskGiB = s.Recommended.MemoryMiB, s.Recommended.CPUs, s.Recommended.DiskGiB
	if !v.advanced.GetRevealChild() {
		v.memory.SetValue(float64(c.MemoryMiB))
		v.cpus.SetValue(float64(c.CPUs))
		v.disk.SetValue(float64(c.DiskGiB))
	}
	v.setupSummary.SetText(vmProfileText(c))
	v.profileDesc.SetText(i18n.T("A balanced profile leaves memory and CPU for your system."))
	v.accept.SetSensitive(!s.Busy)
	v.configure.SetSensitive(!s.Busy)
	v.install.SetSensitive(!s.Busy)
	v.advancedToggle.SetSensitive(!s.Busy)
}

// showProvisioning fills the page shown while Docker pulls the image or
// Windows installs for the first time. It offers the web console (the only
// view of the guest that works yet) and stopping without losing the disk.
func (v *vmWindow) showProvisioning(s VMSnapshot) {
	v.progress.SetFraction(s.Progress)
	if s.ProgressText != "" {
		v.progressText.SetText(s.ProgressText)
	} else if s.State == vm.StateStopping {
		v.progressText.SetText(i18n.T("Stopping…"))
	} else if s.Busy {
		v.progressText.SetText(i18n.T("Windows is installing; this takes a while."))
	} else {
		v.progressText.SetText(i18n.T("Starting the guest…"))
	}
	v.console.SetSensitive(!s.Busy)
	v.provStop.SetSensitive(!s.Busy && s.State != vm.StateStopping)
}

// showReady fills the page shown once a guest is installed. The memory and
// CPU rows are editable (they take effect on the next start); the disk size
// is shown for information, since enlarging it needs a manual resize inside
// Windows.
func (v *vmWindow) showReady(s VMSnapshot) {
	c := s.Config
	if c.Name == "" {
		c = vm.DefaultConfig()
	}
	v.readySummary.SetText(vmProfileText(c))
	if v.readyMemory.GetValueAsInt() == 0 {
		v.readyMemory.SetValue(float64(c.MemoryMiB))
		v.readyCPUs.SetValue(float64(c.CPUs))
	}
	v.diskSize.SetText(fmt.Sprintf("%d GiB", c.DiskGiB))

	running := s.State == vm.StateRunning
	// Only the rows that apply: starting a running guest, or stopping a
	// stopped one, is not an action the user can want.
	v.rowStart.SetVisible(!running)
	v.rowConnect.SetVisible(running)
	v.rowStop.SetVisible(running)
	v.start.SetSensitive(!s.Busy)
	v.connect.SetSensitive(!s.Busy)
	v.consoleReady.SetSensitive(!s.Busy)
	v.stop.SetSensitive(!s.Busy)
	v.readySave.SetSensitive(!s.Busy)
	v.remove.SetSensitive(!s.Busy && !running)
	v.removeData.SetSensitive(!s.Busy && !running)
}

// vmStateText is the headline for a state, in the shell's voice.
func vmStateText(s VMSnapshot) string {
	if s.Err != nil {
		return i18n.T("Something went wrong")
	}
	switch s.phase() {
	case phasePrereq:
		return i18n.T("This system is missing something Windows needs")
	case phaseSetup:
		return i18n.T("Not installed yet")
	case phaseProvisioning:
		if s.State == vm.StateStopping {
			return i18n.T("Stopping")
		}
		return i18n.T("Installing Windows")
	}
	switch s.State {
	case vm.StateRunning:
		return i18n.T("Windows is running")
	case vm.StateStopped:
		return i18n.T("Stopped")
	case vm.StateFailed:
		return i18n.T("Failed")
	}
	return i18n.T("Ready")
}

// vmProfileText is the guest's resources, as the section meta reads them.
func vmProfileText(c vm.Config) string {
	return fmt.Sprintf("%s · %d CPU · %d GiB", humanMiB(c.MemoryMiB), c.CPUs, c.DiskGiB)
}

// humanMiB shows a memory size the way the other windows do.
func humanMiB(mib int) string {
	if mib >= 1024 {
		return fmt.Sprintf("%d GiB", mib/1024)
	}
	return fmt.Sprintf("%d MiB", mib)
}

// setupConfig is the profile as the setup page's editors show it.
func (v *vmWindow) setupConfig() vm.Config {
	c := vm.DefaultConfig()
	c.MemoryMiB = int(v.memory.GetValueAsInt())
	c.CPUs = int(v.cpus.GetValueAsInt())
	c.DiskGiB = int(v.disk.GetValueAsInt())
	return c
}

// readyConfig is the guest's configuration with the editable resources
// taken from the ready page; the disk keeps its configured size.
func (v *vmWindow) readyConfig() vm.Config {
	c := v.manager.Snapshot().Config
	if c.Name == "" {
		return vm.DefaultConfig()
	}
	c.MemoryMiB = int(v.readyMemory.GetValueAsInt())
	c.CPUs = int(v.readyCPUs.GetValueAsInt())
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
