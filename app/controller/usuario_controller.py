from flask import Blueprint, request, jsonify
from app.models.usuario import Usuario
from app.models.usuario_config import UsuarioConfig
from decimal import Decimal
from binance.client import Client
from binance.exceptions import BinanceAPIException
from app.services.binance_service import BinanceService
from app.database import db

usuario_bp = Blueprint('usuario', __name__)

# Função auxiliar para obter pares de trading da Binance
def get_binance_trading_pairs():
    try:
        client = Client(None, None)  # Não precisamos de chaves API para endpoints públicos
        exchange_info = client.get_exchange_info()
        trading_pairs = [symbol['symbol'] for symbol in exchange_info['symbols'] if symbol['status'] == 'TRADING']
        return trading_pairs
    except BinanceAPIException as e:
        print(f"Erro da API Binance: {e}")
        return []
    except Exception as e:
        print(f"Erro ao buscar pares de trading: {e}")
        return []

# Criar usuário
@usuario_bp.route('', methods=['POST'])
def create_usuario():
    data = request.get_json()

    if not data or not data.get('usuario_login') or not data.get('usuario_senha'):
        return jsonify({'error': 'Campos obrigatórios não informados'}), 400

    # Verifica se já existe um usuário com o mesmo login
    existing_user = Usuario.query.filter_by(usuario_login=data['usuario_login']).first()
    if existing_user:
        return jsonify({'error': 'Nome de usuário já está em uso'}), 400

    new_usuario = Usuario(
        usuario_login=data['usuario_login'],
        usuario_senha=data['usuario_senha'],
        usuario_binanceApiKey=data.get('usuario_binanceApiKey'),
        usuario_binanceSecretKey=data.get('usuario_binanceSecretKey')
    )

    try:
        db.session.add(new_usuario)
        db.session.commit()
        
        # Cria configuração padrão para o novo usuário
        default_config = UsuarioConfig(
            usuario_id=new_usuario.usuario_id,
            usuario_config_valorCompra=data.get('valor_compra', 5.00),
            usuario_config_pctGanho=data.get('pct_ganho', 10.00),
            usuario_config_pctPerda=data.get('pct_perda', 10.00)
        )
        
        db.session.add(default_config)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuário criado com sucesso',
            'usuario_id': new_usuario.usuario_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Listar todos os usuários
@usuario_bp.route('', methods=['GET'])
def get_all_usuarios():
    try:
        usuarios = Usuario.query.all()
        result = []
        
        for usuario in usuarios:
            result.append({
                'usuario_id': usuario.usuario_id,
                'usuario_login': usuario.usuario_login,
                'usuario_saldo': float(usuario.usuario_saldo),
                'has_binance_keys': bool(usuario.usuario_binanceApiKey and usuario.usuario_binanceSecretKey)
            })
            
        return jsonify({
            'total': len(result),
            'usuarios': result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Obter usuário por ID
@usuario_bp.route('/<int:usuario_id>', methods=['GET'])
def get_usuario(usuario_id):
    try:
        usuario = Usuario.query.get(usuario_id)
        
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        return jsonify({
            'usuario_id': usuario.usuario_id,
            'usuario_login': usuario.usuario_login,
            'usuario_saldo': float(usuario.usuario_saldo),
            'has_binance_keys': bool(usuario.usuario_binanceApiKey and usuario.usuario_binanceSecretKey)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Atualizar usuário
@usuario_bp.route('/<int:usuario_id>', methods=['PUT'])
def update_usuario(usuario_id):
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
        
    try:
        usuario = Usuario.query.get(usuario_id)
        
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        # Atualiza os campos do usuário
        if 'usuario_login' in data:
            # Verifica se o login já está em uso por outro usuário
            existing = Usuario.query.filter_by(usuario_login=data['usuario_login']).first()
            if existing and existing.usuario_id != usuario_id:
                return jsonify({'error': 'Nome de usuário já está em uso'}), 400
            usuario.usuario_login = data['usuario_login']
            
        if 'usuario_senha' in data:
            usuario.usuario_senha = data['usuario_senha']
            
        if 'usuario_binanceApiKey' in data:
            usuario.usuario_binanceApiKey = data['usuario_binanceApiKey']
            
        if 'usuario_binanceSecretKey' in data:
            usuario.usuario_binanceSecretKey = data['usuario_binanceSecretKey']
            
        # Integração da atualização de saldo
        if 'saldo' in data:
            try:
                # Caso queira substituir o saldo atual
                if 'substituir_saldo' in data and data['substituir_saldo']:
                    usuario.usuario_saldo = Decimal(data['saldo'])
                # Caso padrão: adicionar ao saldo atual
                else:
                    usuario.usuario_saldo += Decimal(data['saldo'])
            except (ValueError, TypeError) as e:
                return jsonify({'error': f'Valor de saldo inválido: {str(e)}'}), 400
            
        db.session.commit()
        
        return jsonify({
            'message': 'Usuário atualizado com sucesso',
            'saldo_atual': float(usuario.usuario_saldo)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Excluir usuário
@usuario_bp.route('/<int:usuario_id>', methods=['DELETE'])
def delete_usuario(usuario_id):
    try:
        usuario = Usuario.query.get(usuario_id)
        
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        db.session.delete(usuario)
        db.session.commit()
        
        return jsonify({'message': 'Usuário excluído com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Criar ordem na Binance
@usuario_bp.route('/<int:usuario_id>/create-order', methods=['POST'])
def create_binance_order(usuario_id):
    data = request.get_json()

    if not data or not data.get('symbol') or not data.get('quantity'):
        return jsonify({'error': 'Símbolo e quantidade são obrigatórios'}), 400

    # Obtém usuário e verifica chaves API
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    if not usuario.usuario_binanceApiKey or not usuario.usuario_binanceSecretKey:
        return jsonify({'error': 'Credenciais da API Binance não configuradas'}), 400

    symbol = data['symbol'].upper()
    quantity = float(data['quantity'])

    # Inicializa o serviço Binance
    binance_service = BinanceService(
        usuario.usuario_binanceApiKey,
        usuario.usuario_binanceSecretKey
    )

    # Primeiro obtém informações do símbolo para validar
    symbol_info = binance_service.get_symbol_info(symbol)
    if not symbol_info['success']:
        return jsonify({'error': symbol_info['error']}), 400

    # Cria ordem de teste primeiro
    test_order = binance_service.create_test_order(symbol, quantity)
    if not test_order['success']:
        return jsonify({
            'error': 'Teste de ordem falhou',
            'details': test_order['error']
        }), 400

    # Se a ordem de teste for bem-sucedida, cria ordem real
    order_result = binance_service.create_buy_order(symbol, quantity)
    if not order_result['success']:
        return jsonify({
            'error': 'Criação de ordem falhou',
            'details': order_result['error']
        }), 400

    return jsonify({
        'message': 'Ordem criada com sucesso',
        'order': order_result['order']
    }), 201

# Obter configuração do usuário
@usuario_bp.route('/<int:usuario_id>/config', methods=['GET'])
def get_usuario_config(usuario_id):
    try:
        # Verificar se o usuário existe
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        config = UsuarioConfig.query.filter_by(usuario_id=usuario_id).first()
        if not config:
            return jsonify({'error': 'Configuração não encontrada para este usuário'}), 404

        return jsonify({
            'valor_compra': float(config.usuario_config_valorCompra),
            'pct_ganho': float(config.usuario_config_pctGanho),
            'pct_perda': float(config.usuario_config_pctPerda)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Criar configuração do usuário
@usuario_bp.route('/<int:usuario_id>/config', methods=['POST'])
def create_usuario_config(usuario_id):
    data = request.get_json()

    # Verificar se o usuário existe
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    # Verificar se já existe configuração para este usuário
    existing_config = UsuarioConfig.query.filter_by(usuario_id=usuario_id).first()
    if existing_config:
        return jsonify({'error': 'Configuração já existe para este usuário'}), 400

    new_config = UsuarioConfig(
        usuario_id=usuario_id,
        usuario_config_valorCompra=data.get('valor_compra', 5.00),
        usuario_config_pctGanho=data.get('pct_ganho', 10.00),
        usuario_config_pctPerda=data.get('pct_perda', 10.00)
    )

    try:
        db.session.add(new_config)
        db.session.commit()
        return jsonify({'message': 'Configuração criada com sucesso'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Atualizar configuração do usuário
@usuario_bp.route('/<int:usuario_id>/config', methods=['PUT'])
def edit_usuario_config(usuario_id):
    data = request.get_json()
    
    # Verificar se o usuário existe
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404
        
    config = UsuarioConfig.query.filter_by(usuario_id=usuario_id).first()
    if not config:
        return jsonify({'error': 'Configuração não encontrada para este usuário'}), 404

    try:
        if 'valor_compra' in data:
            config.usuario_config_valorCompra = Decimal(data['valor_compra'])
        if 'pct_ganho' in data:
            config.usuario_config_pctGanho = Decimal(data['pct_ganho'])
        if 'pct_perda' in data:
            config.usuario_config_pctPerda = Decimal(data['pct_perda'])

        db.session.commit()
        return jsonify({'message': 'Configuração atualizada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500