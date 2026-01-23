# Company-Internal-Chatbot-with-Role-Based-Access-Control-RBAC---Group-1

## Problem Statement

This project builds a secure internal chatbot system that processes natural language queries and retrieves department-specific company information using Retrieval-Augmented Generation (RAG).

The system enforces Role-Based Access Control (RBAC) so that:
- Finance users only see finance documents  
- HR users only see HR documents  
- C-Level users can access all documents  

Unauthorized access is strictly prevented at both search and generation levels.

## Key Features

- Role-Based Access Control (RBAC) at query and retrieval level  
- Semantic search using vector database (Chroma/Qdrant)  
- Secure authentication with JWT  
- Retrieval-Augmented Generation (RAG) with source attribution  
- Streamlit-based chat interface  
- Audit logging for access tracking  

## System Architecture

High-level flow:

1. User logs in via Streamlit UI  
2. FastAPI authenticates user and extracts role from JWT  
3. Query is normalized and role-filtered  
4. Vector DB retrieves only authorized document chunks  
5. Retrieved context is sent to LLM  
6. LLM generates response with source citations  

RBAC is enforced at:
- API layer  
- Vector search layer  
- RAG context building layer  


## Milestone Breakdown

### Milestone 1: Data Preparation & Vector DB
- Document parsing (Markdown, CSV)
- Chunking and metadata tagging
- Role-to-document mapping
- Embedding generation and indexing

Location: `milestone_1_data_preparation/`

### Milestone 2: Backend Auth & Role-Based Search
- JWT authentication
- RBAC middleware
- Role-filtered semantic search

Location: `milestone_2_backend_search/`

### Milestone 3: RAG Pipeline & LLM Integration
- RAG pipeline implementation
- Prompt templates
- Source attribution

Location: `milestone_3_rag_pipeline/`

### Milestone 4: Frontend & Deployment
- Streamlit UI
- API integration
- End-to-end testing

Location: `milestone_4_frontend_deployment/`

## Tech Stack

- Backend: FastAPI, Python 3.8+  
- Frontend: Streamlit  
- Vector Database: Chroma / Qdrant (free tier)  
- Embeddings: Sentence-Transformers (all-MiniLM-L6-v2)  
- LLM: OpenAI GPT (free tier) / HuggingFace  
- Database: SQLite  
- Authentication: JWT (PyJWT)  


## Setup & Run

```bash
git clone <your-repo>
cd your-repo
pip install -r requirements.txt

# Run backend
uvicorn app.main:app --reload

# Run frontend
streamlit run milestone_4_frontend_deployment/streamlit_app/app.py


## Repository Structure

- milestone_1_data_preparation/   -> Parsing, chunking, metadata  
- milestone_2_backend_search/    -> Auth, RBAC, vector search  
- milestone_3_rag_pipeline/      -> RAG + LLM integration  
- milestone_4_frontend_deployment/ -> Streamlit UI  
- data/                          -> Raw and processed data  
- tests/                         -> Unit and integration tests  

