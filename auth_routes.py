from fastapi import APIRouter
from models import Usuario, db
from sqlalchemy.orm import sessionmaker


auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    """
    Essa é a rota padrão de autenticação do nosso sistema.
    """
    return {"mensagem": "Você acessou a rota padrão de autenticação", "autenticado": False}

@auth_ruter.post("/criar_conta")
async def criar_conta(email: str, senha: str, nome: str):
    Session = session(bin=db)
    session = Session()
    usuario = session.query(Usuario).filter(Usuario.email==email).first() # consulta no db
    if usuario:
        # ja existe um usuario com esse email
        return {"mensagem": "já existe um usuário com esse email"}
    else:
        novo_usuario = Usuario(nome, email, senha)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "usuário cadastrado com sucesso"}