import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.database import engine
from sqlmodel import SQLModel

# Importar modelos
from app import models
from app.api.router import api_router

# Garante que a pasta static/images existe
os.makedirs("static/images", exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria as tabelas ao iniciar (idealmente Alembic em produção)
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

# --------------------------------------------------
# 🔥 **CORS — ESSENCIAL para permitir OPTIONS + POST**
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Em produção: coloque o domínio do frontend
    allow_credentials=True,
    allow_methods=["*"],          # <--- Permite OPTIONS, POST, GET etc.
    allow_headers=["*"],          # <--- Permite Content-Type, Authorization etc.
)

# ----------------------
# Rotas
# ----------------------
@app.get("/")
def root():
    return {"message": "API do Jornal UFC está rodando!", "docs": "/docs"}

# ----------------------
# Arquivos Estáticos (Imagens)
# ----------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router, prefix=settings.API_V1_STR)
