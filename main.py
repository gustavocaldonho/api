from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
import models
from database import engine

load_dotenv() # carrega as variáveis de ambiente que estão em .env

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

# cria todas as tabelas no database
models.Base.metadata.create_all(bind=engine)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

from routes.auth_routes import auth_router
from routes.order_routes import order_router
from routes.client_routes import client_router
from routes.item_routes import item_router
from routes.receipt_routes import receipt_router
from routes.payment_routes import payment_router
from routes.revenue_routes import revenue_router
from routes.pre_sale_routes import pre_sale_router

# app.include_router(order_router)
app.include_router(auth_router)
app.include_router(client_router)
app.include_router(item_router)
app.include_router(receipt_router)
app.include_router(payment_router)
app.include_router(revenue_router)
app.include_router(pre_sale_router)