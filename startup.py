import subprocess
import sys
import os
import threading
import time

def start_api():
    """Inicia a API Flask"""
    os.chdir('app')
    subprocess.run([sys.executable, '-m', 'gunicorn', '--bind=0.0.0.0:8000', '--workers=2', '--timeout=120', '--threads=2', 'routes:app'])

def start_streamlit():
    """Inicia o Streamlit"""
    os.chdir('app/streamlit')
    subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'Home.py', '--server.port=8501', '--server.address=0.0.0.0'])

if __name__ == '__main__':
    # Inicia a API em uma thread separada
    api_thread = threading.Thread(target=start_api)
    api_thread.daemon = True
    api_thread.start()
    
    # Aguarda um momento para garantir que a API iniciou
    time.sleep(5)
    
    # Inicia o Streamlit no thread principal
    start_streamlit() 