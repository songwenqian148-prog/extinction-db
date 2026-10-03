import sqlite3
import sys

DB = "data.db"


def run(sql, params=()):
    con = sqlite3.connect(DB)
    try:
        cur = con.execute(sql, params)
        rows = cur.fetchall()
    finally:
        con.close()
    return rows


if __name__ == "__main__":
    sql = sys.argv[1]
    for row in run(sql):
        print(" | ".join("" if v is None else str(v) for v in row))
