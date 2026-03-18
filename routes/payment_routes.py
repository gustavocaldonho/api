from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import date
from dependecies import pegar_sessao
from models.pagamentos import Pagamentos
from utils.utils import converter_data, get_skip

payment_router = APIRouter(prefix="/pagamentos", tags=["pagamentos"])

@payment_router.get("/listar/{empresa_id}")
async def listar_pagamentos(
    empresa_id: int,
    data_inicial: str,
    data_final: str,
    page: int = 0,
    size: int = 10,
    session: Session = Depends(pegar_sessao)
):
    new_data_inicial = converter_data(data_inicial)
    new_data_final = converter_data(data_final)

    pagamentos = (
        session.query(
            Pagamentos.data_movimento,
            Pagamentos.nome,
            func.sum(Pagamentos.valor).label("total_tipo")
        )
        .filter(Pagamentos.empresa_id == empresa_id)
        .filter(Pagamentos.data_movimento.between(new_data_inicial, new_data_final))
        .group_by(Pagamentos.data_movimento, Pagamentos.nome)
        .order_by(Pagamentos.data_movimento)
        .all()
    )
    # if not pagamentos:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Não foram encontrados pagamentos para a empresa no período especificado"
    #     )
    # Agrupar por data
    resultado = {}
    for p in pagamentos:
        data = p.data_movimento
        if data not in resultado:
            resultado[data] = {
                "data_movimento": data,
                "total_dia": Decimal("0"),
                "tipos": []
            }
        resultado[data]["tipos"].append({
            "nome": p.nome,
            "total": p.total_tipo
        })
        resultado[data]["total_dia"] += p.total_tipo

    lista_pagamentos = list(resultado.values())
    # total do período
    total_periodo = sum(d["total_dia"] for d in lista_pagamentos)
    # paginação
    inicio = get_skip(page, size)
    fim = inicio + size
    query_paginada = lista_pagamentos[inicio:fim]

    return {
        "total_periodo": total_periodo,
        "pagamentos": query_paginada
    }

@payment_router.get(
    "/total_periodo/{empresa_id}"
)
async def total_periodo_pagamentos(
    empresa_id: int,
    data_inicial: str,
    data_final: str,
    session: Session = Depends(pegar_sessao)
):
    new_data_inicial = converter_data(data_inicial)
    new_data_final = converter_data(data_final)

    total_periodo = (
        session.query(
            func.coalesce(func.sum(Pagamentos.valor), 0)
        )
        .filter(Pagamentos.empresa_id == empresa_id)
        .filter(Pagamentos.data_movimento.between(new_data_inicial, new_data_final))
        .scalar()
    )

    # valor_formatado = formatar_decimal(total_periodo)
    return {
        "total_periodo": total_periodo
    }