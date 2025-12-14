import streamlit as st

from src.data import database
from src.pages.page_accomplissements import main_accomplissement
from src.pages.page_accueil import main_accueil
from src.pages.page_referentiel import main_referentiel
from src.pages.page_trajectoire import main_trajectoire


def main():
    st.title("Ma trajectoire annuelle")

    page_accomplissement = st.Page(
        page=main_accomplissement,
        title="Mes accomplissements",
        icon="🎉",
        url_path="accomplissements",
    )
    page_trajectoire = st.Page(
        page=main_trajectoire, title="Ma trajectoire", icon="🚀", url_path="trajectoire"
    )
    page_accueil = st.Page(
        page=main_accueil, title="Accueil", icon="🏡", default=True, url_path="accueil"
    )
    page_referentiel = st.Page(
        page=main_referentiel, title="Mon référentiel", icon="⚙️", url_path="referentiel"
    )

    pages = [
        page_accueil,
        page_referentiel,
    ]

    if "df_referentiel" not in st.session_state:
        database.fetch_user_referentiel()

    if "df_contributions" not in st.session_state:
        database.fetch_user_accomplissements()

    if not st.session_state.df_referentiel.is_empty():
        pages.append(page_accomplissement)

    if not st.session_state.df_contributions.is_empty():
        pages.append(page_trajectoire)

    current_page = st.navigation(pages=pages)

    current_page.run()


if __name__ == "__main__":
    main()
