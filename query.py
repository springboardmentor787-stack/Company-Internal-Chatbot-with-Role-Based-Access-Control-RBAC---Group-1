import re

def normalize_query(query: str) -> str:
    """
    Normalize user query for better semantic search.
    """
    query = query.lower()
    query = query.strip()
    query = re.sub(r"\s+", " ", query)
    return query