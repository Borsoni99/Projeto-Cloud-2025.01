#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para iniciar a interface Streamlit localmente (desenvolvimento).
Use este script para execução em ambiente de desenvolvimento.
Para implantação no Azure, use interface/startup.py.

Diferenças principais:
1. Porta 8501 (desenvolvimento) vs. 8000 (Azure)
2. Caminho relativo ajustado para execução na raiz do projeto
"""

import os
import subprocess
import sys

def run_streamlit():
    """Inicia a aplicação Streamlit em ambiente local"""
    try:
        print("Iniciando interface Streamlit em modo de desenvolvimento...")
        # Define o diretório da interface
        interface_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "interface")
        
        # Define o arquivo principal
        main_file = os.path.join(interface_dir, "Home.py")
        
        # Configura o comando para iniciar o Streamlit
        cmd = [
            "streamlit", "run", main_file,
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--browser.serverAddress", "0.0.0.0",
            "--browser.gatherUsageStats", "false",
            "--server.enableCORS", "true"
        ]
        
        # Executa o comando
        subprocess.run(cmd)
    except Exception as e:
        print(f"Erro ao iniciar Streamlit: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_streamlit() 