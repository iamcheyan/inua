package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"

	"github.com/lyricat/inua/internal/vm"
)

type vmStatus struct {
	Platform    vm.Platform `json:"platform"`
	Host        vm.Host     `json:"host"`
	Recommended vm.Profile  `json:"recommended_profile"`
	Config      vm.Config   `json:"config"`
	ConfigPath  string      `json:"config_path"`
	ConfigValid bool        `json:"config_valid"`
	ConfigError string      `json:"config_error,omitempty"`
}

func cmdVM(args []string) error {
	if len(args) == 0 {
		usage()
	}
	switch args[0] {
	case "doctor":
		if len(args) != 1 {
			usage()
		}
		return vmDoctor(false)
	case "status":
		fs := flag.NewFlagSet("vm status", flag.ContinueOnError)
		jsonOutput := fs.Bool("json", false, "output JSON")
		if err := fs.Parse(args[1:]); err != nil {
			return err
		}
		if fs.NArg() != 0 {
			usage()
		}
		return vmDoctor(*jsonOutput)
	default:
		usage()
	}
	return nil
}

func vmDoctor(asJSON bool) error {
	platform := vm.DetectPlatform("/", vm.PlatformProbes{})
	host := vm.DetectHost("/")
	cfg := vm.DefaultConfig()
	path := vm.ConfigPath()
	if b, err := os.ReadFile(path); err == nil {
		if err := json.Unmarshal(b, &cfg); err != nil {
			return fmt.Errorf("read VM config %s: %w", path, err)
		}
	}
	configErr := cfg.Validate()
	status := vmStatus{Platform: platform, Host: host, Recommended: vm.RecommendProfile(host), Config: cfg, ConfigPath: path, ConfigValid: configErr == nil}
	if configErr != nil {
		status.ConfigError = configErr.Error()
	}
	if asJSON {
		enc := json.NewEncoder(os.Stdout)
		enc.SetIndent("", "  ")
		return enc.Encode(status)
	}
	fmt.Printf("Windows VM host: %s\n", platform.OS)
	if platform.Distribution != "" {
		fmt.Printf("Distribution: %s\n", platform.Distribution)
	}
	fmt.Printf("Supported: %t\n", platform.Supported)
	for _, item := range platform.Doctor {
		state := "FAIL"
		if item.Available {
			state = "OK"
		}
		fmt.Printf("%s: %s (%s)\n", state, item.Name, item.Detail)
	}
	fmt.Printf("Recommended resources: %d MiB RAM, %d CPUs, %d GiB disk\n", status.Recommended.MemoryMiB, status.Recommended.CPUs, status.Recommended.DiskGiB)
	fmt.Printf("VM config: %s\n", path)
	if status.ConfigValid {
		fmt.Printf("Config valid: %s, %d MiB RAM, %d CPUs, %d GiB disk\n", cfg.Name, cfg.MemoryMiB, cfg.CPUs, cfg.DiskGiB)
	} else {
		fmt.Printf("Config invalid: %s\n", status.ConfigError)
	}
	return nil
}
