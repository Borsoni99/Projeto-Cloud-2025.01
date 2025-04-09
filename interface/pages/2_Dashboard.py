import os
import sys

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

import streamlit as st
from interface.components.sidebar import show_sidebar

# Configure page settings
st.set_page_config(
    page_title="Trading Bot - Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

# Hide Streamlit default menu and footer
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}

        /* Hide only the default navigation */
        section[data-testid="stSidebarNav"] {display: none !important;}
        div[data-testid="stSidebarNav"] {display: none !important;}

        /* Dark theme and general styles */
        .stApp {
            background-color: #0E1117;
        }

        h1, h2, h3, h4, h5, h6 {
            color: white;
        }

        p {
            color: rgba(250, 250, 250, 0.8);
        }

        /* Card styling */
        div[data-testid="stHorizontalBlock"] > div {
            background-color: rgb(28, 28, 28);
            border-radius: 8px;
            padding: 16px;
            margin: 8px;
        }
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Verificar se o usuário está logado
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.switch_page("Home.py")

# Show sidebar
selected = show_sidebar()
if selected:
    if selected == "configurações":
        st.switch_page("pages/usuario_config.py")
    elif selected == "moedas ativas":
        st.switch_page("pages/moedas_ativas.py")
    elif selected == "comprar ordem":
        st.switch_page("pages/comprar_ordem.py")
    elif selected == "vender ordem":
        st.switch_page("pages/vender_ordem.py")

st.title("📊 Dashboard")

# Add BI Dashboard button and embedded dashboard
st.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <a href=https://app.powerbi.com/groups/me/reports/efb1b5bf-d4af-423c-a201-dd0a843c1540/9659a5494202205bc821?ctid=da49a844-e2e3-40af-86a6-c3819d704f49&experience=power-bi" target="_blank">
        <button style="background-color: #1E88E5; color: white; padding: 12px 24px; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: 500; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); transition: all 0.3s ease;">
            <span style="display: inline-block; vertical-align: middle;">📊 Open BI Dashboard in New Tab</span>
        </button>
    </a>
</div>
""", unsafe_allow_html=True)

# Embedded Power BI Dashboard
st.markdown("### 📈 Power BI Dashboard")
st.markdown("""
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; margin-bottom: 20px;">
    <iframe src="https://app.powerbi.com/reportEmbed?reportId=efb1b5bf-d4af-423c-a201-dd0a843c1540&autoAuth=true&ctid=da49a844-e2e3-40af-86a6-c3819d704f49"
            frameborder="0"
            allowFullScreen="true"
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
    </iframe>
</div>
""", unsafe_allow_html=True)