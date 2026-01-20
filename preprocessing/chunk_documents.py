from langchain_text_splitters import RecursiveCharacterTextSplitter
from load_documents import load_documents_with_metadata
from clean_documents import clean_documents


# ==========================================
# CHUNK DOCUMENTS (ALL DEPARTMENTS)
# ==========================================

def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,      # size of each chunk
        chunk_overlap=60     # overlap to preserve context
    )

    chunks = splitter.split_documents(documents)
    return chunks



# VERIFICATION

if __name__ == "__main__":
    # Step 1: Load documents (ALL departments)
    docs = load_documents_with_metadata()

    # Step 2: Clean documents (ALL departments)
    cleaned_docs = clean_documents(docs)

    # Step 3: Chunk documents (ALL departments)
    chunks = chunk_documents(cleaned_docs)

    print(f"Documents before chunking: {len(cleaned_docs)}")
    print(f"Total chunks created: {len(chunks)}")

    # Show sample chunk from EACH department
    print("\nSample chunk metadata per department:")
    seen = set()
    for chunk in chunks:
        dept = chunk.metadata["dept"]
        if dept not in seen:
            print(chunk.metadata)
            seen.add(dept)

        if len(seen) == 5:   # engineering, finance, hr, marketing, general
            break  