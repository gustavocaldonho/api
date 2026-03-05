from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from dependecies import pegar_sessao
from models.faturamentos import Faturamentos
from sqlalchemy import func
from decimal import Decimal, ROUND_HALF_UP

revenue_router = APIRouter(prefix="/faturamentos", tags=["faturamentos"])

@revenue_router.get(
    "/listar_faturamentos/diario/{empresa_id}",
)
async def listar_faturamentos_diario(
    empresa_id: int,
    data_inicial: date = Query(..., description="Data inicial (YYYY-MM-DD)"),
    data_final: date = Query(..., description="Data final (YYYY-MM-DD)"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    session: Session = Depends(pegar_sessao)
):
    skip = (page - 1) * size
    # agrupando por data_movimento e somando o valor
    faturamentos = (
        session.query(
            Faturamentos.data_movimento,
            func.sum(Faturamentos.valor_total).label("total_dia")
        )
        .filter(Faturamentos.empresa_id == empresa_id)
        .filter(Faturamentos.data_movimento.between(data_inicial, data_final))
        .group_by(Faturamentos.data_movimento)
        .order_by(Faturamentos.data_movimento)
        .all()
    )
    if not faturamentos:
        raise HTTPException(
            status_code=400,
            detail="Não foram encontrados faturamentos para a referida empresa no período especificado"
        )
    # total do período
    total_periodo = sum(r.total_dia for r in faturamentos)
    # paginação
    query_paginada = faturamentos[skip: skip + size]
    # montar resposta
    dados = []
    for r in query_paginada:
        porcentagem = ((r.total_dia / total_periodo) * 100 if total_periodo else Decimal("0")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        dados.append(
            {
                "data_movimento": r.data_movimento,
                "total_dia": r.total_dia,
                "porcentagem": porcentagem
            }
        )
    return {
        "total_faturamento": total_periodo,
        "faturamentos": dados
    }

@revenue_router.get(
    "/listar_faturamentos/vendedor/{empresa_id}",
)
async def listar_faturamentos_vendedor(
    empresa_id: int,
    data_inicial: date = Query(..., description="Data inicial (YYYY-MM-DD)"),
    data_final: date = Query(..., description="Data final (YYYY-MM-DD)"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    session: Session = Depends(pegar_sessao)
):
    skip = (page - 1) * size

    # ESTÁ MOSTRANDO O VENDEDOR_ID -> TROCAR PARA MOSTRAR O NOME DO VENDEDOR -> PRECISA FAZER JOIN COM A TABELA DE USUÁRIOS_INTEGRA (USUÁRIOS_INTEGRA  TEM O NOME DO VENDEDOR)

    # agrupando por vendedor e somando o valor
    faturamentos = (
        session.query(
            Faturamentos.vendedor_id,
            func.sum(Faturamentos.valor_total).label("total_dia")
        )
        .filter(Faturamentos.empresa_id == empresa_id)
        .filter(Faturamentos.data_movimento.between(data_inicial, data_final))
        .group_by(Faturamentos.vendedor_id)
        # .order_by(Faturamentos.data_movimento)
        .all()
    )
    if not faturamentos:
        raise HTTPException(
            status_code=400,
            detail="Não foram encontrados faturamentos para a referida empresa no período especificado"
        )
    # total do período
    total_periodo = sum(r.total_dia for r in faturamentos)
    # paginação
    query_paginada = faturamentos[skip: skip + size]
    # montar resposta
    dados = []
    for r in query_paginada:
        porcentagem = ((r.total_dia / total_periodo) * 100 if total_periodo else Decimal("0")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        dados.append(
            {
                "vendedor_id": r.vendedor_id,
                "total_dia": r.total_dia,
                "porcentagem": porcentagem
            }
        )
    return {
        "total_faturamento": total_periodo,
        "faturamentos": dados
    }