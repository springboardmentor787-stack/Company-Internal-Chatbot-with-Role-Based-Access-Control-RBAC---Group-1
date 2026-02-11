import json
def load_role_mapping():
    # Your logic to load the JSON
    # Make sure the function name matches EXACTLY
    return {
        "HR": ["hr", "general"],
        "Finance": ["finance", "general"],
        "Engineering": ["engineering", "general"],
        "Marketing": ["marketing", "general"],
        "C-Level": ["hr", "finance", "engineering", "marketing", "general"]
}

# This prevents the print from running during import
if __name__ == "__main__":
    print(load_role_mapping())