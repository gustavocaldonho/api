from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from dependecies import pegar_sessao
from models.pre_venda_itens import PreVendaItens
from models.pre_vendas import PreVendas
from models.condicoes_pagamentos import CondicoesPagamentos
from sqlalchemy import func

pre_sale_router = APIRouter(prefix="/pre_vendas", tags=["pre_vendas"])

@pre_sale_router.get(
    "/listar/{empresa_id}",
)
async def listar_faturamentos_diario(
    empresa_id: int,
    vendedor_id: int | None = Query(None),
    data_inicial: date = Query(..., description="Data inicial (YYYY-MM-DD)"),
    data_final: date = Query(..., description="Data final (YYYY-MM-DD)"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    session: Session = Depends(pegar_sessao)
):
    skip = (page - 1) * size
    pre_vendas = (
        session.query(
            PreVendas.id,
            PreVendas.condicao_pagamento_id,
            PreVendas.vendedor_id,
            CondicoesPagamentos.nome,
            PreVendas.data_registro,
            PreVendas.enviado,
            PreVendas.qtd_vezes,
            PreVendas.empresa_id,
            func.sum(PreVendaItens.valor_venda * PreVendaItens.quantidade).label("valor_total")
        )
        .filter(
            PreVendas.empresa_id == empresa_id,
            PreVendas.data_movimento.between(data_inicial, data_final)
        )
        .join(
            CondicoesPagamentos,
            (CondicoesPagamentos.id == PreVendas.condicao_pagamento_id) &
            (CondicoesPagamentos.empresa_id == PreVendas.empresa_id)
        )
        .join(
            PreVendaItens,
            (PreVendaItens.pre_venda_id == PreVendas.id) &
            (PreVendaItens.empresa_id == PreVendas.empresa_id)
        )
        .group_by(
            PreVendas.id,
            PreVendas.vendedor_id,
            PreVendas.condicao_pagamento_id,
            CondicoesPagamentos.nome,
            PreVendas.data_registro,
            PreVendas.enviado,
            PreVendas.qtd_vezes,
            PreVendas.empresa_id
        )
    )

    # se o usuário for o admin, ele pode ver todas as pré-vendas, caso contrário, ele só vê as pré-vendas associadas ao seu vendedor_id
    if vendedor_id:
        pre_vendas = pre_vendas.filter(PreVendas.vendedor_id == vendedor_id)

    if not pre_vendas:
        raise HTTPException(
            status_code=400,
            detail="Não foram encontradas pré-vendas para a referida empresa no período especificado"
        )
    
    # total do período
    total_periodo = sum(pv.valor_total for pv in pre_vendas)
    # paginação
    query_paginada = pre_vendas[skip: skip + size]
    # montando a resposta
    dados = []
    for pv in query_paginada:
        dados.append(
            {
                "pre_venda_id": pv.id,
                "vendedor_id": pv.vendedor_id,
                "condicao_pagamento_id": pv.condicao_pagamento_id,
                "nome_condicao_pagamento": pv.nome,
                "data_registro": pv.data_registro,
                "enviado": pv.enviado,
                "qtd_vezes": pv.qtd_vezes,
                "empresa_id": pv.empresa_id,
                "valor_total": pv.valor_total,  
            }
        )

    return {
        "total_pre_vendas": total_periodo,
        "pre_vendas": dados
    }