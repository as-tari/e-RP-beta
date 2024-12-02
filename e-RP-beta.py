import streamlit as st
import random
import string
import os
from dotenv import load_dotenv

# Muat variabel lingkungan dari file .env
load_dotenv()
ALLOWED_EMAILS = os.getenv("ALLOWED_EMAILS").split(",")

# Fungsi untuk menghasilkan token acak
def generate_token(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Inisialisasi session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "token" not in st.session_state:
    st.session_state.token = None

ROLES = [None, "Requester", "Responder", "Admin"]

def login():
    st.header("Log in")
    email_input = st.text_input("Enter your email to log in")

    if st.button("Request Token"):
        if email_input in ALLOWED_EMAILS:
            st.session_state.token = generate_token()
            subject = "Your Authentication Token"
            body = f"Your token is: {st.session_state.token}"
            mailto_link = f"mailto:{email_input}?subject={subject}&body={body}"
            st.markdown(f"""<div style="background-color:#d4edda;padding:10px;border-radius:5px;color:#155724;"> A token has been generated. Please <a href="{mailto_link}" style="color:#155724;text-decoration:underline;font-weight:bold;">click here</a> to send the token to your email and check your inbox. </div> """, unsafe_allow_html=True)
        else:
            st.error("Unauthorized email address. Please enter a valid authorized email address.")

    if st.session_state.token:
        token_input = st.text_input("Enter your token")

        if st.button("Log in"):
            if token_input == st.session_state.token:
                st.success("Logged in successfully!")
                st.session_state.logged_in = True
                st.session_state.role = st.selectbox("Choose your role", ROLES)
                st.session_state.token = None  # Reset token setelah login
                st.rerun()  # Refresh halaman setelah login
            else:
                st.error("Invalid token.")

def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.rerun()  # Refresh halaman setelah logout

# Mengelola halaman berdasarkan role
role = st.session_state.role

logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")
request_1 = st.Page("request/request_1.py", title="Request 1", icon=":material/help:", default=(role == "Requester"))
request_2 = st.Page("request/request_2.py", title="Request 2", icon=":material/bug_report:")
respond_1 = st.Page("respond/respond_1.py", title="Respond 1", icon=":material/healing:", default=(role == "Responder"))
respond_2 = st.Page("respond/respond_2.py", title="Respond 2", icon=":material/handyman:")
admin_1 = st.Page("admin/admin_1.py", title="Admin 1", icon=":material/person_add:", default=(role == "Admin"))
admin_2 = st.Page("admin/admin_2.py", title="Admin 2", icon=":material/security:")

# Mengelompokkan halaman berdasarkan role
account_pages = [logout_page, settings]
request_pages = [request_1, request_2]
respond_pages = [respond_1, respond_2]
admin_pages = [admin_1, admin_2]

# Menyusun dictionary halaman
page_dict = {}
if st.session_state.role in ["Requester", "Admin"]:
    page_dict["Request"] = request_pages
if st.session_state.role in ["Responder", "Admin"]:
    page_dict["Respond"] = respond_pages
if st.session_state.role == "Admin":
    page_dict["Admin"] = admin_pages

# Menampilkan judul dan logo
st.title("Request manager")
st.image("images/horizontal_blue.png", use_column_width=True)
st.image("images/icon_blue.png", width=50)

# Menampilkan navigasi
if st.session_state.logged_in:
    if len(page_dict) > 0:
        pg = st.navigation({"Account": account_pages} | page_dict)
    else:
        pg = st.navigation([st.Page(login)])
else:
    pg = st.navigation([st.Page(login)])

pg.run()
