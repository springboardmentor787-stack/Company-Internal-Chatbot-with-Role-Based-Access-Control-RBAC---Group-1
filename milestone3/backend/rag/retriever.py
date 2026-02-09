import chromadb
from sentence_transformers import SentenceTransformer

VECTOR_DB_PATH = "data/chroma_db"
COLLECTION_NAME = "chroma_db"

embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
collection = client.get_collection(COLLECTION_NAME)

def retrieve_chunks(query: str, user_role: str):
    query_emb = embedder.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_emb],
        n_results=6,
        include=["documents", "metadatas", "distances"]
    )

    chunks = []
    distances = []

    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        allowed = [r.lower() for r in meta["accessible_roles"].split(",")]

        if user_role.lower() == "c-level":
            pass
        elif user_role.lower() not in allowed:
            continue

        chunks.append({
            "text": doc,
            "source": meta["source_document"],
            "distance": dist
        })
        distances.append(dist)

    if not chunks:
        raise PermissionError("Access denied")

    confidence = round(1 / (1 + sum(distances) / len(distances)), 2)
    return chunks[:3], confidence
