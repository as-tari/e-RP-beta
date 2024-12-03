import streamlit as st
import random
import string
import os
import base64
from dotenv import load_dotenv

# Muat variabel lingkungan dari file .env
load_dotenv()
ALLOWED_EMAILS = os.getenv("ALLOWED_EMAILS").split(",")

# Fungsi untuk menghasilkan token acak
def generate_token(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Fungsi untuk mengenkode token dengan Base64
def encode_token(token):
    return base64.b64encode(token.encode()).decode()

# Fungsi untuk mendekode token dari Base64
def decode_token(encoded_token):
    return base64.b64decode(encoded_token).decode()

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
            raw_token = generate_token()
            encoded_token = encode_token(raw_token)  # Encode token
            st.session_state.token = encoded_token  # Store encoded token
            subject = "Your Authentication Token"
            body = f"Your token is: {raw_token}"  # Send raw token in the email body
            mailto_link = f"mailto:{email_input}?subject={subject}&body={body}"
            st.markdown(f"""<div style="background-color:#d4edda;padding:10px;border-radius:5px;color:#155724;"> A token has been generated. Please <a href="{mailto_link}" style="color:#155724;text-decoration:underline;font-weight:bold;">click here</a> to send the token to your email and check your inbox. </div> """, unsafe_allow_html=True)
        else:
            st.error("Unauthorized email address. Please enter a valid authorized email address.")

    # Input token hanya muncul setelah token dihasilkan
    if st.session_state.token:
        token_input = st.text_input("Enter your token")

        if st.button("Log in"):
            decoded_token = decode_token(st.session_state.token)  # Decode token for verification
            if token_input == decoded_token:
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
