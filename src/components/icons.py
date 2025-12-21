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
    ],
) -> str:
    return f":material/{type}:"
