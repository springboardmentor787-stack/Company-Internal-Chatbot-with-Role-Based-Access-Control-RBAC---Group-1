from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# ✅ UPDATED IMPORT (because file renamed)
from role_mapping import ROLE_HIERARCHY
from query_utils import normalize_query


# =====================================================
# CONFIGURATION
# =====================================================

CHROMA_DB_DIR = "chroma_db"


# =====================================================
# LOAD EMBEDDING MODEL
# =====================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# =====================================================
# LOAD VECTOR DATABASE
# =====================================================

vectordb = Chroma(
    persist_directory=CHROMA_DB_DIR,
    embedding_function=embeddings
)


# =====================================================
# FUNCTION: RBAC + SEMANTIC SEARCH
# =====================================================

def rbac_semantic_search(role: str, department: str, query: str, k: int = 5):
    """
    Performs role-based secure semantic search.
    """

    # Normalize inputs
    role = role.strip()
    department = department.strip().lower()
    query = normalize_query(query)

    # 1️⃣ Validate role
    if role not in ROLE_HIERARCHY:
        return "❌ Invalid role", []

    # 2️⃣ Enforce RBAC
    allowed_departments = ROLE_HIERARCHY[role]
    if department not in allowed_departments:
        return "❌ Access denied", []

    # 3️⃣ Authorized semantic search
    results = vectordb.similarity_search_with_score(
        query=query,
        k=k,
        filter={"dept": department}
    )

    return "✅ Access granted", results


# =====================================================
# DEMO / TEST RUN
# =====================================================

if __name__ == "__main__":

    print("\n=== RBAC SEMANTIC SEARCH DEMO ===")

    while True:
        role = input("\nEnter role (HR / Finance / Engineering / Marketing / C-Level): ").strip()
        dept = input("Enter department (hr / finance / engineering / marketing / general): ").strip().lower()
        query = input("Enter your query: ").strip()

        status, results = rbac_semantic_search(
            role=role,
            department=dept,
            query=query
        )

        print("\nStatus:", status)
        print("Results found:", len(results))

        if results:
            for i, (doc, score) in enumerate(results, start=1):
                print("\n" + "=" * 50)
                print(f"📄 Result {i}")
                print("🔖 Metadata:", doc.metadata)
                print(f"📊 Similarity score: {score:.4f}")
                print("\n📝 Content:")
                print(doc.page_content[:500])
                print("=" * 50)

        cont = input("\nSearch again? (y/n): ").strip().lower()
        if cont != "y":
            print("Exiting RBAC search demo...")
            break
