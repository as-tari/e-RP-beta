import streamlit as st
import random
import string
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

# Load environment variables from .env file
load_dotenv()
allowed_emails = os.getenv("ALLOWED_EMAILS").split(",")
email_username = os.getenv("EMAIL_USERNAME")
email_password = os.getenv("EMAIL_PASSWORD")

# Function to generate a random token
def generate_token(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "token" not in st.session_state:
    st.session_state.token = None
if "email_sent" not in st.session_state:
    st.session_state.email_sent = False

# Main login function
def login():
    st.header("Log in")

    # Input email
    email_input = st.text_input("Enter your email")

    if st.button("Request Token"):
        if email_input in allowed_emails:
            # Generate token
            token = generate_token()
            subject = "Your Authentication Token"
            body = f"Your token is: {token}"

            # Send email using SMTP
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = email_username
            msg["To"] = email_input

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(email_username, email_password)
            server.sendmail(email_username, email_input, msg.as_string())
            server.quit()

            st.success("Token has been sent to your email. Please check your email to enter the token.")
            st.session_state.token = token
            st.session_state.email_sent = True
        else:
            st.error("Unauthorized email address. Please use an allowed email.")

    # Input token only if email has been sent
    if st.session_state.email_sent:
        token_input = st.text_input("Enter your token")

        if st.button("Log in"):
            if token_input == st.session_state.token:
                st.success("Logged in successfully!")
                st.session_state.logged_in = True
                st.session_state.token = None
                st.session_state.email_sent = False
                st.experimental_rerun()
            else:
                st.error("Invalid token.")

# Run the login function
if not st.session_state.logged_in:
    login()
else:
    st.write("Welcome to the application!")
