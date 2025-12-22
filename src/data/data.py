import datetime as dt
import re

import polars as pl
import streamlit as st


@st.cache_data
def objectif(
    date_debut: dt.date | None = None,
    date_fin: dt.date | None = None,
    maille: str = "1d",
    agg_categorie: bool = False,
) -> pl.DataFrame:
    df_referentiel: pl.DataFrame = st.session_state.df_referentiel

    # Current year
    year = dt.date.today().year
    start = dt.date(year, 1, 1)
    end = dt.date(year, 12, 31)

    # Generate daily and weekly ranges
    daily_dates = pl.date_range(start, end, "1d", eager=True)
    weekly_dates = pl.date_range(start, end, "1w", eager=True)
    monthly_dates = pl.date_range(start, end, "1mo", eager=True)
    yearly_dates = pl.date_range(start, end, "1y", eager=True)

    # Function to expand based on FREQUENCY
    def expand_dates(freq: str):
        match = re.match(r"(\d+)([dwy]|mo)", freq)

        if not match:
            return []

        mult, unit = int(match.group(1)), match.group(2)

        if unit == "d":
            # Repeat each day 'mult' times
            return [d for d in daily_dates for _ in range(mult)]

        elif unit == "w":
            # Repeat each week 'mult' times
            return [d for d in weekly_dates for _ in range(mult)]

        elif unit == "mo":
            # Repeat each week 'mult' times
            return [d for d in monthly_dates for _ in range(mult)]

        elif unit == "y":
            # Repeat each week 'mult' times
            return [d for d in yearly_dates for _ in range(mult)]

        else:
            return []

    # Apply expansion
    df_referentiel = df_referentiel.with_columns(
        pl.col("Fréquence")
        .map_elements(expand_dates, return_dtype=pl.List(pl.Date))
        .alias("Date")
    )

    # Explode to duplicate rows
    df_referentiel = df_referentiel.explode("Date")

    df_referentiel = df_referentiel.sort("Date")

    if date_debut is not None and date_fin is not None:
        df_referentiel = df_referentiel.filter(
            pl.col("Date").is_between(date_debut, date_fin)
        )

    df_referentiel = df_referentiel.group_by_dynamic(
        index_column="Date", every=maille, group_by="Catégorie"
    ).agg(pl.sum("Score"))

    df_referentiel = df_referentiel.sort("Date")

    df_referentiel = df_referentiel.with_columns(
        pl.col("Score").cum_sum().alias("Score cumulé")
    )

    if agg_categorie:
        df_referentiel = df_referentiel.group_by("Catégorie").agg(
            pl.col("Score").sum(), pl.col("Score cumulé").last()
        )

    return df_referentiel


@st.cache_data
def realise(
    date_debut: dt.date | None = None,
    date_fin: dt.date | None = None,
    maille: str = "1d",
    agg_categorie: bool = False,
) -> pl.DataFrame:
    df: pl.DataFrame = st.session_state.df_contributions

    if date_debut is not None and date_fin is not None:
        df = df.filter(pl.col("Date").is_between(date_debut, date_fin))

    df = df.sort("Date")

    df = df.with_columns(pl.col("Score").cum_sum().alias("Score cumulé"))

    df = df.group_by_dynamic(
        index_column="Date", every=maille, group_by="Catégorie"
    ).agg(pl.sum("Score"), pl.sum("Score cumulé"))

    df = df.sort("Date")

    if agg_categorie:
        df = df.group_by("Catégorie").agg(
            pl.col("Score").sum(), pl.col("Score cumulé").last()
        )

    return df
