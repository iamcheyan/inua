//go:build !linux

package lobbyservice

import (
	"context"
	"errors"

	"github.com/lyricat/inua/internal/i18n"
)

// Status is how the unit stands: never running where there is no
// systemd.
func Status(context.Context) State { return Stopped }

// Start runs the lobby in a service: only on Linux, with systemd.
func Start(context.Context, Config) error {
	return errors.New(i18n.T("A lobby runs as a service only with systemd."))
}

// Stop ends the service.
func Stop(context.Context) {}
