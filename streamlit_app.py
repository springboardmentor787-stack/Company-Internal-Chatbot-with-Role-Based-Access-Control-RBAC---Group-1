import streamlit as st
import requests
import time
import json
import pandas as pd
import os
from chat_db import *

init_chat_db()

API_URL = os.getenv("API_URL", "http://localhost:8000")

# ----------------------------
# SESSION STATE INIT
# ----------------------------
if "token" not in st.session_state:
    st.session_state.token = None

if "username" not in st.session_state:
    st.session_state.username = None

if "role" not in st.session_state:
    st.session_state.role = None

if "conversations" not in st.session_state:
    st.session_state.conversations = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Secure Enterprise LLM", layout="wide")

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.title("🔐 User Panel")

mode = st.sidebar.radio("🌗 Select Mode", ["Light", "Dark"])

if mode == "Dark":
    st.markdown("""
        <style>
        .stApp {
            background-color: #0E1117;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

ROLE_ACCESS_MAP = {
    "HR": ["HR", "General"],
    "Finance": ["Finance", "General"],
    "Engineering": ["Engineering", "General"],
    "Marketing": ["Marketing", "General"],
    "C-Level": ["HR", "Finance", "Engineering", "Marketing", "General"]
}

# ----------------------------
# AFTER LOGIN → LOAD USER CHATS
# ----------------------------
if st.session_state.username and not st.session_state.conversations:
    st.session_state.conversations = load_user_conversations(
        st.session_state.username
    )

# ----------------------------
# USER INFO
# ----------------------------
if st.session_state.username:
    st.sidebar.markdown(f"### 👤 {st.session_state.username}")
    st.sidebar.markdown(f"**Role:** `{st.session_state.role}`")

    st.sidebar.markdown("### 📂 Accessible Data")
    for item in ROLE_ACCESS_MAP.get(st.session_state.role, []):
        st.sidebar.write(f"• {item}")

    st.sidebar.markdown("---")
    st.sidebar.markdown("## 💬 Conversations")

    # ➕ NEW CHAT
    if st.sidebar.button("➕ New Chat"):
        chat_name = f"Chat {len(st.session_state.conversations) + 1}"
        st.session_state.conversations[chat_name] = []

        save_conversation(
            st.session_state.username,
            chat_name,
            []
        )

        st.session_state.current_chat = chat_name
        st.rerun()

    # SHOW CHATS
    for chat_name in list(st.session_state.conversations.keys()):

        col1, col2, col3 = st.sidebar.columns([4, 1, 1])

        if col1.button(chat_name):
            st.session_state.current_chat = chat_name
            st.rerun()

        # Rename
        if col2.button("✏️", key=f"rename_{chat_name}"):
            st.session_state.rename_target = chat_name

        # Delete
        if col3.button("🗑", key=f"delete_{chat_name}"):
            delete_conversation(st.session_state.username, chat_name)
            del st.session_state.conversations[chat_name]

            if st.session_state.current_chat == chat_name:
                st.session_state.current_chat = None

            st.rerun()

    # Rename UI
    if "rename_target" in st.session_state:
        new_name = st.sidebar.text_input("New name")

        if st.sidebar.button("Save Rename"):
            old_name = st.session_state.rename_target

            rename_conversation(
                st.session_state.username,
                old_name,
                new_name
            )

            st.session_state.conversations[new_name] = \
                st.session_state.conversations.pop(old_name)

            st.session_state.current_chat = new_name
            del st.session_state.rename_target
            st.rerun()

    # Logout
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

else:
    st.sidebar.warning("Not logged in")

# ----------------------------
# TITLE
# ----------------------------
st.title("💬 Secure RBAC Enterprise Chatbot")

# ----------------------------
# LOGIN
# ----------------------------
if not st.session_state.token:

    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = requests.post(
            f"{API_URL}/login",
            data={"username": username, "password": password}
        )

        if response.status_code == 200:
            data = response.json()

            st.session_state.token = data["access_token"]
            st.session_state.username = data["username"]
            st.session_state.role = data["role"]

            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

# ----------------------------
# CHAT SECTION
# ----------------------------
if st.session_state.token:

    if not st.session_state.current_chat:
        if not st.session_state.conversations:
            chat_name = "Chat 1"
            st.session_state.conversations[chat_name] = []
            save_conversation(st.session_state.username, chat_name, [])
            st.session_state.current_chat = chat_name
        else:
            st.session_state.current_chat = list(
                st.session_state.conversations.keys()
            )[0]

    current_chat = st.session_state.current_chat
    messages = st.session_state.conversations[current_chat]

    st.markdown(f"### 🗂 {current_chat}")

    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_prompt = st.chat_input("Ask your question...")

    if user_prompt:

        messages.append({"role": "user", "content": user_prompt})
        update_conversation(
            st.session_state.username,
            current_chat,
            messages
        )

        with st.chat_message("user"):
            st.markdown(user_prompt)

        headers = {
            "Authorization": f"Bearer {st.session_state.token}"
        }

        with st.chat_message("assistant"):
            placeholder = st.empty()

            with st.spinner("Thinking..."):
                response = requests.post(
                    f"{API_URL}/chat",
                    json={"query": user_prompt, "user_role": st.session_state.role},
                    headers=headers
                )

            if response.status_code == 200:

                data = response.json()

                answer = data["answer"]
                confidence = data.get("confidence", 0)
                blocked = data.get("blocked_chunks", 0)
                sources = data.get("sources", [])

                # Typing animation
                displayed = ""
                for char in answer:
                    displayed += char
                    placeholder.markdown(displayed)
                    time.sleep(0.01)

                messages.append({"role": "assistant", "content": answer})
                update_conversation(
                    st.session_state.username,
                    current_chat,
                    messages
                )

                # DETAILS SECTION
                with st.expander("📊 Details"):
                    st.markdown(f"**Confidence:** `{confidence}`")
                    st.markdown(f"**Blocked chunks:** `{blocked}`")
                    st.markdown("**Sources:**")
                    for src in sources:
                        st.write(f"• {src}")

            elif response.status_code == 403:
                st.error("🚫 Access Denied (RBAC)")
            else:
                st.error("Server error")

# ==========================================================
# 🛡️ ENTERPRISE ADMIN DASHBOARD (ADDED - DOES NOT MODIFY ABOVE CODE)
# ==========================================================

if st.session_state.token and st.session_state.role == "C-Level":

    st.sidebar.markdown("---")
    st.sidebar.markdown("## 🛡️ Admin Panel")

    admin_page = st.sidebar.radio(
        "Admin Options",
        ["💬 Chat View", "📊 Logs Dashboard"]
    )

    # Hide chat visually if Admin chooses Logs
    if admin_page == "📊 Logs Dashboard":

        st.markdown("---")
        st.title("🛡️ Enterprise Audit Monitoring")

        headers = {
            "Authorization": f"Bearer {st.session_state.token}"
        }

        response = requests.get(
            f"{API_URL}/logs",
            headers=headers
        )

        if response.status_code == 200:

            logs = response.json()["logs"]

            if logs:

                df = pd.DataFrame(
                    logs,
                    columns=[
                        "ID",
                        "Username",
                        "Role",
                        "Query",
                        "Status",
                        "Timestamp"
                    ]
                )

                # =============================
                # 📋 LOG TABLE
                # =============================
                st.subheader("📋 Access Logs")
                st.dataframe(df, use_container_width=True)

                # =============================
                # 📈 ANALYTICS SECTION
                # =============================
                st.subheader("📈 Log Analytics")

                total_queries = len(df)
                denied_count = len(df[df["Status"] == "DENIED"])
                granted_count = len(df[df["Status"] == "GRANTED"])

                col1, col2, col3 = st.columns(3)

                col1.metric("Total Queries", total_queries)
                col2.metric("Granted", granted_count)
                col3.metric("Denied", denied_count)

                # Role-wise Usage
                st.subheader("📊 Role-wise Usage")
                role_counts = df["Role"].value_counts()
                st.bar_chart(role_counts)

                # =============================
                # 🚨 Risk Indicator
                # =============================
                denial_rate = (
                    (denied_count / total_queries) * 100
                    if total_queries > 0 else 0
                )

                if denial_rate > 30:
                    st.error(
                        f"🚨 High Denial Rate Alert: {denial_rate:.2f}%"
                    )
                else:
                    st.success(
                        f"System Healthy ✅ | Denial Rate: {denial_rate:.2f}%"
                    )

            else:
                st.info("No logs available yet.")

        elif response.status_code == 403:
            st.error("Admin access required.")
        else:
            st.error("Unable to fetch logs from server.")
