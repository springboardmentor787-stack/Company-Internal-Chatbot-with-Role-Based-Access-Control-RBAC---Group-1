import streamlit as st
import requests
import jwt
import time

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Company Internal AI", layout="wide")

# ---------- CLEAN CSS ----------
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #0e1117;
    color: white;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Chat spacing */
[data-testid="stChatMessage"] {
    padding-top: 8px;
    padding-bottom: 8px;
}

/* Confidence badge */
.confidence-badge {
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 12px;
    margin-top: 8px;
    display: inline-block;
    font-weight: 600;
}

.high-confidence {
    background-color: rgba(34,197,94,0.2);
    color: #22c55e;
}

.medium-confidence {
    background-color: rgba(234,179,8,0.2);
    color: #eab308;
}

.low-confidence {
    background-color: rgba(239,68,68,0.2);
    color: #ef4444;
}

/* Input */
textarea {
    background-color: #1f2937 !important;
    color: white !important;
    border-radius: 10px !important;
    border: 1px solid #374151 !important;
}

/* Buttons */
.stButton>button {
    background: #2563eb;
    color: white;
    border-radius: 8px;
    font-weight: 600;
}

.stButton>button:hover {
    background: #1d4ed8;
}

</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None
if "role" not in st.session_state:
    st.session_state.role = None
if "messages" not in st.session_state:
    st.session_state.messages = []

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

    # Sidebar
    with st.sidebar:
        st.markdown("## 🏢 Company Portal")
        st.markdown("---")
        st.markdown(f"👤 **User:** {st.session_state.username}")
        st.markdown(f"🔐 **Role:** `{st.session_state.role}`")
        st.markdown("---")

        if st.button("🧹 Clear Chat"):
            st.session_state.messages = []

        if st.button("🚪 Logout"):
            st.session_state.clear()
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
                        f"<div class='confidence-badge {css_class}'>🔎 {label} Confidence ({conf})</div>",
                        unsafe_allow_html=True
                    )

                if msg.get("response_time") is not None:
                    st.markdown(
                        f"<div style='font-size:12px; opacity:0.7; margin-top:6px;'>⏱ Response Time: {msg['response_time']} ms</div>",
                        unsafe_allow_html=True
                    )

    # Chat input
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
                            f"<div class='confidence-badge {css_class}'>🔎 {label} Confidence ({confidence})</div>",
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
