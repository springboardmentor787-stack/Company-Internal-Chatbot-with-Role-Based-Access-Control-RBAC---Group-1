from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document


embedding = HuggingFaceEmbeddings(
model_name="sentence-transformers/all-MiniLM-L6-v2"
)


docs = [
Document(page_content="Q1 revenue was $5M.", metadata={"role": "finance"}),
Document(page_content="24 paid leaves per year.", metadata={"role": "hr"})
]


vectorstore = Chroma.from_documents(
docs, embedding, persist_directory="chroma_db"
)


vectorstore.persist()
print("Ingestion complete")