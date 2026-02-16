# rbac_demo.py
# Role-Based Access Control Demo
# Flow: Role → Department → Access Granted / Denied

ROLE_ACCESS_MAP = {
    "Finance": ["Finance", "General"],
    "HR": ["HR", "General"],
    "Marketing": ["Marketing", "General"],
    "Engineering": ["Engineering", "General"],
    "C-Level": ["Finance", "HR", "Marketing", "Engineering", "General"]
}


def main():
    print("\n===== ROLE BASED ACCESS CONTROL =====\n")

    # Step 1: Select Role
    print("Select your role:")
    print("1. Finance")
    print("2. HR")
    print("3. Marketing")
    print("4. Engineering")
    print("5. C-Level")

    role_choice = input("\nEnter role (1-5): ").strip()

    role_map = {
        "1": "Finance",
        "2": "HR",
        "3": "Marketing",
        "4": "Engineering",
        "5": "C-Level"
    }

    user_role = role_map.get(role_choice)
    if not user_role:
        print("\n❌ Invalid role selected")
        return

    print(f"\nUser Role: {user_role}")

    # Step 2: Select Department to Access
    print("\nWhich documents do you want to access?")
    print("1. Finance")
    print("2. HR")
    print("3. Marketing")
    print("4. Engineering")
    print("5. General")

    dept_choice = input("\nEnter department (1-5): ").strip()

    dept_map = {
        "1": "Finance",
        "2": "HR",
        "3": "Marketing",
        "4": "Engineering",
        "5": "General"
    }

    department = dept_map.get(dept_choice)
    if not department:
        print("\n❌ Invalid department selected")
        return

    print(f"\nTrying to access {department} documents...\n")

    # Step 3: Access Check
    if department in ROLE_ACCESS_MAP[user_role]:
        print("✅ ACCESS GRANTED")
    else:
        print("❌ ACCESS DENIED")

    print("\n===== END OF DEMO =====")


if __name__ == "__main__":
    main()