import datetime as dt

import polars as pl
import streamlit as st

from src import logger


def bouton_telechargement_referentiel():
    if "df_referentiel" in st.session_state:
        if st.session_state.df_referentiel.is_empty():
            st.warning(
                "Le référentiel est vide, il faut ajouter au moins 1 ligne pour pouvoir l'exporter."
            )

            return

        df: pl.DataFrame = st.session_state.df_referentiel

        data = df.write_csv()

        timestamp = dt.datetime.now().strftime("%Y%m%dT%H%M%S")

        file_name = f"{timestamp}_mon_referentiel.csv"

        st.download_button(
            label="Télécharger mon référentiel",
            type="secondary",
            data=data,
            file_name=file_name,
            mime="text/csv",
            icon="⬇️",
        )

        logger.info("Référentiel téléchargé.")
