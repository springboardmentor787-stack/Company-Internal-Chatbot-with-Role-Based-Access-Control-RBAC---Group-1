from scripts.load_documents import load_documents
from scripts.clean_documents import clean_documents

docs = load_documents()
cleaned_docs = clean_documents(docs)

print(f"✅ Cleaned documents: {len(cleaned_docs)}\n")

sample = cleaned_docs[0]
print("📄 Content preview:")
print(sample.page_content[:300])

print("\n🔐 Metadata:")
print(sample.metadata)
