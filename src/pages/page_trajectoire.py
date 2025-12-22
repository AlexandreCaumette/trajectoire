import datetime as dt
import math

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
    df_accomplissements = data.realise(date_debut, date_fin, maille)

    trace_reelle = go.Scatter(
        x=df_accomplissements["Date"],
        y=df_accomplissements["Score cumulé"],
        mode="lines",
        name="Ma trajectoire",
        marker_color="#04E7FF",
    )

    df_objectif = data.objectif(date_debut, date_fin, maille)

    trace_theorique = go.Scatter(
        x=df_objectif["Date"],
        y=df_objectif["Score cumulé"],
        mode="lines",
        name="Mon objectif",
        marker_color="#1562BC",
    )

    fig = go.Figure()

    fig.add_trace(trace_reelle)

    fig.add_trace(trace_theorique)

    fig.update_layout(
        xaxis=dict(title=dict(text="Date")),
        yaxis=dict(title=dict(text="Score cumulé")),
        legend=dict(title=dict(text="Avancement")),
    )

    return fig


def trajectoire_radar(date_debut: dt.date, date_fin: dt.date, maille: str) -> go.Figure:
    fig = go.Figure()

    df_accomplissements = data.realise(date_debut, date_fin, maille, agg_categorie=True)

    df_objectif = data.objectif(date_debut, date_fin, agg_categorie=True)

    df = df_objectif.join(
        df_accomplissements, on="Catégorie", how="left", suffix="_reel"
    )

    df = df.with_columns((pl.col("Score_reel") / pl.col("Score")).alias("Ratio"))

    df = df.sort("Catégorie")

    def value_to_hex(normalized_value: float) -> str:
        if normalized_value <= 0.2:
            return "#1562BC"

        if normalized_value <= 0.4:
            return "#04E7FF"

        if normalized_value <= 0.8:
            return "#FE8411"

        if normalized_value > 0.8:
            return "#F85027"

        return "#FFFFFF"

    colors = [value_to_hex(ratio) for ratio in df["Ratio"]]

    def value_to_width(normalized_value: float, n_categorie: int) -> float:
        # L'ouverture minimale pour une catégorie est 22.5°
        min_width = math.pi / 8

        # Le ratio de la catégorie permet de gagner entre 0 et 11.225°
        ratio_width = math.pi / 16 * normalized_value

        total_width = min_width + ratio_width

        max_width = 2 * math.pi / n_categorie

        return min(total_width, max_width)

    n_categorie = df["Catégorie"].n_unique()

    widths = [value_to_width(ratio, n_categorie) for ratio in df["Ratio"]]

    fig.add_trace(
        go.Barpolar(
            r=df["Ratio"],
            theta=df["Catégorie"],
            width=widths,
            marker_color=colors,
            marker_line_color="black",
            marker_line_width=2,
            opacity=0.8,
            # Custom hover template
            hovertemplate=(
                "Catégorie : <b>%{theta}</b><br>"
                + "Accomplissement : <b>%{r:.1%}<b><br>"
                + "<extra></extra>"  # Removes the trace name from hover
            ),
        )
    )

    # Set dark background
    fig.update_layout(
        polar=dict(
            bgcolor="darkslategray",
            radialaxis=dict(
                ticksuffix="%",  # Add % sign to ticks
                tickvals=[0.2, 0.4, 0.6, 0.8, 1.0],  # Set tick positions
                ticktext=["20%", "40%", "60%", "80%", "100%"],
                gridcolor="gray",
                linewidth=1,
            ),
            angularaxis=dict(
                gridcolor="gray",
                linewidth=1,
            ),
        ),
    )

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
        fig = trajectoire_radar(date_debut, date_fin, maille)

        st.plotly_chart(figure_or_data=fig)

    with st.expander("Mes accomplissements"):
        fig = accomplissements(date_debut, date_fin)

        st.plotly_chart(figure_or_data=fig)
