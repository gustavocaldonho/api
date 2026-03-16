from decimal import Decimal
from pydantic import BaseModel
from typing import Optional, List

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

class enderecoSchema(BaseModel):
    logradouro: Optional[str]
    numero: Optional[str]
    complemento: Optional[str]
    cep: Optional[str]
    ponto_referencia: Optional[str]
    bairro: Optional[str]
    cidade: Optional[str]
    uf: Optional[str]

    class Config:
        from_attributes = True

class telefoneSchema(BaseModel):
    contato: str

    class Config:
        from_attributes = True

class visualizarPerfilClienteSchema(BaseModel):
    nome: str
    qtd_dupl_pagas: Decimal
    qtd_dupl_atrasadas: Decimal
    qtd_dupl_avencer: Decimal
    total_pago: Decimal
    total_atrasado: Decimal
    total_avencer: Decimal
    total_aberto: Decimal
    dias_maior_atraso: Decimal
    dias_maior_avencer: Decimal
    telefones: List[telefoneSchema]
    enderecos: List[enderecoSchema]

    class Config:
        from_attributes = True

class visualizarResumoClienteSchema(BaseModel):
    id: int
    nome: str
    limite_credito: Decimal
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    cep: Optional[str] = None
    ponto_referencia: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None

    class Config:
        from_attributes = True