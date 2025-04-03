# Trading Bot

Este projeto consiste em uma API Flask para gerenciamento de bots de trading e uma interface Streamlit separada.

## Estrutura do Projeto

```
Projeto-Cloud-2025.01/
│
├── app/                    # API Flask
│   ├── config/             # Configurações
│   ├── controller/         # Controladores (endpoints)
│   ├── database/           # Configuração do banco de dados
│   ├── models/             # Modelos de dados
│   └── __init__.py         # Inicialização da aplicação Flask
│
├── interface/              # Interface Streamlit
│   ├── components/         # Componentes reutilizáveis
│   ├── pages/              # Páginas da aplicação
│   ├── .streamlit/         # Configuração do Streamlit
│   ├── config.py           # Configurações específicas da interface
│   ├── Home.py             # Página inicial (login)
│   ├── startup.py          # Script para iniciar no Azure
│   └── requirements.txt    # Dependências específicas da interface
│
├── run.py                  # Script para iniciar a API Flask
└── run_interface.py        # Script para iniciar a interface Streamlit localmente
```

## Configuração da API

1. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure seu banco de dados MySQL:
- Certifique-se de que o MySQL está em execução
- Crie um banco de dados chamado `trading_bot`
- Atualize a URL de conexão do banco de dados em `app/config/config.py` se necessário

4. Execute a aplicação:
```bash
python run.py
```

## Configuração da Interface

1. Instale as dependências específicas da interface:
```bash
cd interface
pip install -r requirements.txt
```

2. Configure as variáveis de ambiente:
   - Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
   ```
   API_BASE_URL=http://localhost:8000  # URL da API Flask
   STREAMLIT_SERVER_PORT=8501  # Porta para o Streamlit
   ```

3. Execute a interface localmente:
```bash
python run_interface.py
```

## Implantação no Azure

### API Flask

- Use o arquivo `run.py` para iniciar a API
- Comando de inicialização: `gunicorn --bind=0.0.0.0:8000 run:app`
- Porta: 8000

### Interface Streamlit

- Use o arquivo `interface/startup.py` para iniciar a interface
- Comando de inicialização: `python interface/startup.py`
- Porta: 8000 (no Azure)

## Endpoints da API

### Usuario (Usuário)
- `POST /usuario` - Criar novo usuário
- `POST /usuario/login` - Login de usuário

### Moedas Ativas
- `POST /moedas_ativas/<usuario_id>` - Adicionar criptomoeda ativa
- `GET /moedas_ativas/<usuario_id>` - Listar criptomoedas ativas
- `DELETE /moedas_ativas/<usuario_id>/<simbolo>` - Excluir criptomoeda ativa

### Ordem
- `POST /ordem/<usuario_id>` - Criar ordem de compra/venda

## Exemplos de Requisições

### Criar Usuário
```bash
curl -X POST http://localhost:8000/usuario \
  -H "Content-Type: application/json" \
  -d '{
    "usuario_login": "testuser",
    "usuario_senha": "password123",
    "usuario_binanceApiKey": "your-api-key",
    "usuario_binanceSecretKey": "your-secret-key"
  }'
```

### Login de Usuário
```bash
curl -X POST http://localhost:8000/usuario/login \
  -H "Content-Type: application/json" \
  -d '{
    "usuario_login": "testuser",
    "usuario_senha": "password123"
  }'
```

### Adicionar Criptomoeda Ativa
```bash
curl -X POST http://localhost:8000/moedas_ativas/1 \
  -H "Content-Type: application/json" \
  -d '{
    "simbolo": "BTCUSDT"
  }'
``` 