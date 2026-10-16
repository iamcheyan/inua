package vm

import (
	"bufio"
	"errors"
	"net"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
	"time"
)

// Platform describes host facilities needed to run and connect to a Windows VM.
type Platform struct {
	OS            string
	Distribution  string
	Supported     bool
	KVM           DeviceCapability
	DockerSocket  DeviceCapability
	ComposeV2     Capability
	FreeRDP       Capability
	BrowserOpener Capability
	Disk          Capability
	Filesystem    string
	TUN           DeviceCapability
	Doctor        []DoctorItem
}

type Capability struct {
	Available bool
	Detail    string
}
type DeviceCapability struct {
	Available  bool
	Accessible bool
	Path       string
	Detail     string
}
type DoctorItem struct {
	Name      string
	Available bool
	Detail    string
}

type PlatformProbes struct {
	Executable    func(string) bool
	Accessible    func(string) bool
	Filesystem    func(string) string
	Exists        func(string) bool
	CommandOutput func(string, ...string) (string, error)
}

// DetectPlatform inspects host support without modifying system state. Root maps absolute
// paths into a fixture root; probe functions make host-dependent checks deterministic in tests.
func DetectPlatform(root string, probes PlatformProbes) Platform {
	if root == "" {
		root = "/"
	}
	if probes.Exists == nil {
		probes.Exists = func(p string) bool { _, err := os.Stat(p); return err == nil }
	}
	if probes.Accessible == nil {
		probes.Accessible = func(p string) bool {
			fi, err := os.Stat(p)
			if err != nil {
				return false
			}
			if fi.Mode()&os.ModeSocket != 0 {
				// A Unix socket cannot be opened like a file: connecting is
				// what checks the permission bits.
				c, err := net.DialTimeout("unix", p, 250*time.Millisecond)
				if err != nil {
					return false
				}
				_ = c.Close()
				return true
			}
			f, err := os.OpenFile(p, os.O_RDWR, 0)
			if err != nil {
				return false
			}
			_ = f.Close()
			return true
		}
	}
	if probes.Executable == nil {
		probes.Executable = func(name string) bool { _, err := exec.LookPath(name); return err == nil }
	}
	if probes.CommandOutput == nil {
		probes.CommandOutput = func(name string, args ...string) (string, error) {
			out, err := exec.Command(name, args...).CombinedOutput()
			return string(out), err
		}
	}
	mapPath := func(p string) string {
		return filepath.Join(root, strings.TrimPrefix(filepath.Clean(p), string(filepath.Separator)))
	}
	osName, distro := hostOS(root)
	p := Platform{OS: osName, Distribution: distro, Supported: osName == "linux" && supportedDistribution(distro)}
	kvm := mapPath("/dev/kvm")
	p.KVM = DeviceCapability{Path: kvm, Available: probes.Exists(kvm), Accessible: probes.Accessible(kvm)}
	if !p.KVM.Available {
		p.KVM.Detail = "KVM device /dev/kvm is unavailable"
	} else if !p.KVM.Accessible {
		p.KVM.Detail = "current user cannot access /dev/kvm"
	} else {
		p.KVM.Detail = "KVM device is accessible"
	}
	socket := mapPath("/var/run/docker.sock")
	p.DockerSocket = DeviceCapability{Path: socket, Available: probes.Exists(socket), Accessible: probes.Accessible(socket)}
	if !p.DockerSocket.Available {
		p.DockerSocket.Detail = "Docker socket is unavailable"
	} else if !p.DockerSocket.Accessible {
		p.DockerSocket.Detail = "current user cannot access Docker socket"
	} else {
		p.DockerSocket.Detail = "Docker socket is accessible"
	}
	composeVersion, composeErr := composeVersion(probes)
	compose := composeErr == nil && composeVersion != ""
	p.ComposeV2 = Capability{Available: compose, Detail: "Docker Compose v2 plugin unavailable"}
	if compose {
		p.ComposeV2.Detail = "Docker Compose " + composeVersion + " available"
	}
	p.FreeRDP = executableCapability(probes, []string{"xfreerdp", "xfreerdp3"}, "FreeRDP unavailable")
	p.BrowserOpener = executableCapability(probes, []string{"xdg-open"}, "browser opener xdg-open unavailable")
	p.TUN = DeviceCapability{Path: mapPath("/dev/net/tun"), Available: probes.Exists(mapPath("/dev/net/tun")), Accessible: probes.Accessible(mapPath("/dev/net/tun"))}
	if !p.TUN.Available {
		p.TUN.Detail = "TUN device is unavailable"
	} else if !p.TUN.Accessible {
		p.TUN.Detail = "current user cannot access TUN device"
	} else {
		p.TUN.Detail = "TUN device is accessible"
	}
	p.Filesystem = "unknown"
	if probes.Filesystem != nil {
		p.Filesystem = probes.Filesystem(root)
	} else {
		p.Filesystem = detectFilesystem(root)
	}
	p.Disk = Capability{Available: p.Filesystem != "" && p.Filesystem != "unknown", Detail: "filesystem: " + p.Filesystem}
	p.Doctor = []DoctorItem{{"Operating system", p.Supported, distroDetail(osName, distro)}, {"KVM", p.KVM.Available && p.KVM.Accessible, p.KVM.Detail}, {"Docker socket", p.DockerSocket.Available && p.DockerSocket.Accessible, p.DockerSocket.Detail}, {"Docker Compose v2", p.ComposeV2.Available, p.ComposeV2.Detail}, {"FreeRDP", p.FreeRDP.Available, p.FreeRDP.Detail}, {"Browser opener", p.BrowserOpener.Available, p.BrowserOpener.Detail}, {"Disk/filesystem", p.Disk.Available, p.Disk.Detail}, {"TUN", p.TUN.Available && p.TUN.Accessible, p.TUN.Detail}}
	return p
}

// composeVersion reads the Compose v2 plugin's version. Docker prints it bare
// ("2.39.1") or with a leading "v", depending on the release.
func composeVersion(p PlatformProbes) (string, error) {
	out, err := p.CommandOutput("docker", "compose", "version", "--short")
	if err != nil {
		return "", err
	}
	v := strings.TrimPrefix(strings.TrimSpace(out), "v")
	if v == "" || strings.HasPrefix(v, "1.") {
		return "", errors.New("Docker Compose v2 is not available")
	}
	return v, nil
}

// detectFilesystem names the filesystem holding the user's home, where the VM
// disk lives; "unknown" when /proc/mounts cannot be read.
func detectFilesystem(root string) string {
	if root != "/" {
		return "unknown"
	}
	home, err := os.UserHomeDir()
	if err != nil {
		return "unknown"
	}
	data, err := os.ReadFile("/proc/mounts")
	if err != nil {
		return "unknown"
	}
	best, fs := "", ""
	for _, line := range strings.Split(string(data), "\n") {
		fields := strings.Fields(line)
		if len(fields) < 3 {
			continue
		}
		mount := strings.ReplaceAll(fields[1], `\040`, " ")
		if mount == "/" || home == mount || strings.HasPrefix(home, mount+"/") {
			if len(mount) > len(best) {
				best, fs = mount, fields[2]
			}
		}
	}
	if fs == "" {
		return "unknown"
	}
	return fs
}

func executableCapability(p PlatformProbes, names []string, missing string) Capability {
	for _, name := range names {
		if p.Executable(name) {
			return Capability{true, name + " available"}
		}
	}
	return Capability{false, missing}
}
func hostOS(root string) (string, string) {
	if runtime.GOOS != "linux" {
		return runtime.GOOS, ""
	}
	f, err := os.Open(filepath.Join(root, "etc", "os-release"))
	if err != nil {
		return "linux", ""
	}
	defer f.Close()
	values := map[string]string{}
	s := bufio.NewScanner(f)
	for s.Scan() {
		line := s.Text()
		k, v, ok := strings.Cut(line, "=")
		if ok {
			values[k] = strings.Trim(strings.TrimSpace(v), "\"'")
		}
	}
	id := strings.ToLower(values["ID"])
	if id == "" {
		return "linux", ""
	}
	return "linux", id
}
func supportedDistribution(d string) bool { return d == "nixos" || d == "ubuntu" || d == "debian" }
func distroDetail(osName, distro string) string {
	if osName != "linux" {
		return "Windows VM host support requires Linux"
	}
	if !supportedDistribution(distro) {
		return "unsupported Linux distribution: " + distro
	}
	return distro + " supported"
}

type PackagePlan struct {
	Distribution             string
	PackageManager           string
	Packages                 []string
	RequiresUserConfirmation bool
	Confirmation             string
}

// PlanPackages returns recommendations only; it never runs a package manager or changes groups.
func PlanPackages(distribution string) PackagePlan {
	d := strings.ToLower(distribution)
	p := PackagePlan{Distribution: d, RequiresUserConfirmation: true, Confirmation: "Review and confirm before installing packages or changing system configuration."}
	switch d {
	case "nixos":
		p.PackageManager = "nix"
		p.Packages = []string{"docker", "freerdp", "xdg-utils", "qemu_kvm"}
	case "ubuntu", "debian":
		p.PackageManager = "apt"
		p.Packages = []string{"docker.io", "docker-compose-v2", "freerdp3-x11", "xdg-utils", "qemu-system-x86", "qemu-utils"}
	}
	return p
}
