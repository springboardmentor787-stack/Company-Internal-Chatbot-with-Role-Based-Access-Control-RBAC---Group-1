import chromadb

# Initialize Client and Collection
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("docs")

def ask(query, user_role, top_k=3):
    # Query the database
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    print("\n--- FILTERED RESULTS ---")
    found_any = False

    for i, (doc, meta) in enumerate(zip(docs, metas)):
        allowed_roles = meta.get("roles", [])

        # RBAC CHECK: allow only if user role exists in metadata roles
        if user_role not in allowed_roles:
            continue  # skip unauthorized docs

        found_any = True

        print(f"\nResult {i+1}:")
        print("Department:", meta.get("department"))
        print("Roles Allowed:", allowed_roles)
        print("Snippet:", doc[:250], "...")

    if not found_any:
        print("\n❌ Access Denied or No Matching Results for This Role.")

if __name__ == "__main__":
    user_role = input("Enter your role (HR, Finance, Employees, Marketing, Engineering, C-Level): ").strip()
    print(f"\nRole set to: {user_role}")

    while True:
        q = input("\nAsk something (or 'exit'): ")
        if q.lower() == "exit":
            break
        ask(q, user_role)