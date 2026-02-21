import os
from langchain_community.document_loaders import TextLoader, CSVLoader

BASE_PATH = "Fintech-data"

ROLE_MAP = {
    "Finance": "Finance",
    "HR": "HR",
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

            # METADATA 
            for i, doc in enumerate(docs):
                doc.metadata.update({
                    "role": role,
                    "source": file,
                    "file_path": file_path,
                    "doc_id": f"{file}_{i}",
                    "content_type": file.split(".")[-1]
                })

            documents.extend(docs)

    print(f"✅ Total documents loaded: {len(documents)}")
    return documents


if __name__ == "__main__":
    load_documents()
