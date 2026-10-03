# extinction-db

Week 3 assignment. A small SQLite database of mass-extinction records, built
from source material, plus a skill that turns it into an agent.

## Files

| File | What it is |
|---|---|
| `schema.sql` | Table definition for `extinction_records` |
| `records.json` | Facts extracted from source material, one row per fact |
| `code/build_db.py` | Builds `data.db` from `schema.sql` + `records.json` |
| `data.db` | SQLite database (not committed) |
| `sources/` | Original source material |

## Build

```bash
python code/build_db.py
```

Uses only the Python standard library (`sqlite3`).

## Columns

| Column | Meaning |
|---|---|
| `id` | Primary key |
| `date` | Geological age, e.g. 奥陶纪末期，约4.43亿年前 |
| `fact` | Description of the extinction event |
| `names` | Related species / researchers |
| `places` | Fossil or stratigraphic sites |
| `source` | Original source (paper, authoritative paleontology database) |
