# preprocessing/rbac_config.py

ROLE_HIERARCHY = {
    "HR": ["hr", "general"],
    "Finance": ["finance", "general"],
    "Engineering": ["engineering", "general"],
    "Marketing": ["marketing", "general"],
    "C-Level": ["hr", "finance", "engineering", "marketing", "general"]
}