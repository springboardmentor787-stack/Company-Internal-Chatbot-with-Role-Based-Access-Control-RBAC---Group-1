import re
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    collection_name="company_documents",
    embedding_function=embedding_model,
    persist_directory="db/chroma_global"
)

ROLE_PERMISSIONS = {
    "HR": ["HR"],
    "Finance": ["Finance"],
    "Marketing": ["Marketing"],
    "Engineering": ["Engineering"],
    "Employee": ["General"],
    "C-Level": ["HR", "Finance", "Marketing", "Engineering", "General"]
}

user_role = input("Enter your role: ").strip()
raw_query = input("Enter your query: ").strip()

if user_role not in ROLE_PERMISSIONS:
    print("Invalid role")
    exit()

normalized_query = re.sub(r"\s+", " ", raw_query.lower()).strip()

raw_results = db.similarity_search(normalized_query, k=10)

allowed_departments = [
    dept.lower() for dept in ROLE_PERMISSIONS[user_role]
]

authorized_results = []

for doc in raw_results:
    doc_dept = doc.metadata.get("dept", "").lower()

    if user_role == "C-Level":
        authorized_results.append(doc)
    elif doc_dept in allowed_departments:
        authorized_results.append(doc)


print("\n=========== SEARCH SUMMARY ===========")
print("User Role          :", user_role)
print("Query              :", raw_query)
print("Normalized Query   :", normalized_query)
print("------------------------------------")
print("Total Results      :", len(raw_results))
print("Authorized Results :", len(authorized_results))
print("------------------------------------")

if not authorized_results:
    print("Access Decision    : DENIED (RBAC)")
    exit()

print("Access Decision    : GRANTED\n")

for i, doc in enumerate(authorized_results, 1):
    print(f"Result {i}")
    print("Source     :", doc.metadata.get("source"))
    print("Department :", doc.metadata.get("dept"))
    print(doc.page_content[:200])
    print("-" * 60)
