from fastapi import APIRouter
# Corrigido: 'usuarios' (plural) e removido o 'v1' se a pasta não existir
from app.api.v1.endpoints import usuarios 
# from app.api.endpoints import noticias # (Descomente quando criar o arquivo)

api_router = APIRouter()

# O prefixo "/usuarios" significa que as rotas serão: /api/v1/usuarios/
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])

# Futuras inclusões:
# api_router.include_router(noticias.router, prefix="/noticias", tags=["Noticias"])