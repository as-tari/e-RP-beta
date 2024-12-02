import streamlit as st

def show_dashboard():
    st.title("Admin Dashboard")
    st.write(f"You are logged in as {st.session_state.role}.")
