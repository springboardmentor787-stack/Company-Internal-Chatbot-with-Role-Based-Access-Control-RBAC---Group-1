# rbac_core.py

ROLE_HIERARCHY = {
    "employees": ["general"],
    "hr": ["hr"],
    "finance": ["finance"],
    "marketing": ["marketing"],
    "engineering": ["engineering"],
    "c-level": ["general", "hr", "finance", "marketing", "engineering"]
}

def normalize_role(role: str):
    return role.strip().lower()

def allowed_departments(role: str):
    role = normalize_role(role)
    return ROLE_HIERARCHY.get(role, [])

