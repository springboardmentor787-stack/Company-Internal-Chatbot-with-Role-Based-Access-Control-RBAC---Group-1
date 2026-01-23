import os
import sys

# ---------------- PATH FIX (MUST BE FIRST) ----------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(PROJECT_ROOT)

from langchain_chroma import Chroma
from backend.app.role_mapping import ROLE_MAP
from backend.app.embeddings import get_embeddings


# ---------------- CONFIG ----------------
DB_BASE_PATH = os.path.join(PROJECT_ROOT, "db")

# ---------------- ROLE KEYWORDS (STRICT FOR SENSITIVE ROLES) ----------------
ROLE_KEYWORDS = {
    "Finance": [
        "revenue", "revenues", "profit", "profits", "loss", "losses",
        "income", "expense", "expenses",
        "quarter", "quarterly", "financial", "finance",
        "budget", "forecast", "growth", "earnings",
        "margin", "tax", "investment", "roi",
        "balance sheet", "cash flow"
    ],
    "HR": [
        "employee", "employees",
        "attendance", "attendance percentage",
        "leave", "leave balance",
        "salary", "compensation",
        "date of joining", "date of birth",
        "manager", "department", "email", "location"
    ],
    "Engineering": [],
    "Marketing": [],
    "Employees": [],
    "C-Level": []
}

# ---------------- GENERAL (COMPANY-WIDE) KEYWORDS ----------------
GENERAL_KEYWORDS = [
    "company", "vision", "mission",
    "policy", "policies",
    "handbook", "guidelines",
    "code of conduct", "rules",
    "working hours", "leave policy"
]


# ---------------- QUERY INTENT CHECK ----------------
def query_matches_role(role: str, query: str) -> bool:
    if role == "C-Level":
        return True

    query_lower = query.lower()

    # Allow general/company-wide queries for all roles
    if any(gk in query_lower for gk in GENERAL_KEYWORDS):
        return True

    # Strict intent for sensitive roles
    if role in ["Finance", "HR"]:
        keywords = ROLE_KEYWORDS.get(role, [])
        return any(kw in query_lower for kw in keywords)

    return True


# ---------------- LOAD ALL DB PATHS ----------------
def get_all_db_paths():
    paths = []
    for folder in os.listdir(DB_BASE_PATH):
        folder_path = os.path.join(DB_BASE_PATH, folder)
        if os.path.isdir(folder_path):
            paths.append(folder_path)
    return paths


# ---------------- SEMANTIC SEARCH ----------------
def semantic_search():
    role = input("Enter your role: ").strip()
    query = input("Enter your query: ").strip()

    if not query or not query_matches_role(role, query):
        print("\n❌ Access Denied")
        print("Total documents returned: 0")
        print("Total chunks searched: 0")
        return

    query_lower = query.lower()
    is_general_query = any(gk in query_lower for gk in GENERAL_KEYWORDS)

    db_paths = get_all_db_paths()
    if not db_paths:
        print("\n❌ Access Denied")
        print("Total documents returned: 0")
        print("Total chunks searched: 0")
        return

    embeddings = get_embeddings()
    allowed_departments = ROLE_MAP.get(role, [])
    all_results = []
    total_chunks = 0

    # ---------- SEARCH ----------
    for path in db_paths:
        # 🔑 KEY FIX: Route general queries ONLY to general DB
        if is_general_query and "general" not in path.lower():
            continue

        db = Chroma(
            persist_directory=path,
            embedding_function=embeddings
        )

        total_chunks += db._collection.count()

        try:
            search_results = db.similarity_search(query, k=20)
        except Exception:
            continue

        for r in search_results:
            doc_dept = (
                r.metadata.get("department")
                or r.metadata.get("role")
                or ""
            ).lower()

            if role != "C-Level" and doc_dept not in allowed_departments:
                continue

            all_results.append(r)

    if not all_results:
        print("\n❌ Access Denied")
        print("Total documents returned: 0")
        print("Total chunks searched: 0")
        return

    # ---------- DEDUPLICATE ----------
    seen = set()
    final_results = []

    for r in all_results:
        unique_key = (
            r.metadata.get("source"),
            r.metadata.get("row", None)
        )

        if unique_key not in seen:
            seen.add(unique_key)
            final_results.append(r)

        if len(final_results) == 5:
            break

    # ---------- OUTPUT ----------
    print("\n✅ Top 5 Semantic Search Results:\n")

    for i, r in enumerate(final_results, 1):
        snippet = r.page_content[:350].replace("\n", " ")
        print(f"{i}. Source: {r.metadata.get('source')}")
        print(f"   Snippet: {snippet}...\n")

    print(f"Total documents returned: {len(final_results)}")
    print(f"Total chunks searched: {total_chunks}")


# ---------------- RUN ----------------
if __name__ == "__main__":
    semantic_search()




# Finance
# What was the quarterly revenue growth last year?
# Show employee attendance and leave balance details.

# HR
# Show employee attendance percentage and leave balance.
# What was the company’s quarterly profit?

# Engineering
# Explain the system architecture used by the engineering team.
# What was the marketing campaign budget?

#General(Finance , HR, Engineering, Marketing.....)
# What is the Company Vision and Mission?
#What is company core values

