import datetime as dt

import polars as pl
import streamlit as st

from src import logger
from src.components.icons import icon
from src.components.message import message
from src.data import database


def accomplir_une_contribution(accomplissement: dict):
    try:
        accomplissement["date"] = accomplissement["date"].isoformat()

        database.upsert_accomplissement(accomplissement)

        st.rerun()

    except Exception as error:
        logger.error(error)

        message("Une erreur est survenue.", "error")

        raise error


def form_accomplissement():
    df_referentiel: pl.DataFrame = st.session_state["df_referentiel"]

    options_evenement = df_referentiel["Label"].sort().to_list()

    label = st.selectbox(
        label="🗂️ Sélectionner la contribution :",
        options=options_evenement,
    )

    contribution = df_referentiel.filter(pl.col("Label").eq(label))

    categorie: str = contribution["Catégorie"].first()

    score_par_defaut: float = contribution["Score"].mean()

    score = st.number_input(
        label="Valider le chiffrage de la contribution :",
        disabled=label is None,
        min_value=0.0,
        value=score_par_defaut,
        icon=icon("sports_score"),
        help="Le score du référentiel est pris par défaut, mais vous pouvez estimer que le chiffrage réel de cet accomplissement est différent.",
    )

    date_par_defaut = contribution["Echéance"].min()

    if date_par_defaut is None:
        date_par_defaut: str = "today"

    date = st.date_input(
        label="📅 Sélectionner la date d'accomplissement :",
        value=date_par_defaut,
        min_value=dt.date.today().replace(month=1, day=1),
        max_value=dt.date.today(),
        help="L'accomplissement peut avoir eu lieu dans le passé ou aujourd'hui, mais pas dans le futur.",
    )

    accomplissement = {
        "label": label,
        "categorie": categorie,
        "score": score,
        "date": date,
    }

    st.divider()

    if st.button(
        label="Ajouter l'accomplissement",
        disabled=label is None,
        icon=icon("check_circle"),
        type="primary",
    ):
        with st.spinner(show_time=True, text="Enregistrement de l'accomplissement..."):
            accomplir_une_contribution(accomplissement)
