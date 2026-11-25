import sqlite3, json
from datetime import datetime
DB = "test_cases.db"

def init_db():
    with sqlite3.connect(DB) as c:
        c.execute("CREATE TABLE IF NOT EXISTS runs (id INTEGER PRIMARY KEY AUTOINCREMENT, requirement TEXT NOT NULL, cases TEXT NOT NULL, created_at TEXT NOT NULL)")

def save_run(requirement, cases):
    with sqlite3.connect(DB) as c:
        cur = c.execute("INSERT INTO runs(requirement,cases,created_at) VALUES(?,?,?)",
                        (requirement, json.dumps(cases), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        return cur.lastrowid

def get_history():
    with sqlite3.connect(DB) as c:
        rows = c.execute("SELECT id,requirement,created_at FROM runs ORDER BY id DESC").fetchall()
    return [{"id":r[0],"requirement":r[1],"created_at":r[2]} for r in rows]

def get_run(run_id):
    with sqlite3.connect(DB) as c:
        row = c.execute("SELECT cases FROM runs WHERE id=?", (run_id,)).fetchone()
    return json.loads(row[0]) if row else []

def delete_run(run_id):
    with sqlite3.connect(DB) as c:
        c.execute("DELETE FROM runs WHERE id=?", (run_id,))
