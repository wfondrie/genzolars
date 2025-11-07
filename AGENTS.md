# Repository Guidelines

## Project Structure & Module Organization
- Source lives in `src/genzolars`, exposed via the `genzolars:main` entry point defined in `pyproject.toml`. Keep new modules under this package so `uv` picks them up automatically.
- Tests belong in `tests/` using `test_*.py` files that mirror the layout inside `src/`. If you add fixtures or sample data, place them under `tests/resources` to keep imports clean.
- Configuration roots (e.g., `pyproject.toml`, `uv.lock`, `.pre-commit-config.yaml`) sit in the repository top level; update them in the same commit as the code they affect.

## Build, Test, and Development Commands
- `uv run python -m genzolars` — launch the CLI exactly as end users will.
- `uv run pytest` — execute the full test suite; use `-k` or `-m` selectors locally when iterating, but run the full suite before pushing.
- `uv run ruff check .` and `uv run ruff format .` — lint and auto-format; CI assumes a clean run of both commands.
- `pre-commit run --all-files` — mirrors CI hook coverage (imports, formatting, trailing whitespace) so run it before opening a PR.

## Coding Style & Naming Conventions
- Target Python 3.12 syntax and type hints; stick to 4-space indentation and a 79-character line length (see `[tool.ruff]`).
- Prefer expressive, slang-aligned API names externally, but keep internal helpers descriptive and snake_case.
- Docstrings should be concise, even though Ruff currently ignores D100/D203/D213/D401; keep summaries imperative to stay consistent.

## Testing Guidelines
- Use `pytest` with plain asserts; favor fixtures for DataFrame builders so slang transformations stay reusable.
- Name tests after behavior, e.g., `test_filter_hits_different`; place integration flows under `tests/test_cli.py`.
- Aim for high-coverage paths touching both the Gen Z aliases and the underlying Polars calls; add regression tests whenever you add a new alias or behavior flag.

## Commit & Pull Request Guidelines
- Write imperative, 50–72 character commit subjects (`Add drip_join helper`), followed by wrapped body text explaining context plus any `Refs #issue` tags.
- Each PR should describe the user-facing change, list testing commands run, and attach screenshots or sample outputs if CLI behavior changes.
- Keep PRs scoped (one feature or bug-fix); draft PRs are welcome while APIs are still bussin.
