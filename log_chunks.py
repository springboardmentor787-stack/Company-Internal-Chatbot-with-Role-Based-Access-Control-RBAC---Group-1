def log_chunks(query, role, raw_docs, allowed_docs, blocked_docs):
    print("\n" + "=" * 70)
    print("QUERY:", query)
    print("ROLE:", role)

    print("\n--- RAW RETRIEVED CHUNKS ---")
    for i, doc in enumerate(raw_docs):
        print(f"\n[RAW {i+1}]")
        print("Source:", doc.metadata.get("source"))
        print("Department:", doc.metadata.get("department"))
        print("Allowed Roles:", doc.metadata.get("allowed_roles"))
        print("Content:", doc.page_content[:300])

    print("\n--- BLOCKED BY RBAC ---")
    for i, doc in enumerate(blocked_docs):
        print(f"\n[BLOCKED {i+1}]")
        print("Source:", doc.metadata.get("source"))
        print("Department:", doc.metadata.get("department"))
        print("Allowed Roles:", doc.metadata.get("allowed_roles"))

    print("\n--- FINAL ALLOWED CHUNKS ---")
    for i, doc in enumerate(allowed_docs):
        print(f"\n[ALLOWED {i+1}]")
        print("Source:", doc.metadata.get("source"))
        print("Department:", doc.metadata.get("department"))
        print("Allowed Roles:", doc.metadata.get("allowed_roles"))
        print("Content:", doc.page_content[:300])

    print("=" * 70 + "\n")

