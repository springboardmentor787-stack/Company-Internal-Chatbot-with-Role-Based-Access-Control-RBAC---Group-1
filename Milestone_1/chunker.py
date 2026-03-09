import nltk
from nltk.tokenize import sent_tokenize
import tiktoken
import json
import os

from metadata import load_role_mapping, infer_department, get_allowed_roles
from io_utils import list_documents, read_markdown, read_csv
from cleaner import clean_text

# download tokenizer
nltk.download("punkt", quiet=True)

ENCODER = tiktoken.get_encoding("cl100k_base")

RAW_DATA_DIR = "data/raw"
ROLE_CONFIG_PATH = "config/role_mapping.yaml"
OUTPUT_PATH = "data/processed/chunks.jsonl"


# ---------------- TOKEN HELPERS ---------------- #

def count_tokens(text: str) -> int:
    if not text.strip():
        return 0
    return len(ENCODER.encode(text))


def trim_to_last_tokens(text: str, max_tokens: int) -> str:
    tokens = ENCODER.encode(text)
    return ENCODER.decode(tokens[-max_tokens:])


def hard_trim_to_max(text: str, max_tokens: int) -> str:
    tokens = ENCODER.encode(text)
    return ENCODER.decode(tokens[:max_tokens])


# ---------------- CHUNKING ---------------- #

def chunk_text(text, min_tokens=300, max_tokens=512, overlap_tokens=50):

    sentences = sent_tokenize(text)

    chunks = []
    current_chunk = []
    current_tokens = 0

    # ---------- BUILD INITIAL CHUNKS ----------
    for sentence in sentences:
        sentence_tokens = count_tokens(sentence)

        if sentence_tokens == 0:
            continue

        if current_tokens + sentence_tokens > max_tokens:
            chunk = " ".join(current_chunk).strip()

            if count_tokens(chunk) > 0:
                chunks.append(hard_trim_to_max(chunk, max_tokens))

            overlap = trim_to_last_tokens(chunk, overlap_tokens)
            current_chunk = [overlap, sentence]
            current_tokens = count_tokens(overlap) + sentence_tokens
        else:
            current_chunk.append(sentence)
            current_tokens += sentence_tokens

    # last chunk
    if current_chunk:
        chunk = " ".join(current_chunk).strip()
        if count_tokens(chunk) > 0:
            chunks.append(hard_trim_to_max(chunk, max_tokens))

    # ---------- FIX SMALL CHUNKS (<300 TOKENS) ----------
    final_chunks = []

    for chunk in chunks:
        tokens = count_tokens(chunk)

        if tokens < min_tokens and final_chunks:
            merged = final_chunks[-1] + " " + chunk
            merged = hard_trim_to_max(merged, max_tokens)

            if count_tokens(merged) <= max_tokens:
                final_chunks[-1] = merged
            else:
                final_chunks.append(chunk)
        else:
            final_chunks.append(chunk)

    return final_chunks


# ---------------- MAIN ---------------- #

def main():
    print("Chunking documents...\n")

    documents = list_documents(RAW_DATA_DIR)
    role_config = load_role_mapping(ROLE_CONFIG_PATH)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    total_chunks = 0
    all_chunk_records = []

    for doc in documents:

        if doc.endswith(".md"):
            raw_content = read_markdown(doc)
        elif doc.endswith(".csv"):
            raw_content = read_csv(doc)
        else:
            continue

        cleaned_content = clean_text(raw_content)
        chunks = chunk_text(cleaned_content)

        department = infer_department(doc, role_config)
        allowed_roles = get_allowed_roles(department, role_config)

        print(f"\nChunked: {doc}")
        print(f"Department: {department}")
        print(f"Allowed roles: {allowed_roles}")

        for i, chunk in enumerate(chunks, start=1):

            tokens = count_tokens(chunk)

            # safety skip
            if tokens == 0:
                continue

            chunk_id = f"{os.path.basename(doc)}_{i:03d}"

            record = {
                "chunk_id": chunk_id,
                "text": chunk,
                "source_document": os.path.basename(doc),
                "department": department,
                "accessible_roles": allowed_roles,
                "token_count": tokens,
            }

            all_chunk_records.append(record)

            print(f"Chunk {i}: {tokens} tokens → {chunk_id}")

        total_chunks += len(chunks)

    # save JSONL
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for record in all_chunk_records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print("\n✅ Total chunks:", total_chunks)
    print("✅ Saved to:", OUTPUT_PATH)


if __name__ == "__main__":
    main()