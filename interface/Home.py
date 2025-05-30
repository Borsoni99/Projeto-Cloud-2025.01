import os
import sys

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
 
import streamlit as st
import requests
import json
from interface.config import Config

# Configure page settings
st.set_page_config(
    page_title="Trading Bot - Login",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit default menu and footer
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        .stDeployButton {display:none !important;}
        
        /* Hide all navigation elements */
        section[data-testid="stSidebarNav"] {display: none !important;}
        div[data-testid="stToolbar"] {display: none !important;}
        nav[data-testid="stSidebarNav"] {display: none !important;}
        div.sidebar-content {display: none !important;}
        div.sidebar .sidebar-content {display: none !important;}
        [data-testid="collapsedControl"] {display: none !important;}
        header[data-testid="stHeader"] {display: none !important;}
        div[data-testid="stDecoration"] {display: none !important;}
        div[data-testid="stSidebarNavItems"] {display: none !important;}
        button[kind="header"] {display: none !important;}
        div[data-baseweb="tab-list"] {display: none !important;}
        div[role="tablist"] {display: none !important;}
        div[data-testid="stSidebarNavContainer"] {display: none !important;}
        
        /* Title styling */
        .stMarkdown {
            text-align: center !important;
            font-size: 1.5rem !important;
            font-weight: bold !important;
            margin-bottom: 1rem !important;
            color: white !important;
            width: 320px !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        
        /* Remove padding and gap */
        .block-container {
            padding-top: 0;
            padding-bottom: 0;
            margin-top: 0;
        }
        
        /* Login form styles */
        .login-container {
            max-width: 380px;
            margin: 0 auto;
            padding: 32px;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
        }
        
        .login-container h1 {
            margin-bottom: 32px;
            text-align: center;
            font-size: 2rem;
            color: white;
            width: 320px;
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
            margin: 24px auto !important;
            width: 320px !important;
            border-color: rgba(255, 255, 255, 0.1) !important;
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
        
        /* Ensure consistent width for all markdown elements */
        .stMarkdown > div {
            width: 320px !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

def login_user(username, password):
    """Autentica o usuário na API"""
    try:
        response = requests.post(
            f'{Config.API_BASE_URL}/usuario/login',
            json={
                'usuario_login': username,
                'usuario_senha': password
            }
        )
        return response.json() if response.ok else None
    except requests.exceptions.RequestException:
        return None

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = None

# Login form
st.markdown('<div class="login-container">', unsafe_allow_html=True)

# Add title with robot icon
st.markdown("# 🤖 Trading Bot", unsafe_allow_html=True)

username = st.text_input("Usuário")
password = st.text_input("Senha", type="password")

if st.button("Entrar", type="primary", use_container_width=True):
    if not username or not password:
        st.warning("Por favor, preencha todos os campos")
    else:
        result = login_user(username, password)
        
        if result and not result.get('error'):
            st.session_state['logged_in'] = True
            st.session_state['user_data'] = result
            st.switch_page("pages/2_Dashboard.py")
        else:
            error_msg = result.get('error') if result else "Falha no login"
            st.error(error_msg)

st.markdown("---")
if st.button("Criar nova conta", use_container_width=True):
    st.switch_page("pages/_cadastro.py")

st.markdown('</div>', unsafe_allow_html=True) 