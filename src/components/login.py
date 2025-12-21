import streamlit as st

from src.components.icons import icon
from src.components.message import message
from src.data import database
from src.pages.page_accueil import main_accueil
from src.pages.page_referentiel import main_referentiel


def main_signout():
    if database.get_user_id() == "":
        return

    if st.button(label="Me déconnecter", icon=icon("logout"), type="primary"):
        database.signout_user()

        page_accueil = st.Page(
            page=main_accueil,
            title="Accueil",
            icon="🏡",
            default=True,
            url_path="accueil",
        )

        st.switch_page(page_accueil)


def main_signin():
    email = st.text_input(
        label="Mon email :",
        key="signin-email",
        placeholder="harty.show@chou.fleur",
        icon=icon("mail"),
        value="",
    )

    password = st.text_input(
        label="Mon mot de passe :",
        type="password",
        key="signin-password",
        icon=icon("password"),
        placeholder="***********",
        value="",
    )

    if st.button("Se connecter", icon=icon("login"), type="primary"):
        if email == "":
            message("Le champ 'email' doit être renseigné !", type="warning")

            return

        if password == "":
            message("Le champ 'mot de passe' doit être renseigné !", type="warning")

            return

        with st.spinner(text="Connexion...", show_time=True):
            database.signin_user(email, password)

        with st.spinner(text="Récupération de mes informations...", show_time=True):
            database.fetch_user_referentiel()
            database.fetch_user_accomplissements()

        page_referentiel = st.Page(
            page=main_referentiel,
            title="Mon référentiel",
            icon="⚙️",
            url_path="referentiel",
        )

        st.session_state["login_mode"] = ""

        st.switch_page(page=page_referentiel)


def main_signup():
    email = st.text_input(
        label="Mon email :",
        key="signup-email",
        icon=icon("mail"),
        placeholder="harty.show@chou.fleur",
        value="",
    )

    password = st.text_input(
        label="Mon mot de passe :",
        type="password",
        key="signup-password",
        icon=icon("password"),
        placeholder="***********",
        value="",
    )

    confirm_password = st.text_input(
        label="Confirmation du mot de passe :",
        type="password",
        key="signup-confirm-password",
        icon=icon("password"),
        placeholder="***********",
        value="",
    )

    if st.button("Créer un compte", icon=icon("account_circle"), type="primary"):
        if email == "":
            message("Le champ 'email' doit être renseigné !", type="warning")

            return

        if password == "":
            message("Le champ 'mot de passe' doit être renseigné !", type="warning")

            return

        if password != confirm_password:
            message(
                "La confirmation du mot de passe n'est pas égale au mot de passe !",
                type="warning",
            )
            return

        with st.spinner(text="Création du compte...", show_time=True):
            database.signup_user(email, password)
