// Package lobbyservice runs a game lobby (inua-game-lobby) on this
// computer, in a service of its own (a systemd user unit), so its games
// keep running when the Game Lobby window that started it closes. It
// listens on this computer's network, every address of it, or on its
// Tailscale address only; it runs as the user, so the games it hosts may
// have the user's AI play (-ai). No GTK.
package lobbyservice

import (
	"errors"
	"net"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"

	"github.com/lyricat/inua/internal/apps/tailscale"
	"github.com/lyricat/inua/internal/games/gameweb"
)

// Unit is the systemd user unit the lobby runs in.
const Unit = "inua-game-lobby.service"

// LogHint is where the unit's output goes.
const LogHint = "journalctl --user -u " + Unit

// DefaultPort is the port the lobby listens on unless told another.
const DefaultPort = 7340

// Where is where the lobby listens.
type Where string

const (
	Network   Where = "network"   // every address of this computer
	Tailscale Where = "tailscale" // its Tailscale address only
)

// Config is where a lobby run here listens, as the window keeps it.
type Config struct {
	Where Where `json:"where,omitempty"`
	Port  int   `json:"port,omitempty"`
}

// port is the port, DefaultPort unless one is set.
func (c Config) port() string {
	if c.Port <= 0 || c.Port > 65535 {
		return strconv.Itoa(DefaultPort)
	}
	return strconv.Itoa(c.Port)
}

// Listen is the address the lobby listens on.
func (c Config) Listen() (string, error) {
	if c.Where == Tailscale {
		ip, err := tailscale.LocalIP()
		if err != nil {
			return "", err
		}
		return net.JoinHostPort(ip, c.port()), nil
	}
	return ":" + c.port(), nil
}

// Local is the address this computer reaches the lobby at: the loopback
// on the network, the Tailscale address on the tailnet.
func (c Config) Local() (string, error) {
	if c.Where == Tailscale {
		return c.Listen()
	}
	return net.JoinHostPort("127.0.0.1", c.port()), nil
}

// ErrNoNetwork is a computer on no network others could reach it on.
var ErrNoNetwork = errors.New("this computer is on no network")

// Public is the lobby's address as others open it: this computer's
// address on its home network first, or on the tailnet.
func (c Config) Public() (string, error) {
	if c.Where == Tailscale {
		addr, err := c.Listen()
		if err != nil {
			return "", err
		}
		return "http://" + addr, nil
	}
	port, _ := strconv.Atoi(c.port())
	urls := gameweb.URLs(port, "")
	if len(urls) == 0 {
		return "", ErrNoNetwork
	}
	return strings.TrimSuffix(urls[0], "/#"), nil
}

// args are inua-game-lobby's arguments for c: where it listens, its
// address for the links desktops are given (when it has one), and the
// user's AI for the games it hosts.
func (c Config) args() ([]string, error) {
	listen, err := c.Listen()
	if err != nil {
		return nil, err
	}
	args := []string{"-addr", listen}
	if public, err := c.Public(); err == nil {
		args = append(args, "-public-url", public)
	}
	return append(args, "-ai"), nil
}

// program is inua-game-lobby: beside this program, else on the PATH.
func program() (string, error) {
	if exe, err := os.Executable(); err == nil {
		p := filepath.Join(filepath.Dir(exe), "inua-game-lobby")
		if _, err := os.Stat(p); err == nil {
			return p, nil
		}
	}
	return exec.LookPath("inua-game-lobby")
}

// State is how the unit stands.
type State uint8

const (
	Stopped  State = iota
	Starting       // starting, not listening yet
	Running
	Failed // it stopped with an error, or keeps doing so and is started again
)

func (s State) String() string {
	return [...]string{"stopped", "starting", "running", "failed"}[s]
}
