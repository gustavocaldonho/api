
from sqlalchemy import Column, String, Integer, Date, Numeric, Boolean
from database import Base

class Pessoas(Base):
    __tablename__ = "pessoas"

    empresa_id = Column("empresa_id", Integer, primary_key=True)
    id = Column("id", Integer, primary_key=True)
    nome = Column("nome", String)
    ativo = Column("ativo", Boolean)
    fisica_juridica = Column("fisica_juridica", Numeric(1,0))
    cpf_cnpj = Column("cpf_cnpj", String)
    data_nascimento = Column("data_nascimento", Date)
    data_cadastro = Column("data_cadastro", Date)
    limite_credito = Column("limite_credito", Numeric(12,2))
    rg_ie = Column("rg_ie", String)
    sexo = Column("sexo", Numeric(1,0))
    credito_encerrado = Column("credito_encerrado", Boolean)
    mae = Column("mae", String)
    vendedor_codigo = Column("vendedor_codigo", Integer)
    data_registro = Column("data_registro", Date)
    qtd_dupl_pagas = Column("qtd_dupl_pagas", Numeric(8,0))
    qtd_dupl_atrasadas = Column("qtd_dupl_atrasadas", Numeric(8,0))
    qtd_dupl_avencer = Column("qtd_dupl_avencer", Numeric(8,0))
    total_pago = Column("total_pago", Numeric(10,2))
    total_atrasado = Column("total_atrasado", Numeric(10,2))
    total_avencer = Column("total_avencer", Numeric(10, 2))
    dias_maior_atraso = Column("dias_maior_atraso", Numeric(8,0))
    dias_maior_avencer = Column("dias_maior_avencer", Numeric(8,0))

    def __init__(self, empresa_id, id, nome, fisica_juridica, cpf_cnpj, data_nascimento,
                 data_cadastro, limite_credito, rg_ie, sexo, credito_encerrado, mae, vendedor_codigo,
                 data_registro, qtd_dupl_pagas, qtd_dupl_atrasadas, qtd_dupl_avencer, total_pago,
                 total_atrasado, total_avencer, dias_maior_atraso, dias_maior_avencer, ativo=True):
        self.empresa_id = empresa_id
        self.id = id
        self.nome = nome
        self.ativo = ativo
        self.fisica_juridica = fisica_juridica
        self.cpf_cnpj = cpf_cnpj
        self.data_nascimento = data_nascimento
        self.data_cadastro = data_cadastro
        self.limite_credito = limite_credito
        self.rg_ie = rg_ie
        self.sexo = sexo
        self.credito_encerrado = credito_encerrado
        self.mae = mae
        self.vendedor_codigo = vendedor_codigo
        self.data_registro = data_registro
        self.qtd_dupl_pagas = qtd_dupl_pagas
        self.qtd_dupl_atrasadas = qtd_dupl_atrasadas
        self.qtd_dupl_avencer = qtd_dupl_avencer
        self.total_pago = total_pago
        self.total_atrasado = total_atrasado
        self.total_avencer = total_avencer
        self.dias_maior_atraso = dias_maior_atraso
        self.dias_maior_avencer = dias_maior_avencer