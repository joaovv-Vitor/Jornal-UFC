from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.noticia import Noticia

class NoticiaImagem(SQLModel, table=True):
    __tablename__ = "noticia_imagens"
    
    id: int | None = Field(default=None, primary_key=True)
    caminho: str 
    
    noticia_id: int = Field(foreign_key="noticias.id")
    noticia: "Noticia" = Relationship(back_populates="imagens_galeria")