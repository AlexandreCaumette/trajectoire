import polars as pl
import streamlit as st

from src import logger
from src.models import models


def bouton_chargement_referentiel():
    file = st.file_uploader(
        label="Sélectionner un export de référentiel :",
        type="csv",
        accept_multiple_files=False,
    )

    if file is not None:
        logger.debug("Fichier chargé.")

        with st.spinner(show_time=True, text="Chargement des données..."):
            df = pl.read_csv(file, schema=models.SCHEMA_REFERENTIEL)

        st.dataframe(df)

        if st.button(label="Charger ce référentiel", type="secondary", icon="⬆️"):
            logger.debug("Validation du chargement du référentiel")

            st.session_state["df_referentiel"] = df

            st.rerun()
