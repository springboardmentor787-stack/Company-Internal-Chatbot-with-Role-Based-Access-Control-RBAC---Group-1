def get_allowed_departments(role: str):
    role = role.lower()
    
    # C-Level sees everything
    if role == "c-level":
        return ["hr", "finance", "marketing", "engineering", "general"]
    
    # Department heads see their own dept + General
    if role == "hr":
        return ["hr", "general"]     # <--- Crucial for your sick leave query
        
    if role == "finance":
        return ["finance", "general"]
        
    if role == "marketing":
        return ["marketing", "general"]
        
    if role == "engineering":
        return ["engineering", "general"]
    
    # Regular employees only see General
    return ["general"]