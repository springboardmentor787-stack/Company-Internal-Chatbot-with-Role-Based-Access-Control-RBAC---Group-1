from database import get_db

def get_user(username: str):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT username, password, role FROM users WHERE username = ?",
        (username,)
    )
    user = cur.fetchone()
    db.close()
    return user
