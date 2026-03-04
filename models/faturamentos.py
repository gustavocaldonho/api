from sqlalchemy import Column, Integer, Numeric, Date, Date
from database import Base

class Faturamentos(Base):
    __tablename__ = "faturamentos"

    empresa_id = Column("empresa_id", Integer, primary_key=True)
    data_movimento = Column("data_movimento", Date, primary_key=True)
    condicao_pagamento_id = Column("condicao_pagamento_id", Integer, primary_key=True)
    vendedor_id = Column("vendedor_id", Integer, primary_key=True)
    valor_total = Column("valor_total", Numeric(14, 4))
    data_registro = Column("data_registro", Date)

    def __init__(self, empresa_id, data_movimento, condicao_pagamento_id, vendedor_id, valor_total, data_registro):
        self.empresa_id = empresa_id
        self.data_movimento = data_movimento
        self.condicao_pagamento_id = condicao_pagamento_id
        self.vendedor_id = vendedor_id
        self.valor_total = valor_total
        self.data_registro = data_registro