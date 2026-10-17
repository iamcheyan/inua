package backup

import (
	"context"
	"encoding/base64"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"slices"
	"strings"
	"sync"
	"testing"
	"time"
)

// layout makes a configuration directory of the kind inua writes.
func layout(t *testing.T) string {
	t.Helper()
	dir := t.TempDir()
	write(t, filepath.Join(dir, "inua/config.toml"), "[bar]\nclock = \"%H:%M\"\n")
	write(t, filepath.Join(dir, "inua/style.css"), "window { color: red; }\n")
	write(t, filepath.Join(dir, "inua/themes/nord.css"), "@define-color app #2e3440;\n")
	write(t, filepath.Join(dir, "inua/icons/phosphor-bold/go-home-symbolic.svg"), "<svg/>\n")
	write(t, filepath.Join(dir, "hypr/inua.conf"), "input {\n    kb_options = ctrl:nocaps\n}\n")
	return dir
}

func write(t *testing.T, path, content string) {
	t.Helper()
	if err := os.MkdirAll(filepath.Dir(path), 0o755); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(path, []byte(content), 0o644); err != nil {
		t.Fatal(err)
	}
}

// TestCollectReadsTheChosenParts checks what is carried, and where.
func TestCollectReadsTheChosenParts(t *testing.T) {
	dir := layout(t)
	files, missing, err := Collect(dir, []string{"settings", "style", "hyprland"})
	if err != nil {
		t.Fatal(err)
	}
	if len(missing) != 0 {
		t.Errorf("missing parts: %v", missing)
	}
	paths := make([]string, 0, len(files))
	for _, f := range files {
		paths = append(paths, f.Path)
	}
	want := []string{
		"hypr/inua.conf",
		"inua/config.toml",
		"inua/icons/phosphor-bold/go-home-symbolic.svg",
		"inua/style.css",
		"inua/themes/nord.css",
	}
	if !slices.Equal(paths, want) {
		t.Errorf("paths %v, want %v", paths, want)
	}
	for _, f := range files {
		if f.Sum != BlobSum(f.Data) {
			t.Errorf("%s: sum does not match its data", f.Path)
		}
	}
}

// TestCollectLeavesOutWhatIsNotThere: a part with no file is named, not an
// error, so a new computer can push the parts it has.
func TestCollectLeavesOutWhatIsNotThere(t *testing.T) {
	dir := t.TempDir()
	write(t, filepath.Join(dir, "inua/config.toml"), "x = 1\n")
	files, missing, err := Collect(dir, []string{"settings", "assistant"})
	if err != nil {
		t.Fatal(err)
	}
	if len(files) != 1 || files[0].Path != "inua/config.toml" {
		t.Errorf("files %v", files)
	}
	if !slices.Equal(missing, []string{"The assistant's profiles"}) {
		t.Errorf("missing %v", missing)
	}
}

// TestCollectSkipsHistory: the assistant's conversations hold what people
// typed and are not carried.
func TestCollectSkipsHistory(t *testing.T) {
	dir := t.TempDir()
	write(t, filepath.Join(dir, "inua/assistant/profiles.toml"), "x = 1\n")
	write(t, filepath.Join(dir, "inua/assistant/history/2026-10-17.json"), "{}\n")
	files, _, err := Collect(dir, []string{"assistant"})
	if err != nil {
		t.Fatal(err)
	}
	for _, f := range files {
		if strings.Contains(f.Path, "history") {
			t.Errorf("a conversation was carried: %s", f.Path)
		}
	}
	if len(files) != 1 {
		t.Errorf("files %v", files)
	}
}

// TestCollectRefusesAnUnknownPart keeps a typo out of a setup.
func TestCollectRefusesAnUnknownPart(t *testing.T) {
	if _, _, err := Collect(t.TempDir(), []string{"nonsense"}); err == nil {
		t.Fatal("an unknown part was accepted")
	}
}

// TestChangedWritesOnlyWhatDiffers is the heart of "a quiet computer says
// nothing": an unchanged file is not written again.
func TestChangedWritesOnlyWhatDiffers(t *testing.T) {
	same := []byte("unchanged\n")
	other := []byte("changed here\n")
	local := []File{
		{Path: "a.conf", Data: same, Sum: BlobSum(same)},
		{Path: "b.conf", Data: other, Sum: BlobSum(other)},
	}
	remote := map[string]string{
		RepoPath(local[0]): BlobSum(same),        // the same both sides
		RepoPath(local[1]): BlobSum([]byte("x")), // another computer's copy
		"inua/gone.conf":   BlobSum([]byte("y")), // removed here
		"unrelated.txt":    BlobSum([]byte("z")), // not ours, left alone
	}
	write, remove := Changed(local, remote)
	if len(write) != 1 || write[0].Path != "b.conf" {
		t.Errorf("write %v, want only b.conf", write)
	}
	if !slices.Equal(remove, []string{"inua/gone.conf"}) {
		t.Errorf("remove %v, want only our own path", remove)
	}
}

// TestChangedIsQuietWhenNothingMoved: the second push of an unchanged setup
// writes nothing at all.
func TestChangedIsQuietWhenNothingMoved(t *testing.T) {
	dir := layout(t)
	files, _, err := Collect(dir, DefaultParts())
	if err != nil {
		t.Fatal(err)
	}
	remote := make(map[string]string, len(files))
	for _, f := range files {
		remote[RepoPath(f)] = f.Sum
	}
	write, remove := Changed(files, remote)
	if len(write) != 0 || len(remove) != 0 {
		t.Errorf("wrote %d and removed %d with nothing changed", len(write), len(remove))
	}
}

// TestCommitMessageNamesItsFiles says what git history will read.
func TestCommitMessageNamesItsFiles(t *testing.T) {
	f := File{Path: "inua/config.toml", Data: []byte("x"), Sum: BlobSum([]byte("x"))}
	msg := CommitMessage([]File{f}, []string{"inua/old.conf"})
	if !strings.HasPrefix(msg, "inua: back up the settings") {
		t.Errorf("subject: %q", msg)
	}
	if !strings.Contains(msg, "A\tinua/inua/config.toml") {
		t.Errorf("added file not named: %q", msg)
	}
	if !strings.Contains(msg, "D\tinua/old.conf") {
		t.Errorf("removed file not named: %q", msg)
	}
}

// TestParseRepo reads what people type into Settings.
func TestParseRepo(t *testing.T) {
	for in, want := range map[string]string{
		"lyricat/inua-settings":              "lyricat/inua-settings",
		"  lyricat/inua-settings  ":          "lyricat/inua-settings",
		"https://github.com/lyricat/backup":  "lyricat/backup",
		"https://github.com/lyricat/backup/": "lyricat/backup",
		"ssh://git.example.com/owner/backup": "", // an SSH address is not one we write through
		"lyricat":                            "",
		"a/b/c":                              "",
		"":                                   "",
	} {
		got, err := ParseRepo(in)
		if want == "" {
			if err == nil {
				t.Errorf("%q was accepted as %s", in, got)
			}
			continue
		}
		if err != nil {
			t.Errorf("%q: %v", in, err)
			continue
		}
		if got.String() != want {
			t.Errorf("%q: %s, want %s", in, got, want)
		}
	}
}

// fakeGitHub is enough of GitHub's API to push and pull a repository, with
// the refusals a wrong token really meets.
type fakeGitHub struct {
	mu      sync.Mutex
	files   map[string][]byte
	commits int
	token   string // the token it accepts
	canPush bool
	branch  string
	trees   map[string]map[string][]byte // by tree SHA, for base_tree
	blobs   map[string][]byte            // by blob SHA
}

func newFakeGitHub(token string) *fakeGitHub {
	return &fakeGitHub{
		files:   map[string][]byte{},
		token:   token,
		canPush: true,
		branch:  "main",
		trees:   map[string]map[string][]byte{},
		blobs:   map[string][]byte{},
	}
}

func (f *fakeGitHub) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	f.mu.Lock()
	defer f.mu.Unlock()
	if f.token != "" && r.Header.Get("Authorization") != "Bearer "+f.token {
		w.WriteHeader(http.StatusUnauthorized)
		json.NewEncoder(w).Encode(map[string]string{"message": "Bad credentials"})
		return
	}
	repo := "/repos/owner/name"
	switch {
	case r.URL.Path == repo:
		json.NewEncoder(w).Encode(map[string]any{
			"default_branch": f.branch,
			"permissions":    map[string]bool{"push": f.canPush},
		})

	case strings.HasPrefix(r.URL.Path, repo+"/git/ref/heads/"):
		if f.commits == 0 {
			w.WriteHeader(http.StatusNotFound)
			json.NewEncoder(w).Encode(map[string]string{"message": "Not Found"})
			return
		}
		json.NewEncoder(w).Encode(map[string]any{
			"object": map[string]string{"sha": "commit-" + itoa(f.commits)},
		})

	case r.URL.Path == repo+"/git/commits" && r.Method == http.MethodPost:
		var body struct {
			Message string   `json:"message"`
			Tree    string   `json:"tree"`
			Parents []string `json:"parents"`
		}
		json.NewDecoder(r.Body).Decode(&body)
		f.files = map[string][]byte{}
		for p, b := range f.trees[body.Tree] {
			f.files[p] = b
		}
		f.commits++
		json.NewEncoder(w).Encode(map[string]any{"sha": "commit-" + itoa(f.commits)})

	case r.URL.Path == repo+"/git/commits" || strings.HasPrefix(r.URL.Path, repo+"/git/commits/"):
		tree := "tree-" + itoa(f.commits)
		json.NewEncoder(w).Encode(map[string]any{"tree": map[string]string{"sha": tree}})

	case r.URL.Path == repo+"/git/trees" || strings.HasPrefix(r.URL.Path, repo+"/git/trees/"):
		if r.Method == http.MethodPost {
			var body struct {
				BaseTree string           `json:"base_tree"`
				Tree     []map[string]any `json:"tree"`
			}
			json.NewDecoder(r.Body).Decode(&body)
			next := map[string][]byte{}
			if body.BaseTree != "" {
				for p, b := range f.trees[body.BaseTree] {
					next[p] = b
				}
			}
			for _, e := range body.Tree {
				p, _ := e["path"].(string)
				if sha, ok := e["sha"].(string); ok {
					next[p] = f.blobs[sha]
				} else {
					delete(next, p)
				}
			}
			name := "tree-" + itoa(f.commits+1)
			f.trees[name] = next
			json.NewEncoder(w).Encode(map[string]any{"sha": name})
			return
		}
		// GET a tree, recursively.
		name := strings.TrimPrefix(r.URL.Path, repo+"/git/trees/")
		name = strings.Split(name, "?")[0]
		var entries []map[string]string
		for p := range f.files {
			entries = append(entries, map[string]string{"path": p, "type": "blob", "sha": BlobSum(f.files[p])})
		}
		json.NewEncoder(w).Encode(map[string]any{"tree": entries})

	case r.URL.Path == repo+"/git/blobs" || strings.HasPrefix(r.URL.Path, repo+"/git/blobs/"):
		sha := strings.TrimPrefix(r.URL.Path, repo+"/git/blobs/")
		if r.Method == http.MethodPost {
			var body struct {
				Content  string `json:"content"`
				Encoding string `json:"encoding"`
			}
			json.NewDecoder(r.Body).Decode(&body)
			data := mustBase64(body.Content)
			name := BlobSum(data)
			f.blobs[name] = data
			json.NewEncoder(w).Encode(map[string]any{"sha": name})
			return
		}
		json.NewEncoder(w).Encode(map[string]any{
			"content":  toBase64(f.blobs[sha]),
			"encoding": "base64",
		})

	case r.URL.Path == repo+"/git/refs" || strings.HasPrefix(r.URL.Path, repo+"/git/refs/"):
		if r.Method == http.MethodPatch {
			f.commits++
			w.WriteHeader(http.StatusOK)
			json.NewEncoder(w).Encode(map[string]any{"ok": true})
			return
		}
		f.commits++
		json.NewEncoder(w).Encode(map[string]any{"ok": true})

	default:
		w.WriteHeader(http.StatusNotFound)
		json.NewEncoder(w).Encode(map[string]string{"message": "Not Found"})
	}
}

func toBase64(b []byte) string { return base64.StdEncoding.EncodeToString(b) }

func mustBase64(s string) []byte {
	b, err := base64.StdEncoding.DecodeString(s)
	if err != nil {
		panic(err)
	}
	return b
}

func itoa(n int) string {
	if n == 0 {
		return "0"
	}
	var b []byte
	for n > 0 {
		b = append([]byte{byte('0' + n%10)}, b...)
		n /= 10
	}
	return string(b)
}

// TestPushWritesOnceThenStaysQuiet is the promise the feature makes: the
// first push carries everything, the next one says nothing.
func TestPushWritesOnceThenStaysQuiet(t *testing.T) {
	dir := layout(t)
	fake := newFakeGitHub("tok")
	srv := httptest.NewServer(fake)
	defer srv.Close()
	api := &API{Base: srv.URL, Client: srv.Client(), Token: "tok"}
	setup := Setup{Repo: "owner/name", Parts: []string{"settings", "style", "hyprland"}, Interval: "few", Enabled: true}

	first, err := Push(context.Background(), dir, setup, api)
	if err != nil {
		t.Fatal(err)
	}
	if first.Pushed == 0 || first.Commit == "" {
		t.Fatalf("first push wrote nothing: %+v", first)
	}
	if first.URL == "" {
		t.Error("no page for the backup")
	}

	second, err := Push(context.Background(), dir, setup, api)
	if err != nil {
		t.Fatal(err)
	}
	if second.Pushed != 0 || second.Removed != 0 {
		t.Errorf("a quiet push wrote %d and removed %d", second.Pushed, second.Removed)
	}
	if second.Commit != "" {
		t.Error("a quiet push made a commit")
	}
}

// TestPushCarriesAnEdit pushes a changed setting and nothing else.
func TestPushCarriesAnEdit(t *testing.T) {
	dir := layout(t)
	fake := newFakeGitHub("tok")
	srv := httptest.NewServer(fake)
	defer srv.Close()
	api := &API{Base: srv.URL, Client: srv.Client(), Token: "tok"}
	setup := Setup{Repo: "owner/name", Parts: []string{"settings", "style"}, Interval: "few"}

	if _, err := Push(context.Background(), dir, setup, api); err != nil {
		t.Fatal(err)
	}
	write(t, filepath.Join(dir, "inua/style.css"), "window { color: blue; }\n")
	res, err := Push(context.Background(), dir, setup, api)
	if err != nil {
		t.Fatal(err)
	}
	if res.Pushed != 1 {
		t.Errorf("wrote %d files, want only style.css", res.Pushed)
	}
	if got := string(fake.files["inua/inua/style.css"]); !strings.Contains(got, "blue") {
		t.Errorf("the edited file did not arrive: %q", got)
	}
}

// TestPushRemovesWhatIsGone: a theme deleted here goes from the repository,
// so a second computer does not keep it.
func TestPushRemovesWhatIsGone(t *testing.T) {
	dir := layout(t)
	fake := newFakeGitHub("tok")
	srv := httptest.NewServer(fake)
	defer srv.Close()
	api := &API{Base: srv.URL, Client: srv.Client(), Token: "tok"}
	setup := Setup{Repo: "owner/name", Parts: []string{"settings", "style"}, Interval: "few"}

	if _, err := Push(context.Background(), dir, setup, api); err != nil {
		t.Fatal(err)
	}
	if err := os.Remove(filepath.Join(dir, "inua/themes/nord.css")); err != nil {
		t.Fatal(err)
	}
	res, err := Push(context.Background(), dir, setup, api)
	if err != nil {
		t.Fatal(err)
	}
	if res.Removed != 1 {
		t.Errorf("removed %d, want 1", res.Removed)
	}
	if _, ok := fake.files["inua/inua/themes/nord.css"]; ok {
		t.Error("the deleted theme is still in the repository")
	}
}

// TestCheckNamesAWrongToken says at once what a bad token means, rather
// than at the first push hours later.
func TestCheckNamesAWrongToken(t *testing.T) {
	fake := newFakeGitHub("right")
	srv := httptest.NewServer(fake)
	defer srv.Close()

	wrong := &API{Base: srv.URL, Client: srv.Client(), Token: "wrong"}
	_, err := wrong.Check(context.Background(), Repo{"owner", "name"})
	if err == nil {
		t.Fatal("a wrong token was accepted")
	}
	if !strings.Contains(err.Error(), "Bad credentials") {
		t.Errorf("the refusal was not GitHub's own: %v", err)
	}
}

// TestCheckNamesAReadOnlyToken refuses a token that cannot write before a
// setup is saved.
func TestCheckNamesAReadOnlyToken(t *testing.T) {
	fake := newFakeGitHub("tok")
	fake.canPush = false
	srv := httptest.NewServer(fake)
	defer srv.Close()
	api := &API{Base: srv.URL, Client: srv.Client(), Token: "tok"}
	_, err := api.Check(context.Background(), Repo{"owner", "name"})
	if err == nil || !strings.Contains(err.Error(), "not write") {
		t.Fatalf("a read-only token was accepted: %v", err)
	}
}

// TestCheckReadsTheDefaultBranch: a repository whose default is not main is
// pushed to its own branch.
func TestCheckReadsTheDefaultBranch(t *testing.T) {
	fake := newFakeGitHub("tok")
	fake.branch = "trunk"
	srv := httptest.NewServer(fake)
	defer srv.Close()
	api := &API{Base: srv.URL, Client: srv.Client(), Token: "tok"}
	branch, err := api.Check(context.Background(), Repo{"owner", "name"})
	if err != nil {
		t.Fatal(err)
	}
	if branch != "trunk" {
		t.Errorf("branch %q, want trunk", branch)
	}
}

// TestSetupRoundTrip saves and reads a setup with its file mode.
func TestSetupRoundTrip(t *testing.T) {
	dir := t.TempDir()
	in := Setup{
		Repo: "owner/name", Branch: "main", Parts: []string{"style", "settings"},
		Interval: "daily", Enabled: true,
	}
	if err := SaveSetup(dir, in); err != nil {
		t.Fatal(err)
	}
	got, ok := LoadSetup(dir)
	if !ok {
		t.Fatal("the setup did not load")
	}
	if got.Repo != in.Repo || got.Interval != in.Interval || !got.Enabled {
		t.Errorf("got %+v", got)
	}
	if !slices.Equal(NormaliseParts(got.Parts), []string{"settings", "style"}) {
		t.Errorf("parts %v are not in Settings' order", got.Parts)
	}
	info, err := os.Stat(setupPath(dir))
	if err != nil {
		t.Fatal(err)
	}
	if perm := info.Mode().Perm(); perm != 0o600 {
		t.Errorf("mode %o, want 600: the file names a repository", perm)
	}
}

// TestSaveSetupRefusesWhatCannotWork: a bad repository, no parts, an unknown
// interval.
func TestSaveSetupRefusesWhatCannotWork(t *testing.T) {
	for name, s := range map[string]Setup{
		"no parts":    {Repo: "owner/name", Parts: nil, Interval: "few"},
		"bad repo":    {Repo: "nonsense", Parts: []string{"settings"}, Interval: "few"},
		"bad interval": {Repo: "owner/name", Parts: []string{"settings"}, Interval: "often"},
	} {
		if err := SaveSetup(t.TempDir(), s); err == nil {
			t.Errorf("%s was accepted", name)
		}
	}
}

// TestDueFollowsTheInterval says when the schedule pushes.
func TestDueFollowsTheInterval(t *testing.T) {
	dir := t.TempDir()
	s := Setup{Repo: "owner/name", Parts: []string{"settings"}, Interval: "daily", Enabled: true}
	now := time.Date(2026, 10, 17, 12, 0, 0, 0, time.UTC)

	if !Due(dir, s, now) {
		t.Error("a setup that never pushed is not due")
	}
	if err := SaveState(dir, State{Last: now.Add(-2 * time.Hour)}); err != nil {
		t.Fatal(err)
	}
	if Due(dir, s, now) {
		t.Error("pushed two hours ago, daily, is due")
	}
	if err := SaveState(dir, State{Last: now.Add(-25 * time.Hour)}); err != nil {
		t.Fatal(err)
	}
	if !Due(dir, s, now) {
		t.Error("pushed 25 hours ago, daily, is not due")
	}
	s.Enabled = false
	if Due(dir, s, now) {
		t.Error("a disabled setup is due")
	}
}

// TestDueRetriesAfterAFailure: a push that failed is tried again at once,
// not a day later.
func TestDueRetriesAfterAFailure(t *testing.T) {
	dir := t.TempDir()
	s := Setup{Repo: "owner/name", Parts: []string{"settings"}, Interval: "daily", Enabled: true}
	now := time.Now()
	if err := SaveState(dir, State{Last: now, Error: "the token expired"}); err != nil {
		t.Fatal(err)
	}
	if !Due(dir, s, now) {
		t.Error("a failed push is not retried")
	}
}

// TestPushRefusesWithNothingToCarry is a new computer's first attempt: the
// settings it has not written yet are said, not pushed empty.
func TestPushRefusesWithNothingToCarry(t *testing.T) {
	dir := t.TempDir()
	fake := newFakeGitHub("tok")
	srv := httptest.NewServer(fake)
	defer srv.Close()
	api := &API{Base: srv.URL, Client: srv.Client(), Token: "tok"}
	s := Setup{Repo: "owner/name", Parts: []string{"settings"}, Interval: "few"}
	_, err := Push(context.Background(), dir, s, api)
	if err == nil || !strings.Contains(err.Error(), "nothing to carry") {
		t.Fatalf("an empty setup pushed: %v", err)
	}
}
