🏢 Company Internal Chatbot with Role-Based Access Control (RBAC)

A secure AI-powered internal chatbot that uses Retrieval-Augmented Generation (RAG) to provide department-specific company information with strict role-based access control.

📌 Project Overview

This project builds a secure internal chatbot system that:
•	Authenticates users using JWT
•	Assigns department-based roles (Finance, Marketing, HR, Engineering, C-Level, Employees)
•	Restricts document access based on role permissions
•	Uses semantic search over a vector database
•	Generates AI responses using a Retrieval-Augmented Generation (RAG) pipeline
•	Provides source citation for transparency
•	Logs access for auditing purposes
The system ensures secure, fast, and role-restricted knowledge retrieval for internal company use.

🎯 Project Objectives

This project builds a secure internal chatbot system that:
•	Authenticates users using JWT
•	Assigns department-based roles (Finance, Marketing, HR, Engineering, C-Level, Employees)
•	Restricts document access based on role permissions
•	Uses semantic search over a vector database
•	Generates AI responses using a Retrieval-Augmented Generation (RAG) pipeline
•	Provides source citation for transparency
•	Logs access for auditing purposes
The system ensures secure, fast, and role-restricted knowledge retrieval for internal company use.


🏗 System Architecture
User
   ↓
Streamlit Frontend
   ↓
FastAPI Backend
   ↓
JWT Authentication + RBAC Middleware
   ↓
Role-Filtered Semantic Search (Vector DB)
   ↓
RAG Pipeline (LLM + Context Augmentation)
   ↓
AI Response with Source Citation

🔹 Milestone 1: Data Preparation & Vector DB (Weeks 1–2)
•	Environment setup
•	Clone RAG document repository
•	Document exploration & role mapping
•	Preprocessing & chunking (300–512 tokens)
•	Metadata tagging with role permissions
Deliverables:
•	Cleaned document chunks
•	Role-document mapping
•	Preprocessing module
•	Validation report
________________________________________
🔹 Milestone 2: Backend Authentication & Search (Weeks 3–4)
•	Embedding generation using all-MiniLM-L6-v2
•	Vector database setup (Chroma/Qdrant)
•	Semantic search implementation
•	RBAC filtering logic
•	Role hierarchy definition
Deliverables:
•	Vector database with metadata
•	Search module
•	RBAC filtering module
•	Role validation test cases
________________________________________
🔹 Milestone 3: RAG Pipeline & LLM Integration (Weeks 5–6)
•	FastAPI backend setup
•	SQLite user database
•	JWT authentication
•	RBAC middleware
•	LLM integration (OpenAI/HuggingFace)
•	RAG pipeline implementation
•	Source attribution & confidence scoring
Deliverables:
•	Secure backend
•	JWT token system
•	RAG pipeline
•	Prompt templates
•	API endpoints
•	Test cases
________________________________________
🔹 Milestone 4: Frontend & Deployment (Weeks 7–8)
•	Streamlit chat interface
•	Login system
•	Role display
•	Source citation display
•	API integration
•	System testing
•	Documentation & deployment preparation
Deliverables:
•	Streamlit application
•	Integration test suite
•	API documentation
•	User guide
•	Deployment guide
•	Performance & security report
•	Demo video
•	Production-ready GitHub repository


🚀 Features
•	🔐 Secure JWT Authentication
•	🛡 Role-Based Access Control (RBAC)
•	🧠 Semantic Search using Vector Embeddings
•	🤖 Retrieval-Augmented Generation (RAG)
•	📚 Source Citation with Responses
•	📊 Confidence Scoring
•	🖥 Streamlit Chat UI
•	🗄 SQLite User Database
•	📜 Access Audit Logging
•	⚡ Fast Retrieval (<500ms target)
•	⏱ End-to-End Response (<3s target)

🧰 Tech Stack
Component	Technology
Backend	FastAPI (Python 3.8+)
Frontend	Streamlit
Vector Database	Chroma / Qdrant (Free Tier)
Embeddings	Sentence Transformers (all-MiniLM-L6-v2)
LLM	OpenAI GPT (Free Trial) / HuggingFace / LLaMA
Database	SQLite
Authentication	PyJWT
Version Control	GitHub



Document Categories
•	📊 Finance – Quarterly reports, financial summaries
•	📈 Marketing – Campaign reports, market analysis
•	👥 HR – Employee data, handbook, policies
•	⚙ Engineering – Technical architecture, processes
•	📘 General – Company policies, employee handbook
Each document is tagged with metadata specifying:
•	Department
•	Source file
•	Accessible roles


⚙ Installation Guide
1️⃣ Clone Repository
git clone 
cd company-internal-chatbot

2️⃣ Create Virtual Environment
python -m venv venv
Activate environment:
Windows:
venv\Scripts\activate
Mac/Linux:
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Backend (FastAPI)
uvicorn backend.main:app --reload
Backend runs at:

http://127.0.0.1:8000

5️⃣ Run Frontend (Streamlit)
streamlit run frontend/app.py

💬 Usage
1.	Open Streamlit application
2.	Login with valid credentials
3.	Ask department-related questions
4.	System retrieves relevant documents
5.	AI generates response using RAG
6.	Sources are displayed below the response
Example Role Access
Role	Access
Finance	Only finance documents
Marketing	Only marketing documents
HR	Only HR documents
Engineering	Only technical documents
Employees	General company documents
C-Level	All documents



📁 Project Structure
company-internal-chatbot/
│
├── backend/
│   ├── main.py
│   ├── auth.py
│   ├── rbac.py
│   ├── rag_pipeline.py
│   ├── database.py
│   └── models.py
│
├── frontend/
│   └── app.py
│
├── data/
├── vector_store/
├── requirements.txt
└── README.md

📊 Evaluation Criteria
Milestone	Target
Document Parsing	100% documents parsed
Metadata Accuracy	Accurate role mapping
Unauthorized Access	Zero data leaks
Retrieval Latency	< 500ms
End-to-End Response	< 3 seconds
Frontend Usability	Intuitive & responsive
Documentation	Complete & structured

🧪 Testing & Validation
•	Role-based access validation
•	Unauthorized access prevention tests
•	RAG accuracy testing
•	Performance benchmarking
•	Edge-case handling
•	Security validation


🚀 Deployment
•	Complete system integration
•	Security testing
•	Performance optimization
•	Documentation finalization
•	Demo video creation
•	GitHub production-ready repository
