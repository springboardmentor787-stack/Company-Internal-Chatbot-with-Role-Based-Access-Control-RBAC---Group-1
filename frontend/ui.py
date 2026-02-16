import streamlit as st

def set_page_style():
    """Sets global page configuration and custom CSS."""
    st.markdown("""
        <style>
            .stStatusWidget { visibility: hidden; }
            .main { background-color: #f5f7f9; }
            .stChatItem { border-radius: 15px; }
        </style>
    """, unsafe_allow_html=True)

def render_sidebar_profile(user_data):
    """Displays a consistent user profile card in the sidebar."""
    with st.sidebar:
        st.markdown(f"### 👤 {user_data['name']}")
        st.caption(f"**Role:** {user_data['role']}")
        st.caption(f"**Department:** {user_data['dept']}")
        st.divider()
        
        # Guide based on User Role
        if user_data['role'] == "Admin":
            st.success("🛠️ **Admin Access Active**\nYou can view system logs.")
        elif user_data['role'] == "Analyst":
            st.info("📊 **Analyst Access Active**\nFocus on data cross-referencing.")
        
        st.divider()

def display_source_expander(sources, citations):
    """Renders a clean expander for document citations and sources."""
    if sources:
        with st.expander("📚 View Supporting Documents"):
            for src in sources:
                st.write(f"• {src}")
            if citations:
                st.divider()
                st.caption(f"**Reference:** {citations}")

def show_error_message(message):
    """Standardized error display for the app."""
    st.toast(message, icon="⚠️")