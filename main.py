import streamlit as st
from utils.auth import check_role
from admin.dashboard import show_dashboard as admin_dashboard
from team.coordinator import show_dashboard as coordinator_dashboard
from team.navy import show_dashboard as navy_dashboard
from team.niki import show_dashboard as niki_dashboard
from team.eta import show_dashboard as eta_dashboard
from team.tari import show_dashboard as tari_dashboard
from lecturer.dashboard import show_dashboard as lecturer_dashboard
from student.dashboard import show_dashboard as student_dashboard

# Inisialisasi session state
if "role" not in st.session_state:
    st.session_state.role = None

# Fungsi untuk menampilkan dashboard berdasarkan role
def display_dashboard():
    if st.session_state.role == "Admin":
        admin_dashboard()
    elif st.session_state.role == "Team":
        team_role = st.selectbox(["Coordinator", "Eta", "Navy", "Niki", "Tari"])
        if team_role == "Coordinator":
            coordinator_dashboard()
        elif team_role == "Navy":
            navy_dashboard()
        elif team_role == "Niki":
            niki_dashboard()
        elif team_role == "Eta":
            eta_dashboard()
        elif team_role == "Tari":
            tari_dashboard()
    elif st.session_state.role == "Lecturer":
        lecturer_dashboard()
    elif st.session_state.role == "Student":
        student_dashboard()
    else:
        st.warning("Please log in to access your dashboard.")

# Login dan pemilihan role
st.image("images/3.png")
st.title("📑 e-RP Assistant System")
st.logo("static/images/6.png", icon_image="static/images/3.png")
st.markdown("<h2 style='font-family: 'Courier New'; color: blue;'>Welcome!</h2>", unsafe_allow_html=True)
role_input = st.selectbox("Continue log in as", ["Admin", "Team", "Lecturer", "Student"])
st.session_state.role = role_input

display_dashboard()
