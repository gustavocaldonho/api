from fastapi import APIRouter, Depends, HTTPException, Query
from models.pessoas import Pessoas
from models.usuarios_integra import Usuarios_Integra
from dependecies import pegar_sessao, verificar_token
from schemas import VisualizarClientesSchema
from sqlalchemy.orm import Session
from typing import List

client_router = APIRouter(prefix="/client", tags=["clientes"])

@client_router.get("/listar_clientes/{empresa_id}", response_model=List[VisualizarClientesSchema])
async def listar_clientes(empresa_id: int, nome_cliente: str | None = Query(None, min_length=3, max_length=50), 
                          page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), 
                          session: Session = Depends(pegar_sessao)):
    # usuario: Usuarios_Integra = Depends(verificar_token)
    # Query(valor_padrao, greater_or_equal 'ge' (maior ou igual), less_than_or_equal 'le' (menor ou igual))

    # verifica se o usuário (vendedor) possui autorização para consultar os dados dos clientes
    #if not usuario.consultar_pessoas:
    #    raise HTTPException(status_code=401, detail="Você não tem autorização para consultar os clientes")
    
    skip = (page-1)*size
    # se o vendedor possuir autorização, ele consulta os clientes
    query =  session.query(Pessoas).filter(Pessoas.empresa_id==empresa_id)
    # filtrando os clientes pelo nome se o usuário digitar
    if nome_cliente:
        query = query.filter(Pessoas.nome.ilike(f"%{nome_cliente}%"))
    # ordenando os nomes e aplicando a paginação
    clientes = query.order_by(Pessoas.nome).offset(skip).limit(size).all()
    if not clientes:
        raise HTTPException(status_code=400, detail="Não foram encontrados clientes para a referida empresa (empresa_id)")
    else:
        return clientes