import datetime as dt

import plotly.express as px
import plotly.graph_objects as go
import polars as pl
import streamlit as st

from src.data import data


def accomplissements(date_debut: dt.date, date_fin: dt.date) -> go.Figure:
    df: pl.DataFrame = st.session_state.df_contributions

    df = df.filter(pl.col("Date").is_between(date_debut, date_fin))

    df = df.sort("Date")

    df_objectif = data.objectif(date_debut, date_fin)

    fig = px.bar(df, x="Date", y="Score", color="Catégorie")

    return fig


def trajectoire_lineaire(
    date_debut: dt.date, date_fin: dt.date, maille: str
) -> go.Figure:
    df_accomplissements: pl.DataFrame = st.session_state.df_contributions

    df_accomplissements = df_accomplissements.filter(
        pl.col("Date").is_between(date_debut, date_fin)
    )

    df_accomplissements = df_accomplissements.sort("Date")

    df_accomplissements = df_accomplissements.with_columns(
        pl.col("Score").cum_sum().alias("Score cumulé")
    )

    df_accomplissements = df_accomplissements.sort("Date")

    df_accomplissements = df_accomplissements.group_by_dynamic(
        index_column="Date", every=maille
    ).agg(pl.sum("Score"), pl.sum("Score cumulé"))

    trace_reelle = go.Scatter(
        x=df_accomplissements["Date"],
        y=df_accomplissements["Score cumulé"],
        mode="lines",
        name="Ma trajectoire",
    )

    df_objectif = data.objectif(date_debut, date_fin, maille)

    trace_theorique = go.Scatter(
        x=df_objectif["Date"],
        y=df_objectif["Score cumulé"],
        mode="lines",
        name="Mon objectif",
    )

    fig = go.Figure()

    fig.add_trace(trace_reelle)

    fig.add_trace(trace_theorique)

    return fig


def trajectoire_radar(date_debut: dt.date, date_fin: dt.date) -> go.Figure:
    fig = go.Figure()

    df_accomplissements: pl.DataFrame = st.session_state.df_contributions

    df_accomplissements = df_accomplissements.filter(
        pl.col("Date").is_between(date_debut, date_fin)
    )

    df_accomplissements = df_accomplissements.sort("Date")

    df_accomplissements = df_accomplissements.group_by("Catégorie").agg(pl.sum("Score"))

    df_objectif = data.objectif(date_debut, date_fin)

    df_objectif = df_objectif.group_by("Catégorie").agg(pl.sum("Score"))

    df = df_objectif.join(
        df_accomplissements, on="Catégorie", how="left", suffix="_reel"
    )

    df = df.with_columns((pl.col("Score_reel") / pl.col("Score")).alias("Ratio"))

    df = df.sort("Catégorie")

    fig.add_trace(
        go.Scatterpolar(
            r=df["Ratio"],
            theta=df["Catégorie"],
            fill="toself",
        )
    )

    fig.update_layout()

    return fig


def main_trajectoire():
    st.set_page_config(layout="wide")

    st.header("🚀 Ma trajectoire")

    col_date_debut, col_date_fin, col_maille = st.columns(3)

    today = dt.date.today()

    with col_date_debut:
        date_debut = st.date_input(
            label="Sélectionner une date de début :",
            min_value=today.replace(month=1, day=1),
            value=today.replace(month=1, day=1),
            max_value=today.replace(month=12, day=31),
        )

    with col_date_fin:
        date_fin = st.date_input(
            label="Sélectionner une date de fin :",
            min_value=date_debut,
            value="today",
            max_value=today.replace(month=12, day=31),
        )

    with col_maille:
        dict_maille = {"Jour": "1d", "Semaine": "1w", "Mois": "1mo", "Année": "1y"}

        options_maille = dict_maille.keys()

        maille = st.selectbox(
            label="Sélectionner la maille temporelle :", options=options_maille, index=0
        )

        maille = dict_maille.get(maille, "1d")

    st.divider()

    with st.expander("Une trajectoire linéaire ..."):
        fig = trajectoire_lineaire(date_debut, date_fin, maille)

        st.plotly_chart(figure_or_data=fig)

    with st.expander("... mais sous de multiples aspects"):
        fig = trajectoire_radar(date_debut, date_fin)

        st.plotly_chart(figure_or_data=fig)

    with st.expander("Mes accomplissements"):
        fig = accomplissements(date_debut, date_fin)

        st.plotly_chart(figure_or_data=fig)
