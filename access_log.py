# access_log.py

from datetime import datetime

def log_access(user, role, query, status):
    with open("access.log", "a") as f:
        f.write(
            f"{datetime.now()} | {user} | {role} | {query} | {status}\n"
        )
