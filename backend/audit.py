
from datetime import datetime


def audit_log(user, endpoint, query, status):

    line = (
        f"{datetime.utcnow()} | "
        f"user={user.username} | "
        f"role={user.role} | "
        f"endpoint={endpoint} | "
        f"query={query} | "
        f"status={status}"
    )

    print(line)

    with open("access_audit.log", "a") as f:
        f.write(line + "\n")
