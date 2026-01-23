import nltk
from nltk.tokenize import sent_tokenize
from loader import parsed_documents

nltk.download("punkt")
nltk.download("punkt_tab")

def clean_text(text):
    cleaned = (
        text.replace("\n", " ")
        .replace("#", " ")
        .replace("|", " ")
        .replace("*", " ")
    )
    return " ".join(cleaned.split())

def chunk_text(text, max_len=800):
    sentences = sent_tokenize(text)
    chunks = []
    current = ""

    for s in sentences:
        if len(current) + len(s) <= max_len:
            current += " " + s
        else:
            chunks.append(current.strip())
            current = s

    if current:
        chunks.append(current.strip())

    return chunks

cleaned_chunks = []

for doc in parsed_documents:
    chunks = chunk_text(doc["content"])
    for idx, chunk in enumerate(chunks):
        cleaned_chunks.append({
            "file_name": doc["file_name"],
            "department": doc["department"],
            "roles": doc["roles"],
            "chunk_index": idx,
            "chunk": clean_text(chunk)
        })

print("Total cleaned chunks:", len(cleaned_chunks))
