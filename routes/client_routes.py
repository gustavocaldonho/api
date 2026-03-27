from fastapi import APIRouter, Depends, HTTPException, Query
from models.pessoas import Pessoas
from models.enderecos import Enderecos
from models.bairros import Bairros
from models.cidades import Cidades
from models.pessoa_contatos import PessoaContatos
from dependecies import pegar_sessao, verificar_token
from schemas.client_schemas import visualizarPerfilClienteSchema, visualizarResumoClienteSchema
from sqlalchemy.orm import Session
from typing import List
from utils.utils import get_skip

client_router = APIRouter(prefix="/clientes", tags=["clientes"])

@client_router.get("/listar/{empresa_id}", response_model=List[visualizarResumoClienteSchema])
async def listar_clientes(empresa_id: int, nome_cliente: str | None = Query(None, max_length=50), 
                          page: int = 0, size: int = 10, 
                          session: Session = Depends(pegar_sessao)):
    # usuario: Usuarios_Integra = Depends(verificar_token)
    # Query(valor_padrao, greater_or_equal 'ge' (maior ou igual), less_than_or_equal 'le' (menor ou igual))

    # verifica se o usuário (vendedor) possui autorização para consultar os dados dos clientes
    #if not usuario.consultar_pessoas:
    #    raise HTTPException(status_code=401, detail="Você não tem autorização para consultar os clientes")

    skip = get_skip(page, size)

    # construir a query única com joins e filtros aplicados
    clientes_query = (
        session.query(
            Pessoas.id,
            Pessoas.nome,
            Pessoas.limite_credito,
            Enderecos.logradouro,
            Enderecos.numero,
            Enderecos.complemento,
            Enderecos.cep,
            Enderecos.ponto_referencia,
            Bairros.nome.label("bairro"),
            Cidades.nome.label("cidade"),
            Cidades.uf,
        )
        .outerjoin(Enderecos, Enderecos.pessoa_id == Pessoas.id)
        .outerjoin(Bairros, Bairros.id == Enderecos.bairro_id)
        .outerjoin(Cidades, Cidades.id == Enderecos.cidade_id)
        .filter(Pessoas.empresa_id == empresa_id)
        # .filter(Enderecos.sequencia == 1) # garante que pegue apenas o endereço principal (sequencia 1)
    )
    # se o nome do cliente for fornecido, adiciona um filtro para buscar clientes cujo nome contenha a string fornecida (case-insensitive)
    if nome_cliente and nome_cliente.strip():
        clientes_query = clientes_query.filter(Pessoas.nome.ilike(f"%{nome_cliente}%"))
    
    # se o nome do cliente não for fornecido, a consulta retornará todos os clientes da empresa ordenados por nome, paginados de acordo com os parâmetros 'page' e 'size'
    clientes = clientes_query.order_by(Pessoas.nome).offset(skip).limit(size).all()
    
    # se a consulta não retornar nenhum cliente, lança uma exceção HTTP 400 com uma mensagem de erro
    # if not clientes:
    #     raise HTTPException(status_code=400, detail="Não foram encontrados clientes para a referida empresa (empresa_id)")

    # se não forem achado cliente, retoanr uma lista vazia ao invés de lançar uma exceção, para facilitar o tratamento no frontend
    return clientes

@client_router.get("/listar/informacoes_perfil/{empresa_id}/{pessoa_id}", response_model=visualizarPerfilClienteSchema)
async def obter_informacoes_perfil_clientes(empresa_id: int, pessoa_id: int, session: Session = Depends(pegar_sessao)):

    cliente_query = (
        session.query(
            Pessoas.nome,
            Pessoas.qtd_dupl_pagas,
            Pessoas.qtd_dupl_atrasadas,
            Pessoas.qtd_dupl_avencer,
            Pessoas.total_pago,
            Pessoas.total_atrasado,
            Pessoas.total_avencer,
            (Pessoas.total_atrasado + Pessoas.total_avencer).label("total_aberto"),
            Pessoas.dias_maior_atraso,
            Pessoas.dias_maior_avencer,
            Pessoas.limite_credito,
        )
        .filter(Pessoas.empresa_id == empresa_id, 
                Pessoas.id == pessoa_id)
    ).first()

    # se a consulta não retornar nenhum cliente, lança uma exceção HTTP 400 com uma mensagem de erro
    if not cliente_query:
        raise HTTPException(status_code=400, detail="Cliente não encontrado para a referida empresa (empresa_id) e pessoa_id")
    
    telefones_query = (
        session.query(PessoaContatos.contato)
        .filter(PessoaContatos.empresa_id == empresa_id, 
                PessoaContatos.pessoa_id == pessoa_id)
        .order_by(PessoaContatos.sequencia) # ordena os contatos pela sequência para garantir que o contato principal (sequencia 1) venha primeiro
        .all()
    )

    enderecos_query = (
        session.query(
            Enderecos.logradouro,
            Enderecos.numero,
            Enderecos.complemento,
            Enderecos.cep,
            Enderecos.ponto_referencia,
            Bairros.nome.label("bairro"),
            Cidades.nome.label("cidade"),
            Cidades.uf
        )
        .outerjoin(Bairros, Bairros.id == Enderecos.bairro_id)
        .outerjoin(Cidades, Cidades.id == Enderecos.cidade_id)
        .filter(Enderecos.pessoa_id == pessoa_id)
        .order_by(Enderecos.sequencia) # ordena os endereços pela sequência para garantir que o endereço principal (sequencia 1) venha primeiro
        .all()
    )

    return {
        **cliente_query._asdict(),
        "telefones": telefones_query,
        "enderecos": enderecos_query
    }

@client_router.get("/{empresa_id}/{idCliente}")
async def get_cliente_by_Id(empresa_id: int, idCliente: int = 0, 
                       session: Session = Depends(pegar_sessao)):   
    
    # aplica o filtro para buscar o item específico da empresa especificada
    cliente = session.query(Pessoas).filter(Pessoas.empresa_id == empresa_id, Pessoas.id == idCliente).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    return cliente
