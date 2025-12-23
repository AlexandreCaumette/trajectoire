import streamlit as st

from src.components import login
from src.components.icons import icon
from src.data import database


def main_accueil():
    st.header("Accueil")

    col_signup, col_pad, col_signin = st.columns([6, 1, 6], vertical_alignment="center")

    if "login_mode" not in st.session_state:
        st.session_state["login_mode"] = ""

    with col_signup:
        if st.button(
            "Je veux me créer un compte",
            icon=icon("account_circle"),
            type="tertiary",
        ):
            st.session_state["login_mode"] = "signup"

    if database.get_user_id() == "":
        with col_pad:
            st.text("ou")

        with col_signin:
            if st.button("Je veux me connecter", icon=icon("login"), type="tertiary"):
                st.session_state["login_mode"] = "signin"

    st.divider()

    if st.session_state["login_mode"] == "signup":
        st.subheader("Me créer un compte")

        login.main_signup()

    elif st.session_state["login_mode"] == "signin":
        st.subheader("Me connecter à mon compte")

        login.main_signin()
