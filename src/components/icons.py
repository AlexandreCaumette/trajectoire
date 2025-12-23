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
        "reset_settings",
        "home",
    ],
) -> str:
    return f":material/{type}:"
