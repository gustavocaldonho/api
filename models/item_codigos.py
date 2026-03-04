from sqlalchemy import Column, Integer, String, Date
from database import Base


class ItemCodigos(Base):
    __tablename__ = "item_codigos"

    empresa_id = Column("empresa_id", Integer, primary_key=True)
    item_id = Column("item_id", Integer, primary_key=True)
    ean_gtin = Column("ean_gtin", String, primary_key=True)
    data_registro = Column("data_registro", Date)

    def __init__(self, empresa_id, item_id, ean_gtin, data_registro):
        self.empresa_id = empresa_id
        self.item_id = item_id
        self.ean_gtin = ean_gtin
        self.data_registro = data_registro