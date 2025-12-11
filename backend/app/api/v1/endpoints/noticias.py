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


# [US 03] - LISTAR (FEED)
@router.get("/", response_model=list[NoticiaRead])
def listar_feed(
    skip: int = 0, 
    limit: int = 10, 
    session: SessionDep = None
):
    """
    Feed de notícias público.
    """
    service = NoticiaService(session)
    return service.listar_noticias(skip, limit)

# [US 03] - DETALHES (POR SLUG)
@router.get("/{slug}", response_model=NoticiaRead)
def ver_noticia(slug: str, session: SessionDep):
    """
    Acessar notícia pela URL amigável.
    Ex: /noticias/nova-bolsa-2024
    """
    service = NoticiaService(session)
    noticia = service.buscar_por_slug(slug)
    
    if not noticia:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
        
    return noticia

# [US 06] - EXCLUIR
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_noticia(
    id: int, 
    session: SessionDep, 
    current_user: CurrentUser
):
    """
    Deleta uma notícia.
    Regra: Bolsista só apaga a sua. Professor apaga qualquer uma.
    """
    service = NoticiaService(session)
    noticia = service.buscar_por_id(id)

    if not noticia:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")

    # Regra de Permissão (ACL)
    if current_user.role == RoleEnum.BOLSISTA and noticia.autor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você só pode excluir suas próprias notícias.")
    
    if current_user.role == RoleEnum.LEITOR:
        raise HTTPException(status_code=403, detail="Sem permissão.")

    service.deletar_noticia(noticia)
    return None

# [US 05] - EDITAR
@router.patch("/{id}", response_model=NoticiaRead)
def editar_noticia(
    id: int,
    # Campos opcionais (Form)
    titulo: Optional[str] = Form(None),
    conteudo: Optional[str] = Form(None),
    subtitulo: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    imagem: Optional[UploadFile] = File(None),
    
    session: SessionDep = None,
    current_user: CurrentUser = None
):
    """
    Atualiza uma notícia (texto ou imagem).
    """
    service = NoticiaService(session)
    noticia = service.buscar_por_id(id)

    if not noticia:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")

    # Regra de Permissão
    if current_user.role == RoleEnum.BOLSISTA and noticia.autor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você só pode editar suas próprias notícias.")
    
    if current_user.role == RoleEnum.LEITOR:
        raise HTTPException(status_code=403, detail="Sem permissão.")

    noticia_atualizada = service.atualizar_noticia(
        noticia_db=noticia,
        titulo=titulo,
        conteudo=conteudo,
        subtitulo=subtitulo,
        tags_str=tags,
        imagem=imagem
    )
    
    return noticia_atualizada