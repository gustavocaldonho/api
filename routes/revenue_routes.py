from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from dependecies import pegar_sessao
from models.faturamentos import Faturamentos
from models.usuarios_integra import Usuarios_Integra
from models.condicoes_pagamentos import CondicoesPagamentos
from sqlalchemy import func
from decimal import Decimal, ROUND_HALF_UP
from utils.utils import converter_data, get_skip, obter_dia_semana

revenue_router = APIRouter(prefix="/faturamentos", tags=["faturamentos"])

@revenue_router.get(
    "/listar/diario/{empresa_id}",
)
async def listar_faturamentos_diario(
    empresa_id: int,
    data_inicial: str,
    data_final: str,
    page: int = 0,
    size: int = 10,
    session: Session = Depends(pegar_sessao)
):
    new_data_inicial = converter_data(data_inicial)
    new_data_final = converter_data(data_final)

    skip = get_skip(page, size)
    # agrupando por data_movimento e somando o valor
    faturamentos = (
        session.query(
            Faturamentos.data_movimento,
            func.sum(Faturamentos.valor_total).label("total_dia")
        )
        .filter(Faturamentos.empresa_id == empresa_id)
        .filter(Faturamentos.data_movimento.between(new_data_inicial, new_data_final))
        .group_by(Faturamentos.data_movimento)
        .order_by(Faturamentos.data_movimento)
        .all()
    )
    # if not faturamentos:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Não foram encontrados faturamentos para a referida empresa no período especificado"
    #     )
    # total do período
    total_periodo = sum(r.total_dia for r in faturamentos)
    # paginação
    query_paginada = faturamentos[skip: skip + size]
    # montar resposta
    dados = []
    for r in query_paginada:
        porcentagem = ((r.total_dia / total_periodo) * 100 if total_periodo else Decimal("0")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        dia_semana = obter_dia_semana(r.data_movimento)
        dados.append(
            {
                "data_movimento": r.data_movimento,
                "dia_semana": dia_semana,
                "total_dia": r.total_dia,
                "porcentagem": porcentagem
            }
        )
    return {
        "total_faturamento": total_periodo,
        "faturamentos": dados
    }

@revenue_router.get(
    "/listar/vendedor/{empresa_id}",
)
async def listar_faturamentos_vendedor(
    empresa_id: int,
    data_inicial: str,
    data_final: str,
    page: int = 0,
    size: int = 10,
    session: Session = Depends(pegar_sessao)
):
    new_data_inicial = converter_data(data_inicial)
    new_data_final = converter_data(data_final)

    skip = get_skip(page, size)

    # agrupando por vendedor e somando o valor
    total = func.sum(Faturamentos.valor_total).label("total_vendedor")
    faturamentos = (
        session.query(
            Faturamentos.vendedor_id,
            Usuarios_Integra.usuario,
            total,
        )
        .join(Usuarios_Integra, Faturamentos.vendedor_id == Usuarios_Integra.vendedor_id)
        .filter(Faturamentos.empresa_id == empresa_id)
        .filter(Faturamentos.data_movimento.between(new_data_inicial, new_data_final))
        .group_by(Faturamentos.vendedor_id, Usuarios_Integra.usuario)
        .order_by(total.desc())
        .all()
    )
    # if not faturamentos:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Não foram encontrados faturamentos para a referida empresa no período especificado"
    #     )
    # total do período
    total_periodo = sum(r.total_vendedor for r in faturamentos)
    # paginação
    query_paginada = faturamentos[skip: skip + size]
    # montar resposta
    dados = []
    for r in query_paginada:
        porcentagem = ((r.total_vendedor / total_periodo) * 100 if total_periodo else Decimal("0")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        dados.append(
            {
                "vendedor_id": r.vendedor_id,
                "usuario": r.usuario,
                "total_vendedor": r.total_vendedor,
                "porcentagem": porcentagem
            }
        )
    return {
        "total_faturamento": total_periodo,
        "faturamentos": dados
    }

@revenue_router.get(
    "/listar/condicao_pagamento/{empresa_id}",
)
async def listar_faturamentos_condicao_pagamento(
    empresa_id: int,
    data_inicial: str,
    data_final: str,
    page: int = 0,
    size: int = 10,
    session: Session = Depends(pegar_sessao)
):
    new_data_inicial = converter_data(data_inicial)
    new_data_final = converter_data(data_final)

    skip = get_skip(page, size)

    # agrupando por condicao_pagamento e somando o valor
    total = func.sum(Faturamentos.valor_total).label("total")
    faturamentos = (
        session.query(
            Faturamentos.condicao_pagamento_id,
            CondicoesPagamentos.nome,
            total,
        )
        .join(CondicoesPagamentos, Faturamentos.condicao_pagamento_id == CondicoesPagamentos.id)
        .filter(Faturamentos.empresa_id == empresa_id)
        .filter(CondicoesPagamentos.empresa_id == empresa_id)
        .filter(Faturamentos.data_movimento.between(new_data_inicial, new_data_final))
        .group_by(Faturamentos.condicao_pagamento_id, CondicoesPagamentos.nome)
        .order_by(total.desc())
        .all()
    )
    # if not faturamentos:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Não foram encontrados faturamentos para a referida empresa no período especificado"
    #     )
    # total do período
    total_periodo = sum(r.total for r in faturamentos)
    # paginação
    query_paginada = faturamentos[skip: skip + size]
    # montar resposta
    dados = []
    for r in query_paginada:
        porcentagem = ((r.total / total_periodo) * 100 if total_periodo else Decimal("0")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        dados.append(
            {
                "condicao_pagamento_id": r.condicao_pagamento_id,
                "nome": r.nome,
                "total": r.total,
                "porcentagem": porcentagem
            }
        )
    return {
        "total_faturamento": total_periodo,
        "faturamentos": dados
    }

@revenue_router.get(
    "/total/diario/{empresa_id}",
)
async def total_faturamentos_diario(
    empresa_id: int,
    data_inicial: str,
    data_final: str,
    session: Session = Depends(pegar_sessao)
):
    new_data_inicial = converter_data(data_inicial)
    new_data_final = converter_data(data_final)

    # agrupando por data_movimento e somando o valor
    faturamentos = (
        session.query(
            Faturamentos.data_movimento,
            func.sum(Faturamentos.valor_total).label("total_dia")
        )
        .filter(Faturamentos.empresa_id == empresa_id)
        .filter(Faturamentos.data_movimento.between(new_data_inicial, new_data_final))
        .group_by(Faturamentos.data_movimento)
        .order_by(Faturamentos.data_movimento)
        .all()
    )

    total_periodo = sum(r.total_dia for r in faturamentos) if faturamentos else 0

    return {
        "total_periodo": total_periodo
    }

@revenue_router.get(
    "/total/vendedor/{empresa_id}",
)
async def total_faturamentos_vendedor(
    empresa_id: int,
    data_inicial: str,
    data_final: str,
    session: Session = Depends(pegar_sessao)
):
    new_data_inicial = converter_data(data_inicial)
    new_data_final = converter_data(data_final)

    # agrupando por vendedor e somando o valor
    total = func.sum(Faturamentos.valor_total).label("total_vendedor")
    faturamentos = (
        session.query(
            Faturamentos.vendedor_id,
            Usuarios_Integra.usuario,
            total,
        )
        .join(Usuarios_Integra, Faturamentos.vendedor_id == Usuarios_Integra.vendedor_id)
        .filter(Faturamentos.empresa_id == empresa_id)
        .filter(Faturamentos.data_movimento.between(new_data_inicial, new_data_final))
        .group_by(Faturamentos.vendedor_id, Usuarios_Integra.usuario)
        .order_by(total.desc())
        .all()
    )

    total_periodo = sum(r.total_vendedor for r in faturamentos) if faturamentos else 0

    return {
        "total_periodo": total_periodo
    }

@revenue_router.get(
    "/total/condicao_pagamento/{empresa_id}",
)
async def total_faturamentos_condicao_pagamento(
    empresa_id: int,
    data_inicial: str,
    data_final: str,
    session: Session = Depends(pegar_sessao)
):
    new_data_inicial = converter_data(data_inicial)
    new_data_final = converter_data(data_final)

    # agrupando por condicao_pagamento e somando o valor
    total = func.sum(Faturamentos.valor_total).label("total")
    faturamentos = (
        session.query(
            Faturamentos.condicao_pagamento_id,
            CondicoesPagamentos.nome,
            total,
        )
        .join(CondicoesPagamentos, Faturamentos.condicao_pagamento_id == CondicoesPagamentos.id)
        .filter(Faturamentos.empresa_id == empresa_id)
        .filter(CondicoesPagamentos.empresa_id == empresa_id)
        .filter(Faturamentos.data_movimento.between(new_data_inicial, new_data_final))
        .group_by(Faturamentos.condicao_pagamento_id, CondicoesPagamentos.nome)
        .order_by(total.desc())
        .all()
    )

    total_periodo = sum(r.total for r in faturamentos) if faturamentos else 0

    return {
        "total_periodo": total_periodo
    }