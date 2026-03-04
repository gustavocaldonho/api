from sqlalchemy import Column, Integer, Numeric
from database import Base


class PreVendaItens(Base):
    __tablename__ = "pre_venda_itens"

    empresa_id = Column("empresa_id", Integer, primary_key=True)
    pre_venda_id = Column("pre_venda_id", Integer, primary_key=True)
    sequencia = Column("sequencia", Integer, primary_key=True)
    item_id = Column("item_id", Integer)
    quantidade = Column("quantidade", Numeric(12, 4))
    valor_venda = Column("valor_venda", Numeric(12, 4))
    valor_promocao = Column("valor_promocao", Numeric(12, 4))
    valor_desconto = Column("valor_desconto", Numeric(12, 4))

    def __init__(self, empresa_id, pre_venda_id, sequencia, item_id, quantidade, valor_venda, 
                 valor_promocao, valor_desconto):
        self.empresa_id = empresa_id
        self.pre_venda_id = pre_venda_id
        self.sequencia = sequencia
        self.item_id = item_id
        self.quantidade = quantidade
        self.valor_venda = valor_venda
        self.valor_promocao = valor_promocao
        self.valor_desconto = valor_desconto