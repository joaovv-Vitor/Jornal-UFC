# app/core/database.py
from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings

# --- CORREÇÃO AQUI ---
# Mudamos de settings.SQLALCHEMY_DATABASE_URI para settings.DATABASE_URL
database_url = settings.DATABASE_URL

# Ajuste para o driver psycopg (caso a string venha apenas como postgresql://)
if database_url and database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://")

# Criação da Engine
engine = create_engine(database_url, echo=True)

# Função Geradora de Sessão
def get_session():
    with Session(engine) as session:
        yield session

# Injeção de Dependência
SessionDep = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)