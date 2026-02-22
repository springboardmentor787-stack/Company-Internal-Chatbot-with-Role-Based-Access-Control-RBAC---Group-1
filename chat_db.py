import sqlite3
import json

DB_NAME = "chat_history.db"

def init_chat_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            chat_name TEXT,
            messages TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_conversation(username, chat_name, messages):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    messages_json = json.dumps(messages)

    cursor.execute("""
        INSERT INTO conversations (username, chat_name, messages)
        VALUES (?, ?, ?)
    """, (username, chat_name, messages_json))

    conn.commit()
    conn.close()


def update_conversation(username, chat_name, messages):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    messages_json = json.dumps(messages)

    cursor.execute("""
        UPDATE conversations
        SET messages = ?
        WHERE username = ? AND chat_name = ?
    """, (messages_json, username, chat_name))

    conn.commit()
    conn.close()


def load_user_conversations(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT chat_name, messages
        FROM conversations
        WHERE username = ?
    """, (username,))

    rows = cursor.fetchall()
    conn.close()

    conversations = {}

    for chat_name, messages in rows:
        conversations[chat_name] = json.loads(messages)

    return conversations


def delete_conversation(username, chat_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM conversations
        WHERE username = ? AND chat_name = ?
    """, (username, chat_name))

    conn.commit()
    conn.close()


def rename_conversation(username, old_name, new_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE conversations
        SET chat_name = ?
        WHERE username = ? AND chat_name = ?
    """, (new_name, username, old_name))

    conn.commit()
    conn.close()
