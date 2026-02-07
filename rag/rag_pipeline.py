from rag.llm_client import LLMClient
from rag.prompt_templates import build_rag_prompt
from document_loader.secure_semantic_search import secure_semantic_search

llm = LLMClient()

def run_rag(query: str, user_role: str,results):

    if not results:
        return {
            "answer": "Access denied or no relevant information found.",
            "sources": [],
            "confidence": 0.0
        }

    # Build context
    context = "\n\n".join([
    f"Source: {doc.metadata['source']}\n{doc.page_content[:400]}"
    for doc, _ in results
])

    prompt = build_rag_prompt(context, query)
    answer = llm.generate(prompt)

    sources = list(set(doc.metadata["source"] for doc, _ in results))

    return {
        "answer": answer,
        "sources": sources
    }
