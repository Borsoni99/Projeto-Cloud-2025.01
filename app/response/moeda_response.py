from dataclasses import dataclass
from decimal import Decimal
 
@dataclass
class MoedaResponse:
    simbolo: str
    ultimo_preco: Decimal 