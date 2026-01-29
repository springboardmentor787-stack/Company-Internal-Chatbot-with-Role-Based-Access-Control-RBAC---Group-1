# =====================================================
# SEMANTIC RBAC SEARCH – SINGLE FILE VERSION
# =====================================================
# Combines:
# - RBAC configuration
# - Query normalization
# - Semantic vector search
# - Terminal-based user interaction
#
# This file performs PURE SEMANTIC SEARCH
# (search by meaning, not keywords)
# =====================================================

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# =====================================================
# CONFIGURATION
# =====================================================

CHROMA_DB_DIR = "chroma_db"


# =====================================================
# ROLE → DEPARTMENT MAPPING (RBAC POLICY)
# =====================================================

ROLE_HIERARCHY = {
    "HR": ["hr", "general"],
    "Finance": ["finance", "general"],
    "Engineering": ["engineering", "general"],
    "Marketing": ["marketing", "general"],
    "C-Level": ["finance", "hr", "engineering", "marketing", "general"]
}


# =====================================================
# QUERY NORMALIZATION (SEMANTIC HYGIENE)
# =====================================================

def normalize_query(query: str) -> str:
    """
    Normalizes user query for better semantic matching.
    """
    return query.strip().lower()


# =====================================================
# LOAD EMBEDDING MODEL (SEMANTIC UNDERSTANDING)
# =====================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# =====================================================
# LOAD VECTOR DATABASE (ALREADY EMBEDDED DOCUMENTS)
# =====================================================

vectordb = Chroma(
    persist_directory=CHROMA_DB_DIR,
    embedding_function=embeddings
)


# =====================================================
# FUNCTION: SEMANTIC SEARCH WITH RBAC
# =====================================================

def rbac_semantic_search(role: str, department: str, query: str, k: int = 5):
    """
    Performs PURE SEMANTIC SEARCH with RBAC enforcement.

    Steps:
    1. Normalize inputs
    2. Validate role
    3. Enforce RBAC
    4. Perform vector similarity search
    """

    # Normalize inputs
    role = role.strip()
    department = department.strip().lower()
    query = normalize_query(query)

    # 1️⃣ Validate role
    if role not in ROLE_HIERARCHY:
        return "Invalid role", []

    # 2️⃣ RBAC enforcement
    if department not in ROLE_HIERARCHY[role]:
        return "Access denied", []

    # 3️⃣ SEMANTIC VECTOR SEARCH (MEANING-BASED)
    results = vectordb.similarity_search_with_score(
        query=query,
        k=k,
        filter={"dept": department}
    )

    return "Access granted", results


# =====================================================
# MAIN FUNCTION (USER INTERFACE)
# =====================================================

def run():
    """
    Terminal-based Semantic RBAC Search application.
    """

    print("\n🔐 SEMANTIC ROLE-BASED SEARCH\n")

    role = input(
        "Enter your role (HR / Finance / Engineering / Marketing / C-Level): "
    ).strip()

    department = input(
        "Enter department to search (hr / finance / engineering / marketing / general): "
    ).strip().lower()

    query = input("Ask your question (natural language): ").strip()

    # Perform semantic search
    status, results = rbac_semantic_search(
        role=role,
        department=department,
        query=query
    )

    # =============================
    # SEARCH SUMMARY
    # =============================
    print("\n================ SEMANTIC SEARCH SUMMARY ================")
    print("Status        :", status)
    print("Results Found :", len(results))
    print("========================================================")

    if status != "Access granted":
        return

    if not results:
        print("\n⚠️ No semantically relevant results found.")
        return

    # =============================
    # DISPLAY SEMANTIC RESULTS
    # =============================
    print("\n🧠 Top Semantic Matches:\n")

    for idx, (doc, score) in enumerate(results, 1):
        print(f"Result {idx}")
        print("Source file :", doc.metadata.get("source_file"))
        print("Department  :", doc.metadata.get("dept"))
        print("Relevance   :", round(score, 4))
        print("Matched Meaning:")
        print(doc.page_content[:300])
        print("-" * 60)


# =====================================================
# PROGRAM ENTRY POINT
# =====================================================

if __name__ == "__main__":
    run()
