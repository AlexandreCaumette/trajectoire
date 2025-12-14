import streamlit as st

from src.data import database


def main_accueil():
    st.header("Accueil")

    tab_signup, tab_signin = st.tabs(["Me créer un compte", "Me connecter"])

    with tab_signup:
        email = st.text_input(label="Mon email :", key="signup-email")

        password = st.text_input(
            label="Mon mot de passe :", type="password", key="signup-password"
        )

        if st.button("Créer un compte"):
            database.signup_user(email, password)

    with tab_signin:
        email = st.text_input(label="Mon email :", key="signin-email")

        password = st.text_input(
            label="Mon mot de passe :", type="password", key="signin-password"
        )

        if st.button("Se connecter"):
            database.signin_user(email, password)
