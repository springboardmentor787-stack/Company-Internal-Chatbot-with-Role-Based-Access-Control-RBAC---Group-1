import time
from vector_db_utils import load_vector_db, validate_vector_db
from query_utils import normalize_query
from rbac_utils import get_allowed_roles

TOP_K = 5

def secure_semantic_search(query: str, user_role: str):
    vectordb = load_vector_db()
    validate_vector_db(vectordb)

    query = normalize_query(query)
    allowed_roles = get_allowed_roles(user_role)

    start = time.time()

    # 🔐 RBAC APPLIED DURING SEARCH (NOT AFTER)
    results = vectordb.similarity_search_with_score(
        query,
        k=TOP_K,
        filter={"role": {"$in": allowed_roles}}
    )

    latency = round((time.time() - start) * 1000, 2)

    print(f"\n🔐 Role: {user_role}")
    print(f"🔍 Query: {query}")
    print(f"⏱️ Latency: {latency} ms")

    if not results:
        print("❌ ACCESS DENIED or NO RESULTS")
        return []

    for i, (doc, score) in enumerate(results, start=1):
        print(f"\nResult {i}")
        print("Score:", round(score, 4))
        print("Role:", doc.metadata["role"])
        print("Source:", doc.metadata["source"])
        print("Preview:", doc.page_content[:150])

    return results


if __name__ == "__main__":
    role = input("Enter role (HR/Finance/Engineering/Marketing/C-Level): ").strip()
    query = input("Enter query: ").strip()
    secure_semantic_search(query, role)
