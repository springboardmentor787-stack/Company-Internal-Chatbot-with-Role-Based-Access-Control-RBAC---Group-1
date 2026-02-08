import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("docs")
model = SentenceTransformer("all-MiniLM-L6-v2")

def ask(query, top_k=3):
    query_emb = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_emb],
        n_results=top_k,
        include=["documents", "metadatas"]
    )

    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        print("\n--- RESULT ---")
        print("File:", meta["file_name"])
        print("Dept:", meta["department"])
        print("Roles:", meta["roles"])
        print("Chunk:", doc[:300], "...")
        print("----------------")

# TEST QUERY
ask("Quarterly financial performance of FinSolve in 2024")
