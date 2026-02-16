# from datetime import datetime

# def log_access(user, endpoint, query=None, status="UNKNOWN"):
#     print({
#         "timestamp": datetime.utcnow().isoformat(),
#         "username": user.username,
#         "role": user.role,
#         "endpoint": endpoint,
#         "query": query,
#         "status": status
#     })
from backend.logger import audit_logger


def log_access(username, role, endpoint, status, query=None):
    message = (
        f"user={username} | "
        f"role={role} | "
        f"endpoint={endpoint} | "
        f"query={query} | "
        f"status={status}"
    )

    audit_logger.info(message)
