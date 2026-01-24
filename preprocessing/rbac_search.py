from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


from rbac_config import ROLE_HIERARCHY
from query_utils import normalize_query

CHROMA_DB_DIR = "chroma_db"

# Load embeddings + vector DB once
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma(
    persist_directory=CHROMA_DB_DIR,
    embedding_function=embeddings
)


def rbac_semantic_search(role: str, department: str, query: str, k: int = 5):
    """
    Core RBAC + semantic search logic
    """

    role = role.strip()
    department = department.strip().lower()
    query = normalize_query(query)

    # 1️⃣ Validate role
    if role not in ROLE_HIERARCHY:
        return "Invalid role", []

    # 2️⃣ RBAC enforcement
    allowed_departments = ROLE_HIERARCHY[role]
    if department not in allowed_departments:
        return "Access denied", []

    # 3️⃣ Semantic search with metadata filter
    results = vectordb.similarity_search_with_score(
        query=query,
        k=k,
        filter={"dept": department}
    )

    return "Access granted", results
