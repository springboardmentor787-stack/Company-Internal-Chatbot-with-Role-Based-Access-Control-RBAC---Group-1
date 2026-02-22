from pathlib import Path
from langchain_community.document_loaders import TextLoader, CSVLoader
from role_mapping import role_access_mapping
DATA_ROOT = Path("Fintech-data")
all_documents = []

import re

def clean_text(text):
    text = text.lower()

    # Normalize whitespace only
    text = re.sub(r"\s+", " ", text)

    # DO NOT remove useful punctuation like - / :
    # Only remove truly problematic characters
    text = re.sub(r"[^\w\s.,:/()-]", "", text)

    return text.strip()

for department, roles in role_access_mapping.items():
    dept_path = DATA_ROOT / department

    for file in dept_path.glob("*"):


        if file.suffix == ".md":
            loader = TextLoader(str(file), encoding="utf-8")
        elif file.suffix == ".csv":
            loader = CSVLoader(str(file))
        else:
            continue

        docs = loader.load()

        for d in docs:
            d.page_content = clean_text(d.page_content)


        for d in docs:
            d.metadata = {
                "department": department,
                "allowed_roles": roles,
                "source": file.name
            }

        all_documents.extend(docs)

print("Total loaded documents:", len(all_documents))
print("Sample metadata:", all_documents[0].metadata)