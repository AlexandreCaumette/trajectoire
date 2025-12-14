import streamlit as st

from src.components.message import message


def table_referentiel():
    if "df_referentiel" not in st.session_state:
        message("En attente du premier accomplissement.", "info")

        return

    df_referentiel = st.session_state.df_referentiel

    st.dataframe(df_referentiel)
