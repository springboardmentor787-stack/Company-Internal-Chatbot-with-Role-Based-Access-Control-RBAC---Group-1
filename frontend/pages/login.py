import streamlit as st
import requests

API_URL = "http://localhost:8000/login"

st.title("Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):

    if not username or not password:
        st.error("Enter username and password")
    else:
        resp = requests.post(
            API_URL,
            data={
                "username": username,
                "password": password
            }
        )

        if resp.status_code == 200:
            data = resp.json()

            st.session_state["token"] = data["access_token"]
            st.session_state["username"] = username

            st.success("Login successful")
            st.info("Go to Chat page from left menu")

        else:
            st.error("Invalid credentials")
