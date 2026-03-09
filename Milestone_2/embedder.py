import json
import os
from sentence_transformers import SentenceTransformer
import chromadb

CHUNKS_PATH = "data/processed/chunks.jsonl"
EMBEDDED_PATH = "data/processed/chunks_with_embeddings.jsonl"

VECTOR_DB_PATH = "data/chroma_db"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
COLLECTION_NAME = "chroma_db"


# ---------- LOADERS ----------

def load_chunks(path):
    chunks = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))
    return chunks


def load_embedding_cache(path):
    cache = {}
    if not os.path.exists(path):
        return cache

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            cache[record["chunk_id"]] = record
    return cache


def save_embedding_cache(records, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


# ---------- MAIN ----------

def main():

    print("Loading chunks...")
    chunks = load_chunks(CHUNKS_PATH)

    print("Loading embedding cache...")
    cache = load_embedding_cache(EMBEDDED_PATH)

    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Initializing ChromaDB (persistent)...")
    client = chromadb.PersistentClient(path=VECTOR_DB_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    updated_records = []

    for chunk in chunks:

        chunk_id = chunk["chunk_id"]

        # ---------- CACHE ----------
        if chunk_id in cache:
            embedding = cache[chunk_id]["embedding"]
            record = cache[chunk_id]
        else:
            embedding = model.encode(chunk["text"]).tolist()
            record = {**chunk, "embedding": embedding}

        updated_records.append(record)

        department = chunk["department"]

        # ---------- RBAC ROLES ----------
        if department.lower() == "general":
            roles = [
                "Employees", "Finance", "HR",
                "Marketing", "Engineering", "C-Level"
            ]
        else:
            roles = [department, "C-Level"]

        # ---------- STORE ----------
        collection.add(
            ids=[chunk_id],
            embeddings=[embedding],
            documents=[chunk["text"]],
            metadatas=[{
                "source_document": chunk["source_document"],
                "department": department,
                "accessible_roles": ",".join(roles),
                "token_count": chunk["token_count"]
            }]
        )

    save_embedding_cache(updated_records, EMBEDDED_PATH)

    print(f"Embedded {len(updated_records)} chunks")
    print(f"Saved cache to: {EMBEDDED_PATH}")
    print(f"Vector DB stored at: {VECTOR_DB_PATH}")


if __name__ == "__main__":
    main()