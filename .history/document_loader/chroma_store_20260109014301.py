from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from chunk_documents import chunk_documents

PERSIST_DIR = "chroma_db"

def create_chroma_db():
    # Step 1: Get chunks
    chunks = chunk_documents()

    # Step 2: Load embedding model
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Step 3: Store in Chroma
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=PERSIST_DIR
    )

    vectordb.persist()
    print("Chroma DB created successfully.")

    return vectordb


if __name__ == "__main__":
    create_chroma_db()
