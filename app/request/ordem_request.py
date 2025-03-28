from dataclasses import dataclass
from decimal import Decimal

@dataclass
class OrdemRequest:
    simbolo: str
    tp_operacao: str  # 'COMPRA' ou 'VENDA'
    quantidade: Decimal
    preco: Decimal 