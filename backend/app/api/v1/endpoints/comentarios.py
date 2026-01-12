from typing import List
from fastapi import APIRouter, HTTPException, status, Depends

from app.core.database import SessionDep
from app.core.deps import CurrentUser
from app.schemas.comentario import ComentarioCreate, ComentarioRead
from app.services.comentario_service import ComentarioService
from app.services.noticia_service import NoticiaService # Para verificar dono da notícia

router = APIRouter()

# --- [US 08] LISTAR COMENTÁRIOS DE UMA NOTÍCIA ---
# GET /noticias/{id}/comentarios
@router.get("/noticia/{noticia_id}", response_model=List[ComentarioRead])
def listar_comentarios_da_noticia(
    noticia_id: int,
    session: SessionDep
):
    """
    Lista comentários públicos de uma notícia.
    Não exibe comentários ocultos.
    """
    service = ComentarioService(session)
    return service.listar_por_noticia(noticia_id=noticia_id, incluir_ocultos=False)


# --- [US 08] COMENTAR ---
# POST /noticias/{id}/comentarios
@router.post("/noticia/{noticia_id}", response_model=ComentarioRead, status_code=status.HTTP_201_CREATED)
def comentar_noticia(
    noticia_id: int,
    comentario_in: ComentarioCreate,
    session: SessionDep,
    current_user: CurrentUser
):
    """
    Usuário autenticado comenta em uma notícia.
    """
    # Verifica se a notícia existe
    noticia_service = NoticiaService(session)
    if not noticia_service.buscar_por_id(noticia_id):
        raise HTTPException(status_code=404, detail="Notícia não encontrada")

    service = ComentarioService(session)
    return service.criar_comentario(
        conteudo=comentario_in.conteudo,
        usuario_id=current_user.id,
        noticia_id=noticia_id
    )


# --- [US 08] EXCLUIR PRÓPRIO COMENTÁRIO ---
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_comentario(
    id: int,
    session: SessionDep,
    current_user: CurrentUser
):
    """
    Autor do comentário pode excluir o próprio.
    """
    service = ComentarioService(session)
    comentario = service.buscar_por_id(id)

    if not comentario:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")

    # Regra: Só o dono do comentário pode apagar
    if comentario.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você só pode apagar seus próprios comentários.")

    service.deletar_comentario(comentario)
    return None


# --- [US 11] OCULTAR COMENTÁRIO (Autor da Notícia) ---
@router.patch("/{id}/ocultar", response_model=ComentarioRead)
def ocultar_comentario(
    id: int,
    session: SessionDep,
    current_user: CurrentUser
):
    """
    Apenas o AUTOR DA NOTÍCIA pode ocultar comentários nela.
    """
    service = ComentarioService(session)
    comentario = service.buscar_por_id(id)

    if not comentario:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")

    # Verifica a notícia associada para ver quem é o dono
    # Precisamos carregar a noticia (SQLModel usually lazy loads, but safe to fetch via service or attribute check)
    # Como definimos relationship no model, podemos acessar comentario.noticia se estiver carregado,
    # mas para garantir, vamos buscar a notícia.
    
    noticia_service = NoticiaService(session)
    noticia = noticia_service.buscar_por_id(comentario.noticia_id)

    if not noticia:
        raise HTTPException(status_code=404, detail="Notícia associada não encontrada")

    # Regra: Só o autor da notícia pode ocultar
    if noticia.autor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Apenas o autor da notícia pode ocultar comentários.")

    return service.ocultar_comentario(comentario)