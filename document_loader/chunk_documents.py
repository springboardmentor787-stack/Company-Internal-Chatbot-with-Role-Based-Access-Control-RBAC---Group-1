from langchain_text_splitters import RecursiveCharacterTextSplitter
from document_loader.load_documents import load_documents


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
    for idx, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = idx


    print(f"Total chunks created: {len(chunks)}")

    

    return chunks


if __name__ == "__main__":
    chunk_documents()
