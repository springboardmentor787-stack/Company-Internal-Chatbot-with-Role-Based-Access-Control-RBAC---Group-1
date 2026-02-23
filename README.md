# Company-Internal-Chatbot-with-Role-Based-Access-Control-RBAC---Group-1

## Milestone 4 – Frontend & Deployment Preparation

---

## Overview
This milestone focuses on building the user-facing interface and integrating the complete backend pipeline to deliver an end-to-end secure RAG chatbot.

The objective is to provide employees with a conversational interface to query internal documents while enforcing strict role-based access control and maintaining transparency through document sources and confidence scores.

---

## What has been completed

### ✅ Streamlit Frontend Development
- Designed interactive chat interface
- Implemented login screen with authentication
- Displayed user information:
  - Username
  - Role
  - Accessible departments
- Built conversation UI:
  - User message display
  - AI answer display
  - Context details panel
- Implemented source document visibility
- Added confidence score and blocked chunk metrics
- Maintained chat history using session state

---

### ✅ Backend Integration
- Connected Streamlit frontend to FastAPI backend
- Implemented API calls:
  - `/login`
  - `/rag-chunks`
  - `/rag-answer`
  - `/me`
- Handled JWT authentication tokens
- Displayed role directly after login
- Updated accessible documents dynamically per query

---

### ✅ Secure RAG Pipeline Integration
- Retrieval via Chroma vector database
- RBAC filtering applied before generation
- Context passed to LLM for summarization
- Generated answers returned with:
  - Sources
  - Confidence
  - Access status

---

### ✅ Transparency & Monitoring
- Displayed retrieved context for debugging/demo
- Logged every query in audit logs
- Classified responses as:
  - ALLOWED
  - DENIED

---

## System Workflow
1. User logs into Streamlit application  
2. Frontend sends query to backend API  
3. Backend retrieves relevant document chunks  
4. RBAC filters unauthorized content  
5. Allowed context is passed to LLM  
6. LLM generates summarized answer  
7. Frontend displays answer, sources, and metrics  
8. Audit log records interaction  

---

## Technologies Used

### Frontend
- Streamlit

### Backend
- FastAPI
- LangChain
- Chroma Vector Database
- Sentence Transformers

### LLM
- Groq LLM API (Llama family models)

### Security
- JWT Authentication
- RBAC middleware
- Audit logging

---

## Key Features
- Secure enterprise chatbot
- Role-aware document retrieval
- Conversational interface
- Source transparency
- Confidence scoring
- Audit logging
- Modular API architecture

---

## Challenges Faced
- Local LLM performance limitations
- Context repetition in generated answers
- Deployment environment dependency issues
- Python version conflicts on cloud platforms
- Handling large dependency trees

---

## Limitations
- Integration testing partially completed
- Performance benchmarking pending
- Deployment configuration still evolving
- Limited dataset during development phase

---

## Future Improvements
- Automated evaluation metrics
- Streaming responses
- Document auto-ingestion
- Improved prompt engineering
- Production deployment pipeline
- Monitoring dashboard
- Multi-user scalability

---

## Milestone Outcome
Milestone 4 successfully delivers a working **secure RAG chatbot interface** with authentication, role-aware retrieval, and AI answer generation, preparing the system for full deployment and integration testing in the next phase.
