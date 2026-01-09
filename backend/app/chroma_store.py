from langchain_community.vectorstores import Chroma
from langchain_text_splitters import TokenTextSplitter
from backend.app.embeddings import get_embeddings


def build_vector_store(documents, persist_dir):
    splitter = TokenTextSplitter(
        chunk_size=400,
        chunk_overlap=50
    )

    chunks = []
    metadatas = []

    for doc in documents:
        text = doc["text"]
        meta = doc["metadata"]

        # CSV rows = already atomic
        if meta.get("type") == "csv":
            chunks.append(text)
            metadatas.append(meta)

        # MD files = token chunking
        else:
            splits = splitter.split_text(text)
            for s in splits:
                chunks.append(s)
                metadatas.append(meta)

    print(f"\nTotal documents loaded: {len(documents)}")
    print(f"Total chunks created: {len(chunks)}")
    print("Sample chunk metadata:")
    for m in metadatas[:2]:
        print(m)

    embeddings = get_embeddings()

    return Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=persist_dir
    )
