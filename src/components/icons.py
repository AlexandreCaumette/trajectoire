from typing import Literal


def icon(
    type: Literal[
        "label",
        "refresh",
        "download",
        "login",
        "logout",
        "mail",
        "password",
        "account_circle",
        "delete",
        "check_circle",
        "sports_score",
    ],
) -> str:
    return f":material/{type}:"
