package webterm

import (
	"testing"

	"github.com/lyricat/inua/internal/term/settings"
)

// On this computer only, the Web Terminal listens on the loopback
// address at its port.
func TestAddr(t *testing.T) {
	addr, err := Addr(settings.Web{Port: 7681})
	if err != nil || addr != "127.0.0.1:7681" {
		t.Errorf("Addr = %q, %v", addr, err)
	}
}
