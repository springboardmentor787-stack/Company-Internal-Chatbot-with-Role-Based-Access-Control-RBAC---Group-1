from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    collection_name="fintech_docs",
    persist_directory="chroma_db",
    embedding_function=embedding_model
)

print("📦 Total vectors in DB:", vectorstore._collection.count())
