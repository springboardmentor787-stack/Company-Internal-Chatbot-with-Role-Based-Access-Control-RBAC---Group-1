import re
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# --- CONFIGURATION (Must match storage script) ---
DB_PATH = "db/chroma_global"
COLLECTION = "company_documents"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# 1. Initialize Model & Connect to DB
embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
db = Chroma(
    collection_name=COLLECTION,
    embedding_function=embeddings,
    persist_directory=DB_PATH
)

# 2. Access Rules
ROLE_PERMISSIONS = {
    "HR": ["HR"],
    "Finance": ["Finance"],
    "Engineering": ["Engineering"],
    "C-Level": ["HR", "Finance", "Engineering", "General"]
}

# 3. User Input
user_role = input("Enter Role: ").strip()
raw_query = input("Enter Query: ").strip()

# Check if role exists
if user_role not in ROLE_PERMISSIONS:
    print("❌ Invalid Role.")
    exit()

# 4. Search & Filter
# Total results in DB check
total_in_db = db._collection.count()
print(f"DEBUG: Items currently in Database: {total_in_db}")

# Similarity Search
normalized_query = re.sub(r"\s+", " ", raw_query.lower()).strip()
raw_results = db.similarity_search(normalized_query, k=5)

# RBAC Filter
allowed_depts = [d.lower() for d in ROLE_PERMISSIONS[user_role]]
authorized_results = []

for doc in raw_results:
    doc_dept = doc.metadata.get("dept", "").lower()
    if user_role == "C-Level" or doc_dept in allowed_depts:
        authorized_results.append(doc)

# 5. Final Output
print("\n" + "="*30)
print(f"ROLE: {user_role}")
print(f"TOTAL MATCHES FOUND: {len(raw_results)}")
print(f"AUTHORIZED RESULTS: {len(authorized_results)}")
print("="*30)

if not authorized_results:
    print("ACCESS DECISION: DENIED")
else:
    print("ACCESS DECISION: GRANTED\n")
    for i, doc in enumerate(authorized_results, 1):
        print(f"[{i}] {doc.metadata.get('source')} (Dept: {doc.metadata.get('dept')})")
        print(f"Content: {doc.page_content[:150]}...\n")


#--------Querys 
# 1.API Documentation and deployment
# 2.Employee onboarding policy
# 3.Q4 Revenue 2025
# ----------#
#Enter Role: Finance
#Enter Query: insurance claim approval process
#Enter Role: HR ((Wrong))
#Enter Query: insurance claim approval process
#Enter Query: Employee onboarding policy
#Enter Role: C-Level
#Enter Query: system architecture

