---
name: adopt-template
description: De-template-ize a repository freshly created from fannijako/repo_template — sweep the placeholders in pyproject.toml, README.md, CHANGELOG.md, and CLAUDE.md, remove the template's own MAINTENANCE.md backlog, verify nothing template-shaped remains, then delete this skill. Use when a repo was just created from the template, or the user says "bootstrap this repo", "created from the template", or "de-template-ize".
---

# Adopt the template

Turn a fresh copy of `fannijako/repo_template` into a real project. Work on a feature branch off `main` — never commit this straight to `main`.

## 1. Find the residue

```bash
grep -rn --exclude-dir=.git --exclude-dir=.venv -i -e repo_template -e "python package" -e KEY_NAME .
```

Every hit must be updated or consciously kept. Trust the grep over this table if they disagree:

| File | Placeholder | Replace with |
|---|---|---|
| `pyproject.toml` | `name = "repo_template"` | repo name |
| `pyproject.toml` | `description = "Repository template…"` | one-line real description |
| `pyproject.toml` | `[project.urls] Homepage` | real repo URL |
| `README.md` | title + "Repository template for my Python projects" | project overview — what & why |
| `README.md` | coverage badge link URL | real repo URL |
| `README.md` | Dependencies section ("python package 1/2") | real or planned deps, or drop the section |
| `README.md` | `.env` example `KEY_NAME=key_value` | the project's real env vars |
| `CHANGELOG.md` | the template's release history (`[0.1.0] - 2026-07-22` and its entries) | reset to the child's own `## [0.1.0] - <initial commit date>` with "Initial release (from `repo_template`)" |
| `CHANGELOG.md` | compare/tag URLs → `repo_template` | real repo URL |
| `CLAUDE.md` | template note under the title | delete the blockquote |
| `CLAUDE.md` | `## Project specifics` section | real env vars, services, infra facts |
| `MAINTENANCE.md` | whole file — the template repo's own backlog | `git rm`; record under CHANGELOG `Removed` |

Leave alone (generic, no placeholders): `Makefile`, `.github/`, `.pre-commit-config.yaml`, `test/CLAUDE.md`, `.claude/settings.json`, the `release` skill, `LICENSE` (re-license consciously if the project needs it), `src/entrypoint.py` stub and `test/test_entrypoint.py` (replace both as real code lands). Hits inside `.claude/skills/adopt-template/` are self-referential — they disappear in step 4.

## 2. Project-specific defaults

- CHANGELOG `Unreleased`: note the re-purposing.
- `.gitignore`: add project artifact dirs (e.g. `data/`) if the project plan defines them.
- Keep `dependencies = []` in pyproject until code actually lands.

## 3. Verify

```bash
python3 -c "import tomllib; tomllib.load(open('pyproject.toml','rb'))"
```

Re-run the step-1 grep — remaining hits must all be deliberate (e.g. CHANGELOG "Initial release (from `repo_template`)"). Run `make lint` if a venv exists.

## 4. Delete this skill

```bash
git rm -r .claude/skills/adopt-template
```

It has done its job; the `release` skill stays.

## 5. Ship

Commit on the feature branch, open a PR to `main`.
