from fastapi import FastAPI
from app.models import *
from app.core.database import create_db_and_tables
from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(title="Lide API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    # Isso cria as tabelas no banco se elas não existirem
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "API rodando com SQLModel e Python 3.12"}


app.include_router(api_router, prefix=settings.API_V1_STR) # /api/v1