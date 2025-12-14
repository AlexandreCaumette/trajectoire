import streamlit as st

from src.components.form_accomplissement import form_accomplissement
from src.components.table_accomplissement import table_accomplissement


def main_accomplissement():
    st.header("🎉 Mes contributions")

    with st.expander(label="Table de mes accomplissements", expanded=True):
        table_accomplissement()

    with st.expander(label="Accomplir une nouvelle contribution"):
        form_accomplissement()
