from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Header
from jose import jwt, JWTError
from sqlmodel import select

from app.core.database import SessionDep
from app.core.deps import CurrentUser
from app.core.config import settings
from app.models.usuario import RoleEnum, Usuario
from app.schemas.comentario import ComentarioCreate, ComentarioRead
from app.services.comentario_service import ComentarioService
from app.services.noticia_service import NoticiaService

router = APIRouter()

# --- HELPER PARA TOKEN OPCIONAL ---
def get_optional_user(session: SessionDep, authorization: str) -> Optional[Usuario]:
    """Extrai usuário se o token existir e for válido, senão retorna None."""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if email:
            return session.exec(select(Usuario).where(Usuario.email == email)).first()
    except (JWTError, Exception):
        return None
    return None

# --- [US 08] LISTAR COMENTÁRIOS ---
@router.get("/noticia/{noticia_id}", response_model=List[ComentarioRead])
def listar_comentarios_da_noticia(
    noticia_id: int,
    session: SessionDep,
    authorization: Optional[str] = Header(None)
):
    service = ComentarioService(session)
    user = get_optional_user(session, authorization)
    
    # Define se mostra ocultos: Se for ADMIN, PROFESSOR ou BOLSISTA
    incluir_ocultos = False
    if user and user.role in [RoleEnum.PROFESSOR, RoleEnum.BOLSISTA, RoleEnum.ADMIN]:
        incluir_ocultos = True
        
    return service.listar_por_noticia(noticia_id=noticia_id, incluir_ocultos=incluir_ocultos)

# --- [US 08] COMENTAR ---
@router.post("/noticia/{noticia_id}", response_model=ComentarioRead, status_code=status.HTTP_201_CREATED)
def comentar_noticia(
    noticia_id: int,
    comentario_in: ComentarioCreate,
    session: SessionDep,
    current_user: CurrentUser # Aqui o token é OBRIGATÓRIO
):
    noticia_service = NoticiaService(session)
    if not noticia_service.buscar_por_id(noticia_id):
        raise HTTPException(status_code=404, detail="Notícia não encontrada")

    service = ComentarioService(session)
    return service.criar_comentario(
        conteudo=comentario_in.conteudo,
        usuario_id=current_user.id,
        noticia_id=noticia_id
    )

# --- [US 11] OCULTAR/DESOCULTAR (Unificado para clareza) ---
@router.patch("/{id}/{acao}", response_model=ComentarioRead)
def moderar_comentario(
    id: int,
    acao: str, # "ocultar" ou "desocultar"
    session: SessionDep,
    current_user: CurrentUser
):
    if acao not in ["ocultar", "desocultar"]:
        raise HTTPException(status_code=400, detail="Ação inválida")

    service = ComentarioService(session)
    comentario = service.buscar_por_id(id)
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")

    noticia = NoticiaService(session).buscar_por_id(comentario.noticia_id)
    
    is_publisher = current_user.role in [RoleEnum.PROFESSOR, RoleEnum.BOLSISTA, RoleEnum.ADMIN]
    is_autor_noticia = noticia.autor_id == current_user.id

    if acao == "ocultar":
        if not (is_publisher or is_autor_noticia):
            raise HTTPException(status_code=403, detail="Sem permissão para ocultar.")
        return service.ocultar_comentario(comentario)
    
    if acao == "desocultar":
        if not is_publisher:
            raise HTTPException(status_code=403, detail="Apenas editores podem desocultar.")
        return service.desocultar_comentario(comentario)

# --- [US 08] EXCLUIR ---
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_comentario(id: int, session: SessionDep, current_user: CurrentUser):
    service = ComentarioService(session)
    comentario = service.buscar_por_id(id)

    if not comentario or comentario.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="Não permitido.")

    service.deletar_comentario(comentario)
    return None