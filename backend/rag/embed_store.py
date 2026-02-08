import chromadb
from sentence_transformers import SentenceTransformer
from clean_chunker import chunked_docs

client = chromadb.PersistentClient(path="chroma_db")
try:
    client.delete_collection("docs")
except:
    pass

collection = client.create_collection(name="docs", metadata={"hnsw:space": "cosine"})
encoder = SentenceTransformer("all-MiniLM-L6-v2")

for i, doc in enumerate(chunked_docs):
    emb = encoder.encode(doc["chunk"]).tolist()
    collection.add(
        ids=[str(i)],
        embeddings=[emb],
        documents=[doc["chunk"]],
        metadatas=[{
            "file_name": doc["file_name"],
            "department": doc["department"],
            "roles": ",".join(doc["roles"])
        }]
    )

print(f"[OK] Stored {len(chunked_docs)} chunks in ChromaDB")
