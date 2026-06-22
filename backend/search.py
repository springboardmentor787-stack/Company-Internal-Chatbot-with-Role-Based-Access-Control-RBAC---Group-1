from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma(
    persist_directory="vectorstore",
    embedding_function=embedding
)

def role_based_search(query, user_role, username):
    docs = vectordb.similarity_search(query, k=5)

    allowed_docs = []
    for doc in docs:
        allowed_roles = doc.metadata.get("allowed_roles", "")
        if user_role in allowed_roles or user_role == "C-Level":
            allowed_docs.append(doc)

    return allowed_docs
