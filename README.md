🏢 Company Internal Chatbot with Role-Based Access Control (RBAC)

An enterprise-grade AI-powered internal knowledge assistant designed to securely retrieve organization-specific information using Role-Based Access Control (RBAC) and Retrieval-Augmented Generation (RAG).

📖 Table of Contents

Project Overview

Problem Statement

High-Level Architecture

System Sequence Diagram

Authentication Flow

Tech Stack

RBAC Design

RAG Pipeline

Deployment Architecture

Installation & Setup

Future Enhancements

Business Impact

🚀 Project Overview

The Company Internal Chatbot enables employees to securely query internal documents while enforcing strict access policies.

The system ensures:

Users can only access documents allowed for their role

Sensitive information remains protected

AI responses are contextual and accurate

No data leaves the organization

❗ Problem Statement

Organizations struggle with:

Unauthorized access to sensitive documents

Manual HR & IT query handling

Inefficient document retrieval

Unsafe AI adoption

Traditional chatbots lack role-based enforcement mechanisms.

This project solves that using:

RBAC

Vector search

Local LLM inference

Secure backend filtering


🔷 Logical Architecture
User → Streamlit UI → FastAPI Backend → 
Role Validation → Vector Database → 
LLM (Ollama) → Secure Response


🔷 Sequence Flow Explanation

User logs in with role credentials

Streamlit sends login request to FastAPI

FastAPI validates role

User submits query

Backend checks RBAC permissions

Query embedding generated

Vector DB retrieves filtered documents

Context sent to LLM

LLM generates response

Response returned to UI

If unauthorized:

Access Denied: You do not have permission to access this information.



🔷 Authentication & Authorization Flow
User → Login Page → Backend
             ↓
      Validate Credentials
             ↓
        Assign Role
             ↓
        Generate Session
             ↓
   Store Role in Context
             ↓
   Authorize Per Request

🛠️ Tech Stack
🔹 Backend

FastAPI

Python 3.10+

🔹 Frontend

Streamlit

🔹 AI & Retrieval

Ollama (Local LLM Runtime)

ChromaDB (Vector Database)

LangChain (RAG Orchestration)

🔹 Deployment

Docker

Docker Compose

👥 Role-Based Access Control (RBAC)
Role	Access Level
Admin	Full access
HR	HR documents only
Manager	Department-level data
Employee	General policies
🔷 RBAC Enforcement Logic

Each document contains metadata:

{
  "department": "HR",
  "allowed_roles": ["Admin", "HR"]
}


Before retrieval:

if user.role not in document.allowed_roles:
    deny_access()


RBAC is enforced before vector retrieval.

🧠 Retrieval-Augmented Generation (RAG)
RAG Pipeline

Document ingestion

Chunking

Embedding generation

Store in ChromaDB

Query embedding

Role-based filtering

Top-k retrieval

Context injection into LLM

Response generation

🏭 Production Deployment Architecture
🔷 Containerized Services
Docker Compose
│
├── api-service (FastAPI)
├── frontend-service (Streamlit)
└── ollama-service (LLM Runtime)

🔷 Network Architecture
User Browser
     │
     ▼
Streamlit Container (Port 8501)
     │
     ▼
FastAPI Container (Port 8000)
     │
     ▼
Ollama Container (Internal Network)
     │
     ▼
ChromaDB Volume

🛡️ Production Readiness
Category	Implementation
Security	RBAC enforced
Isolation	Docker containers
Scalability	Modular services
Maintainability	Clean architecture
Data Privacy	Local LLM runtime
Governance	Role metadata filtering
💻 Installation Guide (Local Development)
1️⃣ Clone Repository
git clone <repo-url>
cd company-internal-chatbot

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Install Ollama

Download from:
https://ollama.com

Pull model:

ollama pull llama3

▶️ Run Application
Start Backend
uvicorn main:app --reload

Start Frontend
streamlit run app.py


Access at:

http://localhost:8501

🐳 Docker Deployment
docker compose up --build

📂 Project Structure
company-internal-chatbot/
│
├── api/
│   ├── main.py
│   ├── rbac.py
│   ├── retrieval.py
│
├── frontend/
│   ├── app.py
│
├── vector_db/
│
├── Dockerfile.api
├── Dockerfile.streamlit
├── docker-compose.yml
├── requirements.txt
└── README.md

📈 Future Enhancements

JWT Authentication

OAuth Integration

PostgreSQL user management

LDAP / Active Directory integration

Kubernetes deployment

CI/CD pipeline

Monitoring & Logging stack

🎯 Business Impact

✔ Secure AI deployment
✔ Controlled access to sensitive data
✔ Reduced HR & IT workload
✔ Faster internal knowledge retrieval
✔ Enterprise-ready scalable system

👩‍💻 Developed By

Maulika R