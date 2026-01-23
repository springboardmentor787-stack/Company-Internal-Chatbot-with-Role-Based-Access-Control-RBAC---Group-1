import nltk
from nltk.tokenize import sent_tokenize
from loader import load_documents

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

def chunk(text, max_words=150):
    sentences = sent_tokenize(text)
    chunks = []
    current = []

    for sent in sentences:
        words = sent.split()
        if len(current) + len(words) <= max_words:
            current.extend(words)
        else:
            chunks.append(" ".join(current))
            current = words

    if current:
        chunks.append(" ".join(current))

    return chunks

docs = load_documents()
chunked_docs = []

for doc in docs:
    pieces = chunk(doc["content"])
    for idx, piece in enumerate(pieces):
        chunked_docs.append({
            "file_name": doc["file_name"],
            "department": doc["department"],
            "roles": doc["roles"],
            "chunk_index": idx,
            "chunk": piece
        })

print(f"Total chunks: {len(chunked_docs)}")
