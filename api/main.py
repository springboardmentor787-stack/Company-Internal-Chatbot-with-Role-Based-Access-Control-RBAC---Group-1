from fastapi import FastAPI, Depends
from api.auth.auth_routes import router as auth_router
from api.auth.jwt_utils import get_current_user
from document_loader.secure_semantic_search import secure_semantic_search
from rag.rag_pipeline import run_rag
from rag.confidence import calculate_confidence


from api.auth.auth_utils import hash_password
from api.database import engine, SessionLocal, Base
from api.auth.user_models import User

app = FastAPI(
    title="RBAC Semantic Search API",
    description="Company Internal Chatbot with Role-Based Access Control",
    version="1.0"
)
@app.on_event("startup")
def startup_event():
    print("========== STARTUP TRIGGERED ==========")

    Base.metadata.create_all(bind=engine)
    print("SQLite tables created")

    db = SessionLocal()

    default_users = [
        ("ceo", "123", "C-Level"),
        ("finance", "123", "Finance"),
        ("hruser", "123", "HR"),
        ("engg", "123", "Engineering"),
        ("marketing", "123", "Marketing"),
        ("general", "123", "General"),
    ]

    for username, password, role in default_users:
        existing = db.query(User).filter(User.username == username).first()
        if not existing:
            user = User(
                username=username,
                hashed_password=hash_password(password),
                role=role
            )
            db.add(user)

    db.commit()
    db.close()

    print("Users seeded")

    

    print("========== STARTUP FINISHED ==========")
app.include_router(auth_router)

@app.post("/search")
def search(query: str, user=Depends(get_current_user)):
    role = user["role"]

    results = secure_semantic_search(
        query=query,
        user_role=role
    )

    return {
        "access_granted": len(results) > 0,
        "results": [
            {
                "score": score,
                "role": doc.metadata.get("role"),
                "source": doc.metadata.get("source"),
                "preview": doc.page_content[:150]
            }
            for doc, score in results
        ]
    }

@app.post("/rag")
def rag_query(query: str, user=Depends(get_current_user)):
    role = user["role"]

    results = secure_semantic_search(query, role)
    rag_output = run_rag(query, role, results)
    confidence = calculate_confidence(results)

    return {
        "answer": rag_output["answer"],
        "sources": rag_output["sources"],
        "confidence": confidence
    }
@app.get("/documents")
def get_documents(user=Depends(get_current_user)):
    import os

    base_path = "Fintech-data"
    role = user["role"]

    role_folder_map = {
        "Finance": "Finance",
        "HR": "HR",
        "Engineering": "engineering",
        "Marketing": "marketing",
        "General": "general",
        "C-Level": None
    }

    if role == "C-Level":
        folders = ["Finance", "HR", "engineering", "marketing", "general"]
    else:
        folders = []
        folder = role_folder_map.get(role)
        if folder:
            folders.append(folder)
        folders.append("general")

    response = {}

    for folder in folders:
        folder_path = os.path.join(base_path, folder)

        if os.path.exists(folder_path):
            files = [
                f for f in os.listdir(folder_path)
                if f.endswith((".md", ".csv"))
            ]
            response[folder] = files

    return response