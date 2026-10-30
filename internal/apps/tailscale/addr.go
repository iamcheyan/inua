package tailscale

import (
	"errors"
	"net"
)

// tailnetRange is Tailscale's range of addresses (100.64.0.0/10).
var tailnetRange = &net.IPNet{IP: net.IPv4(100, 64, 0, 0), Mask: net.CIDRMask(10, 32)}

// ErrNoAddress is a computer with no Tailscale address.
var ErrNoAddress = errors.New("no Tailscale address: is Tailscale up?")

// LocalIP is this computer's Tailscale IPv4 address, from its network
// interfaces: what a server listens on to be reached over the tailnet
// only (the Web Terminal, the game lobby).
func LocalIP() (string, error) {
	ifaces, err := net.Interfaces()
	if err != nil {
		return "", err
	}
	for _, iface := range ifaces {
		if iface.Flags&net.FlagUp == 0 {
			continue
		}
		addrs, _ := iface.Addrs()
		for _, a := range addrs {
			if n, ok := a.(*net.IPNet); ok && n.IP.To4() != nil && tailnetRange.Contains(n.IP) {
				return n.IP.String(), nil
			}
		}
	}
	return "", ErrNoAddress
}
