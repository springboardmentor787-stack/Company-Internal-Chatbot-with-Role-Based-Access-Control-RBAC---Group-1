import chromadb
from sentence_transformers import SentenceTransformer

VECTOR_DB_PATH = "data/chroma_db"
COLLECTION_NAME = "chroma_db"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def main():

    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
    collection = client.get_collection(COLLECTION_NAME)

    roles = ["Finance", "HR", "Marketing",
             "Engineering", "Employees", "C-Level"]

    print("\nAvailable roles:")
    for r in roles:
        print(" -", r)

    user_role = input("\nEnter your role: ").strip().lower()
    query = input("Enter your query: ").strip()

    print("\nEmbedding query...")
    query_embedding = model.encode(query).tolist()

    print("Searching vector DB...")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=10,
        include=["documents", "metadatas", "distances"]
    )

    print("\nApplying RBAC filtering...")

    allowed_results = []

    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):

        roles_allowed = [
            r.strip().lower()
            for r in meta["accessible_roles"].split(",")
        ]

        # C-Level override
        if user_role == "c-level" or user_role in roles_allowed:
            allowed_results.append((doc, meta, dist))

    if not allowed_results:
        print("\nNo accessible results found.")
        return

    print("\nTop accessible results:\n")

    for i, (doc, meta, dist) in enumerate(allowed_results, start=1):
        print(f"Result {i}")
        print(f"Source document : {meta['source_document']}")
        print(f"Department      : {meta['department']}")
        print(f"Token count     : {meta['token_count']}")
        print(f"Distance        : {dist:.4f}")
        print("Text:")
        print(doc[:500], "...\n")


if __name__ == "__main__":
    main()


# finance
# Q4 financial report