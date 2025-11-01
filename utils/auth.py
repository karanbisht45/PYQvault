import streamlit as st
import backend

def signup_form():
    st.subheader("Create an account")
    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["viewer", "uploader"])
        submitted = st.form_submit_button("Sign up")
        if submitted:
            if not username or not email or not password:
                st.error("All fields are required")
            else:
                ok = backend.add_user(username, email, password, role)
                if ok:
                    st.success("Account created. Please login.")
                else:
                    st.error("An account with this email already exists.")

def login_form():
    st.subheader("Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            user = backend.authenticate_user(email, password)
            if user:
                st.success("Logged in successfully")
                return user
            else:
                st.error("Invalid credentials")
    return None
