import os
import shutil
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# --------------------------------------------------
# 1️⃣ Clean existing vector DB (Important for rebuild)
# --------------------------------------------------
if os.path.exists("vector_db"):
    shutil.rmtree("vector_db")
    print("Old vector_db deleted.")

# --------------------------------------------------
# 2️⃣ Define Enterprise Documents with Categories
# --------------------------------------------------
documents = [
    Document(
        page_content="Employee leave policy allows 20 days annual leave.",
        metadata={"category": "HR", "source": "employee_handbook.md"}
    ),
    Document(
        page_content="Company revenue for 2024 is 10M USD.",
        metadata={"category": "Finance", "source": "finance_report.md"}
    ),
    Document(
        page_content="Engineering roadmap focuses on AI automation.",
        metadata={"category": "Engineering", "source": "engineering_plan.md"}
    ),
    Document(
        page_content="Marketing strategy targets digital platforms.",
        metadata={"category": "Marketing", "source": "marketing_strategy.md"}
    ),
    Document(
        page_content="Board meeting discussed global expansion strategy.",
        metadata={"category": "C-Level", "source": "board_meeting.md"}
    ),
    Document(
        page_content="Company was founded in 2015.",
        metadata={"category": "General", "source": "company_overview.md"}
    ),
]

# --------------------------------------------------
# 3️⃣ Smart Chunking (Enterprise Standard)
# --------------------------------------------------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=50
)

docs = text_splitter.split_documents(documents)

print("\n📄 Chunks Created:")
for d in docs:
    print(f"Content: {d.page_content}")
    print(f"Metadata: {d.metadata}")
    print("-" * 40)

# --------------------------------------------------
# 4️⃣ Local Embedding Model
# --------------------------------------------------
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# --------------------------------------------------
# 5️⃣ Create & Persist Vector Database
# --------------------------------------------------
vectordb = Chroma.from_documents(
    documents=docs,
    embedding=embedding,
    persist_directory="vector_db"
)

vectordb.persist()

print("\n✅ Enterprise Vector DB created successfully!")
