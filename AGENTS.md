# Repository Snapshot (Nov 7, 2025)
- Source code lives in `src/genzolars/`; `__init__.py` imports polars as `_pl`,
  calls `patch_polars()`, and exposes both `pl` plus module-level attribute
  forwarding so `import genzolars as pl` works with zero extra setup alongside
  the CLI entry point `genzolars:main`.
- `_aliases.py` currently binds the following slang helpers onto
  `pl.DataFrame`, `pl.LazyFrame`, and their group-by objects: `yeet`,
  `vibe_check`, `glow_up`, `no_cap`, `slay`, `squad_up`, `link_up`,
  `slide_thru` (asof join), `disband`, `lowkey`, `periodt`, `send_it`,
  `its_giving`, `clout_check`, plus `main_character` on eager DataFrames and
  matching `no_cap`/`its_giving` group-by aggregations.
- Packaging is driven by `pyproject.toml` (`requires-python >=3.11`, Ruff
  `target-version = "py312"`, and the `genzolars` console script).

## Tests & Quality Gates
- Pytest suite resides in `tests/test_genzolars.py` and covers each alias,
  including lazy-frame guards for `send_it(prop=...)`.
- Run `uv run pytest` before committing; prefer descriptive behavior-based
  test names and keep fixtures under `tests/resources/` if new data is
  needed.
- Ruff (`uv run ruff check .` and `uv run ruff format .`) plus the existing
  `pre-commit` configuration must stay green; install hooks with
  `pre-commit install`.

## Dev Workflow
- Use `uv run python -m genzolars` to exercise the CLI exactly as it ships
  (prints "GenZ polars aliases loaded..." today).
- Keep new runtime modules under `src/genzolars/` so `uv` packaging sees
  them, and mirror that structure under `tests/` with `test_*.py` names.
- Configuration roots (`pyproject.toml`, `uv.lock`, `.pre-commit-config.yaml`)
  live at the repo top level; update them alongside any code they affect.

## Style & Collaboration
- Target Python 3.12 syntax/typing but stay compatible with the declared
  runtime floor (3.11+). Follow 4-space indentation, 79-character lines, and
  concise imperative docstrings (even though Ruff currently ignores the D10x
  checks listed in the config).
- Favor expressive, slang-aligned public APIs, while keeping implementation
  helpers descriptive and snake_case.
- Commits: imperative subjects (50–72 chars) with wrapped bodies and any
  `Refs #issue` context. PRs should explain user-facing changes, document
  test commands, and attach screenshots or sample CLI output whenever
  behavior shifts.
