import sqlite3
from auth import hash_password

DB_NAME = "users.db"

users = [
    ("hr_user", "hr123", "HR"),
    ("finance_user", "fin123", "Finance"),
    ("engineer_user", "eng123", "Engineering"),
    ("manager", "manager123", "C-Level"),
]

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

# Create table
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

# Insert users
for username, password, role in users:
    hashed = hash_password(password)
    cur.execute(
        "INSERT OR REPLACE INTO users VALUES (?, ?, ?)",
        (username, hashed, role)
    )

conn.commit()
conn.close()

print("✅ users.db created with sample users")
