import os
import sys

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, project_root)

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from app.config.config import Config
from app.streamlit.components.sidebar import show_sidebar

# Configure page settings
st.set_page_config(
    page_title="Trading Bot - Vender",
    page_icon="💸",
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

        /* Button styling */
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
    elif selected == "comprar ordem":
        st.switch_page("pages/comprar_ordem.py")

# Título da página
st.title("💸 Vender Ordem")

# Função para carregar ordens em aberto
def load_open_orders():
    try:
        response = requests.get(
            f'{Config.API_BASE_URL}/ordem/relatorios/{st.session_state["user_data"]["usuario_id"]}/abertos'
        )
        if response.status_code == 200:
            return response.json()['ordens_abertas']
        else:
            st.error(f"Erro ao carregar ordens: {response.json().get('error', 'Erro desconhecido')}")
            return []
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {str(e)}")
        return []

# Função para executar venda
def execute_sell_order(ordem_relatorio_id, simbolo, quantidade):
    try:
        data = {
            "simbolo": simbolo,
            "tp_operacao": "VENDA",
            "quantidade": quantidade,
            "tipo": "MERCADO",
            "ordem_relatorio_id": ordem_relatorio_id
        }
        
        response = requests.post(
            f'{Config.API_BASE_URL}/ordem/{st.session_state["user_data"]["usuario_id"]}',
            json=data
        )
        
        if response.status_code == 201:
            st.success("✅ Venda executada com sucesso!")
            st.rerun()  # Recarrega a página para atualizar a lista
        else:
            st.error(f"Erro ao executar venda: {response.json().get('error', 'Erro desconhecido')}")
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {str(e)}")

# Carregar ordens em aberto
ordens_abertas = load_open_orders()

if not ordens_abertas:
    st.info("📝 Você não possui ordens em aberto para vender.")
else:
    # Criar DataFrame com as ordens
    df = pd.DataFrame(ordens_abertas)
    
    # Formatar colunas
    df['quantidade'] = df['quantidade'].apply(lambda x: f"{x:.8f}")
    df['preco_compra'] = df['preco_compra'].apply(lambda x: f"${x:,.2f}")
    
    # Exibir tabela de ordens
    st.subheader("📊 Ordens em Aberto")
    
    # Inicializar estado de confirmação se não existir
    if 'confirmar_venda' not in st.session_state:
        st.session_state.confirmar_venda = None
    
    # Exibir tabela
    for index, row in df.iterrows():
        with st.container():
            cols = st.columns([2, 2, 2, 2, 2, 1])
            cols[0].write(row['moeda'])
            cols[1].write(row['quantidade'])
            cols[2].write(row['preco_compra'])
            cols[3].write(row['data_operacao'])
            cols[4].write(row['status'])
            
            # Botão de venda
            ordem_id = row['id']
            
            if st.session_state.confirmar_venda == ordem_id:
                # Mostrar botões de confirmar e cancelar
                col_confirm, col_cancel = cols[5].columns(2)
                if col_confirm.button("✅", key=f"confirm_{ordem_id}"):
                    execute_sell_order(
                        ordem_relatorio_id=ordem_id,
                        simbolo=row['moeda'],
                        quantidade=float(row['quantidade'].replace(',', ''))
                    )
                    st.session_state.confirmar_venda = None
                
                if col_cancel.button("❌", key=f"cancel_{ordem_id}"):
                    st.session_state.confirmar_venda = None
                    st.rerun()
            else:
                # Mostrar botão de venda
                if cols[5].button("Vender", key=f"vender_{ordem_id}"):
                    st.session_state.confirmar_venda = ordem_id
                    st.rerun()
    
    # Adicionar informações adicionais
    st.markdown("---")
    st.markdown("""
        ### ℹ️ Informações
        - As vendas são executadas a mercado para garantir a execução imediata
        - O preço de venda será o preço atual do mercado
        - A venda será executada com a quantidade total da ordem
    """) 