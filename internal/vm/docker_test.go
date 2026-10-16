package vm

import (
	"context"
	"gopkg.in/yaml.v3"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"
)

// fakeRunner stands in for Docker so the lifecycle runs without a daemon.
type fakeRunner struct {
	calls []string
	fail  map[string]error
}

func (f *fakeRunner) Run(_ context.Context, name string, args ...string) (string, error) {
	call := name + " " + strings.Join(args, " ")
	f.calls = append(f.calls, call)
	if err, ok := f.fail[call]; ok {
		return "", err
	}
	return "", nil
}

type fakeSecrets struct{ items map[string][]byte }

func (f *fakeSecrets) Store(_ context.Context, id string, v []byte) error {
	f.items[id] = append([]byte(nil), v...)
	return nil
}
func (f *fakeSecrets) Load(_ context.Context, id string) ([]byte, error) {
	v, ok := f.items[id]
	if !ok {
		return nil, os.ErrNotExist
	}
	return v, nil
}
func (f *fakeSecrets) Delete(_ context.Context, id string) error {
	delete(f.items, id)
	return nil
}

// newTestBackend puts the backend's configuration under a temporary root so
// nothing touches the user's real XDG directories.
func newTestBackend(t *testing.T) (*DockerBackend, Config, *fakeRunner, *fakeSecrets) {
	t.Helper()
	root := t.TempDir()
	t.Setenv("XDG_CONFIG_HOME", filepath.Join(root, "config"))
	t.Setenv("XDG_DATA_HOME", filepath.Join(root, "data"))
	cfg := DefaultConfig()
	cfg.DataDir = filepath.Join(root, "data", "inua", "vm", "windows")
	if err := os.MkdirAll(cfg.DataDir, 0700); err != nil {
		t.Fatal(err)
	}
	runner := &fakeRunner{fail: map[string]error{}}
	secrets := &fakeSecrets{items: map[string][]byte{}}
	b := NewDockerBackend(runner)
	b.Secrets = secrets
	return b, cfg, runner, secrets
}

func TestInstallWritesComposeAndEnvWithoutLeakingSecret(t *testing.T) {
	b, cfg, _, secrets := newTestBackend(t)
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	if err := b.Install(ctx, cfg); err != nil {
		t.Fatalf("install: %v", err)
	}
	dir := filepath.Join(os.Getenv("XDG_CONFIG_HOME"), "inua", "vm", cfg.Name)
	compose, err := os.ReadFile(filepath.Join(dir, dockerComposeFile))
	if err != nil {
		t.Fatalf("compose: %v", err)
	}
	envPath := filepath.Join(dir, ".guest.env")
	info, err := os.Stat(envPath)
	if err != nil {
		t.Fatalf("env file: %v", err)
	}
	if perm := info.Mode().Perm(); perm != 0600 {
		t.Errorf("env file mode = %o, want 0600", perm)
	}
	password, err := secrets.Load(ctx, "inua/windows/"+cfg.Name)
	if err != nil {
		t.Fatalf("stored password: %v", err)
	}
	if len(password) < 32 {
		t.Errorf("generated password is too short: %d", len(password))
	}
	// The password belongs in the 0600 env file alone, never in the project.
	if strings.Contains(string(compose), string(password)) {
		t.Error("the guest password leaked into the Compose project")
	}
	// Ports must stay on the loopback interface.
	if !strings.Contains(string(compose), "127.0.0.1:") {
		t.Error("Compose does not publish ports on the loopback interface")
	}
	if strings.Contains(string(compose), "\n      - \"8006:8006\"") {
		t.Error("the web console is published on every interface")
	}
}

func TestInstallRefusesToOverwriteAnExistingProject(t *testing.T) {
	b, cfg, _, _ := newTestBackend(t)
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := b.Install(ctx, cfg); err != nil {
		t.Fatalf("first install: %v", err)
	}
	if err := b.Install(ctx, cfg); err == nil {
		t.Fatal("a second install replaced an existing project")
	}
}

func TestInstallRefusesWithoutSecretStore(t *testing.T) {
	b, cfg, _, _ := newTestBackend(t)
	b.Secrets = nil
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := b.Install(ctx, cfg); err == nil {
		t.Fatal("install succeeded without a secure password store")
	}
	if _, err := os.Stat(filepath.Join(os.Getenv("XDG_CONFIG_HOME"), "inua", "vm", cfg.Name, dockerComposeFile)); !os.IsNotExist(err) {
		t.Error("a refused install left a Compose project behind")
	}
}

func TestRemoveDeletesProjectEnvAndSecret(t *testing.T) {
	b, cfg, _, secrets := newTestBackend(t)
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := b.Install(ctx, cfg); err != nil {
		t.Fatalf("install: %v", err)
	}
	if err := b.Remove(ctx); err != nil {
		t.Fatalf("remove: %v", err)
	}
	dir := filepath.Join(os.Getenv("XDG_CONFIG_HOME"), "inua", "vm", cfg.Name)
	for _, name := range []string{dockerComposeFile, ".guest.env"} {
		if _, err := os.Stat(filepath.Join(dir, name)); !os.IsNotExist(err) {
			t.Errorf("%s survived removal", name)
		}
	}
	if _, err := secrets.Load(ctx, "inua/windows/"+cfg.Name); !os.IsNotExist(err) {
		t.Error("the stored password survived removal")
	}
}

func TestConsoleURLIsLoopbackOnly(t *testing.T) {
	b, cfg, _, _ := newTestBackend(t)
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := b.Install(ctx, cfg); err != nil {
		t.Fatalf("install: %v", err)
	}
	url, err := b.ConsoleURL()
	if err != nil {
		t.Fatalf("console url: %v", err)
	}
	if !strings.HasPrefix(url, "http://127.0.0.1:") {
		t.Errorf("console url is not loopback: %q", url)
	}
}

func TestSetInstalledRestoresManagedLocations(t *testing.T) {
	b, cfg, _, _ := newTestBackend(t)
	b.SetInstalled(cfg)
	if b.composePath != filepath.Join(os.Getenv("XDG_CONFIG_HOME"), "inua", "vm", cfg.Name, dockerComposeFile) {
		t.Errorf("compose path not restored: %q", b.composePath)
	}
	if b.secretID != "inua/windows/"+cfg.Name {
		t.Errorf("secret id not restored: %q", b.secretID)
	}
	if err := b.ensureInstalled(); err == nil {
		t.Error("ensureInstalled accepted a project that was never written")
	}
}

// The Compose project must be valid YAML: a quoted volume source followed by
// a bare ": /storage" made Docker refuse the project outright.
func TestInstallWritesParsableCompose(t *testing.T) {
	b, cfg, _, _ := newTestBackend(t)
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := b.Install(ctx, cfg); err != nil {
		t.Fatalf("install: %v", err)
	}
	data, err := os.ReadFile(b.composePath)
	if err != nil {
		t.Fatal(err)
	}
	var doc map[string]any
	if err := yaml.Unmarshal(data, &doc); err != nil {
		t.Fatalf("compose is not valid YAML: %v\n%s", err, data)
	}
	services, _ := doc["services"].(map[string]any)
	if services == nil {
		t.Fatalf("compose has no services: %s", data)
	}
	if _, ok := services["windows"]; !ok {
		t.Fatalf("compose has no windows service: %s", data)
	}
}
