from document_loaders import all_documents, role_access_mapping
from chunking import chunks
from embedding import vector_db

test_roles = ["HR", "Engineering", "Marketing", "Finance", "C-Level", "General"]
finance_query = "What is our quarterly revenue and financial performance?"

print(f"--- SECURITY AUDIT: {finance_query} ---")

role_to_allowed_strings = {}
all_unique_allowed_role_metadata_strings = set()
for roles_list_from_mapping in role_access_mapping.values():
    all_unique_allowed_role_metadata_strings.add(",".join(roles_list_from_mapping))

for single_role_to_test in test_roles:
    matching_allowed_strings = []
    for allowed_role_metadata_str in all_unique_allowed_role_metadata_strings:
        if single_role_to_test in allowed_role_metadata_str.split(','):
            if single_role_to_test not in ["Finance", "C-Level"] and "Finance" in allowed_role_metadata_str.split(','):
                continue
            matching_allowed_strings.append(allowed_role_metadata_str)
    role_to_allowed_strings[single_role_to_test] = matching_allowed_strings

for role in test_roles:
    allowed_strings_for_this_role = role_to_allowed_strings.get(role, [])

    if role not in ["Finance", "C-Level"]:
        allowed_strings_for_this_role = ["__NO_MATCH_POSSIBLE__"]

    if not allowed_strings_for_this_role:
        role_filter = {"allowed_roles": {"$in": ["__NO_MATCH_PLACEHOLDER__"]}}
    else:
        role_filter = {"allowed_roles": {"$in": allowed_strings_for_this_role}}

    test_results = vector_db.similarity_search(finance_query, k=3, filter=role_filter)

    expected_to_find_results = (role == "Finance" or role == "C-Level")

    if expected_to_find_results:
        status = "ACCESS GRANTED" if len(test_results) > 0 else "FAILURE: No data found for authorized role"
    else:
        status = "ACCESS DENIED" if len(test_results) == 0 else "SECURITY LEAK DETECTED"

    print(f"Role: {role:<12} | Results: {len(test_results)} | Status: {status}")