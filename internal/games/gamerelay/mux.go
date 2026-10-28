// Package gamerelay carries a game's web traffic between a desktop that
// hosts it and inua-game-lobby, which visitors open: one WebSocket the
// desktop dials, many streams over it. Each stream is a net.Conn, so the
// lobby proxies browsers' requests with net/http and the desktop serves
// them with the game's own handler, unchanged.
//
// A binary message is a frame: its kind, the stream's number (big endian)
// and what it carries. A text message is the lobby and the desktop talking
// about the table (Publish, the lobby's Hosts).
package gamerelay

import (
	"context"
	"encoding/binary"
	"errors"
	"net"
	"sync"
	"time"

	"github.com/gorilla/websocket"
)

const (
	frameOpen   = 1 // a new stream
	frameData   = 2 // bytes for a stream
	frameClose  = 3 // the stream is done, both ways
	frameCredit = 4 // the receiver read this many more bytes (uint32)

	headerSize = 5
	// maxData is the most a data frame carries; window, the most a
	// stream's sender may have unread at the receiver, so a slow browser
	// holds up its own stream only.
	maxData = 32 << 10
	window  = 256 << 10
	// MaxStreams is how many streams a session has at once.
	MaxStreams = 512

	writeWait = 10 * time.Second
	pingEvery = 20 * time.Second
	deadAfter = 60 * time.Second
)

// ErrClosed is what a closed session's streams and Open return.
var ErrClosed = errors.New("gamerelay: closed")

// Session is the streams over one WebSocket. The end that dials opens the
// odd streams, the other the even ones; as a net.Listener it accepts those
// the other end opens.
type Session struct {
	ws      *websocket.Conn
	wmu     sync.Mutex // one writer at a time
	mu      sync.Mutex
	streams map[uint32]*stream
	next    uint32
	accept  chan *stream
	control chan []byte
	done    chan struct{}
	once    sync.Once
}

// NewSession runs the streams over ws; dialer says which end this is.
// It reads ws until either end closes it.
func NewSession(ws *websocket.Conn, dialer bool) *Session {
	s := &Session{ws: ws, streams: map[uint32]*stream{}, next: 2,
		accept: make(chan *stream, 64), control: make(chan []byte, 16), done: make(chan struct{})}
	if dialer {
		s.next = 1
	}
	ws.SetReadLimit(headerSize + maxData + 1024)
	ws.SetReadDeadline(time.Now().Add(deadAfter))
	ws.SetPongHandler(func(string) error { return ws.SetReadDeadline(time.Now().Add(deadAfter)) })
	go s.read()
	go s.ping()
	return s
}

// Done is closed when the session ends.
func (s *Session) Done() <-chan struct{} { return s.done }

// Control is the other end's text messages.
func (s *Session) Control() <-chan []byte { return s.control }

// SendControl sends the other end a text message.
func (s *Session) SendControl(b []byte) error {
	s.wmu.Lock()
	defer s.wmu.Unlock()
	s.ws.SetWriteDeadline(time.Now().Add(writeWait))
	if err := s.ws.WriteMessage(websocket.TextMessage, b); err != nil {
		s.Close()
		return err
	}
	return nil
}

// Open opens a stream to the other end.
func (s *Session) Open() (net.Conn, error) {
	s.mu.Lock()
	select {
	case <-s.done:
		s.mu.Unlock()
		return nil, ErrClosed
	default:
	}
	if len(s.streams) >= MaxStreams {
		s.mu.Unlock()
		return nil, errors.New("gamerelay: too many streams")
	}
	st := newStream(s, s.next)
	s.next += 2
	s.streams[st.id] = st
	s.mu.Unlock()
	if err := s.send(frameOpen, st.id, nil); err != nil {
		return nil, err
	}
	return st, nil
}

// Dial opens a stream, as an http.Transport's DialContext.
func (s *Session) Dial(context.Context, string, string) (net.Conn, error) { return s.Open() }

// Accept waits for a stream the other end opens.
func (s *Session) Accept() (net.Conn, error) {
	select {
	case st := <-s.accept:
		return st, nil
	case <-s.done:
		return nil, ErrClosed
	}
}

// Addr is the session's address as a listener: the other end's.
func (s *Session) Addr() net.Addr { return s.ws.RemoteAddr() }

// Close ends the session and every stream on it.
func (s *Session) Close() error {
	s.once.Do(func() {
		close(s.done)
		s.wmu.Lock()
		s.ws.SetWriteDeadline(time.Now().Add(time.Second))
		s.ws.WriteMessage(websocket.CloseMessage, websocket.FormatCloseMessage(websocket.CloseNormalClosure, ""))
		s.wmu.Unlock()
		s.ws.Close()
		s.mu.Lock()
		streams := s.streams
		s.streams = map[uint32]*stream{}
		s.mu.Unlock()
		for _, st := range streams {
			st.ended(ErrClosed)
		}
	})
	return nil
}

func (s *Session) send(kind byte, id uint32, data []byte) error {
	b := make([]byte, headerSize+len(data))
	b[0] = kind
	binary.BigEndian.PutUint32(b[1:], id)
	copy(b[headerSize:], data)
	s.wmu.Lock()
	defer s.wmu.Unlock()
	select {
	case <-s.done:
		return ErrClosed
	default:
	}
	s.ws.SetWriteDeadline(time.Now().Add(writeWait))
	if err := s.ws.WriteMessage(websocket.BinaryMessage, b); err != nil {
		go s.Close()
		return ErrClosed
	}
	return nil
}

func (s *Session) ping() {
	t := time.NewTicker(pingEvery)
	defer t.Stop()
	for {
		select {
		case <-t.C:
			if s.ws.WriteControl(websocket.PingMessage, nil, time.Now().Add(writeWait)) != nil {
				s.Close()
				return
			}
		case <-s.done:
			return
		}
	}
}

func (s *Session) read() {
	defer s.Close()
	for {
		kind, b, err := s.ws.ReadMessage()
		if err != nil {
			return
		}
		if kind == websocket.TextMessage {
			select {
			case s.control <- b:
			case <-s.done:
				return
			}
			continue
		}
		if len(b) < headerSize {
			return
		}
		id, data := binary.BigEndian.Uint32(b[1:]), b[headerSize:]
		s.mu.Lock()
		st := s.streams[id]
		s.mu.Unlock()
		switch b[0] {
		case frameOpen:
			if st != nil || id%2 == s.next%2 {
				return // the other end opens only its own, and once
			}
			st = newStream(s, id)
			s.mu.Lock()
			full := len(s.streams) >= MaxStreams
			if !full {
				s.streams[id] = st
			}
			s.mu.Unlock()
			if full {
				s.send(frameClose, id, nil)
				continue
			}
			select {
			case s.accept <- st:
			default: // no one accepting fast enough
				s.forget(id)
				s.send(frameClose, id, nil)
			}
		case frameData:
			if st != nil && !st.received(data) {
				return // more than its window: the other end is broken
			}
		case frameClose:
			if st != nil {
				s.forget(id)
				st.ended(nil)
			}
		case frameCredit:
			if st != nil && len(data) == 4 {
				st.credited(int(binary.BigEndian.Uint32(data)))
			}
		default:
			return
		}
	}
}

func (s *Session) forget(id uint32) {
	s.mu.Lock()
	delete(s.streams, id)
	s.mu.Unlock()
}
