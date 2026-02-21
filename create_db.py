from models import db, Base

def criar_banco():
    # Cria todas as tabelas no banco
    Base.metadata.create_all(bind=db)
    print("Banco de dados criado com sucesso!")

if __name__ == "__main__":
    criar_banco()