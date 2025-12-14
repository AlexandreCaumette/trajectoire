import streamlit as st

from src.components.bouton_telechargement import bouton_telechargement_referentiel
from src.components.form_referentiel import (
    form_referentiel,
)
from src.components.table_referentiel import table_referentiel


def main_referentiel():
    st.set_page_config(layout="wide")

    st.header("⚙️ Mon référentiel de contributions")

    with st.expander(label="Table de mes contributions", expanded=True):
        table_referentiel()

        bouton_telechargement_referentiel()

    with st.expander(label="Ajouter une nouvelle contribution"):
        form_referentiel()
