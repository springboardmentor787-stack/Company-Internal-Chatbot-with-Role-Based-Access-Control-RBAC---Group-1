from langchain_chroma import Chroma
from langchain_text_splitters import TokenTextSplitter
from backend.app.embeddings import get_embeddings
import os


def build_vector_store(documents, persist_dir):
    embeddings = get_embeddings()

    # Ensure directory exists
    os.makedirs(persist_dir, exist_ok=True)

    # If no documents, just open (or create) empty DB
    if not documents:
        return Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings
        )

    splitter = TokenTextSplitter(chunk_size=400, chunk_overlap=50)

    chunks = []
    metadatas = []

    for doc in documents:
        text = doc["text"]
        meta = doc["metadata"]

        if meta.get("type") == "csv":
            chunks.append(text)
            metadatas.append(meta)
        else:
            splits = splitter.split_text(text)
            for s in splits:
                chunks.append(s)
                metadatas.append(meta)

    db = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=persist_dir
    )

    db.persist()
    return db


def get_chroma_stats(persist_dir):
    embeddings = get_embeddings()

    db = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )

    return db._collection.count()
