from document_loader.role_config import ROLE_HIERARCHY

def get_allowed_roles(user_role: str):
    """
    Returns list of document roles accessible by the user role.
    """
    if user_role not in ROLE_HIERARCHY:
        raise ValueError("Invalid role")

    return ROLE_HIERARCHY[user_role]
