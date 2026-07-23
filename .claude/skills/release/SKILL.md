---
name: release
description: Cut a release of this repo — bump the version in pyproject.toml, roll the CHANGELOG Unreleased section into a dated version, update the compare links, then tag after merge. Use when the user says "cut a release", "release vX.Y.Z", "bump the version", or "tag a version".
---

# Cut a release

## 1. Preconditions

- Working tree clean, `main` up to date with `origin/main`.
- `make lint`, `make typecheck`, `make test` pass locally.

## 2. Pick the version

SemVer, judged from the `Unreleased` section of `CHANGELOG.md`: breaking change → major, new feature → minor, fixes only → patch. Confirm with the user if ambiguous.

## 3. Release commit (on a branch)

On `release/vX.Y.Z` off `main`:

1. `pyproject.toml`: set `version = "X.Y.Z"`.
2. `CHANGELOG.md`:
   - Rename `## [Unreleased]` to `## [X.Y.Z] - <today, YYYY-MM-DD>` and drop its empty subsections.
   - Insert a fresh empty `## [Unreleased]` skeleton above it (Added / Changed / Deprecated / Removed / Fixed / Security).
   - Update the link refs at the bottom: `[Unreleased]` compares `vX.Y.Z...HEAD`; add `[X.Y.Z]` comparing the previous tag to `vX.Y.Z` (first release links to the tag instead).
3. Commit `chore(release): vX.Y.Z`, push, open a PR to `main`, get it merged.

## 4. Tag and publish

After the merge, on updated `main`:

```bash
git tag -a vX.Y.Z -m "vX.Y.Z"
git push origin vX.Y.Z
gh release create vX.Y.Z --title "vX.Y.Z" --notes-from-tag
```

Prefer pasting the CHANGELOG section as the release notes (`--notes-file`) when it is non-trivial.
