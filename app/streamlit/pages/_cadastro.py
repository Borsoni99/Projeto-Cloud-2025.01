import os
import sys

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, project_root)

import streamlit as st
import requests
import json
from app.config.config import Config

# Configure page settings
st.set_page_config(
    page_title="Trading Bot - Cadastro",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit default menu and footer
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        section[data-testid="stSidebarNav"] {display: none !important;}
        div[data-testid="stToolbar"] {display: none !important;}
        [data-testid="stSidebar"] {display: none !important;}
        header {visibility: hidden !important;}

        /* Remove padding and gap */
        .block-container {
            padding-top: 0;
            padding-bottom: 0;
            margin-top: 0;
        }
        
        /* Form styles */
        .register-container {
            max-width: 380px;
            margin: 0 auto;
            padding: 32px;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }
        
        .register-container h1 {
            margin-bottom: 32px;
            text-align: center;
            font-size: 2rem;
            color: white;
        }

        /* Force all elements to have the same width */
        .element-container, .stTextInput, div.row-widget.stButton {
            width: 320px !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        
        /* Input field styling */
        .stTextInput > div {
            width: 100% !important;
        }
        
        .stTextInput > div > div {
            background-color: rgb(28, 28, 28) !important;
            border-radius: 4px;
            padding: 8px 12px;
            color: white;
            width: 100% !important;
        }
        
        /* Base input styling */
        .stTextInput input {
            color: white !important;
            background-color: transparent !important;
            border: none !important;
            padding: 0 !important;
            width: 100% !important;
            min-height: 0 !important;
            box-shadow: none !important;
        }
        
        /* Password field container */
        div[data-baseweb="input"] {
            background-color: rgb(28, 28, 28) !important;
        }
        
        /* Password input field */
        div[data-baseweb="input"] input[type="password"] {
            color: white !important;
            background-color: transparent !important;
            border: none !important;
            padding: 0 !important;
            width: 100% !important;
            min-height: 0 !important;
            box-shadow: none !important;
        }
        
        /* Hide password toggle button container */
        div[data-baseweb="input"] div[role="button"],
        div[data-baseweb="input"] div[role="presentation"] {
            display: none !important;
        }
        
        /* Override any Streamlit base-web styling */
        div[data-baseweb="base-input"] {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        
        /* Focus state */
        .stTextInput > div > div:focus-within {
            border-color: #FF4B4B !important;
            box-shadow: 0 0 0 1px #FF4B4B;
        }

        div.stButton > button {
            height: 42px;
            border-radius: 4px;
            font-size: 14px;
            transition: all 0.2s;
            width: 100% !important;
        }

        div.stButton > button[kind="primary"] {
            background-color: #FF4B4B !important;
            color: white;
            border: none;
        }
        
        div.stButton > button[kind="primary"]:hover {
            background-color: #E43F3F !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        div.stButton > button:not([kind="primary"]) {
            background-color: transparent;
            color: #FAFAFA;
        }

        div.stButton > button:not([kind="primary"]):hover {
            background-color: rgba(255,255,255,0.1);
        }

        hr {
            margin: 24px auto;
            width: 320px !important;
        }

        /* Adjust input labels */
        .stTextInput label {
            color: rgba(250, 250, 250, 0.8);
            font-size: 0.9rem;
            text-align: left;
            width: 100% !important;
            margin-bottom: 4px;
        }

        /* Dark background */
        .stApp {
            background-color: #0E1117;
        }

        /* Fix any overflow issues */
        .stTextInput, .stButton, input {
            box-sizing: border-box !important;
        }
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

def register_user(username, password, binance_api_key=None, binance_secret_key=None):
    """Registra um novo usuário na API"""
    try:
        data = {
            'usuario_login': username,
            'usuario_senha': password,
        }
        
        if binance_api_key and binance_secret_key:
            data.update({
                'usuario_binanceApiKey': binance_api_key,
                'usuario_binanceSecretKey': binance_secret_key
            })

        response = requests.post(
            f'{Config.API_BASE_URL}/usuario',
            json=data
        )
        return response.json() if response.ok else None
    except requests.exceptions.RequestException:
        return None

# Registration form
st.markdown('<div class="register-container">', unsafe_allow_html=True)
st.title("🤖 Trading Bot")

username = st.text_input("Usuário")
password = st.text_input("Senha", type="password")
binance_api_key = st.text_input("Binance API Key (opcional)")
binance_secret_key = st.text_input("Binance Secret Key (opcional)")

if st.button("Criar Conta", type="primary", use_container_width=True):
    if not username or not password:
        st.warning("Por favor, preencha os campos obrigatórios")
    else:
        result = register_user(username, password, binance_api_key, binance_secret_key)
        if result and not result.get('error'):
            st.success("Conta criada com sucesso!")
            st.switch_page("Home.py")
        else:
            error_msg = result.get('error') if result else "Erro ao criar conta"
            st.error(error_msg)

st.markdown("---")
if st.button("Voltar para Login", use_container_width=True):
    st.switch_page("Home.py")

st.markdown('</div>', unsafe_allow_html=True)