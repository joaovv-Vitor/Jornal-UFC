from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form

from app.core.database import SessionDep
from app.core.deps import CurrentUser
from app.models.usuario import RoleEnum
from app.schemas.noticia import NoticiaRead
# Se você configurou o __init__.py em services, use assim:
from app.services import NoticiaService
# Se não configurou, use: from app.services.noticia_service import NoticiaService

router = APIRouter()

# --- [US 01] CRIAR NOTÍCIA ---
@router.post("/", response_model=NoticiaRead, status_code=status.HTTP_201_CREATED)
def criar_noticia(
    titulo: str = Form(...),
    conteudo: str = Form(...),
    subtitulo: Optional[str] = Form(None),
    tags: str = Form(""),
    categoria_id: Optional[int] = Form(None),
    imagem_capa: UploadFile = File(...),    # Obrigatório
    galeria: List[UploadFile] = File(None), # Opcional (Múltiplos arquivos)
    session: SessionDep = None,
    current_user: CurrentUser = None
):
    """
    Cria uma notícia com capa, categoria e galeria de fotos opcional.
    """
    
    # 1. Validação de Permissão
    if current_user.role == RoleEnum.LEITOR:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Leitores não podem publicar.")
    
    if current_user.role == RoleEnum.BOLSISTA and not current_user.orientador_id:
         raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Bolsista sem orientador não pode publicar.")

    # 2. Validação básica da Capa
    # Nota: Validar a galeria inteira pode ser custoso, mas validamos a capa que é essencial.
    if imagem_capa.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(400, detail="Apenas imagens JPG, PNG ou WEBP são permitidas na capa.")

    # 3. Execução
    service = NoticiaService(session)
    nova_noticia = service.criar_noticia(
        titulo=titulo,
        conteudo=conteudo,
        subtitulo=subtitulo,
        tags_str=tags,
        imagem_capa=imagem_capa,
        autor=current_user,
        categoria_id=categoria_id,
        galeria=galeria or [] # Garante que passe uma lista vazia se for None
    )
    
    return nova_noticia


# --- [US 03] LISTAR (FEED) ---
@router.get("/", response_model=List[NoticiaRead])
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


# --- [US 03] DETALHES (POR SLUG) ---
@router.get("/{slug}", response_model=NoticiaRead)
def ver_noticia(slug: str, session: SessionDep):
    """
    Acessar notícia pela URL amigável.
    """
    service = NoticiaService(session)
    noticia = service.buscar_por_slug(slug)
    
    if not noticia:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
        
    return noticia


# --- [US 06] EXCLUIR ---
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_noticia(
    id: int, 
    session: SessionDep, 
    current_user: CurrentUser
):
    service = NoticiaService(session)
    noticia = service.buscar_por_id(id)

    if not noticia:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")

    # Regras de Permissão
    if current_user.role == RoleEnum.BOLSISTA and noticia.autor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você só pode excluir suas próprias notícias.")
    
    if current_user.role == RoleEnum.LEITOR:
        raise HTTPException(status_code=403, detail="Sem permissão.")

    service.deletar_noticia(noticia)
    return None


# --- [US 05] EDITAR ---
@router.patch("/{id}", response_model=NoticiaRead)
def editar_noticia(
    id: int,
    titulo: Optional[str] = Form(None),
    conteudo: Optional[str] = Form(None),
    subtitulo: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    categoria_id: Optional[int] = Form(None),
    imagem_capa: Optional[UploadFile] = File(None),
    galeria: List[UploadFile] = File(None), # Adicionar fotos
    session: SessionDep = None,
    current_user: CurrentUser = None
):
    """
    Atualiza texto, capa ou adiciona fotos à galeria.
    """
    service = NoticiaService(session)
    noticia = service.buscar_por_id(id)

    if not noticia:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")

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
        categoria_id=categoria_id,
        imagem_capa=imagem_capa,
        galeria=galeria or [] # Proteção contra None
    )
    
    return noticia_atualizada