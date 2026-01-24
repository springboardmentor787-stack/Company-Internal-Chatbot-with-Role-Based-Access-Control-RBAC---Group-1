from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# -----------------------------
# Configuration
# -----------------------------
CHROMA_DB_DIR = "chroma_db"
QUERY = "quarterly revenue"

# Must be same embedding model used during ingestion
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load vector store
vectorstore = Chroma(
    persist_directory=CHROMA_DB_DIR,
    embedding_function=embedding_model
)

# -----------------------------
# Role → Metadata Filters
# -----------------------------
ROLE_FILTERS = {
    "Finance": {"dept": "Finance"},
    "Marketing": {"dept": "Marketing"},
    "HR": {"dept": "HR"},
    "Engineering": {"dept": "Engineering"},
    "Employees": {"dept": "General"},
    "C-Level": None  # Full access
}

# -----------------------------
# RBAC Test Runner
# -----------------------------
def run_rbac_test():
    print("\n===== RBAC TEST RESULTS =====\n")

    for role, filter_condition in ROLE_FILTERS.items():
        print(f"🔐 Testing role: {role}")

        if filter_condition:
            results = vectorstore.similarity_search(
                QUERY,
                k=5,
                filter=filter_condition
            )
        else:
            # C-Level (no filter)
            results = vectorstore.similarity_search(
                QUERY,
                k=5
            )

        print(f"📄 Documents returned: {len(results)}")

        for i, doc in enumerate(results, 1):
            print(f"  {i}. dept={doc.metadata.get('dept')}")
            print(f"     {doc.page_content[:120]}")

        # RBAC assertion logic
        if role != "Finance" and role != "C-Level":
            assert len(results) == 0, f"❌ RBAC FAILED for role: {role}"

       
# -----------------------------
# Execute
# -----------------------------
if __name__ == "__main__":
    run_rbac_test()
results = vectorstore.similarity_search(
    "quarterly revenue",
    k=5,
    filter={"dept": "HR"}
)

assert len(results) == 0

print("✅ Access validated\n")

print("🎯 ALL RBAC TESTS PASSED SUCCESSFULLY")