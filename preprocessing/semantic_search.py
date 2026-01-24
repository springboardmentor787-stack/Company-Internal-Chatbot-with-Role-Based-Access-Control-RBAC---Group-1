from rbac_search import rbac_semantic_search


def run():
    print("\n🔐 Role-Based Semantic Search\n")

    role = input("Enter your role (HR / Finance / Engineering / Marketing / C-Level): ")
    department = input("Enter department to search (hr / finance / engineering / marketing / general): ")
    query = input("Enter your query: ")

    status, results = rbac_semantic_search(role, department, query)

    print("\nStatus:", status)
    print("Results found:", len(results))

    if status != "Access granted":
        return

    print("\nTop accessible results:\n")

    for idx, (doc, score) in enumerate(results, 1):
        print(f"Result {idx}")
        print("Source file :", doc.metadata.get("source_file"))
        print("Department  :", doc.metadata.get("dept"))
        print("Score       :", round(score, 4))
        print("Text:")
        print(doc.page_content[:300])
        print("-" * 60)


if __name__ == "__main__":
    run()
