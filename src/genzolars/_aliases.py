"""Alias polars APIs with Gen Z slang."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from functools import reduce
from typing import Any

import polars as pl
from polars.dataframe import group_by as df_group_by
from polars.lazyframe import group_by as lazy_group_by

Frame = pl.DataFrame | pl.LazyFrame
GroupBy = df_group_by.GroupBy
LazyGroupBy = lazy_group_by.LazyGroupBy
GroupByLike = GroupBy | LazyGroupBy


def _ensure_expr(value: Any) -> pl.Expr:
    return value if isinstance(value, pl.Expr) else pl.lit(value)


def _combine_predicates(predicates: Sequence[Any]) -> pl.Expr:
    exprs = [_ensure_expr(p) for p in predicates]
    return reduce(lambda acc, expr: acc & expr, exprs[1:], exprs[0])


def _attach(cls: type, name: str, func: Callable[..., Any]) -> None:
    setattr(cls, name, func)


def _yeet(self: Frame, *predicates: Any) -> Frame:
    if not predicates:
        raise ValueError("yeet needs at least one predicate expression")
    predicate = (
        _combine_predicates(predicates)
        if len(predicates) > 1
        else _ensure_expr(predicates[0])
    )
    return self.filter(predicate)


def _vibe_check(self: Frame, *columns: Any, **named_columns: Any) -> Frame:
    coerced = {
        name: (expr if isinstance(expr, pl.Expr) else pl.lit(expr))
        for name, expr in named_columns.items()
    }
    return self.select(*columns, **coerced)


def _glow_up(self: Frame, *exprs: Any, **named_exprs: Any) -> Frame:
    return self.with_columns(*exprs, **named_exprs)


def _no_cap_frame(self: Frame, *exprs: Any, **named_exprs: Any) -> Frame:
    return self.select(*exprs, **named_exprs)


def _slay(
    self: Frame,
    by: Any,
    *,
    descending: bool | Sequence[bool] = False,
    nulls_last: bool = False,
    maintain_order: bool = False,
) -> Frame:
    return self.sort(
        by=by,
        descending=descending,
        nulls_last=nulls_last,
        maintain_order=maintain_order,
    )


def _squad_up(
    self: Frame, *keys: Any, maintain_order: bool = True
) -> GroupByLike:
    return self.group_by(*keys, maintain_order=maintain_order)


def _link_up(
    self: Frame,
    other: Frame,
    on: Any | None = None,
    *,
    how: str = "inner",
    left_on: Any | None = None,
    right_on: Any | None = None,
    suffix: str = "_right",
    validate: str | None = None,
    nulls_equal: bool | None = None,
    coalesce: bool | None = None,
    maintain_order: Any | None = None,
    allow_parallel: bool | None = None,
    force_parallel: bool | None = None,
) -> Frame:
    join_kwargs: dict[str, Any] = {"how": how}
    if on is not None:
        join_kwargs["on"] = on
    if left_on is not None:
        join_kwargs["left_on"] = left_on
    if right_on is not None:
        join_kwargs["right_on"] = right_on
    if suffix is not None:
        join_kwargs["suffix"] = suffix
    if validate is not None:
        join_kwargs["validate"] = validate
    if nulls_equal is not None:
        join_kwargs["nulls_equal"] = nulls_equal
    if coalesce is not None:
        join_kwargs["coalesce"] = coalesce
    if maintain_order is not None:
        join_kwargs["maintain_order"] = maintain_order
    if isinstance(self, pl.LazyFrame):
        if allow_parallel is not None:
            join_kwargs["allow_parallel"] = allow_parallel
        if force_parallel is not None:
            join_kwargs["force_parallel"] = force_parallel
    return self.join(other, **join_kwargs)


def _slide_thru(
    self: Frame,
    other: Frame,
    *,
    left_on: Any | None = None,
    right_on: Any | None = None,
    on: Any | None = None,
    by_left: Any | None = None,
    by_right: Any | None = None,
    by: Any | None = None,
    strategy: str = "backward",
    suffix: str = "_right",
    tolerance: Any | None = None,
    allow_parallel: bool | None = None,
    force_parallel: bool | None = None,
    coalesce: bool | None = None,
    allow_exact_matches: bool | None = None,
    check_sortedness: bool | None = None,
) -> Frame:
    join_kwargs: dict[str, Any] = {
        "strategy": strategy,
        "suffix": suffix,
    }
    if left_on is not None:
        join_kwargs["left_on"] = left_on
    if right_on is not None:
        join_kwargs["right_on"] = right_on
    if on is not None:
        join_kwargs["on"] = on
    if by_left is not None:
        join_kwargs["by_left"] = by_left
    if by_right is not None:
        join_kwargs["by_right"] = by_right
    if by is not None:
        join_kwargs["by"] = by
    if tolerance is not None:
        join_kwargs["tolerance"] = tolerance
    if allow_parallel is not None:
        join_kwargs["allow_parallel"] = allow_parallel
    if force_parallel is not None:
        join_kwargs["force_parallel"] = force_parallel
    if coalesce is not None:
        join_kwargs["coalesce"] = coalesce
    if allow_exact_matches is not None:
        join_kwargs["allow_exact_matches"] = allow_exact_matches
    if check_sortedness is not None:
        join_kwargs["check_sortedness"] = check_sortedness
    return self.join_asof(other, **join_kwargs)


def _disband(self: Frame) -> Frame:
    return self


def _lowkey(
    self: Frame, mapping: Mapping[str, str] | None = None, /, **named: str
) -> Frame:
    rename_map: dict[str, str] = {}
    if mapping:
        rename_map.update(mapping)
    rename_map.update(named)
    return self.rename(rename_map)


def _periodt(self: Frame, *subset: str, maintain_order: bool = True) -> Frame:
    if subset:
        target = self.select(*subset)
    else:
        target = self
    return target.unique(maintain_order=maintain_order)


def _main_character(self: pl.DataFrame, column: str | int) -> pl.Series:
    if isinstance(column, int):
        column = self.columns[column]
    return self.select(column).to_series()


def _send_it(
    self: Frame,
    n: int | None = None,
    *,
    prop: float | None = None,
    offset: int = 0,
) -> Frame:
    if prop is not None and not isinstance(self, pl.LazyFrame):
        if not 0 < prop <= 1:
            raise ValueError("prop must be in (0, 1]")
        length = max(int(round(self.height * prop)), 1) if self.height else 0
    elif prop is not None:
        raise ValueError(
            "send_it with prop is only supported on eager DataFrames"
        )
    else:
        length = n if n is not None else 5
    return self.slice(offset, length)


def _its_giving(self: Frame, *columns: Any, sort_desc: bool = True) -> Frame:
    if columns:
        result = self.group_by(*columns, maintain_order=True).len()
    else:
        result = self.select(pl.len().alias("len"))
    renamed = (
        result.rename({"len": "n"}) if "len" in result.columns else result
    )
    return renamed.sort("n", descending=True) if sort_desc else renamed


def _clout_check(self: Frame, name: str = "row_nr", offset: int = 0) -> Frame:
    return self.with_row_index(name=name, offset=offset)


def _gb_no_cap(self: GroupByLike, *exprs: Any, **named_exprs: Any) -> Frame:
    return self.agg(*exprs, **named_exprs)


def _gb_its_giving(self: GroupByLike, sort_desc: bool = True) -> Frame:
    result = self.len().rename({"len": "n"})
    return result.sort("n", descending=True) if sort_desc else result


_PATCHED = False


def patch_polars() -> None:
    global _PATCHED
    if _PATCHED:
        return
    aliases = {
        "yeet": _yeet,
        "vibe_check": _vibe_check,
        "glow_up": _glow_up,
        "no_cap": _no_cap_frame,
        "slay": _slay,
        "squad_up": _squad_up,
        "link_up": _link_up,
        "slide_thru": _slide_thru,
        "disband": _disband,
        "lowkey": _lowkey,
        "periodt": _periodt,
        "send_it": _send_it,
        "its_giving": _its_giving,
        "clout_check": _clout_check,
    }
    for cls in (pl.DataFrame, pl.LazyFrame):
        for name, func in aliases.items():
            _attach(cls, name, func)
    _attach(pl.DataFrame, "main_character", _main_character)
    gb_aliases = {
        "no_cap": _gb_no_cap,
        "its_giving": _gb_its_giving,
    }
    for cls in (GroupBy, LazyGroupBy):
        for name, func in gb_aliases.items():
            _attach(cls, name, func)
    _PATCHED = True


__all__ = ["patch_polars"]
