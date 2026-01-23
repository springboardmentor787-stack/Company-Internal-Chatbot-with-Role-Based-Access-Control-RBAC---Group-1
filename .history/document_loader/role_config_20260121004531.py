# Central role hierarchy configuration

ROLE_HIERARCHY = {
    "HR": ["HR", "General"],
    "Finance": ["Finance", "General"],
    "Engineering": ["Engineering", "General"],
    "Marketing": ["Marketing", "General"],
    "C-Level": ["HR", "Finance", "Engineering", "Marketing", "General"]
}
