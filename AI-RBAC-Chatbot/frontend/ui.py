import streamlit as st
from api import send_query
from auth import logout


def sidebar_ui():
    with st.sidebar:
        st.markdown("## 👤 User Info")
        st.write(f"**Username:** {st.session_state.username}")
        st.write(f"**Role:** {st.session_state.role}")

        if st.button("Logout"):
            logout()


def chat_ui():
    st.subheader("💬 Secure Company Chat")

    query = st.text_input("Ask your question")

    if st.button("Send"):
        if not query.strip():
            st.warning("Please enter a question")
            return

        with st.spinner("Thinking..."):
            response = chat_with_backend(
                st.session_state.token,
                query
            )

        if response.status_code != 200:
            st.error("Backend error")
            return

        result = response.json()

        st.markdown("### 🤖 Answer")
        st.write(result["answer"] or "No answer generated")

        st.markdown("### 📚 Sources")
        for src in result["sources"]:
            with st.expander(
                f"{src['file']} | {src['department']} | score {src['relevance_score']}"
            ):
                st.write(f"Chunk ID: {src['chunk_id']}")

        st.markdown(
            f"### 📊 Confidence Score: `{result['confidence']}`"
        )
