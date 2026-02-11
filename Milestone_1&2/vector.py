import os
import shutil
import time
# Importing the FUNCTIONS from your previous scripts
from load_documents import load_documents_with_metadata
from chunking import chunk_documents 

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# --- CONFIGURATION ---
DB_PATH = "db/chroma_global"
COLLECTION_NAME = "company_documents"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def build_vector_db():
    # 1. Initialize the Embedding Model
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)

    # 2. Load and Chunk Data (Freshly called here)
    print("Loading raw documents...")
    raw_docs = load_documents_with_metadata()
    
    print(f"Chunking {len(raw_docs)} documents...")
    chunks = chunk_documents(raw_docs)

    # 3. Clean Metadata for Chroma compatibility
    # Chroma cannot store lists; we convert them to strings
    clean_chunks = []
    for doc in chunks:
        d = doc.copy()
        for key, value in d.metadata.items():
            if isinstance(value, list):
                d.metadata[key] = ",".join(map(str, value))
        clean_chunks.append(d)

    # 4. Create and Save Database
    print(f"Ingesting {len(clean_chunks)} chunks into ChromaDB...")
    db = Chroma.from_documents(
        documents=clean_chunks,
        embedding=embeddings,
        persist_directory=DB_PATH,
        collection_name=COLLECTION_NAME
    )

    print("\n" + "="*30)
    print("INGESTION COMPLETE")
    print(f"Total Vectors Stored: {db._collection.count()}")
    print("="*30)

if __name__ == "__main__":
    build_vector_db()