from backend.database import engine, Base
from backend.models import User

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully")

if __name__ == "__main__":
    init_db()
