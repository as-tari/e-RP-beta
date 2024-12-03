import streamlit as st
import random
import string
import base64
import os
from dotenv import load_dotenv

# Muat variabel lingkungan dari file .env
load_dotenv()
ALLOWED_EMAILS = os.getenv("ALLOWED_EMAILS").split(",")

# Fungsi untuk menghasilkan token acak
def generate_token(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Fungsi untuk meng-encode token ke Base64
def encode_token(token):
    return base64.b64encode(token.encode()).decode()

# Inisialisasi session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "token" not in st.session_state:
    st.session_state.token = None

# Fungsi utama untuk login
def login():
    st.header("Log in")

    # Input alamat email
    email_input = st.text_input("Enter your email to log in")

    if st.button("Request Token"):
        if email_input in ALLOWED_EMAILS:
            # Generate token
            token = generate_token()
            st.session_state.token = token

            # Encode token in Base64
            encoded_token = encode_token(token)

            # Generate unique URL with the encoded token
            token_link = f"https://your-app.com/retrieve-token?token={encoded_token}"

            # Email body with the link
            subject = "Your Authentication Token"
            body = f"Click the link below to retrieve your token:\n\n{token_link}"

            # Send email using the 'mailto' link
            mailto_link = f"mailto:{email_input}?subject={subject}&body={body}"
            st.markdown(f"""<div style="background-color:#d4edda;padding:10px;border-radius:5px;color:#155724;">A token has been generated. Please <a href="{mailto_link}" style="color:#155724;text-decoration:underline;font-weight:bold;">click here</a> to send the token to your email and check your inbox.</div>""", unsafe_allow_html=True)
        else:
            st.error("Unauthorized email address. Please enter a valid authorized email address.")

    # Input token hanya muncul setelah token dihasilkan
    if st.session_state.token:
        token_input = st.text_input("Enter your token")

        if st.button("Log in"):
            if token_input == st.session_state.token:
                st.success("Logged in successfully!")
                st.session_state.logged_in = True
                st.session_state.token = None  # Reset token setelah login
            else:
                st.error("Invalid token.")

# Menjalankan fungsi login
if not st.session_state.logged_in:
    login()
else:
    st.write("Welcome to the application!")
