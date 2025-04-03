import os
import sys

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

import streamlit as st
import requests
import json
from interface.config import Config

# Configure page settings
st.set_page_config(
    page_title="Trading Bot - Cadastro",
    page_icon="🤖",
    layout="centered"
)



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
            f'{Config.API_BASE_URL}/register',
            json=data
        )
        return response.json() if response.ok else None
    except requests.exceptions.RequestException:
        return None

def main():
    st.title("🤖 Trading Bot - Cadastro")
    
    with st.container():
        # Create registration form
        with st.form("register_form"):
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            confirm_password = st.text_input("Confirmar Senha", type="password")
            
            # Optional Binance API credentials
            st.markdown("---")
            st.markdown("##### Credenciais da Binance (Opcional)")
            st.markdown("Você pode adicionar depois nas configurações do seu perfil")
            
            binance_api_key = st.text_input("Chave da API Binance", "")
            binance_secret_key = st.text_input("Chave Secreta Binance", type="password")
            
            submit_button = st.form_submit_button("Cadastrar")

            if submit_button:
                if not username or not password or not confirm_password:
                    st.warning("Por favor, preencha todos os campos obrigatórios")
                elif password != confirm_password:
                    st.error("As senhas não coincidem")
                else:
                    result = register_user(
                        username, 
                        password,
                        binance_api_key if binance_api_key else None,
                        binance_secret_key if binance_secret_key else None
                    )
                    
                    if result and result.get('success'):
                        st.success("Cadastro realizado com sucesso! Por favor, faça login.")
                        st.markdown("[Ir para Login](/)")
                    else:
                        error_msg = result.get('error') if result else "Falha no cadastro"
                        st.error(error_msg)

    # Login link
    st.markdown("---")
    st.markdown("Já tem uma conta? [Faça login aqui](/)")

if __name__ == "__main__":
    main() 