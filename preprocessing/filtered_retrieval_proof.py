
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

CHROMA_DB_DIR = "chroma_db"

# Role → allowed departments mapping (RBAC POLICY)
ROLE_ACCESS = {
    "HR": ["hr", "general"],
    "Finance": ["finance", "general"],
    "Engineering": ["engineering", "general"],
    "Marketing": ["marketing", "general"],
    "C-Level": ["finance", "hr", "engineering", "marketing", "general"]
}

# Load embeddings and vector DB
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma(
    persist_directory=CHROMA_DB_DIR,
    embedding_function=embeddings
)

# Secure search function (dynamic RBAC)

def secure_search(user_role: str, target_dept: str, query: str, k: int = 5):
    """
    Dynamically enforces RBAC for any role and department.
    """

    # Step 1: Validate role
    if user_role not in ROLE_ACCESS:
        return "Invalid role", []

    # Step 2: RBAC enforcement
    if target_dept not in ROLE_ACCESS[user_role]:
        return "Access denied", []

    # Step 3: Authorized retrieval
    results = vectordb.similarity_search(
        query=query,
        k=k,
        filter={"dept": target_dept}
    )

    return "Access granted", results


# =========================
# DYNAMIC RBAC DEMO
# =========================

if __name__ == "__main__":

    print("\n=== Secure RBAC Vector Search ===")

    while True:
        user_role = input("\nEnter your role (HR / Finance / Engineering / Marketing / C-Level): ").strip()
        target_dept = input("Enter department to search (hr / finance / engineering / marketing / general): ").strip().lower()
        query = input("Enter your query: ").strip()

        status, results = secure_search(
            user_role=user_role,
            target_dept=target_dept,
            query=query
        )

        print("\nStatus:", status)
        print("Results found:", len(results))

        if results:
            print("Sample metadata:", results[0].metadata)

        cont = input("\nDo you want to search again? (y/n): ").strip().lower()
        if cont != "y":
            break
