from backend.db import engine, Base
from backend.models import User

Base.metadata.create_all(bind=engine)
print("Tables created")
