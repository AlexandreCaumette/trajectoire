import streamlit as st

from src.data import database
from src.pages.page_referentiel import main_referentiel


def main_accueil():
    st.header("Accueil")

    tabs = ["Me créer un compte", "Me connecter"]

    if database.get_user_id() != "":
        tabs = ["Me créer un compte", "Me déconnecter"]

    tab_signup, tab_signin = st.tabs(tabs)

    with tab_signup:
        email = st.text_input(label="Mon email :", key="signup-email")

        password = st.text_input(
            label="Mon mot de passe :", type="password", key="signup-password"
        )

        if st.button("Créer un compte"):
            with st.spinner(text="Création du compte...", show_time=True):
                database.signup_user(email, password)

    with tab_signin:
        if database.get_user_id() != "":
            if st.button(label="Me déconnecter"):
                database.signout_user()

                st.rerun()

        else:
            email = st.text_input(label="Mon email :", key="signin-email")

            password = st.text_input(
                label="Mon mot de passe :", type="password", key="signin-password"
            )

            if st.button("Se connecter"):
                with st.spinner(text="Connexion...", show_time=True):
                    database.signin_user(email, password)

                with st.spinner(
                    text="Récupération de mes informations...", show_time=True
                ):
                    database.fetch_user_referentiel()
                    database.fetch_user_accomplissements()

                page_referentiel = st.Page(
                    page=main_referentiel,
                    title="Mon référentiel",
                    icon="⚙️",
                    url_path="referentiel",
                )

                st.switch_page(page=page_referentiel)
