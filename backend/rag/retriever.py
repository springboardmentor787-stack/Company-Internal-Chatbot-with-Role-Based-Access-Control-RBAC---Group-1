import chromadb
from sentence_transformers import SentenceTransformer

# -----------------------------
# CONFIG
# -----------------------------
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "docs"

# -----------------------------
# LOAD RESOURCES
# -----------------------------
print("Loading Embedding Model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print(f"Connecting to ChromaDB at '{CHROMA_PATH}'...")
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

def retrieve_chunks(query, role, allowed_departments, top_k=2):
    print(f"--- RETRIEVING for Role: {role} in Depts: {allowed_departments} ---")
    
    # Generate embedding for the query
    query_emb = model.encode(query).tolist()
    
    # Query ChromaDB
    results = collection.query(
        query_embeddings=[query_emb],
        n_results=top_k,
        where={"department": {"$in": allowed_departments}},
        # Crucial Update: We request 'distances' to calculate confidence
        include=["documents", "metadatas", "distances"]
    )
    
    # Check if we found anything
    if not results['documents'] or not results['documents'][0]:
        print("No relevant chunks found.")
        return []

    # Process results
    structured_results = []
    
    for i in range(len(results['documents'][0])):
        chunk_text = results['documents'][0][i]
        metadata = results['metadatas'][0][i]
        distance = results['distances'][0][i]  # Lower distance = Better match
        
        # --- CONFIDENCE CALCULATION ---
        # Chroma uses L2 (Euclidean) distance by default.
        # 0.0 = Exact Match. > 1.5 = Poor Match.
        # Simple heuristic: Convert 0-2 range to percentage
        # Formula: Score = (1 - (distance / 2)) * 100
        # If distance is > 1.5, confidence drops rapidly.
        
        raw_score = (1 - (distance / 1.8))  # 1.8 is a tuning factor for MiniLM
        confidence_pct = max(0, min(100, int(raw_score * 100)))

        structured_results.append({
            "chunk": chunk_text,
            "file_name": metadata.get("file_name", "Unknown"),
            "department": metadata.get("department", "Unknown"),
            "confidence": confidence_pct  # <--- NEW: Sending score to main.py
        })
        
    print(f"Found {len(structured_results)} chunks. Scores: {[r['confidence'] for r in structured_results]}")
    return structured_results