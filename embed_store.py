import chromadb
from clean_chunker import chunked_docs
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="chroma_db")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create or reset collection
try:
    client.delete_collection("docs")
except:
    pass

collection = client.create_collection(
    name="docs",
    metadata={"hnsw:space": "cosine"}
)

for i, doc in enumerate(chunked_docs):
    embedding = model.encode(doc["chunk"]).tolist()
    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[doc["chunk"]],
        metadatas=[{
            "file_name": doc["file_name"],
            "department": doc["department"],
            "roles": ",".join(doc["roles"])   # store roles as string
        }]
    )

print(f"Stored {len(chunked_docs)} chunks into ChromaDB")
