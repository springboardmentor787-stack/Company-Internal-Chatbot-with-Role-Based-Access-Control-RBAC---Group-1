# run_pipeline.py

from Milestone2.src.loader import load_documents
from Milestone2.src.chunker import chunk_documents
from Milestone2.src.embeddings import get_embedding_model
from Milestone2.src.vector_store import create_vector_store
from Milestone2.src.benchmark import benchmark_search

DATA_PATH = "data/documents"

print("Loading documents...")
documents = load_documents(DATA_PATH)

print("Chunking documents...")
chunks = chunk_documents(documents)

print(f"Total Chunks: {len(chunks)}")

print("Generating embeddings & indexing...")
embedding_model = get_embedding_model()
vector_db = create_vector_store(chunks, embedding_model)

print("Running benchmark...")
benchmark_search([
    "API authentication",
    "deployment steps",
    "error handling",
    "database connection"
])

print("Module 3 completed successfully ✅")
