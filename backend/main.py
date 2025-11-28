from fastapi import FastAPI
from app.core.database import create_db_and_tables

app = FastAPI(title="Lide API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    # Isso cria as tabelas no banco se elas não existirem
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "API rodando com SQLModel e Python 3.12"}