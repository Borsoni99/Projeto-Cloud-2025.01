# Trading Bot API

A Flask-based REST API for managing trading bot users, configurations, and active cryptocurrencies.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your MySQL database:
- Make sure MySQL is running
- Create a database named `trading_bot`
- Update the database connection URL in `app/config/config.py` if needed

4. Run the application:
```bash
python run.py
```

## API Endpoints

### Usuario (User)
- `POST /api/usuario` - Create new user
- `PUT /api/usuario/<usuario_id>/saldo` - Update user balance

### Usuario Config
- `POST /api/usuario/<usuario_id>/config` - Create user configuration
- `GET /api/usuario/<usuario_id>/config` - Get user configuration
- `PUT /api/usuario/<usuario_id>/config` - Update user configuration

### Moedas Ativas (Active Cryptocurrencies)
- `POST /api/usuario/<usuario_id>/moedas` - Add active cryptocurrency
- `DELETE /api/usuario/<usuario_id>/moedas/<moeda_id>` - Delete active cryptocurrency

## Example Requests

### Create User
```bash
curl -X POST http://localhost:5000/api/usuario \
  -H "Content-Type: application/json" \
  -d '{
    "usuario_login": "testuser",
    "usuario_senha": "password123",
    "usuario_binanceApiKey": "your-api-key",
    "usuario_binanceSecretKey": "your-secret-key"
  }'
```

### Update User Balance
```bash
curl -X PUT http://localhost:5000/api/usuario/1/saldo \
  -H "Content-Type: application/json" \
  -d '{
    "saldo": 1000.50
  }'
```

### Create User Config
```bash
curl -X POST http://localhost:5000/api/usuario/1/config \
  -H "Content-Type: application/json" \
  -d '{
    "valor_compra": 10.00,
    "pct_ganho": 15.00,
    "pct_perda": 5.00
  }'
```

### Add Active Cryptocurrency
```bash
curl -X POST http://localhost:5000/api/usuario/1/moedas \
  -H "Content-Type: application/json" \
  -d '{
    "simbolo": "BTCUSDT"
  }'
``` 