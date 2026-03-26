from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from models.itens import Itens
from dependecies import pegar_sessao, verificar_token
from sqlalchemy.orm import Session
from schemas.pre_sale_schemas import VisualizarItensSchema
from utils.utils import get_skip

item_router = APIRouter(prefix="/itens", tags=["itens"])

@item_router.get("/listar/{empresa_id}", response_model=List[VisualizarItensSchema])
async def listar_itens(empresa_id: int, estoque_positivo: bool = Query(False), 
                       nome_item: str | None = Query(None, max_length=50), 
                       page: int = 0, size: int = 10, 
                       session: Session = Depends(pegar_sessao)):   
    
    skip = get_skip(page, size)
    # aplica o filtro para buscar itens da empresa especificada
    itens_query = (session.query(Itens).filter(Itens.empresa_id == empresa_id))
    # se o vender ativar a opção 'estoque_positivo', adiciona um filtro para buscar apenas itens cujo estoque seja maior que zero
    if estoque_positivo:
        itens_query = itens_query.filter(Itens.saldo_estoque > 0)
    # se o nome do item for fornecido, adiciona um filtro para buscar itens cujo nome contenha a string fornecida (case-insensitive)
    if nome_item and nome_item.strip():
        itens_query = itens_query.filter(Itens.nome.ilike(f"%{nome_item}%"))
    # aplica ordenação, paginação e executa a query
    itens = itens_query.order_by(Itens.nome).offset(skip).limit(size).all()
   
    # se a consulta não retornar nenhum item, lança uma exceção HTTP 400 com uma mensagem de erro
    # if not itens:
    #     raise HTTPException(status_code=400, detail="Não foram encontrados itens para a referida empresa (empresa_id)")
    # cada linha é uma tupla na ordem dos campos selecionados; empacotamos em dicionários
    return itens

@item_router.get("/{empresa_id}/{idItem}", response_model=Optional[VisualizarItensSchema])
async def get_item_by_Id(empresa_id: int, idItem: int = 0, 
                       session: Session = Depends(pegar_sessao)):   
    
    # aplica o filtro para buscar o item específico da empresa especificada
    item = session.query(Itens).filter(Itens.empresa_id == empresa_id, Itens.id == idItem).first()
    
    return item
