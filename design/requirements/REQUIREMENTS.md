# REQUIREMENTS — zipsearcher

CLI tool: search for files by NAME inside one or more `.zip` archives **without
decompressing** them — read only the zip **central directory**.

## Why / key implementation constraint
Python's `zipfile.ZipFile(path).infolist()` (and `.namelist()`) parse ONLY the
central directory record at the end of the archive. They do NOT read or inflate
any file payload. This tool MUST use those APIs and MUST NEVER call `.read()`,
`.open()`, or `.extract*()`. Add a code comment at the read site stating this is
why no decompression occurs. Fail-fast philosophy: on a corrupt archive, warn to
stderr and continue to the next archive.

## CLI
```
zipsearcher [OPTIONS] PATTERN ARCHIVE [ARCHIVE ...]
```
- `PATTERN` — matched against each entry inside the zip.
- Matching (default): `fnmatch` glob against the entry's **basename**.
  - `--path` — match against the full internal path instead of the basename.
  - `-i/--ignore-case` — case-insensitive match.
  - `--regex` — treat PATTERN as a Python regex (instead of glob).
- Inputs:
  - `-R/--recursive` — any ARCHIVE that is a directory is walked for `*.zip`.
- Output:
  - default: one line per match `archive.zip:internal/path`.
  - `-l/--files-with-matches` — print only archive paths that contain ≥1 match.
  - `-c/--count` — print `archive.zip:N` counts.
  - `--size` — append the entry's uncompressed size to each match line.
  - `-0/--null` — NUL-separate output records (for xargs -0).
- Exit codes (grep-like): `0` matches found, `1` no matches, `2` an error
  occurred (unreadable/bad archive) and no matches.

## Tests (real, no mocks — build fixture zips in-test with `zipfile`)
basename glob match; `--path` full-path match; `-i` case-insensitive; `--regex`;
no-match → exit 1; bad/corrupt zip → warning + exit 2; `-c` counts;
`-l` files-with-matches; `--size`; multiple archives; `-R` directory walk.
Every test function: one-line docstring describing intent.

## Packaging
Add to `pyproject.toml`: `[project.scripts]` → `zipsearcher = "src.entrypoint:main"`.
Keep `dependencies = []` (stdlib only) so `uv.lock` stays valid.
`README.md`: usage + examples. `CHANGELOG.md` Unreleased → Added.

## Acceptance
`make lint`, `make format-check`, `make typecheck` (mypy strict), `make test`
all green locally and in CI. Real example in README runs correctly.
