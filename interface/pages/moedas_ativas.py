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
    page_title="Trading Bot - Moedas Ativas",
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

        /* Search input styling */
        .stTextInput > div > div {
            background-color: rgb(28, 28, 28) !important;
            border-radius: 4px;
            padding: 8px 12px;
            color: white;
        }
        
        .stTextInput input {
            color: white !important;
            background-color: transparent !important;
            border: none !important;
        }

        /* Multiselect styling */
        .stMultiSelect > div[data-baseweb="select"] {
            background-color: rgb(28, 28, 28) !important;
            border-radius: 4px;
        }

        .stMultiSelect div[role="listbox"] {
            background-color: rgb(28, 28, 28) !important;
        }

        .stMultiSelect [data-testid="stMarkdownContainer"] p {
            color: white !important;
        }

        /* Button styling - Only for main content buttons */
        div[data-testid="column"] .stButton > button {
            background-color: #FF4B4B !important;
            color: white !important;
            border: none !important;
            padding: 8px 16px !important;
            border-radius: 4px !important;
            font-weight: 600 !important;
            transition: all 0.2s !important;
            width: 100% !important;
        }
        
        div[data-testid="column"] .stButton > button:hover {
            background-color: #E43F3F !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }

        /* Center title */
        h1 {
            text-align: center;
            margin-bottom: 2rem;
        }

        /* Adjust spacing */
        .stTextInput, .stMultiSelect {
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
    elif selected == "comprar ordem":
        st.switch_page("pages/comprar_ordem.py")

def get_trading_pairs():
    """Obtém todos os pares de trading disponíveis na Binance"""
    try:
        response = requests.get(f'{Config.API_BASE_URL}/moedas_ativas/trading-pairs')
        if response.ok:
            data = response.json()
            return data.get('trading_pairs', []) 
        else:
            return []
    except Exception as e:
        return []

def create_moeda_ativa(simbolos):
    """Cria moedas ativas para o usuário"""
    try:
        response = requests.post(
            f'{Config.API_BASE_URL}/moedas_ativas/{st.session_state["user_data"]["usuario_id"]}',
            json={'simbolos': simbolos}
        )
        return response.ok, response.json()
    except:
        return False, {'error': 'Erro ao criar moedas ativas'}

def delete_moeda_ativa(moeda_id):
    """Deleta uma moeda ativa do usuário"""
    try:
        response = requests.delete(
            f'{Config.API_BASE_URL}/moedas_ativas/{st.session_state["user_data"]["usuario_id"]}/{moeda_id}'
        )
        return response.ok, response.json()
    except:
        return False, {'error': 'Erro ao deletar moeda ativa'}

# Título da página
st.title("💰 Moedas Ativas")

# Carregar pares de trading disponíveis
if 'trading_pairs' not in st.session_state:
    st.session_state['trading_pairs'] = get_trading_pairs()

# Multiselect com filtro de texto
selected_pairs = st.multiselect(
    "Selecione os pares de trading",
    options=st.session_state['trading_pairs'],
    key="selected_pairs"
)

# Adicionar espaço antes do botão
st.write("")

# Criar três colunas com a do meio menor para o botão
col1, col2, col3 = st.columns([2, 3, 2])
with col2:
    # Botão para salvar
    if st.button("💾 Salvar Moedas Selecionadas", use_container_width=True):
        if selected_pairs:
            success, result = create_moeda_ativa(selected_pairs)
            if success:
                st.success("Moedas ativas criadas com sucesso!")
                # Forçar recarregamento das moedas ativas
                st.session_state['active_pairs'] = None
                # Recarregar a página para limpar a seleção
                st.rerun()
            else:
                st.error(f"Erro ao criar moedas ativas: {result.get('error', 'Erro desconhecido')}")
        else:
            st.warning("Por favor, selecione pelo menos uma moeda.")

# Seção de Moedas Ativas
st.subheader("📊 Moedas Ativas Atuais")

# Carregar moedas ativas do usuário
try:
    response = requests.get(f'{Config.API_BASE_URL}/moedas_ativas/{st.session_state["user_data"]["usuario_id"]}')
    if response.ok:
        data = response.json()
        active_pairs = data.get('moedas', [])
        total = data.get('total', 0)
        
        # Exibir total de moedas ativas
        st.write(f"Total de moedas ativas: {total}")
        
        # Exibir moedas ativas
        if active_pairs:
            # Criar um DataFrame para melhor visualização
            import pandas as pd
            df = pd.DataFrame(active_pairs)
            df.columns = ['ID', 'Símbolo', 'Último Preço']
            
            # Formatar o preço para formato monetário em dólar com 2 casas decimais
            df['Último Preço'] = df['Último Preço'].apply(lambda x: f"${x:,.2f}")
            
            # Criar DataFrame para exibição (sem o ID)
            display_df = df[['Símbolo', 'Último Preço']].copy()
            
            # Estilizar o DataFrame
            st.dataframe(
                display_df,
                hide_index=True,
                column_config={
                    "Símbolo": st.column_config.TextColumn(
                        "Símbolo",
                        help="Par de trading",
                        width="medium"
                    ),
                    "Último Preço": st.column_config.TextColumn(
                        "Último Preço (USD)",
                        help="Preço atual da moeda em dólar",
                        width="medium"
                    )
                }
            )
            
            # Adicionar botões de exclusão abaixo da tabela
            st.subheader("Excluir Moeda")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                moeda_to_delete = st.selectbox(
                    "Selecione a moeda para excluir",
                    options=df['Símbolo'].tolist(),
                    key="moeda_to_delete"
                )
            
            with col2:
                # Adicionar espaço em branco para alinhar com o label do selectbox
                st.write("")
                st.write("")
                # Botão agora estará alinhado com o selectbox
                if st.button("🗑️ Excluir Moeda", key="delete_button", use_container_width=True):
                    # Encontrar o ID da moeda selecionada
                    moeda_id = df[df['Símbolo'] == moeda_to_delete]['ID'].iloc[0]
                    success, result = delete_moeda_ativa(moeda_id)
                    if success:
                        st.success(f"Moeda {moeda_to_delete} excluída com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"Erro ao excluir moeda: {result.get('error', 'Erro desconhecido')}")
        else:
            st.info("Nenhuma moeda ativa no momento.")
    else:
        st.error(f"Erro ao carregar moedas ativas: {response.status_code} - {response.text}")
except Exception as e:
    st.error(f"Erro ao conectar com a API: {str(e)}") 