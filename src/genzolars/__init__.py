"""genzolars – polars but bussin."""

from __future__ import annotations

from typing import Any

import polars as _pl

from ._aliases import patch_polars

patch_polars()

pl = _pl
__all__ = ["patch_polars", "pl"]


def __getattr__(name: str) -> Any:
    return getattr(_pl, name)


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(dir(_pl)))
