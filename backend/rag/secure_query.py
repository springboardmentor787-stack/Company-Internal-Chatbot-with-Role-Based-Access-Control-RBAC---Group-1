import faiss
import pickle
from sentence_transformers import SentenceTransformer


# ===============================
# LOAD RESOURCES
# ===============================
print("Loading FAISS + Metadata + Model...")

index = faiss.read_index("vector.index")

with open("metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Secure RAG Ready.")


# ===============================
# INTENT KEYWORDS
# ===============================
DEPT_KEYWORDS = {
    "hr": [
        "leave", "salary", "attendance", "benefits",
        "policy", "maternity", "paternity", "payroll"
    ],

    "finance": [
        "budget", "revenue", "profit", "expense",
        "tax", "invoice", "audit", "bonus"
    ],

    "engineering": [
        "system", "api", "authentication", "backend",
        "architecture", "deployment", "database", "server"
    ],

    "marketing": [
        "campaign", "brand", "ads", "leads",
        "promotion", "social", "seo", "customer"
    ]
}


# ===============================
# INTENT DETECTOR
# ===============================
def detect_intent(question: str):

    q = question.lower()

    for dept, words in DEPT_KEYWORDS.items():
        for w in words:
            if w in q:
                return dept

    return None


# ===============================
# RBAC CHECK
# ===============================
def is_allowed(user_role, doc_dept, intent):

    user_role = user_role.lower()
    doc_dept = doc_dept.lower()

    # C-Level: full access
    if user_role == "c-level":
        return True

    # If intent exists and mismatches → block
    if intent and intent != user_role:
        return False

    # Own department
    if user_role == doc_dept:
        return True

    # General only for same intent
    if doc_dept == "general" and intent == user_role:
        return True

    return False


# ===============================
# MAIN SEARCH
# ===============================
def secure_search(query: str, user_role: str, k=5):

    # Encode query
    emb = model.encode([query], convert_to_numpy=True)

    # Search FAISS (fetch more for filtering)
    D, I = index.search(emb, k * 3)

    results = []

    # Detect user intent
    intent = detect_intent(query)

    # Filter results
    for idx in I[0]:

        if idx == -1:
            continue

        doc = metadata[idx]

        doc_dept = doc.get("department", "general")
        roles = doc.get("roles", [])

        # RBAC check
        if not is_allowed(user_role, doc_dept, intent):
            continue

        results.append({
            "text": doc["chunk"],
            "source": doc["file_name"],
            "department": doc_dept,
            "roles": roles
        })

        if len(results) >= k:
            break

    return results


# ===============================
# LOCAL TEST
# ===============================
if __name__ == "__main__":

    print("\n--- HR Test ---")
    r = secure_search("what is sick leave policy", "hr")

    for x in r:
        print(x["source"], "->", x["department"])
