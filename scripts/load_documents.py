import os
from langchain_community.document_loaders import TextLoader, CSVLoader

BASE_PATH = "Fintech-data"

# Folder mapping
ROLE_FOLDER_MAP = {
    "Finance": "finance",
    "HR": "hr",
    "Marketing": "marketing",
    "Engineering": "engineering",
    "General": "general"
}

# Role-based access control (MEETING LOGIC)
ROLE_ACCESS_MAP = {
    "Finance": ["Finance", "C-Level"],
    "HR": ["HR", "C-Level"],
    "Marketing": ["Marketing", "C-Level"],
    "Engineering": ["Engineering", "C-Level"],
    "General": ["Finance", "HR", "Engineering", "Marketing", "Employees", "C-Level"]
}

def load_documents():
    documents = []

    for dept, folder in ROLE_FOLDER_MAP.items():
        folder_path = os.path.join(BASE_PATH, folder)

        if not os.path.exists(folder_path):
            print(f"Skipping missing folder: {folder_path}")
            continue

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
                doc.metadata["source"] = file
                doc.metadata["dept"] = dept
                doc.metadata["allowed_roles"] = ",".join(ROLE_ACCESS_MAP[dept])

            documents.extend(docs)

    print(f"✅ Total documents loaded: {len(documents)}")
    return documents


if __name__ == "__main__":
    load_documents()