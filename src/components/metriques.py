import datetime as dt

import streamlit as st

from src.data import data


def metrique_annuelle():
    df_objectif = data.objectif()
    df_realise = data.realise()

    score_objectif = df_objectif["Score"].sum()
    score_realise = df_realise["Score"].sum()
    ratio = score_realise / score_objectif

    st.metric(
        label="Progression annuelle",
        value=f"{score_realise} / {score_objectif} ({ratio:.1%})",
        border=True,
        help="Indicateur d'avancement prenant en compte tous vos accomplissements et tous vos objectifs du référentiel de l'année.",
    )


def metrique_a_date():
    date_debut = dt.date.today().replace(month=1, day=1)
    date_fin = dt.date.today()

    df_objectif = data.objectif(date_debut=date_debut, date_fin=date_fin)
    df_realise = data.realise(date_debut=date_debut, date_fin=date_fin)

    score_objectif = df_objectif["Score"].sum()
    score_realise = df_realise["Score"].sum()
    ratio = score_realise / score_objectif

    st.metric(
        label="Progression à date",
        value=f"{score_realise} / {score_objectif} ({ratio:.1%})",
        border=True,
        help="Indicateur d'avancement prenant en compte vos accomplissements et vos objectifs du référentiel jusqu'à aujourd'hui.",
    )
