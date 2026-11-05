package ui

import (
	"bytes"
	"context"
	"fmt"
	"image"
	"image/png"
	"log"
	"os/exec"
	"time"

	"github.com/lyricat/inua/internal/capture/hyprland"
	"github.com/lyricat/inua/internal/compositor"
	"github.com/lyricat/inua/internal/gtkx"
)

// Wayfire has the windows' geometry but no per-window capture protocol, so
// the overview's pictures are cut from each output's frame: one screenshot
// per output, taken again every couple of seconds while the overview is
// open. The cards are drawn by the same code as Hyprland's; only where the
// pixels come from is different.
const wayfireCaptureEvery = 2 * time.Second

// wayfireTarget is one window to cut out of an output's frame. Both are
// read on the GTK thread, from the snapshot the overview was drawn with.
type wayfireTarget struct {
	id   string
	out  compositor.Output
	rect compositor.Rect
}

// updateWayfireOverview captures the cards' windows as still pictures, one
// pass at a time, and asks for another pass while the overview stays open.
func (s *shellUI) updateWayfireOverview() {
	o := &s.overview
	if !o.st.Open || o.wayfireBusy {
		return
	}
	var ids []string
	for _, card := range o.st.Cards {
		for _, w := range card.Windows {
			ids = append(ids, w.ID)
		}
	}
	targets := wayfireTargets(s.snap, ids)
	if len(targets) == 0 {
		return
	}
	o.captureGen++
	gen := o.captureGen
	o.wayfireBusy = true
	go func() {
		frames, err := captureWayfireFrames(context.Background(), targets)
		gtkx.Post(func() {
			o.wayfireBusy = false
			if o.captureGen != gen || !o.st.Open {
				return
			}
			if err != nil {
				log.Printf("overview capture: %v", err)
				return
			}
			for _, f := range frames {
				w, h := s.overviewPreviewSize(f.Address)
				s.queueOverviewFrame(gen, hyprland.Shrink(f, w, h))
			}
			time.AfterFunc(wayfireCaptureEvery, func() {
				gtkx.Post(func() {
					if o.captureGen == gen && o.st.Open {
						s.updateWayfireOverview()
					}
				})
			})
		})
	}()
}

// wayfireTargets finds the windows to capture in the snapshot: those the
// overview shows, with the output they sit on. A window whose output or
// geometry the compositor does not report is left out; its card keeps the
// title and icon alone.
func wayfireTargets(snap compositor.Snapshot, ids []string) []wayfireTarget {
	want := make(map[string]bool, len(ids))
	for _, id := range ids {
		want[id] = true
	}
	var out []wayfireTarget
	for _, w := range snap.Windows {
		if !want[w.ID] || w.Geometry == nil {
			continue
		}
		o, ok := snap.Output(w.Output)
		if !ok || o.Width <= 0 || o.Height <= 0 {
			continue
		}
		out = append(out, wayfireTarget{id: w.ID, out: o, rect: *w.Geometry})
	}
	return out
}

// cropWindow cuts a window out of its output's frame. The window's place is
// in the layout's logical pixels and the frame is the output in physical
// ones, so the window is moved by the output's own place and scaled before
// it is cut, then kept inside the frame: a window hanging over the edge, or
// one the compositor reports larger than its output, gives what is there.
func cropWindow(frame *image.RGBA, out compositor.Output, win compositor.Rect) *image.RGBA {
	if frame == nil || out.Width <= 0 || out.Height <= 0 || win.W <= 0 || win.H <= 0 {
		return nil
	}
	scale := out.Scale
	if scale <= 0 {
		scale = 1
	}
	x0 := int(float64(win.X-out.X) * scale)
	y0 := int(float64(win.Y-out.Y) * scale)
	x1 := x0 + int(float64(win.W)*scale)
	y1 := y0 + int(float64(win.H)*scale)
	b := frame.Bounds()
	x0, y0 = max(x0, b.Min.X), max(y0, b.Min.Y)
	x1, y1 = min(x1, b.Max.X), min(y1, b.Max.Y)
	if x1 <= x0 || y1 <= y0 {
		return nil
	}
	crop := image.NewRGBA(image.Rect(0, 0, x1-x0, y1-y0))
	for y := y0; y < y1; y++ {
		src := frame.Pix[y*frame.Stride+x0*4 : y*frame.Stride+x1*4]
		dst := crop.Pix[(y-y0)*crop.Stride : (y-y0)*crop.Stride+(x1-x0)*4]
		copy(dst, src)
	}
	return crop
}

// frameOf turns a cropped picture into the frame the overview's textures
// are made from. PNG decodes to R, G, B, A bytes, which is what
// DRM_FORMAT_ABGR8888 (0x34324241) names.
func frameOf(id string, img *image.RGBA) hyprland.Frame {
	b := img.Bounds()
	return hyprland.Frame{
		Address: id,
		Width:   b.Dx(),
		Height:  b.Dy(),
		Stride:  img.Stride,
		Format:  0x34324241,
		Pixels:  img.Pix,
	}
}

// captureWayfireFrames screenshots each output the targets sit on, once,
// and cuts every target out of its frame.
func captureWayfireFrames(ctx context.Context, targets []wayfireTarget) ([]hyprland.Frame, error) {
	frames := make(map[string]*image.RGBA, len(targets))
	var firstErr error
	for _, t := range targets {
		if _, ok := frames[t.out.Name]; ok {
			continue
		}
		img, err := outputFrame(ctx, t.out.Name)
		if err != nil {
			if firstErr == nil {
				firstErr = err
			}
			continue
		}
		frames[t.out.Name] = img
	}
	var out []hyprland.Frame
	for _, t := range targets {
		img, ok := frames[t.out.Name]
		if !ok {
			continue
		}
		if crop := cropWindow(img, t.out, t.rect); crop != nil {
			out = append(out, frameOf(t.id, crop))
		}
	}
	if len(out) == 0 && firstErr != nil {
		return nil, firstErr
	}
	return out, nil
}

// outputFrame is one output as the compositor shows it now, in its own
// pixels: grim reads it through wlr-screencopy, which Wayfire serves.
func outputFrame(ctx context.Context, name string) (*image.RGBA, error) {
	raw, err := exec.CommandContext(ctx, "grim", "-o", name, "-").Output()
	if err != nil {
		return nil, fmt.Errorf("grim -o %s: %w", name, err)
	}
	img, err := png.Decode(bytes.NewReader(raw))
	if err != nil {
		return nil, fmt.Errorf("grim -o %s: %w", name, err)
	}
	if rgba, ok := img.(*image.RGBA); ok {
		return rgba, nil
	}
	b := img.Bounds()
	rgba := image.NewRGBA(image.Rect(0, 0, b.Dx(), b.Dy()))
	for y := b.Min.Y; y < b.Max.Y; y++ {
		for x := b.Min.X; x < b.Max.X; x++ {
			rgba.Set(x-b.Min.X, y-b.Min.Y, img.At(x, y))
		}
	}
	return rgba, nil
}
