import pathlib

import streamlit as st

from src import logger
from src.components import login


@st.fragment(run_every="1s")
def hash_to_param():
    if st.query_params.get("access_token", None) is not None:
        st.rerun()

    elif st.session_state["reset_rerun"] < 1:
        logger.debug(f"Actualisation param url : {st.session_state['reset_rerun']}")

        st.session_state["reset_rerun"] += 1

        st.html(
            body=pathlib.Path(__file__).parent.parent / "scripts" / "hash_to_param.js",
            unsafe_allow_javascript=True,
        )


def main_reset_password():
    st.set_page_config(
        page_title="Réinitialisation", page_icon="🔑", initial_sidebar_state="collapsed"
    )

    st.header("🔑 Réinitialisation de mon mot de passe")

    st.text("Bienvenu dans l'interface de réinitialisation de votre mot de passe.")

    if "reset_rerun" not in st.session_state:
        st.session_state["reset_rerun"] = 0

    if st.query_params.get("access_token", None) is None:
        hash_to_param()

    login.main_form_reset()
