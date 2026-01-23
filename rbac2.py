import chromadb

# -----------------------------
# QUERY EXPANSION FOR HR
# -----------------------------
QUERY_EXPANSIONS = {
    "employees": ["employee", "staff", "workers", "people"],
    "salaries": ["salary", "compensation", "pay"],
    "hr": ["human resources", "hr", "employees", "staff"],
    "emails": ["email", "mail", "contact"],
    "roles": ["position", "job", "role", "title"],
}

def expand_query(query: str):
    words = query.lower().split()
    expanded = set(words)
    for w in words:
        if w in QUERY_EXPANSIONS:
            expanded.update(QUERY_EXPANSIONS[w])
    return " ".join(expanded)

# -----------------------------
# INITIALIZE DB
# -----------------------------
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("docs")

# -----------------------------
# RBAC QUERY FUNCTION
# -----------------------------
def rbac_query(query, user_role, top_k=5):
    user_role = user_role.lower()
    query = expand_query(query)

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "metadatas"]
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    authorized = []

    for doc, meta in zip(docs, metas):
        allowed_lower = [r.lower() for r in meta.get("roles", [])]
        if user_role in allowed_lower:
            authorized.append((doc, meta))

    if not authorized:
        print("\n❌ Access Denied or No Matching Data Found.\n")
        return

    print("\n--- AUTHORIZED RESULTS ---")
    for i, (doc, meta) in enumerate(authorized, 1):
        print(f"\nResult {i}:")
        print("Department:", meta.get("department"))
        print("Allowed Roles:", meta.get("roles"))
        print("Snippet:", doc[:300], "...\n")

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    role = input("Enter your role (HR, Finance, Employees, Marketing, Engineering, C-Level): ").strip()

    while True:
        q = input("\nAsk something (or 'exit'): ").strip()
        if q.lower() == "exit":
            break
        rbac_query(q, role)
