import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
# Import your document loader and chunker from previous milestones
from load_documents import load_documents_with_metadata
from chunking import chunk_documents 

# --- CONFIGURATION (Must match search script) ---
DB_PATH = "db/chroma_global"
COLLECTION = "company_documents"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def build_database():
    # 1. Initialize Model
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    
    # 2. Load and Chunk Data
    print("Loading documents...")
    raw_docs = load_documents_with_metadata()
    print(f"Found {len(raw_docs)} documents. Chunking...")
    chunks = chunk_documents(raw_docs)
    
    # 3. Clear old DB if it exists (To prevent duplicate/messy data)
    if os.path.exists(DB_PATH):
        import shutil
        shutil.rmtree(DB_PATH)

    # 4. Create and Save to Chroma
    print(f"Storing {len(chunks)} chunks into {DB_PATH}...")
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH,
        collection_name=COLLECTION
    )
    print("✅ Database built successfully!")

if __name__ == "__main__":
    build_database()