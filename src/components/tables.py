from typing import Literal

import polars as pl
import streamlit as st

from src import logger
from src.components.icons import icon
from src.components.message import message
from src.data import database


def supprimer_lignes_table(
    rows: list, table: Literal["referentiel", "accomplissements"]
):
    try:
        logger.info(f"Suppression d'éléments de la table {table}.")

        if table == "referentiel":
            df: pl.DataFrame = st.session_state.df_referentiel

        elif table == "accomplissements":
            df: pl.DataFrame = st.session_state.df_contributions

        df = df.filter(pl.arange(0, df.height).is_in(rows))

        liste_ids = df["id"].to_list()

        if table == "referentiel":
            database.delete_referentiel(liste_ids)

        elif table == "accomplissements":
            database.delete_accomplissement(liste_ids)

        message("Les lignes ont bien été supprimées !", "success")

        st.rerun()

    except Exception as error:
        logger.error(error)

        message("Une erreur est survenue.", "error")


def table_accomplissement():
    if "df_contributions" not in st.session_state:
        message("En attente du premier accomplissement.", "info")

        return

    df_contributions: pl.DataFrame = st.session_state.df_contributions

    event = st.dataframe(
        data=df_contributions.drop("id"),
        selection_mode="multi-row",
        on_select="rerun",
    )

    selection = event.get("selection", {})

    rows = selection.get("rows", [])

    if len(rows) > 0:
        label = "Supprimer les lignes sélectionnées"

        if len(rows) == 1:
            label = "Supprimer la ligne sélectionnée"

        if st.button(label=label, icon=icon("delete"), type="tertiary"):
            supprimer_lignes_table(rows, "accomplissements")


def table_referentiel():
    if "df_referentiel" not in st.session_state:
        message("En attente de la première contribution.", "info")

        return

    df_referentiel: pl.DataFrame = st.session_state.df_referentiel

    event = st.dataframe(
        data=df_referentiel.drop("id"), selection_mode="multi-row", on_select="rerun"
    )

    selection = event.get("selection", {})

    rows = selection.get("rows", [])

    if len(rows) > 0:
        label = "Supprimer les lignes sélectionnées"

        if len(rows) == 1:
            label = "Supprimer la ligne sélectionnée"

        if st.button(label=label, icon=icon("delete"), type="tertiary"):
            supprimer_lignes_table(rows, "referentiel")
