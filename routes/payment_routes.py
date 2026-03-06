from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from dependecies import pegar_sessao
from models.pagamentos import Pagamentos
from schemas import (
    RecebPagamListSchema,
    TiposRecebPagamSchema,
    RecebPagamListResponseSchema
)

payment_router = APIRouter(prefix="/pagamentos", tags=["pagamentos"])

@payment_router.get(
    "/listar/{empresa_id}",
    response_model=RecebPagamListResponseSchema
)
async def listar_pagamentos(
    empresa_id: int,
    data_inicial: date = Query(..., description="Data inicial (YYYY-MM-DD)"),
    data_final: date = Query(..., description="Data final (YYYY-MM-DD)"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    session: Session = Depends(pegar_sessao)
):
    skip = (page - 1) * size
    pagamentos_query = session.query(Pagamentos).filter(
        Pagamentos.empresa_id == empresa_id
    )
    if data_inicial and data_final:
        pagamentos_query = pagamentos_query.filter(
            Pagamentos.data_movimento.between(data_inicial, data_final)
        )
    todos_pagamentos = pagamentos_query.all()

    if not todos_pagamentos:
        raise HTTPException(
            status_code=400,
            detail="Não foram encontrados pagamentos para a referida empresa (empresa_id) no período especificado"
        )
    resultado = {}

    for r in todos_pagamentos:
        data = r.data_movimento
        if data not in resultado:
            resultado[data] = {
                "data_movimento": data,
                "total_dia": Decimal("0"),
                "tipos": {
                    "pix": Decimal("0"),
                    "dinheiro": Decimal("0"),
                    "duplicata": Decimal("0"),
                }
            }

        resultado[data]["total_dia"] += r.valor

        nome = r.nome.lower()
        if nome in resultado[data]["tipos"]:
            resultado[data]["tipos"][nome] += r.valor

    lista_dias = list(resultado.values())
    total_faturamento = sum(d["total_dia"] for d in lista_dias)
    lista_dias = lista_dias[skip: skip + size]

    resposta = [
        RecebPagamListSchema(
            data_movimento=v["data_movimento"],
            total_dia=v["total_dia"],
            tipos=TiposRecebPagamSchema(**v["tipos"])
        )
        for v in lista_dias
    ]
    return RecebPagamListResponseSchema(
        total_faturamento=total_faturamento,
        recebimentos=resposta
    )