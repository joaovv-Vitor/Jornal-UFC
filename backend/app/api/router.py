from fastapi import APIRouter
from app.api.v1.endpoints import usuarios, auth, noticias, categoria

api_router = APIRouter()

api_router.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticação"]) 
api_router.include_router(noticias.router, prefix="/noticias", tags=["Notícias"])
api_router.include_router(categoria.router, prefix="/categorias", tags=["Categorias"])