from fastapi import APIRouter, Depends, HTTPException
from models.pessoas import Pessoas
from models.usuarios_integra import Usuarios_Integra
from dependecies import pegar_sessao, verificar_token
from schemas import VisualizarClientesSchema
from sqlalchemy.orm import Session
from typing import List

client_router = APIRouter(prefix="/client", tag=["client"])
    
@client_router.get("/visualizar_clientes/{empresa_id}", response_model=List[VisualizarClientesSchema])
async def visualizar_clientes(empresa_id: int, usuario: Usuarios_Integra = Depends(verificar_token),
                              session: Session = Depends(pegar_sessao)):
    # verifica se o vendedor possui autorização para consultar os dados dos clientes
    if not usuario.consultar_pessoas:
        raise HTTPException(status_code=401, detail="Você não tem autorização para consultar os clientes")
    # se o vendedor possuir autorização, ele consulta os clientes
    clientes = session.query(Pessoas).filter(Pessoas.empresa_id==empresa_id).all()
    if not clientes:
        raise HTTPException(status_code=400, detail="Não foram encontrados clientes para o referido empresa_id")
    else:
        return clientes