import re

def preprocess_query(query):
    query = query.lower()
    query = re.sub(r"[^a-z0-9\s]", "", query)
    query = re.sub(r"\s+", " ", query).strip()
    return query