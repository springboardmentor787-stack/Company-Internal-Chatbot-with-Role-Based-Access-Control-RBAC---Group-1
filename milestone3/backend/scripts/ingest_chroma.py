import json
import os
import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_PATH = "data/processed/chunks.jsonl"
EMBEDDED_PATH = "data/processed/chunks_with_embeddings.jsonl"

VECTOR_DB_PATH = "data/chroma_db"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
COLLECTION_NAME = "chroma_db"


def main():
    if not os.path.exists(CHUNKS_PATH):
        print(f"Missing file: {CHUNKS_PATH}")
        return

    os.makedirs(VECTOR_DB_PATH, exist_ok=True)

    print("Loading chunks...")
    chunks = [json.loads(line) for line in open(CHUNKS_PATH, encoding="utf-8")]

    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Initializing ChromaDB...")
    client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    records = []

    for chunk in chunks:
        embedding = model.encode(chunk["text"]).tolist()

        department = chunk["department"]

        if department.lower() == "general":
            accessible_roles = [
                "Employees", "Finance", "HR",
                "Marketing", "Engineering", "C-Level"
            ]
        else:
            accessible_roles = [department, "C-Level"]

        collection.add(
            ids=[chunk["chunk_id"]],
            documents=[chunk["text"]],
            embeddings=[embedding],
            metadatas=[{
                "source_document": chunk["source_document"],
                "department": department,
                "accessible_roles": ",".join(accessible_roles),  # ✅ REQUIRED
                "token_count": chunk["token_count"]
            }]
        )

        records.append({**chunk, "embedding": embedding})

    os.makedirs(os.path.dirname(EMBEDDED_PATH), exist_ok=True)
    with open(EMBEDDED_PATH, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    print("✅ ChromaDB ingestion complete")
    print(f"Total chunks stored: {len(records)}")


if __name__ == "__main__":
    main()
