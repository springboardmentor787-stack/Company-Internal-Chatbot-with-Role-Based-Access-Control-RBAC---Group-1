from embed_documents import embed_documents_if_needed


# =====================================================
# RBAC POLICY
# =====================================================

ROLE_ACCESS = {
    "HR": ["hr", "general"],
    "Finance": ["finance", "general"],
    "Engineering": ["engineering", "general"],
    "Marketing": ["marketing", "general"],
    "C-Level": ["finance", "hr", "engineering", "marketing", "general"]
}


# =====================================================
# LOAD VECTOR DATABASE (AUTO-EMBED IF NEEDED)
# =====================================================

vectordb = embed_documents_if_needed()


# =====================================================
# FUNCTION: SECURE SEARCH WITH RBAC
# =====================================================

def secure_search(user_role, target_dept, query, k=5):

    # Validate role
    if user_role not in ROLE_ACCESS:
        print("❌ Invalid role")
        return []

    # Enforce RBAC
    if target_dept not in ROLE_ACCESS[user_role]:
        print(f"❌ Access denied for role: {user_role}")
        return []

    # Authorized similarity search
    results = vectordb.similarity_search(
        query=query,
        k=k,
        filter={"dept": target_dept}
    )

    return results


# =====================================================
# INTERACTIVE TERMINAL CHATBOT
# =====================================================

if __name__ == "__main__":

    print("\n=== COMPANY INTERNAL CHATBOT (RBAC ENABLED) ===")
    print("Available roles:", ", ".join(ROLE_ACCESS.keys()))
    print("Available departments: finance, hr, engineering, marketing, general")

    while True:
        print("\n----------------------------------------")

        user_role = input("Enter your role (or type 'exit'): ").strip()
        if user_role.lower() == "exit":
            print("Exiting chatbot...")
            break

        target_dept = input("Enter department to search: ").strip().lower()
        query = input("Enter your query: ").strip()

        results = secure_search(user_role, target_dept, query)

        print(f"\n🔎 Results found: {len(results)}")

        # =================================================
        # DISPLAY FOUND RESULTS
        # =================================================
        if results:
            for idx, doc in enumerate(results, start=1):
                print("\n" + "=" * 50)
                print(f"📄 Result {idx}")
                print("-" * 50)

                # Show metadata
                print("🔖 Metadata:")
                for k, v in doc.metadata.items():
                    print(f"  {k}: {v}")

                # Show document content (limit for readability)
                print("\n📝 Content:")
                print(doc.page_content[:500])  # first 500 characters
                print("=" * 50)
        else:
            print("⚠️ No authorized results found.")
