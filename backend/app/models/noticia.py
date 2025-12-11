from typing import TYPE_CHECKING, Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

# --- IMPORTAÇÕES (RUNTIME) ---
# Importamos as classes reais para que o SQLModel saiba criar as relações no banco
from app.models.tag import Tag, NoticiasTags
from app.models.imagem import NoticiaImagem
from app.models.curtida import CurtidaNoticia

# --- IMPORTAÇÕES (TYPE CHECKING) ---
if TYPE_CHECKING:
    from app.models.usuario import Usuario
    from app.models.categoria import Categoria
    from app.models.comentario import Comentario 

class Noticia(SQLModel, table=True):
    __tablename__ = "noticias"

    id: int | None = Field(default=None, primary_key=True)
    titulo: str
    subtitulo: str | None = None
    conteudo: str
    slug: str = Field(unique=True, index=True)
    imagem_capa: str | None = None 
    publicado: bool = False
    publicado_em: datetime | None = None
    criado_em: datetime = Field(default_factory=datetime.now)
    atualizado_em: datetime = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)

    autor_id: int | None = Field(default=None, foreign_key="usuarios.id")
    categoria_id: int | None = Field(default=None, foreign_key="categorias.id")

    # --- RELACIONAMENTOS ---
    
    # Usuario e Categoria
    autor: Optional["Usuario"] = Relationship(back_populates="noticias")
    categoria: Optional["Categoria"] = Relationship(back_populates="noticias")
    
    # Tags (Many-to-Many)
    tags: List[Tag] = Relationship(back_populates="noticias", link_model=NoticiasTags)
    
    # Curtidas (Link Table explícita)
    curtidas: List[CurtidaNoticia] = Relationship(back_populates="noticia")
    
    # Comentários
    comentarios: List["Comentario"] = Relationship(back_populates="noticia")
    
    # Galeria (One-to-Many)
    imagens_galeria: List[NoticiaImagem] = Relationship(back_populates="noticia")