from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from chunking import chunks
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


for chunk in chunks:
    if isinstance(chunk.metadata.get('allowed_roles'), list):
        chunk.metadata['allowed_roles'] = ",".join(chunk.metadata['allowed_roles'])


vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="./chroma_db"
)