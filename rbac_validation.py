ROLE_ACCESS = {
    "finance": ["finance"],
    "engineering": ["engineering"],
    "hr": ["hr"],
    "c_level": ["finance", "engineering", "hr", "general"]
}

def is_access_allowed(role, metadata):
    doc_dept = metadata.get("department", "").lower()
    return doc_dept in ROLE_ACCESS.get(role, [])
