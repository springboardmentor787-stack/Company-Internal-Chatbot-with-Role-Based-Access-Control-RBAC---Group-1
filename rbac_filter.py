def python_rbac_filter(docs, user_role):
    allowed_docs = []
    blocked_docs = []

    for doc in docs:
        allowed_roles_str = doc.metadata.get("allowed_roles", "")
        allowed_roles = [r.strip() for r in allowed_roles_str.split(",")]

        if user_role == "C-Level" or user_role in allowed_roles:
            allowed_docs.append(doc)
        else:
            blocked_docs.append(doc)

    return allowed_docs, blocked_docs