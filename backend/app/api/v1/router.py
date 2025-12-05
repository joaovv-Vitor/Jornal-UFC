from fastapi import APIRouter
from app.api.v1.endpoints import noticias #, usuarios, tags # Importa seus arquivos

api_router = APIRouter()

# Aqui você registra cada "fatia" da sua API
api_router.include_router(noticias.router, prefix="/noticias", tags=["noticias"])
# api_router.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
# api_router.include_router(tags.router, prefix="/tags", tags=["tags"])