import streamlit as st
from utils.auth import check_role
from admin.dashboard import show_dashboard as admin_dashboard
from coordinator.dashboard import show_dashboard as coordinator_dashboard
from team.navy import show_dashboard as navy_dashboard
from team.niki import show_dashboard as niki_dashboard
from team.eta import show_dashboard as eta_dashboard
from lecturer.dashboard import show_dashboard as lecturer_dashboard
from student.dashboard import show_dashboard as student_dashboard

# Inisialisasi session state
if "role" not in st.session_state:
    st.session_state.role = None

# Fungsi untuk menampilkan dashboard berdasarkan role
def display_dashboard():
    if st.session_state.role == "Admin":
        admin_dashboard()
    elif st.session_state.role == "Coordinator":
        coordinator_dashboard()
    elif st.session_state.role == "Eta":
        navy_dashboard()
    elif st.session_state.role == "Navy":
        niki_dashboard()
    elif st.session_state.role == "Niki":
        eta_dashboard()
    elif st.session_state.role == "Tari":
        eta_dashboard()      
    elif st.session_state.role == "Lecturer":
        lecturer_dashboard()
    elif st.session_state.role == "Student":
        student_dashboard()
    else:
        st.warning("Please log in to access your dashboard.")

# Login dan pemilihan role
st.title("📑 e-RP Assistant System")
role_input = st.selectbox("Select your role", ["Admin", "Coordinator", "Eta", "Navy", "Niki", "Tari", "Lecturer", "Student"])
st.session_state.role = role_input

display_dashboard()
