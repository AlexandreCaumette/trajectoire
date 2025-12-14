import polars as pl
import streamlit as st
from supabase import Client, create_client

from src import logger

SCHEMA_CONTRIBUTIONS = {
    "Label": pl.String,
    "Catégorie": pl.String,
    "Score": pl.Float32,
    "Date": pl.Date,
}

SCHEMA_REFERENTIEL = {
    "Label": pl.String,
    "Catégorie": pl.String,
    "Score": pl.Float32,
    "Echéance": pl.Date,
    "Fréquence": pl.String,
}


@st.cache_resource
def init_database_connection() -> Client:
    try:
        logger.info("Tentative de connexion à la base de données.")

        url: str = st.secrets.supabase_credentials.get("SUPABASE_URL", "")
        key: str = st.secrets.supabase_credentials.get("SUPABASE_KEY", "")

        connection: Client = create_client(url, key)

        logger.info("Connexion à la base de données réussie.")

        return connection

    except Exception as error:
        logger.error(error)

        raise error


def fetch_user_referentiel():
    try:
        logger.debug("Extraction du référentiel.")

        connection = init_database_connection()

        response = (
            connection.table("referentiel")
            .select("id, label, categorie, score, echeance, frequence")
            .execute()
        )

        data = response.data

        df = pl.DataFrame(data=data)

        if not df.is_empty():
            df = df.rename(
                {
                    "label": "Label",
                    "categorie": "Catégorie",
                    "score": "Score",
                    "echeance": "Echéance",
                    "frequence": "Fréquence",
                }
            )

        st.session_state["df_referentiel"] = df

    except Exception as error:
        logger.error(error)

        raise error


def fetch_user_accomplissements():
    try:
        logger.debug("Extraction des accomplissements.")

        connection = init_database_connection()

        response = (
            connection.table("accomplissements")
            .select("id, label, categorie, score, date")
            .execute()
        )

        data = response.data

        df = pl.DataFrame(data=data)

        if not df.is_empty():
            df = df.rename(
                {
                    "label": "Label",
                    "categorie": "Catégorie",
                    "score": "Score",
                    "date": "Date",
                }
            )

        df = df.with_columns(
            pl.col("Date").str.strptime(dtype=pl.Date, format="%Y-%m-%d")
        )

        st.session_state["df_contributions"] = df

    except Exception as error:
        logger.error(error)

        raise error


def get_user_id() -> str:
    if "user" not in st.session_state:
        return ""

    return st.session_state.user.id


def upsert_referentiel(payload: dict):
    try:
        logger.debug("UPSERT d'un élément dans le référentiel.")

        connection = init_database_connection()

        payload["id_user"] = get_user_id()

        connection.table("referentiel").insert(json=payload).execute()

        logger.debug("INSERT réussi.")

        fetch_user_referentiel()

    except Exception as error:
        logger.error(error)

        raise error


def upsert_accomplissement(payload: dict):
    try:
        logger.debug("UPSERT d'un élément dans les accomplissements.")

        connection = init_database_connection()

        payload["id_user"] = get_user_id()

        print(payload)

        connection.table("accomplissements").insert(json=payload).execute()

        logger.debug("INSERT réussi.")

        fetch_user_accomplissements()

    except Exception as error:
        logger.error(error)

        raise error


def signin_user(email: str, password: str):
    try:
        logger.debug("Tentative de connexion.")

        connection = init_database_connection()

        response = connection.auth.sign_in_with_password(
            {
                "email": email,
                "password": password,
            }
        )

        st.session_state["user"] = response.user

        logger.debug("Connexion réussie.")

    except Exception as error:
        logger.error(error)

        raise error


def signup_user(email: str, password: str):
    try:
        logger.debug("Tentative de création de compte.")

        connection = init_database_connection()

        connection.auth.sign_up(
            {
                "email": email,
                "password": password,
            }
        )

        logger.debug("Création de compte réussie.")

    except Exception as error:
        logger.error(error)

        raise error
