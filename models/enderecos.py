
from sqlalchemy import Column, String, Integer, Date, Numeric, Boolean
from database import Base

# ainda não foi feita a migração do banco - CRIAR OS MODELS DE 'BAIRROS' E 'CIDADES'
class Enderecos(Base):
    __tablename__ = "enderecos"

    empresa_id = Column("empresa_id", Integer, primary_key=True)
    pessoa_id = Column("pessoa_id", Integer, primary_key=True)
    sequencia = Column("sequencia", Integer, primary_key=True)
    nome = Column("nome", String)
    ativo = Column("ativo", Boolean)
    bairro_id = Column("bairro_id", Integer)
    cidade_id = Column("cidade_id", Integer)
    logradouro = Column("logradouro", String)
    numero = Column("numero", String)
    complemento = Column("complemento", String)
    cep = Column("cep", String)
    tipo = Column("tipo", Integer)
    padrao = Column("padrao", Boolean)
    ponto_referencia = Column("ponto_referencia", String)
    data_registro = Column("data_registro", Date)

    def __init__(self, empresa_id, pessoa_id, sequencia, nome, ativo, bairro_id, cidade_id, logradouro, 
                 numero, complemento, cep, tipo, padrao, ponto_referencia, data_registro):
        self.empresa_id = empresa_id
        self.pessoa_id = pessoa_id
        self.sequencia = sequencia
        self.nome = nome
        self.ativo = ativo
        self.bairro_id = bairro_id
        self.cidade_id = cidade_id
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.cep = cep
        self.tipo = tipo
        self.padrao = padrao
        self.ponto_referencia = ponto_referencia
        self.data_registro = data_registro