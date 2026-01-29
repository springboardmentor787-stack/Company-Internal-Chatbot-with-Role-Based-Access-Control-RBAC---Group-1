import re
import unicodedata

# Import document loader for verification/testing
# (File exists at ROOT level)
from load_documents import load_documents_with_metadata


# =====================================================
# FUNCTION: CLEAN RAW TEXT
# =====================================================
# Purpose:
# - Normalize encoding
# - Remove noisy characters
# - Standardize whitespace
# - Improve embedding & search quality

def clean_text(text: str) -> str:
    """
    Cleans raw text content by:
    - Normalizing Unicode characters
    - Removing extra spaces
    - Removing unwanted symbols
    """

    # Normalize Unicode (handles encoding issues)
    text = unicodedata.normalize("NFKD", text)

    # Replace multiple spaces/newlines with single space
    text = re.sub(r"\s+", " ", text)

    # Remove unwanted special characters
    # (keeps words, numbers, and basic punctuation)
    text = re.sub(r"[^\w\s.,:;!?()-]", "", text)

    return text.strip()


# =====================================================
# FUNCTION: CLEAN DOCUMENTS (METADATA PRESERVED)
# =====================================================
# Purpose:
# - Clean document text only
# - Keep RBAC metadata intact

def clean_documents(documents):
    """
    Cleans page_content of each document
    while preserving metadata (dept, roles, source).
    """

    cleaned_docs = []

    for doc in documents:
        cleaned_text = clean_text(doc.page_content)

        # Skip empty documents after cleaning
        if not cleaned_text:
            continue

        # Update text only (metadata untouched)
        doc.page_content = cleaned_text
        cleaned_docs.append(doc)

    return cleaned_docs


# =====================================================
# VERIFICATION / TEST RUN
# =====================================================
# Run this file directly to verify cleaning logic

if __name__ == "__main__":

    # Step 1: Load documents from Fintech-data
    docs = load_documents_with_metadata()

    # Step 2: Clean document text
    cleaned_docs = clean_documents(docs)

    # Print stats
    print(f"\n📄 Documents before cleaning: {len(docs)}")
    print(f"✨ Documents after cleaning: {len(cleaned_docs)}")

    # Show sample output
    if cleaned_docs:
        print("\n📌 Sample cleaned document metadata:")
        print(cleaned_docs[0].metadata)

        print("\n📝 Sample cleaned document text (first 200 chars):")
        print(cleaned_docs[0].page_content[:200])
