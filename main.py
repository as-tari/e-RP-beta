import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Log in | e-RP Assistant System"
)
    

# Inisialisasi session state untuk role
if "role" not in st.session_state:
    st.session_state.role = None

# Daftar peran yang tersedia
ROLES = ["Admin", "Team", "Lecturer", "Student"]
TEAM_ROLES = ["Coordinator", "Eta", "Navy", "Niki", "Tari"]

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
