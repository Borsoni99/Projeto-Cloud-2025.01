# Imagem base
FROM --platform=linux/amd64 python:3.9-slim-bullseye

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de requisitos
COPY interface/requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da interface
COPY interface/ /app/interface/

# Adicionar o diretório ao PYTHONPATH
ENV PYTHONPATH=/app

# Expor a porta
EXPOSE 8501

# Comando para iniciar a interface
CMD ["streamlit", "run", "interface/Home.py", "--server.port=8501", "--server.address=0.0.0.0"] 