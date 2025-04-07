# Trading Bot

Este projeto consiste em um sistema de trading automatizado para criptomoedas, composto por uma API Flask para gerenciamento de operações e uma interface Streamlit para interação com o usuário. O sistema permite que usuários configurem, monitorem e executem operações de compra e venda de criptomoedas de forma automatizada.

## Acesso à Aplicação

A aplicação está disponível através do seguinte link:
- URL da Aplicação: [https://ibmec-trading-bot-bfg3gngbgre4ambh.centralus-01.azurewebsites.net](https://ibmec-trading-bot-bfg3gngbgre4ambh.centralus-01.azurewebsites.net)

## Executando a Aplicação

Ao acessar a aplicação através do Azure App Service, você poderá:

1. **Criar uma conta** ou fazer login com credenciais existentes
2. **Configurar suas chaves da API Binance** para permitir operações reais
3. **Adicionar criptomoedas** à sua lista de moedas ativas
4. **Configurar parâmetros de trading** como valor de compra e percentuais de ganho/perda
5. **Iniciar operações automatizadas** ou criar ordens manuais

## Tecnologias Utilizadas

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: Streamlit
- **Banco de Dados**: MySQL (Azure MySQL)
- **Deployment**: Azure App Service
- **Integração com APIs**: Binance API

## API Endpoints

A API do Trading Bot oferece os seguintes endpoints para operações diversas:

### Usuário (`/usuario`)

#### Criar Usuário
- **Método**: `POST`
- **Endpoint**: `/usuario`
- **Descrição**: Cria um novo usuário na plataforma.
- **Corpo da Requisição**:
  ```json
  {
    "usuario_login": "testuser",
    "usuario_senha": "password123",
    "usuario_binanceApiKey": "your-api-key",
    "usuario_binanceSecretKey": "your-secret-key",
    "valor_compra": 10.00,
    "pct_ganho": 15.00,
    "pct_perda": 5.00
  }
  ```
- **Resposta de Sucesso** (201 Created):
  ```json
  {
    "message": "Usuário criado com sucesso",
    "usuario_id": 1
  }
  ```

#### Login de Usuário
- **Método**: `POST`
- **Endpoint**: `/usuario/login`
- **Descrição**: Autentica um usuário existente.
- **Corpo da Requisição**:
  ```json
  {
    "usuario_login": "testuser",
    "usuario_senha": "password123"
  }
  ```
- **Resposta de Sucesso** (200 OK):
  ```json
  {
    "success": true,
    "usuario_id": 1,
    "message": "Login efetuado com sucesso"
  }
  ```

#### Obter Usuário
- **Método**: `GET`
- **Endpoint**: `/usuario/{usuario_id}`
- **Descrição**: Obtém detalhes de um usuário específico.
- **Resposta de Sucesso** (200 OK):
  ```json
  {
    "usuario_id": 1,
    "usuario_login": "testuser",
    "usuario_saldo": 1000.50,
    "has_binance_keys": true
  }
  ```

#### Excluir Usuário
- **Método**: `DELETE`
- **Endpoint**: `/usuario/{usuario_id}`
- **Descrição**: Remove um usuário do sistema.
- **Resposta de Sucesso** (200 OK):
  ```json
  {
    "message": "Usuário excluído com sucesso"
  }
  ```

#### Obter Configurações do Usuário
- **Método**: `GET`
- **Endpoint**: `/usuario/{usuario_id}/config`
- **Descrição**: Obtém as configurações de trading de um usuário.
- **Resposta de Sucesso** (200 OK):
  ```json
  {
    "valor_compra": 10.00,
    "pct_ganho": 15.00,
    "pct_perda": 5.00
  }
  ```

#### Atualizar Configurações do Usuário
- **Método**: `PUT`
- **Endpoint**: `/usuario/{usuario_id}/config`
- **Descrição**: Atualiza as configurações de trading de um usuário.
- **Corpo da Requisição**:
  ```json
  {
    "valor_compra": 20.00,
    "pct_ganho": 12.00,
    "pct_perda": 8.00
  }
  ```
- **Resposta de Sucesso** (200 OK):
  ```json
  {
    "message": "Configuração atualizada com sucesso"
  }
  ```

### Moedas Ativas (`/moedas_ativas`)

#### Listar Pares de Trading Disponíveis
- **Método**: `GET`
- **Endpoint**: `/moedas_ativas/trading-pairs`
- **Descrição**: Lista todos os pares de trading disponíveis na Binance.
- **Resposta de Sucesso** (200 OK):
  ```json
  {
    "success": true,
    "trading_pairs": ["BTCUSDT", "ETHUSDT", "BNBUSDT", ...],
    "count": 100
  }
  ```

#### Listar Moedas Ativas do Usuário
- **Método**: `GET`
- **Endpoint**: `/moedas_ativas/{usuario_id}`
- **Descrição**: Lista todas as moedas ativas configuradas para o usuário.
- **Resposta de Sucesso** (200 OK):
  ```json
  {
    "total": 2,
    "moedas": [
      {
        "id": 1,
        "simbolo": "BTCUSDT",
        "ultimo_preco": 35000.50
      },
      {
        "id": 2,
        "simbolo": "ETHUSDT",
        "ultimo_preco": 2400.75
      }
    ]
  }
  ```

#### Adicionar Moeda Ativa
- **Método**: `POST`
- **Endpoint**: `/moedas_ativas/{usuario_id}`
- **Descrição**: Adiciona uma ou mais moedas à lista de moedas ativas do usuário.
- **Corpo da Requisição** (uma moeda):
  ```json
  {
    "simbolo": "BTCUSDT"
  }
  ```
- **Corpo da Requisição** (várias moedas):
  ```json
  {
    "simbolos": ["BTCUSDT", "ETHUSDT", "ADAUSDT"]
  }
  ```
- **Resposta de Sucesso** (201 Created):
  ```json
  {
    "message": "2 moeda(s) adicionada(s) com sucesso",
    "adicionadas": ["BTCUSDT", "ADAUSDT"],
    "ignoradas": [
      {
        "simbolo": "ETHUSDT",
        "motivo": "Moeda já cadastrada para este usuário"
      }
    ]
  }
  ```

#### Remover Moeda Ativa por ID
- **Método**: `DELETE`
- **Endpoint**: `/moedas_ativas/{usuario_id}/{moeda_id}`
- **Descrição**: Remove uma moeda da lista de moedas ativas do usuário pelo ID.
- **Resposta de Sucesso** (200 OK):
  ```json
  {
    "message": "Moeda ativa removida com sucesso"
  }
  ```

#### Remover Moeda Ativa por Símbolo
- **Método**: `DELETE`
- **Endpoint**: `/moedas_ativas/{usuario_id}/simbolo/{simbolo}`
- **Descrição**: Remove uma moeda da lista de moedas ativas do usuário pelo símbolo.
- **Resposta de Sucesso** (200 OK):
  ```json
  {
    "message": "Moeda BTCUSDT removida com sucesso"
  }
  ```

#### Obter Quantidade Mínima para Trading
- **Método**: `GET`
- **Endpoint**: `/moedas_ativas/binance/min_quantity/{simbolo}`
- **Descrição**: Obtém a quantidade mínima permitida para negociação de um par específico.
- **Resposta de Sucesso** (200 OK):
  ```json
  {
    "success": true,
    "min_quantity": 0.001
  }
  ```

### Ordens (`/ordem`)

#### Criar Ordem
- **Método**: `POST`
- **Endpoint**: `/ordem/{usuario_id}`
- **Descrição**: Cria uma nova ordem de compra ou venda.
- **Corpo da Requisição**:
  ```json
  {
    "simbolo": "BTCUSDT",
    "tp_operacao": "COMPRA",
    "quantidade": 0.001,
    "tipo": "MERCADO"
  }
  ```
- **Resposta de Sucesso** (201 Created):
  ```json
  {
    "message": "Ordem criada com sucesso",
    "ordem_id": "123456",
    "simbolo": "BTCUSDT",
    "tipo": "MERCADO",
    "tp_operacao": "COMPRA",
    "quantidade": 0.001,
    "preco": 35000.00,
    "status": "EXECUTADA"
  }
  ```

#### Listar Ordens
- **Método**: `GET`
- **Endpoint**: `/ordem/{usuario_id}`
- **Descrição**: Lista todas as ordens criadas pelo usuário.
- **Resposta de Sucesso** (200 OK):
  ```json
  {
    "total": 2,
    "ordens": [
      {
        "simbolo": "BTCUSDT",
        "ordem_id": "123456",
        "qtd_executada": 0.001,
        "tipo": "MERCADO",
        "tp_operacao": "COMPRA",
        "preco": 35000.00,
        "status": "EXECUTADA",
        "fills": [
          {
            "quantidade": 0.001,
            "preco": 35000.00
          }
        ]
      },
      {
        "simbolo": "ETHUSDT",
        "ordem_id": "123457",
        "qtd_executada": 0.01,
        "tipo": "LIMITE",
        "tp_operacao": "VENDA",
        "preco": 2500.00,
        "status": "PENDENTE",
        "fills": []
      }
    ]
  }
  ```

#### Obter Ordem Específica
- **Método**: `GET`
- **Endpoint**: `/ordem/{usuario_id}/{ordem_id}`
- **Descrição**: Obtém os detalhes de uma ordem específica.
- **Resposta de Sucesso** (200 OK):
  ```json
  {
    "simbolo": "BTCUSDT",
    "ordem_id": "123456",
    "qtd_executada": 0.001,
    "tipo": "MERCADO",
    "tp_operacao": "COMPRA",
    "preco": 35000.00,
    "status": "EXECUTADA",
    "fills": [
      {
        "quantidade": 0.001,
        "preco": 35000.00
      }
    ]
  }
  ```

#### Listar Ordens Abertas
- **Método**: `GET`
- **Endpoint**: `/ordem/relatorios/{usuario_id}/abertos`
- **Descrição**: Lista todas as ordens em aberto (não vendidas) do usuário.
- **Resposta de Sucesso** (200 OK):
  ```json
  {
    "total": 1,
    "ordens_abertas": [
      {
        "id": 1,
        "moeda": "BTCUSDT",
        "quantidade": 0.001,
        "preco_compra": 35000.00,
        "data_operacao": "2023-10-25 14:30:00",
        "status": "EM CARTEIRA"
      }
    ]
  }
  ```

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