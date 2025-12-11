from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.noticia import Noticia

# Tabela Associativa
class NoticiasTags(SQLModel, table=True):
    __tablename__ = "noticias_tags"
    noticia_id: int | None = Field(default=None, foreign_key="noticias.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="tags.id", primary_key=True)

# Model de Tag
class Tag(SQLModel, table=True):
    __tablename__ = "tags"
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(unique=True)
    slug: str = Field(unique=True)
    
    # "Noticia" em string para evitar erro de importação circular
    noticias: List["Noticia"] = Relationship(back_populates="tags", link_model=NoticiasTags)