from langchain_text_splitters import RecursiveCharacterTextSplitter
from load_documents import all_documents

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunked_documents = []

for doc in all_documents:
    chunks = text_splitter.split_text(doc.page_content)
    for idx, chunk in enumerate(chunks):
        new_doc = doc.copy()              
        new_doc.page_content = chunk      

        new_doc.metadata["chunk_id"] = f"{doc.metadata['source']}__chunk_{idx}"

        chunked_documents.append(new_doc)

if __name__ == "__main__":
    print(f"Original documents: {len(all_documents)}")
    print(f"Total chunks created: {len(chunked_documents)}")
    sample = chunked_documents[0]

    print("\nSample chunk text:")
    print(sample.page_content[:200])

    print("\nSample chunk metadata:")
    print(sample.metadata)
