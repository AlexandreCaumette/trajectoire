import polars as pl
import streamlit as st

from src import logger
from src.components.message import message
from src.data import database
from src.models.exceptions import CustomException


def middleware_contribution(contribution: dict) -> dict:
    df_referentiel: pl.DataFrame = st.session_state["df_referentiel"]

    if "label" not in contribution:
        raise CustomException("Le label est absent de la contribution !")

    if df_referentiel.is_empty():
        return contribution

    if contribution["label"] in df_referentiel["Label"].unique().to_list():
        raise CustomException("Le label existe déjà dans le référentiel !")

    return contribution


def ajouter_nouvelle_contribution(contribution: dict):
    try:
        contribution = middleware_contribution(contribution)

        database.upsert_referentiel(contribution)

        message("La nouvelle contribution a bien été ajoutée !", "success")

        st.rerun()

    except CustomException as error:
        logger.error(error)

        message(str(error), "error")

    except Exception as error:
        logger.error(error)

        raise error


def form_referentiel():
    df_referentiel: pl.DataFrame = st.session_state["df_referentiel"]

    label = st.text_input(
        label="🏷️ Saisissez le label de la contribution :",
        placeholder="Séance d'escrime, Massage californien, etc.",
    )

    options_categorie = []

    if not df_referentiel.is_empty():
        if not df_referentiel.filter(pl.col("Label").eq(label)).is_empty():
            message(
                "Ce label d'accomplissement existe déjà, il faut en trouver un autre.",
                "warning",
            )

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

    else:
        message(
            "La fréquence par défaut associée à cette contribution sera 1 fois par an.",
            type="info",
        )

        contribution.update({"frequence": "1y"})

    st.divider()

    if st.button(label="Ajouter", icon="💾"):
        with st.spinner(
            show_time=True, text="Enregistrement de la nouvelle contribution..."
        ):
            ajouter_nouvelle_contribution(contribution)
