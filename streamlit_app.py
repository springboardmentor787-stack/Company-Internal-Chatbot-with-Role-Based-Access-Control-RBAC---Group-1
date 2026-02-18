import streamlit as st
import requests
import jwt
import time
import os

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Company Internal AI", layout="wide")

# ---------- SESSION ----------
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None
if "role" not in st.session_state:
    st.session_state.role = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# ---------- THEME ----------
def apply_theme():
    if st.session_state.theme == "dark":
        background = "#0e1117"
        text_color = "white"
        sidebar_bg = "#111827"
        card_bg = "#111827"
        input_bg = "#1f2937"
        border_color = "#374151"
    else:
        background = "#f3f4f6"        # soft neutral background
        text_color = "#111827"
        sidebar_bg = "#ffffff"
        card_bg = "#ffffff"
        input_bg = "#ffffff"
        border_color = "#e5e7eb"

    st.markdown(f"""
    <style>

    /* Main App Background */
    .stApp {{
        background-color: {background};
        color: {text_color};
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
        border-right: 1px solid {border_color};
    }}

    /* Chat Container Card Effect */
    .main > div {{
        padding-top: 20px;
    }}

    section[data-testid="stChatMessage"] {{
        background-color: {card_bg};
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }}

    /* Input */
    textarea {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border-radius: 12px !important;
        border: 1px solid {border_color} !important;
        padding: 10px !important;
    }}

    /* Buttons */
    .stButton>button {{
        background: #2563eb;
        color: white;
        border-radius: 10px;
        font-weight: 600;
        border: none;
    }}

    .stButton>button:hover {{
        background: #1d4ed8;
    }}

    /* Confidence badge */
    .confidence-badge {{
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 12px;
        margin-top: 8px;
        display: inline-block;
        font-weight: 600;
    }}

    .high-confidence {{
        background-color: rgba(34,197,94,0.15);
        color: #16a34a;
    }}

    .medium-confidence {{
        background-color: rgba(234,179,8,0.15);
        color: #ca8a04;
    }}

    .low-confidence {{
        background-color: rgba(239,68,68,0.15);
        color: #dc2626;
    }}

    </style>
    """, unsafe_allow_html=True)

apply_theme()

# ---------- LOGIN ----------
def login():
    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.markdown("""
            <div style='
                background-color:#111827;
                padding:40px;
                border-radius:16px;
                box-shadow:0 0 25px rgba(59,130,246,0.2);
            '>
        """, unsafe_allow_html=True)

        st.markdown("## 🚀 Company Internal AI")
        st.markdown("##### Secure Enterprise Assistant")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            response = requests.post(
                f"{BASE_URL}/auth/login",
                json={"username": username, "password": password}
            )

            if response.status_code == 200:
                token = response.json()["access_token"]
                decoded = jwt.decode(token, options={"verify_signature": False})

                st.session_state.token = token
                st.session_state.username = username
                st.session_state.role = decoded.get("role")
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.markdown("</div>", unsafe_allow_html=True)

# ---------- CHAT UI ----------
def chat_ui():

    with st.sidebar:
        st.markdown("## 🏢 Company Portal")
        st.markdown("---")

        

        st.markdown(f"👤 **User:** {st.session_state.username}")
        st.markdown(
            f"<span style='background:#2563eb; padding:4px 10px; border-radius:8px; font-size:12px;'>🔐 {st.session_state.role}</span>",
            unsafe_allow_html=True
        )

        st.markdown("---")
        st.markdown("## 📁 Accessible Files")
        st.markdown("---")

        base_path = "Fintech-data"
        user_role = st.session_state.role

        role_folder_map = {
            "Finance": "Finance",
            "HR": "HR",
            "Engineering": "engineering",
            "Marketing": "marketing",
            "General": "general",
            "C-Level": None
        }

        if user_role == "C-Level":
            accessible_folders = ["Finance", "HR", "engineering", "marketing", "general"]
        else:
            accessible_folders = []
            folder = role_folder_map.get(user_role)
            if folder:
                accessible_folders.append(folder)

        for folder in accessible_folders:
            folder_path = os.path.join(base_path, folder)

            if os.path.exists(folder_path):
                with st.expander(f"📂 {folder.upper()}", expanded=False):
                    files = [
                        f for f in os.listdir(folder_path)
                        if f.endswith((".md", ".csv"))
                    ]

                    if files:
                        for file in files:
                            st.markdown(f"- 📄 {file}")
                    else:
                        st.markdown("_No documents available_")

        st.markdown("---")
        st.markdown("## 🕘 Session History")

        if len(st.session_state.messages) == 0:
            st.caption("No messages yet")
        else:
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.markdown(
                        f"<div style='font-size:12px; opacity:0.7;'>• {msg['content'][:40]}...</div>",
                        unsafe_allow_html=True
                    )

        st.markdown("---")

        if st.button("🧹 Clear Chat"):
            st.session_state.messages = []
            st.rerun()

        if st.button("🚪 Logout"):
            st.session_state.token = None
            st.session_state.username = None
            st.session_state.role = None
            st.session_state.messages = []
            st.rerun()

    st.markdown("## 💬 Company Internal AI Assistant")
    st.caption("Role-Based Secure Knowledge System")
    st.markdown("---")

    # Display messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

            if msg["role"] == "assistant":

                if msg.get("sources"):
                    with st.expander("📚 Sources"):
                        for s in msg["sources"]:
                            st.write(f"- {s}")

                if msg.get("confidence") is not None:
                    conf = msg["confidence"]
                    percentage = int(conf * 100)

                    if conf >= 0.7:
                        label = "High"
                        css_class = "high-confidence"
                    elif conf >= 0.3:
                        label = "Medium"
                        css_class = "medium-confidence"
                    else:
                        label = "Low"
                        css_class = "low-confidence"

                    st.markdown(
                        f"<div class='confidence-badge {css_class}'>🔎 {label} Confidence ({percentage}%)</div>",
                        unsafe_allow_html=True
                    )

                if msg.get("response_time") is not None:
                    st.markdown(
                        f"<div style='font-size:12px; opacity:0.7; margin-top:6px;'>⏱ Response Time: {msg['response_time']} ms</div>",
                        unsafe_allow_html=True
                    )

    prompt = st.chat_input("Ask something securely...")

    if prompt:
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                headers = {
                    "Authorization": f"Bearer {st.session_state.token}"
                }

                start_time = time.time()

                response = requests.post(
                    f"{BASE_URL}/rag",
                    params={"query": prompt},
                    headers=headers
                )

                end_time = time.time()
                response_time = round((end_time - start_time) * 1000, 2)

                if response.status_code == 200:
                    data = response.json()

                    answer = data["answer"]
                    sources = data.get("sources", [])
                    confidence = data.get("confidence", None)

                    st.markdown(answer)

                    if sources:
                        with st.expander("📚 Sources"):
                            for s in sources:
                                st.write(f"- {s}")

                    if confidence is not None:
                        percentage = int(confidence * 100)

                        if confidence >= 0.7:
                            label = "High"
                            css_class = "high-confidence"
                        elif confidence >= 0.3:
                            label = "Medium"
                            css_class = "medium-confidence"
                        else:
                            label = "Low"
                            css_class = "low-confidence"

                        st.markdown(
                            f"<div class='confidence-badge {css_class}'>🔎 {label} Confidence ({percentage}%)</div>",
                            unsafe_allow_html=True
                        )

                    st.markdown(
                        f"<div style='font-size:12px; opacity:0.7; margin-top:6px;'>⏱ Response Time: {response_time} ms</div>",
                        unsafe_allow_html=True
                    )

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                        "confidence": confidence,
                        "response_time": response_time
                    })
                else:
                    st.error("Error getting response")

# ---------- MAIN ----------
if st.session_state.token is None:
    login()
else:
    chat_ui()
