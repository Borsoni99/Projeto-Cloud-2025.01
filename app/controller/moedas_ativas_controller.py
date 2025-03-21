from flask import Blueprint, request, jsonify
from app.models.usuario import Usuario
from app.models.moedas_ativas import MoedasAtivas
from app.database import db
from app.controller.usuario_controller import get_binance_trading_pairs

moedas_ativas_bp = Blueprint('moedas_ativas', __name__)

@moedas_ativas_bp.route('/<int:usuario_id>', methods=['POST'])
def create_moeda_ativa(usuario_id):
    data = request.get_json()

    if not data or not data.get('simbolo'):
        return jsonify({'error': 'Symbol is required'}), 400

    # Get the symbol and convert to uppercase (Binance uses uppercase symbols)
    simbolo = data['simbolo'].upper()

    # Get available trading pairs from Binance
    available_pairs = get_binance_trading_pairs()
    
    # Check if the symbol exists in Binance
    if simbolo not in available_pairs:
        return jsonify({
            'error': 'Invalid trading pair',
            'message': f'The symbol {simbolo} is not available for trading on Binance'
        }), 400

    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'error': 'Usuario not found'}), 404

    new_moeda = MoedasAtivas(
        moedas_ativas_simbolo=simbolo,
        usuario_id=usuario_id
    )

    try:
        db.session.add(new_moeda)
        db.session.commit()
        return jsonify({'message': 'Moeda ativa created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@moedas_ativas_bp.route('/<int:usuario_id>/<int:moeda_id>', methods=['DELETE'])
def delete_moeda_ativa(usuario_id, moeda_id):
    moeda = MoedasAtivas.query.filter_by(moedas_ativas_id=moeda_id, usuario_id=usuario_id).first()

    if not moeda:
        return jsonify({'error': 'Moeda ativa not found'}), 404

    try:
        db.session.delete(moeda)
        db.session.commit()
        return jsonify({'message': 'Moeda ativa deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500