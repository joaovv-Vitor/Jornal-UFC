# app/core/database.py
from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings

# Ajuste para psycopg (PostgreSQL Driver)
# Se sua URL já vier correta do .env, esse replace não quebra nada, mas garante segurança.
database_url = settings.SQLALCHEMY_DATABASE_URI
if database_url and database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://")

# Criação da Engine
engine = create_engine(database_url, echo=True)

# Função Geradora de Sessão
def get_session():
    with Session(engine) as session:
        yield session

# --- A PEÇA QUE FALTAVA ---
# SessionDep é um "apelido" (Type Alias) para a injeção de dependência.
# Toda vez que você usar SessionDep numa rota, o FastAPI executa get_session()
SessionDep = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)