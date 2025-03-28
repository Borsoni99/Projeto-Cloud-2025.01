from dataclasses import dataclass
from decimal import Decimal
from typing import List
from app.response.ordem_fill_response import OrdemFillResponse

@dataclass
class OrdemResponse:
    simbolo: str
    ordem_id: str
    qtd_executada: Decimal
    tipo: str
    tp_operacao: str
    preco: Decimal
    status: str
    fills: List[dict] 