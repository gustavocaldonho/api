from sqlalchemy import Column, Integer, String, Numeric, Boolean, Date
from database import Base


class CondicoesPagamentos(Base):
    __tablename__ = "condicoes_pagamentos"
    
    empresa_id = Column("empresa_id", Integer, primary_key=True)
    id = Column("id", Integer, primary_key=True)
    nome = Column("nome", String)
    ativo = Column("ativo", Boolean)
    tipo_id = Column("tipo_id", Integer)
    dias = Column("dias", Numeric(3, 0))
    vezes_max = Column("vezes_max", Numeric(3, 0))
    data_registro = Column("data_registro", Date)

    def __init__(self, empresa_id, id, nome, tipo_id, dias, vezes_max, data_registro, ativo=True):
        self.empresa_id = empresa_id
        self.id = id
        self.nome = nome
        self.ativo = ativo
        self.tipo_id = tipo_id
        self.dias = dias
        self.vezes_max = vezes_max
        self.data_registro = data_registro