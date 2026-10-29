package appmenu

import (
	"context"
	"fmt"
	"strings"
	"time"

	"github.com/godbus/dbus/v5"

	"github.com/lyricat/inua/internal/dbusmenu"
)

// Client reads the focused application's menu: the Canonical registrar first,
// then inua's own published menu, then the accessibility tree.
type Client struct {
	Registrar *Registrar
	A11y      *A11y
}

func NewClient(r *Registrar, a *A11y) *Client { return &Client{Registrar: r, A11y: a} }

// Menu returns the focused process's menu, or nil when it has none.
func (c *Client) Menu(pid int) ([]Entry, error) {
	if pid <= 0 {
		return nil, nil
	}
	// The registrar is the de-facto protocol: an application that registered a
	// window means its menu is the one to show.
	if c.Registrar != nil {
		if r, ok := c.Registrar.ForPID(pid); ok {
			return c.Registrar.Menu(r)
		}
	}
	if e, ok, err := c.nativeWaylandMenu(pid); ok || err != nil {
		return e, err
	}
	// AT-SPI last: plain GTK4 apps answer it with a skeleton (a menubar whose
	// items have no labels), which must not shadow a real menu nor put blank
	// buttons in the bar.
	if c.A11y != nil {
		if e, err := c.A11y.Menu(pid); err == nil && labelled(e) {
			return e, nil
		}
	}
	return nil, nil
}

// labelled reports whether the menu says anything: at least one top-level item
// with text. A tree of unnamed items is a toolkit skeleton, not a menu.
func labelled(entries []Entry) bool {
	for _, e := range entries {
		if strings.TrimSpace(e.Label) != "" {
			return true
		}
	}
	return false
}

// nativeWaylandMenu finds the menu an inua application published for its
// window, by the well-known name's owning process.
func (c *Client) nativeWaylandMenu(pid int) ([]Entry, bool, error) {
	conn, err := dbus.ConnectSessionBus()
	if err != nil {
		return nil, false, err
	}
	defer conn.Close()
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()
	var names []string
	if err = conn.BusObject().CallWithContext(ctx, "org.freedesktop.DBus.ListNames", 0).Store(&names); err != nil {
		return nil, false, err
	}
	var found []string
	for _, name := range names {
		if !strings.HasPrefix(name, dbusmenu.NamePrefix) {
			continue
		}
		var owner uint32
		if conn.BusObject().CallWithContext(ctx, "org.freedesktop.DBus.GetConnectionUnixProcessID", 0, name).Store(&owner) == nil && int(owner) == pid {
			found = append(found, name)
		}
	}
	// One window per process: with more, the shell has no way to tell which
	// window's menu belongs to the focused one, so it shows none rather than
	// the wrong one's commands.
	if len(found) != 1 {
		return nil, len(found) > 1, nil
	}
	r := Registration{PID: uint32(pid), Service: found[0], Path: dbusmenu.Path}
	entries, err := c.readMenu(conn, r)
	markNative(entries)
	return entries, true, err
}

func (c *Client) readMenu(conn *dbus.Conn, r Registration) ([]Entry, error) {
	obj := conn.Object(r.Service, r.Path)
	obj.Call("com.canonical.dbusmenu.AboutToShow", 0, int32(0))
	call := obj.Call("com.canonical.dbusmenu.GetLayout", 0, int32(0), int32(-1), []string{})
	if call.Err != nil {
		return nil, call.Err
	}
	if len(call.Body) != 2 {
		return nil, fmt.Errorf("appmenu: GetLayout returned %d values", len(call.Body))
	}
	root, ok := call.Body[1].([]any)
	if !ok {
		return nil, fmt.Errorf("appmenu: malformed layout type %T", call.Body[1])
	}
	count := 0
	n, ok := decode(root, 0, &count)
	if !ok {
		return nil, fmt.Errorf("appmenu: malformed or oversized layout")
	}
	setDbusmenuAction(n.Children, r)
	return n.Children, nil
}

func markNative(entries []Entry) {
	for i := range entries {
		if len(entries[i].Children) > 0 {
			markNative(entries[i].Children)
			continue
		}
		entries[i].Action.NativeWayland = true
	}
}

// Activate invokes the entry's action on the application that owns it.
func (c *Client) Activate(e Entry) error {
	switch e.Action.Kind {
	case ActionA11y:
		if c.A11y == nil {
			return fmt.Errorf("appmenu: no accessibility bus")
		}
		return c.A11y.Activate(e)
	case ActionDbusmenu:
		r := Registration{Service: e.Action.Bus, Path: e.Action.Path}
		if e.Action.NativeWayland {
			// inua's own menu lives on its own connection; the shell's
			// registrar connection is not the one that serves it.
			conn, err := dbus.ConnectSessionBus()
			if err != nil {
				return err
			}
			defer conn.Close()
			return conn.Object(r.Service, r.Path).Call("com.canonical.dbusmenu.Event", 0,
				e.Action.Index, "clicked", dbus.MakeVariant(int32(0)), uint32(time.Now().Unix())).Err
		}
		if c.Registrar == nil {
			return fmt.Errorf("appmenu: no registrar")
		}
		return c.Registrar.Activate(r, e.Action.Index)
	}
	return nil
}
