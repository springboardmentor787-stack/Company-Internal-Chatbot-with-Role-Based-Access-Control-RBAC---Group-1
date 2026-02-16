from backend.database import Base, engine
from backend.models import User
from backend.models_audit import AuditLog

Base.metadata.create_all(bind=engine)

print("Database and tables created successfully")