import sqlite3
from pathlib import Path

DB_PATH = Path("data/parking.db")

def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS spots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        spot_name TEXT UNIQUE,
        occupied INTEGER DEFAULT 0
    )
    """)
    # Create 8 spots if none exist
    cur.execute("SELECT COUNT(*) as c FROM spots")
    if cur.fetchone()["c"] == 0:
        for i in range(1, 9):
            cur.execute("INSERT INTO spots (spot_name, occupied) VALUES (?, ?)", (f"Spot {i}", 0))
    conn.commit()
    conn.close()
