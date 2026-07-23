# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [0.1.0] - 2026-07-22

### Added

- Initial release: uv + poetry-core packaging, ruff lint/format, strict mypy, pytest with coverage, 4-job CI with a 3.10–3.13 test matrix, dependabot, pre-commit.
- Claude Code support: root and `test/` `CLAUDE.md`, shared `.claude/settings.json` permission allowlist, and repo skills `adopt-template` and `release`.
- MIT `LICENSE`.
- Real tests for `src/entrypoint.py` (replacing the `test_fake.py` placeholder); coverage measured at 100%.
- CI and license badges in the README.

### Changed

- `[dependency-groups]` floors re-synced with `[project.optional-dependencies]`, and a `build` group added so `make sync` installs the build/twine tooling.
- pre-commit hooks bumped to match the locked tool versions (ruff v0.15.22, mypy v2.3.0, pre-commit-hooks v6.0.0).
- CI installs dependencies with `uv sync --locked` so the lockfile is enforced.

### Fixed

- `make test` never ran pytest: `.PHONY` was assigned as a variable instead of declared as a target, so the `test/` directory shadowed the target.
- CI dependency resolution: `build>=1.5.1` became unsatisfiable after 1.5.1 was yanked from PyPI; relaxed to `build>=1.2.0`.
- README coverage badge overstated coverage (claimed 100% while the placeholder suite covered 0%); the suite now backs the badge.

[Unreleased]: https://github.com/fannijako/repo_template/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/fannijako/repo_template/releases/tag/v0.1.0
