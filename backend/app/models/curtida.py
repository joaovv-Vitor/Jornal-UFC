from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.usuario import Usuario
    from app.models.noticia import Noticia

class CurtidaNoticia(SQLModel, table=True):
    __tablename__ = "curtidas_noticias"
    
    usuario_id: int = Field(foreign_key="usuarios.id", primary_key=True)
    noticia_id: int = Field(foreign_key="noticias.id", primary_key=True)
    criado_em: datetime = Field(default_factory=datetime.now)

    usuario: "Usuario" = Relationship(back_populates="curtidas_noticias")
    noticia: "Noticia" = Relationship(back_populates="curtidas")