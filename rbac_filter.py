from pathlib import Path
import csv

# 1. UPDATED: Keys changed to lowercase for consistent matching
ROLE_ACCESS = {
    "hr": ["hr"],
    "finance": ["finance"],
    "marketing": ["marketing"],
    "engineering": ["engineering"],
    "employees": ["general"],
    "c-level": ["engineering", "finance", "hr", "marketing", "general"]
}

DEPT_KEYWORDS = {
    "hr": ["employee", "attendance", "salary", "hr", "hiring", "payroll", "staff"],
    "finance": ["revenue", "profit", "loss", "investor", "financial", "budget", "cash flow"],
    "marketing": ["campaign", "marketing", "branding", "advertising", "leads", "market"],
    "engineering": ["architecture", "deployment", "api", "system", "engineering", "tech stack"],
    "general": ["policy", "handbook", "guidelines", "employee handbook"]
}

DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data"


def read_md(file_path):
    return file_path.read_text(encoding="utf-8")


def read_csv(file_path):
    rows = []
    with open(file_path, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(" | ".join(row))
    return "\n".join(rows)


def load_data():
    data = {}
    # Ensure DATA_PATH exists to avoid errors if folder is missing
    if not DATA_PATH.exists():
        print(f"Warning: Data path {DATA_PATH} not found.")
        return data

    for dept_folder in DATA_PATH.iterdir():
        if dept_folder.is_dir():
            dept = dept_folder.name.lower()
            data[dept] = []

            for file in dept_folder.iterdir():
                if file.suffix == ".md":
                    content = read_md(file)
                elif file.suffix == ".csv":
                    content = read_csv(file)
                else:
                    continue

                data[dept].append({
                    "file": file.name,
                    "content": content
                })
    return data


DATA = load_data()


def query_matches_department(query, department):
    query = query.lower()
    for kw in DEPT_KEYWORDS.get(department, []):
        if kw in query:
            return True
    return False


def run_console():
    print("\n=== ROLE BASED DATA ACCESS SYSTEM ===\n")

    while True:
        # 2. UPDATED: Used .lower() instead of .capitalize() to handle all case variations
        role = input("Enter your role (HR, Finance, Engineering, Marketing, Employees, C-Level): ").strip().lower()

        if role not in ROLE_ACCESS:
            print("❌ Invalid Role! Try again.\n")
            continue

        dept = input("Enter department to access (hr, finance, engineering, marketing, general): ").strip().lower()

        if dept not in DATA:
            print("❌ Department does not exist or has no data.\n")
            continue

        # Check role permission
        if dept not in ROLE_ACCESS[role]:
            print(f"❌ Access Denied: '{role.upper()}' cannot access '{dept}' department.\n")
        else:
            query = input("Enter your query: ").strip().lower()

            # Check semantic department match
            if not query_matches_department(query, dept):
                print("❌ Access Denied: Query not related to department.\n")
            else:
                # Perform search
                print("\n--- RESULT ---")
                found = False
                for doc in DATA[dept]:
                    if query in doc["content"].lower():
                        print(f"\nFile: {doc['file']}")
                        print("Content Preview:")
                        print(doc["content"][:400] + "...\n")
                        found = True

                if not found:
                    print("No matching results found.\n")

        again = input("Do you want to search again? (y/n): ").strip().lower()
        if again != "y":
            print("\nExiting system. Goodbye!")
            break


if __name__ == "__main__":
    run_console()