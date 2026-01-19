# Milestone 1: Data Preparation & Vector Database

## Objective
Prepare company documents for semantic search by parsing, cleaning, chunking,
embedding, and indexing them into a vector database with role-based metadata.

## Features Implemented
- Parsed Markdown and CSV documents
- Cleaned and normalized text
- Chunked documents into manageable segments
- Assigned department and role-based metadata
- Generated sentence embeddings using Sentence Transformers
- Indexed embeddings using FAISS / ChromaDB

## How to Run

### 1. Load and preprocess documents
```bash
python loader.py
python clean_chunker.py
# Company-Internal-Chatbot-with-Role-Based-Access-Control-RBAC---Group-1
