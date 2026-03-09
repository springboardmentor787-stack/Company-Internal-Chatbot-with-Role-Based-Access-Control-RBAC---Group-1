import sqlite3
from pathlib import Path
from models import hash_password

DB_PATH = Path(__file__).parent / "users.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Drop existing tables
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS access_logs")

    # Create users table
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # 🔥 Create access_logs table
    cursor.execute("""
    CREATE TABLE access_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        role TEXT,
        query TEXT,
        confidence REAL,
        response_time REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    users = [
        ("hr_admin", "Ln_Hr@2026!", "HR"),
        ("fin_manager", "Ln_Fin#2026$", "Finance"),
        ("eng_dev", "Ln_Eng!2026#", "Engineering"),
        ("mkt_lead", "Ln_Mkt&2026*", "Marketing"),
        ("emp_user", "Ln_Emp$2026!", "Employees"),
        ("ceo_exec", "Ln_CEO*Secure1", "C-Level")
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

    print("Database initialized with users + access_logs table.")
    print("DB path:", DB_PATH)

if __name__ == "__main__":
    main()