# embed_store.py

import chromadb
from sentence_transformers import SentenceTransformer
from clean_chunker import chunked_docs


print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Init Chroma
client = chromadb.PersistentClient(path="chroma_db")

# Remove old collection safely
try:
    client.delete_collection("docs")
    print("Old collection deleted.")
except:
    print("No old collection found.")

collection = client.create_collection("docs")

print("Storing documents in Chroma...")


for i, doc in enumerate(chunked_docs):

    text = doc["chunk"]

    embedding = model.encode(text).tolist()

    # ✅ Convert roles list → string
    roles_str = ",".join([r.lower().strip() for r in doc["roles"]])

    metadata = {
        "file_name": doc["file_name"],
        "department": doc["department"].lower().strip(),
        "roles": roles_str      # <-- now string, not list
    }

    collection.add(
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata],
        ids=[str(i)]
    )


print("✅ Chroma DB built successfully!")
print("Total documents:", collection.count())
