from sqlalchemy import Column, Integer, String, Numeric, Boolean, Date, Date
from database import Base


class Itens(Base):
    __tablename__ = "itens"

    empresa_id = Column("empresa_id", Integer, primary_key=True)
    id = Column("id", Integer, primary_key=True)
    nome = Column("nome", String)
    ativo = Column("ativo", Boolean)
    permitir_desconto = Column("permitir_desconto", Boolean)
    nome_grupo = Column("nome_grupo", String)
    nome_subgrupo = Column("nome_subgrupo", String)
    nome_classe = Column("nome_classe", String)
    sigla = Column("sigla", String)
    preco_custo = Column("preco_custo", Numeric(14, 4))
    preco_zero = Column("preco_zero", Numeric(14, 4))
    preco_venda = Column("preco_venda", Numeric(14, 4))
    preco_promocao = Column("preco_promocao", Numeric(14, 4))
    preco_pmc = Column("preco_pmc", Numeric(14, 4))
    saldo_estoque = Column("saldo_estoque", Numeric(14, 4))
    desconto_maximo = Column("desconto_maximo", Numeric(4, 2))
    data_fim_promocao = Column("data_fim_promocao", Date)
    data_inicio_promocao = Column("data_inicio_promocao", Date)
    data_registro = Column("data_registro", Date)

    def __init__(self, empresa_id, id, nome, ativo, permitir_desconto, nome_grupo, 
                 nome_subgrupo, nome_classe, sigla, preco_custo, preco_zero, preco_venda, 
                 preco_promocao, preco_pmc, saldo_estoque, desconto_maximo, data_fim_promocao, 
                 data_inicio_promocao, data_registro):
        self.empresa_id = empresa_id
        self.id = id
        self.nome = nome
        self.ativo = ativo
        self.permitir_desconto = permitir_desconto
        self.nome_grupo = nome_grupo
        self.nome_subgrupo = nome_subgrupo
        self.nome_classe = nome_classe
        self.sigla = sigla
        self.preco_custo = preco_custo
        self.preco_zero = preco_zero
        self.preco_venda = preco_venda
        self.preco_promocao = preco_promocao
        self.preco_pmc = preco_pmc
        self.saldo_estoque = saldo_estoque
        self.desconto_maximo = desconto_maximo
        self.data_fim_promocao = data_fim_promocao
        self.data_inicio_promocao = data_inicio_promocao
        self.data_registro = data_registro