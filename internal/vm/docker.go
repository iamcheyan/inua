package vm

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"errors"
	"fmt"
	"io"
	"net"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"
)

const (
	dockerComposeFile = "compose.yaml"
	dockerImage       = "dockurr/windows"
	rdpReadyTimeout   = 2 * time.Hour
)

// Docker Compose passes PASSWORD to daemon container metadata. Docker access
// is root-equivalent; users must trust the daemon.
// CommandRunner is injectable so backend behavior can be exercised without Docker.
type CommandRunner interface {
	Run(context.Context, string, ...string) (string, error)
}
type GuestSecretStore interface {
	Store(context.Context, string, []byte) error
	Load(context.Context, string) ([]byte, error)
	Delete(context.Context, string) error
}

type execCommandRunner struct{}

func (execCommandRunner) Run(ctx context.Context, name string, args ...string) (string, error) {
	cmd := exec.CommandContext(ctx, name, args...)
	var stdout strings.Builder
	cmd.Stdout = &stdout
	cmd.Stderr = io.Discard
	err := cmd.Run()
	return stdout.String(), err
}

// DockerBackend manages one Dockur Windows container using Docker Compose v2.
type DockerBackend struct {
	Runner       CommandRunner
	Secrets      GuestSecretStore
	WaitInterval time.Duration
	Config       Config
	composePath  string
	secretID     string
}

func NewDockerBackend(runner CommandRunner) *DockerBackend {
	if runner == nil {
		runner = execCommandRunner{}
	}
	return &DockerBackend{Runner: runner, WaitInterval: time.Second}
}

func (b *DockerBackend) Install(ctx context.Context, cfg Config) error {
	if err := cfg.Validate(); err != nil {
		return err
	}
	if err := safeOwnedDir(cfg.DataDir); err != nil {
		return vmError("install", ErrorInvalidConfig, err)
	}
	composeDir := filepath.Join(configBase(), "inua", "vm", cfg.Name)
	if err := safeOwnedDir(composeDir); err != nil {
		return vmError("install", ErrorInvalidConfig, err)
	}
	composePath := filepath.Join(composeDir, dockerComposeFile)
	if err := rejectPathSymlinks(composePath); err != nil {
		return vmError("install", ErrorInvalidConfig, err)
	}
	if _, err := os.Lstat(composePath); err == nil {
		return vmError("install", ErrorConflict, errors.New("compose file already exists"))
	} else if !errors.Is(err, os.ErrNotExist) {
		return vmError("install", ErrorBackend, err)
	}
	if b.Secrets == nil {
		return vmError("install", ErrorUnavailable, errors.New("secure guest password storage is unavailable"))
	}
	password, err := newGuestPassword()
	if err != nil {
		return vmError("install", ErrorBackend, err)
	}
	secretID := "inua/windows/" + cfg.Name
	if err := b.Secrets.Store(ctx, secretID, password); err != nil {
		clear(password)
		return vmError("install", ErrorUnavailable, err)
	}
	defer clear(password)
	envPath := filepath.Join(composeDir, ".guest.env")
	if _, err := os.Lstat(envPath); err == nil {
		_ = b.Secrets.Delete(ctx, secretID)
		return vmError("install", ErrorConflict, errors.New("credential env file already exists"))
	} else if !errors.Is(err, os.ErrNotExist) {
		_ = b.Secrets.Delete(ctx, secretID)
		return vmError("install", ErrorBackend, err)
	}
	if err := writeAtomic(envPath, []byte("PASSWORD="+string(password)+"\n"), 0600); err != nil {
		_ = b.Secrets.Delete(ctx, secretID)
		return vmError("install", ErrorBackend, err)
	}
	content := fmt.Sprintf("services:\n  windows:\n    image: %s\n    container_name: inua-%s\n    environment:\n      VERSION: \"11\"\n      USERNAME: \"Inua\"\n      RAM_SIZE: \"%dG\"\n      CPU_CORES: \"%d\"\n      DISK_SIZE: \"%dG\"\n    env_file:\n      - %s\n    devices:\n      - /dev/kvm\n      - /dev/net/tun\n    cap_add:\n      - NET_ADMIN\n    ports:\n      - \"127.0.0.1:%d:3389/tcp\"\n      - \"127.0.0.1:%d:3389/udp\"\n      - \"127.0.0.1:8006:8006\"\n    volumes:\n      - %s\n    restart: unless-stopped\n    stop_grace_period: 2m\n", dockerImage, cfg.Name, cfg.MemoryMiB/1024, cfg.CPUs, cfg.DiskGiB, yamlQuote(filepath.Join(composeDir, ".guest.env")), cfg.RDPPort, cfg.RDPPort, yamlQuote(cfg.DataDir+":/storage"))
	if err := writeAtomic(composePath, []byte(content), 0600); err != nil {
		_ = b.Secrets.Delete(ctx, secretID)
		return vmError("install", ErrorBackend, err)
	}
	b.Config, b.composePath, b.secretID = cfg, composePath, secretID
	return nil
}

func (b *DockerBackend) Start(ctx context.Context) error {
	if err := b.ensureInstalled(); err != nil {
		return vmError("start", ErrorConflict, err)
	}
	if b.Secrets == nil || b.secretID == "" {
		return vmError("start", ErrorUnavailable, errors.New("secure guest password storage is unavailable"))
	}
	password, err := b.Secrets.Load(ctx, b.secretID)
	if err != nil {
		return vmError("start", ErrorUnavailable, err)
	}
	defer clear(password)
	envPath := filepath.Join(filepath.Dir(b.composePath), ".guest.env")
	if err := writeAtomic(envPath, []byte("PASSWORD="+string(password)+"\n"), 0600); err != nil {
		return vmError("start", ErrorBackend, err)
	}
	if _, err := b.compose(ctx, "up", "-d"); err != nil {
		return vmError("start", ErrorBackend, err)
	}
	deadline := time.NewTimer(rdpReadyTimeout)
	defer deadline.Stop()
	interval := b.WaitInterval
	if interval <= 0 {
		interval = time.Second
	}
	ticker := time.NewTicker(interval)
	defer ticker.Stop()
	for {
		ready, err := b.rdpReady(ctx)
		if err == nil && ready {
			return nil
		}
		select {
		case <-ctx.Done():
			return vmError("start", ErrorUnavailable, ctx.Err())
		case <-deadline.C:
			return vmError("start", ErrorUnavailable, errors.New("Windows guest did not become RDP-ready before timeout"))
		case <-ticker.C:
		}
	}
}

func (b *DockerBackend) State(ctx context.Context) (State, error) {
	if err := b.ensureInstalled(); err != nil {
		return StateUnknown, vmError("state", ErrorConflict, err)
	}
	out, err := b.compose(ctx, "ps", "--status", "running", "--services")
	if err != nil {
		return StateUnknown, vmError("state", ErrorBackend, err)
	}
	if !strings.Contains(out, "windows") {
		return StateStopped, nil
	}
	ready, err := b.rdpReady(ctx)
	if err != nil {
		return StateUnknown, vmError("state", ErrorBackend, err)
	}
	if ready {
		return StateRunning, nil
	}
	return StateStarting, nil
}

func (b *DockerBackend) Stop(ctx context.Context) error {
	if err := b.ensureInstalled(); err != nil {
		return vmError("stop", ErrorConflict, err)
	}
	if _, err := b.compose(ctx, "stop", "-t", "120"); err != nil {
		return vmError("stop", ErrorBackend, err)
	}
	return nil
}

func (b *DockerBackend) Connect(ctx context.Context) (Connection, error) {
	state, err := b.State(ctx)
	if err != nil {
		return Connection{}, err
	}
	if state != StateRunning {
		return Connection{}, vmError("connect", ErrorUnavailable, errors.New("Windows guest is not RDP-ready"))
	}
	return Connection{Address: "127.0.0.1", Port: b.Config.RDPPort}, nil
}

// ConsoleURL is the container's web console, on the loopback interface only.
func (b *DockerBackend) ConsoleURL() (string, error) {
	if err := b.ensureInstalled(); err != nil {
		return "", vmError("console", ErrorConflict, err)
	}
	return "http://127.0.0.1:8006/", nil
}

// Console returns the container's web console address, published on the
// loopback interface by the Compose project.
func (b *DockerBackend) Console(context.Context) (string, error) {
	return b.ConsoleURL()
}

// Remove tears down the managed container, project and stored password. The
// guest disk is deliberately left alone: deleting the user's Windows install
// is a separate, explicitly confirmed act (RemoveData).
func (b *DockerBackend) Remove(ctx context.Context) error {
	if err := b.ensureInstalled(); err != nil {
		return vmError("remove", ErrorConflict, err)
	}
	if _, err := b.compose(ctx, "down"); err != nil {
		return vmError("remove", ErrorBackend, err)
	}
	if err := os.Remove(b.composePath); err != nil && !errors.Is(err, os.ErrNotExist) {
		return vmError("remove", ErrorBackend, err)
	}
	if err := os.Remove(filepath.Join(filepath.Dir(b.composePath), ".guest.env")); err != nil && !errors.Is(err, os.ErrNotExist) {
		return vmError("remove", ErrorBackend, err)
	}
	if b.Secrets != nil && b.secretID != "" {
		if err := b.Secrets.Delete(ctx, b.secretID); err != nil {
			return vmError("remove", ErrorBackend, err)
		}
	}
	return nil
}

// RemoveData deletes the guest disk directory. It only ever removes the
// configured VM data directory itself, after checking that it is the kind of
// path Inua owns: absolute, not a filesystem root, and not a symlink.
func (b *DockerBackend) RemoveData(ctx context.Context) error {
	dir := b.Config.DataDir
	if err := validateOwnedDataDir(dir); err != nil {
		return vmError("remove-data", ErrorInvalidConfig, err)
	}
	if err := rejectPathSymlinks(dir); err != nil {
		return vmError("remove-data", ErrorInvalidConfig, err)
	}
	if _, err := os.Lstat(dir); errors.Is(err, os.ErrNotExist) {
		return nil
	} else if err != nil {
		return vmError("remove-data", ErrorBackend, err)
	}
	return os.RemoveAll(dir)
}

// validateOwnedDataDir rejects anything that is not a plainly-owned VM data
// directory, so a misconfigured path cannot turn RemoveData into a wide rm.
func validateOwnedDataDir(dir string) error {
	clean := filepath.Clean(dir)
	switch {
	case dir == "" || !filepath.IsAbs(clean):
		return errors.New("VM data directory must be absolute")
	case clean == string(filepath.Separator):
		return errors.New("refusing to remove the filesystem root")
	case clean == filepath.Clean(os.Getenv("HOME")) && os.Getenv("HOME") != "":
		return errors.New("refusing to remove the home directory")
	case dir != clean:
		return errors.New("VM data directory must be a clean path")
	}
	return nil
}

func (b *DockerBackend) compose(ctx context.Context, args ...string) (string, error) {
	if b.Runner == nil {
		b.Runner = execCommandRunner{}
	}
	// Pin the project name: Docker Compose otherwise derives it from the
	// directory the file sits in, so any other Compose project whose folder
	// is named "windows" and whose service is "windows" would be treated as
	// this one - and `up -d` would tear its container down.
	argv := []string{"compose", "-p", composeProject(b.Config.Name), "-f", b.composePath}
	argv = append(argv, args...)
	return b.Runner.Run(ctx, "docker", argv...)
}

// composeProject is the Compose project name for a VM, namespaced so it can
// never collide with a user's own Compose files.
func composeProject(name string) string {
	return "inua-vm-" + name
}

// SetInstalled restores the managed Compose location after reading Inua's config.
func (b *DockerBackend) SetInstalled(cfg Config) {
	b.Config = cfg
	if cfg.Name == "" {
		b.composePath = ""
		b.secretID = ""
		return
	}
	dir := filepath.Join(configBase(), "inua", "vm", cfg.Name)
	b.composePath = filepath.Join(dir, dockerComposeFile)
	b.secretID = "inua/windows/" + cfg.Name
}
func (b *DockerBackend) ensureInstalled() error {
	if b.composePath == "" || b.Config.Name == "" {
		return errors.New("VM is not installed by this backend instance")
	}
	if err := rejectPathSymlinks(b.composePath); err != nil {
		return err
	}
	fi, err := os.Stat(b.composePath)
	if err != nil {
		return err
	}
	if !fi.Mode().IsRegular() {
		return errors.New("compose path is not a regular file")
	}
	return nil
}

func (b *DockerBackend) rdpReady(ctx context.Context) (bool, error) {
	if err := ctx.Err(); err != nil {
		return false, err
	}
	conn, err := (&net.Dialer{Timeout: 500 * time.Millisecond}).DialContext(ctx, "tcp", net.JoinHostPort("127.0.0.1", fmt.Sprint(b.Config.RDPPort)))
	if err != nil {
		return false, nil
	}
	_ = conn.Close()
	return true, nil
}

func safeOwnedDir(path string) error {
	if !filepath.IsAbs(path) || filepath.Clean(path) != path || filepath.Clean(path) == string(filepath.Separator) {
		return errors.New("unsafe directory path")
	}
	if err := rejectPathSymlinks(path); err != nil {
		return err
	}
	return os.MkdirAll(path, 0700)
}

func rejectPathSymlinks(path string) error {
	abs, err := filepath.Abs(path)
	if err != nil {
		return err
	}
	vol := filepath.VolumeName(abs)
	cur := vol + string(filepath.Separator)
	for _, part := range strings.Split(strings.TrimPrefix(abs, cur), string(filepath.Separator)) {
		if part == "" {
			continue
		}
		cur = filepath.Join(cur, part)
		fi, err := os.Lstat(cur)
		if errors.Is(err, os.ErrNotExist) {
			continue
		}
		if err != nil {
			return err
		}
		if fi.Mode()&os.ModeSymlink != 0 {
			return fmt.Errorf("symlink path component rejected: %s", cur)
		}
	}
	return nil
}

func writeAtomic(path string, data []byte, mode os.FileMode) error {
	dir := filepath.Dir(path)
	f, err := os.CreateTemp(dir, ".compose-*.tmp")
	if err != nil {
		return err
	}
	name := f.Name()
	defer os.Remove(name)
	if err := f.Chmod(mode); err != nil {
		_ = f.Close()
		return err
	}
	if _, err := f.Write(data); err != nil {
		_ = f.Close()
		return err
	}
	if err := f.Sync(); err != nil {
		_ = f.Close()
		return err
	}
	if err := f.Close(); err != nil {
		return err
	}
	return os.Rename(name, path)
}

func yamlQuote(s string) string {
	return "\"" + strings.NewReplacer("\\", "\\\\", "\"", "\\\"", "\n", "\\n").Replace(s) + "\""
}

func configBase() string {
	if p := os.Getenv("XDG_CONFIG_HOME"); p != "" {
		return p
	}
	home, _ := os.UserHomeDir()
	return filepath.Join(home, ".config")
}

func vmError(op string, kind ErrorKind, err error) error {
	return &Error{Op: op, Kind: kind, Err: err}
}

func newGuestPassword() ([]byte, error) {
	var entropy [32]byte
	if _, err := rand.Read(entropy[:]); err != nil {
		return nil, err
	}
	password := make([]byte, hex.EncodedLen(len(entropy)))
	hex.Encode(password, entropy[:])
	return password, nil
}
