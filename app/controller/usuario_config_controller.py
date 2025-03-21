from flask import Blueprint, request, jsonify
from app.models.usuario import Usuario
from app.models.usuario_config import UsuarioConfig
from decimal import Decimal
from app.database import db

usuario_config_bp = Blueprint('usuario_config', __name__)

@usuario_config_bp.route('/<int:usuario_id>', methods=['POST'])
def create_usuario_config(usuario_id):
    data = request.get_json()

    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'error': 'Usuario not found'}), 404

    if usuario.config:
        return jsonify({'error': 'Config already exists for this user'}), 400

    new_config = UsuarioConfig(
        usuario_id=usuario_id,
        usuario_config_valorCompra=data.get('valor_compra', 5.00),
        usuario_config_pctGanho=data.get('pct_ganho', 10.00),
        usuario_config_pctPerda=data.get('pct_perda', 10.00)
    )

    try:
        db.session.add(new_config)
        db.session.commit()
        return jsonify({'message': 'Config created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@usuario_config_bp.route('/<int:usuario_id>', methods=['GET'])
def get_usuario_config(usuario_id):
    config = UsuarioConfig.query.filter_by(usuario_id=usuario_id).first()
    if not config:
        return jsonify({'error': 'Config not found'}), 404

    return jsonify({
        'valor_compra': float(config.usuario_config_valorCompra),
        'pct_ganho': float(config.usuario_config_pctGanho),
        'pct_perda': float(config.usuario_config_pctPerda)
    }), 200

@usuario_config_bp.route('/<int:usuario_id>', methods=['PUT'])
def edit_usuario_config(usuario_id):
    data = request.get_json()
    config = UsuarioConfig.query.filter_by(usuario_id=usuario_id).first()

    if not config:
        return jsonify({'error': 'Config not found'}), 404

    try:
        if 'valor_compra' in data:
            config.usuario_config_valorCompra = Decimal(data['valor_compra'])
        if 'pct_ganho' in data:
            config.usuario_config_pctGanho = Decimal(data['pct_ganho'])
        if 'pct_perda' in data:
            config.usuario_config_pctPerda = Decimal(data['pct_perda'])

        db.session.commit()
        return jsonify({'message': 'Config updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500