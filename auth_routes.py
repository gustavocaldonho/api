from fastapi import APIRouter, Depends, HTTPException
from models.models import Usuario
from models.empresas import Empresas
from models.usuarios_integra import Usuarios_Integra
from dependecies import pegar_sessao, verificar_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema, ResponseVisualizarVendedoresSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado

def autenticar_usuario(empresa_id_param, usuario_param, senha_param, session):
    usuario = session.query(Usuarios_Integra).filter(Usuarios_Integra.empresa_id==empresa_id_param, 
                                                     Usuarios_Integra.usuario==usuario_param).first()
    if not usuario:
        return False
    # elif not bcrypt_context.verify(senha, usuario.senha):
    elif not usuario.senha == senha_param: # verifica se a senha passada é igual a senha que esta no db. Retorna True ou False
        return False
    return usuario

@auth_router.get("/")
async def home():
    """
    Essa é a rota padrão de autenticação do nosso sistema.
    """
    return {"mensagem": "Você acessou a rota padrão de autenticação", "autenticado": False}

@auth_router.get("/cnpj/visualizar_vendedores/{cnpj}", response_model=ResponseVisualizarVendedoresSchema)
async def visualizar_vendedores(cnpj_empresa: str, session: Session = Depends(pegar_sessao)):
    # busca as informacoes da empresa no banco
    empresa = session.query(Empresas).filter(Empresas.empresa_cnpj==cnpj_empresa).first() # retorna uma linha do banco de dados com todas as informações da empresa
    # verifica se existe a empresa e se tem o aplicativo habilitado
    if not empresa:
        raise HTTPException(status_code=400, detail="CNPJ não encontrado")
    elif not empresa.celular_ativo:
        raise HTTPException(status_code=400, detail="O aplicativo não está habilitado para a referida empresa")
    else:
        # retorna a lista de vendedores da empresa
        vendedores = session.query(Usuarios_Integra).filter(Usuarios_Integra.empresa_id==empresa.id).all()
        return {
            "id_empresa": empresa.id,
            "vendedores": vendedores
        }

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first() # consulta no db
    if usuario:
        # ja existe um usuario com esse email
        # return {"mensagem": "já existe um usuário com esse email"}
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")
    else:
        senha_cryptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_cryptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"usuário cadastrado com sucesso {usuario_schema.email}"}
    
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.empresa_id, login_schema.usuario, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.vendedor_id)
        refresh_token = criar_token(usuario.vendedor_id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token, # apos 7 dias pede email e senha de novo
            "token_type": "Bearer"
        } 

# rota para permitir testar as rotas com cadeado diretamente na docs do fastapi, uma vez que toda rota com cadeado exige um token 
# no header (Authorization) e, esse header não é possível colocar diretamente na docs
@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        } 
    
@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,   
        "token_type": "Bearer"
    }     