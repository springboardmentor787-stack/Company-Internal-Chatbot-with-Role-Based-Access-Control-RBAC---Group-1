📌 Project Overview

This project focuses on building the backend foundation for a secure, company-wide internal chatbot.
Instead of directly exposing internal documents to a language model, the system pre-processes and stores documents in a role-aware vector database, ensuring that security is enforced at the data level itself.

🔐 Core Principle

Semantic search should never bypass access control.
Even if two documents are semantically similar, a user will only retrieve content they are authorized to access, strictly based on their role within the organization.

👥 Supported Roles

The system currently supports the following roles:
HR
Finance
Marketing
Engineering
General Employees
C-Level (full access across all departments)

Each role has a predefined access scope that determines which department documents are visible to them.

🗂️ Data Organization

All company documents are organized department-wise inside the repository:
Fintech-data/
├── finance/
├── marketing/
├── hr/
├── engineering/
└── general/

This folder structure is directly used during ingestion to assign department-level metadata to each document, forming the base for RBAC enforcement.
📄 Supported File Formats
The ingestion pipeline supports commonly used internal documentation formats:
Markdown (.md)
Used for policies, reports, and technical documentation
CSV (.csv)
Used for structured datasets and internal reports

All files are parsed, cleaned, and normalized before further processing.

🚀 Milestone 1: Document Ingestion & RBAC Foundation

Milestone 1 focuses on preparing documents so they can later be used in a secure, role-aware Retrieval-Augmented Generation (RAG) system.

1️⃣ Repository Exploration & Data Understanding
Cloned and explored the provided GitHub repository
Analyzed the folder structure and document distribution
Identified clear department-wise data separation
Verified supported file formats used across teams

2️⃣ Role-to-Department Permission Mapping
A clear role-to-department access map was defined to support RBAC.
This mapping determines:
Which roles can access which department folders
Which documents are visible or hidden for a given role
This permission logic forms the backbone of all future access control decisions.

3️⃣ Document Ingestion Pipeline (LangChain)
A document ingestion pipeline was implemented using LangChain, including:
TextLoader for Markdown files
CSVLoader for CSV files
Each document is loaded programmatically from its respective department folder and processed in a uniform and scalable manner.

4️⃣ Metadata Injection for RBAC
During ingestion, mandatory metadata is injected into every document:
dept → Department the document belongs to
allowed_roles → Roles permitted to access the document
source → Original filename
This metadata is preserved throughout the pipeline and later used to enforce strict role-based filtering.

5️⃣ Document Chunking
To ensure efficient retrieval and accurate search:
Documents are split into smaller chunks using
RecursiveCharacterTextSplitter
Chunk Configuration:
500 tokens per chunk
50 token overlap
This ensures:
Context is preserved
Large documents remain searchable

Access control can be applied at a fine-grained level

6️⃣ Embedding Generation
Each document chunk is converted into a numerical vector using:
sentence-transformers/all-MiniLM-L6-v2
These embeddings capture the semantic meaning of the text and enable similarity-based retrieval.

7️⃣ Vector Database Storage
All embedded chunks are stored in a persistent ChromaDB vector database.
Each vector is stored along with its metadata
The database is persisted locally for reuse across runs
Metadata remains tightly coupled with embeddings to support secure filtering

✅ Current Results

Total documents processed: 109
Total chunks created: 399
Persistent ChromaDB directory: Successfully created
RBAC logic: Fully validated

🔒 When an unauthorized role attempts to access a restricted department, the system correctly returns zero accessible records.
