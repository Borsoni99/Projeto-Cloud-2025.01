import os
import sys

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

import streamlit as st
import requests
from interface.config import Config
from interface.components.sidebar import show_sidebar

# Configure page settings
st.set_page_config(
    page_title="Trading Bot - Configurações",
    page_icon="🤖",
    layout="centered",
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

        /* Input field styling */
        .stNumberInput > div > div > div {
            background-color: rgb(28, 28, 28) !important;
            border-radius: 4px !important;
            border: none !important;
            padding: 8px 12px !important;
            color: white !important;
        }
        
        .stNumberInput input {
            color: white !important;
            background-color: transparent !important;
            border: none !important;
        }

        /* Remove borders and background from increment/decrement buttons */
        .stNumberInput > div > div > div:nth-child(2) > div {
            background: none !important;
            border: none !important;
            color: white !important;
        }

        .stNumberInput > div > div > div:nth-child(2) > div:hover {
            color: #FF4B4B !important;
        }
        
        /* Main content button styling - Only for the form button */
        div[data-testid="stForm"] div[data-testid="baseButton-secondary"] {
            background-color: #FF4B4B !important;
            color: white !important;
            border: none !important;
            padding: 8px 16px !important;
            border-radius: 4px !important;
            font-weight: 600 !important;
            transition: all 0.2s !important;
        }
        
        div[data-testid="stForm"] div[data-testid="baseButton-secondary"]:hover {
            background-color: #E43F3F !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }

        /* Center title */
        h1 {
            text-align: center;
            margin-bottom: 2rem;
        }

        /* Adjust spacing */
        .stNumberInput {
            margin-bottom: 1.5rem;
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
    if selected == "dashboard":
        st.switch_page("pages/2_Dashboard.py")
    elif selected == "moedas ativas":
        st.switch_page("pages/moedas_ativas.py")
    elif selected == "comprar ordem":
        st.switch_page("pages/comprar_ordem.py")

def get_user_config():
    """Obtém as configurações do usuário"""
    try:
        response = requests.get(
            f'{Config.API_BASE_URL}/usuario/{st.session_state["user_data"]["usuario_id"]}/config'
        )
        return response.json() if response.ok else None
    except requests.exceptions.RequestException:
        return None

def update_user_config(valor_compra, pct_ganho, pct_perda):
    """Atualiza as configurações do usuário"""
    try:
        response = requests.put(
            f'{Config.API_BASE_URL}/usuario/{st.session_state["user_data"]["usuario_id"]}/config',
            json={
                'valor_compra': valor_compra,
                'pct_ganho': pct_ganho,
                'pct_perda': pct_perda
            }
        )
        return response.json() if response.ok else None
    except requests.exceptions.RequestException:
        return None

# Carregar configurações atuais
config = get_user_config()

st.title("⚙️ Configurações")

# Formulário de configurações
with st.form("config_form"):
    valor_compra = st.number_input(
        "Valor de Compra (R$)",
        min_value=1.0,
        max_value=10000.0,
        value=float(config['valor_compra']) if config else 5.0,
        step=1.0,
        format="%.2f"
    )
    
    pct_ganho = st.number_input(
        "Porcentagem de Ganho (%)",
        min_value=0.1,
        max_value=100.0,
        value=float(config['pct_ganho']) if config else 10.0,
        step=0.1,
        format="%.1f"
    )
    
    pct_perda = st.number_input(
        "Porcentagem de Perda (%)",
        min_value=0.1,
        max_value=100.0,
        value=float(config['pct_perda']) if config else 10.0,
        step=0.1,
        format="%.1f"
    )
    
    submitted = st.form_submit_button("Salvar Configurações")
    
    if submitted:
        result = update_user_config(valor_compra, pct_ganho, pct_perda)
        if result and not result.get('error'):
            st.success("Configurações atualizadas com sucesso!")
        else:
            st.error(result.get('error') if result else "Erro ao atualizar configurações") 