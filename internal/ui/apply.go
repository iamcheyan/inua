package ui

import (
	"cmp"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strconv"
	"strings"

	"codeberg.org/puregotk/puregotk/v4/gdk"
	"codeberg.org/puregotk/puregotk/v4/gtk"

	"github.com/lyricat/inua/internal/config"
	"github.com/lyricat/inua/internal/i18n"
	"github.com/lyricat/inua/internal/ipc"
	"github.com/lyricat/inua/internal/layershell"
	"github.com/lyricat/inua/internal/notify"
	"github.com/lyricat/inua/internal/rundir"
	"github.com/lyricat/inua/internal/shell"
)

// styles are the CSS providers the shell keeps, so settings can change
// them while it runs.
type styles struct {
	base      *gtk.CssProvider // theme tokens + style.css
	user      *gtk.CssProvider // style.css from the config directory
	wallpaper *gtk.CssProvider // window.wallpaper
	clipboard *gtk.CssProvider // clipboard card opacity
	swatches  *gtk.CssProvider // the settings window's theme swatches
	bar       *gtk.CssProvider // per-workspace bar background transparency
	shell     *gtk.CssProvider // style.transparency, over every floating surface
}

func (s *shellUI) theme() string { return cmp.Or(s.cfg.Style.Theme, "yoru") }

// loadStyles (re)loads the theme, the built-in style and the user's
// stylesheet.
func (s *shellUI) loadStyles() {
	defer func() {
		// Style is compared as a whole in applyConfig, so the settings
		// window's slider must follow it here too.
		if s.settings.win != nil {
			s.settings.transparency.SetValue(float64(s.cfg.Style.Transparency))
			s.settings.transparencyVal.SetText(i18n.Tf("%d%%", s.cfg.Style.Transparency))
		}
	}()
	st := &s.styles
	display := gdk.DisplayGetDefault()
	if st.base == nil {
		st.base, st.user, st.wallpaper = gtk.NewCssProvider(), gtk.NewCssProvider(), gtk.NewCssProvider()
		gtk.StyleContextAddProviderForDisplay(display, st.base, uint32(gtk.STYLE_PROVIDER_PRIORITY_APPLICATION))
		gtk.StyleContextAddProviderForDisplay(display, st.wallpaper, uint32(gtk.STYLE_PROVIDER_PRIORITY_APPLICATION))
		gtk.StyleContextAddProviderForDisplay(display, st.user, uint32(gtk.STYLE_PROVIDER_PRIORITY_USER))
	}
	// The theme defines the colour tokens style.css uses.
	st.base.LoadFromString(s.cfg.ThemeCSS(s.theme(), s.readUI) + shell.ScaleText(s.readUI("style.css"), s.cfg.Style.TextScale))
	user := ""
	if path := s.cfg.CSSPath(); path != "" {
		if css, err := os.ReadFile(path); err == nil {
			user = string(css)
			log.Printf("style: %s", path)
		} else if !os.IsNotExist(err) {
			log.Printf("style: %v", err)
		}
	}
	st.user.LoadFromString(user)
	s.loadIcons()
	s.loadClipboardStyle()
	s.loadBarStyle()
	s.loadShellStyle()
}

func (s *shellUI) loadBarStyle() {
	st := &s.styles
	if st.bar == nil {
		st.bar = gtk.NewCssProvider()
		gtk.StyleContextAddProviderForDisplay(gdk.DisplayGetDefault(), st.bar, uint32(gtk.STYLE_PROVIDER_PRIORITY_APPLICATION+1))
	}
	empty := s.cfg.Style.Transparency
	if s.cfg.Bar.EmptyTransparency != nil {
		empty = *s.cfg.Bar.EmptyTransparency
	}
	occupied := s.cfg.Style.Transparency
	if s.cfg.Bar.WindowTransparency != nil {
		occupied = *s.cfg.Bar.WindowTransparency
	}
	st.bar.LoadFromString(fmt.Sprintf(
		".bar.empty .island { background: alpha(@app, %s); border-radius: %spx; }\n.bar.occupied .island { background: alpha(@app, %s); border-radius: %spx; }\n",
		alpha(1-float64(empty)/100), strconv.Itoa(s.cfg.Style.Radius),
		alpha(1-float64(occupied)/100), strconv.Itoa(s.cfg.Style.Radius)))
}

// shellSurfaces are the floating surfaces the two [style] looks apply to:
// the transparency's background and the radius's corners. The launcher,
// each panel's card, the dock, the shot drawer and the menus; the bar's
// islands are in loadBarStyle, with their own transparency. The settings,
// lock and polkit windows keep their own looks.
const shellSurfaces = `.launcher,
.agenda .card,
.control .card,
.center .card,
.note,
.dock,
.shot-drawer,
popover.menu > contents,
popover.menu > arrow { background: alpha(@app, %s); border-radius: %spx; }
`

// loadClipboardStyle applies the clipboard panel's own opacity, or the
// shell's transparency when it sets none.
func (s *shellUI) loadClipboardStyle() {
	st := &s.styles
	if st.clipboard == nil {
		st.clipboard = gtk.NewCssProvider()
		gtk.StyleContextAddProviderForDisplay(gdk.DisplayGetDefault(), st.clipboard, uint32(gtk.STYLE_PROVIDER_PRIORITY_APPLICATION+1))
	}
	opacity := s.cfg.Style.Transparency
	if s.cfg.Clipboard.Opacity != nil {
		opacity = *s.cfg.Clipboard.Opacity
	}
	// The settings file checks the range (config.validate).
	css := fmt.Sprintf(".clipboard-panel .clipboard-card { background: alpha(@app, %.2f); }\n", 1-float64(opacity)/100)
	st.clipboard.LoadFromString(css)
}

// loadShellStyle applies style.transparency and style.radius over every
// floating surface, so they share one opacity and corner radius the user
// sets once.
func (s *shellUI) loadShellStyle() {
	st := &s.styles
	if st.shell == nil {
		st.shell = gtk.NewCssProvider()
		gtk.StyleContextAddProviderForDisplay(gdk.DisplayGetDefault(), st.shell, uint32(gtk.STYLE_PROVIDER_PRIORITY_APPLICATION+1))
	}
	// The settings file checks both ranges (config.validate).
	st.shell.LoadFromString(fmt.Sprintf(shellSurfaces,
		alpha(1-float64(s.cfg.Style.Transparency)/100),
		strconv.Itoa(s.cfg.Style.Radius)))
}

// alpha renders an opacity as the CSS alpha() argument, two decimals.
func alpha(v float64) string { return fmt.Sprintf("%.2f", v) }

// loadWallpaper styles the wallpaper windows from the settings. Without an
// image they show the theme's ground with the texture, whose tile is
// written to the runtime directory.
func (s *shellUI) loadWallpaper() {
	bg := s.cfg.Background
	w := shell.Wallpaper{Image: s.cfg.ImagePath(), Fit: bg.Fit, Color: bg.Color}
	if w.Image == "" {
		colors := shellThemeColors(s, s.theme())
		path, err := writeTile(colors["field"])
		if err != nil {
			log.Printf("wallpaper: %v", err)
		}
		w.Tile = path
	}
	s.styles.wallpaper.LoadFromString(w.CSS() + strings.ReplaceAll(w.CSS(), "window.wallpaper, window.lock .lock-ground", ".overview .overview-workspace-background"))
}

// shellThemeColors reads a theme's colour tokens.
func shellThemeColors(s *shellUI, name string) map[string]string {
	return shell.ThemeColors(s.cfg.ThemeCSS(name, s.readUI))
}

func writeTile(field string) (string, error) {
	data, err := shell.FieldTile(field, 0.55)
	if err != nil {
		return "", err
	}
	dir, err := rundir.Dir()
	if err != nil {
		return "", err
	}
	path := filepath.Join(dir, "field-"+strings.TrimPrefix(field, "#")+".png")
	if _, err := os.Stat(path); err == nil {
		return path, nil
	}
	return path, os.WriteFile(path, data, 0o644)
}

// syncWallpaper gives a bar's monitor a wallpaper window, or takes it away,
// following background.enable.
func (s *shellUI) syncWallpaper(b *bar) {
	want := s.cfg.Background.Enable && s.layer
	switch {
	case want && b.wallpaper == nil:
		win := gtk.NewApplicationWindow(s.app)
		win.AddCssClass("wallpaper")
		win.SetDecorated(false)
		w := win.GoPointer()
		layershell.InitForWindow(w)
		layershell.SetNamespace(w, "inua-background")
		layershell.SetLayer(w, layershell.LayerBackground)
		layershell.SetMonitor(w, b.mon.GoPointer())
		for _, e := range []layershell.Edge{layershell.EdgeTop, layershell.EdgeBottom, layershell.EdgeLeft, layershell.EdgeRight} {
			layershell.SetAnchor(w, e, true)
		}
		layershell.SetExclusiveZone(w, -1) // under the bar too
		win.Present()
		b.wallpaper = win // the window list holds it; ours goes in dropWallpaper
	case !want && b.wallpaper != nil:
		dropWallpaper(b)
	}
}

func dropWallpaper(b *bar) {
	if b.wallpaper != nil {
		b.wallpaper.Destroy()
		b.wallpaper.Unref()
		b.wallpaper = nil
	}
}

// applyConfig switches to new settings while running: styles, wallpaper,
// bars and the clock follow at once; the launcher and control center read
// their settings when used.
func (s *shellUI) applyConfig(c config.Config) {
	old := s.cfg
	s.cfg = c
	if !old.Assistant.Enable && c.Assistant.Enable {
		s.startAssistant()
	}
	if old.Notify.History && !c.Notify.History {
		go noteHistory(func(path string) error { return notify.ClearHistory(path) })
	}
	if old.Overview != c.Overview {
		s.installOverviewKeys()
	}
	if old.Style != c.Style {
		s.loadStyles()
	} else if old.Style.Transparency != c.Style.Transparency {
		s.loadShellStyle()
	}
	if old.Style.AppIcons != c.Style.AppIcons {
		for _, b := range s.bars {
			if b.dock != nil {
				b.dock.shown = "" // its buttons again, with the icons
			}
		}
		s.renderDocks()
	}
	if old.Bar.EmptyTransparency != c.Bar.EmptyTransparency || old.Bar.WindowTransparency != c.Bar.WindowTransparency {
		s.loadBarStyle()
	}
	if old.Osd.Position != c.Osd.Position && s.osd.win != nil && s.layer {
		s.placeOsd(s.osd.win.GoPointer(), s.osd.mon)
	}
	if old.Style.Theme != c.Style.Theme || old.Background != c.Background || old.Dir != c.Dir {
		s.loadWallpaper()
	}
	for _, b := range s.bars {
		if old.Bar.Density != c.Bar.Density {
			b.setDensity(c.Bar.Density)
		}
		if old.Style.EdgeGaps != c.Style.EdgeGaps {
			b.setEdgeGap(c.Style.EdgeGaps)
		}
		if old.Bar.Enable != c.Bar.Enable {
			b.win.SetVisible(c.Bar.Enable)
		}
		s.syncDock(b)
		b.title.SetVisible(c.Bar.Title)
		b.tray.SetVisible(c.Bar.Tray)
		b.clipboard.SetVisible(c.Clipboard.Enable && c.Clipboard.Bar)
		b.passwords.SetVisible(c.Bar.Pass && s.passwords.hasStore)
		b.setHypr(s, s.snap)
		s.syncWallpaper(b)
	}
	if c.Bar.Pass && !old.Bar.Pass {
		s.checkPasswordsStore() // one may have been made since
	}
	if old.Clipboard.Opacity != c.Clipboard.Opacity {
		s.loadClipboardStyle()
	}
	if old.Clipboard.Enable != c.Clipboard.Enable {
		if c.Clipboard.Enable {
			s.startClipboardCapture()
		} else {
			s.stopClipboardCapture()
			s.closeClipboard()
		}
	}
	if c.Bar.Tray && s.tray.host == nil {
		s.startTray()
	}
	if old.Notify.Enable != c.Notify.Enable {
		s.syncNotify()
	}
	if old.Bar.Clock != c.Bar.Clock {
		s.restartClock()
	}
	s.applyLauncherWeb()
	s.overview.st.SetMRU(c.Overview.MRU)
	s.renderOverview()
	if s.settings.win != nil {
		s.showSettings()
	}
}

// reload reads the settings file again and applies it.
func (s *shellUI) reload() ipc.Response {
	c, warnings, err := config.Load(s.opts.ConfigPath)
	if err != nil {
		return ipc.Response{Error: err.Error()}
	}
	same := s.cfg.Style == c.Style
	s.applyConfig(c)
	if same {
		// The user's theme or icon set may have changed on disk.
		s.loadStyles()
		s.loadWallpaper()
	}
	s.applyHyprland()
	msg := fmt.Sprintf("reloaded %s", s.opts.ConfigPath)
	for _, w := range warnings {
		msg += "\n" + w
	}
	return ipc.Response{OK: true, Result: msg}
}
