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