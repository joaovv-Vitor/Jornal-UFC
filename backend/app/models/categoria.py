from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .noticia import Noticia

class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"

    id: int | None = Field(default=None, primary_key=True)
    nome: str
    slug: str = Field(unique=True)

    noticias: list["Noticia"] = Relationship(back_populates="categoria")