from fastapi import APIRouter
from app.api.v1.endpoints import usuarios, auth#, #noticias

api_router = APIRouter()

api_router.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])

# --- ALTERAÇÃO AQUI ---
# Adicione prefix="/auth" para que as rotas fiquem:
# /api/v1/auth/login
# /api/v1/auth/verificar
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticação"]) 

#api_router.include_router(noticias.router, prefix="/noticias", tags=["Notícias"])