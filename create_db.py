from api.database import engine
from api.auth.user_models import Base

Base.metadata.create_all(bind=engine)
print("✅ User database created")
