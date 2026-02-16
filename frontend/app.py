import streamlit as st
import requests
import datetime

# =====================================================
# CONFIGURATION
# =====================================================

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Company Internal Chatbot",
    page_icon="🤖",
    layout="wide"
)

# =====================================================
# STYLING
# =====================================================

st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
section[data-testid="stSidebar"] {
    background-color: #1f2937;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION INITIALIZATION
# =====================================================

def initialize_session():
    defaults = {
        "access_token": None,
        "username": None,
        "role": None,
        "department": None,
        "chat_history": [],
        "conversation_history": [],
        "sources": [],
        "confidence": None
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session()

# =====================================================
# API FUNCTIONS
# =====================================================

def login_user(username, password):
    try:
        response = requests.post(
            f"{API_BASE_URL}/login",
            data={"username": username, "password": password}
        )

        if response.status_code == 200:
            return response.json()
        else:
            st.error("❌ Invalid credentials")
            return None

    except Exception as e:
        st.error(f"Backend connection error: {e}")
        return None


def send_query(query):
    headers = {
        "Authorization": f"Bearer {st.session_state.access_token}"
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/rag-chunks",
            json={"query": query},
            headers=headers
        )

        if response.status_code == 200:
            return response.json()
        else:
            st.error("Query failed.")
            return None

    except Exception as e:
        st.error(f"Connection error: {e}")
        return None


# =====================================================
# SAVE CHAT (SAFE + NO DUPLICATES)
# =====================================================

def save_chat():
    if st.session_state.chat_history:

        if (
            not st.session_state.conversation_history
            or st.session_state.conversation_history[-1]["messages"]
            != st.session_state.chat_history
        ):
            timestamp = datetime.datetime.now().strftime("%d %b %H:%M")
            st.session_state.conversation_history.append({
                "title": f"Chat - {timestamp}",
                "messages": st.session_state.chat_history.copy()
            })


# =====================================================
# LOGIN PAGE
# =====================================================

def show_login():
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("## 🔐 Company Internal Chatbot Login")
        st.markdown("---")

        with st.form("login_form"):
            username = st.text_input("👤 Username")
            password = st.text_input("🔑 Password", type="password")
            submitted = st.form_submit_button("Login")

            if submitted:
                result = login_user(username, password)

                if result:
                    st.session_state.access_token = result["access_token"]
                    st.session_state.username = result["username"]
                    st.session_state.role = result["role"]
                    st.session_state.department = result.get("department", result["role"])
                    st.success("Login Successful!")
                    st.rerun()


# =====================================================
# SIDEBAR
# =====================================================

def show_sidebar():
    with st.sidebar:

        # =========================
        # USER PROFILE
        # =========================
        st.markdown("## 👤 User Profile")
        st.write(f"**Username:** {st.session_state.username}")
        st.write(f"**Role:** {st.session_state.role}")
        st.write(f"**Department:** {st.session_state.department}")

        st.markdown("---")

        # =========================
        # NEW CHAT
        # =========================
        if st.button("➕ New Chat"):
            save_chat()
            st.session_state.chat_history = []
            st.session_state.sources = []
            st.session_state.confidence = None
            st.rerun()

        st.markdown("---")

        # =========================
        # CHAT HISTORY
        # =========================
        st.markdown("### 🕓 Chat History")

        if not st.session_state.conversation_history:
            st.info("No previous chats")

        # Show latest first
        for i, convo in enumerate(reversed(st.session_state.conversation_history)):
            if st.button(convo["title"], key=f"history_{i}"):

                st.session_state.chat_history = convo["messages"]
                st.session_state.sources = []
                st.session_state.confidence = None
                st.rerun()

        st.markdown("---")

        # =========================
        # LOGOUT (SAFE)
        # =========================
        if st.button("🚪 Logout"):
            save_chat()  # Save before logout

            st.session_state.access_token = None
            st.session_state.username = None
            st.session_state.role = None
            st.session_state.department = None
            st.session_state.chat_history = []
            st.session_state.sources = []
            st.session_state.confidence = None

            st.rerun()


# =====================================================
# CHAT INTERFACE
# =====================================================

def show_chat_interface():
    st.markdown("## 🤖 AI Assistant")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Ask your department-related question...")

    if user_input:

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        with st.spinner("🔎 Retrieving documents..."):
            result = send_query(user_input)

        if result:
            chunks = result.get("allowed_chunks", [])
            confidence = result.get("confidence", 0.0)

            st.session_state.sources = chunks
            st.session_state.confidence = confidence

            if chunks:
                answer_text = f"✅ Found {len(chunks)} relevant document(s)."
            else:
                answer_text = "⚠ No accessible documents found."
        else:
            answer_text = "⚠ Server error."

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer_text
        })

        st.rerun()


# =====================================================
# SOURCE DOCUMENT SECTION
# =====================================================

def show_sources():
    if st.session_state.sources:

        st.markdown("---")
        st.markdown("## 📚 Source Documents")

        for i, chunk in enumerate(st.session_state.sources, 1):
            with st.expander(f"📄 Source {i} | Dept: {chunk.get('dept')}"):
                st.write(f"**File:** {chunk.get('source')}")
                st.write(f"**Allowed Roles:** {chunk.get('allowed_roles')}")
                st.write("**Content Preview:**")
                st.write(chunk.get("content"))

        if st.session_state.confidence is not None:
            st.success(f"🔎 Confidence Score: {st.session_state.confidence:.2f}")


# =====================================================
# MAIN
# =====================================================

if not st.session_state.access_token:
    show_login()
else:
    show_sidebar()
    show_chat_interface()
    show_sources()

# ---------------- SAMPLE QUERIES ----------------
# Marketing:
#   Summarize key highlights of Q4 2024 marketing report
#
# Finance:
#   Summarize the key financial highlights of Q1 2024
#
# Engineering:
#   Describe the backend system architecture