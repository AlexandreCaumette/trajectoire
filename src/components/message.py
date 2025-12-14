from typing import Literal

import streamlit as st


def message(message: str, type: Literal["error", "success", "warning", "info"]):
    if type == "error":
        st.error(body=message, icon="🚨")

    elif type == "success":
        st.success(body=message, icon="✅")

    elif type == "warning":
        st.warning(body=message, icon="⚠️")

    elif type == "info":
        st.info(body=message, icon="ℹ️")
