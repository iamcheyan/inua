package backup

import (
	"bytes"
	"context"
	"encoding/base64"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"path"
	"slices"
	"strconv"
	"strings"
	"time"
)

// maxBody bounds what is read from GitHub for one request.
const maxBody = 32 << 20

// API is GitHub's REST API, the part this needs: a repository's default
// branch, its tree, blobs, commits and a reference to move.
//
// GitHub is the API a person's own repository is written through.
type API struct {
	Base   string // "https://api.github.com"; tests point it elsewhere
	Client *http.Client
	// Token is a fine-grained personal access token with Contents: read
	// and write on the one repository. It is kept in the Secret Service,
	// never in a settings file.
	Token string
}

// GitHub is the API at api.github.com, or at $INUA_BACKUP_API when the
// session sets one: a GitHub Enterprise install, or a test's own server.
func GitHub(token string) *API {
	base := os.Getenv("INUA_BACKUP_API")
	if base == "" {
		base = "https://api.github.com"
	}
	return &API{Base: base, Client: http.DefaultClient, Token: token}
}

// Repo is a repository's owner and name.
type Repo struct{ Owner, Name string }

// ParseRepo reads "owner/name", or the web address of the repository.
func ParseRepo(s string) (Repo, error) {
	s = strings.TrimSpace(s)
	// An SSH address (git at a host, then a path) is not one GitHub's API
	// writes through: refuse it rather than guess.
	if strings.Contains(s, "://") && !strings.HasPrefix(s, "http") {
		return Repo{}, fmt.Errorf("%q: use the repository's web address or owner/name; only the HTTP API can be written through", s)
	}
	if strings.Contains(s, "@") && strings.Contains(s, ":") && !strings.Contains(s, "://") {
		return Repo{}, fmt.Errorf("%q: use the repository's web address or owner/name; an SSH address cannot be written through GitHub's API", s)
	}
	s = strings.TrimSuffix(s, ".git")
	if u, err := url.Parse(s); err == nil && (u.Scheme == "http" || u.Scheme == "https") {
		s = strings.TrimPrefix(u.Path, "/")
	}
	s = strings.Trim(s, "/")
	parts := strings.Split(s, "/")
	if len(parts) != 2 || parts[0] == "" || parts[1] == "" {
		return Repo{}, fmt.Errorf("%q: want owner/name, the repository's address", s)
	}
	return Repo{Owner: parts[0], Name: parts[1]}, nil
}

func (r Repo) String() string { return r.Owner + "/" + r.Name }

// do sends one request and decodes the answer into out when it is not nil.
// A 404 is ErrNotFound, so a caller can tell "no such file yet" from a
// failure.
func (a *API) do(ctx context.Context, method, endpoint string, body, out any) error {
	var reader io.Reader
	if body != nil {
		b, err := json.Marshal(body)
		if err != nil {
			return err
		}
		reader = bytes.NewReader(b)
	}
	req, err := http.NewRequestWithContext(ctx, method, a.Base+endpoint, reader)
	if err != nil {
		return err
	}
	req.Header.Set("Accept", "application/vnd.github+json")
	req.Header.Set("X-GitHub-Api-Version", "2022-11-28")
	if a.Token != "" {
		req.Header.Set("Authorization", "Bearer "+a.Token)
	}
	if body != nil {
		req.Header.Set("Content-Type", "application/json")
	}
	client := a.Client
	if client == nil {
		client = http.DefaultClient
	}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	data, err := io.ReadAll(io.LimitReader(resp.Body, maxBody))
	if err != nil {
		return err
	}
	if resp.StatusCode == http.StatusNotFound {
		return ErrNotFound
	}
	if resp.StatusCode/100 != 2 {
		return fmt.Errorf("%s %s: %s: %s", method, endpoint, resp.Status, githubMessage(data))
	}
	if out != nil {
		if err := json.Unmarshal(data, out); err != nil {
			return fmt.Errorf("%s %s: %w", method, endpoint, err)
		}
	}
	return nil
}

// githubMessage is GitHub's own explanation of a refusal, which says what
// to fix ("Bad credentials", "Resource not accessible by personal access
// token").
func githubMessage(data []byte) string {
	var e struct {
		Message string `json:"message"`
		Errors  []struct {
			Message string `json:"message"`
		} `json:"errors"`
	}
	if json.Unmarshal(data, &e) != nil || e.Message == "" {
		s := strings.TrimSpace(string(data))
		if len(s) > 200 {
			s = s[:200]
		}
		return s
	}
	var b strings.Builder
	b.WriteString(e.Message)
	for _, one := range e.Errors {
		if one.Message != "" {
			b.WriteString("; ")
			b.WriteString(one.Message)
		}
	}
	return b.String()
}

// ErrNotFound is GitHub's 404: the repository, the branch or the file is
// not there.
var ErrNotFound = errors.New("not found on GitHub")

// Check confirms the token may read and write the repository, and returns
// its default branch. It is what Settings runs before saving a setup, so a
// wrong token or a repository the token cannot write is said at once
// rather than at the first push.
func (a *API) Check(ctx context.Context, r Repo) (branch string, err error) {
	var repo struct {
		DefaultBranch string `json:"default_branch"`
		Private       bool   `json:"private"`
		Permissions   struct {
			Push bool `json:"push"`
		} `json:"permissions"`
	}
	if err := a.do(ctx, http.MethodGet, "/repos/"+r.String(), nil, &repo); err != nil {
		if errors.Is(err, ErrNotFound) {
			return "", fmt.Errorf("%s: no such repository, or the token cannot see it", r)
		}
		return "", err
	}
	if !repo.Permissions.Push {
		return "", fmt.Errorf("%s: the token may read this repository but not write it", r)
	}
	return orDefault(repo.DefaultBranch, "main"), nil
}

// orDefault is a default for GitHub's answer when it names no branch.
func orDefault(v, def string) string {
	if v == "" {
		return def
	}
	return v
}

// Tree is a repository's files at one commit, by path with their blob
// SHA-1, which is what Changed compares sums of.
type Tree map[string]string

// Head is the commit the branch points at, and its tree.
func (a *API) Head(ctx context.Context, r Repo, branch string) (commit, tree string, files Tree, err error) {
	var ref struct {
		Object struct {
			SHA string `json:"sha"`
		} `json:"object"`
	}
	err = a.do(ctx, http.MethodGet, "/repos/"+r.String()+"/git/ref/heads/"+url.PathEscape(branch), nil, &ref)
	if errors.Is(err, ErrNotFound) {
		// An empty repository has no branch yet: the first push makes it.
		return "", "", Tree{}, nil
	}
	if err != nil {
		return "", "", nil, err
	}
	commit = ref.Object.SHA
	var c struct {
		Tree struct {
			SHA string `json:"sha"`
		} `json:"tree"`
	}
	if err := a.do(ctx, http.MethodGet, "/repos/"+r.String()+"/git/commits/"+commit, nil, &c); err != nil {
		return "", "", nil, err
	}
	tree = c.Tree.SHA
	files, err = a.tree(ctx, r, tree)
	return commit, tree, files, err
}

// tree reads a tree recursively, keeping the blobs.
func (a *API) tree(ctx context.Context, r Repo, sha string) (Tree, error) {
	var t struct {
		Tree []struct {
			Path string `json:"path"`
			Type string `json:"type"`
			SHA  string `json:"sha"`
		} `json:"tree"`
		Truncated bool `json:"truncated"`
	}
	err := a.do(ctx, http.MethodGet, "/repos/"+r.String()+"/git/trees/"+sha+"?recursive=1", nil, &t)
	if err != nil {
		return nil, err
	}
	if t.Truncated {
		return nil, fmt.Errorf("%s: the repository's tree is too large to read in one request", r)
	}
	files := make(Tree, len(t.Tree))
	for _, e := range t.Tree {
		if e.Type == "blob" {
			files[e.Path] = e.SHA
		}
	}
	return files, nil
}

// Blobs reads files of a tree by path, for the ones this computer does not
// have: a part that arrived from another computer, or a copy to keep.
func (a *API) Blobs(ctx context.Context, r Repo, files Tree, want []string) (map[string][]byte, error) {
	out := make(map[string][]byte, len(want))
	for _, p := range want {
		sha, ok := files[p]
		if !ok {
			continue
		}
		var blob struct {
			Content  string `json:"content"`
			Encoding string `json:"encoding"`
		}
		if err := a.do(ctx, http.MethodGet, "/repos/"+r.String()+"/git/blobs/"+sha, nil, &blob); err != nil {
			return nil, err
		}
		if blob.Encoding != "base64" {
			return nil, fmt.Errorf("%s: unexpected blob encoding %q", p, blob.Encoding)
		}
		data, err := base64.StdEncoding.DecodeString(strings.ReplaceAll(blob.Content, "\n", ""))
		if err != nil {
			return nil, fmt.Errorf("%s: %w", p, err)
		}
		out[p] = data
	}
	return out, nil
}

// Push writes files and deletes paths in one commit on branch, creating the
// branch and the repository's first commit when they are not there. A push
// with nothing to write or remove does nothing and reports false.
func (a *API) Push(ctx context.Context, r Repo, branch string, write []File, remove []string, message string) (commit string, pushed bool, err error) {
	if len(write) == 0 && len(remove) == 0 {
		return "", false, nil
	}
	parent, tree, remote, err := a.Head(ctx, r, branch)
	if err != nil {
		return "", false, err
	}
	// The remote changed under us since the caller read it: push what it
	// still needs, so a push never resurrects a file another computer
	// removed.
	write, remove = Changed(write, remote)
	if len(write) == 0 && len(remove) == 0 {
		return parent, false, nil
	}

	entries := make([]map[string]any, 0, len(write)+len(remove))
	for _, f := range write {
		sha, err := a.blob(ctx, r, f.Data)
		if err != nil {
			return "", false, err
		}
		entries = append(entries, map[string]any{
			"path": RepoPath(f), "mode": "100644", "type": "blob", "sha": sha,
		})
	}
	for _, p := range remove {
		entries = append(entries, map[string]any{
			"path": p, "mode": "100644", "type": "blob", "sha": nil,
		})
	}

	body := map[string]any{"tree": entries}
	if tree != "" {
		body["base_tree"] = tree
	}
	var madeTree struct {
		SHA string `json:"sha"`
	}
	if err := a.do(ctx, http.MethodPost, "/repos/"+r.String()+"/git/trees", body, &madeTree); err != nil {
		return "", false, err
	}

	commitBody := map[string]any{"message": message, "tree": madeTree.SHA}
	if parent != "" {
		commitBody["parents"] = []string{parent}
	}
	var madeCommit struct {
		SHA string `json:"sha"`
	}
	if err := a.do(ctx, http.MethodPost, "/repos/"+r.String()+"/git/commits", commitBody, &madeCommit); err != nil {
		return "", false, err
	}

	if parent == "" {
		// The repository had no branch: make it, at this commit.
		ref := map[string]any{"ref": "refs/heads/" + branch, "sha": madeCommit.SHA}
		if err := a.do(ctx, http.MethodPost, "/repos/"+r.String()+"/git/refs", ref, nil); err != nil {
			return "", false, err
		}
		return madeCommit.SHA, true, nil
	}
	upd := map[string]any{"sha": madeCommit.SHA, "force": false}
	if err := a.do(ctx, http.MethodPatch, "/repos/"+r.String()+"/git/refs/heads/"+url.PathEscape(branch), upd, nil); err != nil {
		return "", false, err
	}
	return madeCommit.SHA, true, nil
}

// blob writes one file and returns its SHA-1.
func (a *API) blob(ctx context.Context, r Repo, data []byte) (string, error) {
	body := map[string]any{
		"content":  base64.StdEncoding.EncodeToString(data),
		"encoding": "base64",
	}
	var made struct {
		SHA string `json:"sha"`
	}
	if err := a.do(ctx, http.MethodPost, "/repos/"+r.String()+"/git/blobs", body, &made); err != nil {
		return "", err
	}
	return made.SHA, nil
}

// Pull reads the files of a part from the repository, for a computer that
// is setting itself up from another's copy.
func (a *API) Pull(ctx context.Context, r Repo, branch string, part Part) ([]File, error) {
	_, _, remote, err := a.Head(ctx, r, branch)
	if err != nil {
		return nil, err
	}
	prefix := Root + "/"
	var want []string
	for p := range remote {
		if !strings.HasPrefix(p, prefix) {
			continue
		}
		if belongsTo(strings.TrimPrefix(p, prefix), part) {
			want = append(want, p)
		}
	}
	slices.Sort(want)
	blobs, err := a.Blobs(ctx, r, remote, want)
	if err != nil {
		return nil, err
	}
	files := make([]File, 0, len(want))
	for _, p := range want {
		data := blobs[p]
		files = append(files, File{
			Path: strings.TrimPrefix(p, prefix),
			Data: data,
			Sum:  BlobSum(data),
		})
	}
	return files, nil
}

// belongsTo says whether a repository path is one of a part's.
func belongsTo(p string, part Part) bool {
	for _, rel := range part.Paths {
		if p == rel || strings.HasPrefix(p, rel+"/") {
			return true
		}
	}
	return false
}

// PushedAt is when the branch last changed, for Settings to show how long
// ago the backup ran.
func (a *API) PushedAt(ctx context.Context, r Repo, branch string) (time.Time, error) {
	var ref struct {
		Object struct {
			SHA string `json:"sha"`
		} `json:"object"`
	}
	if err := a.do(ctx, http.MethodGet, "/repos/"+r.String()+"/git/ref/heads/"+url.PathEscape(branch), nil, &ref); err != nil {
		return time.Time{}, err
	}
	var c struct {
		Committer struct {
			Date time.Time `json:"date"`
		} `json:"committer"`
	}
	if err := a.do(ctx, http.MethodGet, "/repos/"+r.String()+"/git/commits/"+ref.Object.SHA, nil, &c); err != nil {
		return time.Time{}, err
	}
	return c.Committer.Date, nil
}

// RateLimited says whether err is GitHub refusing for rate, which a
// scheduled push should wait out rather than report as a failure.
func RateLimited(err error) bool {
	var e interface{ Error() string }
	if !errors.As(err, &e) {
		return false
	}
	s := e.Error()
	return strings.Contains(s, "rate limit") || strings.Contains(s, "429") ||
		strings.Contains(s, "abuse")
}

// RetryAfter is how long a rate-limited push should wait: GitHub's own
// answer where the body carries it, else a minute.
func RetryAfter(err error) time.Duration {
	var e interface{ Error() string }
	if errors.As(err, &e) {
		for _, f := range strings.Fields(e.Error()) {
			if n, err := strconv.Atoi(strings.Trim(f, ",.;")); err == nil && n > 0 && n < 3600 {
				return time.Duration(n) * time.Second
			}
		}
	}
	return time.Minute
}

// WebURL is the page of the backup in a browser: the folder the files are
// written under.
func WebURL(r Repo, branch string) string {
	return "https://github.com/" + r.String() + "/tree/" + path.Join(branch, Root)
}
