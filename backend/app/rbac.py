from backend.app.role_mapping import ROLE_MAP
import os
import pandas as pd

BASE_PATH = "db/Fintech-data"


def load_data(role, filter):
    role = role.strip()
    filter = filter.strip().lower()

    allowed = ROLE_MAP.get(role)

    if not allowed:
        return None

    # C-Level sees everything when filter = c-level
    if role == "C-Level" and filter == "c-level":
        folders = allowed
    else:
        if filter not in allowed:
            return None
        folders = [filter]

    documents = []

    for folder in folders:
        path = os.path.join(BASE_PATH, folder)

        if not os.path.exists(path):
            continue

        for file in os.listdir(path):
            file_path = os.path.join(path, file)

            # ========= MARKDOWN FILES =========
            if file.endswith(".md"):
                with open(file_path, "r", encoding="utf-8") as f:
                    documents.append({
                        "text": f.read(),
                        "metadata": {
                            "source": file,
                            "role": folder.capitalize(),
                            "type": "md"
                        }
                    })

            # ========= CSV FILES (HR DATA) =========
            elif file.endswith(".csv"):
                df = pd.read_csv(file_path)

                for idx, row in df.iterrows():
                    employee_block = "\n".join([
                        f"employee_id: {row.get('employee_id', '')}",
                        f"full_name: {row.get('full_name', '')}",
                        f"role: {row.get('role', '')}",
                        f"department: {row.get('department', '')}",
                        f"email: {row.get('email', '')}",
                        f"location: {row.get('location', '')}",
                        f"date_of_birth: {row.get('date_of_birth', '')}",
                        f"date_of_joining: {row.get('date_of_joining', '')}",
                        f"manager_id: {row.get('manager_id', '')}",
                        f"salary: {row.get('salary', '')}",
                        f"leave_balance: {row.get('leave_balance', '')}",
                        f"leaves_taken: {row.get('leaves_taken', '')}",
                        f"attendance_pct: {row.get('attendance_pct', '')}",
                    ])

                    documents.append({
                        "text": employee_block,
                        "metadata": {
                            "source": file,
                            "row": int(idx),
                            "role": folder.upper(),
                            "type": "csv"
                        }
                    })

    return documents
