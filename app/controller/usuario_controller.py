from flask import Blueprint, request, jsonify
from app.models.usuario import Usuario
from decimal import Decimal
from binance.client import Client
from binance.exceptions import BinanceAPIException
from app.services.binance_service import BinanceService
from app.database import db

usuario_bp = Blueprint('usuario', __name__)

# Add this function to get all trading pairs from Binance
def get_binance_trading_pairs():
    try:
        client = Client(None, None)  # We don't need API keys for public endpoints
        exchange_info = client.get_exchange_info()
        trading_pairs = [symbol['symbol'] for symbol in exchange_info['symbols'] if symbol['status'] == 'TRADING']
        return trading_pairs
    except BinanceAPIException as e:
        print(f"Binance API error: {e}")

        
        return []
    except Exception as e:
        print(f"Error fetching trading pairs: {e}")
        return []

@usuario_bp.route('', methods=['POST'])
def create_usuario():
    data = request.get_json()

    if not data or not data.get('usuario_login') or not data.get('usuario_senha'):
        return jsonify({'error': 'Missing required fields'}), 400

    new_usuario = Usuario(
        usuario_login=data['usuario_login'],
        usuario_senha=data['usuario_senha'],
        usuario_binanceApiKey=data.get('usuario_binanceApiKey'),
        usuario_binanceSecretKey=data.get('usuario_binanceSecretKey')
    )

    try:
        db.session.add(new_usuario)
        db.session.commit()
        return jsonify({'message': 'Usuario created successfully', 'usuario_id': new_usuario.usuario_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@usuario_bp.route('/<int:usuario_id>/saldo', methods=['PUT'])
def update_saldo(usuario_id):
    data = request.get_json()

    if 'saldo' not in data:
        return jsonify({'error': 'Saldo is required'}), 400

    try:
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({'error': 'Usuario not found'}), 404

        usuario.usuario_saldo += Decimal(data['saldo'])
        db.session.commit()
        return jsonify({'message': 'Saldo updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Add a new endpoint to get all available trading pairs
@usuario_bp.route('/trading-pairs', methods=['GET'])
def get_trading_pairs():
    try:
        trading_pairs = get_binance_trading_pairs()
        return jsonify({
            'trading_pairs': trading_pairs,
            'count': len(trading_pairs)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@usuario_bp.route('/<int:usuario_id>/create-order', methods=['POST'])
def create_binance_order(usuario_id):
    data = request.get_json()

    if not data or not data.get('symbol') or not data.get('quantity'):
        return jsonify({'error': 'Symbol and quantity are required'}), 400

    # Get user and verify API keys
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'error': 'Usuario not found'}), 404

    if not usuario.usuario_binanceApiKey or not usuario.usuario_binanceSecretKey:
        return jsonify({'error': 'Binance API credentials not configured'}), 400

    symbol = data['symbol'].upper()
    quantity = float(data['quantity'])

    # Initialize Binance service
    binance_service = BinanceService(
        usuario.usuario_binanceApiKey,
        usuario.usuario_binanceSecretKey
    )

    # First get symbol information to validate
    symbol_info = binance_service.get_symbol_info(symbol)
    if not symbol_info['success']:
        return jsonify({'error': symbol_info['error']}), 400

    # Create test order first
    test_order = binance_service.create_test_order(symbol, quantity)
    if not test_order['success']:
        return jsonify({
            'error': 'Test order failed',
            'details': test_order['error']
        }), 400

    # If test order succeeds, create real order
    order_result = binance_service.create_buy_order(symbol, quantity)
    if not order_result['success']:
        return jsonify({
            'error': 'Order creation failed',
            'details': order_result['error']
        }), 400

    return jsonify({
        'message': 'Order created successfully',
        'order': order_result['order']
    }), 201