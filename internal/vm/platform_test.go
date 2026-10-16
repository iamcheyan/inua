package vm

import (
	"errors"
	"net"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestDetectPlatformWithInjectedProbes(t *testing.T) {
	root := t.TempDir()
	if err := os.MkdirAll(filepath.Join(root, "etc"), 0755); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(filepath.Join(root, "etc", "os-release"), []byte("ID=ubuntu\n"), 0600); err != nil {
		t.Fatal(err)
	}
	for _, p := range []string{"dev/kvm", "var/run/docker.sock", "dev/net/tun"} {
		path := filepath.Join(root, p)
		if err := os.MkdirAll(filepath.Dir(path), 0755); err != nil {
			t.Fatal(err)
		}
		if err := os.WriteFile(path, nil, 0600); err != nil {
			t.Fatal(err)
		}
	}
	platform := DetectPlatform(root, PlatformProbes{Exists: func(string) bool { return true }, Accessible: func(string) bool { return true }, CommandOutput: func(string, ...string) (string, error) { return "v2.29.1", nil }, Executable: func(n string) bool { return n == "xfreerdp3" || n == "xdg-open" }, Filesystem: func(string) string { return "ext4" }})
	if !platform.Supported || platform.Distribution != "ubuntu" || !platform.KVM.Accessible || !platform.DockerSocket.Accessible || !platform.ComposeV2.Available || !platform.FreeRDP.Available || !platform.BrowserOpener.Available || !platform.Disk.Available || !platform.TUN.Available {
		t.Fatalf("incomplete platform detection: %+v", platform)
	}
	if len(platform.Doctor) != 8 {
		t.Fatalf("doctor items = %d", len(platform.Doctor))
	}
}

func TestPlanPackagesRequiresConfirmation(t *testing.T) {
	for distro, manager := range map[string]string{"nixos": "nix", "ubuntu": "apt", "debian": "apt"} {
		plan := PlanPackages(distro)
		if plan.PackageManager != manager || len(plan.Packages) == 0 || !plan.RequiresUserConfirmation || plan.Confirmation == "" {
			t.Errorf("invalid plan for %s: %+v", distro, plan)
		}
	}
	if p := PlanPackages("arch"); p.PackageManager != "" || len(p.Packages) != 0 {
		t.Errorf("unexpected unsupported plan: %+v", p)
	}
}

func TestDetectPlatformChecksComposeV2Output(t *testing.T) {
	for _, tc := range []struct {
		output string
		err    error
		want   bool
	}{{"v2.29.1", nil, true}, {"v1.29.2", nil, false}, {"", errors.New("missing plugin"), false}} {
		platform := DetectPlatform(t.TempDir(), PlatformProbes{CommandOutput: func(name string, args ...string) (string, error) {
			if name != "docker" || strings.Join(args, " ") != "compose version --short" {
				t.Errorf("unexpected command: %s %v", name, args)
			}
			return tc.output, tc.err
		}})
		if platform.ComposeV2.Available != tc.want {
			t.Errorf("Compose output %q, error %v: %+v", tc.output, tc.err, platform.ComposeV2)
		}
	}
}

// A Docker socket cannot be opened like a file; accessibility must come from
// connecting to it, or every user would be told they lack access.
func TestDetectPlatformConnectsToDockerSocket(t *testing.T) {
	root := t.TempDir()
	if err := os.MkdirAll(filepath.Join(root, "var", "run"), 0755); err != nil {
		t.Fatal(err)
	}
	if err := os.MkdirAll(filepath.Join(root, "dev"), 0755); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(filepath.Join(root, "dev", "kvm"), nil, 0600); err != nil {
		t.Fatal(err)
	}
	ln, err := net.Listen("unix", filepath.Join(root, "var", "run", "docker.sock"))
	if err != nil {
		t.Fatal(err)
	}
	defer ln.Close()
	go func() {
		for {
			c, err := ln.Accept()
			if err != nil {
				return
			}
			_ = c.Close()
		}
	}()
	p := DetectPlatform(root, PlatformProbes{})
	if !p.DockerSocket.Accessible {
		t.Fatalf("a listening Unix socket should be accessible: %+v", p.DockerSocket)
	}
}
