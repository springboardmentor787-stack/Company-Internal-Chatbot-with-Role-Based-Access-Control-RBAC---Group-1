from secure_query import secure_search


def retrieve_chunks(query: str, role: str, top_k: int = 5):
    return secure_search(query, role, top_k)
