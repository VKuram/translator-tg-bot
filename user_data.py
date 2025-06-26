from telegram import User
import sqlite3
import json

db_file_path = "cache.db"

def get_user_fullname(user: User) -> str:
    user_data = [
        getattr(user, "id"),
        getattr(user, "first_name"),
        getattr(user, "last_name"),
        getattr(user, "username"),
    ]

    return ", ".join([str(ud) for ud in user_data if (ud is not None and ud != "")])

def init_db():
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            id TEXT PRIMARY KEY,
            messages TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_user_cache(user_id: str, user_messages: list):
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    serialized = json.dumps(user_messages)  # сериализуем список словарей в строку
    cursor.execute("""
        INSERT OR REPLACE INTO cache (id, messages)
        VALUES (?, ?)
    """, (user_id, serialized))
    conn.commit()
    conn.close()

def load_user_cache(user_id: str) -> list:
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    cursor.execute("SELECT messages FROM cache WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return []

def delete_user_cache(user_id: str):
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cache'")
    table_exists = cursor.fetchone()

    if not table_exists:
        conn.close()
        return

    cursor.execute("DELETE FROM cache WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
