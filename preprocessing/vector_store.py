
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# ===============================
# CONFIG
# ===============================

CHROMA_DB_DIR = "chroma_db"

ROLE_ACCESS = {
    "HR": ["hr", "general"],
    "Finance": ["finance", "general"],
    "Engineering": ["engineering", "general"],
    "Marketing": ["marketing", "general"],
    "C-Level": ["finance", "hr", "engineering", "marketing", "general"]
}

# ===============================
# LOAD VECTOR DB
# ===============================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma(
    persist_directory=CHROMA_DB_DIR,
    embedding_function=embeddings
)

# ===============================
# SECURE SEARCH FUNCTION
# ===============================

def secure_search(user_role, target_dept, query, k=5):

    # Validate role
    if user_role not in ROLE_ACCESS:
        print("❌ Invalid role")
        return []

    # RBAC enforcement
    if target_dept not in ROLE_ACCESS[user_role]:
        print("❌ Access denied or no data available for role:", user_role)
        return []

    # Authorized retrieval
    results = vectordb.similarity_search(
        query=query,
        k=k,
        filter={"dept": target_dept}
    )

    return results

# ===============================
# INTERACTIVE TERMINAL LOOP
# ===============================

if __name__ == "__main__":

    print("\n=== COMPANY INTERNAL CHATBOT (RBAC ENABLED) ===")
    print("Available roles:", ", ".join(ROLE_ACCESS.keys()))
    print("Available departments: finance, hr, engineering, marketing, general")

    while True:
        print("\n------------------------------------")
        user_role = input("Enter your role (or type 'exit'): ").strip()
        if user_role.lower() == "exit":
            print("Exiting chatbot...")
            break

        target_dept = input("Enter department to search: ").strip().lower()
        query = input("Enter your query: ").strip()

        results = secure_search(user_role, target_dept, query)

        print("Results found:", len(results))

        if results:
            print("\nSample chunk metadata:")
            print(results[0].metadata)
