import streamlit as st

def show_dashboard():
    st.title("{st.session_state.role} Dashboard")
    st.write(f"You are logged in as {st.session_state.role}.")
