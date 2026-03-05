from fastapi import APIRouter, Depends, HTTPException, Query
from models.recebimentos import Recebimentos
from dependecies import pegar_sessao
from schemas import RecebimentosListSchema
from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal

receipt_router = APIRouter(prefix="/recebimentos", tags=["recebimentos"])

receipt_router.get("/listar_recebimentos/{empresa_id}", response_model=RecebimentosListSchema)
async def listar_recebimentos(empresa_id: int, 
                              data_inicial: date = Query(..., description="Data inicial (YYYY-MM-DD)"),
                              data_final: date = Query(..., description="Data final (YYYY-MM-DD)"),
                              page: int = Query(1, ge=1), 
                              size: int = Query(10, ge=1, le=100), 
                              session: Session = Depends(pegar_sessao)):
    skip = (page-1)*size
    recebimentos_query = (session.query(Recebimentos).filter(Recebimentos.empresa_id == empresa_id))

    if data_inicial and data_final:
        recebimentos_query = recebimentos_query.filter(Recebimentos.data_movimento.between(data_inicial, data_final))

    recebimentos = recebimentos_query.order_by(Recebimentos.data_movimento.desc()).offset(skip).limit(size).all()
    if not recebimentos:
        raise HTTPException(status_code=400, detail="Não foram encontrados recebimentos para a referida empresa (empresa_id) no período especificado")
    
    total_recebimentos = Decimal(0)
    for r in recebimentos:
        total_recebimentos += r.valor

    return RecebimentosListSchema(recebimentos=recebimentos, total_recebimentos=total_recebimentos)