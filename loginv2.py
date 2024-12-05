import streamlit as st
from PIL import Image
import random
import string
import os
from dotenv import load_dotenv

# Page config
st.set_page_config(
    page_title="Log in | e-RP Assistant System"
)

# Welcome text
st.write("Welcome to e-RP Assistant System!")

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
if "role" not in st.session_state:
    st.session_state.role = None

# Function for login
def login():
    st.header("Log in")

    # Input email address
    email_input = st.text_input("Enter your email to log in")

    if st.button("Request Token"):
        if email_input in ALLOWED_EMAILS:
            # Generate token
            st.session_state.token = generate_token()
            subject = "Your Authentication Token"
            body = f"Your token is: {st.session_state.token}"
            mailto_link = f"mailto:{email_input}?subject={subject}&body={body}"
            st.markdown(f"""<div style="background-color:#d4edda;padding:10px;border-radius:5px;color:#155724;"> A token has been generated. Please <a href="{mailto_link}" style="color:#155724;text-decoration:underline;font-weight:bold;">click here</a> to send the token to your email and check your inbox. </div> """, unsafe_allow_html=True)
        else:
            st.error("Unauthorized email address. Please enter a valid authorized email address.")

    # Input token only appears after token is generated
    if st.session_state.token:
        token_input = st.text_input("Enter your token")

        if st.button("Log in"):
            if token_input == st.session_state.token:
                st.success("Logged in successfully!")
                st.session_state.logged_in = True
                st.session_state.token = None  # Reset token after login
                select_role()  # Call function to select role after successful login
            else:
                st.error("Invalid token.")

# Function to select role after login
def select_role():
    st.header("Select Your Role")
    roles = ["Admin", "Team", "Lecturer", "Student"]
    role = st.selectbox("Choose your role", roles)

    if role == "Team":
        team_roles = ["Coordinator", "Eta", "Navy", "Niki", "Tari"]
        team_role = st.selectbox("Choose your team role", team_roles)
        if st.button("Confirm Role"):
            st.session_state.role = (role, team_role)
            st.success(f"You are logged in as {role} - {team_role}.")
            st.experimental_rerun()  # Refresh the app to show the appropriate dashboard
    else:
        if st.button("Confirm Role"):
            st.session_state.role = (role, None)
            st.success(f"You are logged in as {role}.")
            st.experimental_rerun()  # Refresh the app to show the appropriate dashboard

# Function to display the application based on role
def display_app():
    st.write("Welcome to the application!")
    # Here you can add the logic to display different dashboards based on the role
    if st.session_state.role[0] == "Admin":
        st.write("Admin Dashboard")
        # Add admin dashboard logic here
    elif st.session_state.role[0] == "Team":
        st.write(f"{st.session_state.role[1]} Dashboard")
        # Add team dashboard logic here
    elif st.session_state.role[0] == "Lecturer":
        st.write("Lecturer Dashboard")
        # Add lecturer dashboard logic here
    elif st.session_state.role[0] == "Student":
        st.write("Student Dashboard")
        # Add student dashboard logic here

# Display the login form or the application based on login state
if not st.session_state.logged_in:
    login()
else:
    display_app()
