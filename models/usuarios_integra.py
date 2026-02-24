from sqlalchemy import Column, String, Integer, Date, Numeric
from database import Base

class Usuarios_Integra(Base):
    __tablename__ = "usuarios_integra"

    empresa_id = Column("empresa_id", Integer, primary_key=True, nullable=False)
    usuario = Column("usuario", String, primary_key=True, nullable=False)
    senha = Column("senha", String)
    vendedor_id = Column("vendedor_id", Integer, nullable=False)
    consultar_pessoas = Column("consultar_pessoas", String) 
    consultar_itens = Column("consultar_itens", String)
    consultar_faturamentos = Column("consultar_faturamentos", String)
    consultar_recebimentos = Column("consultar_recebimentos", String)
    efetuar_pre_vendas = Column("efetuar_pre_vendas", String)
    data_registro = Column("data_registro", Date)
    consultar_pagamentos = Column("consultar_pagamentos", String)
    desconto_maximo = Column("desconto_maximo", Numeric(4,2))
    digitar_preco_venda = Column("digitar_preco_venda", String)
    gerar_gordura_precos = Column("gerar_gordura_precos", String)
    total_gordura = Column("total_gordura", Numeric(10,2))

    def __init__(self, empresa_id, usuario, senha, vendedor_id, data_registro, total_gordura, 
                 consultar_pessoas=0, consultar_itens=0, consultar_faturamentos=0, 
                 consultar_recebimentos=0, efetuar_pre_vendas=0, consultar_pagamentos=0, 
                 desconto_maximo=0, digitar_preco_venda=0, gerar_gordura_precos=0):
        self.empresa_id = empresa_id
        self.usuario = usuario
        self.senha = senha
        self.vendedor_id = vendedor_id 
        self.consultar_pessoas = consultar_pessoas
        self.consultar_itens = consultar_itens
        self.consultar_faturamentos = consultar_faturamentos
        self.consultar_recebimentos = consultar_recebimentos
        self.efetuar_pre_vendas = efetuar_pre_vendas
        self.data_registro = data_registro
        self.consultar_pagamentos = consultar_pagamentos
        self.desconto_maximo = desconto_maximo
        self.digitar_preco_venda = digitar_preco_venda
        self.gerar_gordura_precos = gerar_gordura_precos
        self.total_gordura = total_gordura