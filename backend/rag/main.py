from fastapi import FastAPI, Depends

# Routers & Security
from auth_routes import router as auth_router
from rbac_dependency import get_current_user

# RAG
from retriever import retrieve_chunks
from prompt_builder import build_prompt
from llm_engine import generate_answer


# =========================
# CREATE APP (VERY IMPORTANT)
# =========================
app = FastAPI(title="Internal Chatbot API")


# =========================
# REGISTER ROUTES
# =========================
app.include_router(auth_router)


# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health_check():
    return {"status": "ok"}


# =========================
# TEST PROTECTED
# =========================
@app.get("/protected")
def protected_route(user=Depends(get_current_user)):
    return {
        "message": "You are authorized",
        "user": user
    }


# =========================
# FINAL RAG CHAT API
# =========================
from rbac_rules import get_allowed_departments


@app.post("/chat")
def chat(
    data: dict,
    user=Depends(get_current_user)
):
    query = data.get("query")
    role = user["role"].lower()

    if not query:
        return {"error": "Query missing"}

    # 🔐 STEP 1: Get allowed depts
    allowed_depts = get_allowed_departments(role)

    if not allowed_depts:
        return {
            "answer": "You do not have access to any department data.",
            "sources": []
        }

    # 🧠 STEP 2: Retrieve
    chunks = retrieve_chunks(query, role)

    # 🔍 STEP 3: HARD FILTER (Final RBAC)
    filtered = []

    for ch in chunks:
        if ch["department"] in allowed_depts:
            filtered.append(ch)

    if not filtered:
        return {
            "answer": "I do not have access to that information.",
            "sources": []
        }

    # ✍️ STEP 4: Prompt
    prompt, used_chunks = build_prompt(filtered, query)

    answer = generate_answer(prompt)

    # 📚 STEP 5: Sources
    sources = []

    for i, ch in enumerate(used_chunks, 1):
        sources.append({
            "id": i,
            "department": ch["department"],
            "source": ch["source"],
            "roles": ch["roles"]
        })

    return {
        "question": query,
        "role": role,
        "answer": answer,
        "sources": sources
    }
