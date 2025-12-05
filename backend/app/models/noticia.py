from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .usuario import Usuario
    from .categoria import Categoria
    from .comentario import Comentario

# --- Curtidas em Notícias ---
class CurtidaNoticia(SQLModel, table=True):
    __tablename__ = "curtidas_noticias"

    # Chave primária composta (usuario + noticia) impede likes duplicados
    usuario_id: int = Field(foreign_key="usuarios.id", primary_key=True)
    noticia_id: int = Field(foreign_key="noticias.id", primary_key=True)
    criado_em: datetime = Field(default_factory=datetime.now)

    # Relacionamentos para facilitar a navegação
    usuario: "Usuario" = Relationship(back_populates="curtidas_noticias")
    noticia: "Noticia" = Relationship(back_populates="curtidas")

# Tabela associativa pode ficar aqui ou em um arquivo separado se preferir
class NoticiasTags(SQLModel, table=True):
    noticia_id: int | None = Field(default=None, foreign_key="noticias.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="tags.id", primary_key=True)

class Tag(SQLModel, table=True):
    __tablename__ = "tags"
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    slug: str = Field(unique=True)
    
    noticias: list["Noticia"] = Relationship(back_populates="tags", link_model=NoticiasTags)

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

    # Aspas para evitar importar Usuario e Categoria em tempo de execução
    autor: Optional["Usuario"] = Relationship(back_populates="noticias")
    categoria: Optional["Categoria"] = Relationship(back_populates="noticias")
    comentarios: list["Comentario"] = Relationship(back_populates="noticia")
    tags: list[Tag] = Relationship(back_populates="noticias", link_model=NoticiasTags)
    
    # --- NOVO RELACIONAMENTO ---
    curtidas: list["CurtidaNoticia"] = Relationship(back_populates="noticia")
    