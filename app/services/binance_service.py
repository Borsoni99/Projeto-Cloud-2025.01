from binance.client import Client
from binance.exceptions import BinanceAPIException
from decimal import Decimal
from app.config.config import Config

class BinanceService:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret, testnet=True)  # Using mainnet

    def get_symbol_info(self, symbol: str):
        """
        Get symbol information including quantity precision
        """
        try:
            info = self.client.get_symbol_info(symbol)
            return {
                'success': True,
                'info': info
            }
        except BinanceAPIException as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_symbol_price(self, symbol: str):
        """
        Obtém o último preço de uma moeda na Binance
        """
        try:
            price = self.client.get_symbol_ticker(symbol=symbol)
            return {
                'success': True,
                'price': price['price']
            }
        except BinanceAPIException as e:
            return {
                'success': False,
                'error': str(e)
            }

    def create_order(self, symbol: str, side: str, quantity: float, price: float = None, order_type: str = 'LIMIT', time_in_force: str = 'GTC', is_test: bool = False):
        """
        Cria uma ordem na Binance
        Args:
            symbol: Símbolo do par de trading (ex: 'BTCUSDT')
            side: Lado da ordem ('BUY' ou 'SELL')
            quantity: Quantidade da ordem
            price: Preço para ordens limit (opcional)
            order_type: Tipo de ordem ('MARKET' ou 'LIMIT')
            time_in_force: Tempo em vigor para ordens limit ('GTC', 'IOC', 'FOK')
            is_test: Se True, cria uma ordem de teste
        """
        try:
            params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'quantity': quantity
            }
            
            # Adiciona parâmetros específicos para ordens limit
            if order_type == 'LIMIT':
                if not price:
                    raise ValueError('Preço é obrigatório para ordens limit')
                params['price'] = price
                params['timeInForce'] = time_in_force
                
            # Usa create_test_order se is_test for True
            order_method = self.client.create_test_order if is_test else self.client.create_order
            order = order_method(**params)
            
            return {
                'success': True,
                'order': order
            }
        except BinanceAPIException as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_binance_trading_pairs(self):
        """
        Obtém todos os pares de trading disponíveis na Binance
        """
        try:
            exchange_info = self.client.get_exchange_info()
            trading_pairs = [symbol['symbol'] for symbol in exchange_info['symbols'] if symbol['status'] == 'TRADING']
            return trading_pairs
        except BinanceAPIException as e:
            print(f"Erro da API Binance: {e}")
            return []
        except Exception as e:
            print(f"Erro ao buscar pares de trading: {e}")
            return []

