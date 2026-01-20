import os
from langchain_community.document_loaders import TextLoader, CSVLoader

# LOGIC MAP: FOLDER → ROLES (RBAC POLICY)

ROLE_MAPPING = {
    "finance": ["Finance", "C-Level"],
    "hr": ["HR", "C-Level"],
    "engineering": ["Engineering", "C-Level"],
    "marketing": ["Marketing", "C-Level"],
    "general": ["Employees", "Finance", "HR", "Engineering", "Marketing", "C-Level"]
}

BASE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "Fintech-data")
)

# LOAD DOCUMENTS + APPLY ROLE MAPPING + METADATA


def load_documents_with_metadata():
    documents = []

    for folder in os.listdir(BASE_PATH):
        folder_path = os.path.join(BASE_PATH, folder)

        if not os.path.isdir(folder_path):
            continue

        dept = folder.lower()

        # Explicit logic map check
    
        if dept not in ROLE_MAPPING:
            continue

        allowed_roles = ROLE_MAPPING[dept]

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)

            if file.endswith(".md"):
                loader = TextLoader(file_path, encoding="utf-8")
                docs = loader.load()

            elif file.endswith(".csv"):
                loader = CSVLoader(file_path)
                docs = loader.load()

            else:
                continue

            for doc in docs:
                doc.metadata = {
                    "dept": dept,
                    "allowed_roles": ",".join(allowed_roles),  # convert list → string
                    "source_file": file
                }
                documents.append(doc)

    return documents



# VERIFICATION 


if __name__ == "__main__":
    docs = load_documents_with_metadata()

    print(f"Total documents loaded: {len(docs)}")

    seen = set()
    print("\nSample metadata per department:")

    for doc in docs:
        dept = doc.metadata["dept"]
        if dept not in seen:
            print(doc.metadata)
            seen.add(dept)

        if len(seen) == len(ROLE_MAPPING):
            break
