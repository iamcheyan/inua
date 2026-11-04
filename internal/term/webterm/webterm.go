// Package webterm is the Web Terminal: inua-termd serve (internal/term/web)
// run as a service of its own (a systemd user unit on Linux, a launchd
// agent on macOS), turned on in inua-term's settings and started again at
// login while it is on, and its link. It holds the page's token, kept in
// the keyring. No GTK, and none of the page's files: the shell starts it
// too.
package webterm

import (
	"context"
	"fmt"
	"net"
	"net/url"
	"strconv"
	"time"

	"github.com/lyricat/inua/internal/apps/tailscale"
	"github.com/lyricat/inua/internal/term/host"
	"github.com/lyricat/inua/internal/term/settings"
)

// Addr is where the Web Terminal listens: this computer, or its Tailscale
// address.
func Addr(w settings.Web) (string, error) {
	host := "127.0.0.1"
	if w.Tailscale {
		ip, err := tailscale.LocalIP()
		if err != nil {
			return "", err
		}
		host = ip
	}
	return net.JoinHostPort(host, strconv.Itoa(w.Port)), nil
}

// Link is the page's address with its token: what a phone opens.
func Link(ctx context.Context, w settings.Web) (string, error) {
	addr, err := Addr(w)
	if err != nil {
		return "", err
	}
	token, err := Token(ctx, false)
	if err != nil {
		return "", err
	}
	return "http://" + addr + "/?t=" + url.QueryEscape(token), nil
}

// Start runs inua-termd serve in its service, as w says, and waits for it
// to listen. One running already is stopped first: its address may have
// changed.
func Start(ctx context.Context, w settings.Web) error {
	addr, err := Addr(w)
	if err != nil {
		return err
	}
	// The token first: the service has no one to ask for the keyring.
	if _, err := Token(ctx, false); err != nil {
		return err
	}
	self, err := host.Program("inua-termd")
	if err != nil {
		return err
	}
	Stop(ctx)
	if err := launch(ctx, self, addr); err != nil {
		return err
	}
	for {
		if c, err := net.DialTimeout("tcp", addr, time.Second); err == nil {
			c.Close()
			return nil
		}
		if !Running(ctx) {
			return fmt.Errorf("inua-termd serve stopped: %s says why", logHint)
		}
		select {
		case <-ctx.Done():
			return ctx.Err()
		case <-time.After(200 * time.Millisecond):
		}
	}
}

// AtLogin starts the Web Terminal when it was left on: the shell calls it
// once the session is there.
func AtLogin(ctx context.Context) error {
	set, _, err := settings.Load(settings.Path())
	if err != nil || !set.Web.On || Running(ctx) {
		return err
	}
	return Start(ctx, set.Web)
}
