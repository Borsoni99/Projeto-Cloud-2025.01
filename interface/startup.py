#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para iniciar a interface Streamlit no Azure (produção).
Use este script para implantação no ambiente Azure.
Para execução local/desenvolvimento, use run_interface.py na raiz.

Diferenças principais:
1. Porta 8000 (Azure) vs. 8501 (desenvolvimento)
2. Caminho relativo ajustado para execução dentro da pasta interface
"""

import os
import subprocess
import sys

def start_streamlit():
    """Inicia a aplicação Streamlit no ambiente Azure"""
    try:
        print("Adaptando arquivos para ambiente Azure...")
        # Executa o adaptador para ajustar os imports
        try:
            from azure_adapter import fix_imports
            fix_imports()
        except Exception as e:
            print(f"Erro ao adaptar arquivos: {str(e)}")
            print("Continuando com a inicialização...")
        
        print("Iniciando interface Streamlit no ambiente Azure...")
        
        # Define o arquivo principal
        main_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Home.py")
        
        # Configura o comando para iniciar o Streamlit
        cmd = [
            "streamlit", "run", main_file,
            "--server.port", "8000",  # Usa a porta padrão do Azure
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
    start_streamlit() 