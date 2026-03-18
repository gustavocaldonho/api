from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import date
from dependecies import pegar_sessao
from models.recebimentos import Recebimentos
from utils.utils import get_skip, converter_data

receipt_router = APIRouter(prefix="/recebimentos", tags=["recebimentos"])

@receipt_router.get(
    "/listar/{empresa_id}"
)
async def listar_recebimentos(
    empresa_id: int,
    data_inicial: str,
    data_final: str,
    page: int = 0,
    size: int = 10,
    session: Session = Depends(pegar_sessao)
):
    new_data_inicial = converter_data(data_inicial)
    new_data_final = converter_data(data_final)

    recebimentos = (
        session.query(
            Recebimentos.data_movimento,
            Recebimentos.nome,
            func.sum(Recebimentos.valor).label("total_tipo")
        )
        .filter(Recebimentos.empresa_id == empresa_id)
        .filter(Recebimentos.data_movimento.between(new_data_inicial, new_data_final))
        .group_by(Recebimentos.data_movimento, Recebimentos.nome)
        .order_by(Recebimentos.data_movimento)
        .all()
    )
    # if not recebimentos:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Não foram encontrados recebimentos para a referida empresa (empresa_id) no período especificado"
    #     )
    # agrupar por data
    resultado = {}
    for r in recebimentos:
        data = r.data_movimento
        if data not in resultado:
            resultado[data] = {
                "data_movimento": data,
                "total_dia": Decimal("0"),
                "tipos": []
            }
        resultado[data]["tipos"].append({
            "nome": r.nome,
            "total": r.total_tipo 
        })
        resultado[data]["total_dia"] += r.total_tipo

    lista_recebimentos = list(resultado.values())
    # total do período
    total_periodo = sum(d["total_dia"] for d in lista_recebimentos)
    # paginação
    inicio = get_skip(page, size)
    fim = inicio + size
    query_paginada = lista_recebimentos[inicio:fim]

    return {
        "total_periodo": total_periodo,
        "recebimentos": query_paginada
    }


@receipt_router.get(
    "/total_periodo/{empresa_id}"
)
async def total_periodo_recebimentos(
    empresa_id: int,
    data_inicial: str,
    data_final: str,
    session: Session = Depends(pegar_sessao)
):
    new_data_inicial = converter_data(data_inicial)
    new_data_final = converter_data(data_final)

    total_periodo = (
        session.query(
            func.coalesce(func.sum(Recebimentos.valor), 0)
        )
        .filter(Recebimentos.empresa_id == empresa_id)
        .filter(Recebimentos.data_movimento.between(new_data_inicial, new_data_final))
        .scalar()
    )

    if total_periodo == 0:
        total_periodo = 10.11

    return {"total_periodo": total_periodo}