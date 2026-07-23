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

## [1.0.0] - 2026-07-23

### Added

- Initial release: `zipsearcher` CLI that searches filenames inside zip archives by reading only the central directory (`zipfile.infolist()`), never decompressing any member.
- Matching options: `fnmatch` glob on the basename (default), `--path` for the full internal path, `-i/--ignore-case`, and `--regex` for Python regex patterns.
- Input options: `-R/--recursive` walks directory arguments for `*.zip`.
- Output options: default `archive:path` lines, `-l/--files-with-matches`, `-c/--count`, `--size`, and `-0/--null` NUL-separated records.
- Grep-like exit codes: `0` matches found, `1` no matches, `2` an error occurred and no matches.
- Real pytest suite building fixture zips in-test and covering every documented behavior.

### Removed

- The `repo_template` `MAINTENANCE.md` backlog and the one-shot `adopt-template` skill (template bootstrap complete).

[Unreleased]: https://github.com/Emasoft/zipsearcher/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Emasoft/zipsearcher/releases/tag/v1.0.0
