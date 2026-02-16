from sentence_transformers import SentenceTransformer


# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


# -------------------------
# EMBED TEXT
# -------------------------

def embed_text(text: str):

    if not text:
        return []

    embedding = model.encode(text)

    return embedding.tolist()
