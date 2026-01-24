import time
from scripts.vector_store import load_vector_db, validate_vector_db
from query import normalize_query

TOP_K = 5

def semantic_search(query: str):
    vectordb = load_vector_db()
    validate_vector_db(vectordb)

    query = normalize_query(query)

    start = time.time()
    results = vectordb.similarity_search_with_score(query, k=TOP_K)
    latency = round((time.time() - start) * 1000, 2)

    print(f"\n🔍 Query: {query}")
    print(f"⏱️ Latency: {latency} ms")

    for i, (doc, score) in enumerate(results, start=1):
        print(f"\nResult {i}")
        print("Score:", round(score, 4))
        print("Role:", doc.metadata["role"])
        print("Source:", doc.metadata["source"])
        print("Preview:", doc.page_content[:150])

    return latency, results


if __name__ == "__main__":
    q = input("Enter query: ")
    semantic_search(q)