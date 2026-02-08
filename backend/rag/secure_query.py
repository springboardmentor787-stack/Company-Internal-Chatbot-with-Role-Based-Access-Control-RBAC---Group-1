import faiss
import pickle
from sentence_transformers import SentenceTransformer


# =========================
# LOAD RESOURCES
# =========================

try:
    index = faiss.read_index("vector.index")

    with open("metadata.pkl", "rb") as f:
        metadata = pickle.load(f)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("FAISS + Metadata + Model Loaded.")

except Exception as e:
    print("❌ Failed to load resources:", e)
    raise e


# =========================
# RBAC VALIDATION
# =========================

def validate_access(user_role: str, doc_dept: str) -> bool:

    user_role = user_role.lower().strip()
    doc_dept = doc_dept.lower().strip()

    # C-Level: All access
    if user_role == "c-level":
        return True

    # General docs
    if doc_dept == "general":
        return True

    # Same department
    if user_role == doc_dept:
        return True

    return False


# =========================
# MAIN SEARCH FUNCTION
# =========================

def secure_search(query: str, user_role: str, k: int = 3):

    # Encode query
    query_vec = model.encode(
        [query],
        convert_to_numpy=True
    )

    # FAISS search (overfetch)
    D, I = index.search(query_vec, k * 3)

    results = []

    for idx in I[0]:

        if idx == -1:
            continue

        doc = metadata[idx]

        doc_dept = doc.get("department", "general")

        # 🔧 SAFE ROLE NORMALIZATION
        raw_roles = doc.get("roles", [])

        if isinstance(raw_roles, str):
            roles = [r.strip().lower() for r in raw_roles.split(",")]
        elif isinstance(raw_roles, list):
            roles = [r.strip().lower() for r in raw_roles]
        else:
            roles = []

        # Permission check
        if validate_access(user_role, doc_dept):

            results.append({
                "text": doc.get("chunk", ""),
                "source": doc.get("file_name", "unknown"),
                "department": doc_dept,
                "roles": roles
            })

        if len(results) >= k:
            break

    return results


# =========================
# TEST
# =========================

if __name__ == "__main__":

    print("Testing secure search...")

    test = secure_search("leave policy", "hr")

    for r in test:
        print(r)
