from dataclasses import dataclass
from decimal import Decimal

@dataclass
class OrdemFillResponse:
    quantidade: Decimal
    preco: Decimal 