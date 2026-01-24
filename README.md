Company Internal Chatbot with Role-Based Access Control (RBAC)

This project implements a secure internal chatbot for a company using semantic search and role-based access control (RBAC).
Employees can query internal documents, but access is strictly controlled based on their role and department.

📌Project Structure

company_chatbot_rbac/
│
├── data/
│   └── Fintech-data/
│       ├── HR/
│       ├── Finance/
│       ├── Marketing/
│       ├── Engineering/
│       └── general/
│
├── preprocessing/
│   ├── load_documents.py
│   ├── clean_documents.py
│   ├── chunk_documents.py
│   ├── vector_store.py
│   ├── rbac_config.py
│   ├── query_utils.py
│   ├── rbac_search.py
│   └── semantic_search.py
│
├── chroma_db/
├── .gitignore
├── README.md
└── venv/


🚀 Milestone 1: Document Ingestion & Vector Database
Objective

Prepare internal company documents for semantic search.

What was implemented?

->Loaded documents from multiple departments (HR, Finance, Marketing, Engineering, General)

->Cleaned and normalized text data

->Chunked documents into smaller semantic units

->Generated embeddings using: sentence-transformers/all-MiniLM-L6-v2
Stored embeddings in ChromaDB

Indexed documents with metadata:

department

source file

allowed roles

Output

Fully populated vector database

Verified document chunking and embedding storage

Initial filtering proof for department-based access.
 
🔐 Milestone 2: Role-Based Semantic Search (RBAC)
Objective

Enable secure, role-based access to documents using semantic search.

Roles Supported

HR

Finance

Engineering

Marketing

C-Level

General (only general documents)

Role Hierarchy : C-Level > Department Roles > General
What was implemented

Central RBAC configuration (rbac_config.py)

Role hierarchy enforcement

Query normalization (query_utils.py)

Semantic search with metadata filtering

Access validation before retrieval

Interactive terminal-based search interface

How Access Works

1.User enters:
  Role, Department, Query.
2.System validates role
3.RBAC rules are applied
4.If allowed → semantic search runs
5.If not allowed → access denied

Example

Finance user querying HR data → ❌ Access denied

C-Level querying any department → ✅ Access granted

General role accessing non-general data → ❌ Access denied 