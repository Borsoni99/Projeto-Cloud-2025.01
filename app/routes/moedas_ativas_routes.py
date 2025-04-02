from flask import Blueprint, request, jsonify
from app.models.moedas_ativas import MoedasAtivas
from app.database import db
from binance.client import Client
from app.config.config import Config

bp = Blueprint('moedas_ativas', __name__)

@bp.route('/trading-pairs', methods=['GET'])
def get_trading_pairs():
    """Obtém todos os pares de trading disponíveis na Binance"""
    try:
        client = Client(Config.BINANCE_API_KEY, Config.BINANCE_API_SECRET)
        exchange_info = client.get_exchange_info()
        trading_pairs = [symbol['symbol'] for symbol in exchange_info['symbols'] if symbol['status'] == 'TRADING']
        return jsonify({'trading_pairs': trading_pairs}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:usuario_id>', methods=['GET'])
def get_active_pairs(usuario_id):
    """Obtém as moedas ativas do usuário"""
    try:
        moedas = MoedasAtivas.query.filter_by(usuario_id=usuario_id).all()
        return jsonify({
            'moedas': [{'simbolo': moeda.moedas_ativas_simbolo} for moeda in moedas]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:usuario_id>', methods=['POST'])
def create_active_pairs(usuario_id):
    """Cria ou atualiza as moedas ativas do usuário"""
    try:
        data = request.get_json()
        if not data or 'simbolos' not in data:
            return jsonify({'error': 'Missing symbols data'}), 400

        # Primeiro, remove todas as moedas ativas existentes do usuário
        MoedasAtivas.query.filter_by(usuario_id=usuario_id).delete()

        # Adiciona as novas moedas selecionadas
        for simbolo in data['simbolos']:
            nova_moeda = MoedasAtivas(
                moedas_ativas_simbolo=simbolo,
                usuario_id=usuario_id
            )
            db.session.add(nova_moeda)

        db.session.commit()
        return jsonify({'message': 'Moedas ativas atualizadas com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 