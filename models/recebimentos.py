from sqlalchemy import Column, Integer, String, Numeric, Date
from database import Base

class Recebimentos(Base):
    __tablename__ = "recebimentos"

    empresa_id = Column("empresa_id", Integer, primary_key=True)
    data_movimento = Column("data_movimento", Date, primary_key=True)
    nome = Column("nome", String, primary_key=True)
    valor = Column("valor", Numeric(14, 2))

    def __init__(self, empresa_id, data_movimento, nome, valor):
        self.empresa_id = empresa_id
        self.data_movimento = data_movimento
        self.nome = nome
        self.valor = valor