import time
from vector_db_utils import load_vector_db, validate_vector_db
from query_utils import normalize_query
from rbac_utils import get_allowed_roles

TOP_K = 5

# 🔁 POLICY TOGGLE
# True  -> Strict RBAC (DENY if no authorized results)
# False -> Soft RBAC (allow fallback behavior if needed)
STRICT_RBAC_MODE = True


def secure_semantic_search(query: str, user_role: str):
    vectordb = load_vector_db()
    validate_vector_db(vectordb)

    original_query = query
    query = normalize_query(query)
    allowed_roles = get_allowed_roles(user_role)

    start = time.time()

    # 🔐 RBAC APPLIED DURING SEARCH
    results = vectordb.similarity_search_with_score(
        query,
        k=TOP_K,
        filter={"role": {"$in": allowed_roles}}
    )

    latency = round((time.time() - start) * 1000, 2)

    # ================= OUTPUT SUMMARY =================
    print("\n================ SEARCH SUMMARY ================\n")
    print(f"User Role           : {user_role}")
    print(f"Query               : {original_query}")
    print(f"Normalized Query    : {query}")
    print(f"Allowed Roles       : {allowed_roles}")
    print(f"Total Results Found : {len(results)}")
    print(f"Search Latency      : {latency} ms")
    print(f"Top-K               : {TOP_K}")

    # 🚫 STRICT RBAC DECISION
    if len(results) == 0 and STRICT_RBAC_MODE:
        print("\nAccess Decision     : ❌ DENIED (RBAC)")
        print("Reason              : No authorized documents matched the query.")
        print("\n================================================")
        return []

    # ✅ ACCESS GRANTED
    print("\nAccess Decision     : ✅ GRANTED")
    print("\n--- Top Authorized Results ---\n")

    for i, (doc, score) in enumerate(results, start=1):
        print(f"Result {i}")
        print(f"Score   : {round(score, 4)}")
        print(f"Role    : {doc.metadata.get('role')}")
        print(f"Source  : {doc.metadata.get('source')}")
        print(f"Preview : {doc.page_content[:150]}")
        print("-" * 40)

    print("\n================================================")
    return results


if __name__ == "__main__":
    role = input("Enter role (HR/Finance/Engineering/Marketing/C-Level): ").strip()
    query = input("Enter query: ").strip()
    secure_semantic_search(query, role)
