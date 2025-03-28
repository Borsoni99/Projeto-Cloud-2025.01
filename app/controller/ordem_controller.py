from flask import Blueprint, request, jsonify
from app.models.usuario import Usuario
from app.models.ordem import Ordem, OrdemFill
from app.models.ordem_relatorio import OrdemRelatorio
from app.request.ordem_request import OrdemRequest
from app.response.ordem_response import OrdemResponse
from app.response.ordem_fill_response import OrdemFillResponse
from app.services.binance_service import BinanceService
from app.database import db
from decimal import Decimal
from datetime import datetime

ordem_bp = Blueprint('ordem', __name__)

@ordem_bp.route('/<int:usuario_id>', methods=['POST'])
def create_ordem(usuario_id):
    """Cria uma nova ordem"""
    try:
        # Verificar se o usuário existe
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        # Verificar se o usuário tem chaves da Binance configuradas
        if not usuario.usuario_binanceApiKey or not usuario.usuario_binanceSecretKey:
            return jsonify({'error': 'Credenciais da Binance não configuradas'}), 400
            
        # Obter dados da requisição
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
            
        # Validar dados obrigatórios
        required_fields = ['simbolo', 'tp_operacao', 'quantidade']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
                
        # Verificar tipo de ordem (padrão é MERCADO)
        tipo_ordem = data.get('tipo', 'MERCADO').upper()
        if tipo_ordem not in ['MERCADO', 'LIMITE']:
            return jsonify({'error': 'Tipo de ordem deve ser MERCADO ou LIMITE'}), 400
            
        # Se for ordem LIMITE, preço é obrigatório
        if tipo_ordem == 'LIMITE' and 'preco' not in data:
            return jsonify({'error': 'Preço é obrigatório para ordens LIMITE'}), 400
            
        # Criar objeto OrdemRequest
        ordem_request = OrdemRequest(
            simbolo=data['simbolo'].upper(),
            tp_operacao=data['tp_operacao'].upper(),
            quantidade=Decimal(str(data['quantidade'])),
            preco=Decimal(str(data.get('preco', '0')))
        )
        
        # Validar tipo de operação
        if ordem_request.tp_operacao not in ['COMPRA', 'VENDA']:
            return jsonify({'error': 'Tipo de operação deve ser COMPRA ou VENDA'}), 400
            
        # Inicializar serviço Binance
        binance_service = BinanceService(
            usuario.usuario_binanceApiKey,
            usuario.usuario_binanceSecretKey
        )
        
        # Verificar se o símbolo existe
        symbol_info = binance_service.get_symbol_info(ordem_request.simbolo)
        if not symbol_info['success']:
            return jsonify({'error': 'Símbolo não encontrado na Binance'}), 400
            
        # Mapear tipo de operação para formato Binance
        side = 'BUY' if ordem_request.tp_operacao == 'COMPRA' else 'SELL'
        
        # Criar ordem na Binance com base no tipo
        if tipo_ordem == 'MERCADO':
            # Ordem a mercado
            order_result = binance_service.create_order(
                symbol=ordem_request.simbolo,
                side=side,
                quantity=float(ordem_request.quantidade),
                order_type='MARKET'
            )
        else:
            # Ordem limitada
            order_result = binance_service.create_order(
                symbol=ordem_request.simbolo,
                side=side,
                quantity=float(ordem_request.quantidade),
                price=float(ordem_request.preco),
                order_type='LIMIT',
                time_in_force='GTC'  # Good Till Canceled
            )
        
        if not order_result['success']:
            return jsonify({'error': order_result['error']}), 400
            
        # Processar a resposta da Binance
        binance_order = order_result['order']
        
        # Calcular quantidade executada e preço médio
        qtd_executada = Decimal('0')
        preco_medio = Decimal('0')
        fills = []
        
        if 'fills' in binance_order:
            for fill in binance_order['fills']:
                qtd = Decimal(fill['qty'])
                preco = Decimal(fill['price'])
                qtd_executada += qtd
                preco_medio = (preco_medio * (qtd_executada - qtd) + preco * qtd) / qtd_executada if qtd_executada > 0 else preco
                
                # Criar fill no banco de dados
                ordem_fill = OrdemFill(
                    quantidade=qtd,
                    preco=preco
                )
                fills.append(ordem_fill)
        
        # Se for uma ordem LIMITE sem fills, usar o preço definido
        if tipo_ordem == 'LIMITE' and qtd_executada == 0:
            preco_medio = ordem_request.preco
            
        # Definir status base no tipo de ordem
        status = 'EXECUTADA' if tipo_ordem == 'MERCADO' else ('EXECUTADA' if qtd_executada > 0 else 'PENDENTE')
        
        # Criar ordem no banco de dados
        nova_ordem = Ordem(
            usuario_id=usuario_id,
            simbolo=ordem_request.simbolo,
            tp_operacao=ordem_request.tp_operacao,
            quantidade=ordem_request.quantidade,
            preco=preco_medio,
            qtd_executada=qtd_executada,
            tipo=tipo_ordem,
            status=status
        )
        
        # Adicionar fills à ordem
        nova_ordem.fills = fills
        
        db.session.add(nova_ordem)
        
        # Atualizar relatório de ordens
        data_atual = datetime.now()
        
        # Se for uma ordem executada, atualizar o relatório
        if status == 'EXECUTADA' and qtd_executada > 0:
            if ordem_request.tp_operacao == 'COMPRA':
                # Para compras, criar um novo registro no relatório
                relatorio = OrdemRelatorio(
                    usuario_id=usuario_id,
                    preco_compra=preco_medio,
                    preco_venda=Decimal('0'),  # Inicialmente sem venda
                    qtd=qtd_executada,
                    moeda=ordem_request.simbolo,  # Usar o símbolo completo
                    data_operacao=data_atual
                )
                db.session.add(relatorio)
            else:  # VENDA
                # Para vendas, buscar um registro de compra correspondente 
                # com a mesma quantidade e ainda não vendido
                relatorio = OrdemRelatorio.query.filter_by(
                    usuario_id=usuario_id,
                    moeda=ordem_request.simbolo,
                    preco_venda=0,
                    qtd=qtd_executada
                ).order_by(OrdemRelatorio.data_operacao).first()
                
                # Se encontrou um registro correspondente, atualizar com o preço de venda
                if relatorio:
                    relatorio.preco_venda = preco_medio
                    relatorio.data_operacao = data_atual
        
        db.session.commit()
        
        # Criar resposta
        ordem_response = OrdemResponse(
            simbolo=nova_ordem.simbolo,
            ordem_id=str(nova_ordem.ordem_id),
            qtd_executada=nova_ordem.qtd_executada,
            tipo=nova_ordem.tipo,
            tp_operacao=nova_ordem.tp_operacao,
            preco=nova_ordem.preco,
            status=nova_ordem.status,
            fills=[OrdemFillResponse(
                quantidade=fill.quantidade,
                preco=fill.preco
            ).__dict__ for fill in nova_ordem.fills]
        )
        
        return jsonify(ordem_response.__dict__), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ordem_bp.route('/<int:usuario_id>', methods=['GET'])
def get_ordens(usuario_id):
    """Lista todas as ordens de um usuário"""
    try:
        # Verificar se o usuário existe
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        # Obter todas as ordens do usuário
        ordens = Ordem.query.filter_by(usuario_id=usuario_id).all()
        
        # Montar resposta
        resultado = []
        for ordem in ordens:
            fills = []
            for fill in ordem.fills:
                fills.append(OrdemFillResponse(
                    quantidade=fill.quantidade,
                    preco=fill.preco
                ).__dict__)
                
            ordem_response = OrdemResponse(
                simbolo=ordem.simbolo,
                ordem_id=str(ordem.ordem_id),
                qtd_executada=ordem.qtd_executada,
                tipo=ordem.tipo,
                tp_operacao=ordem.tp_operacao,
                preco=ordem.preco,
                status=ordem.status,
                fills=fills
            )
            resultado.append(ordem_response.__dict__)
            
        return jsonify({
            'total': len(resultado),
            'ordens': resultado
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ordem_bp.route('/<int:usuario_id>/<int:ordem_id>', methods=['GET'])
def get_ordem(usuario_id, ordem_id):
    """Obtém uma ordem específica"""
    try:
        # Verificar se o usuário existe
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        # Obter a ordem
        ordem = Ordem.query.filter_by(
            ordem_id=ordem_id,
            usuario_id=usuario_id
        ).first()
        
        if not ordem:
            return jsonify({'error': 'Ordem não encontrada'}), 404
            
        # Montar resposta
        fills = []
        for fill in ordem.fills:
            fills.append(OrdemFillResponse(
                quantidade=fill.quantidade,
                preco=fill.preco
            ).__dict__)
            
        ordem_response = OrdemResponse(
            simbolo=ordem.simbolo,
            ordem_id=str(ordem.ordem_id),
            qtd_executada=ordem.qtd_executada,
            tipo=ordem.tipo,
            tp_operacao=ordem.tp_operacao,
            preco=ordem.preco,
            status=ordem.status,
            fills=fills
        )
        
        return jsonify(ordem_response.__dict__), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ordem_bp.route('/relatorios/<int:usuario_id>', methods=['GET'])
def get_relatorios(usuario_id):
    """Lista todos os relatórios de ordens de um usuário"""
    try:
        # Verificar se o usuário existe
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        # Obter todos os relatórios do usuário
        relatorios = OrdemRelatorio.query.filter_by(usuario_id=usuario_id).all()
        
        # Montar resposta
        resultado = []
        for relatorio in relatorios:
            lucro = None
            if relatorio.preco_venda > 0:
                # Calcular lucro/prejuízo se a moeda foi vendida
                lucro = float(relatorio.preco_venda - relatorio.preco_compra)
                percentual = float((relatorio.preco_venda / relatorio.preco_compra - 1) * 100) if relatorio.preco_compra > 0 else 0
            else:
                lucro = 0
                percentual = 0
                
            resultado.append({
                'id': relatorio.id,
                'moeda': relatorio.moeda,
                'quantidade': float(relatorio.qtd),
                'preco_compra': float(relatorio.preco_compra),
                'preco_venda': float(relatorio.preco_venda),
                'data_operacao': relatorio.data_operacao.strftime('%Y-%m-%d %H:%M:%S'),
                'lucro': lucro,
                'percentual': round(percentual, 2),
                'status': 'VENDIDO' if relatorio.preco_venda > 0 else 'EM CARTEIRA'
            })
            
        return jsonify({
            'total': len(resultado),
            'relatorios': resultado
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 