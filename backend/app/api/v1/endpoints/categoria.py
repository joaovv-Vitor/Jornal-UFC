from typing import List
from fastapi import APIRouter, HTTPException, status, Depends

from app.core.database import SessionDep
from app.core.deps import CurrentUser
from app.models.usuario import RoleEnum
from app.schemas.categoria import CategoriaCreate, CategoriaRead
from app.services.categoria_service import CategoriaService

router = APIRouter()

# --- PUBLICO: Listar para preencher o Select do Frontend ---
@router.get("/", response_model=List[CategoriaRead])
def listar_categorias(session: SessionDep):
    """
    Lista todas as categorias. Usado para montar o menu e filtros.
    """
    service = CategoriaService(session)
    return service.listar_categorias()

# --- RESTRITO: Criar Categoria ---
@router.post("/", response_model=CategoriaRead, status_code=status.HTTP_201_CREATED)
def criar_categoria(
    categoria_in: CategoriaCreate,
    session: SessionDep,
    current_user: CurrentUser
):
    """
    Cria uma nova categoria. Apenas ADMIN ou PROFESSOR.
    """
    # Validação de Permissão (Exemplo)
    if current_user.role not in [RoleEnum.ADMIN, RoleEnum.PROFESSOR]:
        raise HTTPException(
            status_code=403, 
            detail="Apenas administradores podem criar categorias."
        )

    service = CategoriaService(session)
    return service.criar_categoria(nome=categoria_in.nome)

# --- RESTRITO: Deletar ---
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_categoria(
    id: int,
    session: SessionDep,
    current_user: CurrentUser
):
    if current_user.role not in [RoleEnum.ADMIN, RoleEnum.PROFESSOR]:
        raise HTTPException(status_code=403, detail="Sem permissão.")

    service = CategoriaService(session)
    service.deletar_categoria(id)
    return None