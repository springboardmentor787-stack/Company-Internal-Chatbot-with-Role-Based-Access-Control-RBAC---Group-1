import re
import unicodedata
from load_documents import load_documents_with_metadata



# CLEAN TEXT


def clean_text(text: str) -> str:
    # Handle encoding issues
    text = unicodedata.normalize("NFKD", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove unwanted special characters
    text = re.sub(r"[^\w\s.,:;!?()-]", "", text)

    return text.strip()



# CLEAN DOCUMENTS (METADATA PRESERVED)


def clean_documents(documents):
    cleaned_docs = []

    for doc in documents:
        cleaned_text = clean_text(doc.page_content)

        if not cleaned_text:
            continue

        # Update text only, keep metadata
        doc.page_content = cleaned_text
        cleaned_docs.append(doc)

    return cleaned_docs



# VERIFICATION


if __name__ == "__main__":
    docs = load_documents_with_metadata()
    cleaned_docs = clean_documents(docs)

    print(f"Documents before cleaning: {len(docs)}")
    print(f"Documents after cleaning: {len(cleaned_docs)}")

    if cleaned_docs:
        print("\nSample cleaned document metadata:")
        print(cleaned_docs[0].metadata)

        print("\nSample cleaned document text (first 200 chars):")
        print(cleaned_docs[0].page_content[:200])
