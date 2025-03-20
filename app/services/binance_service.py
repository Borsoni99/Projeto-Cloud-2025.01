from binance.client import Client
from binance.exceptions import BinanceAPIException
from decimal import Decimal

class BinanceService:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret, testnet=True)  # Using testnet

    def create_test_order(self, symbol: str, quantity: float):
        """
        Creates a market buy order on Binance testnet
        """
        try:
            order = self.client.create_test_order(
                symbol=symbol,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
            return {
                'success': True,
                'order': order
            }
        except BinanceAPIException as e:
            return {
                'success': False,
                'error': str(e)
            }

    def create_buy_order(self, symbol: str, quantity: float):
        """
        Creates a real market buy order on Binance testnet
        """
        try:
            order = self.client.create_order(
                symbol=symbol,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
            return {
                'success': True,
                'order': order
            }
        except BinanceAPIException as e:
            return {
                'success': False,
                'error': str(e)
            }

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