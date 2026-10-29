package webterm

import (
	"os/exec"
	"strings"
	"testing"
)

// The agent's property list carries the program, its environment escaped,
// and the start at login and again after a failure.
func TestPlist(t *testing.T) {
	p := string(plist(Label, []string{"/Applications/inua-term.app/Contents/MacOS/inua-termd", "serve", "--addr", "127.0.0.1:7681"},
		[][2]string{{"PATH", "/usr/bin:/bin"}, {"LANG", "a&b<c"}}, "/Users/u/Library/Logs/inua-term-web.log"))
	for _, want := range []string{
		"<key>Label</key><string>io.github.lyricat.Inua.Term.Web</string>",
		"<array><string>/Applications/inua-term.app/Contents/MacOS/inua-termd</string><string>serve</string><string>--addr</string><string>127.0.0.1:7681</string></array>",
		"<key>PATH</key><string>/usr/bin:/bin</string><key>LANG</key><string>a&amp;b&lt;c</string>",
		"<key>RunAtLoad</key><true/>",
		"<key>KeepAlive</key><dict><key>SuccessfulExit</key><false/></dict>",
		"<key>StandardErrorPath</key><string>/Users/u/Library/Logs/inua-term-web.log</string>",
	} {
		if !strings.Contains(p, want) {
			t.Errorf("plist lacks %s:\n%s", want, p)
		}
	}
	if lint, err := exec.LookPath("plutil"); err == nil {
		cmd := exec.Command(lint, "-lint", "-")
		cmd.Stdin = strings.NewReader(p)
		if out, err := cmd.CombinedOutput(); err != nil {
			t.Errorf("plutil -lint: %v: %s", err, out)
		}
	}
}

// Only a job in the running state runs: one waiting to be spawned again
// after a failure does not.
func TestRunning(t *testing.T) {
	up := "gui/501/io.github.lyricat.Inua.Term.Web = {\n\tactive count = 1\n\tstate = running\n\tpid = 812\n}\n"
	down := "gui/501/io.github.lyricat.Inua.Term.Web = {\n\tactive count = 0\n\tstate = spawn scheduled\n\tlast exit code = 1\n}\n"
	if !running([]byte(up)) || running([]byte(down)) {
		t.Errorf("running: up %v, down %v", running([]byte(up)), running([]byte(down)))
	}
}
