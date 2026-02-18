# Central role hierarchy configuration

ROLE_HIERARCHY = {"General": ["General"],
    "HR": ["HR", "General"],
    "Finance": ["Finance", "General"],
    "Engineering": ["Engineering", "General"],
    "Marketing": ["Marketing", "General"],
    "C-Level": ["HR", "Finance", "Engineering", "Marketing", "General"]
}
