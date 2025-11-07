"""genzolars – polars but bussin."""

from __future__ import annotations

import sys
from typing import Any

import polars as _pl

from ._aliases import patch_polars

patch_polars()

pl = _pl
__all__ = ["patch_polars", "pl", "main"]


def __getattr__(name: str) -> Any:
    return getattr(_pl, name)


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(dir(_pl)))


def main() -> None:  # pragma: no cover - CLI shim
    """Emit the genzolars banner for `python -m` executions."""
    sys.stderr.write("GenZ polars aliases loaded. Import polars and cook.\n")
