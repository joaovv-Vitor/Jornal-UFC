# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine
from sqlmodel import SQLModel

# Importar modelos para que o SQLModel os reconheça ao criar o banco
from app import models
from app.api.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria as tabelas no banco de dados ao iniciar
    # Em produção, recomenda-se usar Alembic para migrações
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

@app.get("/")
def root():
    return {"message": "API do Jornal UFC está rodando!", "docs": "/docs"}

app.include_router(api_router, prefix=settings.API_V1_STR)