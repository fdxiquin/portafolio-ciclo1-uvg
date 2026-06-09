from __future__ import annotations

import streamlit as st


st.set_page_config(
    page_title="Portafolio | Daniel Fernando Xiquin Tezén",
    page_icon="DX",
    layout="wide",
    initial_sidebar_state="expanded",
)


pages = [
    st.Page("views/inicio.py", title="Inicio", icon=":material/home:", default=True),
    st.Page("views/portafolio.py", title="Portafolio académico", icon=":material/folder:"),
    st.Page("views/primer_ciclo.py", title="Mi primer ciclo en UVG", icon=":material/school:"),
]


navigation = st.navigation(pages)
navigation.run()
