from pathlib import Path
import csv

DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data"
print("DATA PATH:", DATA_PATH)
print("EXISTS:", DATA_PATH.exists())

ROLE_MAPPING = {
    "engineering": ["Engineering", "C-Level"],
    "finance": ["Finance", "C-Level"],
    "hr": ["HR", "C-Level"],
    "marketing": ["Marketing", "C-Level"],
    "general": ["Employees", "C-Level"]
}

def read_md(file_path):
    return file_path.read_text(encoding="utf-8")

def read_csv(file_path):
    rows = []
    with open(file_path, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(" | ".join(row))
    return "\n".join(rows)

def load_documents():
    documents = []

    for department_folder in DATA_PATH.iterdir():
        if department_folder.is_dir():
            department = department_folder.name.lower()
            roles = ROLE_MAPPING.get(department, ["C-Level"])

            for file in department_folder.iterdir():
                if file.suffix == ".md":
                    content = read_md(file)
                elif file.suffix == ".csv":
                    content = read_csv(file)
                else:
                    continue

                documents.append({
                    "file_name": file.name,
                    "department": department,
                    "roles": roles,
                    "content": content
                })

    return documents


# Export for other modules
parsed_documents = load_documents()

if __name__ == "__main__":
    print("Total documents loaded:", len(parsed_documents))
    for doc in parsed_documents:
        print("-----")
        print("File:", doc["file_name"])
        print("Department:", doc["department"])
        print("Allowed Roles:", doc["roles"])
        print("Content Preview:", doc["content"][:200])
