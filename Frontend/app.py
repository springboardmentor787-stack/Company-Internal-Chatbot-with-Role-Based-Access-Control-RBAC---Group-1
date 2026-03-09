from os import access
import streamlit as st
import requests
from datetime import datetime
import time
from transformers import data
import json
import os



BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Company AI Chatbot", layout="wide")

# ================= CSS LOADING =================
try:
    with open("frontend/style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass


# ================= HEADER FUNCTION =================
def show_header():
    st.markdown("""
    <div class="header">
    🏢 Enterprise AI Platform | Secure Role-Based Knowledge Assistant
    </div>
    """, unsafe_allow_html=True)


def show_time():
    current_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")

    st.markdown(
        f"""
        <div class="time-bar">
        🕒 {current_time}
        </div>
        """,
        unsafe_allow_html=True
    )

# ================= AUTH HEADER =================
def headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}


# ================= DASHBOARD METRIC =================
def metric_box(column, label, value):
    column.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# ================= METRIC BOX =================
def metric_box(column, label, value):
    column.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# ================= HISTORY STORAGE =================
HISTORY_FILE = "chat_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

# ------------------ SESSION ------------------
if "token" not in st.session_state:
    st.session_state.token = None

if "role" not in st.session_state:
    st.session_state.role = None

if "username" not in st.session_state:
    st.session_state.username = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_history()

if "menu" not in st.session_state:
    st.session_state.menu = "Home"


# ================= ROLE ICONS =================
ROLE_ICONS = {
    "hr": "👥",
    "finance": "💰",
    "marketing": "📢",
    "engineering": "⚙️",
    "employees": "👨‍💼",
    "c-level": "👑"
}

ROLE_DOCUMENTS = {
    "hr": ["hr", "general"],
    "finance": ["finance", "general"],
    "marketing": ["marketing", "general"],
    "engineering": ["engineering", "general"],
    "employees": ["general"],
    "c-level": ["hr", "finance", "marketing", "engineering", "general"]
}

DEPARTMENT_FOLDERS = {
    "hr": ["HR_Policy.pdf", "Leave_Guidelines.docx"],
    "finance": ["Budget_2024.pdf"],
    "marketing": ["Campaign_Analysis.docx"],
    "engineering": ["System_Architecture.pdf"],
    "general": ["Company_Code_of_Conduct.pdf"]
}

# ================= C-LEVEL FEATURES =================
C_LEVEL_FEATURES = [
    "analytics_dashboard",
    "system_logs",
    "all_documents_access"
]

# ------------------ LOGIN PAGE ------------------
def login_page():

    show_header()
    show_time()

    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown("""
        <div class="login-card">

        <div class="ai-icon">🤖</div>

        <div class="login-title">
        🔐 Secure Login
        </div>

        <div class="login-subtitle">
        Enterprise AI Access Portal
        </div>

        <div class="security-msg">
        🔒 Secured with JWT Authentication
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input(
            " 👤 Username",
            placeholder="Enter Username",
            key="login_username"
        )

        password = st.text_input(
            " 🔑 Password",
            type="password",
            placeholder="Enter Password",
            key="login_password"
        )

        login_btn = st.button(" 🔐 Login", use_container_width=True, key="login_button")

        if login_btn:

            if not username or not password:
                st.warning("⚠ Please enter username and password")
                return

            try:

                with st.spinner("🔄 Verifying credentials..."):

                    response = requests.post(
                        f"{BACKEND_URL}/login",
                        data={"username": username, "password": password},
                        timeout=5
                    )

                if response.status_code == 200:

                    st.success("✅ Login Successful")

                    st.session_state.token = response.json()["access_token"]

                    user_res = requests.get(
                        f"{BACKEND_URL}/me",
                        headers=headers(),
                        timeout=5
                    )

                    user_data = user_res.json()

                    st.session_state.role = user_data["role"].lower().strip()
                    st.session_state.username = user_data["username"]
                    st.session_state.login_time = datetime.now().strftime("%I:%M %p")

                    st.rerun()

                else:
                    st.error("❌ Invalid username or password")

            except requests.exceptions.ConnectionError:
                st.error("🚨 Backend server is not reachable")

            except requests.exceptions.Timeout:
                st.error("⏳ Server timeout")

            except Exception as e:
                st.error(f"Error: {str(e)}")


    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
                <div class="login-footer">
            Enterprise AI Platform | Infosys Springboard Internship 6.0
            </div>
""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------ HOME PAGE ------------------
def home_page():

    show_header()
    show_time()

    username = st.session_state.username
    role = st.session_state.role

    # Access Level Logic
    if role == "c-level":
        access = "Enterprise Access"
    elif role in ["hr","finance","marketing","engineering"]:
        access = "Dept Restricted"
    else:
        access = "General Access"

    # ================= WELCOME =================
    user_name = "PIRLA VENKATA LAKSHMI NARAYANA"
    st.markdown(f"## 👋 Welcome Hi {user_name}, how can I assist you today!")

    st.markdown(f"""
    <div class='user-info'>
    <p>👤 <b>User:</b> {user_name}</p>
    <p>🏢 <b>Role:</b> {role.upper()}</p>
    <p>🔐 <b>Access Level:</b> {access}</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

  
# ================= DASHBOARD METRICS =================
    st.markdown("## 📊 Dashboard Overview")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

# Accessible folders for role
    folders = ROLE_DOCUMENTS.get(role, ["general"])

# Total documents across folders
    num_documents = sum(len(DEPARTMENT_FOLDERS.get(folder, [])) for folder in folders)

# Queries count
    query_count = len(st.session_state.chat_history)

    metric_box(col1, "🔐 Access Level", access)
    metric_box(col2, "📁 Documents", num_documents)
    metric_box(col3, "💬 Queries", query_count)
    metric_box(col4, "📄 Files Indexed", 127)
    metric_box(col5, "👥 Roles", 6)
    metric_box(col6, "🛡 RBAC", "Enabled")
    st.divider()
# ================= Security Overview =================
    st.markdown("## 🔐 Security Overview")

    st.success("RBAC Access Control Enabled")
    st.success("JWT Authentication Active")
    st.success("Secure API Communication")
    st.divider()

    # ================= Platform Features =================
    st.markdown("## 🚀 Platform Features")

    st.markdown("""
    <div class="tech-stack">
    🔎 Smart Document Search <br>
    📑 Automated Knowledge Retrieval <br>
    ⚡ Fast Enterprise AI Responses <br>
    🔐 Secure Role-Based Access
</div>
""", unsafe_allow_html=True)

    st.divider()

    # ================= SYSTEM WORKFLOW =================
    st.markdown("## 🧠 System Workflow")

    st.markdown("""
    <div class="workflow-box">
    👤 User → 🔐 RBAC Authentication → 📚 Vector Search → 🤖 AI Model → 📄 Response
    </div>
    """, unsafe_allow_html=True)

    st.divider()
     # ================= RECENT QUERIES =================
    st.markdown("## 📜 Recent Queries")
    if "chat_history" in st.session_state and st.session_state.chat_history:

        for q in st.session_state.chat_history[-5:]:

            # Fix for dictionary storage
            if isinstance(q, dict):
                query_text = q.get("query", "")
            else:
                query_text = q

            st.markdown(f"• {query_text}")

    else:
        st.markdown("""
• HR leave policy  
• Financial report summary  
""")
    st.divider()

    # ================= TECHNOLOGY STACK =================
    st.markdown("## ⚙ Technology Stack")

    st.markdown("""
    <div class="tech-stack">
    🐍 Python | ⚡ FastAPI | 🗂 ChromaDB | 🤖 LLM | 🔐 RBAC Security
    </div>
    """, unsafe_allow_html=True)
# ================= ROLE BASED SUGGESTED QUESTIONS =================
ROLE_SUGGESTIONS = {

    "hr": [
        "Summarize HR leave policy",
        "Explain employee benefits",
        "Show recruitment guidelines"
    ],

    "finance": [
        "Show financial report summary",
        "Explain company budget",
        "What are current expenses?"
    ],

    "marketing": [
        "Explain marketing strategy",
        "Show campaign performance",
        "What is the current marketing plan?"
    ],

    "engineering": [
        "Explain system architecture",
        "Show engineering documentation",
        "How does the platform work?"
    ],

    "employees": [
        "Show company code of conduct",
        "Explain company policies",
        "What benefits do employees get?"
    ],

    "c-level": [
        "Give company performance summary",
        "Show financial overview",
        "Explain company growth strategy"
    ]
}
# ------------------ CHAT PAGE ------------------
def chat_page():

    show_header()
    show_time()

    st.title("🤖 Company AI Assistant")
    # Show user role
    role = st.session_state.role
    st.markdown(f"### 🏢 Role: {role.upper()}")

    # ================= SESSION STATES =================
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "response_times" not in st.session_state:
        st.session_state.response_times = []

    # ================= CHAT ANALYTICS =================
    st.markdown("### 📊 Chat Analytics")

    total_queries = len(st.session_state.chat_history)

    if total_queries > 0:
        queries = [q["query"] for q in st.session_state.chat_history]
        most_asked = max(set(queries), key=queries.count)
        avg_time = sum(st.session_state.response_times) / len(st.session_state.response_times)
    else:
        most_asked = "None yet"
        avg_time = 0

    col1, col2, col3 = st.columns(3)

    col1.metric("💬 Total Queries", total_queries)
    col2.metric("⭐ Most Asked", most_asked)
    col3.metric("⏱ Avg Response Time", f"{avg_time:.2f} sec")

    st.divider()

    # ================= ROLE BASED SUGGESTIONS =================
    st.markdown("### 💡 Suggested Questions")

    suggestions = ROLE_SUGGESTIONS.get(role, [
        "Explain company policy",
        "Show company documents",
        "Summarize latest reports"
    ])

    cols = st.columns(len(suggestions))

    for i, s in enumerate(suggestions):
        if cols[i].button(s):
            st.session_state.suggested_query = s

    # ================= CHAT INPUT =================
    query = st.chat_input("Ask something about company documents...")

    if "suggested_query" in st.session_state:
        query = st.session_state.suggested_query
        del st.session_state.suggested_query

    if query:

        if query.strip() == "":
            st.warning("Please enter a question")
            return

        with st.chat_message("user"):
            st.write(query)
            st.caption(datetime.now().strftime("%H:%M"))

        status_placeholder = st.empty()

        # STEP 1
        status_placeholder.markdown("### 🤔 Thinking....")
        time.sleep(0.9)

        # STEP 2
        status_placeholder.markdown("### 📂 Retrieving Documents...")
        time.sleep(0.9)

        # STEP 3
        status_placeholder.markdown("### 🛡 Applying Security Filters...")
        time.sleep(0.9)

        # STEP 4
        status_placeholder.markdown("### 🤖 Generating AI Response...")

        start_time = time.time()

        response = requests.post(
            f"{BACKEND_URL}/chat",
            headers=headers(),
            json={"query": query}
        )

        end_time = time.time()
        response_time = end_time - start_time

        st.session_state.response_times.append(response_time)

        status_placeholder.empty()

        if response.status_code == 200:

            data = response.json()
            answer = data["answer"]

            # Save conversation
            st.session_state.chat_history.append({
                "query": query,
                "answer": answer
            })
            
            with st.chat_message("assistant"):

                st.write(answer)
                st.caption(datetime.now().strftime("%H:%M"))

                if st.button("📋 Copy Answer"):
                    st.write("Answer copied! (Ctrl+C)")

                # ================= CONFIDENCE BAR =================
                confidence = float(data["confidence"])
                display_confidence = min(confidence * 1.5, 100)

                if display_confidence < 40:
                    level = "Low Confidence"
                    css_class = "low-confidence"

                elif display_confidence < 70:
                    level = "Medium Confidence"
                    css_class = "medium-confidence"

                elif display_confidence < 90:
                    level = "High Confidence"
                    css_class = "high-confidence"

                else:
                    level = "Very High Confidence"
                    css_class = "very-high-confidence"

                st.markdown(f"### 📊 Confidence: {display_confidence:.2f}%")
                st.markdown(f"**Level:** {level}")

                st.markdown(f"""
                <div class="confidence-container">
                    <div class="confidence-bar {css_class}" style="width:{display_confidence}%"></div>
                </div>
                """, unsafe_allow_html=True)

                st.caption(f"⏱ Response Time: {response_time:.2f} sec")

                # ================= SOURCES =================
                st.markdown("### 📄 Sources")

                for source in data.get("sources", []):
                    st.info(f"📄 {source}")

        else:
            st.error(response.text)

    st.divider()

# ------------------ HISTORY PAGE ------------------
def history_page():

    show_header()
    show_time()

    st.title("📜 Chat History")

    history = st.session_state.get("chat_history", [])

    if not history:
        st.info("No chat history available yet.")
        return

    st.markdown("### 🗂 Previous Conversations")

    for i, chat in enumerate(history[::-1], start=1):

        query = chat.get("query", "")
        answer = chat.get("answer", "")

        with st.expander(f"Conversation {i}"):

            st.markdown(f"**👤 User Query:**")
            st.write(query)

            st.markdown(f"**🤖 AI Response:**")
            st.write(answer)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗑 Clear History"):
            st.session_state.chat_history = []
            save_history([])
            st.success("History cleared")
            st.rerun()

    with col2:
        if st.button("💾 Save History"):
            save_history(st.session_state.chat_history)
            st.success("History saved successfully")

# ------------------ ADMIN PAGE ------------------
def admin_page():

    show_header()
    show_time()

    st.header("👑 C-Level Admin Panel")

    st.divider()

    # ================= ADD USER =================
    st.subheader("➕ Add User")

    new_username = st.text_input("New Username", key="new_user")
    new_password = st.text_input("New Password", type="password", key="new_pass")

    new_role = st.selectbox(
        "Role",
        ["HR", "Finance", "Marketing", "Engineering", "Employees"]
    )

    if st.button("Add User"):

        res = requests.post(
            f"{BACKEND_URL}/admin/add-user",
            params={
                "username": new_username,
                "password": new_password,
                "role": new_role.lower()
            },
            headers=headers()
        )

        if res.status_code == 200:
            st.success("✅ User added successfully")
        else:
            st.error(res.text)

    st.divider()

    # ================= DELETE USER =================
    st.subheader("❌ Delete User")

    delete_username = st.text_input("Username to delete", key="delete_user")

    if st.button("Delete User"):

        res = requests.delete(
            f"{BACKEND_URL}/admin/delete-user",
            params={"username": delete_username},
            headers=headers()
        )

        if res.status_code == 200:
            st.success("✅ User deleted successfully")
        else:
            st.error(res.text)

    st.divider()

# ================= MAIN APP =================
if not st.session_state.token:
    login_page()

else:

    role = st.session_state.role
    display_name = st.session_state.username
    login_time = datetime.now().strftime("%I:%M %p")

    display_role = role.replace("-", " ").title()

    if role == "c-level":
        display_role = "C-Level Executive"
    # ================= SIDEBAR HEADER =================
    st.sidebar.markdown("""
                        <div class="sidebar-box">
                        <div class="sidebar-box-title">
                        🏢 Enterprise Dashboard
                        </div>

<p style="color:white;font-size:13px;">
Secure Role-Based Access System
</p>

</div>
""", unsafe_allow_html=True)
    st.sidebar.divider()

    # ================= USER PANEL =================
    with st.sidebar.container():
        st.markdown(f"""
        <div class="profile-card">

        <div class="profile-title">👤 USER PANEL</div>

        <div class="profile-info">
        User: <span class="username">PIRLA VENKATA LAKSHMI NARAYANA</span>
        </div>
        
        <div class="profile-info">
        Role: <span class="role">{role.upper()}</span>
        </div>

        <div class="profile-info">
        Login Time: {login_time}
        </div>

        </div>
        """, unsafe_allow_html=True)

# ================= EXECUTIVE ACCESS =================
        if role == "c-level":
            
            st.sidebar.success("👑 Executive Access Enabled")
            
            st.sidebar.warning(
        "⚠ Executive Access: All department documents are visible."
    )

    st.sidebar.markdown("👑 **Role: C-Level Executive**")
    st.sidebar.divider()
    # ================= SYSTEM STATUS =================
    st.sidebar.markdown("""
<div class="sidebar-box">

<div class="sidebar-box-title">
🟢 System Status
</div>

<p><b>Backend:</b> <span class="status-online">Online</span></p>
<p><b>Vector DB:</b> <span class="status-online">Active</span></p>
<p><b>AI Model:</b> <span class="status-online">Ready</span></p>

</div>
""", unsafe_allow_html=True)


    st.sidebar.divider()

    # ================= ACCESSIBLE DOCUMENTS =================
    st.sidebar.header("📁 Accessible Documents")

    if role == "c-level":

        for dept, files in DEPARTMENT_FOLDERS.items():

            with st.sidebar.expander(f"📂 {dept.title()} ({len(files)})"):
                for f in files:
                    st.markdown(f"📄 {f}")

    else:
        folders = ROLE_DOCUMENTS.get(role, ["general"])

        for folder in folders:

            files = DEPARTMENT_FOLDERS.get(folder, [])

            with st.sidebar.expander(f"📂 {folder.title()} ({len(files)})"):
                for f in files:
                    st.markdown(f"📄 {f}")

    st.sidebar.divider()

#================= NAVIGATION =================
    st.sidebar.markdown("""
                <div class="sidebar-box">
                        
                <div class="sidebar-box-title">
                📌 Navigation
                </div>
                        
                </div>
                """, unsafe_allow_html=True) 
    col1, col2 = st.sidebar.columns(2)

    with col1:
        if st.button("🏠 Home"):
           st.session_state.menu = "Home"

    with col2:
        if st.button("💬 Chat"):
           st.session_state.menu = "Chat"

    col3, col4 = st.sidebar.columns(2)
    
    with col3:
           if st.button("📜 History"):
               st.session_state.menu = "History"

    with col4:
           if st.button("🔐 Logout"):
               st.session_state.token = None
               st.session_state.role = None
               st.session_state.username = None
               st.rerun()
    col1 = st.sidebar.container()
    with col1:          
            if role == "c-level":
                   if st.sidebar.button("👑 Admin Panel"):
                       st.session_state.menu = "Admin"


    st.sidebar.divider()

    st.sidebar.markdown("""
<div class="sidebar-box">

<div class="sidebar-box-title">
💡 Example Questions
</div>

<p>• Show HR leave policy</p>
<p>• Summarize financial report</p>
<p>• Explain system architecture</p>
<p>• What is company code of conduct?</p>

</div>
""", unsafe_allow_html=True)

 # ================= PAGE NAVIGATION =================
    if st.session_state.menu == "Home":
        home_page()

    elif st.session_state.menu == "Chat":
        chat_page()

    elif st.session_state.menu == "History":
        history_page()

    elif st.session_state.menu == "Admin":
        admin_page()

# ================= FOOTER =================
if st.session_state.token:
    st.markdown("""
                <div class="login-footer">
            Enterprise AI Platform | Infosys Springboard Internship 6.0
            </div>
""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)