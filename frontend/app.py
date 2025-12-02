import streamlit as st
from pages import homepage

st.set_page_config(
    page_title="SummAIze",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS global
st.markdown("""
    <style>
        html, body {
            margin: 0 !important;
            padding: 0 !important;
            height: 100% !important;
            overflow: hidden !important;
        }

        .stApp {
            padding: 0 !important;
            margin: 0 !important;
            background-color: white !important;
        }

        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewBlockContainer"],
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }

        /* Esconder header e footer padrão */
        header { display: none !important; }
        footer { display: none !important; }

        /* Esconder toolbar */
        [data-testid="stToolbar"] { display: none !important; }

        /* Esconder sidebar */
        section[data-testid="stSidebar"] {
            display: none !important;
        }

        /* ESSE é o botão da seta (toggle do sidebar) */
        [data-testid="collapsedControl"] {
            display: none !important;
        }

        /* Se quiseres ainda esconder o deploy / running, etc., podes adicionar:
        .stDeployButton { visibility: hidden; }
        [data-testid="stStatusWidget"] { visibility: hidden; }
        */
    </style>
""", unsafe_allow_html=True)

homepage.show()
