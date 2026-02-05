from langchain_community.vectorstores import Chroma
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
    "HR": ["HR", "General"],
    "Finance": ["Finance", "General"],
    "Engineering": ["Engineering", "General"],
    "Marketing": ["Marketing", "General"],
    "Employee": ["General"],
    "C-Level": ["HR", "Finance", "Engineering", "Marketing", "General"]
}

def retrieve_documents(query: str, role: str, k: int = 5):
    raw_results = db.similarity_search_with_score(query, k=k)

    allowed = [d.lower() for d in ROLE_PERMISSIONS[role]]
    authorized = []

    for doc, score in raw_results:
        dept = doc.metadata.get("dept", "").lower()
        if dept in allowed:
            authorized.append((doc, score))

    return authorized
