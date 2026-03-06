from fastapi import APIRouter, Depends, HTTPException, Query
from models.pessoas import Pessoas
from models.enderecos import Enderecos
from models.bairros import Bairros
from models.cidades import Cidades
from models.pessoa_contatos import PessoaContatos
from dependecies import pegar_sessao, verificar_token
from schemas import VisualizarClientesSchema
from sqlalchemy.orm import Session
from typing import List

client_router = APIRouter(prefix="/clientes", tags=["clientes"])

@client_router.get("/listar/{empresa_id}", response_model=List[VisualizarClientesSchema])
async def listar_clientes(empresa_id: int, nome_cliente: str | None = Query(None, min_length=3, max_length=50), 
                          page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), 
                          session: Session = Depends(pegar_sessao)):
    # usuario: Usuarios_Integra = Depends(verificar_token)
    # Query(valor_padrao, greater_or_equal 'ge' (maior ou igual), less_than_or_equal 'le' (menor ou igual))

    # verifica se o usuário (vendedor) possui autorização para consultar os dados dos clientes
    #if not usuario.consultar_pessoas:
    #    raise HTTPException(status_code=401, detail="Você não tem autorização para consultar os clientes")
    
    skip = (page-1)*size

    # construir a query única com joins e filtros aplicados
    clientes_query = (
        session.query(
            Pessoas.nome.label("nome_pessoa"),
            Pessoas.limite_credito,
            Enderecos.logradouro,
            Enderecos.numero,
            Enderecos.complemento,
            Enderecos.cep,
            Enderecos.ponto_referencia,
            Bairros.nome.label("bairro"),
            Cidades.nome.label("cidade"),
            Cidades.uf,
            PessoaContatos.contato
        )
        .outerjoin(Enderecos, Enderecos.pessoa_id == Pessoas.id)
        .outerjoin(Bairros, Bairros.id == Enderecos.bairro_id)
        .outerjoin(Cidades, Cidades.id == Enderecos.cidade_id)
        .outerjoin(PessoaContatos, (
            PessoaContatos.pessoa_id == Pessoas.id) 
            & (PessoaContatos.empresa_id == empresa_id) 
            & (PessoaContatos.sequencia == 1)) # join para pegar o contato principal do cliente (sequencia 1)
        .filter(Pessoas.empresa_id == empresa_id)
    )
    # se o nome do cliente for fornecido, adiciona um filtro para buscar clientes cujo nome contenha a string fornecida (case-insensitive)
    if nome_cliente:
        clientes_query = clientes_query.filter(Pessoas.nome.ilike(f"%{nome_cliente}%"))
    # aplica ordenação, paginação e executa a query
    clientes = clientes_query.order_by(Pessoas.nome).offset(skip).limit(size).all()
    # se a consulta não retornar nenhum cliente, lança uma exceção HTTP 400 com uma mensagem de erro
    if not clientes:
        raise HTTPException(status_code=400, detail="Não foram encontrados clientes para a referida empresa (empresa_id)")
    # cada linha é uma tupla na ordem dos campos selecionados; empacotamos em dicionários
    resultado = [
        {
            "nome_pessoa": nome_pessoa,
            "limite_credito": limite_credito,
            "logradouro": logradouro,
            "numero": numero,
            "complemento": complemento,
            "cep": cep,
            "ponto_referencia": ponto_referencia,
            "bairro": bairro,
            "cidade": cidade,
            "uf": uf,
            "contato": contato
        }
        for nome_pessoa, limite_credito, logradouro, numero, complemento, 
            cep, ponto_referencia, bairro, cidade, uf, contato 
            in clientes
    ]
    return resultado