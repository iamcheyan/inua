package vm

import (
	"errors"
	"os"
	"path/filepath"
	"testing"
)

func TestConfigValidate(t *testing.T) {
	cfg := DefaultConfig()
	if err := cfg.Validate(); err != nil {
		t.Fatalf("default config invalid: %v", err)
	}
	for name, mutate := range map[string]func(*Config){
		"relative data":  func(c *Config) { c.DataDir = "vm" },
		"root data":      func(c *Config) { c.DataDir = string(filepath.Separator) },
		"traversal name": func(c *Config) { c.Name = "../vm" },
		"invalid port":   func(c *Config) { c.RDPPort = 65536 },
		"low memory":     func(c *Config) { c.MemoryMiB = MinMemoryMiB - 1 },
	} {
		t.Run(name, func(t *testing.T) {
			bad := cfg
			mutate(&bad)
			err := bad.Validate()
			var typed *Error
			if !errors.As(err, &typed) || typed.Kind != ErrorInvalidConfig {
				t.Fatalf("got %v, want invalid config error", err)
			}
		})
	}
}

func TestRecommendProfile(t *testing.T) {
	p := RecommendProfile(Host{MemoryBytes: 8 << 30, CPUs: 8, FreeDiskBytes: 200 << 30})
	if p.MemoryMiB != 4096 || p.CPUs != 6 || p.DiskGiB != 64 {
		t.Fatalf("unexpected profile: %+v", p)
	}
	p = RecommendProfile(Host{})
	if p.MemoryMiB < MinMemoryMiB || p.CPUs < MinCPUs || p.DiskGiB < MinDiskGiB {
		t.Fatalf("profile below minimum: %+v", p)
	}
	// The caps keep the guest modest on a large host.
	p = RecommendProfile(Host{MemoryBytes: 1 << 50, CPUs: 128, FreeDiskBytes: 1 << 50})
	if p.MemoryMiB != 16384 || p.CPUs != 8 || p.DiskGiB != 128 {
		t.Fatalf("profile exceeds caps: %+v", p)
	}
}
func TestDetectHostRoot(t *testing.T) {
	root := t.TempDir()
	if err := os.MkdirAll(filepath.Join(root, "proc"), 0755); err != nil {
		t.Fatal(err)
	}
	if err := os.MkdirAll(filepath.Join(root, "var"), 0755); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(filepath.Join(root, "proc", "meminfo"), []byte("MemTotal:       8192000 kB\n"), 0600); err != nil {
		t.Fatal(err)
	}
	h := DetectHost(root)
	if h.MemoryBytes != 8192000*1024 {
		t.Fatalf("memory = %d", h.MemoryBytes)
	}
	if h.CPUs < 1 || h.OS == "" {
		t.Fatalf("incomplete host: %+v", h)
	}
}
