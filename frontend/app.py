import streamlit as st
import requests
import sys
import os
import json

# Add root folder to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from preprocessing.rbac_config import ROLE_HIERARCHY

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Company Internal Chatbot",
    layout="wide"
)

# ================= SESSION STATE =================
if "token" not in st.session_state:
    st.session_state.token = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# ================= THEME =================
if st.session_state.theme == "dark":
    background = "#0e1117"
    card_bg = "#1c1f26"
    text_color = "white"
    user_bg = "#2d3748"
else:
    background = "#f5f7fa"
    card_bg = "#ffffff"
    text_color = "#111111"
    user_bg = "#dbeafe"

# ================= STYLING =================
st.markdown(f"""
<style>
.main {{
    background-color: {background};
}}

h1, h2, h3, h4 {{
    color: {text_color};
}}

.user-msg {{
    background-color: {user_bg};
    padding: 12px;
    border-radius: 15px;
    margin-bottom: 10px;
}}

.bot-msg {{
    background-color: {card_bg};
    padding: 12px;
    border-radius: 15px;
    margin-bottom: 10px;
}}

.source-box {{
    background-color: {card_bg};
    padding: 8px;
    border-radius: 8px;
    margin-top: 5px;
}}
</style>
""", unsafe_allow_html=True)

# ================= LOGIN =================
if st.session_state.token is None:

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
        <div style='text-align:center; margin-top:80px;'>
            <h1 style="color:#ff8c00;">🤖 Secure Company Knowledge Assistant</h1>
            <p style='opacity:0.8; font-size:16px;'>
            AI-powered, role-based document intelligence system.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):
            response = requests.post(
                f"{API_URL}/login",
                json={"username": username, "password": password}
            )

            if response.status_code == 200:
                st.session_state.token = response.json()["access_token"]
                st.rerun()
            else:
                st.error("Invalid credentials")

# ================= DASHBOARD =================
else:

    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.get(f"{API_URL}/me", headers=headers)

    if response.status_code != 200:
        st.session_state.token = None
        st.stop()

    user = response.json()

    # ================= HEADER =================
    col1, col2 = st.columns([10, 1])

    with col1:
        st.markdown("""
        <div style="display:flex; align-items:center; gap:12px;">
            <div style="font-size:32px; color:#ff8c00;">🤖</div>
            <div>
                <h1 style="margin:0;">Company Internal Chatbot</h1>
                <p style="margin:0; opacity:0.7;">
                Secure Retrieval & AI-Powered Knowledge System
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        with st.popover("⋮"):
            if st.button("🌗 Toggle Theme"):
                st.session_state.theme = (
                    "light" if st.session_state.theme == "dark" else "dark"
                )
                st.rerun()

            if st.button("🗑 Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()

            if st.session_state.chat_history:
                chat_json = json.dumps(st.session_state.chat_history, indent=2)
                st.download_button(
                    label="📥 Download Chat",
                    data=chat_json,
                    file_name="chat_history.json",
                    mime="application/json"
                )

    # ================= SIDEBAR =================
    with st.sidebar:
        st.markdown("### 👤 User Profile")
        st.write(f"**Username:** {user['username']}")
        st.write(f"**Role:** {user['role']}")

        st.divider()

        st.markdown("### 📂 Accessible Departments")
        allowed = ROLE_HIERARCHY.get(user["role"], [])
        for dept in allowed:
            st.write(f"• {dept.capitalize()}")

        st.divider()

        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.chat_history = []
            st.rerun()

    # ================= CHAT FORM (FIXED) =================
    with st.form("chat_form", clear_on_submit=True):

        col_input, col_btn = st.columns([8, 1])

        with col_input:
            query = st.text_input("Ask your question")

        with col_btn:
            submitted = st.form_submit_button("Ask")

        if submitted and query.strip():

            st.session_state.chat_history.append(("user", query))

            with st.spinner("Generating response..."):
                chat_response = requests.post(
                    f"{API_URL}/chat",
                    json={"question": query},
                    headers=headers
                )

            if chat_response.status_code == 200:
                data = chat_response.json()
                answer = data.get("answer", "No response")
                confidence = data.get("confidence", 0.0)
                sources = data.get("sources", [])

                st.session_state.chat_history.append(
                    ("bot", answer, confidence, sources)
                )
            else:
                st.error("Server error.")

    # ================= DISPLAY CHAT =================
    for item in st.session_state.chat_history:

        if item[0] == "user":
            st.markdown(f"""
            <div class="user-msg">
            👤 <b>You:</b><br>{item[1]}
            </div>
            """, unsafe_allow_html=True)

        elif item[0] == "bot":
            _, answer, confidence, sources = item

            st.markdown(f"""
            <div class="bot-msg">
            <span style="color:#ff8c00; font-size:18px;">🤖</span> 
            <b style="color:#ff8c00;">Assistant:</b><br>
            {answer}
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"**Confidence:** {confidence * 100:.1f}%")

            if sources:
                st.markdown("**Sources:**")
                for src in sources:
                    st.markdown(
                        f"<div class='source-box'>{src}</div>",
                        unsafe_allow_html=True
                    )
