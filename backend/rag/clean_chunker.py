from loader import load_documents


# ---------------------------
# HR CSV CHUNKER
# ---------------------------

def chunk_hr_csv(content):

    lines = [l.strip() for l in content.splitlines() if l.strip()]

    if len(lines) < 2:
        return []

    # Detect separator
    if "|" in lines[0]:
        sep = "|"
    elif "," in lines[0]:
        sep = ","
    else:
        return []

    headers = [h.strip() for h in lines[0].split(sep)]

    chunks = []

    for row in lines[1:]:

        cols = [c.strip() for c in row.split(sep)]

        if len(cols) != len(headers):
            continue

        parts = []

        for i in range(len(headers)):
            parts.append(f"{headers[i]}: {cols[i]}")

        chunks.append("\n".join(parts))

    return chunks


# ---------------------------
# MARKDOWN CHUNKER
# ---------------------------

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


# ===========================
# MAIN PIPELINE (GLOBAL)
# ===========================

docs = load_documents()

chunked_docs = []


for doc in docs:

    # HR CSV
    if doc["file_name"].endswith(".csv") and doc["department"] == "hr":

        entries = chunk_hr_csv(doc["content"])

        for entry in entries:

            chunked_docs.append({
                "file_name": doc["file_name"],
                "department": doc["department"],
                "roles": doc["roles"],
                "chunk": entry
            })


    # OTHER FILES
    else:

        chunks = chunk_markdown(doc["content"])

        for c in chunks:

            chunked_docs.append({
                "file_name": doc["file_name"],
                "department": doc["department"],
                "roles": doc["roles"],
                "chunk": c
            })


# ===========================
# DEBUG
# ===========================

print(f"Total chunks created: {len(chunked_docs)}")

print("\n--- SAMPLE HR CHUNKS ---")

count = 0

for d in chunked_docs:

    if d["department"] == "hr":

        print(d["chunk"])
        print("------")

        count += 1

    if count == 5:
        break
