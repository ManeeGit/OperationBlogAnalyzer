import streamlit as st
from datetime import datetime, timedelta
from mongodb import add_user

def admin_panel():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🛠 Admin Panel")

    with st.sidebar.expander("➕ Add New User"):
        new_username = st.text_input("New Username", key="new_user")
        new_password = st.text_input("New Password", type="password", key="new_pass")

        role = st.selectbox("User Role", ["Normal User", "Admin"])
        is_admin_flag = (role == "Admin")

        is_temp = st.checkbox("Temporary User?")
        expiry_days = st.number_input("Expires in (days)", min_value=1, max_value=365, value=7) if is_temp else None

        if st.button("Create User"):
            expires_at = datetime.utcnow() + timedelta(days=expiry_days) if is_temp else None
            success = add_user(new_username, new_password, expires_at, is_admin_flag)
            if success:
                st.success(f"✅ User '{new_username}' created as {'Admin' if is_admin_flag else 'Normal'} user.")
            else:
                st.error("❌ User creation failed or user already exists.")
