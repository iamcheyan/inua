package appmenu

import (
	"context"
	"encoding/xml"
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
	if e, ok, err := c.kdeMenu(pid); ok || err != nil {
		return e, err
	}
	if e, ok, err := c.nativeWaylandMenu(pid); ok || err != nil {
		return e, err
	}
	// AT-SPI last: plain GTK4 apps answer it with a skeleton (a menubar whose
	// items have no labels), which must not shadow a real menu nor put blank
	// buttons in the bar. A browser's sections come through with no items at
	// all - it builds them when its own menu opens - and the shell cannot
	// fill them without pressing them, which crashes Firefox. So a tree of
	// empty sections is no menu either.
	if c.A11y != nil {
		if e, err := c.A11y.Menu(pid); err == nil && fillable(e) {
			return e, nil
		}
	}
	return nil, nil
}

// fillable reports whether a menu is one the bar can show: sections with
// their items, or named sections the application builds when they open (a
// browser's), which the bar fills one at a time as they are asked for. A
// tree of unnamed items is a toolkit skeleton and stays out.
func fillable(entries []Entry) bool {
	for _, e := range entries {
		if strings.TrimSpace(e.Label) == "" || e.Separator {
			continue
		}
		if len(e.Children) > 0 || Fillable(e) {
			return true
		}
	}
	return false
}

// Fillable reports whether an entry's items are made when it opens: the
// application answered with a named section and an action to open it, and
// nothing under it yet.
func Fillable(e Entry) bool {
	return len(e.Children) == 0 && !e.Separator && e.Label != "" &&
		e.Action.Kind == ActionA11y && e.Action.Bus != "" && e.Action.Path != ""
}

// labelled reports whether the menu says anything: at least one top-level
// item with text and a menu under it. A tree of unnamed items is a toolkit
// skeleton, not a menu; a bar of sections whose items the application only
// makes when its own menu opens (Firefox's, Chrome's) is a menu the shell
// cannot fill, and showing its titles would offer empty menus.
func labelled(entries []Entry) bool {
	for _, e := range entries {
		if strings.TrimSpace(e.Label) != "" && len(e.Children) > 0 {
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

// Fill reads the items of a section the application builds when it opens
// (a browser's File, Edit …): it opens that section once and closes it.
func (c *Client) Fill(e Entry) ([]Entry, error) {
	if c.A11y == nil {
		return nil, fmt.Errorf("appmenu: no accessibility bus")
	}
	return c.A11y.FillSection(e)
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
		if e.Action.NativeWayland || e.Action.Direct {
			// An endpoint the shell reads itself (inua's own menu, a KDE
			// application's) lives on the application's own connection: the
			// shell's registrar connection is not the one that serves it.
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

// kdeNamePrefix starts the well-known name a KDE application publishes its
// menu on: "org.kde.dolphin-280254", "org.kde.kate-3230144".
const kdeNamePrefix = "org.kde."

// kdeMenuRoot is where a KDE application's menus hang: /MenuBar, with one
// child for each window's menu (/MenuBar/1, /MenuBar/2 …).
const kdeMenuRoot = dbus.ObjectPath("/MenuBar")

// kdeMenu reads the menu a KDE application (Dolphin, Kate, Konsole …)
// exports on its own well-known name. KDE does not use the Canonical
// registrar and its applications are native Wayland, so this is the only
// place their menu is; the object is a plain com.canonical.dbusmenu tree,
// which the registrar's reader takes as it is.
//
// A process with more than one menu (several windows) shows none, as with
// inua's own: without a per-window identity the shell cannot tell which
// window's menu belongs to the focused one.
func (c *Client) kdeMenu(pid int) ([]Entry, bool, error) {
	conn, err := dbus.ConnectSessionBus()
	if err != nil {
		return nil, false, err
	}
	defer conn.Close()
	ctx, cancel := context.WithTimeout(context.Background(), callTimeout)
	defer cancel()
	var names []string
	if err = conn.BusObject().CallWithContext(ctx, "org.freedesktop.DBus.ListNames", 0).Store(&names); err != nil {
		return nil, false, err
	}
	var found []Registration
	for _, name := range names {
		if !strings.HasPrefix(name, kdeNamePrefix) {
			continue
		}
		var owner uint32
		if conn.BusObject().CallWithContext(ctx, "org.freedesktop.DBus.GetConnectionUnixProcessID", 0, name).Store(&owner) != nil || int(owner) != pid {
			continue
		}
		path, err := kdeMenuPath(conn, name)
		if err != nil || path == "" {
			// A name of KDE's with no menu (Kate until it is asked for
			// one, an application that keeps its menus to itself): not a
			// reason to stop looking, nor to stop the other sources.
			continue
		}
		found = append(found, Registration{PID: uint32(pid), Service: name, Path: path})
	}
	if len(found) != 1 {
		return nil, len(found) > 1, nil
	}
	entries, err := c.readMenu(conn, found[0])
	if err != nil {
		return nil, true, err
	}
	if !labelled(entries) {
		return nil, true, nil
	}
	direct(entries)
	return entries, true, nil
}

// kdeMenuPath is the object a KDE application exports its menu at: the
// first child of /MenuBar ("/MenuBar/2"), or "" when it has none. KDE
// names the child after the window it belongs to, so the path is read from
// the introspection XML rather than guessed at.
func kdeMenuPath(conn *dbus.Conn, service string) (dbus.ObjectPath, error) {
	ctx, cancel := context.WithTimeout(context.Background(), callTimeout)
	defer cancel()
	var decoded string
	call := conn.Object(service, kdeMenuRoot).CallWithContext(ctx, "org.freedesktop.DBus.Introspectable.Introspect", 0)
	if call.Err != nil {
		return "", call.Err
	}
	if err := call.Store(&decoded); err != nil {
		return "", err
	}
	// The reply is the object's own node, with its children inside it. The
	// root carries no name of its own (the bus answers "<node>" there, only
	// the test's fixture has a name), so the first child named is the menu's.
	var node struct {
		Children []struct {
			Name string `xml:"name,attr"`
		} `xml:"node"`
	}
	if err := xml.Unmarshal([]byte(decoded), &node); err != nil {
		return "", err
	}
	for _, child := range node.Children {
		if child.Name == "" || strings.ContainsAny(child.Name, "/<>") {
			continue
		}
		return kdeMenuRoot + "/" + dbus.ObjectPath(child.Name), nil
	}
	return "", nil
}

// direct marks entries the shell read itself: their clicks go to the
// application's connection, not through the Registrar.
func direct(entries []Entry) {
	for i := range entries {
		if len(entries[i].Children) > 0 {
			direct(entries[i].Children)
			continue
		}
		entries[i].Action.Direct = true
	}
}
