import os
import google.generativeai as genai
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for text in input:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=text,
                task_type="retrieval_document"
            )
            embeddings.append(result['embedding'])
        return embeddings

embedder = GeminiEmbeddingFunction()