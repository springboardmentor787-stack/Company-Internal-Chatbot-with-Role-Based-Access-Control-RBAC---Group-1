# Company Internal Chatbot with Role-Based Access Control (RBAC)

A secure backend system for a **company-wide internal chatbot** built using  
**Retrieval-Augmented Generation (RAG)**, **Vector Databases**, and **Role-Based Access Control (RBAC)**.

The project focuses on **security-first design** — ensuring that users can only retrieve
information they are authorized to see, even during semantic search and AI-generated responses.

---
## 📌 Project Overview

In a real company, internal documents belong to different departments (HR, Finance, Engineering, etc.).
If we directly connect these documents to a language model, **sensitive data leakage becomes a serious risk**.

This project solves that problem by:

- Preprocessing and embedding documents **with role-based metadata**
- Storing them in a **role-aware vector database**
- Enforcing RBAC **before and after semantic retrieval**
- Integrating a **secure RAG pipeline** that generates answers only from authorized content

> 🔐 **Core Rule:**  
> Semantic similarity should never bypass access control.
---

## 👥 Supported Roles

The system currently supports the following organizational roles:

- **HR**
- **Finance**
- **Marketing**
- **Engineering**
- **General Employee**
- **C-Level** (access to all departments)

Each role has a clearly defined access scope that determines which documents are visible.

---
## 🗂️ Data Organization

All documents are organized department-wise inside the repository:

Fintech-data/
├── finance/
├── marketing/
├── hr/
├── engineering/
└── general/

This folder structure is **directly used during ingestion** to assign department metadata,
which becomes the foundation for RBAC enforcement.
---

## 📄 Supported File Formats

The ingestion pipeline supports common internal documentation formats:

- **Markdown (`.md`)**
  - Policies, reports, technical documentation
- **CSV (`.csv`)**
  - Structured datasets, summaries, internal reports

All files are parsed, cleaned, and normalized before embedding.

---
# 🚀 Milestone 1: Document Ingestion & RBAC Foundation

Milestone 1 focuses on **preparing documents** so they can later be used in a secure,
role-aware RAG system.
---
### 1️⃣ Repository Exploration & Data Understanding

- Cloned and explored the provided GitHub dataset
- Analyzed folder structure and department separation
- Identified supported file formats across departments
- Verified that data can be cleanly mapped to roles
---

### 2️⃣ Role-to-Department Permission Mapping

A clear role-to-department access map was defined.

This mapping determines:
- Which roles can access which department folders
- Which documents are visible or hidden for a user

This logic becomes the **single source of truth** for access control throughout the project.
---

### 3️⃣ Document Ingestion Pipeline (LangChain)

A scalable ingestion pipeline was implemented using **LangChain**, including:

- `TextLoader` for Markdown files
- `CSVLoader` for CSV files

Each document is loaded programmatically and treated uniformly, making the pipeline easy to extend.
---

### 4️⃣ Metadata Injection for RBAC

During ingestion, **mandatory metadata** is attached to every document chunk:

- `dept` → Department the document belongs to
- `allowed_roles` → Roles permitted to access the document
- `source` → Original filename

This metadata stays attached to embeddings and is later used for **strict RBAC filtering**.
---

### 5️⃣ Document Chunking

Documents are split into smaller, searchable units using:

- `RecursiveCharacterTextSplitter`

**Chunk configuration:**
- Chunk size: **~500 tokens**
- Overlap: **~50 tokens**

This ensures:
- Context preservation
- Efficient semantic search
- Fine-grained access control at chunk level
---

### 6️⃣ Embedding Generation

Each document chunk is converted into a vector using:
These embeddings capture semantic meaning and enable similarity-based retrieval.
---

### 7️⃣ Vector Database Storage

All embeddings are stored in a **persistent ChromaDB vector store**.

- Metadata is stored alongside embeddings
- Database is reused across runs
- Enables secure, role-aware retrieval
---

### ✅ Milestone 1 Results

- **Total documents processed:** 109  
- **Total chunks created:** 399  
- **Persistent ChromaDB:** Successfully created  
- **RBAC validation:** Passed  

Unauthorized roles correctly receive **zero accessible records**.

--

# 🚀 Milestone 2: Semantic Search with RBAC Enforcement

Milestone 2 builds on the ingestion pipeline to enable **secure semantic search**.

---

### 🔎 Semantic Search Flow

1. User submits a natural-language query
2. Query is normalized and embedded
3. Vector similarity search retrieves top-K chunks
4. **RBAC filtering is applied after retrieval**
5. Only authorized chunks are returned

This prevents:
- Privilege escalation
- Cross-department leakage
- Inference attacks via embeddings

---

### 🔐 Key Security Principle

RBAC is enforced **after vector retrieval**, not before.

This ensures that:
- Similarity search remains accurate
- Unauthorized content is never exposed
- Metadata cannot be inferred from results

---

# 🚀 Milestone 3: Backend Authentication with RBAC and RAG/LLM Integration
**🔹 Module 5: Backend Authentication & RBAC Middleware**

Module 5 introduces a fully functional backend with secure authentication and role-based access control.
✔ FastAPI Backend Setup
-FastAPI backend initialized and modularized
-Clean separation of authentication, database, routes, and middleware
-Swagger / OpenAPI enabled for interactive API testing

✔ User Database (SQLite)
-SQLite database implemented using SQLAlchemy
-User model includes:
-Username
-Hashed password
-Role
-Sample users created for RBAC validation

✔ Authentication (Login Flow)
-Secure login endpoint implemented
-Passwords verified using hashing
-Successful login returns a JWT access token

✔ JWT Token Handling
JWT tokens contain:
-Username
-Role
-Tokens are validated on every protected request
-Invalid or missing tokens are rejected automatically

✔ RBAC Middleware & Protected Routes
-Centralized role-based access control (RBAC) dependency
-Role checks applied at route level
-Access examples:
--HR-only endpoints
--Finance-only endpoints
--Engineering endpoints
--C-Level full-access endpoints
--General employee endpoints

✅ Module 5 Outcome
-Secure authentication system implemented
-Consistent RBAC enforcement across backend
-Backend ready for AI-powered document workflows

**🔹 Module 6: RAG Pipeline & LLM Integration**

Module 6 integrates a secure Retrieval-Augmented Generation (RAG) pipeline with the RBAC-enabled backend.

🧠 Objective
-To generate AI responses only from authorized documents, with:
-Role-aware filtering
-Source attribution
-Confidence scoring

🔗 RAG Pipeline Flow
User → Authentication
     → Role Identification
     → RBAC-Filtered Retrieval
     → Context Assembly
     → LLM Response Generation
     → Source Attribution + Confidence Score

🤖 LLM Integration
-Free HuggingFace LLM used for response generation
-LLM never accesses raw documents directly
-Only authorized document chunks are provided as context
-Prompt structure reduces hallucinations

🧩 Prompt Design
-System instructions
-Retrieved document context
-User query
-Explicit instruction to answer only from provided context

📌 Source Attribution
Each response includes:
-File name
-Department
-Chunk ID
-Relevance score
-This makes the system auditable and explainable.

📊 Confidence Scoring
-Confidence score is calculated using:
-Average similarity score of retrieved chunks
-Number of relevant chunks used
-Normalized relevance range
-This avoids blind trust in AI responses.

✅ Module 6 Outcome
-End-to-end secure RAG pipeline implemented
-Role-based document retrieval enforced
-AI responses generated only from authorized data
-Source attribution and confidence scoring included
-System ready for UI integration or production hardening

🔐 Final Security Guarantee
At no point can:
-HR access Finance documents
-Engineering access HR data
-General employees access restricted departments
-Even when documents are semantically similar, RBAC always takes priority.





