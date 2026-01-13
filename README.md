# Company-Internal-Chatbot-with-Role-Based-Access-Control-RBAC---Group-1
Project Overview

This project focuses on building the backend foundation for a secure company-wide internal chatbot.
Instead of directly exposing documents to a language model, the system first prepares and stores documents in a role-aware vector database, ensuring security is enforced at the data level itself.

The key idea behind this project is:

Semantic search should never bypass access control.

Even if two documents are semantically similar, users should only see content they are authorized to access based on their role.

Supported Roles

The system currently supports the following roles:

HR

Finance

Marketing

Engineering

General Employees

C-Level (full access across all departments)

Each role has a predefined scope of access that determines which department documents are visible.

Data Organization

All company documents are organized department-wise inside the repository:

Fintech-data/
├── finance/
├── marketing/
├── hr/
├── engineering/
└── general/


This folder structure is directly used to assign department-level metadata during document ingestion.

Supported File Formats

The document ingestion pipeline supports common internal documentation formats:

Markdown (.md) – policies, reports, technical documentation

CSV (.csv) – structured datasets and internal reports

All files are parsed and normalized before further processing.

Milestone 1: Document Ingestion & RBAC Foundation

Milestone 1 focuses on preparing documents so they can later be used in a secure, role-aware RAG system.

1. Repository Exploration & Data Understanding

Cloned and explored the provided GitHub repository

Analyzed folder structure and document distribution

Identified department-wise separation of data

Identified supported file formats used across teams

2. Role-to-Department Permission Mapping

A clear role-to-department access map was defined to support RBAC.

This mapping determines:

Which roles are allowed to access which department folders

Which documents should be visible or hidden for a given role

This permission logic forms the backbone of all future access control decisions.

3. Document Ingestion Pipeline (LangChain)

A document ingestion pipeline was implemented using LangChain, with:

TextLoader for Markdown files

CSVLoader for CSV files

Each document is loaded programmatically from its department folder and processed uniformly.

4. Metadata Injection for RBAC

During ingestion, mandatory metadata is injected into every document:

dept – department the document belongs to

allowed_roles – roles permitted to access the document

source – original filename

This metadata is preserved throughout the pipeline and later used to enforce role-based filtering.

5. Document Chunking

To ensure efficient processing and retrieval:

Documents are split into smaller chunks using RecursiveCharacterTextSplitter

Chunk configuration:

500 tokens per chunk

50 token overlap

Chunking ensures:

Context is preserved

Large documents can be searched accurately

Access control can be applied at a fine-grained level

6. Embedding Generation

Each document chunk is converted into a numerical vector using:

sentence-transformers/all-MiniLM-L6-v2

These embeddings capture the semantic meaning of the text and enable similarity-based retrieval.

7. Vector Database Storage

All embedded chunks are stored in a persistent ChromaDB vector database.

Each vector is stored along with its metadata

The database is persisted locally for reuse across runs

Metadata remains tightly coupled with embeddings to support secure filtering

Current Results

Total documents processed: 109

Total chunks created: 399

Persistent ChromaDB directory successfully created

RBAC logic validated using role-based access checks

When an unauthorized role attempts to access a department, the system correctly returns zero accessible records.