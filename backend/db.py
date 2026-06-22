import sqlite3
from datetime import datetime
from passlib.context import CryptContext

DATABASE = "users.db"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_connection():
    return sqlite3.connect(DATABASE)


def create_users_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    conn.commit()
    conn.close()


def create_logs_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        role TEXT,
        query TEXT,
        status TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def add_user(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO users (username, password, role)
    VALUES (?, ?, ?)
    """, (username, hash_password(password), role))

    conn.commit()
    conn.close()


def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT username, password, role FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "username": row[0],
            "password": row[1],
            "role": row[2]
        }

    return None


def insert_log(username, role, query, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO logs (username, role, query, status, timestamp)
    VALUES (?, ?, ?, ?, ?)
    """, (username, role, query, status, str(datetime.now())))

    conn.commit()
    conn.close()


def get_all_logs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM logs ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    return rows


def get_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM logs")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT role, COUNT(*) FROM logs GROUP BY role")
    role_counts = cursor.fetchall()

    conn.close()

    return total, role_counts