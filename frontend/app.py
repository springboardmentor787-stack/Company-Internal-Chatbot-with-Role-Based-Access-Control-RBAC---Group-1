import streamlit as st
import requests
from jose import jwt

API_BASE = "http://127.0.0.1:8000"
SECRET_KEY = "mysecret"
ALGORITHM = "HS256"

st.set_page_config(
    page_title="Company Internal Chatbot",
    page_icon="💼",
    layout="wide"
)

# ---------------- Session State ---------------- #

if "token" not in st.session_state:
    st.session_state.token = None

if "role" not in st.session_state:
    st.session_state.role = None

if "username" not in st.session_state:
    st.session_state.username = None

# ---------------- Authentication ---------------- #

def login(username, password):
    response = requests.post(
        f"{API_BASE}/login",
        data={
            "username": username,
            "password": password
        }
    )

    if response.status_code == 200:
        data = response.json()

        if "access_token" not in data:
            return False

        token = data["access_token"]

        # Decode JWT to extract role and username
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        st.session_state.token = token
        st.session_state.role = decoded["role"]
        st.session_state.username = decoded["sub"]

        return True

    return False


def logout():
    st.session_state.token = None
    st.session_state.role = None
    st.session_state.username = None


# ---------------- Chat ---------------- #

def ask_question(query):
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    response = requests.post(
        f"{API_BASE}/chat",
        json={"query": query},
        headers=headers
    )

    return response.json()


# ---------------- Admin ---------------- #

def get_logs():
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    response = requests.get(
        f"{API_BASE}/admin/logs",
        headers=headers
    )

    return response.json()


def get_stats():
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    response = requests.get(
        f"{API_BASE}/admin/stats",
        headers=headers
    )

    return response.json()


# ================= UI ================= #

st.title("💼 Company Internal Chatbot")

# -------- LOGIN SCREEN -------- #

if st.session_state.token is None:

    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        success = login(username, password)

        if success:
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

# -------- MAIN APP -------- #

else:

    st.sidebar.markdown("### User Info")
    st.sidebar.write(f"👤 Username: {st.session_state.username}")
    st.sidebar.write(f"🔐 Role: {st.session_state.role}")

    if st.sidebar.button("Logout"):
        logout()
        st.rerun()

    st.subheader("Ask a Question")

    query = st.text_input("Enter your question")

    if st.button("Submit Query"):
        if query.strip() == "":
            st.warning("Please enter a question.")
        else:
            result = ask_question(query)

            st.markdown("### Answer")
            st.write(result.get("answer", result))

    # -------- ADMIN DASHBOARD -------- #

    if st.session_state.role == "C-Level":

        st.markdown("---")
        st.subheader("📊 Admin Dashboard")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("View Logs"):
                logs = get_logs()
                st.write(logs)

        with col2:
            if st.button("View Stats"):
                stats = get_stats()
                st.write(stats)