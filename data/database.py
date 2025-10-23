import sqlite3
from datetime import datetime

DB_PATH = "data/notes.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        text TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_note(user_id, text):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (user_id, text, created_at) VALUES (?, ?, ?)",
                   (user_id, text, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_notes(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, text, created_at FROM notes WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_note(note_id, user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ? AND user_id = ?", (note_id, user_id))
    conn.commit()
    conn.close()

def find_notes(user_id, keyword):
    conn = sqlite3.connect('data/notes.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, text FROM notes WHERE user_id = ? AND text LIKE ?",
        (user_id, f"%{keyword}%")
    )
    results = cursor.fetchall()
    conn.close()
    return results
