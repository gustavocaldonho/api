from sqlalchemy import Column, String, Integer, Boolean, Numeric, Date
from database import Base

class Cidades(Base):
    __tablename__ = "cidades"

    empresa_id = Column("empresa_id", Integer, primary_key=True)
    id = Column("id", Integer, primary_key=True)
    nome = Column("nome", String)
    ativo = Column("ativo", Boolean)
    uf = Column("uf", String)
    valor_disk_entrega = Column("valor_disk_entrega", Numeric(8,2))
    data_registro = Column("data_registro", Date)

    def __init__(self, empresa_id, nome, uf, valor_disk_entrega, 
                data_registro, ativo=True):
        self.empresa_id = empresa_id
        self.nome = nome
        self.ativo = ativo
        self.uf = uf
        self.valor_disk_entrega = valor_disk_entrega
        self.data_registro = data_registro