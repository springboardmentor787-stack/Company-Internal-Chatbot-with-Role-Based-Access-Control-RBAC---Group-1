import langchain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from document_loaders import all_documents
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", ".", " "],
    chunk_size=500,
    chunk_overlap=50,
    length_function=len
)

chunks = text_splitter.split_documents(all_documents)

print("Total chunks:", len(chunks))
print("Sample chunk metadata:", chunks[0].metadata)