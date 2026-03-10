from pydantic import BaseModel
from typing import Optional, List

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