import os
from langchain_community.document_loaders import TextLoader, CSVLoader

BASE_PATH = "Fintech-data"

ROLE_MAP = {
    "Finance": "finance",
    "HR": "hr",
    "Marketing": "marketing",
    "Engineering": "engineering",
    "General": "general"
}

def load_documents():
    documents = []

    for role, folder in ROLE_MAP.items():
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
                doc.metadata["role"] = role
                doc.metadata["source"] = file

            documents.extend(docs)

    print(f"Total documents loaded: {len(documents)}")
    return documents


if __name__ == "__main__":
    load_documents()
