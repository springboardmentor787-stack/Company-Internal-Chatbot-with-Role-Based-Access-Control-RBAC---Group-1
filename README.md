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
  
----

  

