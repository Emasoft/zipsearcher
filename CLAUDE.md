# CLAUDE.md

Operating guide for AI agents working in this repo. `README.md` covers what the project is; this file covers how to work on it.

> **Template note:** this repo was created from [fannijako/repo_template](https://github.com/fannijako/repo_template). While template placeholders remain, run the `adopt-template` skill (`.claude/skills/adopt-template/`) first.

## Toolchain

- **uv** — environment + dependencies. Never `pip install`; use `uv add` / `uv add --group dev`.
- **poetry-core** — PEP 517 build backend; packages declared in `[tool.poetry] packages` (currently `src`).
- **ruff** — lint + format, line length 127. **mypy** — strict mode. **pytest** — coverage on `src`.
- Python ≥ 3.10; CI tests 3.10–3.13.

## Commands

All work goes through the Makefile:

| Command | What it does |
|---|---|
| `make sync` | create `.venv`, install all dependency groups |
| `make lint` / `make format` / `make format-check` | ruff |
| `make typecheck` | mypy (strict; covers `src/` and `main.py`) |
| `make test` | pytest with coverage (term-missing) |
| `make pre-commit` | all pre-commit hooks on all files |
| `make run` | `python main.py` |

Lint, typecheck, and tests must pass locally before opening a PR.

## Layout

- `main.py` — thin launcher; the real entrypoint is `src/entrypoint.py:main`.
- `src/` — application code (the installable package).
- `test/` — pytest suite (singular, not `tests/`); conventions in `test/CLAUDE.md`.

## Gotchas

- Dev/test dependencies are declared twice in `pyproject.toml`: `[project.optional-dependencies]` (pip extras) and `[dependency-groups]` (what `uv sync --all-groups` installs). Keep both in sync when adding one.
- mypy is `strict = true` — new code needs full type annotations from the start.
- CI (`.github/workflows/ci.yaml`) runs the same ruff/mypy/pytest commands as the Makefile, so green locally ≈ green in CI.

## Conventions

- Conventional-commit style messages (`feat:`, `fix:`, `ci(deps):` …). Branch off `main`; never commit to `main` directly.
- User-visible changes go under `Unreleased` in `CHANGELOG.md` (Keep a Changelog).
- Releases: use the `release` skill (`.claude/skills/release/`).

## Project specifics

<!-- Filled in when adopting the template; the adopt-template skill sweeps this section. -->
- Environment variables: `KEY_NAME` — placeholder, see README Usage.
- External services / infrastructure: none yet.
