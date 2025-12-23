import streamlit as st

from src.components.login import main_reset


def main_reset_password():
    st.set_page_config(
        page_title="Réinitialisation", page_icon="🔑", initial_sidebar_state="collapsed"
    )

    st.header("🔑 Réinitialisation de mon mot de passe")

    st.text("Bienvenu dans l'interface de réinitialisation de votre mot de passe.")

    main_reset()
