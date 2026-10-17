# Backup

`inua backup` carries the settings that make a desktop yours to a GitHub
repository, on a schedule, so the next computer starts with them too.

What travels is a folder of plain files, not a sealed archive: the
repository holds the same text you would edit, so it can be read, compared
and repaired by hand. The token that writes it is not among them; it stays
in the Secret Service (`inua-keyring`).

## The parts

Each part is chosen on Settings → Backup.

| Part | What it carries | Where it goes in the repository |
| --- | --- | --- |
| `settings` | `config.toml`, the shell's settings | `inua/inua/config.toml` |
| `style` | `style.css`, `themes/`, `icons/` | `inua/inua/style.css`, `inua/inua/themes/…` |
| `hyprland` | `hypr/inua.conf` and `hypr/inua.lua`, the Hyprland settings inua writes | `inua/hypr/…` |
| `apps` | the light apps' own state, `inua/apps/` | `inua/inua/apps/…` |
| `assistant` | the assistant's profiles | `inua/inua/assistant/…` |

Everything is written under `inua/` in the repository, so a repository may
hold other things beside it; nothing outside that folder is ever removed.

A part with no file yet — a new computer that has not changed its theme —
is named once and skipped, not written empty and not an error.

The assistant's conversations are never carried: they hold what people
typed, and `history/` is skipped even when the profiles are chosen.

## A push

The push reads the repository's tree, compares each file by git's own blob
name (SHA-1 over the file), and writes one commit for whatever differs:

- **A file that has not changed here since the last push is not written
  again.** A computer that keeps its settings says nothing at all; the
  repository does not fill with identical commits.
- **A file deleted here is deleted there**, so a second computer does not
  keep a theme that is gone.
- **A file changed on both sides keeps this computer's copy**, and the one
  it replaced is named in the commit message. The other computer's next push
  sees the change and carries it, so the two converge.

One request per file, plus one tree and one commit: a settings folder is a
few dozen small files, well inside GitHub's limits.

## The schedule

Settings → Backup turns it on and picks the interval (hourly, every few
hours, once a day, once a week). The shell checks every five minutes and
pushes when the interval has passed, so an hour's interval is met within
five minutes of it, on a login that is already busy.

A failed push is retried at the next check rather than waiting out the
interval, and says so once in a notification: it means the settings stopped
being carried. A successful push is not announced — it is meant to be
quiet — but Settings says when it last ran and what it wrote.

`inua backup` with no argument says where things stand without touching the
network: the repository, the parts, the schedule, and what the last push
did.

## The token

A fine-grained personal access token with **Contents: read and write** on
the one repository is enough. Create it on GitHub (Settings → Developer
settings → Personal access tokens → Fine-grained tokens), scope it to the
repository, and paste it into Settings → Backup, or store it from a
terminal:

```sh
inua backup token        # reads it without echoing, keeps it in the keyring
inua backup token -delete
```

Settings → Backup's **Check the repository** asks GitHub whether the token
may write it before anyone waits for a scheduled push to say so: a wrong
token, a repository the token cannot see, and a token that may read but not
write are each named at once.

The token is stored under the label *inua: GitHub backup token* with the
attributes `application=inua`, `purpose=backup-github`,
`username=inua-backup`, so it can be found and removed with `pass` or any
Secret Service client. It is never written to `config.toml`, to
`backup.json`, or to the repository.

## Files

| Path | What |
| --- | --- |
| `$XDG_CONFIG_HOME/inua/backup.json` | the repository, branch, parts and interval (mode 600) |
| `$XDG_CONFIG_HOME/inua/backup-state.json` | when the last push ran, its commit, and any error |
| the Secret Service | the token, and nothing else |

A file of its own rather than `config.toml`: the settings window writes
`config.toml`, and a repository's schedule is not a shell setting. Deleting
`backup.json` turns the backup off and leaves the repository alone.

## The command line

```sh
inua backup                       # where things stand
inua backup parts                 # the parts, and which a new setup carries
inua backup push [--repo owner/name] [--token T] [--branch B] [--parts a,b]
inua backup pull [--repo owner/name] [--token T] [--branch B] [--parts a,b]
inua backup token [-delete]
```

`push` and `pull` take a repository, token and branch for one run, over the
saved setup, so a first push needs no Settings visit:

```sh
inua backup push --repo your-name/inua-settings
```

`pull` writes only what is not here. A file this computer already has and
has changed is kept, and named:

```
inua: inua/style.css: kept this computer's copy
```

That is what makes a pull safe to run on a computer someone has been using.

`$INUA_BACKUP_API` points the client at a GitHub Enterprise install, or at a
test's own server, instead of `https://api.github.com`.

## Limits

- A push compares whole files, not lines: two computers that edit the same
  file between pushes converge on whichever pushed last, and the replaced
  copy is named in the commit rather than merged.
- A repository whose tree is too large to read in one request (over 100,000
  entries) is refused rather than pushed blind.
- Nothing is encrypted. The repository must be private; a public one would
  publish the desktop's settings.
- Removing a part from the setup does not remove its files from the
  repository: a part no longer chosen is left as it was, so turning a part
  off and on again does not have to re-upload it.
