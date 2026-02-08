import csv
from pathlib import Path
from loader import load_documents

def chunk_hr_csv(content):
    lines = content.split("\n")
    if not lines:
        return []

    headers = lines[0].split("|")
    headers = [h.strip() for h in headers if h.strip()]  # Clean headers

    chunks = []
    for row in lines[1:]:
        cols = row.split("|")
        # clean columns
        cols = [c.strip() for c in cols if c.strip()]
        
        if len(cols) != len(headers):
            continue
        
        # CREATE READABLE TEXT INSTEAD OF DICT
        # Example: "Leave Type: Casual\nEntitlement: 12 Days"
        entry_text = "\n".join([f"{headers[i]}: {cols[i]}" for i in range(len(headers))])
        chunks.append(entry_text)
        
    return chunks

def chunk_markdown(text, max_words=120):
    words = text.split()
    chunks = []
    current = []
    for w in words:
        if len(current) < max_words:
            current.append(w)
        else:
            chunks.append(" ".join(current))
            current = [w]
    if current:
        chunks.append(" ".join(current))
    return chunks

# Main Processing Logic
docs = load_documents()
chunked_docs = []

for doc in docs:
    if doc["file_name"].endswith(".csv") and doc["department"] == "hr":
        entries = chunk_hr_csv(doc["content"])
        for entry in entries:
            chunked_docs.append({
                "file_name": doc["file_name"],
                "department": doc["department"],
                "roles": doc["roles"],
                "chunk": entry  # Now this is clean text, not a dict string
            })
    else:
        chunks = chunk_markdown(doc["content"])
        for c in chunks:
            chunked_docs.append({
                "file_name": doc["file_name"],
                "department": doc["department"],
                "roles": doc["roles"],
                "chunk": c
            })

print(f"Total chunks: {len(chunked_docs)}")