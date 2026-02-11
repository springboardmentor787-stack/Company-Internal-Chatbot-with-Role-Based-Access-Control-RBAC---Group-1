import os
from pathlib import Path
from langchain_community.document_loaders import TextLoader, CSVLoader

# =====================================================
# ROLE-BASED ACCESS CONTROL (RBAC) POLICY
# =====================================================

ROLE_MAPPING = {
    "finance": ["Finance", "C-Level"],
    "hr": ["HR", "C-Level"],
    "engineering": ["Engineering", "C-Level"],
    "marketing": ["Marketing", "C-Level"],
    "general": ["Employees", "Finance", "HR", "Engineering", "Marketing", "C-Level"]
}

# =====================================================
# BASE PATH (CORRECT FOR YOUR PROJECT)
# =====================================================
# load_documents.py → Milestone_1
# Fintech-data is one level ABOVE Milestone_1

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASE_PATH = PROJECT_ROOT / "Fintech-data"

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

    if not BASE_PATH.exists():
        raise FileNotFoundError(f"❌ Fintech-data folder not found: {BASE_PATH}")

    print(f"📂 Loading documents from: {BASE_PATH}")

    # Loop through department folders
    for folder in os.listdir(BASE_PATH):
        folder_path = BASE_PATH / folder

        if not folder_path.is_dir():
            continue

        dept = folder.lower()

        if dept not in ROLE_MAPPING:
            continue

        allowed_roles = ROLE_MAPPING[dept]

        print(f"➡️ Processing department: {dept}")

        for file in os.listdir(folder_path):
            file_path = folder_path / file

            if file.endswith(".md"):
                loader = TextLoader(str(file_path), encoding="utf-8")
                docs = loader.load()

            elif file.endswith(".csv"):
                loader = CSVLoader(str(file_path))
                docs = loader.load()

            else:
                continue

            for doc in docs:
                doc.metadata = {
                    "dept": dept,
                    "allowed_roles": ",".join(allowed_roles),
                    "source_file": file
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
