# genzolars
---
> polars but make it bussin fr fr no cap

## What is this?
`genzolars` is a tiny shim that patches Polars the moment you import it (or run the `genzolars` console script). Every row op, column select, join, or group-by suddenly speaks fluent Gen Z, and you can even `import genzolars as pl` to access the full Polars surface straight from this package.

## Installation
### Direct from GitHub
Add to a uv project:
```bash
uv add git+https://github.com/wfondrie/genzolars
```

Or install with pip:
```bash
pip install git+https://github.com/wfondrie/genzolars
```

### Check the CLI vibes
```bash
uv run python -m genzolars
# -> GenZ polars aliases loaded. Import polars and cook.
```
The CLI bootstraps the patching process—no flags, args, or subcommands
yet. Think of it as a smoke test: once you see the banner, your environment is
ready to `import genzolars as pl` in notebooks, scripts, or the REPL and start
calling the slang APIs immediately.

## The translation guide
| Polars API | genzolars slang | Why it fits |
|------------|----------------|-------------|
| `filter` | `yeet` | Toss the rows that fail the vibe check |
| `select` / `with_columns(select-only)` | `vibe_check` / `glow_up` | Keep only the columns that matter or give them a makeover |
| `with_columns` | `glow_up` | Transform your data into its best self |
| `select` | `no_cap` (on group-bys) | Tell the truth with fresh aggregations |
| `sort` | `slay` | Rank by pure slay factor |
| `group_by` | `squad_up` | Assemble squads before the ops |
| `join` (all flavors) | `link_up` | Merge tables and keep your day-ones close |
| `join_asof` | `slide_thru` | Slide into the nearest timestamp’s DMs |
| `rename` | `lowkey` | Sneak in new column names |
| `unique` | `periodt` | Drop dupes, periodt |
| `slice` | `send_it` | Grab the top chunk and send it |
| `count` | `its_giving` | Count how many vibes are detected |
| `with_row_index` | `clout_check` | Add row IDs to track who’s getting clout |
| `pull` | `main_character` | Make a column the star of the show |
| `group_by().agg` | `squad_up(...).no_cap` | Summaries but honest |

## Examples that slap
### Basic workflow
```python
import genzolars as pl

snacks = pl.DataFrame(
    {
        "snack": ["takis", "mochi", "celery", "hot cheetos"],
        "heat": [9, 6, 1, 10],
        "crunch": [8, 7, 2, 9],
    }
)

top_spice = (
    snacks
    .yeet(pl.col("heat") >= 6)
    .glow_up(drip=pl.col("crunch") * pl.col("heat"))
    .slay("drip", descending=True)
    .send_it(3)
)
print(top_spice)
```

### Grouped summaries
```python
import genzolars as pl

streams = pl.DataFrame(
    {
        "artist": ["SZA", "SZA", "Charli", "Charli", "SZA"],
        "track": ["Kill Bill", "Snooze", "360", "Von dutch", "Notice Me"],
        "streams": [120, 95, 80, 60, 70],
    }
)

leaderboard = (
    streams
    .squad_up("artist")
    .no_cap(total=pl.col("streams").sum(), avg=pl.col("streams").mean())
    .its_giving()
    .slay("n", descending=True)
)
print(leaderboard)
```

### Timestamp linking & row clout
```python
import genzolars as pl

drop_schedule = pl.DataFrame(
    {
        "ts": [1, 3, 5],
        "fit": ["grunge", "cozy", "y2k"],
    }
)
photo_dump = pl.DataFrame(
    {
        "ts": [2, 4, 6],
        "likes": [420, 380, 610],
    }
)

synced = (
    photo_dump.slide_thru(drop_schedule, on="ts", tolerance=2)
    .clout_check(name="post_id")
    .slay("likes", descending=True)
)
print(synced)
```

### CLI vibes
```bash
uv run python -m genzolars
# -> GenZ polars aliases loaded. Import polars and cook.
```
## Why tho?
Because data tooling should be fun. Toss some `yeet()`s into your notebooks, get a laugh in code review, and still ship legit Polars pipelines. Inspired by the `genzplyr` R package’s energy, but now for Pythonic dataframes.

## Slang glossary
- **Bussin** – extremely good
- **Fr fr** – for real, for real (emphasis)
- **No cap** – no lie
- **Yeet** – throw it out
- **Vibe check** – see if it passes the mood
- **Glow up** – step up your look
- **Slay** – do it flawlessly
- **Squad** – your group
- **Lowkey** – on the down-low
- **Periodt** – end of discussion, emphasis
- **Main character** – the focal point
- **Send it** – commit fully
- **It’s giving…** – the vibe it’s channeling
- **Clout** – social status / attention

## Contributing
Pull requests, new slang ideas, and docs edits are all welcome. Please run:
```bash
uv run pytest
uv run ruff check .
```
before pushing so CI stays chill.

## License
MIT – remix however you want, just keep it fun.
