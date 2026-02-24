from sqlalchemy import Column, String, Integer, Boolean, Date, Numeric
from database import Base

class Empresas(Base):
    __tablename__ = "empresas"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    empresa_cnpj = Column("empresa_cnpj", String)
    nome = Column("nome", String)
    data_vencimento = Column("data_vencimento", Date)
    data_registro = Column("data_registro", Date) 
    cpf_contabilista = Column("cpf_contabilista", String)
    contador = Column("contador", Boolean, default=False)
    senha = Column("senha", String)
    razao_social = Column("razao_social", String)
    celular_ativo = Column("celular_ativo", Boolean, default=False)
    disk_entrega_item_id = Column("disk_entrega_item_id", Numeric(14,0))
    data_ultimo_acesso = Column("data_ultimo_acesso", Date)
    qtd_bulas = Column("qtd_bulas", Numeric(10,0), default=0)
    qtd_imagens = Column("qtd_imagens", Numeric(10,0), default=0)

    def __init__(self, cnpj, nome, data_vencimento, data_registro, 
                 cpf_contabilista, senha, razao_social, 
                 disk_entrega_item_id, data_ultimo_acesso, contador=False, celular_ativo=False, qtd_bulas=0, 
                 qtd_imagens=0):
        self.empresa_cnpj = cnpj
        self.nome = nome
        self.data_vencimento = data_vencimento
        self.data_registro = data_registro
        self.cpf_contabilista = cpf_contabilista
        self.contador = contador
        self.senha = senha
        self.razao_social = razao_social
        self.celular_ativo = celular_ativo
        self.disk_entrega_item_id = disk_entrega_item_id
        self.data_ultimo_acesso = data_ultimo_acesso
        self.qtd_bulas = qtd_bulas
        self.qtd_imagens = qtd_imagens