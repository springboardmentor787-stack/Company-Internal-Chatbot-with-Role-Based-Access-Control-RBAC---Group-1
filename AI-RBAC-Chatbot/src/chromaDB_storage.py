import os
from role_mapping import load_role_mapping
from chunk_doc import chunked_documents
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# -----------------------------
# Embedding model (used only for DB storage)
# -----------------------------
embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# -----------------------------
# User input
# -----------------------------
user_role = input("Enter your role: ").strip()
data_filter = input(
    "Enter data filter (hr / finance / engineering / marketing / general): "
).strip().lower()

# -----------------------------
# Load RBAC mapping
# -----------------------------
ROLE_MAPPING = load_role_mapping()

dept_map = {
    "hr": "HR",
    "finance": "Finance",
    "engineering": "engineering",
    "marketing": "marketing",
    "general": "general"
}

if data_filter not in dept_map:
    print("Invalid department")
    print("Accessible files: 0")
    exit()

dept_name = dept_map[data_filter]
allowed_roles = ROLE_MAPPING.get(dept_name, [])

# -----------------------------
# RBAC check
# -----------------------------
if user_role not in allowed_roles:
    print("Access Denied")
    print("Accessible files: 0")
    exit()

print("Access Granted")

# -----------------------------
# Filter chunks by department
# -----------------------------
filtered_chunks = [
    doc for doc in chunked_documents
    if doc.metadata.get("dept", "").lower() == data_filter
]

# -----------------------------
# Count unique files + pick one sample doc
# -----------------------------
unique_file_names = set()
sample_doc = None

for doc in filtered_chunks:
    source = doc.metadata.get("source")
    if source not in unique_file_names:
        unique_file_names.add(source)
        if sample_doc is None:
            sample_doc = doc

file_count = len(unique_file_names)

if file_count == 0:
    print("Accessible files: 0")
    print("No documents available for this department")
    exit()

print(f"Accessible files: {file_count}")

# -----------------------------
# (Optional) Store in ChromaDB
# -----------------------------
clean_docs = []
for doc in filtered_chunks:
    d = doc.model_copy()
    if isinstance(d.metadata.get("allowed_roles"), list):
        d.metadata["allowed_roles"] = ",".join(d.metadata["allowed_roles"])
    clean_docs.append(d)

persist_path = f"db/chroma_{user_role}_{data_filter}"
db_exists = os.path.exists(persist_path)

db = Chroma(
    collection_name=f"{dept_name}_documents",
    embedding_function=embedding_model,
    persist_directory=persist_path
)

if not db_exists:
    db.add_documents(clean_docs)
    print("Vector database created successfully")
else:
    print("Vector database already exists, reusing it")

# -----------------------------
# Sample preview
# -----------------------------
print("\nSAMPLE PREVIEW\n")
print("File:", sample_doc.metadata.get("source"))
print("Department:", sample_doc.metadata.get("dept"))
print("Preview:")
print(sample_doc.page_content[:300])
