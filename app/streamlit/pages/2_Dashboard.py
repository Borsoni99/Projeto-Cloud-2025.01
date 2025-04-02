import os
import sys

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, project_root)

import streamlit as st
from app.streamlit.components.sidebar import show_sidebar

# Configure page settings
st.set_page_config(
    page_title="Trading Bot - Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit default menu and footer
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        section[data-testid="stSidebarNav"] {display: none !important;}
        div[data-testid="stToolbar"] {display: none !important;}
        
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

st.title("📊 Dashboard")

# Layout em colunas para os cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 💰 Saldo")
    st.markdown("R$ 1.000,00")

with col2:
    st.markdown("### 📈 Lucro Total")
    st.markdown("R$ 250,00")

with col3:
    st.markdown("### 🎯 Operações")
    st.markdown("15 operações realizadas")

# Gráficos e tabelas
st.markdown("### 📊 Histórico de Operações")
st.markdown("Em desenvolvimento...") 