# zipsearcher

[![CI](https://github.com/Emasoft/zipsearcher/actions/workflows/ci.yaml/badge.svg)](https://github.com/Emasoft/zipsearcher/actions/workflows/ci.yaml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

## Project Overview

`zipsearcher` searches for files by **name** inside one or more `.zip` archives
**without decompressing** them. It reads only the zip **central directory** (the
index of entry names and sizes stored at the end of every archive), so it stays
fast and cheap even on very large archives — no member payload is ever inflated.

Stdlib only, no third-party dependencies.

## Installation

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then sync the environment:

```bash
make sync
```

This creates `.venv/` and installs the project plus the `dev` and `test` groups.
The `zipsearcher` console script is installed as part of the project.

## Usage

```
zipsearcher [OPTIONS] PATTERN ARCHIVE [ARCHIVE ...]
```

`PATTERN` is matched against each entry inside the archive. By default it is an
`fnmatch` glob matched against the entry's **basename**.

| Option | Effect |
|---|---|
| `--path` | match against the full internal path instead of the basename |
| `-i`, `--ignore-case` | case-insensitive match |
| `--regex` | treat `PATTERN` as a Python regex instead of a glob |
| `-R`, `--recursive` | any `ARCHIVE` that is a directory is walked for `*.zip` |
| `-l`, `--files-with-matches` | print only archive paths that contain at least one match |
| `-c`, `--count` | print `archive.zip:N` counts |
| `--size` | append the entry's uncompressed size to each match line |
| `-0`, `--null` | NUL-separate output records (for `xargs -0`) |

Exit codes are grep-like: `0` matches found, `1` no matches, `2` an error
occurred (unreadable/bad archive) and no matches.

## Examples

Find every `.py` file across two archives (basename glob):

```bash
$ zipsearcher '*.py' project.zip vendor.zip
project.zip:src/app.py
project.zip:src/util.py
vendor.zip:lib/pkg/__init__.py
```

Match on the full internal path, case-insensitively:

```bash
$ zipsearcher --path -i 'DOCS/*.md' project.zip
project.zip:docs/readme.md
```

Use a regex and show uncompressed sizes:

```bash
$ zipsearcher --regex --size '^log\d+\.txt$' logs.zip
logs.zip:log01.txt:2048
logs.zip:log02.txt:4096
```

Count matches per archive, recursively over a directory tree:

```bash
$ zipsearcher -R -c '*.png' ./assets
assets/ui.zip:12
assets/icons/set.zip:37
```

List only the archives that contain a match, NUL-separated for `xargs -0`:

```bash
$ zipsearcher -l -0 'secret*' *.zip | xargs -0 ls -l
```

## Common tasks

```bash
make lint          # ruff check
make format        # ruff format (in place)
make format-check  # ruff format --check
make typecheck     # mypy (strict)
make test          # pytest with coverage
make pre-commit    # all pre-commit hooks on all files
make run           # python main.py
make clean         # remove .venv and caches
```

## Claude Code

- `CLAUDE.md` — operating guide for AI agents (commands, layout, gotchas); `test/CLAUDE.md` adds test conventions.
- `.claude/settings.json` — shared permission allowlist (`make` / `uv` commands).
- `.claude/skills/release/` — cuts a release (version bump, CHANGELOG roll, tag).

Personal overrides belong in `.claude/settings.local.json` / `CLAUDE.local.md` (gitignored).
