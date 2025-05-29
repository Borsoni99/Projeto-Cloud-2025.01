from flask import Blueprint, request, jsonify
from app.models.usuario import Usuario
from app.models.moedas_ativas import MoedasAtivas
from app.database import db
from app.services.binance_service import BinanceService
from decimal import Decimal
from binance.client import Client


moedas_ativas_bp = Blueprint('moedas_ativas', __name__)

@moedas_ativas_bp.route('/trading-pairs', methods=['GET'])
def get_trading_pairs():
    """Obtém todos os pares de trading que estão disponíveis na Binance"""
    try:
        # Inicializar o serviço Binance sem chaves API
        binance_service = BinanceService(None, None)
        trading_pairs = binance_service.get_binance_trading_pairs()
        
        if not trading_pairs:
            return jsonify({
                'success': False,
                'error': 'Nenhum par de trading encontrado'
            }), 404
            
        return jsonify({
            'success': True,
            'trading_pairs': trading_pairs,
            'count': len(trading_pairs)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@moedas_ativas_bp.route('/<int:usuario_id>', methods=['GET'])
def get_moedas_ativas(usuario_id):
    """Obtém todas as moedas ativas de um usuário com seus últimos preços"""
    try:
        # Verificar se o usuário existe
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        # Obter todas as moedas ativas do usuário
        moedas = MoedasAtivas.query.filter_by(usuario_id=usuario_id).all()
        
        # Inicializar serviço Binance (sem chaves API, pois só precisamos de dados públicos)
        binance_service = BinanceService(None, None)
        
        # Montar resposta
        resultado = []
        for moeda in moedas:
            # Obter último preço da moeda
            preco_info = binance_service.get_symbol_price(moeda.moedas_ativas_simbolo)
            
            if preco_info['success']:
                resultado.append({
                    'id': moeda.moedas_ativas_id,
                    'simbolo': moeda.moedas_ativas_simbolo,
                    'ultimo_preco': float(preco_info['price'])
                })
            else:
                resultado.append({
                    'id': moeda.moedas_ativas_id,
                    'simbolo': moeda.moedas_ativas_simbolo,
                    'ultimo_preco': None,
                    'erro': preco_info['error']
                })
            
        return jsonify({
            'total': len(resultado),
            'moedas': resultado
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@moedas_ativas_bp.route('/<int:usuario_id>', methods=['POST'])
def create_moeda_ativa(usuario_id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    # Verificar se o usuário existe
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    binance_service = BinanceService(None, None)
        
    # Obter pares de trading disponíveis na Binance
    available_pairs = binance_service.get_binance_trading_pairs()
    
    # Suporte para adicionar uma única moeda ou múltiplas moedas
    simbolos = []
    if 'simbolo' in data:
        simbolos = [data['simbolo'].upper()]
    elif 'simbolos' in data and isinstance(data['simbolos'], list):
        simbolos = [simbolo.upper() for simbolo in data['simbolos']]
    else:
        return jsonify({'error': 'É necessário fornecer o campo "simbolo" ou uma lista de "simbolos"'}), 400
    
    # Preparar listas para rastrear resultados
    moedas_adicionadas = []
    moedas_ignoradas = []
    
    # Adicionar cada moeda à lista
    for simbolo in simbolos:
        # Verificar se o símbolo existe na Binance
        if simbolo not in available_pairs:
            moedas_ignoradas.append({
                'simbolo': simbolo,
                'motivo': f'O símbolo {simbolo} não está disponível para trading na Binance'
            })
            continue
            
        # Verificar se a moeda já está cadastrada para este usuário
        moeda_existente = MoedasAtivas.query.filter_by(
            usuario_id=usuario_id,
            moedas_ativas_simbolo=simbolo
        ).first()
        
        if moeda_existente:
            moedas_ignoradas.append({
                'simbolo': simbolo,
                'motivo': 'Moeda já cadastrada para este usuário'
            })
            continue
            
        # Criar nova moeda ativa
        new_moeda = MoedasAtivas(
            moedas_ativas_simbolo=simbolo,
            usuario_id=usuario_id
        )
        
        db.session.add(new_moeda)
        moedas_adicionadas.append(simbolo)

    # Commit das alterações ao banco de dados
    try:
        db.session.commit()
        
        # Preparar resposta
        resposta = {
            'message': f'{len(moedas_adicionadas)} moeda(s) adicionada(s) com sucesso',
            'adicionadas': moedas_adicionadas
        }
        
        if moedas_ignoradas:
            resposta['ignoradas'] = moedas_ignoradas
            
        return jsonify(resposta), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@moedas_ativas_bp.route('/<int:usuario_id>/<int:moeda_id>', methods=['DELETE'])
def delete_moeda_ativa(usuario_id, moeda_id):
    """Remove uma moeda ativa pelo ID"""
    moeda = MoedasAtivas.query.filter_by(moedas_ativas_id=moeda_id, usuario_id=usuario_id).first()

    if not moeda:
        return jsonify({'error': 'Moeda ativa não encontrada'}), 404

    try:
        db.session.delete(moeda)
        db.session.commit()
        return jsonify({'message': 'Moeda ativa removida com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@moedas_ativas_bp.route('/<int:usuario_id>/simbolo/<simbolo>', methods=['DELETE'])
def delete_moeda_por_simbolo(usuario_id, simbolo):
    """Remove uma moeda ativa pelo símbolo"""
    simbolo = simbolo.upper()
    
    moeda = MoedasAtivas.query.filter_by(
        usuario_id=usuario_id,
        moedas_ativas_simbolo=simbolo
    ).first()

    if not moeda:
        return jsonify({'error': f'Moeda {simbolo} não encontrada para este usuário'}), 404

    try:
        db.session.delete(moeda)
        db.session.commit()
        return jsonify({'message': f'Moeda {simbolo} removida com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@moedas_ativas_bp.route('/binance/min_quantity/<simbolo>', methods=['GET'])
def get_min_quantity(simbolo):
    """Obtém a quantidade mínima permitida para um par de trading"""
    try:
        # Inicializar o serviço Binance sem chaves API (apenas dados públicos)
        binance_service = BinanceService(None, None)
        
        # Converter o símbolo para maiúsculo
        simbolo = simbolo.upper()
        
        # Obter a quantidade mínima
        result = binance_service.get_min_quantity(simbolo)
        
        if result['success']:
            return jsonify({
                'success': True,
                'min_quantity': result['min_quantity']
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Função auxiliar para obter pares de trading da Binance
def get_binance_trading_pairs():
    """
    Obtém todos os pares de trading disponíveis na Binance
    Não requer chaves API pois usa endpoints públicos
    """
    try:
        # Criar cliente sem chaves API para endpoints públicos
        client = Client(None, None)
        
        # Obter informações da exchange
        exchange_info = client.get_exchange_info()
        
        # Filtrar apenas pares que estão ativos para trading
        trading_pairs = [
            symbol['symbol'] 
            for symbol in exchange_info['symbols'] 
            if symbol['status'] == 'TRADING' and 
               symbol['isSpotTradingAllowed'] and 
               symbol['quoteAsset'] == 'USDT'  # Apenas pares com USDT
        ]
        
        # Ordenar por símbolo
        trading_pairs.sort()
        
        return trading_pairs
    except Exception as e:
        print(f"Erro ao buscar pares de trading: {e}")
        return []