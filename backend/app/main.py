from backend.app.rbac import load_data
from backend.app.clean_documents import clean_documents
from backend.app.chroma_store import build_vector_store
from langchain.text_splitter import TokenTextSplitter


role = input("Enter your role: ")
filter = input("Enter data filter (hr / finance / engineering / marketing / general): ")

docs = load_data(role, filter)

# ---- RBAC FAILURE HANDLING ----
if not docs:
    print("\n❌ Access Denied")

    print("\n🔹 Building empty Chroma Vector Store...")

    db = build_vector_store(
        [],
        persist_dir=f"db/chroma_{role}_{filter}"
    )

    print("\nTotal documents loaded: 0")
    print("Total chunks created: 0")
    print("Vector DB Ready (empty)")
    exit()

# ------------------------------

# Extract text for cleaning
raw_texts = [d["text"] for d in docs]

print(f"\nBefore cleaning: {len(raw_texts)}")

# CLEAN
cleaned = clean_documents(raw_texts)

print(f"After cleaning: {len(cleaned)}")

# Reattach metadata after cleaning
documents = []
for i in range(len(cleaned)):
    documents.append({
        "text": cleaned[i],
        "metadata": docs[i]["metadata"]
    })

# TOKEN CHUNKING (for visual verification)
splitter = TokenTextSplitter(chunk_size=400, chunk_overlap=50)

print("\n🔹 Cleaned & Chunked output:\n")

for i, doc in enumerate(documents):
    chunks = splitter.split_text(doc["text"])
    for j, chunk in enumerate(chunks):
        print(f"\n--- Document {i+1} | Chunk {j+1} ---")
        print(chunk)

# BUILD CHROMA VECTOR DB
print("\n🔹 Building Chroma Vector Store...\n")

db = build_vector_store(
    documents,
    persist_dir=f"db/chroma_{role}_{filter}"
)

print("\n✅ Vector DB Ready")













# from backend.app.rbac import load_data
# from backend.app.clean_documents import clean_documents
# from backend.app.chroma_store import build_vector_store
# from langchain.text_splitter import TokenTextSplitter


# role = input("Enter your role: ")
# filter = input("Enter data filter (hr / finance / engineering / marketing / general): ")

# docs = load_data(role, filter)

# if not docs:
#     print("❌ Access Denied or No Data")
#     exit()

# # Extract text for cleaning
# raw_texts = [d["text"] for d in docs]

# print(f"\nBefore cleaning: {len(raw_texts)}")

# # CLEAN
# cleaned = clean_documents(raw_texts)

# print(f"After cleaning: {len(cleaned)}")

# # Reattach metadata after cleaning
# documents = []
# for i in range(len(cleaned)):
#     documents.append({
#         "text": cleaned[i],
#         "metadata": docs[i]["metadata"]
#     })

# # TOKEN CHUNKING (for visual verification)
# splitter = TokenTextSplitter(chunk_size=400, chunk_overlap=50)

# print("\n🔹 Cleaned & Chunked output:\n")

# for i, doc in enumerate(documents):
#     chunks = splitter.split_text(doc["text"])
#     for j, chunk in enumerate(chunks):
#         print(f"\n--- Document {i+1} | Chunk {j+1} ---")
#         print(chunk)

# # BUILD CHROMA VECTOR DB
# print("\n🔹 Building Chroma Vector Store...\n")

# db = build_vector_store(
#     documents,
#     persist_dir=f"db/chroma_{role}_{filter}"
# )

# print("\n✅ Vector DB Ready")


# from backend.app.rbac import load_data
# from backend.app.chroma_store import build_vector_store

# role = input("Enter your role: ")
# filter = input("Enter data filter (hr / finance / engineering / marketing / general): ")

# texts = load_data(role, filter)

# if not texts:
#     print("❌ Access Denied: You are not allowed to view this data")
#     exit()

# vectordb = build_vector_store(texts, f"chroma_{role}_{filter}")

# query = input("Ask a question: ")

# results = vectordb.similarity_search(query, k=3)

# for r in results:
#     print(r.page_content)
