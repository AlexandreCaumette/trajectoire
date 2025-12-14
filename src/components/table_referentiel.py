import polars as pl
import streamlit as st

from src.models import models


def table_referentiel():
    if "df_referentiel" in st.session_state:
        df_referentiel = st.session_state.df_referentiel

    else:
        df_referentiel = pl.DataFrame(schema=models.SCHEMA_REFERENTIEL)

        st.session_state["df_referentiel"] = df_referentiel

    st.dataframe(df_referentiel)
