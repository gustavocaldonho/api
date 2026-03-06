from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from dependecies import pegar_sessao
from models.recebimentos import Recebimentos
from schemas import (
    RecebPagamListSchema,
    TiposRecebPagamSchema,
    RecebPagamListResponseSchema
)

receipt_router = APIRouter(prefix="/recebimentos", tags=["recebimentos"])

@receipt_router.get(
    "/listar/{empresa_id}",
    response_model=RecebPagamListResponseSchema
)
async def listar_recebimentos(
    empresa_id: int,
    data_inicial: date = Query(..., description="Data inicial (YYYY-MM-DD)"),
    data_final: date = Query(..., description="Data final (YYYY-MM-DD)"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    session: Session = Depends(pegar_sessao)
):
    skip = (page - 1) * size
    recebimentos_query = session.query(Recebimentos).filter(
        Recebimentos.empresa_id == empresa_id
    )
    if data_inicial and data_final:
        recebimentos_query = recebimentos_query.filter(
            Recebimentos.data_movimento.between(data_inicial, data_final)
        )
    todos_recebimentos = recebimentos_query.all()

    if not todos_recebimentos:
        raise HTTPException(
            status_code=400,
            detail="Não foram encontrados recebimentos para a referida empresa (empresa_id) no período especificado"
        )
    resultado = {}

    for r in todos_recebimentos:
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