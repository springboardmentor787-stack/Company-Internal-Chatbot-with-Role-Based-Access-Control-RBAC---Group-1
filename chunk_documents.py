from langchain_text_splitters import RecursiveCharacterTextSplitter

# Import document loader (ROOT-level file)
from load_documents import load_documents_with_metadata


# =====================================================
# FUNCTION: VALIDATE DOCUMENTS
# =====================================================
# Purpose:
# - Remove empty documents
# - Ensure required RBAC metadata exists
# - Prevent errors during chunking & embedding

def validate_documents(documents):
    """
    Filters documents to ensure:
    - Content is not empty
    - Required metadata keys are present
    """

    valid_docs = []

    for doc in documents:
        # Skip empty content
        if not doc.page_content or not doc.page_content.strip():
            continue

        # Ensure RBAC metadata exists
        if "dept" not in doc.metadata or "allowed_roles" not in doc.metadata:
            continue

        valid_docs.append(doc)

    return valid_docs


# =====================================================
# FUNCTION: CHUNK DOCUMENTS (ALL DEPARTMENTS)
# =====================================================
# Purpose:
# - Break large documents into smaller chunks
# - Improve embedding + retrieval performance
# - Preserve context using overlap

def chunk_documents(documents):
    """
    Splits validated documents into chunks
    while retaining metadata.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,     # Max characters per chunk
        chunk_overlap=60    # Context overlap between chunks
    )

    chunks = splitter.split_documents(documents)
    return chunks


# =====================================================
# VERIFICATION / TEST RUN
# =====================================================

if __name__ == "__main__":

    # Step 1: Load documents from Fintech-data (all departments)
    docs = load_documents_with_metadata()

    # Step 2: Validate documents (NEW step)
    validated_docs = validate_documents(docs)

    # Step 3: Chunk documents for vector embedding
    chunks = chunk_documents(validated_docs)

    # Print stats
    print(f"\n📄 Documents after validation: {len(validated_docs)}")
    print(f"🧩 Total chunks created: {len(chunks)}")

    # =================================================
    # SAMPLE OUTPUT: One chunk per department
    # =================================================
    print("\n📌 Sample chunk metadata per department:\n")

    seen_departments = set()

    for chunk in chunks:
        dept = chunk.metadata["dept"]

        if dept not in seen_departments:
            print(chunk.metadata)
            seen_departments.add(dept)

        if len(seen_departments) == 5:  # finance, hr, engineering, marketing, general
            break
