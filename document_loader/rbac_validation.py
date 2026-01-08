from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


PERSIST_DIR = "chroma_db"

ROLE_MENU = {
    "1": "HR",
    "2": "Finance",
    "3": "Engineering",
    "4": "Marketing",
    "5": "C-Level"
}

ROLE_ACCESS_MAP = {
    "HR": ["HR", "General"],
    "Finance": ["Finance", "General"],
    "Engineering": ["Engineering", "General"],
    "Marketing": ["Marketing", "General"],
    "C-Level": ["Finance", "HR", "Engineering", "Marketing", "General"]
}

TOP_K = 5
PREVIEW_LIMIT = 3


def run_rbac_demo():
    # Load vector DB
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embedding_model
    )

    # Role selection
    print("Select your role:")
    for k, v in ROLE_MENU.items():
        print(f"{k}. {v}")

    role_choice = input("Enter role number: ").strip()
    user_role = ROLE_MENU.get(role_choice)

    if not user_role:
        print("Invalid role.")
        return

    print(f"\nUser role selected: {user_role}")

    # Query input
    query = input("\nEnter your query: ").strip()

    # Semantic search
    retrieved = vectordb.similarity_search(query, k=TOP_K)

    # RBAC filtering
    allowed_roles = ROLE_ACCESS_MAP[user_role]
    authorized = [
        doc for doc in retrieved
        if doc.metadata.get("role") in allowed_roles
    ]

    # Decision
    print("\n🔐 ACCESS DECISION")

    if len(authorized) == 0:
        print("❌ ACCESS DENIED")
        print(f"{user_role} users are not authorized to access this data.")
        return

    print("✅ ACCESS GRANTED")

    print("\n📄 TOP AUTHORIZED DOCUMENT PREVIEW")
    for i, doc in enumerate(authorized[:PREVIEW_LIMIT], start=1):
        print(f"\nDocument {i}")
        print("Source:", doc.metadata["source"])
        print("Role:", doc.metadata["role"])
        print("Preview:", doc.page_content[:150])


if __name__ == "__main__":
    run_rbac_demo()
