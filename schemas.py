from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional, List

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    # sera interpretado como orm e nao como dicionario
    class Config:
        from_attributes = True

class PedidoSchema(BaseModel):
    id_usuario: int

    class Config:
        from_attributes = True 

# class LoginSchema(BaseModel):
#     email: str
#     senha: str

#     class Config:
#         from_attributes = True

class LoginSchema(BaseModel):
    empresa_id: int
    usuario: str
    senha: str

    class Config:
        from_attributes = True

class ItemPedidoSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float
    # id_pedido -> nao precisa pois ja eh passado na rota de adicionar item ao pedido

    class Config:
        from_attributes = True

class ResponsePedidoSchema(BaseModel):
    id: int
    status: str
    preco: float
    itens: List[ItemPedidoSchema]

    class Config:
        from_attributes = True

class VendedorSchema(BaseModel):
    vendedor_id: int
    usuario: str

    class Config:
        from_attributes = True

class ResponseVisualizarVendedoresSchema(BaseModel):
    id_empresa: int
    nome_empresa: str
    vendedores: List[VendedorSchema]

    class Config:
        from_attributes = True

class VisualizarClientesSchema(BaseModel):
    nome_pessoa: str # Pessoas
    logradouro: Optional[str] = None  # Endereco
    numero: Optional[str] = None  # Endereco
    complemento: Optional[str] = None # Endereco
    bairro: Optional[str] = None # Bairro
    cidade: Optional[str] = None # Cidades
    cep: Optional[str] = None # Endereco
    ponto_referencia: Optional[str] = None # Endereco
    uf: Optional[str] = None  # Cidades
    contato: Optional[str] = None # PessoaContatos
    limite_credito: float # Pessoas

    class Config:
        from_attributes = True

class VisualizarItensSchema(BaseModel):
    id: int
    nome: str 
    ativo: bool 
    permitir_desconto: bool 
    nome_grupo: str 
    nome_subgrupo: str 
    nome_classe: str 
    sigla: str 
    preco_custo: Decimal 
    preco_zero: Decimal 
    preco_venda: Decimal 
    preco_promocao: Decimal 
    preco_pmc: Decimal 
    saldo_estoque: Decimal 
    desconto_maximo: Decimal 
    data_fim_promocao: Optional[date] = None
    data_inicio_promocao: Optional[date] = None
    data_registro: datetime 

    class Config:
        from_attributes = True

class PreVendaItemCreateSchema(BaseModel):
    sequencia: int
    item_id: int
    quantidade: Decimal
    valor_venda: Decimal
    valor_promocao: Decimal
    valor_desconto: Decimal

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
