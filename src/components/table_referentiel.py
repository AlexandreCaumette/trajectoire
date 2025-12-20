import polars as pl
import streamlit as st

from src import logger
from src.components.message import message
from src.data import database


def supprimer_referentiels(rows: list):
    try:
        logger.info("Suppression d'éléments dans le référentiel.")

        df_referentiel: pl.DataFrame = st.session_state.df_referentiel

        df_referentiel = df_referentiel.filter(
            pl.arange(0, df_referentiel.height).is_in(rows)
        )

        id_referentiel = df_referentiel["id"].to_list()

        database.delete_referentiel(id_referentiel=id_referentiel)

        message("Les lignes ont bien été supprimées !", "success")

        st.rerun()

    except Exception as error:
        logger.error(error)

        message("Une erreur est survenue.", "error")


def table_referentiel():
    if "df_referentiel" not in st.session_state:
        message("En attente de la première contribution.", "info")

        return

    df_referentiel = st.session_state.df_referentiel

    event = st.dataframe(
        data=df_referentiel, selection_mode="multi-row", on_select="rerun"
    )

    selection = event.get("selection", {})

    rows = selection.get("rows", [])

    if len(rows) > 0:
        label = "Supprimer les lignes sélectionnées"

        if len(rows) == 1:
            label = "Supprimer la ligne sélectionnée"

            if st.button(label=label, icon="🗑️"):
                supprimer_referentiels(rows)
