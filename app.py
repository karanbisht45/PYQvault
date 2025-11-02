import streamlit as st
import base64
from utils import auth, file_handler, analytics
import backend

st.set_page_config(page_title="PYQ Management System", page_icon="📚", layout="wide")
backend.init_db()

# ----------------- EMBED LOGO SAFELY -----------------
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Convert logo to base64 for reliable display
logo_base64 = get_base64_image("picture4.png")

# ----------------- HEADER SECTION -----------------
st.markdown(
    f"""
    <div style='text-align: center;'>
        <img src='data:image/png;base64,{logo_base64}' width='90' style='display: block; margin: 0 auto;'>
        <h2 style='margin-bottom: 0; font-family: "Segoe UI", sans-serif;'>Graphic Era Hill University</h2>
        <h3 style='color: #666; font-family: "Segoe UI", sans-serif;'>PYQvault</h3>
    </div>
    <hr>
    """,
    unsafe_allow_html=True
)

# ----------------- LOGIN SYSTEM -----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

if not st.session_state.logged_in:
    col1, col2 = st.columns([2, 2])
    with col1:
        st.header("Welcome 🔎")
        st.write("Upload and browse previous year question papers. Create an account to upload.")
        st.write("If you're a student just browsing, you can signup as a `viewer` or use a guest experience.")
    with col2:
        choice = st.selectbox("Go to", ["Login", "Sign up"])
        if choice == "Login":
            user = auth.login_form()
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()
        else:
            auth.signup_form()
else:
    user = st.session_state.user
    st.sidebar.write(f"Logged in as: **{user['username']}** — {user['role']}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    st.sidebar.title("Navigation")
    if user["role"] == "uploader":
        nav = st.sidebar.radio("Menu", ["Upload PYQ", "My Uploads", "Browse PYQs", "Analytics", "Profile"])
    else:
        nav = st.sidebar.radio("Menu", ["Browse PYQs", "Favorites", "Analytics", "Profile"])

    if nav == "Upload PYQ":
        file_handler.upload_pyq(user)
    elif nav == "Browse PYQs":
        file_handler.browse_pyqs(user)
    elif nav == "Favorites":
        st.info("Favorites feature: Coming soon.")
    elif nav == "Analytics":
        analytics.show_dashboard()
    elif nav == "Profile":
        st.subheader("Profile")
        st.write("Username:", user["username"])
        st.write("Email:", user["email"])
        st.write("Role:", user["role"])
