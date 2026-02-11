from pathlib import Path
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# =====================================================
# PATHS
# =====================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "db" / "chroma_global"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# =====================================================
# LOAD VECTOR DATABASE
# =====================================================

def load_vector_db():
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)

    db = Chroma(
        persist_directory=str(DB_PATH),
        embedding_function=embeddings,
        collection_name="company_documents"
    )

    return db


# =====================================================
# SIMPLE CHAT FUNCTION
# =====================================================

def ask_question(query, user_role):
    db = load_vector_db()

    results = db.similarity_search(
        query,
        k=5
    )

    # RBAC filtering
    authorized_results = []
    for doc in results:
        allowed_roles = doc.metadata.get("allowed_roles", "")
        if user_role in allowed_roles:
            authorized_results.append(doc)

    return authorized_results


# =====================================================
# TEST RUN
# =====================================================

if __name__ == "__main__":
    role = input("Enter your role (HR / Finance / Engineering / Marketing / C-Level): ")
    query = input("Ask your question: ")

    answers = ask_question(query, role)

    print(f"\n✅ Authorized results found: {len(answers)}\n")

    for i, doc in enumerate(answers, 1):
        print(f"--- Result {i} ---")
        print(doc.page_content[:500])
        print("Metadata:", doc.metadata)
        print()


#| Role        | Question               |
#| ----------- | ---------------------- |
#| Finance     | claim approval process |
#| HR          | employee leave policy  |
#| Engineering | system architecture    |
#| Marketing   | customer acquisition   |
#| C-Level     | company financial risk |
