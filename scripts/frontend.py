# frontend.py (Streamlit app)

import streamlit as st
import requests

API_URL = "http://localhost:8000"  # adjust if running backend elsewhere

st.set_page_config(page_title="Chatbot Client", layout="wide")
st.title("🔐 Secure Chatbot Demo")

# Initialize session state for token and user info
if 'token' not in st.session_state:
    st.session_state['token'] = None
if 'user' not in st.session_state:
    st.session_state['user'] = None
def logout():
    """Clears session state and resets the app to login."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

# Sidebar for user info and logout
if st.session_state.get('user'):
    st.sidebar.markdown(f"**Logged in as:** {st.session_state['user']['full_name']} ({st.session_state['user']['role']})")
    if st.sidebar.button("Logout"):
        logout()
else:
    st.sidebar.text("Not logged in.")
if not st.session_state['token']:
    st.subheader("Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            try:
                res = requests.post(f"{API_URL}/login", data={"username": username, "password": password})
                if res.status_code == 200:
                    data = res.json()
                    st.session_state['token'] = data["access_token"]
                    # Fetch current user info from backend
                    me_res = requests.get(f"{API_URL}/me", headers={"Authorization": f"Bearer {st.session_state['token']}"})
                    if me_res.status_code == 200:
                        st.session_state['user'] = me_res.json()
                        st.success("Logged in successfully!")
                        st.experimental_rerun()
                    else:
                        st.error("Failed to fetch user info.")
                        logout()
                elif res.status_code == 401:
                    st.error("Login failed: incorrect credentials.")
                else:
                    st.error(f"Login failed (status {res.status_code}).")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {e}")
else:
    st.subheader("Chat with SecureBot")
    query = st.text_input("Enter your query:")
    if st.button("Send Query"):
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        try:
            res = requests.post(f"{API_URL}/chat", json={"query": query}, headers=headers)
            if res.status_code == 200:
                answer = res.json().get("response", "")
                st.write(f"**Bot:** {answer}")
            elif res.status_code == 401:
                st.error("Session expired or invalid. Please log in again.")
                logout()
            elif res.status_code == 403:
                st.error("Permission denied for this action.")
            elif res.status_code == 422:
                st.error("Invalid input (422). Please check your query.")
            else:
                st.error(f"Error {res.status_code}: {res.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to server: {e}")
else:
    st.subheader("Chat with SecureBot")
    query = st.text_input("Enter your query:")
    if st.button("Send Query"):
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        try:
            res = requests.post(f"{API_URL}/chat", json={"query": query}, headers=headers)
            if res.status_code == 200:
                answer = res.json().get("response", "")
                st.write(f"**Bot:** {answer}")
            elif res.status_code == 401:
                st.error("Session expired or invalid. Please log in again.")
                logout()
            elif res.status_code == 403:
                st.error("Permission denied for this action.")
            elif res.status_code == 422:
                st.error("Invalid input (422). Please check your query.")
            else:
                st.error(f"Error {res.status_code}: {res.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to server: {e}")
# Show conversation (optional: could append to history)
if st.session_state.get('token'):
    st.sidebar.title("User Info")
    if st.session_state['user']:
        user = st.session_state['user']
        st.sidebar.write(f"**Username:** {user['username']}")
        st.sidebar.write(f"**Role:** {user['role']}")
        st.sidebar.write(f"**Full Name:** {user['full_name']}")
