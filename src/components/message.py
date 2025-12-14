from typing import Literal

import streamlit as st


def message(message: str, type: Literal["error", "success", "warning"]):
    if type == "error":
        st.error(body=message, icon="🚨")

    elif type == "success":
        st.success(body=message, icon="✅")

    elif type == "warning":
        st.warning(body=message, icon="⚠️")
