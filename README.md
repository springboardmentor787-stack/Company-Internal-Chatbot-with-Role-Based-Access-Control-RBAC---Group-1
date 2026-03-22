# 🏢 AI Company Internal Chatbot with Role-Based Access Control (RBAC)
## 🌐 Live Demo
| Component |	Link|
|-----------|-----|
|Frontend (Streamlit UI) |	https://Lakshmanpv-company-chatbot-frontend.hf.space/|
|Backend API (FastAPI Docs)|	[https://Lakshmanpv-chatbot.hf.space](https://huggingface.co/spaces/Lakshmanpv/chartbot)/docs|

⚠️ **Note:** Both frontend and backend are hosted on Hugging Face Spaces (Free CPU tier).
The first request may take 20–40 seconds if the Space is sleeping.


<h2> 📌 Project Overview </h2>
<h6>The Company Internal Chatbot is an AI-powered system that allows employees to query internal company documents using natural language.</h6>
<h6>It uses Retrieval-Augmented Generation (RAG) to generate accurate, context-based answers while enforcing Role-Based Access Control (RBAC) to ensure data security.</h6>

**The system combines:**
<ul>
  <li>🔐 Secure authentication</li>
  <li>🧠 Semantic search</li>
  <li>📚 Document retrieval</li>
  <li>🤖 AI response generation</li>
</ul>

----

📌 Project Statement:
----
The goal of this project is to build a secure internal chatbot system that processes natural language queries and retrieves department-specific company information using RetrievalAugmented Generation (RAG). The system will authenticate users, assign roles (Finance,Marketing, HR, Engineering, C-Level, Employees), and provide role-based access to company documents stored in a vector database. 

Users will input queries and receive context-rich,sourced responses restricted by their role permissions. All documents for RAG are provided via GitHub repository: https://github.com/springboardmentor441p-coderr/Fintech-data.

---
<h2>Expected Outcomes</h2>
<ul>
<li>Extract, preprocess, and index company documents (Markdown and CSV) into a vector database with role-based metadata tags.</li>
<li></l>Implement secure user authentication and role-based access control (RBAC) middleware.</li>
Build a RAG pipeline integrating semantic search with free LLMs (OpenAI GPT or open-source alternatives) to generate evidence-based responses.</li>
<li>Enforce role-based data access (e.g., Finance users see finance documents, Marketing sees marketing documents, and C-Level users have access to all documents).</li>
<li>Develop a Streamlit web interface for user login, chat interaction, and role-specific information retrieval.</li>
<li>Deploy a complete, fully documented system on GitHub using only free and open-source tools.</li>
</ul>

---

<h2>✨ Key Features</h2>

<h4>🔐 Secure Authentication</h4>
<ul>
  <li>JWT-based authentication using FastAPI.</li>
  <li>Users must log in to access the chatbot system.</li>
  <li>Passwords are securely stored using hashing (bcrypt).</li>
</ul>

---

### 🛡️ Role-Based Access Control (RBAC)</h4>
- Each user is assigned a role:
  - Finance
  - HR
  - Marketing
  - Engineering
  - Employees
  - C-Level
- RBAC is enforced at:
  - API layer
  - Document retrieval layer
- Unauthorized access is strictly blocked
- **C-Level users** have full access across all departments

---

<h2>📊 Access Control Levels</h2>
  
| Role              | Access Level                                    |
| ----------------- | ----------------------------------------------- |
| 👨‍💼 Employee    | Access to general company documents             |
| 💰 Finance        | Access to financial reports and finance data    |
| 📢 Marketing      | Access to marketing campaigns and reports       |
| 👥 HR             | Access to employee data and HR policies         |
| 🧑‍💻 Engineering | Access to technical and system documents        |
| 👨‍💻 Manager     | Access to employee + department-level documents |
| 🏢 C-Level        | Full access to all company documents            |
| 🛠 Admin          | Full system access + analytics + monitoring     |

---

<h3>📚 Retrieval-Augmented Generation (RAG)</h3>
<ul>
  <li>User queries are processed using a RAG pipeline</li>
  <li>Relevant document chunks are retrieved from the vector database</li>
  <li>Responses are generated only from retrieved context</li>
  <li>Prevents hallucinations and ensures factual accuracy</li>
  <li>If no data is found → system returns:</li>
  👉 “I don’t know”
</ul>

---

### 🧠 Semantic Search with Vector Database

- Documents are converted into embeddings using:
  - `sentence-transformers/all-MiniLM-L6-v2`
- Stored in ChromaDB
- Enables semantic similarity search instead of keyword matching
- Improves accuracy of information retrieval

---

### 📊 Confidence Scoring</h3>

- Each response includes a confidence score</li>
- Each response includes a confidence score
  - Calculated based on:
- Average similarity / vector distance
- Helps users evaluate answer reliability
  
---

### 🧾 Source Attribution</h3>
- Every response includes:
  - Source document references
- Ensures:
  - Transparency
  - Trustworthiness
  - Traceability
    
---

### 🖥️ Streamlit-Based User Interface
- Interactive UI built using Streamlit
- Features:
  - Login system
  - Chat interface
  - Role display
  - Real-time responses
   
---

### 🧩 Modular & Scalable Design
- Clean and modular code structure:
  - Preprocessing module 
  - Vector search module
  - RBAC module
  - RAG pipeline
  - Frontend
- Easy to extend:
  - Add new roles
  - Add new documents
  - Upgrade models

  ---

### 📝 Access Audit Logging
- Logs all:
  - User queries
  - Access attempts
- Helps in:
  - Monitoring usage
  - Debugging
  - Security auditing
   
---

### 🏗️ System Architecture

- The system follows a layered modular architecture designed for:
   - ✔ Security
   - ✔ Scalability
   - ✔ Maintainability
   - ✔ Clear separation of concerns
    
---

### 📥 Data Ingestion Pipeline (One-Time Setup)
**🔹 Step 1: Raw Documents**
- Stored in:
  ```
   data/raw/
  ```
- Includes:
 - Finance documents
 - HR policies
 - Marketing reports
 - Engineering docs
 - General handbook
  
---

**🔹 Step 2: Preprocessing & Chunking**
- Documents are:
  - Cleaned
  - Normalized
  - Split into chunks (300–512 tokens)
Each chunk contains metadata:
  - Source document
  - Department
  - Accessible roles
  - Token count
  
---

**🔹 Step 3: Embedding Generation**
- Model used:
```
sentence-transformers/all-MiniLM-L6-v2
```
- Converts text into vector embeddings

---

**🔹 Step 4: Vector Storage**
- Stored in ChromaDB
- Includes:
  - Embeddings
  - Metadata
- Enables:
  - ✔ Fast semantic search
  - ✔ Role-based filtering

---

<h2>🔄 User Query Flow (Runtime)</h2>

<h4>1️⃣ User Interface (Streamlit)</h4>
<ul>
  <li>User logs in via UI</li>
  <li>JWT token is generated</li>
</ul>
<h4>2️⃣ Authentication & RBAC</h4>
<ul>
  <li>Backend verifies JWT token</li>
  <li>Extracts user role</li>
  <li>Applies RBAC rules</li>
</ul>
<h4>3️⃣ Role-Filtered Semantic Search</h4>
<ul>
  <li>Query is converted into embedding</li>
  <li>Query is converted into embedding</li>
  <li>Vector DB is searched</li>
  <li>Results are filtered based on role</li>
  <li>Results are filtered based on role</li>
</ul>
<h4>4️⃣ RAG Pipeline</h4>
<ul>
  <li>Top relevant chunks are selected</li>
  <li>Context is added to prompt</li>
  <li>Sent to LLM (FLAN-T5)</li>
</ul>
<h4>5️⃣ Response Generation</h4>
<h5>System returns:</h5>
<ul>
  <li>✅ Answer</li>
  <li>📄 Source references</li>
  <li>📊 Confidence score</li>
</ul>
Also:
<li>Logs access for auditing</li>

---

<h2>🧠 Architecture Overview Diagram (Logical)</h2>


```text
+----------------------+
|    Streamlit UI      |
|  (User Interaction)  |
+----------+-----------+
           |
           v
+----------------------+
|   FastAPI Backend    |
|  - JWT Auth          |
|  - RBAC Enforcement  |
+----------+-----------+
           |
           v
+----------------------+
|   Vector Database    |
|     (ChromaDB)       |
|  - Embeddings        |
|  - Metadata          |
+----------+-----------+
           |
           v
+----------------------+
|     RAG Pipeline     |
|  - Context Builder   |
|  - FLAN-T5 LLM       |
+----------+-----------+
           |
           v
+----------------------+
|  Final Response      |
|  - Answer            |
|  - Sources           |
|  - Confidence Score  |
+----------------------+
```

---

<h1>🗂️ Milestone Breakdown</h1>

The project was developed in a structured, milestone-driven manner over 8 weeks, ensuring gradual progress from data preparation to deployment and documentation.

---

 Milestone 1: Data Preparation & Vector Database
 ----
<ins> 📆 Weeks 1 – 2 :- </ins>

<h3>Goal<h3>

Prepare company documents so the AI system can search them efficiently.
----
<h3>Tasks</h3>

<h4>Environment Setup</h4>
<ul>
<li>Install Python environment</li>
<li>Install required libraries:</li>
  <ul>
      <li>FastAPI</li>
      <li>Streamlit</li>
      <li>LangChain</li>
      <li>Sentence Transformers</li>
      <li>Pandas</li>
  </ul>
</ul>
<h3>Document Exploration</h3>

Analyze company documents from the GitHub repository.

**Document types:**
<ul>
  <li>Markdown</li>
  <li>CSV</li>
</ul>
<h3>Role-Document Mapping</h3>

**Example:**

|Role	    |Accessible |Documents
|-----    |-----------|---------|
|Finance  |	Financial | Reports|
|Marketing|	Marketing| campaigns|
|HR|	Employee| policies|
|Engineering|	Technical| architecture|
|Employees|	General| handbook|
|C-Level|	All| documents|

<h3>Document Preprocessing</h3>
<h4>Steps:</h4>
<ol>
  <li>Parse documents</li>
  <li>Clean text</li>
  <li>Split into chunks (300–512 tokens)</li>
  <li>Add metadata</li>
  <li>Store document chunks</li>
</ol>

<h3>Deliverables</h3>
<ul>
  <li>Clean document dataset</li>
  <li>Metadata mapping</li>
  <li>Document chunking system</li>
</ul>

---

🥈 Milestone 2: Backend Search & RBAC
----
<ins> 📆 Weeks 3 – 4 :- </ins>

<h3>Goal:-<h3>
  
Develop backend search system with secure role-based filtering.
----
<h3>Vector Database Creation</h3>

**Steps:**
<ol>
  <li>Generate embeddings</li>
  <li>Store embeddings in vector database</li>
  <li>Attach metadata</li>
  <li>Enable semantic search</li>
</ol>
Example DB:

```
Chroma DB
```

<h3>Role-Based Access Control</h3>

RBAC ensures users only see permitted documents.

Role hierarchy:

```
C-Level
   ↓
Department Staff
   ↓
General Employees
```

Example rule:

```
Finance users cannot access HR documents
```
<h3>Deliverables</h3>
<ul>
  <li>Vector database with embeddings</li>
  <li>Semantic search system</li>
  <li>Semantic search system</li>
</ul>

---

🥉 Milestone 3: RAG Pipeline & LLM Integration
----
<ins> 📆 Weeks 5 – 6 </ins>

<h3>Goal:-</h3>

Create the AI pipeline that generates answers using retrieved documents.
----
<h3>Authentication System</h3>

Backend uses **JWT authentication.**

**Steps:**
<ol>
  <li>User login</li>
  <li>Token generation</li>
  <li>Role verification</li>
  <li>Secure endpoint access</li>
</ol>

**Database:**

```
SQLite
```
**RAG Pipeline**

<h4>Pipeline flow:</h4>

```
User Query
   ↓
Retrieve Relevant Documents
   ↓
Add Context to Prompt
   ↓
Send Prompt to LLM
   ↓
Generate Response
```

**Additional Features**
<ul>
  <li>Source citation</li>
  <li>Confidence scoring</li>
  <li>Prompt templates</li>
</ul>
<h3>Deliverables</h3>
<ul>
  <li>RAG pipeline</li>
  <li>LLM integration</li>
  <li>Response generation system</li>
</ul>

---

🏅 Milestone 4: Frontend & Deployment
----
<ins> 📆 Weeks 7 – 8 </ins>
<h3>Goal:-</h3>

Build the UI and deploy the complete chatbot system.
----
<h3>Streamlit Frontend</h3>
<h4>Features:</h4>
<ul>
  <li>Login page</li>
  <li>Chat interface</li>
  <li>Role display</li>
  <li>Source citation</li>
  <li>Confidence bars</li>
</ul>
<h3>System Integration</h3>

**Combine:**

```
Frontend
+
Backend
+
Vector Database
+
LLM
```
<h3>Final Testing</h3>
**Testing includes:**
<ul>
  <li>Role access validation</li>
  <li>Query accuracy</li>
  <li>System performance</li>
  <li>Error handling</li>
</ul>
<h3>Deliverables</h3>
<ul>
  <li>Complete chatbot system</li>
  <li>Deployment</li>
  <li>User documentation</li>
  <li>Demo video</li>
  <li>GitHub repository</li>
</ul>

<h2>⚙️ Technology Stack</h2>

|Component|	Technology
|---------|-----------|
|Backend |	FastAPI|
|Frontend|	Streamlit|
|Vector Database |Chroma / Qdrant|
Embeddings|	Sentence Transformers|
|LLM	|OpenAI GPT |
|Database|	SQLite|
|Authentication|PyJWT|
|Version Control|GitHub|
---

## 🧰 Tech Stack

The project is built entirely using **free and open-source technologies**, ensuring accessibility, reproducibility, and ease of deployment.

---

### 🖥️ Backend
| Component | Technology |
|---------|------------|
| Web Framework | FastAPI |
| API Server | Uvicorn |
| Authentication | JWT (python-jose) |
| Password Security | bcrypt (passlib) |
| Database | SQLite |
| Access Control | Custom RBAC Middleware |

---

### 🧠 Retrieval & AI
| Component | Technology |
|---------|------------|
| Embedding Model | sentence-transformers/all-MiniLM-L6-v2 |
| Vector Database | ChromaDB |
| LLM | FLAN-T5 (google/flan-t5-base) |
| RAG Strategy | Retrieval-Augmented Generation |
| Confidence Scoring | Vector-distance-based scoring |

---

### 📄 Data Processing
| Component | Technology |
|---------|------------|
| Document Formats | Markdown, CSV |
| Text Processing | NLTK, Regex |
| Configuration | YAML |
| Data Handling | Pandas |

---

### 🖥️ Frontend
| Component | Technology |
|---------|------------|
| Web Interface | Streamlit |
| User Interaction | Chat-based UI |
| Source Display | Inline citations |

---

### 🔧 Dev & Utilities
| Component | Technology |
|---------|------------|
| Language | Python 3.8+ |
| Version Control | Git & GitHub |
| Logging | Python Logging |
| HTTP Client | Requests |
| Token Handling | tiktoken |

---

### ☁️ Deployment
| Component | Technology |
|---------|------------|
| Hosting | Local / VM |
| Package Management | pip + requirements.txt |
| Environment | Virtualenv / venv |

---

<h3>⚙️ Setup and Run Instructions</h3>

Follow the steps below to set up and run the project locally.

----

📌 Prerequisites
- Python **3.8 or higher**
- Git
- Virtual environment tool (`venv` or `virtualenv`)
- Internet connection (for model downloads on first run)

---

**🛠 Installation**

 📥 Clone Repo
```
git clone https://github.com/yourusername/company-chatbot-rbac.git
cd company-chatbot-rbac
```

### 🧪 Create and Activate Virtual Environment

It is recommended to use a Python virtual environment to isolate project dependencies.

---
#### 🪟 Windows
```bash
python -m venv venv
venv\Scripts\activate
```
#### 🪟 🐧 Linux / 🍎 macOS
```bash
python3 -m venv venv
source venv/bin/activate
```
### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```
---

### 🗂️ Initialize User Database

This step creates demo users and roles.

```bash
python milestone_3/init_db.py
```
---

### 📊 Prepare Vector Database
```bash
python milestone_1/preprocess_docs.py
python milestone_2/embedder.py
```
---

### 🚀 Start Backend
```bash
uvicorn milestone_3.main:app --workers 2
```
---

### 🖥️ Start Frontend

```bash
streamlit run milestone_4/app.py
```

## 🔐 RBAC Role Matrix

The system enforces **strict Role-Based Access Control (RBAC)** to ensure users can only access information permitted by their role.

Each document chunk is tagged with role metadata, and access is enforced at both the **API layer** and **vector retrieval layer**.

---

### 👥 User Roles

- **Employees**
- **Finance**
- **HR**
- **Marketing**
- **Engineering**
- **C-Level**

---

### 📄 Department Access Matrix

| Role        | Finance Docs | HR Docs | Marketing Docs | Engineering Docs | General Docs |
|------------|--------------|---------|----------------|------------------|--------------|
| Employees  | ❌ No        | ❌ No   | ❌ No          | ❌ No            | ✅ Yes       |
| Finance    | ✅ Yes       | ❌ No   | ❌ No          | ❌ No            | ✅ Yes       |
| HR         | ❌ No        | ✅ Yes  | ❌ No          | ❌ No            | ✅ Yes       |
| Marketing  | ❌ No        | ❌ No   | ✅ Yes         | ❌ No            | ✅ Yes       |
| Engineering| ❌ No        | ❌ No   | ❌ No          | ✅ Yes           | ✅ Yes       |
| C-Level    | ✅ Yes       | ✅ Yes  | ✅ Yes         | ✅ Yes           | ✅ Yes       |

---

<h2>📁 Project Structure Overview<h2></h2>

The project is organized by milestones to clearly reflect the development lifecycle and ensure modularity, scalability, and ease of maintenance.

```text
├── requirements.txt
├── README.md
│
├── config/
│   └── role_mapping.yaml
│
├── data/
│   ├── raw/
│   │   ├── finance/
│   │   ├── hr/
│   │   ├── marketing/
│   │   ├── engineering/
│   │   └── general/
│   │
│   ├── processed/
│   │   ├── chunks.json
│   │   └── chunks_with_embeddings.jsonl
│   │
│   └── chroma_db/
│
├── milestone_1/          # Data preparation & preprocessing
│   ├── cleaner.py
│   ├── chunker.py
│   ├── metadata.py
│   ├── preprocess_docs.py
│   └── validation_tests.py
│
├── milestone_2/          # Embedding & semantic search
│   ├── embedder.py
│   ├── search.py
│   └── check_chroma_db.py
│
├── milestone_3/          # Backend, RBAC & RAG
│   ├── main.py
│   ├── auth.py
│   ├── rbac.py
│   ├── rag.py
│   ├── llm.py
│   ├── routes.py
│   ├── ai_routes.py
│   ├── database.py
│   ├── models.py
│   ├── init_db.py
│   ├── users.db
│   ├── logs.py
│   └── access.log
│
└── frontend/          # Frontend
    └── app.py
    └── style.css
```

---
  
<h2>🎯 Expected System Performance</h2>

| Milestone | Evaluation Metric                    | Target                         |
| --------- | ------------------------------------ | ------------------------------ |
| 1         | Document parsing & metadata accuracy | 100% document parsing          |
| 2         | Role-based access & search quality   | Zero unauthorized access       |
| 3         | Authentication & RAG functionality   | Response < 3 seconds           |
| 4         | Frontend usability & deployment      | Working system + documentation |

---

<h2>🖼️ Screenshots</h2>

<h4>The following screenshots demonstrate the key functionalities of the system, including authentication, role-based access control, and RAG-based responses.</h4>

<h5>🔐 User Login Interface</h5>
Shows the Streamlit-based login screen where users authenticate using their credentials.
<img width="1364" height="621" alt="image" src="https://github.com/user-attachments/assets/dfa8c093-a6ef-45c6-9cfb-ee51c88951e5" />
<img width="1366" height="255" alt="image" src="https://github.com/user-attachments/assets/a91d450e-22fb-4984-864c-caab0ca3aef4" />

---

<h4>🚫 Role-Based Access Control (RBAC) – Access Denied (Wrong IDP)</h4>
Illustrates access denial when a user attempts to authenticate or query the system using an incorrect or unauthorized Identity Provider (IDP).
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/3941c78e-5663-4889-96ac-377f8fb1c3dc" />

---

<h2>🔑 Demo Credentials</h2>
<h4>The system comes with preconfigured demo users for testing different roles and access levels.</h4>

|Username|Password|Role
|--------|--------|---|
|hr_admin | Ln_Hr@2026! | HR|
|fin_manager | Ln_Fin#2026$ | Finance|
|eng_dev | Ln_Eng!2026# | Engineering|
|mkt_lead	| Ln_Mkt&2026* |Marketing|
|emp_user | Ln_Emp$2026! |	Employees|
|ceo_exec | Ln_CEO*Secure1 |	C-Level|

**These users are created during the one-time database initialization step using init_db.py.**

---

<h2>📄 License</h2>

This project is released under the **MIT License**.

You are free to use, modify, and distribute this project with proper attribution.

---

### 👨‍💻 Author :- Pirla Venkata Lakshmi Narayana
### 🎓 B.E CSE (AIML)
**Project Type:** Company Internal Chatbot with RBAC & RAG  
**Tech Stack:** FastAPI · Streamlit · ChromaDB · Sentence Transformers · FLAN-T5
