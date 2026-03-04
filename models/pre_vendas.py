from sqlalchemy import Column, Integer, String, Numeric, Boolean, Date
from database import Base

class PreVendas(Base):
    __tablename__ = "pre_vendas"

    empresa_id = Column("empresa_id", Integer, primary_key=True)
    id = Column("id", Integer, primary_key=True)
    destinatario_id = Column("destinatario_id", Integer)
    vendedor_id = Column("vendedor_id", Integer)
    condicao_pagamento_id = Column("condicao_pagamento_id", Integer)
    data_registro = Column("data_registro", Date)
    data_movimento = Column("data_movimento", Date)
    numero = Column("numero", Integer)
    disk_entrega = Column("disk_entrega", Boolean)
    enviado = Column("enviado", Boolean)
    observacao = Column("observacao", String)
    ide_mobile = Column("ide_mobile", String)
    qtd_vezes = Column("qtd_vezes", Numeric(2, 0), default=0)

    def __init__(self, empresa_id, id, destinatario_id, vendedor_id, condicao_pagamento_id, 
                 data_registro, data_movimento, numero, disk_entrega, enviado, observacao, 
                 ide_mobile, qtd_vezes):
        self.empresa_id = empresa_id
        self.id = id
        self.destinatario_id = destinatario_id
        self.vendedor_id = vendedor_id
        self.condicao_pagamento_id = condicao_pagamento_id
        self.data_registro = data_registro
        self.data_movimento = data_movimento
        self.numero = numero
        self.disk_entrega = disk_entrega
        self.enviado = enviado
        self.observacao = observacao
        self.ide_mobile = ide_mobile
        self.qtd_vezes = qtd_vezes