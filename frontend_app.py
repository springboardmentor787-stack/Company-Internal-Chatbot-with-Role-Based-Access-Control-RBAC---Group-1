import streamlit as st
import requests

BACKEND = "http://127.0.0.1:8000"

st.set_page_config(page_title="Internal Role Based RAG", layout="wide")

# ---------------------------
# Role → accessible departments
# ---------------------------
ROLE_ACCESS = {
    "Finance": ["Finance", "General"],
    "HR": ["HR", "General"],
    "Engineering": ["Engineering", "General"],
    "Marketing": ["Marketing", "General"],
    "C-Level": ["Finance", "HR", "Engineering", "Marketing", "General"],
    "General": ["General"]
}

# ---------------------------
# Session state
# ---------------------------
if "token" not in st.session_state:
    st.session_state.token = None

if "role" not in st.session_state:
    st.session_state.role = None

if "username" not in st.session_state:
    st.session_state.username = None

if "chat" not in st.session_state:
    st.session_state.chat = []

if "accessible_docs" not in st.session_state:
    st.session_state.accessible_docs = []


# ---------------------------
# LOGIN PAGE
# ---------------------------
if st.session_state.token is None:

    st.title("🏢 Company Internal Chatbot")
    st.caption("Secure • Role-Based • RAG powered")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        r = requests.post(
            f"{BACKEND}/login",
            data={
                "username": username,
                "password": password
            }
        )

        if r.status_code == 200:
            st.session_state.token = r.json()["access_token"]
            st.session_state.username = username

            # -------------------------
            # Fetch role immediately
            # -------------------------
            headers = {
                "Authorization": f"Bearer {st.session_state.token}"
            }

            me = requests.get(f"{BACKEND}/me", headers=headers)

            if me.status_code == 200:
                st.session_state.role = me.json()["role"]
                st.session_state.accessible_docs = ROLE_ACCESS.get(
                    st.session_state.role, []
                )

            st.success("Login successful")
            st.rerun()

        else:
            st.error("Invalid credentials")


# ---------------------------
# CHAT PAGE
# ---------------------------
else:

    # ---------- SIDEBAR ----------
    with st.sidebar:

        st.markdown("### 👤 Logged in as")
        st.write(st.session_state.username)

        st.markdown("### 🔐 Role")
        st.success(st.session_state.role if st.session_state.role else "Unknown")

        st.markdown("---")

        st.markdown("### 📁 Accessible documents")

        if st.session_state.accessible_docs:
            for d in st.session_state.accessible_docs:
                st.markdown(f"- {d}")
        else:
            st.caption("No access information available")

        st.markdown("---")

        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

    # ---------- MAIN AREA ----------

    st.markdown("## 💬 Internal Knowledge Chat")
    st.caption("Ask questions based on your access level")

    query = st.text_input("Ask a question")

    if st.button("Send") and query.strip():

        headers = {
            "Authorization": f"Bearer {st.session_state.token}"
        }

        r = requests.post(
            f"{BACKEND}/rag-answer",
            json={"query": query},
            headers=headers
        )

        if r.status_code != 200:
            st.error(r.text)

        else:
            data = r.json()

            # keep role in sync (safety)
            st.session_state.role = data["user_role"]

            # accessible departments (not files)
            st.session_state.accessible_docs = ROLE_ACCESS.get(
                st.session_state.role, []
            )

            st.session_state.chat.append({
                "question": query,
                "answer": data["answer"],
                "confidence": data["confidence"],
                "sources": data["sources"],
                "blocked": data["blocked_chunks"]
            })


    # ---------- CHAT HISTORY ----------

    for msg in reversed(st.session_state.chat):

        st.markdown("### 🧑 You")
        st.info(msg["question"])

        st.markdown("### 🤖 Answer")

        if not msg["answer"]:
            st.warning("No accessible documents found for your role.")
        else:
            st.success(msg["answer"])

        with st.expander("📊 Details"):
            st.write("Confidence:", msg["confidence"])
            st.write("Blocked chunks:", msg["blocked"])
            st.write("Sources:")
            for s in msg["sources"]:
                st.markdown(f"- {s}")
