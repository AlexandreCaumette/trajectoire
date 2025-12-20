import streamlit as st

from src.components import boutons
from src.components.form_accomplissement import form_accomplissement
from src.components.table_accomplissement import table_accomplissement


def main_accomplissement():
    st.header("🎉 Mes contributions")

    with st.expander(label="Table de mes accomplissements", expanded=True):
        table_accomplissement()

        st.divider()

        col_telechargement, col_actualisation = st.columns(2)

        with col_actualisation:
            boutons.bouton_actualisation(table="accomplissements")

        with col_telechargement:
            boutons.bouton_telechargement(table="accomplissements")

    with st.expander(label="Accomplir une nouvelle contribution"):
        form_accomplissement()
