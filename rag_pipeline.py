import os
import pandas as pd
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# -----------------------------
# 1️⃣ OpenAI API Key
# -----------------------------
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Set OPENAI_API_KEY in your environment variables!")

# -----------------------------
# 2️⃣ Role → department map (RBAC)
# -----------------------------
ROLE_ACCESS_MAP = {
    "engineering": ["Engineering"],
    "hr": ["HR"],
    "finance": ["Finance"],
    "marketing": ["Marketing"],
    "c-level": ["Engineering", "HR", "Finance", "Marketing", "General"]
}

# -----------------------------
# 3️⃣ Chroma DB config
# -----------------------------
DB_DIR = "db"             # folder where vector DB is saved
BASE_PATH = "documents"   # folder with department subfolders
DEPARTMENTS = ["Engineering", "HR", "Finance", "Marketing", "General"]

# -----------------------------
# 4️⃣ Initialize embeddings and splitter
# -----------------------------
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    openai_api_key=OPENAI_API_KEY
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# -----------------------------
# 5️⃣ Load docs with metadata
# -----------------------------
def load_docs():
    all_docs = []
    for dept in DEPARTMENTS:
        folder_path = os.path.join(BASE_PATH, dept)
        if not os.path.exists(folder_path):
            print(f"Folder not found: {folder_path}")
            continue

        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                content = ""

                if file.endswith(".md"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                elif file.endswith(".csv"):
                    df = pd.read_csv(file_path)
                    content = df.to_string(index=False)
                else:
                    continue

                chunks = text_splitter.split_text(content)
                for chunk in chunks:
                    doc = Document(
                        page_content=chunk,
                        metadata={"department": dept}
                    )
                    all_docs.append(doc)

        print(f"Loaded {len(all_docs)} chunks from {dept}")

    return all_docs

# -----------------------------
# 6️⃣ Create / persist vector DB
# -----------------------------
def create_vector_db(docs):
    vector_db = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    vector_db.persist()
    print(f"✅ Vector DB created with {len(docs)} chunks")
    return vector_db

# -----------------------------
# 7️⃣ RBAC-protected retrieval
# -----------------------------
def secure_similarity_search(vector_db, query, user_role, k=10):
    user_role = user_role.lower()
    allowed_departments = ROLE_ACCESS_MAP.get(user_role)
    if not allowed_departments:
        raise PermissionError(f"Unauthorized role: {user_role}")

    # Chroma filter
    if len(allowed_departments) == 1:
        metadata_filter = {"department": allowed_departments[0]}
    else:
        metadata_filter = {"department": {"$in": allowed_departments}}

    docs = vector_db.similarity_search(
        query=query,
        k=k,
        filter=metadata_filter
    )

    return docs

# -----------------------------
# 8️⃣ Main script
# -----------------------------
if __name__ == "__main__":
    # Step 1: Load documents and create DB
    all_docs = load_docs()
    if not all_docs:
        print("No documents found. Please add documents under 'documents/' folder.")
        exit()

    vector_db = create_vector_db(all_docs)

    # Step 2: Query loop
    while True:
        query = input("\nEnter your query (or 'exit' to quit): ")
        if query.lower() == "exit":
            break

        user_role = input("Enter your role: ")

        try:
            docs = secure_similarity_search(vector_db, query, user_role, k=5)
            if not docs:
                print("No documents found or access denied.")
            else:
                print(f"\nFound {len(docs)} documents:")
                for i, doc in enumerate(docs, 1):
                    dept = doc.metadata.get("department", "Unknown")
                    preview = doc.page_content[:150].replace("\n", " ")
                    print(f"{i}. [{dept}] {preview}...")

        except PermissionError as e:
            print("Access denied:", e)
