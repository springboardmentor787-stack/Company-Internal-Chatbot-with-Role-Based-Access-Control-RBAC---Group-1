# Company-Internal-Chatbot-with-Role-Based-Access-Control-RBAC---Group-1

# 🤖 AI Company-Internal Chatbot with RBAC 

A secure, production-ready Company Internal Chatbot built using Retrieval-Augmented Generation (RAG) and strict Role-Based Access Control (RBAC). This system ensures that users can only retrieve information they are authorized to see, eliminating any possibility of cross-department data leakage.

---
🚀 Project Overview
--
This project implements a secure internal knowledge base where search results are filtered dynamically based on the user's role. It is designed to handle sensitive data like payroll (HR) or quarterly revenue (Finance) without exposing it to unauthorized staff. By integrating a RAG pipeline with enforced metadata filtering, we ensure that the AI only "sees" what the user is permitted to see.

---
🔒 Key Guarantees
-
- **Security is enforced at the database level :-** If a user lacks permissions, the system returns zero results rather than leaking data.
- **Role-Aware Context :-** The search engine is "blind" to any documents outside of the user's assigned departmental scope.
- **Data Integrity :-** 100% accurate role mapping ensures that sensitive files remain isolated.
- **Evidence-Based Responses :-** The system provides answers only from verified company documents, reducing AI hallucinations.
  
---
<h2>👥 Supported Roles & Access Scope</h2>

Access is governed by a strict hierarchy to maintain departmental privacy :

<table>
  <tr>
    <th>Role</th>
    <th>Access Permissions</th>
  </tr>
  <tr>
    <td>Finance</td>
    <td>Finance Documents + General Company Policies</td>
  </tr>
  <tr>
    <td>Marketing</td>
    <td>Marketing Reports + General Company Policies</td>
  </tr>
  <tr>
    <td>HR</td>
    <td>Personnel Files + HR Policies + General Company Policies</td>
  </tr>
  <tr>
    <td>Engineering</td>
    <td>Technical Architecture + Processes + General Policies</td>
  </tr>
  <tr>
    <td>Employees</td>
    <td>General Company Policies & Handbooks only</td>
  </tr>
  <tr>
    <td>C-Level</td>
    <td>Full Administrative Access (All Departments)</td>
  </tr>
</table>

---
🎯 Project Objectives:
--
**🔵 Milestone 1: Data Preparation & Vector DB**
   - Extract, clean, and chunk company documents (Markdown/CSV).
   - Index data into a vector database with precise role-based metadata tags.
     
**🔵 Milestone 2: Role-Based Access & Search Quality**
   - Implement RBAC filtering logic within the retrieval pipeline.
   - Optimize for high-speed retrieval (Target: < 500ms).
     
**🔵 Milestone 3: Authentication & RAG Pipeline**
   - Build a FastAPI backend with JWT authentication and LLM integration.
     
**🔵 Milestone 4: Frontend Usability & Deployment**
   - Develop a Streamlit web interface and finalize documentation.

---
<h2>📌 Milestone 1: Results & Verification</h2>
<h3>Status: ✅ COMPLETED</h3>

The foundation of the system is built upon robust data ingestion and structural organization.

- **Document Parsing:** 100% of .md, .csv, and .txt files from the repository are successfully parsed.

- **Token-Safe Chunking:** Implemented RecursiveCharacterTextSplitter to break documents into segments of **300-512 tokens**. This ensures context is preserved while staying within model limits.

- **Role-Based Metadata Injection:** Every text chunk is "stamped" with a metadata role tag, creating a secure link between the data and its authorized audience.

---
<h2>--- Phase 1: Loading & Role Modeling ---</h2>

- **Total documents loaded:** 21

- Accurate role mapping applied to all files.

<h2>--- Phase 2: Text Chunking ---</h2>

- **Total chunks created:** 182

- **Strategy:** Recursive Character Splitting (Size: 500, Overlap: 50)

🚀 How to Run

1. Setup Environment
   
   - cd C:/Users/naray/OneDrive/Desktop/Company_Internal_Chatbot
   ./venv/Scripts/activate
   
2. Load and preprocess documents
   - C:/Users/naray/OneDrive/Desktop/Company_Internal_Chatbot/venv/Scripts/python.exe c:/Users/naray/OneDrive/Desktop/Company_Internal_Chatbot/Fintech-data/load_documents.py
     
   - C:/Users/naray/OneDrive/Desktop/Company_Internal_Chatbot/venv/Scripts/python.exe c:/Users/naray/OneDrive/Desktop/Company_Internal_Chatbot/Fintech-data/chunk_documents.py
     
   - C:/Users/naray/OneDrive/Desktop/Company_Internal_Chatbot/venv/Scripts/python.exe c:/Users/naray/OneDrive/Desktop/Company_Internal_Chatbot/Fintech-data/Vectorization.py
     
   - C:/Users/naray/OneDrive/Desktop/Company_Internal_Chatbot/venv/Scripts/python.exe c:/Users/naray/OneDrive/Desktop/Company_Internal_Chatbot/Fintech-data/Role_filter.py
---
<h2>🔐 Milestone 2: RBAC Logic Results</h2>
<h3>Status:📝 WORKING</h3>

---
Company_Internal_Chatbot/

├── backend/

│   ├── app/

│   │   ├── rag/                # Milestones 1 & 2

│   │   │   ├── load_documents.py

│   │   │   ├── vector_store.py

│   │   │   └── retriever.py

│   │   ├── api/                # Milestone 3

│   │   │   ├── main.py

│   │   │   ├── auth.py

│   │   │   └── models.py

│   │   └── database/           # SQLite for Users

│   └── vector_db/              # Persistent ChromaDB

├── frontend/                   # Milestone 4

│   └── streamlit_app.py

├── data/

│   └── Fintech-data/           # Raw Source Files

├── requirements.txt

└── README.md
