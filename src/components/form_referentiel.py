import polars as pl
import streamlit as st

from src import logger
from src.components.message import message
from src.models import models


def ajouter_nouvelle_contribution(contribution: dict):
    try:
        row = [
            contribution.get("label", None),
            contribution.get("categorie", None),
            contribution.get("score", None),
            contribution.get("echeance", None),
            contribution.get("frequence", None),
        ]

        nouvelle_contribution = pl.DataFrame(
            data=[row],
            schema=models.SCHEMA_REFERENTIEL,
        )

        df_referentiel = st.session_state["df_referentiel"]

        st.session_state["df_referentiel"] = pl.concat(
            [df_referentiel, nouvelle_contribution]
        )

        logger.info("Nouvelle contribution ajoutée au référentiel.")

        st.rerun()

        message("La nouvelle contribution a bien été ajoutée !", "success")

    except Exception as error:
        logger.error(error)

        message("Une erreur est survenue et a empêché l'ajout.", "error")


def form_referentiel():
    label = st.text_input(
        label="🏷️ Saisissez le label de la contribution :",
        placeholder="Séance d'escrime, Massage californien, etc.",
    )

    df_referentiel: pl.DataFrame = st.session_state["df_referentiel"]

    options_categorie = df_referentiel["Catégorie"].unique().sort().to_list()

    default_categories = ["Sport", "Santé", "Relation", "Culture"]

    options_categorie = list(set(options_categorie + default_categories))

    categorie = st.selectbox(
        label="🗂️ Sélectionner la catégorie de la contribution :",
        options=options_categorie,
        accept_new_options=True,
    )

    score = st.number_input(
        label="💯 Saisissez le score de la contribution :", min_value=0, step=5
    )

    contribution = {"score": score, "categorie": categorie, "label": label}

    st.divider()

    afficher_frequence = st.toggle(
        label="Paramétrer une fréquence théorique d'accomplissement ?",
        value=False,
    )

    if afficher_frequence:
        quantite = st.number_input(
            label="Sélectionner la quantité associée à la fréquence :",
            min_value=0,
            value=1,
            step=1,
        )

        dict_options = {
            f"{quantite} par jour": f"{quantite}d",
            f"{quantite} par semaine": f"{quantite}w",
            f"{quantite} par mois": f"{quantite}mo",
            f"{quantite} par année": f"{quantite}y",
        }

        options_frequence = dict_options.keys()

        frequence = st.radio(
            label="Sélectionner la fréquence d'accomplissement théorique :",
            options=options_frequence,
        )

        frequence = dict_options.get(frequence, "y")

        echeance = st.date_input(
            label="📅 Saisissez l'échéance de la contribution :",
            format="DD/MM/YYYY",
            value=None,
            help="Laisser la date vide si la contribution n'a pas d'échéance particulière.",
        )

        contribution.update({"frequence": frequence, "echeance": echeance})

    st.divider()

    if st.button(label="Ajouter", icon="💾"):
        with st.spinner(
            show_time=True, text="Enregistrement de la nouvelle contribution..."
        ):
            ajouter_nouvelle_contribution(contribution)
