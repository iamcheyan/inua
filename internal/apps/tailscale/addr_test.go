package tailscale

import (
	"net"
	"testing"
)

// A Tailscale address found is in Tailscale's range.
func TestLocalIP(t *testing.T) {
	if ip, err := LocalIP(); err == nil && !tailnetRange.Contains(net.ParseIP(ip)) {
		t.Errorf("Tailscale address %s outside 100.64.0.0/10", ip)
	}
}
