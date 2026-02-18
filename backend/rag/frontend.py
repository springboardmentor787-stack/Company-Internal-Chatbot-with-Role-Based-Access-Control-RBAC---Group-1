import streamlit as st
import requests

# -------------------------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------------------------
API_BASE_URL = "https://my-chatbot-backend.onrender.com"

st.set_page_config(
    page_title="AI Corporate Chatbot",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------------------------------------------------
if "token" not in st.session_state:
    st.session_state["token"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None
if "user" not in st.session_state:
    st.session_state["user"] = None
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# -------------------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------------------
def login(username, password):
    try:
        response = requests.post(
            f"{API_BASE_URL}/login",
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state["token"] = data["access_token"]
            st.session_state["role"] = data["role"]
            st.session_state["user"] = username
            st.success(f"Logged in as {username} ({data['role']})")
            st.rerun()
        else:
            st.error("Invalid Username or Password")
    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to Backend. Is 'main.py' running?")

def get_accessible_files():
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    try:
        response = requests.get(f"{API_BASE_URL}/files", headers=headers)
        if response.status_code == 200:
            return response.json().get("files", {})
        return {}
    except:
        return {}

def get_chatbot_response(question, department):
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    
    # --- NEW: SEND CHAT HISTORY FOR CONTEXT ---
    # We take the last 4 messages to save space but provide context
    simple_history = [
        {"role": m["role"], "content": m["content"]} 
        for m in st.session_state["messages"][-4:] 
    ]
    
    payload = {
        "question": question, 
        "department": department,
        "history": simple_history  # <--- Sending history to backend
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            return {"answer": "🚫 Access Denied: You do not have permission to view this department.", "sources": []}
        else:
            return {"answer": f"⚠️ Error: {response.text}", "sources": []}
    except Exception as e:
        return {"answer": f"Connection Error: {str(e)}", "sources": []}

def get_confidence_style(score):
    """Returns colors based on confidence score."""
    if score > 70:
        return "#d4edda", "#155724"  # Light Green Background, Dark Green Text
    elif score > 40:
        return "#fff3cd", "#856404"  # Light Yellow Background, Dark Yellow Text
    else:
        return "#f8d7da", "#721c24"  # Light Red Background, Dark Red Text

# -------------------------------------------------------------------------
# LOGIN SCREEN
# -------------------------------------------------------------------------
if st.session_state["token"] is None:
    # We use 3 columns: Left(spacer), Middle(content), Right(spacer)
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("🔒 Corporate Secure Login")
        st.markdown("Please sign in to access company documents.")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            login(username, password)

# -------------------------------------------------------------------------
# MAIN APP
# -------------------------------------------------------------------------
else:
    # --- SIDEBAR ---
    with st.sidebar:
        st.title(f"👤 {st.session_state['user'].upper()}")
        st.caption(f"Role: **{st.session_state['role'].upper()}**")
        
        # --- Side-by-Side Action Buttons ---
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🧹 Clear", use_container_width=True):
                st.session_state["messages"] = []
                st.rerun()
                
        with col2:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state["token"] = None
                st.session_state["messages"] = []
                st.rerun()
            
        st.divider()
        st.subheader("📂 Accessible Files")
        
        # --- FILE LISTING ---
        files_map = get_accessible_files()
        if files_map:
            for dept, files in files_map.items():
                # Force expander to show even if empty, but show (Empty) text inside
                with st.expander(f"📁 {dept.upper()}", expanded=False):
                    if files:
                        for f in files:
                            st.markdown(f"- 📄 `{f}`")
                    else:
                        st.caption("*(Empty Folder)*")
        else:
            st.caption("⚠️ Could not load file list.")

    # --- CHAT AREA ---
    st.title("🤖 Enterprise RAG Chatbot")
    
    dept_options = ["hr", "finance", "marketing", "engineering", "general"]
    selected_dept = st.selectbox("Select Target Department:", dept_options)

    # Display History
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
            if msg.get("is_assistant"):
                score = msg.get("confidence", 0)
                bg_color, text_color = get_confidence_style(score)
                
                # Confidence Box
                st.markdown(f"""
                <div style="
                    padding: 10px; 
                    border-radius: 8px; 
                    background-color: {bg_color}; 
                    color: {text_color}; 
                    border: 1px solid {text_color};
                    margin-top: 10px;
                    margin-bottom: 10px;">
                    <strong>📊 Confidence Score:</strong> {score}%
                </div>
                """, unsafe_allow_html=True)

                if msg.get("sources"):
                    with st.expander("📚 View Source Documents"):
                        for src in msg["sources"]:
                             st.markdown(f"- `{src['file_name']}` ({src['department']}) - **{src['confidence']}% Match**")

    # --- INPUT ---
    if prompt := st.chat_input("Ask a question about company documents..."):
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Thinking..."):
            api_res = get_chatbot_response(prompt, selected_dept)
            answer = api_res.get("answer", "No answer generated.")
            sources = api_res.get("sources", [])
            
            avg_confidence = 0
            if sources:
                avg_confidence = int(sum(s['confidence'] for s in sources) / len(sources))

        with st.chat_message("assistant"):
            st.markdown(answer)
            
            bg_color, text_color = get_confidence_style(avg_confidence)
            
            st.markdown(f"""
            <div style="
                padding: 10px; 
                border-radius: 8px; 
                background-color: {bg_color}; 
                color: {text_color}; 
                border: 1px solid {text_color};
                margin-top: 10px;
                margin-bottom: 10px;">
                <strong>📊 Confidence Score:</strong> {avg_confidence}%
            </div>
            """, unsafe_allow_html=True)
            
            if sources:
                with st.expander("📚 View Source Documents"):
                    for src in sources:
                        st.markdown(f"- `{src['file_name']}` ({src['department']}) - **{src['confidence']}% Match**")

        st.session_state["messages"].append({
            "role": "assistant", 
            "content": answer, 
            "is_assistant": True,
            "confidence": avg_confidence,
            "sources": sources
        })