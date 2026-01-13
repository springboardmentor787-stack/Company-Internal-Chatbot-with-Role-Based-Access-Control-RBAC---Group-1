from pathlib import Path
from langchain_community.document_loaders import TextLoader, CSVLoader
from role_mapping import load_role_mapping


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Fintech-data"

ROLE_MAPPING = load_role_mapping()

all_documents = []

for dept_folder in DATA_DIR.iterdir():
    if not dept_folder.is_dir():
        continue

    dept_name = dept_folder.name

    if dept_name not in ROLE_MAPPING:
        
        continue

    allowed_roles = ROLE_MAPPING[dept_name]

    for file_path in dept_folder.iterdir():
        if file_path.suffix == ".md":
            loader = TextLoader(str(file_path), encoding="utf-8")
        elif file_path.suffix == ".csv":
            loader = CSVLoader(str(file_path))
        else:
            continue

        docs = loader.load()
        
        for doc in docs:
            doc.metadata["dept"] = dept_name
            doc.metadata["allowed_roles"] = allowed_roles
            doc.metadata["source"] = file_path.name

            all_documents.append(doc)

if __name__ == "__main__":
    print(f"Total documents loaded: {len(all_documents)}")
    print("\nSample document from each department:")
    seen_depts = set()

    for doc in all_documents:
        dept = doc.metadata["dept"]
        if dept not in seen_depts:
            print(f"\nDepartment: {dept}")
            print("Source:", doc.metadata["source"])
            print(doc.page_content[:200])
            print("Metadata:", doc.metadata)
            seen_depts.add(dept)


