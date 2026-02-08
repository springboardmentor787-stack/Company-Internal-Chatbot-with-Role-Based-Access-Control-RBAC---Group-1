from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from chunker import chunked_docs

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [doc["chunk"] for doc in chunked_docs]
embeddings = model.encode(texts, convert_to_numpy=True)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Save metadata separately
metadata = chunked_docs

np.save("embeddings.npy", embeddings)
faiss.write_index(index, "vector.index")

import pickle
with open("metadata.pkl", "wb") as f:
    pickle.dump(metadata, f)

print("Embedding & index build complete!")
print("Total embeddings:", len(embeddings))
