from backend.models_audit import AuditLog
from backend.database import SessionLocal

def log_access(username: str, role: str, endpoint: str, action: str):
    db = SessionLocal()
    log = AuditLog(
        username=username,
        role=role,
        endpoint=endpoint,
        action=action
    )
    db.add(log)
    db.commit()
    db.close()
