from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

PERSIST_DIR = "chroma_db"

def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def load_vector_db():
    embedding = get_embedding_model()
    vectordb = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embedding
    )
    return vectordb

def validate_vector_db(vectordb):
    count = vectordb._collection.count()
    if count == 0:
        raise ValueError("❌ Vector DB is empty.")
    print(f"✅ Vector DB loaded with {count} vectors.")
