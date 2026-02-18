import streamlit as st
import requests
import json
from auth import login_ui
from api import send_query, BASE_URL

st.set_page_config(
    page_title="Company Internal AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
    .main-title {
        font-size: 36px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #6c757d;
        margin-bottom: 30px;
    }
    .role-badge {
        padding: 6px 12px;
        border-radius: 20px;
        background-color: #0d6efd;
        color: white;
        font-size: 14px;
        font-weight: 600;
    }
    .confidence-box {
        padding: 10px;
        border-radius: 8px;
        background-color: #639FE2;
        margin-top: 10px;
        color: white;
    }
    .source-card {
        background-color: #996ECB;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# session state
if "token" not in st.session_state:
    st.session_state.token = None

if "username" not in st.session_state:
    st.session_state.username = None

if "role" not in st.session_state:
    st.session_state.role = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown('<div class="main-title">🤖 Company Internal AI Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Secure | Role-Based | AI Powered</div>', unsafe_allow_html=True)

if st.session_state.token is None:
    login_ui()

else:

    with st.sidebar:

        st.markdown("""
        <style>
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1f2235 0%, #242741 100%);
            padding: 25px;
        }

        .user-card {
            background: #2c2f4a;
            padding: 18px;
            border-radius: 12px;
            margin-bottom: 20px;
        }

        .role-pill {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            background-color: #7b61ff;
            color: white;
            font-size: 13px;
            font-weight: 600;
            margin-top: 6px;
        }

        .divider {
            border-top: 1px solid #3a3f63;
            margin: 20px 0;
        }

        .logout-btn button {
            width: 100%;
            background-color: transparent;
            color: #ff4b4b;
            border: 1px solid #ff4b4b;
            border-radius: 8px;
            padding: 8px;
            font-weight: 600;
        }

        .logout-btn button:hover {
            background-color: #ff4b4b;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)

        # 🔹 User Info Card
        st.markdown(f"""
            <div class="user-card">
                <div style="font-size:18px;font-weight:600;">👤 User Info</div>
                <div style="margin-top:10px;"><b>Username:</b> {st.session_state.username}</div>
                <div class="role-pill">{st.session_state.role}</div>
            </div>
        """, unsafe_allow_html=True)

        ROLE_ACCESS = {
            "HR": ["HR", "General"],
            "Finance": ["Finance", "General"],
            "Engineering": ["Engineering", "General"],
            "Marketing": ["Marketing", "General"],
            "C-Level": ["HR", "Finance", "Engineering", "Marketing", "General"],
            "General": ["General"]
        }

        DOCUMENT_ACCESS = {
            "HR": ["HR/hr_data.csv", "general/employee_handbook.md"],
            "Finance": [
                "Finance/financial_summary.md",
                "Finance/quarterly_financial_report.md",
                "general/employee_handbook.md"
            ],
            "Engineering": [
                "engineering/engineering_master_doc.md",
                "general/employee_handbook.md"
            ],
            "Marketing": [
                "marketing/market_report_q4_2024.md",
                "marketing/marketing_report_2024.md",
                "marketing/marketing_report_q1_2024.md",
                "marketing/marketing_report_q2_2024.md",
                "marketing/marketing_report_q3_2024.md",
                "general/employee_handbook.md"
            ],
            "C-Level": [
                "HR/hr_data.csv",
                "Finance/financial_summary.md",
                "Finance/quarterly_financial_report.md",
                "engineering/engineering_master_doc.md",
                "marketing/market_report_q4_2024.md",
                "marketing/marketing_report_2024.md",
                "marketing/marketing_report_q1_2024.md",
                "marketing/marketing_report_q2_2024.md",
                "marketing/marketing_report_q3_2024.md",
                "general/employee_handbook.md"
            ],
            "General": ["general/employee_handbook.md"]
        }

        allowed_depts = ROLE_ACCESS.get(st.session_state.role, [])
        allowed_docs = DOCUMENT_ACCESS.get(st.session_state.role, [])

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("### 📂 Accessible Documents")

        for dept in allowed_depts:
            with st.expander(f"📁 {dept}", expanded=False):
                for doc in allowed_docs:
                    if dept.lower() in doc.lower():
                        st.markdown(f"📄 {doc}")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

       
        st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.username = None
            st.session_state.role = None
            st.session_state.chat_history = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # 💬 Chat Interface (OUTSIDE SIDEBAR)
    st.markdown("### 💬 Chat Interface")

    user_input = st.chat_input("Ask something about company documents...")

    if user_input:
        st.session_state.chat_history.append(("user", user_input))

        response = send_query(user_input, st.session_state.token)

        if response:
            answer = response.get("answer", "")
            sources = response.get("sources", [])
            confidence = response.get("confidence", 0)

            st.session_state.chat_history.append(
                ("assistant", answer, sources, confidence)
            )
        else:
            st.session_state.chat_history.append(
                ("assistant", "Server error occurred.", [], 0)
            )

    for message in st.session_state.chat_history:

        if message[0] == "user":
            with st.chat_message("user"):
                st.markdown(message[1])

        elif message[0] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(message[1])

                if len(message) > 3:
                    st.markdown(
                        f'<div class="confidence-box"><b>Confidence:</b> {message[3]}</div>',
                        unsafe_allow_html=True
                    )

                if len(message) > 2 and message[2]:
                    st.markdown("#### 📂 Sources Used")

                    for src in message[2]:
                        st.markdown(f"""
                        <div class="source-card">
                            <b>File:</b> {src.get("file")} <br>
                            <b>Department:</b> {src.get("department")} <br>
                            <b>Relevance:</b> {src.get("relevance_score")} <br>
                        </div>
                        """, unsafe_allow_html=True)
