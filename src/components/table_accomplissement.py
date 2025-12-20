import polars as pl
import streamlit as st

from src import logger
from src.components.message import message
from src.data import database


def supprimer_accomplissements(rows: list):
    try:
        logger.info("Suppression d'éléments dans les accomplissements.")

        df_contributions: pl.DataFrame = st.session_state.df_contributions

        df_contributions = df_contributions.filter(
            pl.arange(0, df_contributions.height).is_in(rows)
        )

        id_accomplissement = df_contributions["id"].to_list()

        database.delete_accomplissement(id_accomplissement=id_accomplissement)

        message("Les lignes ont bien été supprimées !", "success")

        st.rerun()

    except Exception as error:
        logger.error(error)

        message("Une erreur est survenue.", "error")


def table_accomplissement():
    if "df_contributions" not in st.session_state:
        message("En attente du premier accomplissement.", "info")

        return

    df_contributions = st.session_state.df_contributions

    event = st.dataframe(
        data=df_contributions, selection_mode="multi-row", on_select="rerun"
    )

    selection = event.get("selection", {})

    rows = selection.get("rows", [])

    if len(rows) > 0:
        label = "Supprimer les lignes sélectionnées"

        if len(rows) == 1:
            label = "Supprimer la ligne sélectionnée"

        if st.button(label=label, icon="🗑️"):
            supprimer_accomplissements(rows)
