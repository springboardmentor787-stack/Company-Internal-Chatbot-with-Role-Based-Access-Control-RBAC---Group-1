import os
from langchain_community.document_loaders import TextLoader, CSVLoader

# =====================================================
# ROLE-BASED ACCESS CONTROL (RBAC) POLICY
# =====================================================
# Folder name  -> Roles allowed to access files inside it

ROLE_MAPPING = {
    "finance": ["Finance", "C-Level"],
    "hr": ["HR", "C-Level"],
    "engineering": ["Engineering", "C-Level"],
    "marketing": ["Marketing", "C-Level"],
    "general": ["Employees", "Finance", "HR", "Engineering", "Marketing", "C-Level"]
}

# =====================================================
# BASE PATH
# =====================================================
# load_documents.py is at ROOT level
# Fintech-data folder is directly inside the project

BASE_PATH = os.path.join(os.path.dirname(__file__), "Fintech-data")

# =====================================================
# FUNCTION: Load documents + attach RBAC metadata
# =====================================================

def load_documents_with_metadata():
    """
    Reads all department folders inside Fintech-data,
    loads .md and .csv files,
    and attaches role-based metadata to each document.
    """

    documents = []

    # Loop through department folders (finance, hr, etc.)
    for folder in os.listdir(BASE_PATH):
        folder_path = os.path.join(BASE_PATH, folder)

        # Skip files, process only folders
        if not os.path.isdir(folder_path):
            continue

        dept = folder.lower()

        # Skip folders not defined in RBAC policy
        if dept not in ROLE_MAPPING:
            continue

        # Roles allowed for this department
        allowed_roles = ROLE_MAPPING[dept]

        # Loop through files inside department folder
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)

            # Load Markdown files
            if file.endswith(".md"):
                loader = TextLoader(file_path, encoding="utf-8")
                docs = loader.load()

            # Load CSV files
            elif file.endswith(".csv"):
                loader = CSVLoader(file_path)
                docs = loader.load()

            # Ignore unsupported file types
            else:
                continue

            # Attach metadata to each document
            for doc in docs:
                doc.metadata = {
                    "dept": dept,                               # department name
                    "allowed_roles": ",".join(allowed_roles),  # RBAC roles
                    "source_file": file                        # original filename
                }
                documents.append(doc)

    return documents

# =====================================================
# VERIFICATION / TEST RUN
# =====================================================

if __name__ == "__main__":
    docs = load_documents_with_metadata()

    print(f"\n✅ Total documents loaded: {len(docs)}")

    seen_departments = set()
    print("\n📌 Sample metadata per department:\n")

    for doc in docs:
        dept = doc.metadata["dept"]
        if dept not in seen_departments:
            print(doc.metadata)
            seen_departments.add(dept)

        if len(seen_departments) == len(ROLE_MAPPING):
            break
