import streamlit as st
import random
import string
import os
from dotenv import load_dotenv
import urllib.parse

# Muat variabel lingkungan dari file .env
load_dotenv()
ALLOWED_EMAILS = os.getenv("ALLOWED_EMAILS").split(",")

# Fungsi untuk menghasilkan token acak
def generate_token(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Fungsi untuk membuat file token yang akan diunduh
def create_token_file(token):
    # Nama file token
    token_file_name = "token.txt"
    with open(token_file_name, "w") as file:
        file.write(f"Your token is: {token}")
    return token_file_name

# Fungsi untuk membuat link mailto dengan instruksi
def create_mailto_link(email, subject, token_file_name):
    # Instruksi untuk badan email
    body = "Click on the attached file to retrieve your token."
    body_encoded = urllib.parse.quote(body)  # URL-encode badan email
    mailto_link = f"mailto:{email}?subject={subject}&body={body_encoded}"
    return mailto_link

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
            st.session_state.token = generate_token()

            # Create the token file and get the file name
            token_file_name = create_token_file(st.session_state.token)

            # Create mailto link with instructions
            subject = "Your Authentication Token"
            mailto_link = create_mailto_link(email_input, subject, token_file_name)

            # Display mailto link to open the user's email client
            st.markdown(f"""<div style="background-color:#d4edda;padding:10px;border-radius:5px;color:#155724;"> A token has been generated. Please <a href="{mailto_link}" style="color:#155724;text-decoration:underline;font-weight:bold;">click here</a> to send the token to your email and check your inbox. </div> """, unsafe_allow_html=True)
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
