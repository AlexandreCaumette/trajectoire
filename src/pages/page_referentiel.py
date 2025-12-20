import streamlit as st

from src.components import boutons
from src.components.form_referentiel import (
    form_referentiel,
)
from src.components.table_referentiel import table_referentiel


def main_referentiel():
    st.header("⚙️ Mon référentiel de contributions")

    with st.expander(label="Table de mes contributions", expanded=True):
        table_referentiel()

        st.divider()

        col_telechargement, col_actualisation = st.columns(2)

        with col_actualisation:
            boutons.bouton_actualisation(table="référentiel")

        with col_telechargement:
            boutons.bouton_telechargement(table="référentiel")

    with st.expander(label="Ajouter une nouvelle contribution"):
        form_referentiel()
