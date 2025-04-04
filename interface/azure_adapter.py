#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para adaptar os arquivos para funcionarem no Azure.
Este script é executado durante o deploy para ajustar os imports.
"""

import os
import re
import sys

def fix_imports():
    """Corrige os imports nos arquivos para funcionarem no Azure"""
    print("Adaptando arquivos para o Azure...")
    
    # Obtém o diretório atual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Lista de arquivos Python a serem processados
    py_files = []
    for root, _, files in os.walk(current_dir):
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file))
    
    # Padrões de substituição
    replacements = [
        (r'from interface\.', 'from '),  # Substitui "from interface." por "from "
        (r'import interface\.', 'import '),  # Substitui "import interface." por "import "
    ]
    
    # Processa cada arquivo
    for file_path in py_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Aplica as substituições
        modified = False
        for pattern, replacement in replacements:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                modified = True
        
        # Se o arquivo foi modificado, salva as alterações
        if modified:
            print(f"Adaptando arquivo: {os.path.basename(file_path)}")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    print("Adaptação concluída!")

if __name__ == "__main__":
    fix_imports() 