from rag.gemini_client import LLMClient
from rag.prompt_templates import build_rag_prompt


llm = LLMClient()


def run_rag(query: str, user_role: str, results):

    if not results:
        return {
            "answer": "Access denied or no relevant information found.",
            "sources": []
        }

    # Build context
    context = "\n\n".join([
        doc.page_content
        for doc, _ in results
    ])

    prompt = build_rag_prompt(context, query)

    answer = llm.generate(prompt)

    sources = list(set(doc.metadata["source"] for doc, _ in results))

    return {
        "answer": answer,
        "sources": sources
    }
