# Handles embedding + vector DB creation

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from load_documents import load_documents_with_metadata
from clean_documents import clean_documents
from chunk_documents import chunk_documents


# =====================================================
# CONFIG
# =====================================================

CHROMA_DB_DIR = "chroma_db"

# Load embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# =====================================================
# EMBEDDING FUNCTION
# =====================================================

def embed_documents_if_needed():
    """
    Creates embeddings and stores them in Chroma DB
    only if the database is empty.
    """

    # Load existing DB (if any)
    vectordb = Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embeddings
    )

    # Skip embedding if DB already has data
    if vectordb._collection.count() > 0:
        print("✅ Chroma DB already exists. Skipping embedding.")
        return vectordb

    print("⚠️ No existing DB found. Creating embeddings...")

    # Step 1: Load documents
    docs = load_documents_with_metadata()

    # Step 2: Clean documents
    docs = clean_documents(docs)

    # Step 3: Chunk documents
    chunks = chunk_documents(docs)

    print(f"📄 Documents loaded: {len(docs)}")
    print(f"🧩 Chunks created: {len(chunks)}")

    # Step 4: Create vector DB (auto-persisted)
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR
    )

    print("✅ Documents embedded and stored in Chroma DB")

    return vectordb


# =====================================================
# RUN DIRECTLY (OPTIONAL TEST)
# =====================================================

if __name__ == "__main__":
    print("🚀 Starting embedding process...")
    embed_documents_if_needed()
