import sqlite3
import os
from .security import hash_password

DB_PATH = "data/users.db"

def init_db():
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )
    """)

    users = [
        ("hr_admin", "Hr@2026!", "HR"),
        ("fin_manager", "Fin#2026$", "Finance"),
        ("mkt_lead", "Mkt@2026#", "Marketing"),
        ("eng_dev", "Eng!2026$", "Engineering"),
        ("emp_user", "Emp@2026!", "Employees"),
        ("ceo_exec", "CEO#Secure1", "C-Level")
    ]

    for u,p,r in users:
        try:
            cur.execute(
                "INSERT INTO users VALUES (?,?,?)",
                (u, hash_password(p), r)
            )
        except:
            pass

    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cur.fetchone()
    conn.close()
    return user
