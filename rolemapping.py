ROLE_MAPPING = {
    "Finance": {
        "dept": "Finance",
        "allowed_roles": ["Finance", "C-Level"]
    },
    "Marketing": {
        "dept": "Marketing",
        "allowed_roles": ["Marketing", "C-Level"]
    },
    "HR": {
        "dept": "HR",
        "allowed_roles": ["HR", "C-Level"]
    },
    "Engineering": {
        "dept": "Engineering",
        "allowed_roles": ["Engineering", "C-Level"]
    },
    "General": {
        "dept": "General",
        "allowed_roles": [
            "Finance", "Marketing", "HR", "Engineering", "C-Level"
        ]
    }
}

def map_document_to_metadata(file_path: str):
    folder = file_path.split("/")[1]  # fintech-data/<FOLDER>/file
    return ROLE_MAPPING.get(folder, ROLE_MAPPING["General"])
