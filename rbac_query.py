# rbac_query.py
# RBAC + Query-Based Secure Retrieval (Milestone 2 Extension)

from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

CHROMA_DB_PATH = "chroma_db"

ROLE_ACCESS_MAP = {
    "Finance": ["Finance", "General"],
    "HR": ["HR", "General"],
    "Marketing": ["Marketing", "General"],
    "Engineering": ["Engineering", "General"],
    "C-Level": ["Finance", "HR", "Marketing", "Engineering", "General"]
}


def main():
    print("\n===== SECURE RBAC QUERY DEMO =====\n")

    # Step 1: Role selection
    print("Select your role:")
    print("1. Finance")
    print("2. HR")
    print("3. Marketing")
    print("4. Engineering")
    print("5. C-Level")

    role_choice = input("\nEnter role (1-5): ").strip()

    role_map = {
        "1": "Finance",
        "2": "HR",
        "3": "Marketing",
        "4": "Engineering",
        "5": "C-Level"
    }

    user_role = role_map.get(role_choice)
    if not user_role:
        print("\n❌ Invalid role")
        return

    print(f"\nUser Role: {user_role}")

    # Step 2: Department selection
    print("\nWhich department documents do you want to access?")
    print("1. Finance")
    print("2. HR")
    print("3. Marketing")
    print("4. Engineering")
    print("5. General")

    dept_choice = input("\nEnter department (1-5): ").strip()

    dept_map = {
        "1": "Finance",
        "2": "HR",
        "3": "Marketing",
        "4": "Engineering",
        "5": "General"
    }

    department = dept_map.get(dept_choice)
    if not department:
        print("\n❌ Invalid department")
        return

    # Step 3: RBAC validation
    if department not in ROLE_ACCESS_MAP[user_role]:
        print(f"\n❌ ACCESS DENIED: {user_role} cannot access {department} documents")
        return

    print("\n✅ RBAC Validation PASSED")

    # Step 4: Enter query
    query = input("\nEnter your query: ").strip()

    # Step 5: Load ChromaDB
    embedding_function = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embedding_function
    )

    # Step 6: Secure retrieval (department-filtered search)
    results = vectordb.similarity_search(
        query,
        k=3,
        filter={"dept": department}
    )

    if not results:
        print("\nNo authorized documents matched the query.")
        return

    # Step 7: Display results
    print("\n--- AUTHORIZED SEARCH RESULTS ---\n")
    for i, doc in enumerate(results, 1):
        print(f"[Result {i}] Source: {doc.metadata.get('source')}")
        print(doc.page_content[:300])
        print("-" * 40)

    print("\n===== END OF DEMO =====")


if __name__ == "__main__":
    main()