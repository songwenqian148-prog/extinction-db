import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "records.json"
DB = ROOT / "data.db"


def main():
    records = json.loads(RECORDS.read_text(encoding="utf-8"))

    con = sqlite3.connect(DB)
    existing = {r[0] for r in con.execute("SELECT id FROM extinction_records")}

    inserted = []
    for r in records:
        if r.get("id") in existing:
            continue
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
        inserted.append(r.get("id"))

    con.commit()
    count = con.execute("SELECT COUNT(*) FROM extinction_records").fetchone()[0]
    con.close()
    print(f"inserted ids {inserted}; table now has {count} rows")


if __name__ == "__main__":
    main()
