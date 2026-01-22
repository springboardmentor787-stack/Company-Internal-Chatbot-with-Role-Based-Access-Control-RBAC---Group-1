from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from chunk_documents import chunk_documents

PERSIST_DIR = "chroma_db"

def create_chroma_db():
    # Get chunks
    chunks = chunk_documents()

    # Embedding model (meeting specified)
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create Chroma DB (local)
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=PERSIST_DIR
    )

    vectordb.persist()
    print("✅ Chroma DB created successfully.")
    print(f"📁 Vector store location: {PERSIST_DIR}")

    return vectordb


if __name__ == "__main__":
    create_chroma_db()