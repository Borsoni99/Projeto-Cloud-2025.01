import os
import sys

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, project_root)

import streamlit as st
import requests
from decimal import Decimal
from app.config.config import Config
from app.streamlit.components.sidebar import show_sidebar

# Configure page settings
st.set_page_config(
    page_title="Trading Bot - Comprar",
    page_icon="💰",
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
        
        /* Main content button styling */
        div[data-testid="baseButton-secondary"] {
            background-color: #FF4B4B !important;
            color: white !important;
            border: none !important;
            padding: 8px 16px !important;
            border-radius: 4px !important;
            font-weight: 600 !important;
            transition: all 0.2s !important;
        }
        
        div[data-testid="baseButton-secondary"]:hover {
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
    elif selected == "configurações":
        st.switch_page("pages/usuario_config.py")
    elif selected == "moedas ativas":
        st.switch_page("pages/moedas_ativas.py")

def get_active_pairs():
    """Obtém os pares ativos do usuário"""
    try:
        response = requests.get(
            f'{Config.API_BASE_URL}/moedas_ativas/{st.session_state["user_data"]["usuario_id"]}'
        )
        if response.ok:
            data = response.json()
            return [moeda['simbolo'] for moeda in data.get('moedas', [])]
        return []
    except Exception as e:
        st.error(f"Erro ao carregar pares ativos: {str(e)}")
        return []

def create_market_order(symbol, quantity):
    """Cria uma ordem de mercado"""
    try:
        # Converter quantidade para string com 8 casas decimais
        quantity_str = f"{quantity:.8f}"
        
        # Log para debug
        st.write("Enviando requisição com dados:")
        st.write({
            'simbolo': symbol,
            'tp_operacao': 'COMPRA',
            'quantidade': quantity_str,
            'tipo': 'MERCADO'
        })
        
        response = requests.post(
            f'{Config.API_BASE_URL}/ordem/{st.session_state["user_data"]["usuario_id"]}',
            json={
                'simbolo': symbol,
                'tp_operacao': 'COMPRA',
                'quantidade': quantity_str,
                'tipo': 'MERCADO'
            }
        )
        
        # Log da resposta para debug
        if not response.ok:
            st.write(f"Erro na resposta: {response.status_code}")
            st.write(f"Conteúdo da resposta: {response.text}")
            
        return response.json() if response.ok else None
    except Exception as e:
        st.error(f"Erro ao criar ordem: {str(e)}")
        return None

st.title("💰 Comprar")

# Carregar pares ativos
active_pairs = get_active_pairs()

if not active_pairs:
    st.warning("Você não possui moedas ativas. Adicione moedas na página 'Moedas Ativas' primeiro.")
else:
    # Formulário de compra
    with st.form("buy_form"):
        # Seleção do par de trading
        selected_pair = st.selectbox(
            "Selecione o Par de Trading",
            options=active_pairs,
            format_func=lambda x: x
        )
        
        # Campo de quantidade
        quantity = st.number_input(
            "Quantidade",
            min_value=0.0,
            step=0.0001,
            format="%.4f"
        )
        
        # Botão de compra
        submitted = st.form_submit_button("Comprar")
        
        if submitted:
            if quantity <= 0:
                st.error("A quantidade deve ser maior que zero.")
            else:
                # Criar ordem de mercado
                result = create_market_order(selected_pair, quantity)
                
                if result and not result.get('error'):
                    st.success(f"Ordem de compra criada com sucesso para {quantity} {selected_pair}!")
                    
                    # Mostrar detalhes da ordem
                    st.write("Detalhes da Ordem:")
                    st.json({
                        'Símbolo': result.get('simbolo'),
                        'Quantidade Executada': float(result.get('qtd_executada', 0)),
                        'Preço Médio': float(result.get('preco', 0)),
                        'Status': result.get('status'),
                        'Tipo': result.get('tipo')
                    })
                else:
                    st.error(f"Erro ao criar ordem: {result.get('error') if result else 'Erro desconhecido'}") 