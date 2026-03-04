from sqlalchemy import Column, Integer, String, Numeric, Date, Text
from database import Base

class Xmls(Base):
    __tablename__ = "xmls"

    empresa_id = Column("empresa_id", Integer, primary_key=True)
    id = Column("id", Integer, primary_key=True)
    modelo = Column("modelo", Numeric(2, 0))
    serie = Column("serie", Numeric(2, 0))
    numero = Column("numero", Numeric(12, 0))
    chave_xml = Column("chave_xml", String)
    xml = Column("xml", Text)
    data_registro = Column("data_registro", Date)
    data_movimento = Column("data_movimento", Date)
    entrada_saida = Column("entrada_saida", Numeric(1, 0), default=1)

    def __init__(self, empresa_id, id, modelo, serie, numero, chave_xml, xml, 
                 data_registro, data_movimento, entrada_saida):
        self.empresa_id = empresa_id
        self.id = id
        self.modelo = modelo
        self.serie = serie
        self.numero = numero
        self.chave_xml = chave_xml
        self.xml = xml
        self.data_registro = data_registro
        self.data_movimento = data_movimento
        self.entrada_saida = entrada_saida