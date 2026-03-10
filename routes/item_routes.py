from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from models.itens import Itens
from dependecies import pegar_sessao, verificar_token
from sqlalchemy.orm import Session
from schemas.pre_sale_schemas import VisualizarItensSchema

item_router = APIRouter(prefix="/itens", tags=["itens"])

@item_router.get("/listar/{empresa_id}", response_model=List[VisualizarItensSchema])
async def listar_itens(empresa_id: int, estoque_positivo: bool = Query(False), 
                       nome_item: str | None = Query(None, min_length=3, max_length=50), 
                       page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), 
                       session: Session = Depends(pegar_sessao)):   
    # usuario: Usuarios_Integra = Depends(verificar_token)
    # Query(valor_padrao, greater_or_equal 'ge' (maior ou igual), less_than_or_equal 'le' (menor ou igual))

    # verifica se o usuário (vendedor) possui autorização para consultar os dados dos itens
    #if not usuario.consultar_itens:
    #    raise HTTPException(status_code=401, detail="Você não tem autorização para consultar os itens")
    
    skip = (page-1)*size
    # aplica o filtro para buscar itens da empresa especificada
    itens_query = (session.query(Itens).filter(Itens.empresa_id == empresa_id))
    # se o vender ativar a opção 'estoque_positivo', adiciona um filtro para buscar apenas itens cujo estoque seja maior que zero
    if estoque_positivo:
        itens_query = itens_query.filter(Itens.saldo_estoque > 0)
    # se o nome do item for fornecido, adiciona um filtro para buscar itens cujo nome contenha a string fornecida (case-insensitive)
    if nome_item:
        itens_query = itens_query.filter(Itens.nome.ilike(f"%{nome_item}%"))
    # aplica ordenação, paginação e executa a query
    itens = itens_query.order_by(Itens.nome).offset(skip).limit(size).all()
    # se a consulta não retornar nenhum item, lança uma exceção HTTP 400 com uma mensagem de erro
    if not itens:
        raise HTTPException(status_code=400, detail="Não foram encontrados itens para a referida empresa (empresa_id)")
    # cada linha é uma tupla na ordem dos campos selecionados; empacotamos em dicionários
    return itens