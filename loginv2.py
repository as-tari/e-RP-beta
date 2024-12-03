import streamlit as st
import random
import string
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
ALLOWED_EMAILS = os.getenv("ALLOWED_EMAILS").split(",")

# Function to generate a random token
def generate_token(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "token" not in st.session_state:
    st.session_state.token = None

# Main login function
def login():
    st.header("Log in")

    # Input email address
    email_input = st.text_input("Enter your email to log in")

    if st.button("Request Token"):
        if email_input in ALLOWED_EMAILS:
            # Generate token
            token = generate_token()
            st.session_state.token = token  # Store the token for verification

            # Create the email subject and body
            subject = "Your Authentication Token"
            body = "You have requested a login token. Please check the application for your token."

            # Create the mailto link
            mailto_link = f"mailto:{email_input}?subject={subject}&body={body}"

            # Display a clickable link for the user
            st.markdown(f"""<div style="background-color:#d4edda;padding:10px;border-radius:5px;color:#155724;">
                            A token has been generated. Please <a href="{mailto_link}" style="color:#155724;text-decoration:underline;font-weight:bold;">click here</a> to send the email.
                            You must send the email first before you can enter your token.
                            </div>""", unsafe_allow_html=True)
        else:
            st.error("Unauthorized email address. Please enter a valid authorized email address.")

    # Input token only appears after the token is generated
    if st.session_state.token:
        token_input = st.text_input("Enter your token")

        if st.button("Log in"):
            if token_input == st.session_state.token:
                st.success("Logged in successfully!")
                st.session_state.logged_in = True
                st.session_state.token = None  # Reset token after login
            else:
                st.error("Invalid token.")

# Run the login function
if not st.session_state.logged_in:
    login()
else:
    st.write("Welcome to the application!")
