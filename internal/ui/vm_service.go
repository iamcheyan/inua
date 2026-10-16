package ui

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"net"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"sync"
	"syscall"
	"time"

	"github.com/godbus/dbus/v5"

	"github.com/lyricat/inua/internal/ipc"
	"github.com/lyricat/inua/internal/keyring"
	"github.com/lyricat/inua/internal/vm"
)

// shellVMManager is the shell's implementation of VMManager: it owns the
// Docker backend, the persisted configuration and the operation lock.
type vmService struct {
	mu         sync.Mutex
	backend    *vm.DockerBackend
	config     vm.Config
	host       vm.Host
	platform   vm.Platform
	hasConfig  bool
	busy       bool
	err        error
	state      vm.State
	stateErr   error
	refreshing bool
	secretConn *dbus.Conn // the Secret Service session, held for the shell's life
}

// vmSecretStore keeps the guest password in the Secret Service under inua's
// own attributes; the Compose environment file is written from it at start.
type vmSecretStore struct{ client *keyring.Client }

func vmSecretAttrs(id string) map[string]string {
	return map[string]string{"application": "inua", "kind": "windows-vm", "id": id}
}
func (s vmSecretStore) Store(ctx context.Context, id string, value []byte) error {
	return s.client.Store(ctx, "Inua Windows VM", vmSecretAttrs(id), value)
}
func (s vmSecretStore) Load(ctx context.Context, id string) ([]byte, error) {
	v, ok, err := s.client.Lookup(ctx, vmSecretAttrs(id))
	if err != nil {
		return nil, err
	}
	if !ok {
		return nil, errors.New("the Windows VM password is missing from the Secret Service")
	}
	return v, nil
}
func (s vmSecretStore) Delete(_ context.Context, id string) error {
	return s.client.Delete(vmSecretAttrs(id))
}

type vmPersisted struct {
	Config    vm.Config `json:"config"`
	Installed bool      `json:"installed"`
}

func newVMService() *vmService {
	s := &vmService{host: vm.DetectHost(""), platform: vm.DetectPlatform("", vm.PlatformProbes{})}
	s.config = vm.DefaultConfig()
	s.backend = vm.NewDockerBackend(nil)
	// The Secret Service session must outlive this call: closing the bus
	// connection here would break every later password read.
	if conn, err := dbus.ConnectSessionBus(); err == nil {
		if client, err := keyring.Connect(conn, keyring.AlgDH); err == nil {
			s.secretConn = conn
			s.backend.Secrets = vmSecretStore{client: client}
		} else {
			_ = conn.Close()
		}
	}
	s.load()
	return s
}

func (s *vmService) load() {
	data, err := os.ReadFile(vm.ConfigPath())
	if err != nil {
		return
	}
	var saved vmPersisted
	if json.Unmarshal(data, &saved) != nil || saved.Config.Validate() != nil {
		return
	}
	s.mu.Lock()
	s.config, s.hasConfig = saved.Config, saved.Installed
	s.backend.SetInstalled(saved.Config)
	s.mu.Unlock()
}

// snapshot is non-blocking: it reports the state last observed by refresh,
// because its callers run on the GTK main thread. Reading Docker there (a
// subprocess, up to seconds) would stall the whole shell.
func (s *vmService) snapshot() VMSnapshot {
	s.mu.Lock()
	cfg, has, busy, oldErr, state, stateErr := s.config, s.hasConfig, s.busy, s.err, s.state, s.stateErr
	s.mu.Unlock()
	if !has {
		state = vm.StateStopped
	}
	// The host checks, one line each, so the window can show every check and
	// mark the ones that fail.
	checks := make([]vm.DoctorItem, 0, len(s.platform.Doctor)+1)
	checks = append(checks, s.platform.Doctor...)
	if s.backend.Secrets == nil {
		checks = append(checks, vm.DoctorItem{
			Name:   "Secret Service",
			OK:     false,
			Reason: vm.ReasonMissing,
		})
	}
	available := s.platform.Supported && s.platform.KVM.Available && s.platform.KVM.Accessible &&
		s.platform.DockerSocket.Available && s.platform.DockerSocket.Accessible &&
		s.platform.ComposeV2.Available && s.platform.FreeRDP.Available && s.backend.Secrets != nil
	err := stateErr
	if err == nil {
		err = oldErr
	}
	return VMSnapshot{Config: cfg, State: state, Checks: checks, Busy: busy,
		Available: available, HasConfig: has, Recommended: vm.RecommendProfile(s.host), Host: s.host, Err: err}
}

// refresh reads the backend state off the main thread and records it for
// snapshot; overlapping calls collapse into the one already running.
func (s *vmService) refresh() {
	s.mu.Lock()
	if s.refreshing {
		s.mu.Unlock()
		return
	}
	s.refreshing = true
	has := s.hasConfig
	s.mu.Unlock()
	go func() {
		var state vm.State
		var err error
		if has {
			ctx, cancel := context.WithTimeout(context.Background(), 15*time.Second)
			state, err = s.backend.State(ctx)
			cancel()
		} else {
			state = vm.StateStopped
		}
		s.mu.Lock()
		if has {
			s.state, s.stateErr = state, err
		} else {
			s.state, s.stateErr = vm.StateStopped, nil
		}
		s.refreshing = false
		s.mu.Unlock()
	}()
}

// Snapshot, Doctor and Status are the UI-facing reads; all are non-blocking.
func (s *vmService) Snapshot() VMSnapshot { return s.snapshot() }

// Doctor is the checks as plain lines, for `inua call vm doctor`.
func (s *vmService) Doctor() string {
	var b strings.Builder
	for _, c := range s.snapshot().Checks {
		if c.OK {
			fmt.Fprintf(&b, "OK   %s\n", c.Name)
			continue
		}
		fmt.Fprintf(&b, "FAIL %s (%s)\n", c.Name, c.Reason)
	}
	return strings.TrimRight(b.String(), "\n")
}

func (s *vmService) Status() (vm.State, error) {
	x := s.snapshot()
	if x.Err != nil {
		return x.State, x.Err
	}
	return x.State, nil
}

// AcceptProfile saves the recommendation as the VM's configuration.
func (s *vmService) AcceptProfile(c vm.Config) error { return s.Configure(c) }

// Configure writes the Compose project and remembers the configuration, but
// does not start the VM: the image download and first Windows installation are
// their own, visible step (Start).
func (s *vmService) Configure(c vm.Config) error {
	if err := c.Validate(); err != nil {
		return err
	}
	if err := s.begin(); err != nil {
		return err
	}
	var opErr error
	defer func() { s.end(opErr) }()
	ctx, cancel := context.WithTimeout(context.Background(), 20*time.Minute)
	defer cancel()
	if err := s.backend.Install(ctx, c); err != nil {
		opErr = err
		return err
	}
	s.mu.Lock()
	s.config, s.hasConfig = c, true
	s.mu.Unlock()
	if err := s.save(true); err != nil {
		opErr = err
		return err
	}
	return nil
}

func (s *vmService) Install() error { return s.Start() }

func (s *vmService) Start() error {
	if err := s.begin(); err != nil {
		return err
	}
	var opErr error
	defer func() { s.end(opErr) }()
	if s.backend.Secrets == nil {
		opErr = errors.New("the Secret Service is unavailable; the Windows VM password cannot be kept safely")
		return opErr
	}
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Hour)
	defer cancel()
	opErr = s.backend.Start(ctx)
	return opErr
}

func (s *vmService) Connect() error {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	c, err := s.backend.Connect(ctx)
	if err != nil {
		return err
	}
	return startRDPClient(c.Address, c.Port)
}

// Console opens the container's web console in the browser: during the first
// Windows installation it is the only usable view of the guest.
func (s *vmService) Console() error {
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()
	url, err := s.backend.Console(ctx)
	if err != nil {
		return err
	}
	return openBrowser(url)
}

// openBrowser hands a URL to the desktop's opener.
func openBrowser(url string) error {
	bin, err := exec.LookPath("xdg-open")
	if err != nil {
		return errors.New("no browser opener (xdg-open) is installed")
	}
	cmd := exec.Command(bin, url)
	cmd.SysProcAttr = &syscall.SysProcAttr{Setsid: true}
	if err := cmd.Start(); err != nil {
		return err
	}
	go cmd.Wait()
	return nil
}

func (s *vmService) Stop() error {
	if err := s.begin(); err != nil {
		return err
	}
	var opErr error
	defer func() { s.end(opErr) }()
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Minute)
	defer cancel()
	opErr = s.backend.Stop(ctx)
	return opErr
}

func (s *vmService) Remove() error {
	if err := s.begin(); err != nil {
		return err
	}
	var opErr error
	defer func() { s.end(opErr) }()
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Minute)
	defer cancel()
	if err := s.backend.Remove(ctx); err != nil {
		opErr = err
		return err
	}
	if err := os.Remove(vm.ConfigPath()); err != nil && !errors.Is(err, os.ErrNotExist) {
		opErr = err
		return err
	}
	s.mu.Lock()
	s.hasConfig, s.config = false, vm.DefaultConfig()
	s.mu.Unlock()
	return nil
}

// RemoveData deletes the guest disk. It runs only after Remove (or when no
// configuration remains), so the container that had the disk mounted is gone.
func (s *vmService) RemoveData() error {
	if err := s.begin(); err != nil {
		return err
	}
	var opErr error
	defer func() { s.end(opErr) }()
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Minute)
	defer cancel()
	if opErr = s.backend.RemoveData(ctx); opErr != nil {
		return opErr
	}
	if err := os.Remove(vm.ConfigPath()); err != nil && !errors.Is(err, os.ErrNotExist) {
		opErr = err
		return err
	}
	s.mu.Lock()
	s.hasConfig, s.config = false, vm.DefaultConfig()
	s.mu.Unlock()
	return nil
}

func (s *vmService) begin() error {
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.busy {
		return errors.New("another Windows VM operation is in progress")
	}
	s.busy, s.err = true, nil
	return nil
}
func (s *vmService) end(err error) {
	s.mu.Lock()
	s.busy, s.err = false, err
	s.mu.Unlock()
	s.refresh() // so the next status shows what the operation did
}

func (s *vmService) save(installed bool) error {
	if err := os.MkdirAll(filepath.Dir(vm.ConfigPath()), 0700); err != nil {
		return err
	}
	s.mu.Lock()
	data, err := json.MarshalIndent(vmPersisted{Config: s.config, Installed: installed}, "", "  ")
	s.mu.Unlock()
	if err != nil {
		return err
	}
	tmp, err := os.CreateTemp(filepath.Dir(vm.ConfigPath()), ".vm-*.tmp")
	if err != nil {
		return err
	}
	name := tmp.Name()
	defer os.Remove(name)
	if err = tmp.Chmod(0600); err == nil {
		_, err = tmp.Write(append(data, '\n'))
	}
	if err == nil {
		err = tmp.Sync()
	}
	if closeErr := tmp.Close(); err == nil {
		err = closeErr
	}
	if err != nil {
		return err
	}
	return os.Rename(name, vm.ConfigPath())
}

func (s *vmService) profileConfig() vm.Config {
	p := vm.RecommendProfile(s.host)
	c := vm.DefaultConfig()
	c.MemoryMiB, c.CPUs, c.DiskGiB = p.MemoryMiB, p.CPUs, p.DiskGiB
	return c
}

func (s *shellUI) vmRequest(fn string) ipc.Response {
	m := s.vm.manager
	switch fn {
	case "open":
		s.openVMManager()
	case "status":
		// The cached state goes out at once and the next read refreshes it,
		// so the shell's main loop never waits on Docker.
		x := m.Snapshot()
		m.refresh()
		if x.Err != nil {
			return ipc.Response{Error: x.Err.Error()}
		}
		return ipc.Response{OK: true, Result: string(x.State)}
	case "doctor":
		return ipc.Response{OK: true, Result: m.Doctor()}
	case "configure":
		// Write the project from the recommended profile, without starting.
		return asyncVM(fn, func() error { return m.Configure(m.profileConfig()) })
	case "install":
		// A one-shot first install, as the name suggests: write the project
		// from the recommended profile when there is none, then start the
		// container, which downloads the image and installs Windows.
		return asyncVM(fn, func() error {
			if !m.Snapshot().HasConfig {
				if err := m.Configure(m.profileConfig()); err != nil {
					return err
				}
			}
			return m.Start()
		})
	case "connect":
		return asyncVM(fn, m.Connect)
	case "stop":
		return asyncVM(fn, m.Stop)
	case "remove":
		return asyncVM(fn, m.Remove)
	case "remove-data":
		return asyncVM(fn, m.RemoveData)
	default:
		return ipc.Response{Error: "unknown vm function " + fn}
	}
	return ipc.Response{OK: true}
}

// asyncVM runs a long lifecycle action without blocking the control socket
// (the shell's main loop must keep running), and reports the failure the
// caller would otherwise never see. The manager serializes the operations, so
// a second request is refused rather than racing.
func asyncVM(name string, action func() error) ipc.Response {
	go func() {
		if err := action(); err != nil {
			logErr("vm "+name, err)
		}
	}()
	return ipc.Response{OK: true}
}

// startRDPClient opens FreeRDP on a loopback endpoint.
func startRDPClient(address string, port int) error {
	for _, name := range []string{"xfreerdp3", "xfreerdp"} {
		bin, err := exec.LookPath(name)
		if err != nil {
			continue
		}
		args := []string{"/v:" + net.JoinHostPort(address, fmt.Sprint(port)), "/f", "/dynamic-resolution", "/cert:tofu", "/clipboard"}
		cmd := exec.Command(bin, args...)
		cmd.SysProcAttr = &syscall.SysProcAttr{Setsid: true}
		if err := cmd.Start(); err != nil {
			return err
		}
		go cmd.Wait()
		return nil
	}
	return errors.New("FreeRDP is not installed")
}
