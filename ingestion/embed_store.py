from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.utils import filter_complex_metadata

from ingestion.load_documents import load_documents

VECTOR_DB_DIR = "vector_db/chroma_db"

def build_vector_db():
    documents = load_documents()

    if len(documents) == 0:
        raise RuntimeError("❌ No documents found for embedding")

    documents = filter_complex_metadata(documents)

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=VECTOR_DB_DIR
    )

    vectordb.persist()

    print(f"✅ Stored {len(documents)} chunks in vector DB")

if __name__ == "__main__":
    build_vector_db()
