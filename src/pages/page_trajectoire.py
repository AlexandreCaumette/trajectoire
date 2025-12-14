import plotly.express as px
import plotly.graph_objects as go
import polars as pl
import streamlit as st

from src.data import data


def accomplissements() -> go.Figure:
    df: pl.DataFrame = st.session_state.df_contributions

    fig = px.bar(df, x="Date", y="Score", color="Catégorie")

    return fig


def trajectoire_lineaire() -> go.Figure:
    df_accomplissements: pl.DataFrame = st.session_state.df_contributions

    df_accomplissements = df_accomplissements.sort("Date")

    df_accomplissements = df_accomplissements.with_columns(
        pl.col("Score").cum_sum().alias("Score cumulé")
    )

    trace_reelle = go.Scatter(
        x=df_accomplissements["Date"],
        y=df_accomplissements["Score cumulé"],
        mode="lines",
        name="Ma trajectoire",
    )

    df_objectif = data.objectif()

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


def trajectoire_radar() -> go.Figure:
    fig = go.Figure()

    df_accomplissements: pl.DataFrame = st.session_state.df_contributions

    df_accomplissements = df_accomplissements.group_by("Catégorie").agg(pl.sum("Score"))

    df_objectif = data.objectif()

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

    st.subheader("Une trajectoire linéaire ...")

    fig = trajectoire_lineaire()

    st.plotly_chart(figure_or_data=fig)

    st.subheader("... mais sous de multiples aspects")

    fig = trajectoire_radar()

    st.plotly_chart(figure_or_data=fig)

    st.subheader("Mes accomplissements")

    fig = accomplissements()

    st.plotly_chart(figure_or_data=fig)
