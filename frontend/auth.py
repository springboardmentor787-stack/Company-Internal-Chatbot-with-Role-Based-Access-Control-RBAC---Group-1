import streamlit as st
from frontend.api_client import login_user

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def login_screen():
    st.title("🔐 Company Internal Chatbot")
    with st.container(border=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            res = login_user(username, password)
            if res and res.status_code == 200:
                data = res.json()
                st.session_state.logged_in = True
                st.session_state.token = data.get("access_token")
                st.session_state.user = data.get("user") # Contains name, role, dept
                st.rerun()
            else:
                st.error("Invalid credentials or server unreachable.")