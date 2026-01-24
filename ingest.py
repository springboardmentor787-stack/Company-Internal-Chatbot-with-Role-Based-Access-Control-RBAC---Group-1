# ingest/ingest.py

from ingest.loaders import load_documents
from ingest.chunker import chunk_documents
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

BASE_DATA_PATH = "data"
CHROMA_DB_DIR = "chroma_db"


def main():
    print("Loading documents...")
    documents = load_documents(BASE_DATA_PATH)
    print(f"Loaded documents: {len(documents)}")

    print("Chunking documents...")
    chunks = chunk_documents(documents)
    print(f"Total chunks created: {len(chunks)}")

    print("Generating embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Storing in ChromaDB...")
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR,
    )

    print("Ingestion completed successfully.")


if __name__ == "__main__":
    main()
