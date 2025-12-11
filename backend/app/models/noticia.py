# app/db/models/noticia.py
from typing import TYPE_CHECKING, Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.usuario import Usuario
    from app.models.categoria import Categoria
    from app.models.comentario import Comentario  # <--- Agora existe!

# --- Tabela Associativa (Noticias <-> Tags) ---
class NoticiasTags(SQLModel, table=True):
    noticia_id: int | None = Field(default=None, foreign_key="noticias.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="tags.id", primary_key=True)

# --- Model de Tag ---
class Tag(SQLModel, table=True):
    __tablename__ = "tags"
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(unique=True)
    slug: str = Field(unique=True)
    
    noticias: List["Noticia"] = Relationship(back_populates="tags", link_model=NoticiasTags)

# --- Curtidas em Notícias ---
class CurtidaNoticia(SQLModel, table=True):
    __tablename__ = "curtidas_noticias"
    usuario_id: int = Field(foreign_key="usuarios.id", primary_key=True)
    noticia_id: int = Field(foreign_key="noticias.id", primary_key=True)
    criado_em: datetime = Field(default_factory=datetime.now)

    usuario: "Usuario" = Relationship(back_populates="curtidas_noticias")
    noticia: "Noticia" = Relationship(back_populates="curtidas")

# --- Model Principal de Noticia ---
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

    autor_id: int | None = Field(default=None, foreign_key="usuarios.id")
    categoria_id: int | None = Field(default=None, foreign_key="categorias.id")

    # Relacionamentos
    autor: Optional["Usuario"] = Relationship(back_populates="noticias")
    categoria: Optional["Categoria"] = Relationship(back_populates="noticias") # <--- Conectado
    
    tags: List[Tag] = Relationship(back_populates="noticias", link_model=NoticiasTags)
    curtidas: List["CurtidaNoticia"] = Relationship(back_populates="noticia")
    comentarios: List["Comentario"] = Relationship(back_populates="noticia") # <--- Conectado