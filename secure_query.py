from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from rbac2 import allowed_departments_for

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = np.load("embeddings.npy")
index = faiss.read_index("vector.index")

with open("metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

def secure_search(query, user_role, top_k=5):
    allowed = allowed_departments_for(user_role)
 
    query_emb = model.encode([query], convert_to_numpy=True)
    D, I = index.search(query_emb, k=50)  # top 50 raw matches
 
    results = []
    for idx in I[0]:
        doc = metadata[idx]
        if doc["department"] in allowed:
            results.append(doc)
        if len(results) >= top_k:
            break
 
    return results

if __name__ == "__main__":
    role = input("Enter role: ")
    query = input("Ask anything: ")
    out = secure_search(query, role)
    for r in out:
        print(r["file_name"], "->", r["department"])