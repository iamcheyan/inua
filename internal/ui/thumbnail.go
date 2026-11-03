package ui

import (
	"bytes"
	"context"
	"errors"
	"image"
	"image/draw"
	"image/png"
	"os"
	"os/exec"
	"path/filepath"
	"strings"

	xdraw "golang.org/x/image/draw"

	"codeberg.org/puregotk/puregotk/v4/gdk"
	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/hypr"
	"github.com/lyricat/inua/internal/shell"
)

// windowThumbnail captures and crops one window from its output. Wayfire
// has no per-window capture protocol.
func (s *shellUI) windowThumbnail(ctx context.Context, snap hypr.Snapshot, address string) (string, error) {
	for _, window := range snap.Toplevels {
		if window.Address != address {
			continue
		}
		paths, err := s.windowThumbnails(ctx, snap, []hypr.Toplevel{window}, 0, 0)
		if err != nil {
			return "", err
		}
		return paths[0], nil
	}
	return "", errors.New("window is gone")
}

// windowThumbnails captures each output once, then crops every requested
// window from that frame. Windows on different outputs use their own frame.
func (s *shellUI) windowThumbnails(ctx context.Context, snap hypr.Snapshot, windows []hypr.Toplevel, maxW, maxH int) ([]string, error) {
	type group struct {
		monitor hypr.Monitor
		windows []hypr.Toplevel
		indices []int
	}
	groups := make([]group, 0, len(windows))
	byMonitor := make(map[string]int, len(windows))
	for i, window := range windows {
		var monitor hypr.Monitor
		found := false
		for _, candidate := range snap.Monitors {
			if candidate.Name == window.Monitor {
				monitor, found = candidate, true
				break
			}
		}
		if !found || monitor.Width <= 0 {
			return nil, errors.New("window monitor is unknown")
		}
		j, ok := byMonitor[monitor.Name]
		if !ok {
			j = len(groups)
			byMonitor[monitor.Name] = j
			groups = append(groups, group{monitor: monitor})
		}
		groups[j].windows = append(groups[j].windows, window)
		groups[j].indices = append(groups[j].indices, i)
	}

	paths := make([]string, len(windows))
	for _, group := range groups {
		raw, err := exec.CommandContext(ctx, "grim", "-o", group.monitor.Name, "-").Output()
		if err != nil {
			return nil, err
		}
		img, err := png.Decode(bytes.NewReader(raw))
		if err != nil {
			return nil, err
		}
		for i, window := range group.windows {
			thumb, err := cropWindowThumbnail(img, group.monitor, window)
			if err != nil {
				return nil, err
			}
			if maxW > 0 && maxH > 0 {
				thumb = shrinkWindowThumbnail(thumb, maxW, maxH)
			}
			paths[group.indices[i]], err = saveWindowThumbnail(window.Address, thumb)
			if err != nil {
				return nil, err
			}
		}
	}
	return paths, nil
}

func cropWindowThumbnail(img image.Image, monitor hypr.Monitor, window hypr.Toplevel) (image.Image, error) {
	x, y, w, h := 0.0, 0.0, 0.0, 0.0
	if geometry, ok := window.Raw["geometry"].([]any); ok && len(geometry) >= 4 {
		x, _ = geometry[0].(float64)
		y, _ = geometry[1].(float64)
		w, _ = geometry[2].(float64)
		h, _ = geometry[3].(float64)
	} else {
		x, y = overviewPair(window.Raw["at"], 0, 0)
		w, h = overviewPair(window.Raw["size"], 0, 0)
	}
	// Wayfire's geometry is global; grim captures one output at a time.
	x -= float64(monitor.X)
	y -= float64(monitor.Y)
	if w <= 0 || h <= 0 {
		return nil, errors.New("window has no geometry")
	}
	factor := float64(img.Bounds().Dx()) / float64(monitor.Width)
	if monitor.Scale > 1 && x+w <= float64(monitor.Width)/monitor.Scale+2 {
		factor = monitor.Scale
	}
	rect := image.Rect(
		int(x*factor), int(y*factor),
		int((x+w)*factor), int((y+h)*factor),
	).Intersect(img.Bounds())
	if rect.Empty() {
		return nil, errors.New("window is outside the output")
	}
	thumb := image.NewRGBA(image.Rect(0, 0, rect.Dx(), rect.Dy()))
	draw.Draw(thumb, thumb.Bounds(), img, rect.Min, draw.Src)
	return thumb, nil
}

func shrinkWindowThumbnail(img image.Image, maxW, maxH int) image.Image {
	bounds := img.Bounds()
	w, h := shell.ThumbSize(bounds.Dx(), bounds.Dy(), maxW, maxH)
	if w == bounds.Dx() && h == bounds.Dy() {
		return img
	}
	small := image.NewRGBA(image.Rect(0, 0, w, h))
	xdraw.ApproxBiLinear.Scale(small, small.Bounds(), img, bounds, xdraw.Src, nil)
	return small
}

func saveWindowThumbnail(address string, thumb image.Image) (string, error) {
	dir := filepath.Join(os.Getenv("XDG_RUNTIME_DIR"), "inua", "thumbs")
	if err := os.MkdirAll(dir, 0o700); err != nil {
		return "", err
	}
	name := strings.NewReplacer(":", "-", "/", "-").Replace(address) + ".png"
	path := filepath.Join(dir, name)
	file, err := os.Create(path)
	if err != nil {
		return "", err
	}
	if err := png.Encode(file, thumb); err != nil {
		file.Close()
		return "", err
	}
	if err := file.Close(); err != nil {
		return "", err
	}
	return path, nil
}

func setPictureFile(picture *gtk.Picture, path string) error {
	texture, err := gdk.NewTextureFromFilename(path)
	if err != nil {
		return err
	}
	picture.SetPaintable(texture)
	texture.Unref()
	return nil
}
