from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from dependecies import pegar_sessao
from models.pre_venda_itens import PreVendaItens
from models.pre_vendas import PreVendas
from models.condicoes_pagamentos import CondicoesPagamentos
from models.pessoas import Pessoas
from models.itens import Itens
from schemas.pre_sale_schemas import PreVendaCreateSchema
from sqlalchemy import func
from decimal import Decimal, ROUND_HALF_UP
from utils.utils import converter_data, get_skip

pre_sale_router = APIRouter(prefix="/pre_vendas", tags=["pre_vendas"])

@pre_sale_router.get(
    "/listar/{empresa_id}",
)
async def listar_pre_vendas(
    empresa_id: int,
    data_inicial: str,
    data_final: str,
    vendedor_id: int = 0,
    page: int = 0,
    size: int = 10,
    session: Session = Depends(pegar_sessao)
):
    new_data_inicial = converter_data(data_inicial)
    new_data_final = converter_data(data_final)
    skip = get_skip(page, size)
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
            func.sum(PreVendaItens.valor_venda * PreVendaItens.quantidade).label("valor_total"),
            func.count(PreVendaItens.item_id).label("qtd_itens")
        )
        .filter(
            PreVendas.empresa_id == empresa_id,
            PreVendas.data_movimento.between(new_data_inicial, new_data_final)
        )
        # REMOVER O << OUTERJOIN >>, POIS A CONDIÇÃO DE PAGAMENTO É OBRIGATÓRIA NA PRÉ-VENDA, ENTÃO PODEMOS USAR JOIN NORMAL.
        # DEIXEI SOMENTE PARA TESTE.
        .outerjoin(
            CondicoesPagamentos,
            (CondicoesPagamentos.id == PreVendas.condicao_pagamento_id) &
            (CondicoesPagamentos.empresa_id == PreVendas.empresa_id)
        )
        .outerjoin(
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
    if vendedor_id and vendedor_id > 0:
        pre_vendas = pre_vendas.filter(PreVendas.vendedor_id == vendedor_id)

    # if not pre_vendas:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Não foram encontradas pré-vendas para a referida empresa no período especificado"
    #     )
    
    # total do período
    # total_periodo = sum(pv.valor_total for pv in pre_vendas)
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
                "qtd_itens": pv.qtd_itens
            }
        )
    return {
        # "total_pre_vendas": total_periodo,
        "pre_vendas": dados
    }

@pre_sale_router.get(
    "/itens/listar/{pre_venda_id}",
)
async def listar_pre_venda_itens(
    pre_venda_id: int,
    page: int = 0,
    size: int = 10,
    session: Session = Depends(pegar_sessao)
):
    if not pre_venda_id or pre_venda_id <= 0:
        return {}

    skip = get_skip(page, size)
    pre_vendas_itens = (
        session.query(
            PreVendas.destinatario_id,
            Pessoas.nome.label("destinatario_nome"),
            PreVendaItens.item_id,
            Itens.nome,
            PreVendaItens.sequencia,
            PreVendaItens.quantidade,
            Itens.preco_zero,
            PreVendaItens.valor_desconto,
            PreVendaItens.valor_promocao,
            PreVendaItens.valor_venda,
        )
        .filter(
            PreVendaItens.pre_venda_id == pre_venda_id,
        )
        .join(
            PreVendaItens,
            (PreVendas.id == PreVendaItens.pre_venda_id) &
            (PreVendas.empresa_id == PreVendaItens.empresa_id)
        )
        .join(
            Itens,
            (Itens.id == PreVendaItens.item_id)
        )
        .join(
            Pessoas,
            (Pessoas.id == PreVendas.destinatario_id)
        )
        .order_by(PreVendaItens.sequencia)
    )
    
    # paginação
    query_paginada = pre_vendas_itens[skip: skip + size]

    destinatario_id = 0
    destinatario_nome = ''
    
    # montando a resposta
    dados = []
    for pvi in query_paginada:
        destinatario_id = pvi.destinatario_id
        destinatario_nome = pvi.destinatario_nome

        if not destinatario_id or not destinatario_nome:
            destinatario_nome = "Destinatário não encontrado"

        desconto_porcentagem = ((pvi.valor_desconto / (pvi.preco_zero * pvi.quantidade)) * 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) if pvi.preco_zero > 0 else Decimal("0")
        dados.append(
            {
                "item_nome": pvi.nome,
                "sequencia": pvi.sequencia,
                "item_id": pvi.item_id,
                "quantidade": pvi.quantidade,
                "preco_zero": pvi.preco_zero,
                "valor_desconto": pvi.valor_desconto,
                "desconto_porcentagem": desconto_porcentagem,
                "valor_promocao": pvi.valor_promocao,
                "valor_venda": pvi.valor_venda,
            }
        )
    return {
        "destinatario_id": destinatario_id,
        "destinatario_nome": destinatario_nome,
        "itens": dados
    }

@pre_sale_router.get(
    "/destinatario/{pre_venda_id}",
)
async def obter_destinatario(
    pre_venda_id: int,
    session: Session = Depends(pegar_sessao)
):
    destinatario = (
        session.query(
            PreVendas.destinatario_id.label("id"),
            Pessoas.nome.label("nome"),
        )
        .join(
            Pessoas,
            Pessoas.id == PreVendas.destinatario_id
        )
        .filter(
            PreVendas.id == pre_venda_id,
        )
    ).first()

    if not destinatario:
        return {}

    return {
        "destinatario_id": destinatario.id,
        "destinatario_nome": destinatario.nome
    }

@pre_sale_router.get(
    "/condicoes_pagamento/{empresa_id}",
)
async def obter_condicoes_pagamento(
    empresa_id: int,
    session: Session = Depends(pegar_sessao)
):
    condicoes_pagamento = (
        session.query(
            CondicoesPagamentos.nome,
            CondicoesPagamentos.id,
            CondicoesPagamentos.dias,
            CondicoesPagamentos.vezes_max,
        )
        .filter(
            CondicoesPagamentos.empresa_id == empresa_id,
            CondicoesPagamentos.ativo == True
        )
    ).all()

    if not condicoes_pagamento:
        return {}
    
    dados = []
    for cp in condicoes_pagamento:
        dados.append({
            "id": cp.id,
            "nome": cp.nome,
            "dias": cp.dias,
            "vezes_max": cp.vezes_max
        })
    return dados
    

@pre_sale_router.get(
    "/total_periodo/{empresa_id}",
)
async def total_periodo(
    empresa_id: int,
    data_inicial: str,
    data_final: str,
    vendedor_id: int = 0,
    session: Session = Depends(pegar_sessao)
):
    new_data_inicial = converter_data(data_inicial)
    new_data_final = converter_data(data_final)
    
    total_periodo = (
        session.query(
            func.sum(PreVendaItens.valor_venda * PreVendaItens.quantidade).label("valor_total")
        )
        .select_from(PreVendas)
        .join(
            PreVendaItens,
            (PreVendaItens.pre_venda_id == PreVendas.id) &
            (PreVendaItens.empresa_id == PreVendas.empresa_id)
        )
        .filter(
            PreVendas.empresa_id == empresa_id,
            PreVendas.data_movimento.between(new_data_inicial, new_data_final)
        )
    )

    if vendedor_id and vendedor_id > 0:
        total_periodo = total_periodo.filter(PreVendas.vendedor_id == vendedor_id)
    
    total_periodo = total_periodo.scalar() or Decimal(0)

    return {
        "total_periodo": total_periodo
    }

@pre_sale_router.post("/inserir")
async def inserir_pre_venda(
    dados: PreVendaCreateSchema,
    session: Session = Depends(pegar_sessao)
):
    # buscando o último id da pré-venda para a empresa e incrementa em 1 para criar o novo id
    ultimo_id = session.query(func.max(PreVendas.id)).filter(PreVendas.empresa_id == dados.empresa_id).scalar()
    novo_id = (ultimo_id or 0) + 1

    # valor_desconto_total = sum(item.valor_desconto for item in dados.itens) * dados.desconto_geral

    # cria a pre venda
    pre_venda = PreVendas(
        empresa_id=dados.empresa_id,
        id=novo_id,
        destinatario_id=dados.destinatario_id,
        vendedor_id=dados.vendedor_id,
        condicao_pagamento_id=dados.condicao_pagamento_id,
        data_registro=date.today(),
        data_movimento=date.today(),
        numero=dados.numero,
        disk_entrega=dados.disk_entrega,
        enviado=dados.enviado,
        observacao=dados.observacao,
        ide_mobile=dados.ide_mobile,
        qtd_vezes=dados.qtd_vezes,
    )

    session.add(pre_venda) # precisa adicionar a pré-venda antes de inserir os itens para obter o id da pré-venda
    session.flush() # para garantir que o id da pré-venda seja gerado antes de inserir os itens

    valor_total = Decimal(0)

    # inserindo os itens
    for item in dados.itens:

        valor_item = item.valor_venda * item.quantidade
        valor_total += Decimal(str(valor_item))

        pre_venda_item = PreVendaItens(
            empresa_id=dados.empresa_id,
            pre_venda_id=pre_venda.id,
            sequencia=item.sequencia,
            item_id=item.item_id,
            quantidade=item.quantidade,
            valor_venda=item.valor_venda,
            valor_promocao=item.valor_promocao,
            valor_desconto=item.valor_desconto,
        )

        session.add(pre_venda_item)

    pre_venda.valor_total = valor_total

    session.commit()

    return {
        "mensagem": "Pré venda inserida com sucesso",
        "pre_venda_id": pre_venda.id,
        "valor_total": valor_total
    }

@pre_sale_router.put("/editar/{empresa_id}/{pre_venda_id}")
async def editar_pre_venda(
    empresa_id: int,
    pre_venda_id: int,
    dados: PreVendaCreateSchema,
    session: Session = Depends(pegar_sessao)
):
    pre_venda = session.query(PreVendas).filter(
        PreVendas.empresa_id == empresa_id,
        PreVendas.id == pre_venda_id
    ).first()

    if not pre_venda:
        raise HTTPException(status_code=404, detail="Pré venda não encontrada")

    # atualiza cabeçalho
    pre_venda.destinatario_id = dados.destinatario_id
    pre_venda.vendedor_id = dados.vendedor_id
    pre_venda.condicao_pagamento_id = dados.condicao_pagamento_id
    pre_venda.numero = dados.numero
    pre_venda.disk_entrega = dados.disk_entrega
    pre_venda.enviado = dados.enviado
    pre_venda.observacao = dados.observacao
    pre_venda.ide_mobile = dados.ide_mobile
    pre_venda.qtd_vezes = dados.qtd_vezes
    pre_venda.data_movimento = date.today()

    # remove itens antigos
    session.query(PreVendaItens).filter(
        PreVendaItens.empresa_id == empresa_id,
        PreVendaItens.pre_venda_id == pre_venda_id
    ).delete()

    valor_total = Decimal(0)

    # insere novos itens
    for item in dados.itens:

        valor_item = item.valor_venda * item.quantidade
        valor_total += Decimal(str(valor_item))

        novo_item = PreVendaItens(
            empresa_id=empresa_id,
            pre_venda_id=pre_venda_id,
            sequencia=item.sequencia,
            item_id=item.item_id,
            quantidade=item.quantidade,
            valor_venda=item.valor_venda,
            valor_promocao=item.valor_promocao,
            valor_desconto=item.valor_desconto
        )
        session.add(novo_item)

    pre_venda.valor_total = valor_total

    session.commit()

    return {
        "mensagem": "Pré venda atualizada com sucesso",
        "pre_venda_id": pre_venda_id,
        "valor_total": valor_total
    }

@pre_sale_router.delete("/excluir/{empresa_id}/{pre_venda_id}")
async def excluir_pre_venda(
    empresa_id: int,
    pre_venda_id: int,
    session: Session = Depends(pegar_sessao)
):
    pre_venda = session.query(PreVendas).filter(
        PreVendas.empresa_id == empresa_id,
        PreVendas.id == pre_venda_id
    ).first()

    if not pre_venda:
        raise HTTPException(status_code=404, detail="Pré venda não encontrada")

    # remove os itens
    session.query(PreVendaItens).filter(
        PreVendaItens.empresa_id == empresa_id,
        PreVendaItens.pre_venda_id == pre_venda_id
    ).delete()

    # remove a pré-venda
    session.delete(pre_venda)

    session.commit()

    return {
        "mensagem": "Pré venda excluída com sucesso",
        "pre_venda_id": pre_venda_id
    }