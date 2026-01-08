from langchain_text_splitters import RecursiveCharacterTextSplitter
from load_documents import load_documents


def chunk_documents():
    # Step 1: Load documents (from previous module)
    documents = load_documents()

    # Step 2: Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,      # ~300–512 tokens
        chunk_overlap=50      # preserve context
    )

    # Step 3: Split documents into chunks
    chunks = text_splitter.split_documents(documents)

    print(f"Total chunks created: {len(chunks)}")

    # Optional: inspect one chunk
    sample_chunk = chunks[0]
    print("\nSample chunk metadata:")
    print(sample_chunk.metadata)
    print("\nSample chunk content (first 300 chars):")
    print(sample_chunk.page_content[:300])

    return chunks


if __name__ == "__main__":
    chunk_documents()
