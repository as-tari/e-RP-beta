import streamlit as st
import requests
import os
from urllib.parse import urlencode

# GitHub OAuth configuration
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")  # Set your GitHub Client ID
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")  # Set your GitHub Client Secret
REDIRECT_URI = "http://localhost:8501/auth"  # Change this to your redirect URI

# Function to get GitHub access token
def get_access_token(code):
    token_url = "https://github.com/login/oauth/access_token"
    payload = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    headers = {"Accept": "application/json"}
    response = requests.post(token_url, json=payload, headers=headers)
    return response.json().get("access_token")

# Function to get user information
def get_user_info(access_token):
    user_url = "https://api.github.com/user"
    headers = {"Authorization": f"token {access_token}"}
    response = requests.get(user_url, headers=headers)
    return response.json()

# Main application
def main():
    st.title("GitHub OAuth Login")

    # Check if the user is already logged in
    if "user" in st.session_state:
        st.write(f"Logged in as: {st.session_state.user['login']}")
        st.write("User  Info:")
        st.json(st.session_state.user)
        if st.button("Logout"):
            del st.session_state.user  # Clear user session
            st.experimental_rerun()
    else:
        # Generate GitHub login URL
        github_login_url = f"https://github.com/login/oauth/authorize?{urlencode({'client_id': GITHUB_CLIENT_ID, 'redirect_uri': REDIRECT_URI})}"
        st.markdown(f"[Login with GitHub]({github_login_url})")

        # Handle the callback from GitHub
        if "code" in st.experimental_get_query_params():
            code = st.experimental_get_query_params()["code"][0]
            access_token = get_access_token(code)
            if access_token:
                user_info = get_user_info(access_token)
                st.session_state.user = user_info  # Store user info in session state
                st.experimental_rerun()  # Refresh the app to show user info
            else:
                st.error("Failed to retrieve access token.")

if __name__ == "__main__":
    main()
