import sqlite3
from pathlib import Path
from models import hash_password

DB_PATH = Path(__file__).parent / "users.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")

    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    users = [
        ("hr", "12345", "HR"),
        ("finance", "12345", "Finance"),
        ("eng", "12345", "Engineering"),
        ("marketing", "12345", "Marketing"),
        ("emp", "12345", "Employees"),
        ("ceo", "12345", "C-Level")
    ]

    hashed_users = [
        (u, hash_password(p), r) for (u, p, r) in users
    ]

    cursor.executemany(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        hashed_users
    )

    conn.commit()
    conn.close()

    print("Database initialized successfully.")

if __name__ == "__main__":
    main()
