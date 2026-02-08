ROLE_ACCESS = {
    "hr": ["hr", "general"],
    "finance": ["finance", "general"],
    "engineering": ["engineering", "general"],
    "marketing": ["marketing", "general"],
    "employees": ["general"],
    "c-level": ["hr", "finance", "engineering", "marketing", "general"]
}


def get_allowed_departments(role: str):
    return ROLE_ACCESS.get(role.lower(), [])
