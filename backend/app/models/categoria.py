from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.noticia import Noticia

class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(unique=True, index=True)
    slug: str = Field(unique=True) # Para URLs amigáveis ex: /categoria/tecnologia

    # Relacionamento
    noticias: List["Noticia"] = Relationship(back_populates="categoria")