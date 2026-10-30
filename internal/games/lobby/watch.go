package lobby

import (
	"context"
	"net/http"
	"time"

	"github.com/gorilla/websocket"

	"github.com/lyricat/inua/internal/games/gamerelay"
)

// Watch follows the tables of the lobby at addr (a lobby's address as the
// user gives it), calling got with them as they change, until ctx ends
// or the connection drops.
func Watch(ctx context.Context, addr string, got func([]Table)) error {
	u, err := gamerelay.WatchURL(addr)
	if err != nil {
		return err
	}
	d := websocket.Dialer{HandshakeTimeout: 15 * time.Second, Proxy: http.ProxyFromEnvironment}
	ws, _, err := d.DialContext(ctx, u, nil)
	if err != nil {
		return err
	}
	defer ws.Close()
	stop := context.AfterFunc(ctx, func() { ws.Close() })
	defer stop()
	ws.SetReadLimit(1 << 20)
	for {
		var m Tables
		if err := ws.ReadJSON(&m); err != nil {
			if ctx.Err() != nil {
				return ctx.Err()
			}
			return err
		}
		if m.T == "tables" {
			got(m.Tables)
		}
	}
}
