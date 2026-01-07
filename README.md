# Company-Internal-Chatbot-with-Role-Based-Access-Control-RBAC---Group-1

## Milestone 1 – Data Preparation & Vector Database

### Overview
This milestone focuses on preparing company documents for a secure, role-aware RAG system.  
The goal is to parse, chunk, embed, and store documents with role-based metadata for later access control.

### What has been completed
- Cloned and explored the provided GitHub data repository
- Identified department folders:
  - Finance
  - Marketing
  - HR
  - Engineering
  - General
- Identified file formats:
  - Markdown (`.md`)
  - CSV (`.csv`)
- Defined a role-to-department permission map to support RBAC
- Implemented a document ingestion pipeline using LangChain:
  - `TextLoader` for Markdown/Text files
  - `CSVLoader` for CSV files
- Injected mandatory metadata into each document:
  - `department`
  - `allowed_roles`
  - `source` (filename)
- Chunked documents using `RecursiveCharacterTextSplitter`
  - Chunk size: 300–512 tokens
  - Chunk overlap: ~50 tokens
- Generated embeddings using `sentence-transformers/all-MiniLM-L6-v2`
- Stored all embedded chunks in a persistent ChromaDB vector store (`chroma_db`)

### Current Results
- Total documents loaded: **109**
- Total chunks created: **399**
- A local ChromaDB directory has been successfully created and persisted

### Notes
- Initial file-loading issues were encountered locally due to Windows path handling and hidden file extensions
- The ingestion pipeline was validated in Google Colab (Linux environment), confirming the logic is correct and portable

