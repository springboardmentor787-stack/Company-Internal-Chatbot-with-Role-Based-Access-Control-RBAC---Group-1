from load_documents import all_documents
from chunk_doc import chunked_documents

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    collection_name="company_documents",
    embedding_function=embedding_model,
    persist_directory="db/chroma_global"
)

# Clean metadata (important for Chroma)
clean_docs = []
for doc in chunked_documents:
    d = doc.model_copy()
    if isinstance(d.metadata.get("allowed_roles"), list):
        d.metadata["allowed_roles"] = ",".join(d.metadata["allowed_roles"])
    clean_docs.append(d)

db.add_documents(clean_docs)

print("Ingestion complete")
print("Total vectors stored:", db._collection.count())
