package gamerelay

import (
	"encoding/binary"
	"io"
	"net"
	"os"
	"sync"
	"time"
)

// stream is one connection over a session: what arrived waits in buf for
// Read; Write sends while the other end has room (credit).
type stream struct {
	s  *Session
	id uint32

	mu       sync.Mutex
	cond     *sync.Cond
	buf      []byte
	credit   int   // what may still be sent
	unacked  int   // read since the last credit sent back
	closed   bool  // this end closed it
	peerDone bool  // the other end closed it, or the session ended
	err      error // why, when the session ended
	rdl, wdl time.Time
	rt, wt   *time.Timer
}

func newStream(s *Session, id uint32) *stream {
	st := &stream{s: s, id: id, credit: window}
	st.cond = sync.NewCond(&st.mu)
	return st
}

func (st *stream) Read(p []byte) (int, error) {
	st.mu.Lock()
	for len(st.buf) == 0 {
		switch {
		case st.closed:
			st.mu.Unlock()
			return 0, net.ErrClosed
		case st.peerDone:
			err := st.err
			st.mu.Unlock()
			if err == nil {
				err = io.EOF
			}
			return 0, err
		case passed(st.rdl):
			st.mu.Unlock()
			return 0, os.ErrDeadlineExceeded
		}
		st.cond.Wait()
	}
	n := copy(p, st.buf)
	st.buf = st.buf[n:]
	if len(st.buf) == 0 {
		st.buf = nil
	}
	st.unacked += n
	back := 0
	if st.unacked >= window/4 && !st.peerDone {
		back, st.unacked = st.unacked, 0
	}
	st.mu.Unlock()
	if back > 0 {
		var b [4]byte
		binary.BigEndian.PutUint32(b[:], uint32(back))
		st.s.send(frameCredit, st.id, b[:])
	}
	return n, nil
}

func (st *stream) Write(p []byte) (int, error) {
	sent := 0
	for sent < len(p) {
		st.mu.Lock()
		for st.credit == 0 && !st.closed && !st.peerDone && !passed(st.wdl) {
			st.cond.Wait()
		}
		switch {
		case st.closed:
			st.mu.Unlock()
			return sent, net.ErrClosed
		case st.peerDone:
			st.mu.Unlock()
			return sent, io.ErrClosedPipe
		case st.credit == 0:
			st.mu.Unlock()
			return sent, os.ErrDeadlineExceeded
		}
		n := min(len(p)-sent, maxData, st.credit)
		st.credit -= n
		st.mu.Unlock()
		if err := st.s.send(frameData, st.id, p[sent:sent+n]); err != nil {
			return sent, err
		}
		sent += n
	}
	return sent, nil
}

func (st *stream) Close() error {
	st.mu.Lock()
	if st.closed {
		st.mu.Unlock()
		return nil
	}
	st.closed = true
	tell := !st.peerDone
	st.cond.Broadcast()
	st.mu.Unlock()
	st.s.forget(st.id)
	if tell {
		st.s.send(frameClose, st.id, nil)
	}
	return nil
}

// received takes bytes from the other end; false when it sent more than
// its window.
func (st *stream) received(b []byte) bool {
	st.mu.Lock()
	defer st.mu.Unlock()
	if len(st.buf)+len(b) > window {
		return false
	}
	if !st.closed {
		st.buf = append(st.buf, b...)
		st.cond.Broadcast()
	}
	return true
}

func (st *stream) credited(n int) {
	st.mu.Lock()
	st.credit = min(st.credit+n, window)
	st.cond.Broadcast()
	st.mu.Unlock()
}

// ended: the other end closed the stream (err nil), or the session ended.
func (st *stream) ended(err error) {
	st.mu.Lock()
	st.peerDone, st.err = true, err
	st.cond.Broadcast()
	st.mu.Unlock()
}

func (st *stream) LocalAddr() net.Addr  { return st.s.ws.LocalAddr() }
func (st *stream) RemoteAddr() net.Addr { return st.s.ws.RemoteAddr() }

func (st *stream) SetDeadline(t time.Time) error {
	st.SetReadDeadline(t)
	return st.SetWriteDeadline(t)
}

func (st *stream) SetReadDeadline(t time.Time) error {
	st.mu.Lock()
	defer st.mu.Unlock()
	st.rdl = t
	st.rt = st.wake(st.rt, t)
	return nil
}

func (st *stream) SetWriteDeadline(t time.Time) error {
	st.mu.Lock()
	defer st.mu.Unlock()
	st.wdl = t
	st.wt = st.wake(st.wt, t)
	return nil
}

// wake wakes the waiting Read or Write when a deadline passes.
func (st *stream) wake(old *time.Timer, t time.Time) *time.Timer {
	if old != nil {
		old.Stop()
	}
	st.cond.Broadcast()
	if t.IsZero() {
		return nil
	}
	return time.AfterFunc(time.Until(t), func() {
		st.mu.Lock()
		st.cond.Broadcast()
		st.mu.Unlock()
	})
}

func passed(t time.Time) bool { return !t.IsZero() && !time.Now().Before(t) }
