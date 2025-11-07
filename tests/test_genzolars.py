"""Regression tests for the genzolars slang extensions."""

from __future__ import annotations

import pytest
from polars.testing import assert_frame_equal, assert_series_equal

import genzolars as pl


def _sample_frame() -> pl.DataFrame:
    """Create a tiny leaderboard for use across multiple tests."""
    return pl.DataFrame(
        {
            "name": ["A", "B", "C"],
            "score": [4, 2, 9],
            "team": ["x", "y", "x"],
        }
    )


def test_yeet_and_vibe_check() -> None:
    """Ensure yeet filtering and vibe_check selections behave like Polars."""
    df = _sample_frame().yeet(pl.col("score") > 3).vibe_check("name", "score")
    expected = pl.DataFrame({"name": ["A", "C"], "score": [4, 9]})
    assert_frame_equal(df, expected)


def test_glow_up_and_main_character() -> None:
    """Verify glow_up adds columns and main_character pulls series."""
    df = _sample_frame().glow_up(new_score=pl.col("score") * 10)
    assert "new_score" in df.columns
    series = df.main_character("new_score")
    assert_series_equal(series, pl.Series("new_score", [40, 20, 90]))


def test_squad_up_and_no_cap() -> None:
    """Check grouped aggregations via squad_up().no_cap()."""
    result = (
        _sample_frame()
        .squad_up("team")
        .no_cap(pl.col("score").sum().alias("total"))
    )
    expected = pl.DataFrame({"team": ["x", "y"], "total": [13, 2]})
    assert_frame_equal(result, expected)


def test_periodt_and_its_giving() -> None:
    """Confirm unique extraction and counting helpers."""
    unique = _sample_frame().periodt("team")
    assert_frame_equal(unique, pl.DataFrame({"team": ["x", "y"]}))

    counts = _sample_frame().its_giving("team")
    expected = pl.DataFrame(
        {
            "team": ["x", "y"],
            "n": pl.Series("n", [2, 1], dtype=pl.UInt32),
        }
    )
    assert_frame_equal(counts, expected)


def test_slay_and_send_it_and_lazy_guard() -> None:
    """Exercise sort/slice helpers and lazy guards for send_it."""
    sliced = _sample_frame().slay("score", descending=True).send_it(prop=0.5)
    expected = pl.DataFrame(
        {
            "name": ["C", "A"],
            "score": [9, 4],
            "team": ["x", "x"],
        }
    )
    assert_frame_equal(sliced, expected)

    lf = _sample_frame().lazy()
    with pytest.raises(ValueError):
        lf.send_it(prop=0.5)

    with pytest.raises(ValueError):
        _sample_frame().yeet()


def test_link_up_eager_and_lazy() -> None:
    """Cover eager and lazy join alias behavior."""
    left = pl.DataFrame(
        {
            "team": ["x", "x", "y"],
            "score": [4, 9, 2],
        }
    )
    right = pl.DataFrame(
        {
            "team": ["x", "y"],
            "coach": ["alex", "casey"],
        }
    )
    collab = left.link_up(right, on="team")
    expected = pl.DataFrame(
        {
            "team": ["x", "x", "y"],
            "score": [4, 9, 2],
            "coach": ["alex", "alex", "casey"],
        }
    )
    assert_frame_equal(collab, expected)

    right_offset = pl.DataFrame(
        {
            "squad": ["x", "z"],
            "mascot": ["lynx", "zebra"],
        }
    )
    left_join = left.link_up(
        right_offset,
        how="left",
        left_on="team",
        right_on="squad",
        suffix="_squad",
    )
    expected_left = pl.DataFrame(
        {
            "team": ["x", "x", "y"],
            "score": [4, 9, 2],
            "mascot": ["lynx", "lynx", None],
        }
    )
    assert_frame_equal(left_join, expected_left)

    lazy_result = (
        left.lazy()
        .link_up(
            right.lazy(),
            on="team",
            allow_parallel=False,
        )
        .collect()
    )
    assert_frame_equal(lazy_result, expected)


def test_slide_thru_and_clout_check() -> None:
    """Validate join_asof alias and row-index helper."""
    quotes = pl.DataFrame(
        {
            "ts": [1, 3, 5],
            "price": [10.0, 10.5, 11.0],
        }
    )
    trades = pl.DataFrame(
        {
            "ts": [2, 4, 6],
            "size": [100, 50, 75],
        }
    )
    matched = trades.slide_thru(
        quotes,
        on="ts",
        suffix="_quote",
        tolerance=2,
    )
    expected = pl.DataFrame(
        {
            "ts": [2, 4, 6],
            "size": [100, 50, 75],
            "price": [10.0, 10.5, 11.0],
        }
    )
    assert_frame_equal(matched, expected)

    quotes_groups = pl.DataFrame(
        {
            "ts": [1, 2, 3, 4],
            "price": [5.0, 6.0, 7.0, 8.0],
            "side": ["buy", "buy", "sell", "sell"],
        }
    )
    trades_groups = pl.DataFrame(
        {
            "ts": [2, 3, 4],
            "size": [10, 20, 30],
            "side": ["buy", "buy", "sell"],
        }
    )
    grouped = trades_groups.slide_thru(
        quotes_groups,
        left_on="ts",
        right_on="ts",
        by_left="side",
        by_right="side",
        allow_exact_matches=False,
        check_sortedness=False,
    )
    expected_grouped = pl.DataFrame(
        {
            "ts": [2, 3, 4],
            "size": [10, 20, 30],
            "side": ["buy", "buy", "sell"],
            "price": [5.0, 6.0, 7.0],
        }
    )
    assert_frame_equal(grouped, expected_grouped)

    counted = trades.clout_check(name="row_id", offset=5)
    expected_counts = trades.with_row_index(name="row_id", offset=5)
    assert_frame_equal(counted, expected_counts)

    lazy_counts = trades.lazy().clout_check().collect()
    assert_frame_equal(lazy_counts, trades.with_row_index(name="row_nr"))

    lazy_join = (
        trades.lazy()
        .slide_thru(
            quotes.lazy(),
            on="ts",
            check_sortedness=False,
        )
        .collect()
    )
    assert_frame_equal(lazy_join, matched)
