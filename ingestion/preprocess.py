import re

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x20-\x7E]", " ", text)
    return text.strip()

def preprocess_documents(documents):
    for doc in documents:
        doc.page_content = clean_text(doc.page_content)
    return documents
