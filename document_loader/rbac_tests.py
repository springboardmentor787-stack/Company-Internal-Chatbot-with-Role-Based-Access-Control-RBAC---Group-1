from secure_semantic_search import secure_semantic_search

TEST_CASES = [
    ("Finance", "employee leave policy", False),
    ("HR", "employee leave policy", True),
    ("Engineering", "system architecture", True),
    ("Finance", "system architecture", False),
    ("C-Level", "salary processing", True),
]

def run_rbac_tests():
    print("\n🔐 RBAC VALIDATION TESTS\n")

    for role, query, expected in TEST_CASES:
        print("=" * 60)
        print(f"Role: {role}")
        print(f"Query: {query}")

        results = secure_semantic_search(query, role)
        allowed = len(results) > 0

        if allowed == expected:
            print("✅ TEST PASSED")
        else:
            print("❌ TEST FAILED")


if __name__ == "__main__":
    run_rbac_tests()
