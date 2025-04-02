from flask import Blueprint, request, jsonify
from app.models.usuario import Usuario
from app.models.usuario_config import UsuarioConfig
from decimal import Decimal
from binance.client import Client
from binance.exceptions import BinanceAPIException
from app.services.binance_service import BinanceService
from app.database import db

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('usuario_login') or not data.get('usuario_senha'):
        return jsonify({'error': 'Campos obrigatórios não informados'}), 400

    try:
        usuario = Usuario.query.filter_by(usuario_login=data['usuario_login']).first()
        
        if usuario and usuario.usuario_senha == data['usuario_senha']:
            return jsonify({
                'success': True,
                'usuario_id': usuario.usuario_id,
                'message': 'Login efetuado com sucesso'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Usuário ou senha inválidos'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

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