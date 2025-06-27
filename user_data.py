from telegram import User
import sqlite3
import json

db_file_path = "cache.db"

def get_user_full_name(user: User) -> str:
    """Форматирует данные пользователя в Markdown-список."""
    user_data_types = ["id", "first_name", "last_name", "username", "language_code", "is_premium"]
    user_data = []

    for data_type in user_data_types:
        value = getattr(user, data_type, None)
        if value:
            user_data.append(f"`{data_type}`: `{value}`")  # Моноширинный вывод

    return "\n".join(user_data) if user_data else "Нет данных о пользователе."

def init_db():
    """Инициализация БД с кэшем диалога с чат-ботом"""
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
    """Сохранение диалога в БД с кэшем"""
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
    """Чтение диалога из БД с кэшем"""
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    cursor.execute("SELECT messages FROM cache WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return []

def delete_user_cache(user_id: str):
    """Удаление кэша диалога"""
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
