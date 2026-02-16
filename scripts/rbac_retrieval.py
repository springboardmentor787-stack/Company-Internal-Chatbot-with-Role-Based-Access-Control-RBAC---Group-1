# rbac_retrieval_demo.py
# Milestone 2 – Role-Based Retrieval with Access Audit Logging

import csv
from datetime import datetime
from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

CHROMA_DB_PATH = "chroma_db"
AUDIT_LOG_FILE = "access_audit_log.csv"


def log_access(role, department, status):
    """Log every access attempt for auditing"""
    with open(AUDIT_LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            role,
            department,
            status
        ])


def main():
    print("\n===== ROLE BASED DOCUMENT RETRIEVAL =====\n")

    # Step 1: Select Role
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

    # Step 2: Select Department
    print("\nWhich department documents to retrieve?")
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

    print(f"\nTrying to retrieve {department} documents...\n")

    # Step 3: Load ChromaDB
    embedding_function = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embedding_function
    )

    # Step 4: Metadata Filtering (Department)
    results = vectordb.get(
        where={"dept": department}
    )

    documents = results.get("documents", [])
    metadatas = results.get("metadatas", [])

    # Step 5: RBAC Enforcement
    authorized_docs = []
    for doc, meta in zip(documents, metadatas):
        allowed_roles = meta.get("allowed_roles", "")
        if user_role in allowed_roles:
            authorized_docs.append(doc)

    # Step 6: Output + Audit Log
    if authorized_docs:
        print(f"✅ Retrieved {len(authorized_docs)} authorized documents.\n")
        print("Sample document content (first 300 chars):\n")
        print(authorized_docs[0][:300])

        log_access(user_role, department, "GRANTED")
    else:
        print("❌ Access Denied: No authorized documents found.")
        log_access(user_role, department, "DENIED")

    print("\n===== END OF DEMO =====")


if __name__ == "__main__":
    main()