import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "records.json"
SCHEMA = ROOT / "schema.sql"
DB = ROOT / "data.db"


def main():
    schema = SCHEMA.read_text(encoding="utf-8")
    records = json.loads(RECORDS.read_text(encoding="utf-8"))

    con = sqlite3.connect(DB)
    con.execute("DROP TABLE IF EXISTS extinction_records")
    con.executescript(schema)

    for r in records:
        con.execute(
            "INSERT INTO extinction_records (id, date, fact, names, places, source)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (
                r.get("id"),
                r.get("date"),
                r.get("fact"),
                r.get("names"),
                r.get("places"),
                r.get("source"),
            ),
        )

    con.commit()
    count = con.execute("SELECT COUNT(*) FROM extinction_records").fetchone()[0]
    con.close()
    print(f"built {DB.name}: {count} rows")


if __name__ == "__main__":
    main()
