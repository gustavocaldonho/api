from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional, List

class VisualizarItensSchema(BaseModel):
    id: int
    nome: str 
    ativo: bool 
    permitir_desconto: bool 
    nome_grupo: str 
    nome_subgrupo: str 
    nome_classe: str 
    sigla: str 
    preco_custo: float
    preco_zero: float
    preco_venda: float
    preco_promocao: float
    preco_pmc: float
    saldo_estoque: int
    desconto_maximo: float
    data_fim_promocao: Optional[date] = None
    data_inicio_promocao: Optional[date] = None
    data_registro: datetime 

    class Config:
        from_attributes = True

class PreVendaItemCreateSchema(BaseModel):
    sequencia: int
    item_id: int
    quantidade: int
    valor_venda: float
    valor_promocao: float
    valor_desconto: float

    class Config:
        from_attributes = True

class PreVendaCreateSchema(BaseModel):
    empresa_id: int
    destinatario_id: int
    vendedor_id: int
    condicao_pagamento_id: int
    # desconto_geral: Decimal # não tem na tabela PreVenda
    numero: int
    disk_entrega: bool
    enviado: bool
    observacao: str
    ide_mobile: str
    qtd_vezes: int
    itens: List[PreVendaItemCreateSchema]

    class Config:
        from_attributes = True