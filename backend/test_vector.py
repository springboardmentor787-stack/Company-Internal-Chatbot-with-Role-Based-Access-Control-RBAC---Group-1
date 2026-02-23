# test_vector.py

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

results = vectordb.similarity_search("salary", k=5)

print("Results count:", len(results))

if results:
    print("Sample metadata:", results[0].metadata)
