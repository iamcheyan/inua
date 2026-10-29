package appmenu

// Client is the menu of whatever application has focus: the accessibility
// tree when the toolkit exports one, the Canonical registrar otherwise.

import (
	"fmt"
)

// Client reads menus from both sources and activates what it returns.
type Client struct {
	Registrar *Registrar
	A11y      *A11y
}

// NewClient returns a client over the given registrar, and over the
// accessibility bus when a11y is non-nil.
func NewClient(registrar *Registrar, a11y *A11y) *Client {
	return &Client{Registrar: registrar, A11y: a11y}
}

// Menu returns the focused process's menu, or nil when it has none.
func (c *Client) Menu(pid int) ([]Entry, error) {
	if c == nil || pid <= 0 {
		return nil, nil
	}
	if c.A11y != nil {
		entries, err := c.A11y.Menu(pid)
		if err == nil && len(entries) > 0 {
			return entries, nil
		}
	}
	if c.Registrar != nil {
		if reg, ok := c.Registrar.ForPID(pid); ok {
			return c.Registrar.Menu(reg)
		}
	}
	return nil, nil
}

// Activate invokes the entry's action on the application that owns it.
func (c *Client) Activate(entry Entry) error {
	switch entry.Action.Kind {
	case ActionA11y:
		if c.A11y == nil {
			return fmt.Errorf("appmenu: no accessibility bus")
		}
		return c.A11y.Activate(entry)
	case ActionDbusmenu:
		if c.Registrar == nil {
			return fmt.Errorf("appmenu: no registrar")
		}
		reg := Registration{Service: entry.Action.Bus, Path: entry.Action.Path}
		return c.Registrar.Activate(reg, entry.Action.Index)
	default:
		return nil
	}
}
