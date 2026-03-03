from sqlalchemy import Column, Integer, String, TIMESTAMP
from database import Base

class PessoaContatos(Base):
    __tablename__ = "pessoa_contatos"

    empresa_id = Column("empresa_id", Integer, primary_key=True)
    pessoa_id = Column("pessoa_id", Integer, primary_key=True)
    sequencia = Column("sequencia", Integer, primary_key=True)
    nome = Column("nome", String)
    tipo = Column("tipo", Integer)
    contato = Column("contato", String)
    data_registro = Column("data_registro", TIMESTAMP)

    def __init__(self, empresa_id, pessoa_id, sequencia, nome, tipo, contato, data_registro):
        self.empresa_id = empresa_id
        self.pessoa_id = pessoa_id
        self.sequencia = sequencia
        self.nome = nome
        self.tipo = tipo
        self.contato = contato
        self.data_registro = data_registro