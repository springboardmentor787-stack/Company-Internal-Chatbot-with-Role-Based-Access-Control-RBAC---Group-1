def has_access(user_role: str, allowed_roles_str: str) -> bool:
    if not allowed_roles_str:
        return False
    allowed_roles = allowed_roles_str.split(",")
    return user_role in allowed_roles
