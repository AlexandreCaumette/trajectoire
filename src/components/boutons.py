import datetime as dt
from typing import Literal

import polars as pl
import streamlit as st

from src import logger
from src.components.message import message
from src.data import database


def bouton_telechargement(table: Literal["référentiel", "accomplissements"]):
    if table == "référentiel":
        key = "df_referentiel"

    elif table == "accomplissements":
        key = "df_contributions"

    if key not in st.session_state:
        return

    df: pl.DataFrame = st.session_state[key]

    if df.is_empty():
        message(
            message=f"Le {table} est vide, il faut ajouter au moins 1 ligne pour pouvoir l'exporter.",
            type="warning",
        )

        return

    data = df.write_csv()

    timestamp = dt.datetime.now().strftime("%Y%m%dT%H%M%S")

    file_name = f"{timestamp}_{table}.csv"

    label = "Télécharger"

    if table == "référentiel":
        label = f"{label} mon {table}"

    elif table == "accomplissements":
        label = f"{label} mes {table}"

    st.download_button(
        label=f"Télécharger mon {table}",
        type="primary",
        data=data,
        file_name=file_name,
        mime="text/csv",
        icon="⬇️",
    )

    logger.info(f"{table} téléchargé.")


def bouton_actualisation(table: Literal["référentiel", "accomplissements"]):
    label = "Actualiser"

    if table == "référentiel":
        label = f"{label} le {table}"

    elif table == "accomplissements":
        label = f"{label} les {table}"

    if st.button(label=label, icon="🔄", type="secondary"):
        with st.spinner(show_time=True, text="Actualisation..."):
            if table == "référentiel":
                database.fetch_user_referentiel()

            elif table == "accomplissements":
                database.fetch_user_accomplissements()

            st.rerun()
