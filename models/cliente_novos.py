from sqlalchemy import Column, Integer, String, Numeric, Date
from database import Base

class ClienteNovos(Base):
    __tablename__ = "cliente_novos"

    id = Column("id", Integer, primary_key=True)
    empresa_id = Column("empresa_id", Integer)
    nome = Column("nome", String)
    endereco = Column("endereco", String)
    bairro_id = Column("bairro_id", Integer)
    cidade_id = Column("cidade_id", Integer)
    cpf_cnpj = Column("cpf_cnpj", String)
    rg_ie = Column("rg_ie", String)
    fone = Column("fone", String)
    celular = Column("celular", String)
    nome_fantasia = Column("nome_fantasia", String)
    email = Column("email", String)
    sexo = Column("sexo", Numeric(1, 0))
    data_nascimento = Column("data_nascimento", Date)
    limite_credito = Column("limite_credito", Numeric(10, 2))
    fisica_juridica = Column("fisica_juridica", Numeric(1, 0))
    numero = Column("numero", String)
    cep = Column("cep", String)

    def __init__(self, empresa_id, nome, endereco, bairro_id, cidade_id, cpf_cnpj, rg_ie, 
                 fone, celular, nome_fantasia, email, sexo, data_nascimento, limite_credito, 
                 fisica_juridica, numero, cep):
        self.empresa_id = empresa_id
        self.nome = nome
        self.endereco = endereco
        self.bairro_id = bairro_id
        self.cidade_id = cidade_id
        self.cpf_cnpj = cpf_cnpj
        self.rg_ie = rg_ie
        self.fone = fone
        self.celular = celular
        self.nome_fantasia = nome_fantasia
        self.email = email
        self.sexo = sexo
        self.data_nascimento = data_nascimento
        self.limite_credito = limite_credito
        self.fisica_juridica = fisica_juridica
        self.numero = numero
        self.cep = cep