from document_loaders import all_documents, role_access_mapping                 
from chunking import chunks
from embedding import vector_db
from query_processing import preprocess_query
from rbac_filter import python_rbac_filter
from log_chunks import log_chunks
def run_role_based_query():
    query = input("Enter your query: ").strip()
    role = input("Enter your role (HR / Engineering / Finance / Marketing / C-Level/ General): ").strip()

    if not query or not role:
        print("Query and role are required.")
        return

    query = preprocess_query(query)

    raw_docs = vector_db.similarity_search(query, k=5)

    allowed_docs, blocked_docs = python_rbac_filter(raw_docs, role)

    log_chunks(query, role, raw_docs, allowed_docs, blocked_docs)

    if not allowed_docs:
        print("ACCESS DENIED OR NO RELEVANT DATA FOUND")
        return

    print("\n--- FINAL ANSWER CONTEXT ---")
    for doc in allowed_docs:
        print(doc.page_content[:300])

run_role_based_query()