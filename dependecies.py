from models import db
from sqlalchemy.orm import sessionmaker

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session() # generator
        yield session # pega a sessao e retorna sem encerrar a funcao, porque precisa encessar a sessao
    finally:
        session.close()