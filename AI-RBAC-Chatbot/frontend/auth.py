import streamlit as st
from api import login_user


def init_auth_state():
    if "token" not in st.session_state:
        st.session_state.token = None
    if "username" not in st.session_state:
        st.session_state.username = None
    if "role" not in st.session_state:
        st.session_state.role = None


def login_ui():
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = login_user(username, password)

        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data["access_token"]
            st.session_state.username = data["username"]
            st.session_state.role = data["role"]
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")


def logout():
    st.session_state.token = None
    st.session_state.username = None
    st.session_state.role = None
    st.rerun()
