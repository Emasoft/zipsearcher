# test/ conventions

## Layout

- The directory is `test/` (singular) — `pyproject.toml` sets `testpaths = ["test"]`. Don't create `tests/`.
- Mirror the `src/` package structure: `test/<package>/test_<module>.py`, each test package with an `__init__.py`.
- Fixtures live in `conftest.py` at the deepest level that covers their users: `test/<package>/conftest.py` first, root `test/conftest.py` only for cross-package fixtures.

## Style

- Fixtures are small builders that return real domain objects in a known state (construct, set fields, return). No autouse fixtures, no fixture factories.
- Prefer real objects over mocks; mock only at process boundaries (network, subprocess, clock).
- Group related behaviors in a `class Test<Behavior>`; plain functions are fine for simple modules.
- One behavior per test; the name carries the spec (`test_score_set_on_game_ended`). No docstrings or comments — names must be self-explanatory.
- Variations of a baseline object go through a module-private helper (`_BASE` constant + `_make(**overrides)` using `dataclasses.replace`), not through parametrize. Keep `@pytest.mark.parametrize` for genuine input matrices (seeds, sizes).
- Compare floats with `pytest.approx`.

## Running

- `make test` — whole suite with coverage (`--cov=src --cov-report=term-missing`).
- Narrower runs: `uv run pytest test/<package>/` or a single file.
- A new `src/` module without tests shows up immediately in term-missing.

## Template residue

- `test_entrypoint.py` covers the template's stub entrypoint — replace it as real code lands.
