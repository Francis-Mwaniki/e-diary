import streamlit as st
from utils.database import initialize_database, login_user, register_user

def main():
    initialize_database()
    st.title("Dairy Farm Management System")

    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'login_type' not in st.session_state:
        st.session_state.login_type = None
    if 'show_registration' not in st.session_state:
        st.session_state.show_registration = False

    if st.session_state.user is None:
        if st.session_state.show_registration:
            show_registration_page()
        else:
            show_login_page()

def show_login_page():
    st.subheader("Login")
    with st.form(key="login_form"):
        login_type = st.radio("Login as:", ("Farmer", "Admin"), key="login_type_radio")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        col1, col2 = st.columns(2)
        submit_button = col1.form_submit_button(label="Login")
        register_button = col2.form_submit_button(label="Register")

    if submit_button:
        user = login_user(username, password, login_type.lower())
        if user:
            if user['is_active']:
                st.session_state.user = user
                st.session_state.login_type = login_type.lower()
                st.success("Login successful. Please navigate to your dashboard.")
            else:
                st.error("Your account is inactive. Please contact the admin.")
        else:
            st.error("Invalid credentials")

    if register_button:
        st.session_state.show_registration = True
        st.rerun()

def show_registration_page():
    st.subheader("Register")
    with st.form(key="registration_form"):
        username = st.text_input("Username", key="reg_username")
        password = st.text_input("Password", type="password", key="reg_password")
        role = st.selectbox("Role", ["farmer", "admin"], key="reg_role")
        submit_button = st.form_submit_button(label="Register")

    if submit_button:
        if register_user(username, password, role):
            st.success("Registration successful. Please login.")
            st.session_state.show_registration = False
            st.rerun()
        else:
            st.error("Username already exists")

    if st.button("Back to Login"):
        st.session_state.show_registration = False
        st.rerun()

if __name__ == "__main__":
    main()