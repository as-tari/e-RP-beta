import streamlit as st
import random
import string
import os
from dotenv import load_dotenv

# Memuat variabel lingkungan dari file .env
load_dotenv()
allowed_emails = os.getenv("ALLOWED_EMAILS").split(",")

# Fungsi untuk menghasilkan token acak
def generate_token(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Inisialisasi session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "token" not in st.session_state:
    st.session_state.token = None

# Fungsi utama untuk login
def login():
    st.header("Log in")

    # Input alamat email
    email_input = st.text_input("Enter your email")

    if st.button("Request Token"):
        if email_input in allowed_emails:
            # Generate token
            st.session_state.token = generate_token()
            subject = "Your Authentication Token"
            body = f"Your token is: {st.session_state.token}"
            mailto_link = f"mailto:{email_input}?subject={subject}&body={body}"
            st.markdown(f"[Click here to send your token]({mailto_link})")
            st.success("Token has been sent to your email. Please check your inbox.")
        else:
            st.error("Unauthorized email address. Please use an allowed email.")

    # Input token
    if st.session_state.token:
        token_input = st.text_input("Enter your token")

        if st.button("Log in"):
            if token_input == st.session_state.token:
                st.success("Logged in successfully!")
                st.session_state.logged_in = True
                st.session_state.token = None  # Reset token setelah login
                st.experimental_rerun()  # Refresh halaman
            else:
                st.error("Invalid token.")

# Menjalankan fungsi login
if not st.session_state.logged_in:
    login()
else:
    st.write("Welcome to the application!")
