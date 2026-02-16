def is_access_allowed(user_role, metadata):
    allowed_roles = metadata.get("allowed_roles", "")
    allowed_roles = [r.strip() for r in allowed_roles.split(",")]
    return user_role in allowed_roles