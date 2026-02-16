import os
import chromadb
from sentence_transformers import SentenceTransformer
from clean_chunker import chunked_docs  # Imports your processed data

# -----------------------------
# CONFIG
# -----------------------------
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "docs"

# -----------------------------
# 1. SETUP DATABASE (NO DELETION)
# -----------------------------
print(f"Connecting to ChromaDB at '{CHROMA_PATH}'...")

# We do NOT use shutil.rmtree() here, so your folder stays safe.
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

# -----------------------------
# 2. LOAD MODEL
# -----------------------------
print("Loading Embedding Model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# 3. PROCESS & INDEX DATA
# -----------------------------
if not chunked_docs:
    print("❌ ERROR: No documents found! Check your 'loader.py' and 'data/' folder.")
    exit()

print(f"Found {len(chunked_docs)} chunks. preparing data...")

ids = []
documents = []
metadatas = []
embeddings = []

for i, doc in enumerate(chunked_docs):
    
    # Prepare data
    chunk_text = doc["chunk"]
    file_name = doc["file_name"]
    dept = doc["department"]
    
    # Handle Roles (Convert list to string for Chroma compatibility)
    roles = doc["roles"]
    if isinstance(roles, list):
        roles_str = str(roles)
    else:
        roles_str = str(roles)

    # Create a unique ID for each chunk
    # (Using doc_i means re-running this script updates existing entries)
    ids.append(f"doc_{i}")
    
    documents.append(chunk_text)
    
    metadatas.append({
        "file_name": file_name,
        "department": dept,
        "roles": roles_str
    })
    
    # Generate Embedding
    emb = model.encode(chunk_text).tolist()
    embeddings.append(emb)

# -----------------------------
# 4. UPSERT TO CHROMA
# -----------------------------
print(f"Upserting {len(documents)} chunks into database...")

# .upsert() will update existing IDs and add new ones
collection.upsert(
    ids=ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas
)

print(f"✅ Success! Updated database with {len(documents)} documents.")
print("You can now restart your server: 'uvicorn main:app --reload'")