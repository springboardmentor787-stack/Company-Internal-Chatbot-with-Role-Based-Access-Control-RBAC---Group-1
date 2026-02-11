"""
Role-Based Access Control logic.
"""

ROLE_PERMISSIONS = {
    "HR": ["hr"],
    "Finance": ["finance"],
    "Marketing": ["marketing"],
    "Engineering": ["engineering"],
    "Employees": ["general"],
    "C-Level": ["hr","finance","marketing","engineering","general"]
}

def detect_department(question):
    """Detect department from keywords."""
    q = question.lower()
    if "leave" in q or "salary" in q:
        return "hr"
    elif "revenue" in q or "profit" in q:
        return "finance"
    elif "architecture" in q:
        return "engineering"
    else:
        return "general"

def is_allowed(role, department):
    """Check if role has permission."""
    return department in ROLE_PERMISSIONS.get(role, [])
