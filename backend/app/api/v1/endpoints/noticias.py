# app/api/endpoints/noticias.py
from typing import Optional
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form

from app.core.database import SessionDep
from app.core.deps import CurrentUser
from app.models.usuario import RoleEnum
from app.schemas.noticia import NoticiaRead
from app.services.noticia_service import NoticiaService # <--- Importe o Serviço

router = APIRouter()

@router.post("/", response_model=NoticiaRead, status_code=status.HTTP_201_CREATED)
def criar_noticia(
    titulo: str = Form(...),
    conteudo: str = Form(...),
    subtitulo: Optional[str] = Form(None),
    tags: str = Form(""),
    imagem: UploadFile = File(...),
    session: SessionDep = None, # SessionDep já injeta a sessão
    current_user: CurrentUser = None
):
    """
    Cria uma notícia com upload de imagem.
    """
    
    # 1. Validação de Permissão (Isso continua sendo resp. do Endpoint/Controller)
    if current_user.role == RoleEnum.LEITOR:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Leitores não podem publicar.")
    
    if current_user.role == RoleEnum.BOLSISTA and not current_user.orientador_id:
         raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Bolsista sem orientador não pode publicar.")

    # 2. Validação básica de arquivo (Controller)
    if imagem.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(400, detail="Apenas imagens JPG, PNG ou WEBP são permitidas.")

    # 3. Chama o Serviço para fazer o trabalho pesado
    service = NoticiaService(session)
    nova_noticia = service.criar_noticia(
        titulo=titulo,
        conteudo=conteudo,
        subtitulo=subtitulo,
        tags_str=tags,
        imagem=imagem,
        autor=current_user
    )
    
    return nova_noticia