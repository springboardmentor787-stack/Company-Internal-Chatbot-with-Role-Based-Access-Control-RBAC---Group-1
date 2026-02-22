"""
Milestone 3 Backend Prototype:
RBAC-secured Retrieval-Augmented Generation (RAG)
"""

from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from transformers import pipeline
from rbac_validation import is_access_allowed

TOP_K = 5 # Number of documents retrieved before RBAC filtering


def main():
    # ---------------------------
    # Load embedding model
    # ---------------------------
    embedding = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    # ---------------------------
    # Load existing Chroma DB
    # ---------------------------
    vectordb = Chroma(
        persist_directory="chroma_db",
        embedding_function=embedding
    )

    # ---------------------------
    # Load lightweight LLM
    # ---------------------------
    llm = pipeline(
        "text2text-generation",
        model="google/flan-t5-small",
        max_length=200
    )

    # ---------------------------
    # User Input
    # ---------------------------
    role = input("Enter your role: ").strip()
    query = input("Enter your query: ").strip()

    # ---------------------------
    # Retrieve relevant documents
    # ---------------------------
    retrieved_docs = vectordb.similarity_search(query, k=TOP_K)

    authorized_docs = []
    for doc in retrieved_docs:
        if is_access_allowed(role, doc.metadata):
            authorized_docs.append(doc)

    if not authorized_docs:
        print("\n❌ ACCESS DENIED")
        print("No authorized documents available for this role.")
        return

    # ---------------------------
    # Build context for LLM
    # ---------------------------
    context = "\n\n".join([doc.page_content for doc in authorized_docs])

    context = context[:2000]

    prompt = f"""
Answer the question using ONLY the context below.

Context:
{context}

Question:
{query}
"""

    # ---------------------------
    # Generate Answer
    # ---------------------------
    response = llm(prompt)

    print("\n✅ Answer:")
    print(response[0]["generated_text"])


if __name__ == "__main__":
    main()
