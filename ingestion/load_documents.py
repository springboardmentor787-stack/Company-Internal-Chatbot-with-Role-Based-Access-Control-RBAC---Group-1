import os
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "Fintech-data")
)

ROLE_MAP = {
    "finance": "Finance,C-Level",
    "hr": "HR,C-Level",
    "engineering": "Engineering,C-Level",
    "marketing": "Marketing,C-Level",
    "general": "Finance,HR,Engineering,C-Level"
}

def load_documents():
    print("Using BASE_DIR:", BASE_DIR)

    if not os.path.exists(BASE_DIR):
        raise RuntimeError(f"❌ BASE_DIR does not exist: {BASE_DIR}")

    documents = []

    for department in os.listdir(BASE_DIR):
        dept_path = os.path.join(BASE_DIR, department)

        if not os.path.isdir(dept_path):
            continue

        dept_key = department.lower()
        allowed_roles = ROLE_MAP.get(dept_key, "")

        for file in os.listdir(dept_path):
            if not file.endswith(".md"):
                continue

            file_path = os.path.join(dept_path, file)

            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50
            )

            chunks = splitter.split_text(text)

            for idx, chunk in enumerate(chunks):
                documents.append(
                    Document(
                        page_content=chunk,
                        metadata={
                            "source": file,
                            "department": department,
                            "allowed_roles": allowed_roles,
                            "chunk_id": idx
                        }
                    )
                )

    print(f"✅ Total chunks created: {len(documents)}")
    return documents

if __name__ == "__main__":
    load_documents()
