from sqlalchemy import Column, String, Integer, Boolean, Date, Numeric
from database import Base

class Bairros(Base):
    __tablename__ = "bairros"

    empresa_id = Column("empresa_id", Integer, primary_key=True)
    id = Column("id", Integer, primary_key=True)
    nome = Column("nome", String)
    ativo = Column("ativo", Boolean)
    cidade_id = Column("cidade_id", Integer)
    valor_disk_entrega = Column("valor_disk_entrega", Numeric(8,2))
    data_registro = Column("data_registro", Date)

    def __init__(self, empresa_id, nome, cidade_id, valor_disk_entrega,
                 data_registro, ativo=True):
        self.empresa_id = empresa_id
        self.nome = nome
        self.ativo = ativo
        self.cidade_id = cidade_id
        self.valor_disk_entrega = valor_disk_entrega
        self.data_registro = data_registro