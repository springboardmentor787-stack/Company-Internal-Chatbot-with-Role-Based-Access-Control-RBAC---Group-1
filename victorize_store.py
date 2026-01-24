from scripts.load_documents import load_documents
from scripts.clean_documents import clean_documents
from scripts.chunk_documents import chunk_documents
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

CHROMA_DB_DIR = "chroma_db"

def sanitize_metadata(metadata):
    clean_meta = {}
    for k, v in metadata.items():
        if isinstance(v, (str, int, float, bool)) or v is None:
            clean_meta[k] = v
        else:
            clean_meta[k] = str(v)
    return clean_meta

def sanitize_chunks(chunks):
    sanitized = []
    for doc in chunks:
        sanitized.append(
            Document(
                page_content=doc.page_content,
                metadata=sanitize_metadata(doc.metadata)
            )
        )
    return sanitized

def vectorize_and_store(chunks):
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=CHROMA_DB_DIR
    )
    vector_db.persist()
    return vector_db

if __name__ == "__main__":
    docs = load_documents()
    cleaned_docs = clean_documents(docs)
    chunks = chunk_documents(cleaned_docs)
    chunks = sanitize_chunks(chunks)
    vectorize_and_store(chunks)
    print("Vectorization complete")
    print(f"ChromaDB stored at: {CHROMA_DB_DIR}")
    
