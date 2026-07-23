# Python repository template

[![CI](https://github.com/fannijako/repo_template/actions/workflows/ci.yaml/badge.svg)](https://github.com/fannijako/repo_template/actions/workflows/ci.yaml)
[![Coverage Status](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://github.com/fannijako/repo_template)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

## Project Overview

Repository template for my Python projects.

Toolchain:
- **[uv](https://docs.astral.sh/uv/)** — environment & dependency management
- **[poetry-core](https://python-poetry.org/)** — PEP 517 build backend
- **[ruff](https://docs.astral.sh/ruff/)** — linting & formatting
- **pytest** — testing

## Dependencies

- python package 1
- python package 2

## Installation

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then sync the environment:

```bash
make sync
```

This creates `.venv/` and installs the project plus the `dev` and `test` groups.

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

The repo is Claude-ready:

- `CLAUDE.md` — operating guide for AI agents (commands, layout, gotchas); `test/CLAUDE.md` adds test conventions.
- `.claude/settings.json` — shared permission allowlist (`make` / `uv` commands).
- `.claude/skills/adopt-template/` — bootstraps a fresh copy of this template (sweeps placeholders, then deletes itself).
- `.claude/skills/release/` — cuts a release (version bump, CHANGELOG roll, tag).

Personal overrides belong in `.claude/settings.local.json` / `CLAUDE.local.md` (gitignored).

## Usage

Create a `.env` file with the variables your app needs:

```bash
KEY_NAME=key_value
```

Then:

```bash
make sync
make run
```
