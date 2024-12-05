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

def login():
    st.header("Log in")
    role = st.selectbox("Choose your role", ROLES)

    if role == "Team":
        team_role = st.selectbox("Choose your team role", TEAM_ROLES)
        if st.button("Log in"):
            st.session_state.role = (role, team_role)
            st.rerun()  # Menggunakan rerun untuk memperbarui tampilan
    else:
        if st.button("Log in"):
            st.session_state.role = (role, None)
            st.rerun()  # Menggunakan rerun untuk memperbarui tampilan

def logout():
    st.session_state.role = None
    st.rerun()  # Menggunakan rerun untuk memperbarui tampilan

# Menampilkan logo aplikasi
image = Image.open('static/images/logo.png')
st.image(image, caption=None, width=50, use_column_width=False, clamp=False, channels="RGB", output_format="auto")
st.logo("static/images/logo1.png", icon_image="static/images/logo1.png")

# Menampilkan halaman login jika belum login
if st.session_state.role is None:
    login()
else:
    # Menentukan halaman berdasarkan peran
    logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
    settings = st.Page("admin/settings.py", title="Settings", icon=":material/settings:")
    
    # Halaman untuk Admin
    if st.session_state.role[0] == "Admin":
        admin_dashboard = st.Page("admin/dashboard.py", title="Admin Dashboard", icon=":material/person_add:")
        manage_users = st.Page("admin/manage_users.py", title="Manage Users", icon=":material/security:")
    
    # Halaman untuk Team
    if st.session_state.role[0] == "Team":
        team_dashboard = st.Page(f"team/{st.session_state.role[1].lower()}.py", title=f"{st.session_state.role[1]} Dashboard", icon=":material/group:")
    
    # Halaman untuk Lecturer
    if st.session_state.role[0] == "Lecturer":
        lecturer_dashboard = st.Page("lecturer/dashboard.py", title="Lecturer Dashboard", icon=":material/teacher:")
    
    # Halaman untuk Student
    if st.session_state.role[0] == "Student":
        student_dashboard = st.Page("student/dashboard.py", title="Student Dashboard", icon=":material/student:")

    # Menyusun halaman berdasarkan peran
    account_pages = [logout_page, settings]
    page_dict = {}

    if st.session_state.role[0] == "Admin":
        page_dict["Admin"] = [admin_dashboard, manage_users]
    if st.session_state.role[0] == "Team":
        page_dict["Team"] = [team_dashboard]
    if st.session_state.role[0] == "Lecturer":
        page_dict["Lecturer"] = [lecturer_dashboard]
    if st.session_state.role[0] == "Student":
        page_dict["Student"] = [student_dashboard]

    # Menampilkan navigasi
    if len(page_dict) > 0:
        pg = st.navigation({"Account": account_pages} | page_dict)
    else:
        pg = st.navigation([st.Page(login)])

    pg.run()
